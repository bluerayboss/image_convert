import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import os, subprocess
from converter import convert_webp_to_gif_animated

SUPPORTED_FORMATS = ['webp', 'gif', 'jpg', 'png']

HACKER_GREEN = "#00FF00"
HACKER_BG = "#0d0d0d"
HACKER_DARK = "#1a1a1a"
HACKER_ACCENT = "#39FF14"

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ 이미지 포맷 변환기")
        self.root.geometry("400x400")
        self.root.configure(bg=HACKER_BG)

        self.file_paths = []
        self.last_output_dir = ""
        self.log_lines = []

        self.setup_ui()

    def setup_ui(self):
        self.url_var = tk.StringVar()
        self.source_var = tk.StringVar()
        self.target_var = tk.StringVar()
        self.filename_var = tk.StringVar()

        tk.Label(self.root, text="이미지 변환 프로그램", font=("Arial", 14, "bold"), fg=HACKER_GREEN, bg=HACKER_BG).pack(pady=10)

        self.url_entry = tk.Entry(self.root, textvariable=self.url_var, fg=HACKER_GREEN, bg=HACKER_DARK, insertbackground=HACKER_GREEN)
        self.url_entry.pack(padx=10, fill='x')
        self.url_entry.insert(0, "URL 입력 (선택사항)")

        tk.Button(self.root, text="이미지 열기", command=self.open_files, fg=HACKER_GREEN, bg=HACKER_DARK, activebackground=HACKER_ACCENT).pack(pady=10)

        combo = tk.Frame(self.root, bg=HACKER_BG)
        combo.pack()

        self.source_combo = ttk.Combobox(combo, textvariable=self.source_var, state='readonly')
        self.source_combo['values'] = SUPPORTED_FORMATS
        self.source_combo.pack(side='left', padx=(10, 5))

        tk.Label(combo, text="→", fg=HACKER_GREEN, bg=HACKER_BG).pack(side='left')

        self.target_combo = ttk.Combobox(combo, textvariable=self.target_var, state='readonly')
        self.target_combo['values'] = SUPPORTED_FORMATS
        self.target_combo.pack(side='left', padx=(5, 10))

        tk.Label(self.root, text="저장될 파일 이름", fg=HACKER_GREEN, bg=HACKER_BG).pack(pady=(10, 2))
        self.filename_entry = tk.Entry(self.root, textvariable=self.filename_var, fg=HACKER_GREEN, bg=HACKER_DARK, insertbackground=HACKER_GREEN)
        self.filename_entry.pack(padx=10, fill='x')

        btns = tk.Frame(self.root, bg=HACKER_BG)
        btns.pack(pady=10)
        tk.Button(btns, text="변 환", width=10, command=self.convert_images, fg=HACKER_GREEN, bg=HACKER_DARK).pack(side='left', padx=5)
        tk.Button(btns, text="폴더 열기", width=10, command=self.open_output_folder, fg=HACKER_GREEN, bg=HACKER_DARK).pack(side='left', padx=5)

        self.log_box = tk.Text(self.root, height=10, fg=HACKER_GREEN, bg=HACKER_DARK)
        self.log_box.pack(padx=10, pady=10, fill='both')
        self.log_box.insert(tk.END, "[로그 시작]\n")
        self.log_box.config(state='disabled')

    def log(self, msg):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')

    def open_files(self):
        paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.webp")])
        if paths:
            self.file_paths = list(paths)
            ext = os.path.splitext(paths[0])[1].lower().replace('.', '')
            if ext in SUPPORTED_FORMATS:
                self.source_var.set(ext)
                self.log(f"[선택됨] {len(paths)}개 파일")

    def open_output_folder(self):
        if self.last_output_dir and os.path.isdir(self.last_output_dir):
            subprocess.run(['explorer', self.last_output_dir], check=False)
        else:
            self.log("[알림] 열 수 있는 폴더가 없습니다.")

    def convert_images(self):
        src = self.source_var.get()
        dst = self.target_var.get()
        base = self.filename_var.get().strip()

        if not dst or not self.file_paths:
            self.log("[오류] 포맷 또는 파일이 없습니다.")
            return

        try:
            for i, path in enumerate(self.file_paths):
                name = f"{base}_{i+1}.{dst}" if base else f"image{i+1}.{dst}"
                directory = os.path.dirname(path)
                save_path = os.path.join(directory, name)

                if src == "webp" and dst == "gif":
                    convert_webp_to_gif_animated(path, save_path)
                else:
                    with Image.open(path) as img:
                        img.convert("RGB").save(save_path, dst.upper())

                self.last_output_dir = directory
                self.log(f"[완료] {path} → {save_path}")

            self.log("[성공] 변환 완료.")
        except Exception as e:
            self.log(f"[에러] {e}")

