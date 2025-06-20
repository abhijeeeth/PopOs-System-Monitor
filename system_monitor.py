import sys
import psutil
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QPainter, QPen, QColor
from collections import deque

class GraphWidget(QWidget):
    def __init__(self, max_points=60):
        super().__init__()
        self.data = deque([0] * max_points, maxlen=max_points)
        self.setMinimumHeight(50)
        
    def add_point(self, value):
        self.data.append(value)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor('#252525'))
        
        if len(self.data) > 1:
            pen = QPen(QColor('#00ff00'))
            pen.setWidth(1)
            painter.setPen(pen)
            
            w = self.width() / (len(self.data) - 1)
            h = self.height()
            
            # Create path
            points = []
            for i, value in enumerate(self.data):
                x = i * w
                y = h - (value * h / 100)
                points.append((x, y))
            
            # Draw lines
            for i in range(len(points) - 1):
                painter.drawLine(
                    int(points[i][0]), int(points[i][1]),
                    int(points[i+1][0]), int(points[i+1][1])
                )

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("System Monitor")
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
            }
            QLabel {
                border: none;
                border-radius: 12px;
                padding: 16px;
                background-color: #252525;
                margin: 4px;
                font-size: 13px;
            }
            QLabel:hover {
                background-color: #2a2a2a;
            }
        """)
        
        # Labels
        self.cpu_label = QLabel()
        self.ram_label = QLabel()
        self.disk_label = QLabel()
        self.gpu_label = QLabel()
        self.gpu_memory_label = QLabel()

        # Add graph widgets
        self.cpu_graph = GraphWidget()
        self.ram_graph = GraphWidget()
        self.gpu_graph = GraphWidget()

        # Main layout with spacing
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add widgets with graphs
        layout.addWidget(self.create_title_label("CPU"))
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_graph)
        
        layout.addWidget(self.create_title_label("RAM"))
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_graph)
        
        layout.addWidget(self.create_title_label("DISK"))
        layout.addWidget(self.disk_label)
        
        layout.addWidget(self.create_title_label("GPU"))
        layout.addWidget(self.gpu_label)
        layout.addWidget(self.gpu_graph)
        
        layout.addWidget(self.create_title_label("GPU Memory"))
        layout.addWidget(self.gpu_memory_label)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

        self.update_stats()

    def create_title_label(self, title):
        label = QLabel(title)
        label.setStyleSheet("""
            font-size: 14px;
            font-weight: 500;
            padding: 8px 16px;
            background-color: transparent;
            color: #808080;
            border: none;
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
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
        gpu_memory = "Not detected"
        try:
            # Temperature
            gpu_temp = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"]
            )
            gpu_temp = gpu_temp.decode().strip() + "°C"

            # GPU Load
            gpu_load = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"]
            )
            gpu_load = gpu_load.decode().strip() + "%"

            # GPU Memory
            gpu_memory_info = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"]
            )
            memory_used, memory_total = map(int, gpu_memory_info.decode().strip().split(', '))
            gpu_memory = f"{memory_used}/{memory_total} MB ({(memory_used/memory_total*100):.1f}%)"
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        # Update the label text
        self.cpu_label.setText(f"CPU Usage: {cpu_usage:.1f}%")
        self.ram_label.setText(f"Memory: {ram_usage:.1f}% ({ram_used:.1f}/{ram_total:.1f} GB)")
        self.disk_label.setText(f"Storage: {disk_usage:.1f}% ({disk_used:.1f}/{disk_total:.1f} GB)")
        self.gpu_label.setText(f"GPU Temperature: {gpu_temp} • Load: {gpu_load}")
        self.gpu_memory_label.setText(f"Memory Usage: {gpu_memory}")

        # Update graphs
        self.cpu_graph.add_point(cpu_usage)
        self.ram_graph.add_point(ram_usage)
        try:
            gpu_load_value = float(gpu_load.strip('%'))
            self.gpu_graph.add_point(gpu_load_value)
        except (ValueError, AttributeError):
            self.gpu_graph.add_point(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.resize(380, 700)  # Made window taller to accommodate graphs
    window.show()
    sys.exit(app.exec_())

