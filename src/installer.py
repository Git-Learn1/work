import os
import requests
import customtkinter  # type: ignore
import webbrowser
import shutil
import rich
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from CTkMessagebox import CTkMessagebox  # type: ignore
from res import condarc, video_infer

python_exe_path = ""
cuda_flag = False
tip = "安装/更新完成！"
text_column = "[progress.description]{task.description}"
text_column_2 = "[progress.percentage]{task.percentage:>3.0f}%"

def download_file(install_path, url, save_name):
    r = requests.get(url, stream=True)
    with open(f"{install_path}\\{save_name}", "wb") as fp:
        with Progress(TextColumn(text_column), BarColumn(), TextColumn(text_column_2), TimeRemainingColumn(), TimeElapsedColumn()) as progress:
            total_length = int(r.headers.get("content-length"))  # type: ignore
            percent_tqdm = progress.add_task(description="下载进度", total=100)
            for ch in r.iter_content(chunk_size=round(total_length/100)):
                if ch:
                    fp.write(ch)
                    progress.advance(percent_tqdm, advance=1)

def install_venv(install_path: str):
    global python_exe_path, cuda_flag
    os.environ["path"] = f"{install_path};"+os.environ["path"]
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    rich.print("正在安装环境，请稍后...")
    if os.system("micromamba")!=0:
        download_file(install_path, "https://mirror.ghproxy.com/https://github.com/mamba-org/micromamba-releases/releases/download/1.5.8-0/micromamba-win-64", "micromamba.exe")
    with open(f"{install_path}\\.condarc", "w", encoding="utf-8") as f:
        f.write(condarc)
    i = os.popen(f"{install_path}\\envs\\venv\\python.exe -V")
    python_flag = False
    if i.read().startswith("Python 3.10"):
        python_flag = True
    i.close()
    if not python_flag:
        os.system(f"micromamba -r {install_path} create -n venv python=3.10 -c conda-forge -y")
    python_exe_path = f"micromamba -r {install_path} run -n venv python"
    os.system(f"{python_exe_path} -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"{python_exe_path} -m pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 xformers==0.0.25 -f https://mirror.sjtu.edu.cn/pytorch-wheels/cu118/torch_stable.html")
    i = os.popen(f"""{python_exe_path} -c "import torch;print(torch.cuda.is_available())" """)
    j = os.popen(f"""{python_exe_path} -c "import torch;print(torch.__version__)" """)
    if i.read().startswith("True"):cuda_flag = True
    elif j.read().endswith("+cu118"):os.system(f"{python_exe_path} -m pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 xformers==0.0.25 -i https://pypi.tuna.tsinghua.edu.cn/simple --force-reinstall")
    i.close()
    j.close()

def install_sd(install_path: str, master):
    global python_exe_path
    install_path = "".join(["\\" if i == "/" else i for i in list(install_path)])
    install_venv(install_path)
    if not os.path.exists(f"{install_path}\\envs\\venv\\Library\\bin\\git.exe"):os.system(f"micromamba -r {install_path} -n venv install git -y")
    git_exe_path = f"micromamba -r {install_path} run -n venv git"
    os.system(f"{python_exe_path} -m pip install git+https://gitee.com/aa46/CLIP.git --verbose")
    os.system(f"{python_exe_path} -m pip install git+https://gitee.com/aa46/invisible-watermark.git --verbose")
    os.system(f"{python_exe_path} -m pip install https://mirror.ghproxy.com/https://github.com/Gourieff/Assets/raw/main/Insightface/insightface-0.7.3-cp310-cp310-win_amd64.whl --prefer-binary --verbose")
    os.system(f"{git_exe_path} clone https://gitee.com/aa46/stable-diffusion-webui.git {install_path}\\sd --depth=1 --recursive")
    os.chdir(f"{install_path}/sd")
    os.system(f"{git_exe_path} pull")
    os.system(f"{git_exe_path} submodule update --init --recursive")
    os.system(f"{python_exe_path} -m pip install -r {install_path}\\sd\\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.chdir(f"{install_path}\\sd")
    a = ["@echo off\n", "\n", "\n", "\n", "\n", "\n"]
    a[2] = f"set PYTHON={install_path}\\envs\\venv\\python.exe\n"
    a[3] = f"set GIT={install_path}\\envs\\venv\\Library\\bin\\git.exe\n"
    a[4] = "set VENV_DIR=\n"
    a[5] = "%PYTHON% launch.py --xformers\n"
    if not cuda_flag:
        a[5] = "%PYTHON% launch.py --xformers --skip-torch-cuda-test --use-cpu all --precision full --no-half\n"
    with open("webui-user.bat", "w", encoding="utf-8") as f:
        f.writelines(a)
    start_btn = customtkinter.CTkButton(master, text="启动", command=lambda:(webbrowser.open("https://tags.novelai.dev"),os.system("start cmd /k webui-user.bat")))
    start_btn.grid(row=5, column=4)
    master.widgets.append(start_btn)
    CTkMessagebox(title="成功", message=tip+"\n注：因配置原因，部分电脑可能无法成功运行", icon="info")
    
def install_sovits(install_path: str, master):
    global python_exe_path
    install_path = "".join(["\\" if i == "/" else i for i in list(install_path)])
    install_venv(install_path)
    os.system(f"{python_exe_path} -m pip install so-vits-svc-fork \"pysimplegui<5\" -U -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"{python_exe_path} -m pip install so-vits-svc-fork --no-deps --force-reinstall -U -i https://pypi.tuna.tsinghua.edu.cn/simple")
    if not os.path.exists(f"{install_path}\\sovits"):
        os.mkdir(f"{install_path}\\sovits")
    os.chdir(f"{install_path}\\sovits")
    scripts_path = f"micromamba -r {install_path} run -n venv "
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
    if not os.path.exists(f"{install_path}\\yolo"):os.mkdir(f"{install_path}\\yolo")
    os.chdir(f"{install_path}\\yolo")
    if not os.path.exists(f"{install_path}\\yolo\\yolov8n.pt"):download_file(f"{install_path}\\yolo", "https://mirror.ghproxy.com/https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt", "yolov8n.pt")
    master.start_installation.grid(row=5, column=2)
    start_btn = customtkinter.CTkButton(master, text="启动命令行", command=lambda:(webbrowser.open("https://docs.ultralytics.com/zh/quickstart/"), webbrowser.open("https://docs.ultralytics.com/zh/modes/predict/"), os.system(f"start {python_exe_path} -m IPython")))
    start_btn.grid(row=5, column=3)
    video_btn = customtkinter.CTkButton(master, text="视频推理", command=lambda:video_infer(customtkinter.filedialog.askopenfilename(title='选择你要处理的视频文件', filetypes=[('视频文件', '*.mp4')]),"".join(["/" if i == "\\" else i for i in list(install_path)]),python_exe_path))
    video_btn.grid(row=5, column=4)
    master.widgets.append(start_btn)
    master.widgets.append(video_btn)
    CTkMessagebox(title="成功", message=tip, icon="info")
