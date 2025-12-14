# 🗺️ MechKeys Roadmap

Plans for future versions of MechKeys for macOS.

## 🚀 Version 3.0 (Planned)

### 1. The "Panic Button" (Global Hotkey)
- **Goal:** Instantly toggle sound mute/unmute without using the mouse.
- **Implementation:** Register a global hotkey (e.g., `Cmd + Option + M`).
- **Use Case:** Quickly muting the app when a meeting starts or a colleague walks in.

### 2. Typewriter Mode (The "Ding!")
- **Goal:** Add a rewarding "Carriage Return" bell sound.
- **Implementation:** Detect the `Enter` key specifically and play a distinct `ding.wav` or `bell.ogg` on top of the switch sound.
- **Customization:** Toggleable in the menu.

### 3. Dynamic Flow (WPM Intensity)
- **Goal:** Audio feedback that matches your typing energy.
- **Implementation:** Measure WPM (Words Per Minute) in real-time.
    - **Low WPM:** Quiet, gentle sounds.
    - **High WPM:** Louder, sharper sounds.

## 🔮 Future Ideas
- **Custom Sound Packs:** Drag-and-drop support for adding new folders of OGG files.
- **Per-Key Customization:** Ability to set specific sounds for specific keys (e.g., a "quack" sound for Spacebar).
