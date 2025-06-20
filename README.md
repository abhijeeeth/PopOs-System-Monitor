# 🖥️ System Monitor App for Pop!_OS/Linux

A simple **Python + PyQt5** app that displays **live CPU, RAM, Disk, and GPU (NVIDIA)** statistics.

---

## ✨ Features
✅ Displays:
- **CPU Usage (%)**
- **RAM Usage (%) & Total**
- **Disk Usage (%) & Total**
- **GPU Temp & Usage (%)** (NVIDIA)

✅ Simple, clean, bold labels for better readability.  
✅ Refreshes every second.

---

## ⚡️ Requirements
- **Pop!_OS / Ubuntu / Debian-based Linux** or **Windows**
- **Python 3.10 or later**
- **NVIDIA GPU** (optional)

### Python Packages
- `psutil`
- `PyQt5`

**Additional GPU Requirement**:
- `nvidia-smi` available (for GPU stats)
  - Linux: Included with NVIDIA drivers
  - Windows: Included with NVIDIA drivers

---

## 🚀 Installation & Usage

### Install Dependencies

**Linux**:
```bash
sudo apt install python3 python3-pip
pip3 install psutil pyqt5
```

**Windows**:
```bash
pip install psutil pyqt5
```

### Running the App
**Linux**:
```bash
python3 system_monitor.py
```

**Windows**:
```bash
python system_monitor.py
```

## 📊 Output
The app displays a window with real-time monitoring of:
- CPU Usage percentage
- RAM Usage and total available memory
- Disk Usage and total storage
- GPU Temperature and Usage (for NVIDIA GPUs)

## 📝 Notes
- Updates every second automatically
- If NVIDIA GPU is not detected, GPU stats will show "Not detected"
- Tested on Pop!_OS 22.04

## 👤 Author
- **Name**: Abhijith Shaji
- **GitHub**: [abhijeeeth](https://github.com/abhijeeeth)
- **LinkedIn**: [stabhijith](https://www.linkedin.com/in/stabhijith)