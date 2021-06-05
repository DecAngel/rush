from framework.request import (
    get_fire_image_v,
    get_weather_image_v,
    get_vad_frames_v,
    get_crowd_image_v,
    get_OD_v,

    get_vad_frames_xian
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
    'crowd-image-v': {
        'method': get_crowd_image_v,
        'args': {}
    },
    # 'od-v': {
    #     'method': get_OD_v,
    #     'args': {}
    # },
    'vad-frames-xian': {
        'method': get_vad_frames_xian,
        'args': {}
    },
}
