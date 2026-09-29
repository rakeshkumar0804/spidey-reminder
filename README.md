# 🕷 Spider Break Companion

A lightweight, transparent Windows desktop reminder companion that brings Spider-Man to your desktop for eye and hydration breaks!

![Visual Target](spiderman_hanging.png)

## Features

- **Spider-Man Animation**: Spider-Man hangs upside down on a web attached to the top edge of your Windows screen. He smoothly descends when a break is due, settles near the upper-right corner, and climbs back up when dismissed.
- **Eye & Water Reminders**:
  - **Eye Break**: 20-minute default interval with a live 20-second countdown ("Look 20 feet away for 20 seconds").
  - **Water Break**: 120-minute default interval, configurable to 60 minutes or custom intervals ("Time to drink water").
- **Automatic dismissal**: Eye, water, and one-time custom reminders each get a 20-second countdown after the final word appears. At zero, the card closes, Spider-Man ascends, and the web retracts (about 1.3 seconds for the exit). Done dismisses early; Snooze 5m keeps a custom reminder pending.
- **Staged entrance**: The supplied white web appears first, Spider-Man descends, the empty card opens, and the sentence appears one word every 300 ms. The app’s Reduced Motion checkbox shows the full card immediately while keeping the timer; leaving it unchecked plays the full sequence, independently of Windows animation preferences.
- **Artwork**: The supplied character illustration is cut out in `spiderman_hanging.png`. The supplied web texture is embedded in `overlay.py`, so no extra asset file or folder is needed.
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

## Updating an existing checkout

Quit the existing tray app, pull the latest changes into your existing repository, then run `start.bat` again. The project keeps the same root-level file structure.

Validation: countdown, completion callbacks, custom snoozing, and the reduced-motion override were checked with offscreen Qt. The owner also confirmed the entrance animation and automatic dismissal working on Windows. Multi-monitor and different DPI configurations have not been comprehensively tested.
