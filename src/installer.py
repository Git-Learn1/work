import os
import requests
import customtkinter  # type: ignore
import webbrowser
import shutil
import rich
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from CTkMessagebox import CTkMessagebox  # type: ignore

python_exe_path = ""
cuda_flag = False
tip = "安装/更新完成！"
text_column = "[progress.description]{task.description}"
text_column_2 = "[progress.percentage]{task.percentage:>3.0f}%"

def install_python(install_path: str):
    r = requests.get("https://registry.npmmirror.com/-/binary/python/3.10.11/python-3.10.11-amd64.exe", stream=True)
    with open("python-3.10.11-amd64.exe", "wb") as fp:
        with Progress(TextColumn(text_column), BarColumn(), TextColumn(text_column_2), TimeRemainingColumn(), TimeElapsedColumn()) as progress:
            total_length = int(r.headers.get("content-length"))  # type: ignore
            percent_tqdm = progress.add_task(description="下载进度", total=100)
            for ch in r.iter_content(chunk_size=round(total_length/100)):
                if ch:
                    fp.write(ch)
                    progress.advance(percent_tqdm, advance=1)
    os.system(f"python-3.10.11-amd64.exe /passive Shortcuts=0 Include_doc=0 TargetDir={install_path}\\py")
    
def install_git(install_path: str):
    r = requests.get("https://registry.npmmirror.com/-/binary/git-for-windows/v2.44.0.windows.1/Git-2.44.0-64-bit.exe", stream=True)
    with open("git-installer.exe", "wb") as fp:
        with Progress(TextColumn(text_column), BarColumn(), TextColumn(text_column_2), TimeRemainingColumn(), TimeElapsedColumn()) as progress:
            total_length = int(r.headers.get("content-length"))  # type: ignore
            percent_tqdm = progress.add_task(description="下载进度", total=100)
            for ch in r.iter_content(chunk_size=round(total_length/100)):
                if ch:
                    fp.write(ch)
                    progress.advance(percent_tqdm, advance=1)
    os.system(f"git-installer.exe /SILENT /NOCANCEL /NORESTART /FORCECLOSEAPPLICATIONS /DIR={install_path}/git")

def install_vc():
    r = requests.get("https://aka.ms/vs/17/release/vc_redist.x64.exe", stream=True)
    with open("vc_redist.exe", "wb") as fp:
        with Progress(TextColumn(text_column), BarColumn(), TextColumn(text_column_2), TimeRemainingColumn(), TimeElapsedColumn()) as progress:
            total_length = int(r.headers.get("content-length"))  # type: ignore
            percent_tqdm = progress.add_task(description="下载进度", total=100)
            for ch in r.iter_content(chunk_size=round(total_length/100)):
                if ch:
                    fp.write(ch)
                    progress.advance(percent_tqdm, advance=1)
    os.system(f"vc_redist.exe /passive /norestart")

def install_venv(install_path: str):
    global python_exe_path, cuda_flag
    try:install_vc()
    except:rich.print("若未安装 Visual C++ 运行库，请手动下载安装！https://aka.ms/vs/17/release/vc_redist.x64.exe")
    os.environ["path"] = f"{install_path}\\git\\bin;{install_path}\\venv\\Scripts;"+os.environ["path"]
    fp_list = [os.popen(f"{install_path}\\venv\\Scripts\\python.exe -V"), os.popen(f"{install_path}\\venv\\python.exe -V")]
    for i in fp_list:
        if i.read().startswith("Python 3.10"):
            python_exe_path = i.read()
            break
    for i in fp_list: i.close()
    if not python_exe_path and os.system("py -3.10 -c \"exit(0)\"") != 0:
        install_python(install_path)
        os.system(f"{install_path}\\py\\python.exe -m venv {install_path}\\venv\\")
        python_exe_path = f"{install_path}\\venv\\Scripts\\python.exe"
    elif not python_exe_path:
        os.system(f"py -3.10 -m venv {install_path}\\venv\\")
        python_exe_path = f"{install_path}\\venv\\Scripts\\python.exe"
    if os.path.exists(f"{install_path}\\venv\\pyvenv.cfg"):
        with open(f"{install_path}\\venv\\pyvenv.cfg", "r", encoding="utf-8") as f:
            a = f.readlines()
        
        if os.path.exists(f"{install_path}\\venv\\py"):
            a[0] = f"home = {install_path}\\venv\\py\n"
        else:
            fa = os.popen(f"""py -3.10 -c "import sys;print(sys.executable)" """)
            s = os.path.split(fa.read())[0]+"\n"
            fa.close()
            a[0] = f"home = {s}"
        with open(f"{install_path}\\venv\\pyvenv.cfg", "w", encoding="utf-8") as f:
            f.writelines(a)
    os.system(f"{python_exe_path} -m pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple")
    os.system(f"{python_exe_path} -m pip install -U pip setuptools wheel IPython pickleshare -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"{python_exe_path} -m pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 xformers -i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://download.pytorch.org/whl/cu118")
    fp_list = [os.popen(f"{install_path}\\venv\\Scripts\\python.exe -V"), os.popen(f"{install_path}\\venv\\python.exe -V")]
    i = os.popen(f"""{python_exe_path} -c "import torch;print(torch.cuda.is_available())" """)
    j = os.popen(f"""{python_exe_path} -c "import torch;print(torch.__version__)" """)
    if i.read().startswith("True"):cuda_flag = True
    elif j.read().endswith("+cu118"):os.system(f"{python_exe_path} -m pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 xformers -i https://pypi.tuna.tsinghua.edu.cn/simple -U --force-reinstall")
    i.close()
    j.close()

def install_sd(install_path: str, master):
    global python_exe_path
    install_path = "".join(["\\" if i == "/" else i for i in list(install_path)])
    install_venv(install_path) 
    if os.system("git --version") and os.system(f"{install_path}\\git\\bin\\git.exe --version"):
        install_git(install_path)
    git_exe_path = "git" if os.system("git --version") == 0 else f"{install_path}\\git\\bin\\git.exe"
    os.system(f"{git_exe_path} clone https://gitee.com/stable_diffusion/stable-diffusion-webui.git {install_path}\\sd --depth=1")
    os.chdir(f"{install_path}/sd")
    os.system("git pull")
    os.system(f"{python_exe_path} -m pip install -r {install_path}\\sd\\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple")
    if cuda_flag:
        # 没有 CUDA 还来跑什么 AI 啊，真的不嫌慢吗？？？
        os.system(f"{python_exe_path} -m pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 xformers -i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://download.pytorch.org/whl/cu118")
    else: os.system(f"{python_exe_path} -m pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 xformers -i https://pypi.tuna.tsinghua.edu.cn/simple -U")
    os.chdir(f"{install_path}\\sd")
    with open("webui-user.bat", "r", encoding="utf-8") as f:
        a = f.readlines()
    a[2] = f"set PYTHON={install_path}\\venv\\Scripts\\python.exe\n"
    a[3] = f"set GIT={git_exe_path}\n"
    a[4] = f"set VENV_DIR={install_path}\\venv\\\n"
    a[5] = "call webui.bat --xformers\n"
    if not cuda_flag:
        a[5] = "call webui.bat --xformers --skip-torch-cuda-test --use-cpu all --precision full --no-half\n"
    with open("webui-user.bat", "w", encoding="utf-8") as f:
        f.writelines(a)
    start_btn = customtkinter.CTkButton(master, text="启动", command=lambda:(webbrowser.open("https://tags.novelai.dev"),os.system("start cmd /k webui-user.bat")))
    start_btn.grid(row=5, column=4)
    master.widgets.append(start_btn)
    CTkMessagebox(title="成功", message=tip+"\n注：因配置原因，部分电脑无法成功运行", icon="info")
    
def install_sovits(install_path: str, master):
    global python_exe_path
    install_path = "".join(["\\" if i == "/" else i for i in list(install_path)])
    if os.path.exists(f"{install_path}\\.cache") and not os.path.exists(f"{os.environ['USERPROFILE']}\\.cache"):
        shutil.copytree(f"{install_path}\\.cache", f"{os.environ['USERPROFILE']}\\.cache")
    install_venv(install_path)
    os.system(f"{python_exe_path} -m pip install so-vits-svc-fork \"pysimplegui<5\" -U -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"{python_exe_path} -m pip install so-vits-svc-fork --no-deps --force-reinstall -U -i https://pypi.tuna.tsinghua.edu.cn/simple")
    if not os.path.exists(f"{install_path}\\sovits"):
        os.mkdir(f"{install_path}\\sovits")
    os.chdir(f"{install_path}\\sovits")
    scripts_path = f"{install_path}\\venv\\Scripts\\"
    master.start_installation.grid(row=5, column=2)
    start_btn = customtkinter.CTkButton(master, text="启动命令行", command=lambda:os.system("start cmd"))
    start_btn.grid(row=5, column=3)
    infer_btn = customtkinter.CTkButton(master, text="一键训练", command=lambda:(os.system(f"{scripts_path}svc pre-split"),os.system(f"{scripts_path}svc pre-resample"),os.system(f"{scripts_path}svc pre-config"),os.system(f"{scripts_path}svc pre-hubert"),os.system(f"{scripts_path}svc train")))
    infer_btn.grid(row=5, column=4)
    gui_btn = customtkinter.CTkButton(master, text="GUI推理", command=lambda:os.system("{scripts_path}svcg"))
    gui_btn.grid(row=5, column=5)
    master.widgets.append(start_btn)
    master.widgets.append(infer_btn)
    master.widgets.append(gui_btn)
    CTkMessagebox(title="注意", message=tip+"\n推理前请确保文件如下所示\n安装目录\\sovits\\dataset_raw_raw\\{你想给这个音色取得名字}\\{音频文件}.wav\n若遇到网络问题 (huggingface 被墙) 请用完全品！\n要推出训练请按Ctrl+C", icon="info")
    
def install_yolo(install_path: str, master):
    global python_exe_path
    install_path = "".join(["\\" if i == "/" else i for i in list(install_path)])
    install_venv(install_path)
    os.system(f"{python_exe_path} -m pip install ultralytics -U -i https://pypi.tuna.tsinghua.edu.cn/simple")
    start_btn = customtkinter.CTkButton(master, text="启动命令行", command=lambda:(webbrowser.open("https://docs.ultralytics.com/zh/quickstart/"), webbrowser.open("https://docs.ultralytics.com/zh/modes/predict/"), os.system(f"start {python_exe_path} -m IPython")))
    start_btn.grid(row=5, column=4)
    os.chdir(f"{install_path}")
    master.widgets.append(start_btn)
    CTkMessagebox(title="成功", message=tip, icon="info")
