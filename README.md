# 🕷 Spider Break Companion

A lightweight, transparent Windows desktop reminder companion that brings Spider-Man to your desktop for eye and hydration breaks!

![Visual Target](spiderman_hanging.png)

## Features

- **Spider-Man Animation**: Spider-Man hangs upside down on a web attached to the top edge of your Windows screen. He smoothly descends when a break is due, settles near the upper-right corner, and climbs back up when dismissed.
- **Eye & Water Reminders**:
  - **Eye Break**: 20-minute default interval with a live 20-second countdown ("Look 20 feet away for 20 seconds").
  - **Water Break**: 120-minute default interval, configurable to 60 minutes or custom intervals ("Time to drink water").
- **Clean Visual Target UI**: Matches the modern card design with red corner accents, red header tags, and responsive buttons (`Done` and `Snooze 5m`).
- **Focus Protection**: Uses native Windows `WS_EX_NOACTIVATE` window styling so keyboard focus is never stolen while you are coding or typing.
- **System Tray App**: Runs quietly in the notification area. Right-click the tray icon to pause/resume reminders, open settings, or run quick test animations.
- **Break Queueing**: If multiple breaks trigger at the same time, they are queued and played sequentially rather than being missed.
- **Multi-Monitor & DPI Scaling**: Automatically anchors to the active monitor top screen edge across display scaling configurations.

---

## How to Launch on Windows

### Option 1: Direct Python Launch
Make sure Python 3.10+ and requirements are installed:
```powershell
pip install PyQt5 Pillow pywin32 pystray
python companion.py
```

### Option 2: Windows Batch Launcher
Double-click `start.bat` in the project folder to run the application quietly in the background without opening a command prompt window.

---

## Quick Testing
To inspect the animation immediately without waiting for timers:
1. Right-click the spider icon in your Windows System Tray (near the clock).
2. Click **👁 Test eye break** or **💧 Test water reminder**.
3. Alternatively, open **Settings...** and click the **Test Eye Break** or **Test Water Break** buttons.
