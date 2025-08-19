Klar – hier ist dein **erweitertes, direkt GitHub‑fertiges `README.md`**, in dem jetzt auch die `.app`‑Download‑Option und der bekannte Icon‑Bug dokumentiert sind. Du kannst den folgenden Inhalt so übernehmen:

```markdown
# 🖱️ Mac Autoclicker – PyQt6 & Quartz

Ein funktionsreicher, macOS‑spezifischer Auto‑Clicker mit moderner PyQt6‑Oberfläche.  
Ermöglicht präzises automatisches Klicken (Single oder Double) mit einstellbarem Intervall, Maustaste, Anzahl und zufälligem Zeit‑Jitter.

---

## ✨ Features

- **Cross‑Thread Architektur**: Klicklogik läuft in einem separaten `QThread` – UI bleibt responsiv.
- **Präzise Steuerung**:
  - Intervall von **1 ms bis 1 h**
  - **Single‑ oder Double‑Klicks**
  - **Links/Rechts/Mittlere Maustaste**
  - **Feste Klickanzahl** oder **unendlich**
- **Zufalls‑Jitter (ms)** zur realistischeren Klick‑Simulation
- **3‑Sekunden‑Countdown** vor Start zum Schutz vor versehentlichem Aktivieren
- **Einstellungen speichern** (JSON im User‑Library‑Verzeichnis)
- **Moderner UI‑Look** mit Qt Fusion Theme
- **Nur macOS**: nutzt AppKit & Quartz APIs für native Event‑Erzeugung

---

## 📦 Voraussetzungen

- **macOS** (Zugriff auf Bedienungshilfen muss gewährt werden)
- **Python 3.9+** (empfohlen, nur für die „selbst kompilieren“-Variante)
- Abhängigkeiten (für manuellen Start):
  ```bash
  pip install PyQt6 pyobjc
  ```
- **Bedienungshilfen aktivieren**:  
  `Systemeinstellungen` → `Sicherheit` → `Bedienungshilfen` → App hinzufügen & erlauben.

---

## 🚀 Installation & Nutzung

### 1. Fertige `.app` herunterladen
- Gehe zum **[Releases](../../releases)**‑Bereich auf GitHub.
- Lade die neueste `.app`‑Datei herunter.
- Verschiebe sie in deinen Programme‑Ordner.
- Beim ersten Start ggf. in `Systemeinstellungen` → `Sicherheit` die Ausführung erlauben.

### 2. Selbst kompilieren (für Entwickler)
```bash
# Repo klonen
git clone https://github.com/DEINUSERNAME/mac-autoclicker.git
cd mac-autoclicker

# Abhängigkeiten installieren
pip install -r requirements.txt

# App mit py2app oder pyinstaller bauen
python setup.py py2app  # oder pyinstaller main.py --onefile --windowed
```

> ⚠️ **Bekannter Bug:** Beim Kompilieren wird aktuell statt des Custom‑Icons das Standard‑Python‑2‑Icon angezeigt. Funktionalität ist nicht beeinträchtigt – nur die Optik.  
> Workaround: `.icns`‑Datei manuell im `.app`‑Bundle ersetzen, bis Bug behoben ist.

---

## 🖥️ Bedienung

1. **Intervall einstellen** – Sekunden zwischen Klicks (z. B. `0.05` für 20 CPS).
2. **Jitter (ms)** – Zufällige Zeitabweichung pro Klick.
3. **CPS‑Anzeige** – Zeigt Klicks pro Sekunde basierend auf Intervall.
4. **Maustaste & Klick‑Typ** auswählen.
5. **Anzahl der Klicks** – `-1` = unendlich, oder beliebige feste Zahl.
6. **Start** – Button klicken. Countdown läuft, danach startet der Auto‑Clicker.
7. **Stop** – Jederzeit beenden.

> 💡 Tipp: „Unendlich“‑Button setzt Klickanzahl direkt auf `-1`.

---

## ⚙️ Technische Details

### Architektur
- **GUI**: `AutoClickerWindow` (PyQt6) – steuert Eingaben, Countdown, Thread‑Start/-Stopp, Persistenz.
- **Worker Thread**: `ClickerThread` – erzeugt macOS‑native MouseDown/MouseUp Events via Quartz:
  - `CGEventCreateMouseEvent`
  - `CGEventPost` (`kCGHIDEventTap`)
- **Timing**: `time.perf_counter()` für präzises Scheduling und Drift‑Vermeidung.
- **Persistenz**: JSON‑Datei im Pfad:
  ```
  ~/Library/Application Support/MacAutoclicker/settings.json
  ```

### Event‑Mapping
| GUI‑Einstellung | Quartz Events                           |
|-----------------|----------------------------------------|
| Links           | `kCGEventLeftMouseDown` / `Up`          |
| Rechts          | `kCGEventRightMouseDown` / `Up`         |
| Mitte           | `kCGEventOtherMouseDown` / `Up`         |

---

## 📂 Projektstruktur

```
mac-autoclicker/
├── main.py                # Hauptprogramm (GUI + Thread)
├── requirements.txt       # Python-Abhängigkeiten
├── setup.py               # Build-Skript für py2app/pyinstaller
├── README.md              # Diese Datei
└── icons/                 # Custom Icon (.icns)
```

---

## 🔒 Sicherheit & Berechtigungen

- **Nur macOS**: Andere OS haben keine kompatiblen APIs für `Quartz`/`AppKit`.
- **Bedienungshilfen**: Ohne diese Berechtigung verweigert macOS die Event‑Injection.
- **Nutzung**: Verantwortungsbewusst einsetzen – Auto‑Clicker können als Bot‑Verhalten erkannt werden.

---

## 🛠️ Geplante Verbesserungen

- [ ] Bugfix: Custom‑Icon auch in kompilierter `.app` anzeigen
- [ ] Konfigurierbarer Double‑Click Abstand
- [ ] Unterstützung für positionsbasiertes Klicken (Koordinaten‑Ziel)
- [ ] Verbesserte Energieeffizienz bei langen Intervallen

---

## 🤝 Beitrag & Lizenz

Beiträge, Bugreports und Pull Requests sind willkommen!  
Bitte vor PR‑Erstellung ein Issue eröffnen.

**Lizenz:** MIT (siehe [LICENSE](LICENSE))
```

---

Wenn du magst, kann ich dir zusätzlich den **Workaround‑Abschnitt für den Icon‑Bug** so ausformulieren, dass er auch gleich die Terminal‑Befehle zum manuellen Ersetzen des `.icns` enthält – dann hätten Nutzer direkt die Lösung im README. Willst du, dass ich den noch ergänze?
