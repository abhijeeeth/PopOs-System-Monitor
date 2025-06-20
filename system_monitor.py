import sys
import psutil
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("SYS_MONITOR::POP_OS")
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;
                color: #00ff00;
                font-family: 'Courier New';
            }
            QLabel {
                border: 1px solid #00ff00;
                padding: 5px;
                background-color: #001100;
            }
        """)
        
        # Labels
        self.cpu_label = QLabel()
        self.ram_label = QLabel()
        self.disk_label = QLabel()
        self.gpu_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.create_title_label("CPU"))
        layout.addWidget(self.cpu_label)

        layout.addWidget(self.create_title_label("RAM"))
        layout.addWidget(self.ram_label)

        layout.addWidget(self.create_title_label("Disk"))
        layout.addWidget(self.disk_label)

        layout.addWidget(self.create_title_label("GPU"))
        layout.addWidget(self.gpu_label)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

        self.update_stats()

    def create_title_label(self, title):
        label = QLabel(f"[ {title}_METRICS ]")
        label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            border: 2px solid #00ff00;
            border-radius: 5px;
            padding: 5px;
            background-color: #002200;
        """)
        return label

    def update_stats(self):
        # CPU Usage
        cpu_usage = psutil.cpu_percent(interval=0.5)

        # RAM Usage
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_used = ram.used / (1024**3)
        ram_total = ram.total / (1024**3)

        # Disk Usage
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        disk_used = disk.used / (1024**3)
        disk_total = disk.total / (1024**3)

        # GPU Usage & Temp
        gpu_temp = "Not detected"
        gpu_load = "Not detected"
        try:
            gpu_temp = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"]
            )
            gpu_temp = gpu_temp.decode().strip() + "°C"

            gpu_load = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"]
            )
            gpu_load = gpu_load.decode().strip() + "%"
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        # Set Labels with more technical formatting
        self.cpu_label.setText(f"[UTILIZATION]: {cpu_usage:.1f}% | STATUS: MONITORING")
        self.ram_label.setText(f"[MEMORY_USAGE]: {ram_usage:.1f}% | ALLOCATED: {ram_used:.1f}/{ram_total:.1f}GB")
        self.disk_label.setText(f"[STORAGE_STATUS]: {disk_usage:.1f}% | CAPACITY: {disk_used:.1f}/{disk_total:.1f}GB")
        self.gpu_label.setText(f"[GPU_METRICS] | TEMP: {gpu_temp} | LOAD: {gpu_load}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.resize(400, 400)  # Made window slightly larger
    window.show()
    sys.exit(app.exec_())

