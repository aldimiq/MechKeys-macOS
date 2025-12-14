# ⌨️ MechKeys for macOS

**MechKeys** is a macOS menu bar application that simulates the sound of mechanical keyboard switches as you type. It works system-wide, adding a satisfying "thock" to every keystroke, whether you're coding, writing an email, or chatting on Slack.

## ✨ Features (v2.0)

*   **System-Wide Sound:** Works in any application.
*   **Zero Dock Presence:** Runs quietly in the menu bar.
*   **3 Audio Modes:**
    *   **Mono:** Focused, centered sound.
    *   **Stereo:** Realistic left/right spatial panning.
    *   **3D (Pro):** Spatial panning with distance attenuation and bass-boosted spacebar.
*   **Volume Control:** Adjust the click volume independently of your system volume.
*   **Sound Packs:** Includes high-quality mechanical switch sounds (Black, Blue, Brown, Red).
*   **Humanization:** Subtle random variations in pitch and volume for a natural feel.

## 📦 Installation

### Pre-built App
1.  Download the latest release.
2.  Drag `MechKeys.app` to your `Applications` folder.
3.  Launch the app.

### Running from Source

**Requirements:**
*   Python 3.9+
*   `pip`

**Steps:**
1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    python3 app.py
    ```

## 🛠️ Building the App (Developer)

To create a standalone `.app` bundle:

1.  Ensure you have the requirements installed.
2.  Run the build script:
    ```bash
    ./build.sh
    ```
3.  The app will be created in the `dist/` folder.

## 🤝 Contributing

See [ROADMAP.md](ROADMAP.md) for planned features. Pull requests are welcome!

## 🤖 Built with Gemini

This project was developed with the assistance of **Google Gemini**, an advanced AI model. Gemini helped with:
*   **Architecture**: Designing the `SoundPack` and `ConfigManager` classes.
*   **Core Logic**: Implementing the stereo panning and 3D audio algorithms.
*   **Refactoring**: Fixing `rumps` menu construction and optimizing performance.
*   **Security**: Auditing dependencies and securing configuration storage.
*   **Documentation**: Generating release notes and project descriptions.

## 📄 License

MIT License
