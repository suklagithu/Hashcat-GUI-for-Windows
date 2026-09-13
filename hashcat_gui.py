#!/usr/bin/env python3
"""
Hashcat Graphical Suite - Single Raw Log Interactive Edition
"""

import sys
import shutil
import subprocess
import threading
import re
import webbrowser
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

APP_NAME = "Hashcat Graphical Suite (Interactive Secure Mode)"
CONVERT_DIR = Path.home() / ".hashcat_suite_converted"
CONVERT_DIR.mkdir(exist_ok=True)
DOWNLOADS = Path.home() / "Downloads"


def find_binary(name):
    return shutil.which(name)


def next_case_folder():
    i = 1
    while True:
        folder = DOWNLOADS / f"case{i}"
        if not folder.exists():
            folder.mkdir()
            return folder
        i += 1


def auto_detect_mode(file_path):
    ext = Path(file_path).suffix.lower()

    if ext in [".cap", ".pcap", ".pcapng", ".hc22000"]:
        return 22000

    if ext == ".txt":
        try:
            with open(file_path, "r", errors="ignore") as f:
                first_line = f.readline().strip()
        except:
            return None

        if re.fullmatch(r"[a-fA-F0-9]{32}", first_line):
            return 0
        if re.fullmatch(r"[a-fA-F0-9]{40}", first_line):
            return 100
        if re.fullmatch(r"[a-fA-F0-9]{64}", first_line):
            return 1400
        if first_line.startswith("$2"):
            return 3200

    return None


def convert_if_needed(file_path):
    ext = Path(file_path).suffix.lower()
    if ext not in [".cap", ".pcap", ".pcapng"]:
        return file_path

    hcx = find_binary("hcxpcapngtool")
    if not hcx:
        raise RuntimeError("hcxpcapngtool not installed")

    output = CONVERT_DIR / (Path(file_path).stem + ".hc22000")

    if not output.exists():
        subprocess.run([hcx, "-o", str(output), file_path])

    return str(output)


class HashcatWorker(QtCore.QObject):
    output = QtCore.pyqtSignal(str)
    speed = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)

    def __init__(self, cmd, case_folder):
        super().__init__()
        self.cmd = cmd
        self.case_folder = case_folder
        self._stop = False

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self._stop = True

    def _run(self):
        try:
            raw_file = open(self.case_folder / "raw_output.log", "wb")

            proc = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            for raw_line in iter(proc.stdout.readline, b''):
                if self._stop:
                    proc.terminate()
                    break

                raw_file.write(raw_line)
                line = raw_line.decode("utf-8", errors="ignore")
                self.output.emit(line)

                spd = re.search(r"Speed.*?:\s*(.*)", line)
                if spd:
                    self.speed.emit(spd.group(1))

                if ":" in line and not line.startswith("Speed"):
                    raw_file.write(line.encode())

            proc.wait()
            raw_file.close()
            self.finished.emit(proc.returncode)

        except Exception as e:
            self.output.emit(f"Worker Error: {e}")
            self.finished.emit(-1)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1300, 850)
        self.worker = None
        self.case_folder = None
        self._build_ui()

    def _build_ui(self):
        main = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(main)

        title = QtWidgets.QLabel("🔥 Hashcat Interactive Secure Mode")
        title.setFont(QtGui.QFont("Arial", 22, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        form = QtWidgets.QFormLayout()

        self.hash_edit = QtWidgets.QLineEdit()
        btn_hash = QtWidgets.QPushButton("Browse")
        btn_hash.clicked.connect(self._browse_hash)
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.hash_edit)
        h_layout.addWidget(btn_hash)

        self.word_edit = QtWidgets.QLineEdit()
        btn_word = QtWidgets.QPushButton("Browse")
        btn_word.clicked.connect(self._browse_word)
        w_layout = QtWidgets.QHBoxLayout()
        w_layout.addWidget(self.word_edit)
        w_layout.addWidget(btn_word)

        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItem("Auto Detect", -1)
        self.mode_combo.addItem("22000 - WPA/WPA2", 22000)
        self.mode_combo.addItem("0 - MD5", 0)
        self.mode_combo.addItem("100 - SHA1", 100)
        self.mode_combo.addItem("1400 - SHA256", 1400)
        self.mode_combo.addItem("1000 - NTLM", 1000)
        self.mode_combo.addItem("3200 - bcrypt", 3200)

        form.addRow("Hash File:", h_layout)
        form.addRow("Wordlist:", w_layout)
        form.addRow("Mode:", self.mode_combo)
        layout.addLayout(form)

        self.status_label = QtWidgets.QLabel("Status: Idle")
        layout.addWidget(self.status_label)

        self.speed_label = QtWidgets.QLabel("Speed: -")
        layout.addWidget(self.speed_label)

        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        btn_layout = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton("Start")
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.clear_btn = QtWidgets.QPushButton("Clear Console")
        self.open_btn = QtWidgets.QPushButton("Open Case Folder")

        self.stop_btn.setEnabled(False)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.open_btn)

        layout.addLayout(btn_layout)

        self.start_btn.clicked.connect(self._start)
        self.stop_btn.clicked.connect(self._stop)
        self.clear_btn.clicked.connect(self.console.clear)
        self.open_btn.clicked.connect(self._open_folder)

        self.setCentralWidget(main)

    def _browse_hash(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select file", "",
            "All Supported (*.cap *.pcap *.pcapng *.hc22000 *.txt)"
        )
        if file:
            self.hash_edit.setText(file)
            detected = auto_detect_mode(file)
            if detected:
                index = self.mode_combo.findData(detected)
                if index != -1:
                    self.mode_combo.setCurrentIndex(index)

    def _browse_word(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select wordlist")
        if file:
            self.word_edit.setText(file)

    def _build_cmd(self):
        hc = find_binary("hashcat")
        if not hc:
            raise RuntimeError("hashcat not found")

        file = self.hash_edit.text().strip()
        if not file:
            raise RuntimeError("No file selected")

        file = convert_if_needed(file)

        mode = self.mode_combo.currentData()
        if mode == -1:
            mode = auto_detect_mode(file)
            if not mode:
                raise RuntimeError("Auto detection failed")

        cmd = [
            hc,
            "-m", str(mode),
            file,
            self.word_edit.text().strip(),
            "--potfile-disable",
            "--status",
            "--status-timer=5"
        ]

        return cmd

    def _start(self):
        self.case_folder = next_case_folder()
        self.status_label.setText(f"Running → {self.case_folder}")
        self.console.clear()

        try:
            cmd = self._build_cmd()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
            return

        self.worker = HashcatWorker(cmd, self.case_folder)
        self.worker.output.connect(self.console.append)
        self.worker.speed.connect(self.speed_label.setText)
        self.worker.finished.connect(self._finished)
        self.worker.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def _stop(self):
        if self.worker:
            self.worker.stop()

    def _finished(self, code):
        self.status_label.setText(f"Finished (code={code})")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def _open_folder(self):
        if self.case_folder:
            webbrowser.open(str(self.case_folder))


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
