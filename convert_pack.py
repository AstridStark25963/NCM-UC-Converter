import os
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from ttkthemes import ThemedTk


def xor_encrypt(file_path):
    with open(file_path, "rb") as f:
        content = bytearray(f.read())

    for i in range(len(content)):
        content[i] ^= 163

    # Check the file header to determine the file type
    file_header = content[:4].hex()
    if file_header == "664c6143":  # Check if the file header is "fLaC" in hexadecimal
        output_file_path = file_path + ".flac"
    else:
        output_file_path = file_path + ".mp3"

    with open(output_file_path, "wb") as f:
        f.write(bytes(content))


def choose_file():
    file_paths = filedialog.askopenfilenames(title="选择文件", filetypes=[("网易云缓存文件", "*.uc")])
    for file_path in file_paths:
        file_listbox.insert(tk.END, file_path)


def start_conversion():
    files = file_listbox.get(0, tk.END)
    total_files = len(files)

    if total_files == 0:
        messagebox.showwarning("警告", "请先选择文件")
        return

    def conversion_worker(file_path, index):
        xor_encrypt(file_path)
        progress = (index + 1) / total_files * 100
        progress_var.set(progress)

    def check_progress():
        completed_threads = sum(thread.is_alive() == False for thread in threads)
        if completed_threads == total_files:
            progress_var.set(100)
            messagebox.showinfo("完成", "文件转换完成")
        else:
            root.after(100, check_progress)

    threads = []
    for index, file_path in enumerate(files):
        thread = threading.Thread(target=conversion_worker, args=(file_path, index))
        threads.append(thread)
        thread.start()

    root.after(100, check_progress)


def on_close():
    root.destroy()


# 创建主窗口，使用ThemedTk
root = ThemedTk(theme="arc")  # 选择主题，"arc"是一种现代化的主题
root.title("网易云缓存文件转码工具")
root.geometry("400x300")  # 设置窗口大小

# 选择文件按钮，使用ttk.Button
choose_button = ttk.Button(root, text="选择文件", command=choose_file)
choose_button.pack(pady=10)

# 文件列表框，使用ttk.Listbox
file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5, width=50)
file_listbox.pack(pady=10)

# 开始转换按钮，使用ttk.Button
start_button = ttk.Button(root, text="开始转换", command=start_conversion)
start_button.pack(pady=10)

# 进度条，使用ttk.Progressbar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, length=300, mode="determinate")
progress_bar.pack(pady=10)

# 设置窗口图标
icon_path = os.path.join(os.path.dirname(__file__), "music.ico")
root.iconbitmap(icon_path)

# 绑定关闭窗口时的回调函数
root.protocol("WM_DELETE_WINDOW", on_close)

# 运行主循环
root.mainloop()
