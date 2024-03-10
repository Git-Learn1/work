import os
import requests
import customtkinter  # type: ignore
import webbrowser
import shutil
from threading import Thread
from CTkMessagebox import CTkMessagebox  # type: ignore
from customtkinter import CTkProgressBar, CTkLabel  # type: ignore

python_exe_path = ""
tip = "安装/更新完成！"

def install_python(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master):
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
    
def install_git(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master):
    CTkMessagebox(title="警告", message="未找到 Git，将自动安装！", icon="warning")
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

def install_venv(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master):
    global python_exe_path
    os.environ["path"] = f"{install_path}/git/bin;{install_path}/venv/Scripts;"+os.environ["path"]
    fp_list = [os.popen(f"{install_path}/venv/Scripts/python.exe -V"), os.popen(f"{install_path}/venv/python.exe -V")]
    for i in fp_list:
        if i.read().startswith("Python 3.10"):
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
    os.system(f"{python_exe_path} -m pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple")
    os.system(f"{python_exe_path} -m pip install -U pip setuptools wheel IPython pickleshare -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"{python_exe_path} -m pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 -i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://download.pytorch.org/whl/cu118")
        
def install_sd(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master):
    global python_exe_path
    install_venv(install_path, progress_bar, progress_label, master)
    if os.system("git --version") and os.system(f"{install_path}/git/bin/git.exe --version"):
        t = Thread(target=install_git, args=(install_path, progress_bar, progress_label, master))
        t.start()
        return
    git_exe_path = "git" if os.system("git --version") == 0 else f"{install_path}/git/bin/git.exe"
    os.system(f"{git_exe_path} clone https://gitee.com/stable_diffusion/stable-diffusion-webui.git {install_path}/sd --depth=1")
    os.chdir(f"{install_path}/sd")
    os.system("git pull")
    os.system(f"{python_exe_path} -m pip install -r {install_path}/sd/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"{python_exe_path} -m pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 xformers -i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://download.pytorch.org/whl/cu118")
    os.chdir(f"{install_path}/sd")
    with open("webui-user.bat", "r", encoding="utf-8") as f:
        a = f.readlines()
    a[2] = f"set PYTHON={install_path}/venv/Scripts/python.exe\n"
    a[3] = f"set GIT={git_exe_path}\n"
    a[4] = f"set VENV_DIR={install_path}/venv/\n"
    a[5] = "call webui.bat --xformers\n"
    with open("webui-user.bat", "w", encoding="utf-8") as f:
        f.writelines(a)
    start_btn = customtkinter.CTkButton(master, text="启动", command=lambda:(webbrowser.open("https://tags.novelai.dev"),os.system("start cmd /k webui-user.bat")))
    start_btn.grid(row=5, column=4)
    CTkMessagebox(title="成功", message=tip, icon="info")
    
def install_sovits(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master):
    global python_exe_path
    if os.path.exists(f"{install_path}/.cache") and not os.path.exists(f"{os.environ['USERPROFILE']}/.cache"):
        shutil.copytree(f"{install_path}/.cache", f"{os.environ['USERPROFILE']}/.cache")
    install_venv(install_path, progress_bar, progress_label, master)
    os.system(f"{python_exe_path} -m pip install so-vits-svc-fork \"pysimplegui<5\" -U -i https://pypi.tuna.tsinghua.edu.cn/simple")
    if not os.path.exists(f"{install_path}/sovits"):
        os.mkdir(f"{install_path}/sovits")
    os.chdir(f"{install_path}/sovits")
    master.start_installation.grid(row=5, column=2)
    start_btn = customtkinter.CTkButton(master, text="启动命令行", command=lambda:os.system("start cmd"))
    start_btn.grid(row=5, column=3)
    infer_btn = customtkinter.CTkButton(master, text="一键训练", command=lambda:(os.system("svc pre-split"),os.system("svc pre-resample"),os.system("svc pre-config"),os.system("svc pre-hubert"),os.system("svc train")))
    infer_btn.grid(row=5, column=4)
    gui_btn = customtkinter.CTkButton(master, text="GUI推理", command=lambda:os.system("svc gui"))
    gui_btn.grid(row=5, column=5)
    master.widgets.append(start_btn)
    master.widgets.append(infer_btn)
    master.widgets.append(gui_btn)
    CTkMessagebox(title="注意", message=tip+"\n推理前请确保文件如下所示\n安装目录/sovits/dataset_raw_raw/{你想给这个音色取得名字}/{音频文件}.wav\n若遇到网络问题 (huggingface 被墙) 请用完全品！\n要推出训练请按Ctrl+C", icon="info")
    
def install_yolo(install_path: str, progress_bar: CTkProgressBar, progress_label: CTkLabel, master):
    global python_exe_path
    install_venv(install_path, progress_bar, progress_label, master)
    os.system(f"{python_exe_path} -m pip install ultralytics -U -i https://pypi.tuna.tsinghua.edu.cn/simple")
    start_btn = customtkinter.CTkButton(master, text="启动命令行", command=lambda:(webbrowser.open("https://docs.ultralytics.com/zh/quickstart/"), webbrowser.open("https://docs.ultralytics.com/zh/modes/predict/"), os.system(f"start {python_exe_path} -m IPython")))
    start_btn.grid(row=5, column=4)
    os.chdir(f"{install_path}")
    master.widgets.append(start_btn)
    CTkMessagebox(title="成功", message=tip, icon="info")
