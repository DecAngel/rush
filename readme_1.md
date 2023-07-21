# 课题四后端服务器


# 安装
1. 安装python3.9并新建虚拟环境
    ```shell
    virtualenv .venv
    source .venv/bin/activate
    ```
2. 安装pytorch==2.0.1
    ```shell
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
    ```
3. 安装timm、pytorch-geometric、tensorboardX、matplotlib、opencv-python、pandas、skimage
    ```shell
    python -m pip install timm torch-geometric tensorboardX matplotlib opencv-python pandas scikit-image
    ```
4. 安装flask、flask_cors、flask-apscheduler
   ```shell
   python -m pip install flask flask_cors flask-apscheduler
   ```
