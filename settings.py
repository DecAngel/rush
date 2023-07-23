from pathlib import Path


# Backend Settings
host = '0.0.0.0'
port = '5000'
mode = ['display', 'run'][1]

# Root Path
root_path = Path(__file__).parents[0]

# Demo Images Path
demo_images_path = root_path.joinpath('demo')

# Fire Detection
fire_image_dir = r'D:\datasets\data\dataset\fire'
fire_detection_model_dir = r'D:\datasets\data\models\fire'
fire_device = 0

# Video Anomaly Detection
vad_videos_dir = r'D:\datasets\data\dataset\VAD\ShanghaiTech\testing\frames'
vad_model_dir = r'D:\datasets\data\models\vad\shanghaitech\model.pth'
vad_mitems_dir = r'D:\datasets\data\models\vad\shanghaitech\keys.pt'
vad_xian_videos_dir = '/home/yuanyu/projects/data/DaYanTa_2/8_C51/frames'
vad_xian_label_df_path = '/home/yuanyu/projects/dyt_VAD/label.csv'
vad_xian_model_dir = './models/MNAD/exp/Xian/pred/log/model.pth'
vad_xian_mitems_dir = './models/MNAD/exp/Xian/pred/log/keys.pt'
vad_device = 0

# Weather Classification
wc_classes = ['cloudy', 'haze', 'rainy', 'snow', 'sunny', 'thunder']
wc_image_dir = r'D:\datasets\data\dataset\weather'
wc_model_root = r'D:\datasets\data\models\weather'
wc_device = 0

# PV Detector
pv_cfg_path = r'D:\datasets\data\models\PV\default.yaml'
pv_device = 0

# Crowd Counting
crowd_img_path_v = r'D:\datasets\data\dataset\crowd\test.jpg'
crowd_count_model_path = r'D:\datasets\data\models\crowd\lasted_model.pth'
crowd_device = 0

# Gas Detection
gas_dir = r'D:\datasets\data\dataset\gas'
gas_device = 0
