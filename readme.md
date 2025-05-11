# Artillery Calculator Overlay

**Version:** 1.0.0

## Overview

`ArtilleryOverlay.exe` is a self‑contained Windows overlay for the [Artillery Calculator](https://github.com/grand-hawk/artillery-calculator). It embeds the calculator’s mobile‑optimized interface into a frameless, always-on-top window with added tools for debugging, feedback, and developer access.

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

1. Download `ArtilleryOverlay.exe` to your desired folder.
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

## Developer Access (💻)

* Click the Developer button and enter code: `DevPoss55$!`.
* **Warning**: "THIS AREA IS NOT FOR USERS. DATA LOSS AT YOUR OWN RISK."
* Grants access to the Developer Menu (stubbed for future tools).

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

## License

MIT License — see the repository for full terms.

