fire_image_dir = './models/fire_classification/data'
fire_detection_model_root = './models/fire_classification/runs/default'

vad_videos_dir = './models/MNAD/dataset/ShanghaiTech/testing/frames'
# vad_videos_dir = '/home/yuanyu/projects/data/DaYanTa_2/8_C51/frames'
vad_model_dir = './models/MNAD/exp/ShanghaiTech/pred/log/model.pth'
vad_mitems_dir = './models/MNAD/exp/ShanghaiTech/pred/log/keys.pt'

wc_classes = ['cloudy', 'haze', 'rainy', 'snow', 'sunny', 'thunder']
wc_image_dir = './models/weather_classification/data'
wc_model_root = './models/weather_classification/runs/default'

PV_cfg_path = './models/PVCGN/trained/default.yaml'

crowd_img_path = './models/crowd_count/test.jpg'
crowd_count_model_path = './models/crowd_count/crowd_counting/lasted_model.pth'
crowd_count_gpus = [0, 1]
