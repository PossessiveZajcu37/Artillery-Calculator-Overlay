import os
import sys, time, json
from pathlib import Path
import psutil, subprocess
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont

# — load config & bail if feature disabled —

def _kill_watcher_procs(script_name_stem: str):
    for proc in psutil.process_iter(attrs=["pid","name","exe"]):
        try:
            name = (proc.info["name"] or "").lower()
            exe  = Path(proc.info["exe"] or "").stem.lower()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
        if name == script_name_stem or exe == script_name_stem:
            proc.kill()

class PopupWindow(QWidget):
    def __init__(self, message: str, duration_ms: int = 10000, flash_red: bool = False, flash_green: bool = False):
        super().__init__(flags=Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.NoFocus)

        self.container = QWidget(self)
        self.container.setStyleSheet("background-color: #2c3e50; border-radius: 12px;")
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20,12,20,12)

        label = QLabel(message, self.container)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #ecf0f1;")
        label.setFont(QFont("Segoe UI", 13))
        layout.addWidget(label)

        # Add the "Tip" box below the main message
        tip_box = QWidget(self.container)
        tip_box.setStyleSheet("""
            background-color: #34495e;
            border-radius: 8px;
            padding: 10px;
        """)
        tip_layout = QVBoxLayout(tip_box)
        tip_layout.setContentsMargins(10, 2, 10, 2)  # Further reduced margin between "Tip:" and the tip message
        
        # Add the "Tip:" label
        tip_label_header = QLabel("Tip:", tip_box)
        tip_label_header.setAlignment(Qt.AlignLeft)
        tip_label_header.setStyleSheet("color: #ecf0f1; font-size: 14px; font-weight: bold;")
        tip_layout.addWidget(tip_label_header)

        # Add the actual tip message with a larger font size
        tip_label = QLabel("The Auto-Launch feature is togglable in the Artillery Overlay's settings.", tip_box)
        tip_label.setWordWrap(True)
        tip_label.setAlignment(Qt.AlignCenter)
        tip_label.setStyleSheet("color: #ecf0f1; font-size: 16px; font-style: italic;")  # Increased font size
        tip_layout.addWidget(tip_label)

        # Adjust the layout to add the tip box
        layout.addWidget(tip_box)
        self.container.adjustSize()
        w, h = self.container.width(), self.container.height()
        self.resize(w, h)
        self.container.setGeometry(0, 0, w, h)

        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.x() + (screen.width() - w) // 2
        y = screen.y() + 20
        self.setGeometry(QRect(x, y, w, h))

        self.flash_count = 0
        if flash_red:
            self._flash = False
            t = QTimer(self)
            t.timeout.connect(self._toggle_red)
            t.start(500)
        if flash_green:
            self._flash_green = False
            t = QTimer(self)
            t.timeout.connect(self._toggle_green)
            t.start(500)

        # Make the box stay open for the specified duration
        QTimer.singleShot(duration_ms, self.close)

    def _toggle_red(self):
        bg = "#e74c3c" if self._flash else "#2c3e50"
        self.container.setStyleSheet(f"background-color: {bg}; border-radius: 12px;")
        self._flash = not self._flash

    def _toggle_green(self):
        bg = "#2ecc71" if self._flash_green else "#2c3e50"
        self.container.setStyleSheet(f"background-color: {bg}; border-radius: 12px;")
        self._flash_green = not self._flash_green
        self.flash_count += 1
        if self.flash_count >= 6:  # Flash green 3 times
            self._flash_green = False  # Stop flashing green

    def show_(self):
        super().show()
        self.raise_()
        self.activateWindow()

class MonitorThread(QThread):
    started = pyqtSignal()
    stopped = pyqtSignal()
    def __init__(self):
        super().__init__()
        self._run = True
        self._last = False

    def run(self):
        while self._run:
            running = any(p.name().lower()=="robloxplayerbeta.exe" for p in psutil.process_iter())
            if running and not self._last:   self.started.emit()
            if not running and self._last:   self.stopped.emit()
            self._last = running
            time.sleep(1)

    def stop(self):
        self._run=False
        self.wait()

class Watcher:
    def __init__(self):
        QApplication.setQuitOnLastWindowClosed(False)
        self.thread = MonitorThread()
        self.thread.started.connect(self.on_start)
        self.thread.stopped.connect(self.on_stop)
        self.proc = None
        self.thread.start()

    def _popup(self, msg, flash=False, flash_red=False, flash_green=False):
        # pass through either flag
        w = PopupWindow(msg, flash_red=(flash or flash_red), flash_green=flash_green)
        w.destroyed.connect(lambda _,x=w: None)
        w.show_()

    def on_start(self):
        print(f"[DEBUG] Watcher triggered – will try to launch: {ARTILLERY_PATH!r}")

        # 1) If *our* child is still running, bail out
        if self.proc and self.proc.poll() is None:
            return

        # 2) If *any* process with the same executable name is running, bail out
        art_name = Path(ARTILLERY_PATH).name.lower()
        for p in psutil.process_iter(attrs=("name", "exe")):
            try:
                pname = (p.info["name"] or "").lower()
                pexe  = (Path(p.info["exe"] or "").name or "").lower()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

            if pname == art_name or pexe == art_name:
                print(f"[DEBUG] Detected existing Artillery process ({pname}/{pexe}); will not relaunch.")
                return

        # 3) No instance found → launch it
        self._popup("Roblox launched.\nStarting Artillery Calculator…", flash_green=True)
        try:
            self.proc = subprocess.Popen([ARTILLERY_PATH])
            print(f"[DEBUG] Launched Artillery from {ARTILLERY_PATH}")
        except Exception as e:
            self._popup(f"Failed to start:\n{e}")
            print(f"[ERROR] Failed to start Artillery: {e}")


    def on_stop(self):
       
        artillery_stem = Path(ARTILLERY_PATH).stem.lower()
        artillery_running = any(
            (p.info["name"] or "").lower() == artillery_stem or
            Path(p.info["exe"] or "").stem.lower() == artillery_stem
            for p in psutil.process_iter(attrs=["name","exe"])
        )
        if not artillery_running:
            # nothing to do if we never launched or it’s already gone
            return

        self._popup("Roblox closed.\nShutting Artillery Calculator…", flash_red=True)
        QTimer.singleShot(10000, self._kill)

    def _kill(self):
        # kill our child if still running
        if self.proc and self.proc.poll() is None:
            self.proc.kill()

        # kill any other Artillery process (match by stem, so .exe or .pyw both match)
        artillery_stem = Path(ARTILLERY_PATH).stem.lower()
        for p in psutil.process_iter(attrs=["pid","name","exe"]):
            try:
                name = (p.info["name"] or "").lower()
                exe  = Path(p.info["exe"] or "").stem.lower()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
            if name == artillery_stem or exe == artillery_stem:
                p.kill()

if __name__=="__main__":
    watcher_stem = Path(__file__).stem.lower()  
    try:
        _kill_watcher_procs(watcher_stem)
    except Exception as e:
        print(f"[DEBUG] _kill_watcher_procs failed (but continuing): {e}")
    app = QApplication(sys.argv)
    cfg_file = Path.home()/".overlay_config.json"
    if not cfg_file.exists():
        QMessageBox.critical(None, "Config Missing", "Overlay config not found. Aborting. Please try to re-run the Artillery Calculator exe file before trying again.")
        sys.exit(1)
    cfg = json.loads(cfg_file.read_text())
    print(f"[DEBUG] on_roblox_startup in config is {cfg.get('on_roblox_startup')}")
    if not cfg.get("on_roblox_startup", False):
        print("[DEBUG] aborting because on_roblox_startup is false")
        sys.exit(0)
    ARTILLERY_PATH = cfg["paths"]["overlay_exe"]
    ARTILLERY_NAME = Path(ARTILLERY_PATH).name
    w = Watcher()
    code = app.exec_()
    w.thread.stop()
    sys.exit(code)
