## 1. 预处理西安地铁视频：

首先，将工作目录切换至项目根目录：/home/yuanyu/projects/rush/process_xian_video_for_VAD。然后按下述步骤操作

1. 将一个目录下的视频按 10 s 一个片段切分

    ```bash
    python clip_videos.py --src /home/yuanyu/projects/data/DaYanTa/8_C31/2021-04-29 --target /home/yuanyu/projects/data/DaYanTa_2/8_C31/tmp
    ```

2. 将切分后的视频片段转为图片文件夹

    ```bash
    python videos_to_frames.py --data_path /home/yuanyu/projects/data/DaYanTa_2/8_C31/tmp
    ```

## 2. 预处理标注文件：将对原始视频的标注转换为对图片文件夹的标注

    ```bash
    python resolve_label.py --src dyt_51_0429.csv --target label_dyt_51_0429.csv
    ```

## 3. （此步骤针对一个摄像头）根据预处理的标注文件，在某一路摄像头的经过预处理的地铁视频上，划分正常样本和异常样本，使用正常样本作为训练集训练一个模型

    进入项目 rush 的根目录 /home/yuanyu/projects/rush

1. 在 models/MNAD/configs.py 中增加相应摄像头的配置

2. 运行 Train_xian.py

    ```bash
    python -m models.MNAD.Train_xian --config config_8_C51
    ```