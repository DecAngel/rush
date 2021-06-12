from models import (
    FireDetector,
    VideoAnomalyDetector,
    CrowdCounter
    # WeatherClassifier,
    # PVCDetector,
)


model_config_dict = {
    'fire_detector': {
        'data_lists': [
            [
                'fire-image-v'
            ]
            # [
            #     'fire-image'
            # ]
        ],
        'model': FireDetector
    },
    'video_anomaly_detector': {
        'data_lists': [
            [
                'vad-frames-v'
            ],
            # [
            #     'vad-frames-xian'
            # ]
        ],
        'model': VideoAnomalyDetector
    },
    'crowd_counter': {
        'data_lists': [
            [
                'crowd-image-v'
            ]
        ],
        'model': CrowdCounter
    },
    # 'weather_classifier': {
    #     'data_lists': [
    #         [
    #             'weather-image-v'
    #         ]
    #         # [
    #         #     'weather-image'
    #         # ]
    #     ],
    #     'model': WeatherClassifier
    # },
    # 'pv_detector': {
    #     'data_lists': [
    #         [
    #             'od-v'
    #         ]
    #     ],
    #     'model': PVCDetector
    # }
}
