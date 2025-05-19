import sys, time, json
from pathlib import Path
import psutil, subprocess
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont

# — load config & bail if feature disabled —

class PopupWindow(QWidget):
    def __init__(self, message: str, duration_ms: int = 5000, flash_red: bool = False):
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

        self.container.adjustSize()
        w, h = self.container.width(), self.container.height()
        self.resize(w, h)
        self.container.setGeometry(0,0,w,h)

        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.x() + (screen.width()-w)//2
        y = screen.y() + 20
        self.setGeometry(QRect(x,y,w,h))

        QTimer.singleShot(duration_ms, self.close)
        if flash_red:
            self._flash = False
            t = QTimer(self)
            t.timeout.connect(self._toggle)
            t.start(500)
            # store the timer so it sticks around

    def _toggle(self):
        bg = "#e74c3c" if self._flash else "#2c3e50"
        self.container.setStyleSheet(f"background-color: {bg}; border-radius: 12px;")
        self._flash = not self._flash

    def show_(self):
        super().show(); self.raise_(); self.activateWindow()

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

    def _popup(self, msg, flash=False, flash_red=False):
        # pass through either flag
        w = PopupWindow(msg, flash_red=(flash or flash_red))
        w.destroyed.connect(lambda _,x=w: None)
        w.show_()

    def on_start(self):
        self._popup("Roblox launched.\nStarting Artillery…")
        # 1) Check our own child handle first
        running_child = self.proc and self.proc.poll() is None

        # 2) Also scan system for any other Artillery processes
        already_running = False
        for p in psutil.process_iter(attrs=["name", "exe"]):
            try:
                name = p.info["name"] or ""
                exe  = p.info["exe"] or ""
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
            if Path(name).stem.lower() == Path(ARTILLERY_PATH).stem.lower() \
                or Path(exe).stem.lower()  == Path(ARTILLERY_PATH).stem.lower():
                already_running = True
                break

        # Only spawn a new one if none found
        if not running_child and not already_running:
            try:
                self.proc = subprocess.Popen([ARTILLERY_PATH])
            except Exception as e:
                self._popup(f"Failed to start:\n{e}")

    def on_stop(self):
        self._popup("Roblox closed.\nShutting Artillery…", flash_red=True)
        QTimer.singleShot(5000, self._kill)

    def _kill(self):
        if self.proc and self.proc.poll() is None:
            self.proc.kill()
        for p in psutil.process_iter():
            if p.name().lower()==ARTILLERY_NAME.lower():
                p.kill()

if __name__=="__main__":
    app = QApplication(sys.argv)
    cfg_file = Path.home()/".overlay_config.json"
    if not cfg_file.exists():
        QMessageBox.critical(None, "Config Missing", "Overlay config not found. Aborting. Please try to re-run the Artillery Calculator exe file before trying again.")
        sys.exit(1)
    cfg = json.loads(cfg_file.read_text())
    if not cfg.get("on_roblox_startup", False):
        sys.exit(0)
    ARTILLERY_PATH = cfg["paths"]["overlay_exe"]
    ARTILLERY_NAME = Path(ARTILLERY_PATH).name
    w = Watcher()
    code = app.exec_()
    w.thread.stop()
    sys.exit(code)
