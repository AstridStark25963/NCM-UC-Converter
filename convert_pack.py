import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import threading
from ttkthemes import ThemedTk
import base64
import os

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
    file_paths = filedialog.askopenfilenames(
        title="选择文件", filetypes=[("网易云缓存文件", "*.uc")]
    )
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

# 将图标文件内容转换成base64字符串
icon_data = """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"""

# 创建临时文件保存图标
temp_icon_path = "temp_icon.ico"
with open(temp_icon_path, "wb") as temp_icon:
    temp_icon.write(base64.b64decode(icon_data))

def on_close():
    # 在窗口关闭时删除临时文件
    if os.path.exists(temp_icon_path):
        os.remove(temp_icon_path)
    root.destroy()

# 创建主窗口，使用ThemedTk
root = ThemedTk(theme="arc")  # 选择主题，"arc"是一种现代化的主题
root.title("网易云缓存文件转码工具")
root.geometry("400x300")  # 设置窗口大小

# 设置窗口图标，使用临时文件
root.iconbitmap(temp_icon_path)

# 绑定关闭窗口时的回调函数
root.protocol("WM_DELETE_WINDOW", on_close)

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

# 运行主循环
root.mainloop()
