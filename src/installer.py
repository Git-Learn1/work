import os
import requests
import customtkinter  # type: ignore
import time
from threading import Thread
from CTkMessagebox import CTkMessagebox  # type: ignore
from customtkinter import CTkProgressBar, CTkLabel, CTk  # type: ignore

python_exe_path = ""

def install_pytorch():
    CTkMessagebox(title="提示", message="目前正在安装，程序会假死，注意留意控制台内容", icon="info")

def install_python(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master: CTk):
    CTkMessagebox(title="警告", message="未找到 Python 3.10！将自动安装", icon="warning")
    r = requests.get("https://registry.npmmirror.com/-/binary/python/3.10.11/python-3.10.11-amd64.exe", stream=True)
    with open("python-3.10.11-amd64.exe", "wb") as fp:
        total_length = int(r.headers.get("content-length"))  # type: ignore
        progress_bar.configure(width=600)
        progress_bar.set(0)
        progress_bar.grid(row=4, column=1, columnspan=5)
        progress_label.grid(row=4, column=5)
        i = 0
        for ch in r.iter_content(chunk_size=round(total_length/100)):
            if ch:
                fp.write(ch)
                progress_bar.set((i+1)/100)
                progress_label.configure(text=f"{i}%/100%")
                i += 1
        progress_bar.grid_forget()
        progress_label.grid_forget()
    os.system(f"python-3.10.11-amd64.exe /passive Shortcuts=0 Include_doc=0 TargetDir={install_path}/venv")
    install_venv(install_path, progress_bar, progress_label, master)
    
def install_git(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master: CTk):
    CTkMessagebox(title="警告", message="未找到 Python 3.10！将自动安装", icon="warning")
    r = requests.get("https://registry.npmmirror.com/-/binary/git-for-windows/v2.44.0.windows.1/Git-2.44.0-64-bit.exe", stream=True)
    with open("git.exe", "wb") as fp:
        total_length = int(r.headers.get("content-length"))  # type: ignore
        progress_bar.configure(width=600)
        progress_bar.set(0)
        progress_bar.grid(row=4, column=1, columnspan=5)
        progress_label.grid(row=4, column=5)
        i = 0
        for ch in r.iter_content(chunk_size=round(total_length/100)):
            if ch:
                fp.write(ch)
                progress_bar.set((i+1)/100)
                progress_label.configure(text=f"{i}%/100%")
                i += 1
        progress_bar.grid_forget()
        progress_label.grid_forget()
    os.system(f"git.exe /passive /NOCANCEL /NORESTART /FORCECLOSEAPPLICATIONS /DIR={install_path}/git")
    install_sd(install_path, progress_bar, progress_label, master)

def install_venv(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master: CTk):
    global python_exe_path
    fp_list = [os.popen(f"{install_path}/venv/Scripts/python.exe -V"), os.popen(f"{install_path}/venv/python.exe -V")]
    for i in fp_list:
        if i.read().startswith("Python 3.10"):
            CTkMessagebox(title="提示", message="找到 Python 3.10", icon="info")
            python_exe_path = i.read()
        for j in fp_list: j.close()
        break
    if not python_exe_path and os.system("py -3.10 -c \"exit(0)\"") != 0:
        t1 = Thread(target=install_python, args=(install_path, progress_bar, progress_label, master))  # type: ignore
        t1.start()  # type: ignore
        return
    else:
        os.system(f"py -3.10 -m venv {install_path}/venv/")
        python_exe_path = f"{install_path}/venv/Scripts/python.exe"
    t = Thread(target=install_pytorch)
    t.start()
    os.system(f"{python_exe_path} -m pip install -U pip setuptools wheel")
    os.system(f"{python_exe_path} -m pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://download.pytorch.org/whl/cu121")
        
def install_sd(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master: CTk):
    global python_exe_path
    install_venv(install_path, progress_bar, progress_label, master)
    if os.system("git --version") and os.system(f"{install_path}/git/bin/git.exe --version"):
        CTkMessagebox(title="警告", message="未找到 Git，将自动安装！", icon="warning")
        install_git(install_path, progress_bar, progress_label, master)
    os.environ["path"] += f";{install_path}/git/bin"
    os.system(f"git clone https://gitee.com/stable_diffusion/stable-diffusion-webui.git {install_path}/sd --depth=1")
    os.chdir(f"{install_path}/sd")
    os.system("git pull")
    os.system(f"{python_exe_path} -m pip install -r {install_path}/sd/requirements.txt -U -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"{python_exe_path} -m pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://download.pytorch.org/whl/cu121")
    CTkMessagebox(title="成功", message="安装/更新完成！", icon="info")
    
def install_sovits(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master: CTk):
    global python_exe_path
    install_venv(install_path, progress_bar, progress_label, master)
    os.system(f"{python_exe_path} -m pip install so-vits-svc-fork -U")
    
def install_yolo(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master: CTk):
    global python_exe_path
    install_venv(install_path, progress_bar, progress_label, master)
    os.system(f"{python_exe_path} -m pip install ultralytics -U")
