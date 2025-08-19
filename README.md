# 🖱️ Mac Autoclicker – PyQt6 & Quartz

A feature-rich, macOS‑specific auto‑clicker with a modern PyQt6 interface.  
Provides precise automated clicking (single or double) with configurable interval, mouse button, click count, and random time jitter.

---

## ✨ Features

- **Cross‑thread architecture**: Clicking logic runs in a separate `QThread` – UI remains responsive.
- **Precise control**:
  - Interval from **1 ms to 1 h**
  - **Single** or **Double** clicks
  - **Left / Right / Middle mouse button**
  - **Fixed click count** or **infinite**
- **Random jitter (ms)** for more natural click simulation
- **3‑second countdown** before starting to prevent accidental activation
- **Save settings** (JSON in user's Library folder)
- **Modern UI look** with Qt Fusion theme
- **macOS only**: uses AppKit & Quartz APIs for native event generation

---

## 📦 Requirements

- **macOS** (must grant Accessibility access)
- **Python 3.9+** (recommended, only for "build yourself" option)
- Dependencies (for manual run):
  ```bash
  pip install PyQt6 pyobjc
  ```
- **Enable Accessibility**:  
  `System Settings` → `Privacy & Security` → `Accessibility` → add the app and allow.

---

## 🚀 Installation & Usage

### 1. Download ready‑to‑use `.app`
- Go to the **[Releases](../../releases)** section on GitHub.
- Download the latest `.app` file.
- Move it to your Applications folder.
- On first launch, you may need to allow execution in `System Settings` → `Privacy & Security`.

### 2. Build yourself (for developers)
```bash
# Clone the repo
git clone https://github.com/YOURUSERNAME/mac-autoclicker.git
cd mac-autoclicker

# Install dependencies
pip install -r requirements.txt

# Build the .app using py2app or pyinstaller
python setup.py py2app  # or: pyinstaller main.py --onefile --windowed
```

> ⚠️ **Known Bug:** When building, the resulting `.app` currently shows the default Python 2 icon instead of the custom icon.  
> Functionality is unaffected – it's purely cosmetic.  
> **Workaround:** Manually replace the `.icns` file inside the `.app` bundle until the bug is fixed.

---

## 🖥️ How to Use

1. **Set the interval** – seconds between clicks (e.g., `0.05` for 20 CPS).
2. **Jitter (ms)** – random variation applied to the interval per click.
3. **CPS label** – shows clicks per second based on the interval.
4. **Select mouse button** and **click type**.
5. **Set click count** – `-1` = infinite, or any fixed number.
6. **Start** – press the button, countdown runs, then clicking starts.
7. **Stop** – press the button to end clicking.

> 💡 Tip: The **"Infinite"** button sets click count to `-1` instantly.

---

## ⚙️ Technical Details

### Architecture
- **GUI**: `AutoClickerWindow` (PyQt6) – handles input, countdown, starting/stopping the thread, and settings persistence.
- **Worker thread**: `ClickerThread` – generates macOS native MouseDown/MouseUp events via Quartz:
  - `CGEventCreateMouseEvent`
  - `CGEventPost` (`kCGHIDEventTap`)
- **Timing**: `time.perf_counter()` for precise scheduling and drift prevention.
- **Persistence**: JSON file stored at:
  ```
  ~/Library/Application Support/MacAutoclicker/settings.json
  ```

### Event Mapping
| GUI Option | Quartz Events                  |
|------------|---------------------------------|
| Left       | `kCGEventLeftMouseDown` / `Up`  |
| Right      | `kCGEventRightMouseDown` / `Up` |
| Middle     | `kCGEventOtherMouseDown` / `Up` |

---

## 📂 Project Structure

```
mac-autoclicker/
├── main.py                # Main application (GUI + thread)
├── requirements.txt       # Python dependencies
├── setup.py               # Build script for py2app/pyinstaller
├── README.md              # This file
└── icons/                 # Custom icon (.icns)
```

---

## 🔒 Security & Permissions

- **macOS only**: No compatible APIs for other OS.
- **Accessibility**: Without permission, macOS will block event injection.
- **Usage**: Use responsibly – auto‑clickers may be detected as bot behaviour.

---

## 🛠️ Planned Improvements

- [ ] Fix: Ensure custom icon appears in built `.app`
- [ ] Configurable double‑click gap
- [ ] Support for coordinate‑based clicking
- [ ] Improved power efficiency for long intervals

---

## 🤝 Contributing & License

Contributions, bug reports, and pull requests are welcome!  
Please open an issue before submitting a PR.

**License:** MIT (see [LICENSE](LICENSE))
```
