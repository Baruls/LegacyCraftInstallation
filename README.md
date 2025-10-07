# LegacyCraft Installer

A simple application that automatically installs the required Fabric version and mods to enhance the gameplay experience on the LegacyCraft Minecraft server.

## ✨ Features

* **One-Click Setup:** Installs everything you need with just a few clicks.
* **Automatic Version Installation:** Downloads and installs the correct, official Fabric client version for the server.
* **Mod Installation:** Downloads and installs all required client-side mods directly from the official repository.
* **Backup System:** Automatically offers to back up any existing mods before installing new ones.
* **Launcher Profile Creation:** Creates a dedicated "LegacyCraft" profile in your Minecraft Launcher for easy access, complete with a custom icon.

## 🚀 How to Use

1.  Go to the [**Releases**](https://github.com/Baruls/LegacyCraftInstallation/releases) page.
2.  Download the latest `LegacyCraftInstaller.exe` file.
3.  Run the `.exe` file.
4.  Follow the on-screen prompts (confirm installation, backup mods, etc.).
5.  Once finished, open your Minecraft Launcher.
6.  Select the new **"LegacyCraft"** profile and click Play!

## 📚 Credits & Links

This installer bundles the following amazing projects. Please support their official pages!

* **[FabricMC](https://fabricmc.net/)** - The lightweight, experimental modding toolchain for Minecraft.
* **[Fabric API](https://modrinth.com/mod/fabric-api)** - The core library required for most Fabric mods to function.
* **[Simple Voice Chat](https://modrinth.com/plugin/simple-voice-chat)** - Adds proximity-based voice chat to the game.
* **[Iris Shaders](https://modrinth.com/mod/iris)** - Enables shader support for Sodium.
* **[Just Enough Book](https://modrinth.com/mod/justenoughbook)** - A simple in-game recipe book.
* **[Sodium](https://modrinth.com/mod/sodium)** - A powerful rendering engine replacement for improved performance.

## 🛠️ For Developers (Building from Source)

This project is built with Python and Tkinter for the GUI.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Baruls/LegacyCraftInstallation.git](https://github.com/Baruls/LegacyCraftInstallation.git)
    cd LegacyCraftInstallation
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate
    ```

3.  **Install dependencies:**
    *(Create a `requirements.txt` file first by running `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Build the executable:**
    ```bash
    pyinstaller --onefile --noconsole --icon="icon.ico" LCInstallation.py
    ```
