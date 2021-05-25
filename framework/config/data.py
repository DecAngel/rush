from framework.request import (
    get_fire_image_v,
    get_weather_image_v,
    get_vad_frames_v,
    get_OD_v
)


data_meteinfo_dict = {
    'fire-image-v': {
        # 'sensors': ['virtual image'],
        'method': get_fire_image_v,
        'args': {}
    },
    'weather-image-v': {
        # 'sensors': ['virtual image'],
        'method': get_weather_image_v,
        'args': {}
    },
    'vad-frames-v': {
        'method': get_vad_frames_v,
        'args': {}
    },
    'od-v': {
        'method': get_OD_v,
        'args': {}
    }
}
