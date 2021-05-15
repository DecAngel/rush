from models import (
    FireDetector,
    WeatherClassifier,
    VideoAnomalyDetector
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
    'weather_classifier': {
        'data_lists': [
            [
                'weather-image-v'
            ]
            # [
            #     'weather-image'
            # ]
        ],
        'model': WeatherClassifier
    },
    'video_anomaly_detector': {
        'data_lists': [
            [
                'vad-frames-v'
            ]
            # [
            #     'weather-image'
            # ]
        ],
        'model': VideoAnomalyDetector
    },
}
