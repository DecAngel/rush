host = '0.0.0.0'
port = '5000'
# mode = 'display'
mode = 'run'

fire_image_dir = './data/dataset/fire'
fire_detection_model_root = './data/models/fire'

vad_videos_dir = './models/MNAD/dataset/ShanghaiTech/testing/frames'
vad_model_dir = './data/models/vad/shanghaitech/model.pth'
vad_mitems_dir = './data/models/vad/shanghaitech/keys.pt'
xian_vad_videos_dir = '/home/yuanyu/projects/data/DaYanTa_2/8_C51/frames'
xian_label_df_path = '/home/yuanyu/projects/dyt_VAD/label.csv'
xian_vad_model_dir = './models/MNAD/exp/Xian/pred/log/model.pth'
xian_vad_mitems_dir = './models/MNAD/exp/Xian/pred/log/keys.pt'

wc_classes = ['cloudy', 'haze', 'rainy', 'snow', 'sunny', 'thunder']
wc_image_dir = './data/dataset/weather'
wc_model_root = './data/models/weather'

PV_cfg_path = './data/models/PV/default.yaml'

crowd_img_path = './data/dataset/crowd/test.jpg'
crowd_count_model_path = './data/models/crowd/lasted_model.pth'
crowd_count_gpus = [0, 1]

gas_dir = './data/dataset/gas'
