import os
import requests
import ctypes
import shutil
import sys
import threading
import tkinter as tk
from tkinter import ttk
import zipfile

def show_question(title, text):
    return ctypes.windll.user32.MessageBoxW(0, text, title, 0x20 | 0x4)

def show_message(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0x40 | 0x0)

def handle_version_install(progress_bar, status_label, root_window):
    status_label.config(text="Checking Minecraft version...")
    root_window.update_idletasks()

    versions_folder = os.path.join(os.getenv('APPDATA'), '.minecraft', 'versions')
    target_version_folder = os.path.join(versions_folder, 'fabric-1.21.8')
    os.makedirs(versions_folder, exist_ok=True)

    if os.path.exists(target_version_folder):
        replace_response = show_question("Version Found", "Minecraft version 'fabric-1.21.8' already exists.\n\nDo you want to replace it?")
        if replace_response == 6:
            try:
                status_label.config(text="Removing existing version...")
                root_window.update_idletasks()
                shutil.rmtree(target_version_folder)
            except Exception as e:
                show_message("Error", f"Failed to remove existing version folder.\n{e}")
                return False
        else:
            return True

    try:
        # Buat folder target baru yang kosong
        os.makedirs(target_version_folder, exist_ok=True)

        # Daftar file yang akan diunduh ke dalam folder versi
        # GANTI FILE ID DI BAWAH INI DENGAN ID ANDA
        version_files_to_download = {
            'fabric-1.21.8.jar': '1i8w5piXwhBlLUJatISNxNXA9xFu_uUpy', #1wXl771dTHO8Mv0lqhUZ5BzI9w07HUEPn
            'fabric-1.21.8.json': '1txMcxYFAfYQQlt6I4SnY8R8VR8kkcMwA'
        }
        
        session = requests.Session()
        URL = "https://docs.google.com/uc?export=download"
        
        for filename, file_id in version_files_to_download.items():
            status_label.config(text=f"Downloading version file: {filename}...")
            progress_bar['value'] = 0
            root_window.update_idletasks()
            
            destination_path = os.path.join(target_version_folder, filename)
            
            # Gunakan logika download yang sudah terbukti andal
            response = session.get(URL, params={'id': file_id}, stream=True)
            token = None
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    token = value
                    break
            if token:
                params = {'id': file_id, 'confirm': token}
                response = session.get(URL, params=params, stream=True)

            # Pengecekan penting untuk memastikan yang diunduh bukan HTML
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' in content_type:
                show_message("Download Error", f"The link for '{filename}' is not a direct download link. Please create a new share link.")
                return False

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
        
        show_message("Success", "Minecraft version fabric-1.21.8 has been installed successfully.")
        return True

    except Exception as e:
        show_message("Version Install Error", f"An error occurred during version installation:\n{e}")
        return False

def handle_mods_install(progress_bar, status_label, root_window):
    mods_folder = os.path.join(os.getenv('APPDATA'), '.minecraft', 'mods')
    os.makedirs(mods_folder, exist_ok=True)

    existing_jars = [f for f in os.listdir(mods_folder) if f.endswith('.jar')]
    if existing_jars:
        backup_response = show_question("Backup Mods?", "Your mods folder already contains files.\n\nWould you like to backup existing mods before continuing?")
        if backup_response == 6:
            status_label.config(text="Backing up existing mods...")
            root_window.update_idletasks()
            backup_folder = os.path.join(mods_folder, 'backup_mods')
            os.makedirs(backup_folder, exist_ok=True)
            for jar_file in existing_jars:
                shutil.move(os.path.join(mods_folder, jar_file), os.path.join(backup_folder, jar_file))
    
    files_to_download = {
        'VoiceChat.jar': '1i8w5piXwhBlLUJatISNxNXA9xFu_uUpy',
        'Sodium.jar': '1HCZR6nVj0_7GR-J9mkZmsEwG_a6DjRQs',
        'JustEnoughBook.jar': '1gC1JHJhPNoHw0HG_j1cNq6rEAuxJxbTS',
        'FabricAPI.jar': '1nU1Gb4_l2aPTKnuEdwyB2-xzaObqzAHc',
        'Iris.jar': '19anH2j6ua9pSB5ma-BY4K4v9s8tMyA4j'
    }

    session = requests.Session()
    total_files = len(files_to_download)
    for i, (filename, file_id) in enumerate(files_to_download.items()):
        status_label.config(text=f"Downloading Mod ({i+1}/{total_files}): {filename}...")
        progress_bar['value'] = 0
        root_window.update_idletasks()

        URL = "https://docs.google.com/uc?export=download"
        destination_path = os.path.join(mods_folder, filename)
        
        response = session.get(URL, params={'id': file_id}, stream=True)
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
                break
        if token:
            params = {'id': file_id, 'confirm': token}
            response = session.get(URL, params=params, stream=True)

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

def main_process_thread(progress_bar, status_label, root_window):
    try:
        install_version_response = show_question("Install Minecraft Version?", "Do you want to install Fabric 1.21.8?\n\n(This is required for the mods to work).")
        if install_version_response == 6: 
            version_success = handle_version_install(progress_bar, status_label, root_window)
            if not version_success:
                root_window.destroy()
                return
        
        handle_mods_install(progress_bar, status_label, root_window)

        show_message("Installation Complete!", f"All required files have been installed.")

    except Exception as e:
        show_message("An Error Occurred", f"An unexpected error occurred during the process:\n{e}")
    finally:
        root_window.destroy()

if __name__ == "__main__":
    initial_response = show_question(
        "Legacy Craft Requirement Installation",
        "You are about to install the required files for the modpack.\n\nDo you want to continue?"
    )
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