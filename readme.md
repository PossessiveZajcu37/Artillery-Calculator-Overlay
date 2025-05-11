# Artillery Calculator Overlay

**Version:** 1.0.1

---

## Disclaimer

The `ArtilleryOverlay.exe` file is 100% safe to use. However, due to the packing method used, it may be flagged by antivirus software as a potential threat. You can test the file as much as you want, and it is safe to run on your system. The packer used makes the file appear suspicious to some antivirus systems, but rest assured, this is a false positive.![image](https://github.com/user-attachments/assets/7fcb6d2f-b34e-4666-a72f-b724bcb15722)


---

## Overview

`ArtilleryOverlay.exe` is a self‑contained Windows overlay for the [Artillery Calculator](https://github.com/grand-hawk/artillery-calculator). It embeds the calculator’s mobile‑optimized interface into a frameless, always-on-top window with added tools for debugging, feedback, and developer access. The file is available in [releases.](https://github.com/PossessiveZajcu37/Artillery-Calculator-Overlay/releases/latest)
![image](https://github.com/user-attachments/assets/7bb2fe95-acb8-4cb9-9daa-70ed9fc0af15)
![image](https://github.com/user-attachments/assets/0e3dd596-3bc1-478e-931b-9768a71c324f)


---

## Key Features

* **Embedded Web View**: Directly loads the artillery-calculator site in a Qt WebEngine view.
* **Floating Overlay**: Frameless, always‑on‑top window, docked to the top‑right by default.
* **Lock & Drag**: Enable or disable window dragging via Settings.
* **Transparency Control**: Adjust opacity from 0% (fully transparent) to 100% (opaque).
* **FPS Counter**: Optional overlay to display real‑time frames per second.
* **Optional Data Debugging**:

  * Console logs posted live to Discord via webhook.
  * Automatic overlay screenshots every 30 seconds.
* **Developer Access**: Secure menu behind an access code, with warning about potential data loss.
* **Feedback Reporting**: In‑app dialog to send bug reports or feature requests to Discord, with a 2‑minute cooldown.
* **Hotkey Support**: Press `F8` to toggle visibility and display a hint when hidden.
* **Loading Screen**: Centered progress bar window during startup.

---

## Requirements

* **OS**: Windows 10 or later
* **Installation**: No external dependencies—everything is bundled in `ArtilleryOverlay.exe`.

---

## Installation & Launch

1. Download `ArtilleryOverlay.exe` from the releases section.
2. Double‑click the executable to run.
3. The loading screen will appear, then the overlay will launch.
4. Use `F8` to show or hide the overlay.

---

## Configuration

On first run, a configuration file is created at:

```
%USERPROFILE%\.overlay_config.json
```

Default content:

```json
{
  "optional_data": false
}
```

* **optional\_data**: If `true`, enables live log posting and automatic screenshots.

---

## Usage

* **Start**: Run `ArtilleryOverlay.exe`.
* **Toggle**: Press `F8` to show/hide the overlay.
* **Minimize**: Click **Minimize**; restore with `F8`.
* **Close**: Click **Close**, then confirm exit.

---

## Settings Dialog (⚙️)

1. **Lock/Unlock Window**: Toggle dragging mode.
2. **Reset Position**: Snap back to top‑right.
3. **Transparency**: Adjust overlay opacity.
4. **Toggle FPS Counter**.
5. **Optional Data**: Enable/disable live logs & screenshots (30 s interval); shows a thank‑you popup on enable.
6. **Discord Webhook URL**: Enter a webhook to send manual screenshots.
7. **Reload Page**: Refresh the embedded calculator.
8. **Send Screenshot**: Capture and post a screenshot.
9. **View Dev Logs**: Available only when Optional Data is enabled.
10. **Credits**:

    > Full credits to [grand-hawk/artillery-calculator](https://github.com/grand-hawk/artillery-calculator) for the calculator itself; this overlay adds \~700 lines of integration code.

---

## Feedback (🐞)

* Open the feedback dialog, enter your message, and send.
* Posts to Discord via the configured webhook.
* Subsequent submissions are blocked for 2 minutes (cooldown).

---

## Credits

* **Overlay & Integration**: PossessiveZajcu37 on Roblox
* **Calculator Logic**: [grand-hawk/artillery-calculator](https://github.com/grand-hawk/artillery-calculator)

---

## Images

* **Images are available to be seen in releases**

---

## License

MIT License — see the repository for full terms.

---

**Information Box:**
You can download the file from the [Releases](https://github.com/grand-hawk/artillery-overlay/releases) section.
