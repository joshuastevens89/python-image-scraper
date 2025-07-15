import os
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Supported extensions
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
VIDEO_EXTS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
MEDIA_EXTS = IMAGE_EXTS.union(VIDEO_EXTS)

class MediaScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Scraper")
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar()
        self.total_files = 0
        self.copied_files = 0

        self.setup_ui()

    def setup_ui(self):
        # Source folder
        tk.Label(self.root, text="Start folder:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.source_dir, width=60).pack()
        tk.Button(self.root, text="Browse...", command=self.browse_source).pack(pady=5)

        # Destination folder
        tk.Label(self.root, text="Destination folder:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.dest_dir, width=60).pack()
        tk.Button(self.root, text="Choose folder...", command=self.browse_dest).pack(pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=400, mode='determinate')
        self.progress.pack(pady=15)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Scan and Copy", command=self.start_scraping)
        self.start_button.pack()

    def browse_source(self):
        folder = filedialog.askdirectory(title="Select source directory")
        if folder:
            self.source_dir.set(folder)

    def browse_dest(self):
        folder = filedialog.askdirectory(title="Select destination folder")
        if folder:
            self.dest_dir.set(folder)

    def start_scraping(self):
        if not self.source_dir.get() or not self.dest_dir.get():
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return
        self.start_button.config(state='disabled')
        threading.Thread(target=self.scrape_files, daemon=True).start()

    def scrape_files(self):
        all_media_files = []
        for foldername, _, filenames in os.walk(self.source_dir.get()):
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in MEDIA_EXTS:
                    full_path = os.path.join(foldername, filename)
                    all_media_files.append(full_path)

        self.total_files = len(all_media_files)
        self.progress["maximum"] = self.total_files
        self.copied_files = 0

        for filepath in all_media_files:
            try:
                shutil.copy2(filepath, self.dest_dir.get())
                self.copied_files += 1
                self.progress["value"] = self.copied_files
            except Exception as e:
                print(f"Failed to copy {filepath}: {e}")

        messagebox.showinfo("Done", f"Copied {self.copied_files} files.")
        self.start_button.config(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaScraperApp(root)
    root.mainloop()
