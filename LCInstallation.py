import os
import requests
import ctypes
import shutil
import sys
import threading
import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
import base64

# Fungsi pop-up (tidak berubah)
def show_question(title, text):
    return ctypes.windll.user32.MessageBoxW(0, text, title, 0x20 | 0x4)

def show_message(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0x40 | 0x0)

# Fungsi download (tidak berubah)
def download_file(url, destination_path, progress_bar, status_label, root_window):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(destination_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        percentage = (downloaded_size / total_size) * 100
                        progress_bar['value'] = percentage
                        root_window.update_idletasks()
        return True
    except Exception as e:
        show_message("Download Error", f"Failed to download {os.path.basename(destination_path)}.\n\nError: {e}")
        return False

# FUNGSI BARU UNTUK MEMBUAT PROFIL DI MINECRAFT LAUNCHER
def create_launcher_profile(status_label, root_window):
    try:
        status_label.config(text="Creating launcher profile...")
        root_window.update_idletasks()
        
        PROFILE_NAME = "LegacyCraft"
        VERSION_ID = "fabric-1.21.8"
        PROFILE_ID = "legacycraft-profile-autogen"
        
        minecraft_folder = os.path.join(os.getenv('APPDATA'), '.minecraft')
        profiles_path = os.path.join(minecraft_folder, 'launcher_profiles.json')

        # --- Bagian Baru untuk Ikon dari URL ---
        icon_string = "Furnace" # Default jika download logo gagal
        # URL langsung ke file gambar mentah di GitHub
        logo_url = "https://raw.githubusercontent.com/Baruls/LegacyCraftInstallation/main/logo.png" 
        
        try:
            # Unduh gambar dari URL
            response = requests.get(logo_url)
            response.raise_for_status() # Cek jika link error
            
            # Ubah data gambar yang diunduh menjadi teks Base64
            b64_string = base64.b64encode(response.content).decode('utf-8')
            icon_string = f"data:image/png;base64,{b64_string}"
        except Exception as e:
            print(f"Failed to download custom icon, using default. Error: {e}")
        # --- Akhir dari Bagian Baru ---

        new_profile = {
            "name": PROFILE_NAME,
            "type": "custom",
            "created": datetime.now().isoformat(),
            "lastUsed": datetime.now().isoformat(),
            "lastVersionId": VERSION_ID,
            "icon": icon_string # Menggunakan ikon dari URL atau default
        }
        
        if os.path.exists(profiles_path):
            with open(profiles_path, 'r') as f:
                profiles_data = json.load(f)
        else:
            profiles_data = {"profiles": {}}

        profiles_data["profiles"][PROFILE_ID] = new_profile
        
        with open(profiles_path, 'w') as f:
            json.dump(profiles_data, f, indent=4)
            
        return True
    except Exception as e:
        show_message("Profile Creation Error", f"Failed to create Minecraft Launcher profile.\n\nError: {e}")
        return False

# Fungsi instalasi versi (tidak berubah)
def handle_version_install(progress_bar, status_label, root_window):
    versions_folder = os.path.join(os.getenv('APPDATA'), '.minecraft', 'versions')
    target_version_folder = os.path.join(versions_folder, 'fabric-1.21.8')
    os.makedirs(versions_folder, exist_ok=True)
    if os.path.exists(target_version_folder):
        replace_response = show_question("Version Found", "Minecraft version 'fabric-1.21.8' already exists.\n\nDo you want to replace it?")
        if replace_response == 6:
            shutil.rmtree(target_version_folder)
        else:
            return True
    os.makedirs(target_version_folder)
    version_files_to_download = {
        'fabric-1.21.8.jar': 'https://raw.githubusercontent.com/Baruls/LegacyCraftInstallation/main/versions/fabric-1.21.8.jar',
        'fabric-1.21.8.json': 'https://raw.githubusercontent.com/Baruls/LegacyCraftInstallation/main/versions/fabric-1.21.8.json'
    }
    for filename, url in version_files_to_download.items():
        status_label.config(text=f"Downloading version file: {filename}...")
        progress_bar['value'] = 0
        destination_path = os.path.join(target_version_folder, filename)
        if not download_file(url, destination_path, progress_bar, status_label, root_window):
            return False
    return True

# Fungsi instalasi mod (tidak berubah)
def handle_mods_install(progress_bar, status_label, root_window):
    mods_folder = os.path.join(os.getenv('APPDATA'), '.minecraft', 'mods')
    os.makedirs(mods_folder, exist_ok=True)
    existing_jars = [f for f in os.listdir(mods_folder) if f.endswith('.jar')]
    if existing_jars:
        backup_response = show_question("Backup Mods?", "Your mods folder already contains files.\n\nWould you like to backup existing mods?")
        if backup_response == 6:
            status_label.config(text="Backing up existing mods...")
            backup_folder = os.path.join(mods_folder, 'backup_mods')
            os.makedirs(backup_folder, exist_ok=True)
            for jar_file in existing_jars:
                shutil.move(os.path.join(mods_folder, jar_file), os.path.join(backup_folder, jar_file))
    mods_to_download = {
        'JEB.jar': 'https://raw.githubusercontent.com/Baruls/LegacyCraftInstallation/main/mods/JEB.jar',
        'fabric-api.jar': 'https://raw.githubusercontent.com/Baruls/LegacyCraftInstallation/main/mods/fabric-api.jar',
        'iris.jar': 'https://raw.githubusercontent.com/Baruls/LegacyCraftInstallation/main/mods/iris.jar',
        'sodium.jar': 'https://raw.githubusercontent.com/Baruls/LegacyCraftInstallation/main/mods/sodium.jar',
        'voicechat.jar': 'https://raw.githubusercontent.com/Baruls/LegacyCraftInstallation/main/mods/voicechat.jar'
    }
    total_files = len(mods_to_download)
    for i, (filename, url) in enumerate(mods_to_download.items()):
        status_label.config(text=f"Downloading Mod ({i+1}/{total_files}): {filename}...")
        progress_bar['value'] = 0
        destination_path = os.path.join(mods_folder, filename)
        if not download_file(url, destination_path, progress_bar, status_label, root_window):
            return False
    return True

# Fungsi utama yang mengatur alur (DIUBAH)
def main_process_thread(progress_bar, status_label, root_window):
    try:
        version_installed = False # Penanda apakah versi diinstal di sesi ini
        install_version_response = show_question("Install Minecraft Version?", "Do you want to install Fabric 1.21.8?")
        if install_version_response == 6:
            if not handle_version_install(progress_bar, status_label, root_window):
                root_window.destroy(); return
            version_installed = True
        
        if not handle_mods_install(progress_bar, status_label, root_window):
             root_window.destroy(); return

        # DIUBAH: Panggil fungsi pembuatan profil setelah semua instalasi selesai
        if version_installed:
            if not create_launcher_profile(status_label, root_window):
                root_window.destroy(); return

        show_message("Installation Complete!", "All required files and profiles have been installed successfully.")
    except Exception as e:
        show_message("An Error Occurred", f"An unexpected error occurred:\n{e}")
    finally:
        root_window.destroy()

# Bagian utama yang dijalankan (tidak berubah)
if __name__ == "__main__":
    initial_response = show_question("Legacy Craft Requirement Installation", "You are about to install the required files for the modpack.\n\nDo you want to continue?")
    if initial_response == 6:
        root = tk.Tk()
        root.title("LegacyCraft Installer")
        root.geometry("450x150")
        root.resizable(False, False)
        status_label = ttk.Label(root, text="Preparing to install...", font=("Helvetica", 10))
        status_label.pack(pady=10, padx=20, anchor="w")
        progress_bar = ttk.Progressbar(root, orient="horizontal", length=410, mode="determinate")
        progress_bar.pack(pady=10, padx=20)
        main_thread = threading.Thread(target=main_process_thread, args=(progress_bar, status_label, root), daemon=True)
        main_thread.start()
        root.mainloop()
    else:
        sys.exit()