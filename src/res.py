import os

condarc = """channels:
  - defaults
  - conda-forge
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  deepmodeling: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/
"""

def video_infer(video_path, install_path, python_exe_path):
    var = f"""from ultralytics import YOLO
import cv2
import os
model = YOLO('yolov8n.pt')
video_path = "{video_path}"
cap = cv2.VideoCapture(video_path)
i = 0
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc(*"XVID")
writer = cv2.VideoWriter("{install_path}/yolo/result.mp4", fourcc, fps, size, True)
if not os.path.exists("{install_path}/yolo/result"):os.mkdir("{install_path}/yolo/result")
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow('推理结果', annotated_frame)
        cv2.imwrite("{install_path}/yolo/result/%d.png"%i, annotated_frame)
        writer.write(annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    i+=1
cap.release()
writer.release()
cv2.destroyAllWindows()
"""
    with open(f"{install_path}\\yolo\\video_infer.py", "w", encoding="utf-8") as f:
        f.write(var)
    os.system(f"{python_exe_path} {install_path}\\yolo\\video_infer.py")
