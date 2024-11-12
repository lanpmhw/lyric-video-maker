import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from video_generator import generate_lyric_video

class LyricVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("动态歌词视频生成器")
        self.root.geometry("900x600")

        self.lrc_file = None
        self.output_file = None

        # LRC文件选择按钮和文本框
        self.lrc_button = tk.Button(self.root, text="选择LRC文件", command=self.select_lrc_file)
        self.lrc_button.place(x=50, y=50, width=120, height=30)

        self.lrc_textbox = tk.Entry(self.root, width=40)
        self.lrc_textbox.place(x=180, y=50, width=250, height=30)

        # 输出文件路径选择按钮和文本框
        self.output_button = tk.Button(self.root, text="选择输出视频路径", command=self.select_output_file)
        self.output_button.place(x=50, y=100, width=120, height=30)

        self.output_textbox = tk.Entry(self.root, width=40)
        self.output_textbox.place(x=180, y=100, width=250, height=30)

        # 生成视频按钮
        self.generate_button = tk.Button(self.root, text="生成视频", command=self.start_video_generation)
        self.generate_button.place(x=50, y=150, width=120, height=30)

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(self.root, variable=self.progress_var, from_=0, to=100, orient="horizontal", length=400)
        self.progress_bar.place(x=50, y=200)

    def select_lrc_file(self):
        self.lrc_file = filedialog.askopenfilename(title="选择LRC文件", filetypes=[("LRC Files", "*.lrc")])
        if self.lrc_file:
            self.lrc_textbox.delete(0, tk.END)
            self.lrc_textbox.insert(0, self.lrc_file)

    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])
        if self.output_file:
            self.output_textbox.delete(0, tk.END)
            self.output_textbox.insert(0, self.output_file)

    def update_progress(self, progress):
        self.progress_var.set(progress)
        self.root.update_idletasks()  # 强制更新进度条

    def start_video_generation(self):
        if not self.lrc_file or not self.output_file:
            messagebox.showerror("错误", "请先选择LRC文件和输出路径")
            return

        # 启动后台线程执行视频生成
        threading.Thread(target=self.generate_video).start()

    def generate_video(self):
        try:
            generate_lyric_video(self.lrc_file, self.output_file, progress_callback=self.update_progress)
            messagebox.showinfo("完成", "视频生成成功！")
        except Exception as e:
            messagebox.showerror("错误", f"视频生成失败：{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricVideoApp(root)
    root.mainloop()

