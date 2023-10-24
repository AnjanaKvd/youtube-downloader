import tkinter as tk
from tkinter import filedialog
import pyperclip
from downloader import YouTubeDownloader

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        
        self.video_url_label = tk.Label(root, text="Enter YouTube Video URL:")
        self.video_url_label.pack()

        self.video_url_entry = tk.Entry(root, width=40)
        self.video_url_entry.pack()

        self.paste_button = tk.Button(root, text="Paste", command=self.paste_clipboard)
        self.paste_button.pack()

        self.quality_label = tk.Label(root, text="Select Video Quality:")
        self.quality_label.pack()

        self.quality_var = tk.StringVar(root)
        self.quality_var.set("Highest Resolution")  # Default quality

        self.quality_menu = tk.OptionMenu(root, self.quality_var, "Highest Resolution", "720p", "480p", "360p")
        self.quality_menu.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack()

        self.download_button = tk.Button(root, text="Download Video", command=self.download_video)
        self.download_button.pack()

        self.downloading_label = tk.Label(root, text="")
        self.downloading_label.pack()

    def paste_clipboard(self):
        clipboard_data = pyperclip.paste()
        self.video_url_entry.delete(0, tk.END)
        self.video_url_entry.insert(0, clipboard_data)

    def browse_folder(self):
        download_folder = filedialog.askdirectory()
        if download_folder:
            self.download_path = download_folder

    def download_video(self):
        video_url = self.video_url_entry.get()
        downloader = YouTubeDownloader(video_url)

        # Map user-selected quality to PyTube stream filter
        quality_map = {
            "Highest Resolution": "highest",
            "720p": "720p",
            "480p": "480p",
            "360p": "360p"
        }
        selected_quality = self.quality_var.get()

        if selected_quality in quality_map:
            stream = downloader.yt.streams.filter(res=quality_map[selected_quality])[-1]
        else:
            stream = downloader.yt.streams.get_highest_resolution()

        if hasattr(self, 'download_path'):
            download_path = self.download_path
        else:
            download_path = "./"  # Default is the current directory

        downloader.show_video_details()

        self.downloading_label.config(text="Downloading...")
        self.root.update_idletasks()

        try:
            stream.download(output_path=download_path)
            self.downloading_label.config(text="Download complete.")
        except Exception as e:
            self.downloading_label.config(text=f"Download failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
