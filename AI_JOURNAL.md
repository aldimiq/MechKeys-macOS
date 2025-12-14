# 🤖 AI Development Journal: MechKeys

This document logs the collaborative development process between the human developer and **Google Gemini** (the AI assistant) in building MechKeys for macOS.

## 📅 Session 1: Core Architecture & Audio Engine (v2.0)

**Goal:** Transform a basic sound player into a feature-rich app.

### 🧠 AI Contributions
*   **Class Design:** Proposed the `SoundPack` class structure to handle loading, slicing, and managing multiple switch types (Black, Blue, Brown, Red).
*   **Spatial Audio Logic:**
    *   Designed the `KEY_PAN_MAP` dictionary to map physical keyboard keys (QWERTY) to stereo pan values (Left 0.0 -> Right 1.0).
    *   Implemented **3D Audio** simulation using algorithmic volume attenuation based on distance from the center.
    *   Added **"Thock Boost"**: Logic to bass-boost specific keys like `Space` and `Enter` for a more satisfying feel.
*   **Persistence:** Built the `ConfigManager` class to save user preferences (`~/.mechkeys.json`) between sessions.
*   **Debugging:** Identified and fixed a critical `TypeError` in the `rumps` library usage where submenu construction was failing (`add()` vs `subMenu` argument).

## 📅 Session 2: Security & UX Polish (v2.1)

**Goal:** Harden the application for public release and improve the first-run experience.

### 🧠 AI Contributions
*   **Security Audit:**
    *   **Risk Identification:** Flagged that `requirements.txt` had unpinned dependencies (Supply Chain Risk) and that the config file was readable by other users.
    *   **Implementation:**
        *   Pinned exact library versions (e.g., `pynput==1.8.1`).
        *   Added `os.chmod(path, 0o600)` to ensure the config file is only readable by the owner.
*   **User Experience (UX):**
    *   **Problem:** Users might not know they need to enable "Input Monitoring" in macOS System Settings.
    *   **Solution:** Implemented a startup check using `rumps.alert`. Added logic to allow the user to "Don't show again," persisting that choice in the config.
*   **DevOps & Release:**
    *   Created the `./build.sh` script to automate the `py2app` build process.
    *   Organized the repository structure (moving assets/scripts).
    *   Generated the Git tags and release artifacts (`.zip`) via CLI.

## 🚀 Conclusion

MechKeys demonstrates how AI can accelerate software engineering by handling boilerplate, suggesting algorithmic improvements, and performing security audits, allowing the developer to focus on product vision and refinement.
