import os
import requests
import zipfile
from tkinter import Tk, ttk, filedialog, messagebox, IntVar
from io import BytesIO
import shutil
from urllib.request import urlopen
from ttkthemes import ThemedStyle

class ModManager:
    def __init__(self, root):
        # Apply the themed style
        style = ThemedStyle(root)
        style.set_theme("equilux")  # Choose a ttk theme
        style.configure('TButton', padding=6, relief='flat', background='gray', borderwidth=0, focuscolor='gray')
        style.configure('TCheckbutton', padding=6, relief='flat', background='gray', borderwidth=0)

        root.title("ZenFlow VR Mod Manager")

        # Set the default background color to gray
        root.configure(bg='gray')

        # Adjust the window size
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.label = ttk.Label(root, text="ZenFlow VR Mod Manager", font=("Helvetica", 20), background='gray')
        self.label.pack(pady=20)

        self.select_folder_button = ttk.Button(root, text="Select Game Folder", command=self.select_game_folder, style='TButton')
        self.select_folder_button.pack(pady=10)

        # Toggle for BepInEx installation
        self.bepinex_toggle = IntVar()
        self.bepinex_toggle.set(0)  # Set the default state to off (uninstalled)

        self.bepinex_toggle_button = ttk.Checkbutton(root, text="Toggle BepInEx Installation", variable=self.bepinex_toggle, style='TCheckbutton')
        self.bepinex_toggle_button.pack(pady=10)

        # Toggle for Unity Explorer installation
        self.unity_explorer_toggle = IntVar()
        self.unity_explorer_toggle.set(0)  # Set the default state to off (uninstalled)

        self.unity_explorer_toggle_button = ttk.Checkbutton(root, text="Toggle Unity Explorer", variable=self.unity_explorer_toggle, style='TCheckbutton')
        self.unity_explorer_toggle_button.pack(pady=10)

        # Button to install selected mods
        self.install_selected_button = ttk.Button(root, text="Install Selected", command=self.install_selected, style='TButton')
        self.install_selected_button.pack(pady=20)

        # Initialize game folder
        self.game_folder = None

    def select_game_folder(self):
        self.game_folder = filedialog.askdirectory()
        messagebox.showinfo("Game Folder Selected", f"Game folder set to: {self.game_folder}")

    def install_selected(self):
        if not self.game_folder:
            messagebox.showerror("Error", "Please select the game folder first.")
            return

        try:
            if self.bepinex_toggle.get() == 1:
                self.install_bepinex()

            if self.unity_explorer_toggle.get() == 1:
                self.install_unity_explorer()

            messagebox.showinfo("Installation Complete", "Selected mods installed successfully!")
        except Exception as e:
            messagebox.showerror("Installation Error", f"Error installing mods: {str(e)}")

    def install_bepinex(self):
        try:
            # Download BepInEx zip from GitHub
            url = "https://github.com/BepInEx/BepInEx/releases/download/v5.4.22/BepInEx_x64_5.4.22.0.zip"
            response = requests.get(url)
            response.raise_for_status()

            # Extract zip content
            with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_ref:
                zip_ref.extractall(self.game_folder)

            print("BepInEx installed successfully!")

        except Exception as e:
            messagebox.showerror("Installation Error", f"Error installing BepInEx: {str(e)}")

    def install_unity_explorer(self):
        try:
            # Download Unity Explorer from Thunderstore
            unity_explorer_url = "https://thunderstore.io/package/download/sinai-dev/UnityExplorer/4.8.2/"
            unity_explorer_zip = os.path.join(self.game_folder, "UnityExplorer_4.8.2.zip")

            response = requests.get(unity_explorer_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                with open(unity_explorer_zip, 'wb') as f:
                    f.write(response.content)

                # Extract zip content
                unity_explorer_folder = os.path.join(self.game_folder, "UnityExplorer")
                with zipfile.ZipFile(unity_explorer_zip, 'r') as zip_ref:
                    zip_ref.extractall(unity_explorer_folder)

                # Move Unity Explorer files to BepInEx/plugins
                bepinex_plugins_folder = os.path.join(self.game_folder, "BepInEx", "plugins")
                os.makedirs(bepinex_plugins_folder, exist_ok=True)

                for root, dirs, files in os.walk(unity_explorer_folder):
                    for file in files:
                        shutil.move(os.path.join(root, file), bepinex_plugins_folder)

                print("Unity Explorer installed successfully!")

                # Optional: Remove the downloaded zip file and the empty UnityExplorer folder
                os.remove(unity_explorer_zip)
                os.rmdir(unity_explorer_folder)

            else:
                print(f"Failed to download Unity Explorer. Status code: {response.status_code}")

        except Exception as e:
            messagebox.showerror("Installation Error", f"Error installing Unity Explorer: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    mod_manager = ModManager(root)
    root.mainloop()
