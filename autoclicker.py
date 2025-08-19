import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QDoubleSpinBox, 
                           QComboBox, QCheckBox, QLineEdit, QSpinBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
import json
import os

class ClickerThread(QThread):
    finished = pyqtSignal()
    
    def __init__(self, interval, button, click_type, count=-1, delay=0, offset=0):
        super().__init__()
        self.interval = interval
        self.button = button
        self.click_type = click_type
        self.count = count
        self.running = True
        self.delay = delay
        self.offset = offset
        self.stopped = False
    
    def run(self):
        import time
        import random
        from AppKit import NSEvent
        from Quartz import CGEventCreateMouseEvent, CGEventPost, kCGHIDEventTap, kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGEventRightMouseDown, kCGEventRightMouseUp, kCGEventOtherMouseDown, kCGEventOtherMouseUp
        if self.delay > 0:
            time.sleep(self.delay)
        next_click = time.perf_counter()
        clicks_performed = 0
        while self.running and (self.count == -1 or clicks_performed < self.count):
            now = time.perf_counter()
            if now >= next_click:
                # Mausposition abfragen
                from Quartz import CGEventCreate, CGEventGetLocation
                loc = CGEventGetLocation(CGEventCreate(None))
                x, y = int(loc.x), int(loc.y)
                # Button bestimmen
                if self.button == 'left':
                    down = kCGEventLeftMouseDown
                    up = kCGEventLeftMouseUp
                elif self.button == 'right':
                    down = kCGEventRightMouseDown
                    up = kCGEventRightMouseUp
                else:
                    down = kCGEventOtherMouseDown
                    up = kCGEventOtherMouseUp
                # Klick ausführen
                def click_once():
                    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, down, (x, y), 0))
                    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, up, (x, y), 0))
                if self.click_type == "Single":
                    click_once()
                elif self.click_type == "Double":
                    click_once()
                    time.sleep(0.05)
                    click_once()
                clicks_performed += 1
                offset_val = random.uniform(-self.offset, self.offset) / 1000.0
                next_click = now + max(0.001, self.interval + offset_val)
            time.sleep(0.001)
        self.running = False
        self.finished.emit()
    
    def stop(self):
        self.running = False
        self.stopped = True

class AutoClickerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clicker_thread = None
        self.initUI()
        self.load_settings()
        
    def initUI(self):
        self.setWindowTitle('Mac Autoclicker')
        self.setFixedSize(400, 370)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        # Intervall-Einstellung
        interval_layout = QHBoxLayout()
        interval_label = QLabel('Klick-Intervall (Sekunden):')
        self.interval_spinbox = QDoubleSpinBox()
        self.interval_spinbox.setRange(0.001, 3600)
        self.interval_spinbox.setSingleStep(0.001)
        self.interval_spinbox.setValue(1.0)
        self.interval_spinbox.valueChanged.connect(self.update_cps_label)
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_spinbox)
        layout.addLayout(interval_layout)
        # Offset-Intervall
        offset_layout = QHBoxLayout()
        offset_label = QLabel('Offset (ms):')
        self.offset_spinbox = QSpinBox()
        self.offset_spinbox.setRange(0, 1000)
        self.offset_spinbox.setValue(0)
        offset_layout.addWidget(offset_label)
        offset_layout.addWidget(self.offset_spinbox)
        layout.addLayout(offset_layout)
        # CPS-Anzeige
        self.cps_label = QLabel('CPS: 1.00')
        layout.addWidget(self.cps_label)
        # Mausbutton-Auswahl
        button_layout = QHBoxLayout()
        button_label = QLabel('Maustaste:')
        self.button_combo = QComboBox()
        self.button_combo.addItems(['Links', 'Rechts', 'Mitte'])
        button_layout.addWidget(button_label)
        button_layout.addWidget(self.button_combo)
        layout.addLayout(button_layout)
        # Klick-Typ
        click_type_layout = QHBoxLayout()
        click_type_label = QLabel('Klick-Typ:')
        self.click_type_combo = QComboBox()
        self.click_type_combo.addItems(['Single', 'Double'])
        click_type_layout.addWidget(click_type_label)
        click_type_layout.addWidget(self.click_type_combo)
        layout.addLayout(click_type_layout)
        # Anzahl der Klicks
        count_layout = QHBoxLayout()
        count_label = QLabel('Anzahl der Klicks:')
        self.count_spinbox = QSpinBox()
        self.count_spinbox.setRange(-1, 99999)
        self.count_spinbox.setValue(-1)
        self.count_spinbox.setSpecialValueText('Unendlich')
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.count_spinbox)
        # Button für Unendlich
        self.unendlich_button = QPushButton('Unendlich')
        self.unendlich_button.clicked.connect(self.set_unendlich)
        count_layout.addWidget(self.unendlich_button)
        layout.addLayout(count_layout)
        # Start/Stop Button
        self.start_stop_button = QPushButton('Start')
        self.start_stop_button.clicked.connect(self.toggle_clicking)
        layout.addWidget(self.start_stop_button)
        # Einstellungen speichern Checkbox
        self.save_settings_checkbox = QCheckBox('Einstellungen speichern')
        self.save_settings_checkbox.setChecked(True)
        layout.addWidget(self.save_settings_checkbox)
        self.update_cps_label()
        # Timer für Countdown
        self.countdown_timer = QTimer()
        self.countdown_timer.setInterval(1000)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_value = 0
        
    def update_cps_label(self):
        interval = self.interval_spinbox.value()
        cps = 1.0 / interval if interval > 0 else 0
        self.cps_label.setText(f'CPS: {cps:.2f}')
        
    def toggle_clicking(self):
        if self.clicker_thread is None or not self.clicker_thread.running:
            self.start_clicking()
        else:
            self.stop_clicking()
            
    def start_clicking(self):
        self.countdown_value = 3
        self.start_stop_button.setText(f'Start ({self.countdown_value})')
        self.start_stop_button.setEnabled(False)
        self.countdown_timer.start()
        
    def update_countdown(self):
        self.countdown_value -= 1
        if self.countdown_value > 0:
            self.start_stop_button.setText(f'Start ({self.countdown_value})')
        else:
            self.countdown_timer.stop()
            self.start_stop_button.setText('Stop')
            self.start_stop_button.setEnabled(True)
            interval = self.interval_spinbox.value()
            button_text = self.button_combo.currentText().lower()
            button = 'left' if button_text == 'links' else 'right' if button_text == 'rechts' else 'middle'
            click_type = self.click_type_combo.currentText()
            count = self.count_spinbox.value()
            offset = self.offset_spinbox.value()
            self.clicker_thread = ClickerThread(interval, button, click_type, count, delay=0, offset=offset)
            self.clicker_thread.finished.connect(self.on_clicking_finished)
            self.clicker_thread.start()
        
    def stop_clicking(self):
        if self.clicker_thread and self.clicker_thread.running:
            self.clicker_thread.stop()
            self.clicker_thread.wait()
        self.clicker_thread = None
        self.start_stop_button.setText('Start')
        self.start_stop_button.setEnabled(True)
        
    def on_clicking_finished(self):
        self.start_stop_button.setText('Start')
        self.clicker_thread = None
        self.start_stop_button.setEnabled(True)
        
    def closeEvent(self, event):
        self.stop_clicking()
        if self.save_settings_checkbox.isChecked():
            self.save_settings()
        event.accept()
        
    def save_settings(self):
        settings = {
            'interval': self.interval_spinbox.value(),
            'button': self.button_combo.currentText(),
            'click_type': self.click_type_combo.currentText(),
            'count': self.count_spinbox.value(),
            'offset': self.offset_spinbox.value(),
            'save_settings': self.save_settings_checkbox.isChecked()
        }
        settings_path = os.path.expanduser('~/Library/Application Support/MacAutoclicker')
        os.makedirs(settings_path, exist_ok=True)
        with open(os.path.join(settings_path, 'settings.json'), 'w') as f:
            json.dump(settings, f)
            
    def load_settings(self):
        settings_path = os.path.expanduser('~/Library/Application Support/MacAutoclicker/settings.json')
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
            self.interval_spinbox.setValue(settings.get('interval', 1.0))
            self.button_combo.setCurrentText(settings.get('button', 'Links'))
            self.click_type_combo.setCurrentText(settings.get('click_type', 'Single'))
            self.count_spinbox.setValue(settings.get('count', -1))
            self.offset_spinbox.setValue(settings.get('offset', 0))
            self.save_settings_checkbox.setChecked(settings.get('save_settings', True))
        except:
            pass

    def set_unendlich(self):
        self.count_spinbox.setValue(-1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Stil für ein modernes Aussehen
    app.setStyle('Fusion')
    
    window = AutoClickerWindow()
    window.show()
    
    sys.exit(app.exec())
