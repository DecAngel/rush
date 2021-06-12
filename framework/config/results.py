'''model 列表
已有：
fire_detector
crowd_counter
video_anomaly_detector

不使用：
weather_classifier
pv_detector

无：
gas_detector
'''
import datetime


results_dict_list = [
    # result 0
    {
        'fire_detector': {
            'results': [
                {
                    'type': 'fire',
                    'anomaly': True,
                    'pred': False,  # new added
                    'time': datetime.datetime(2021, 5, 1, 12, 20, 20),
                    'type_zh': '火灾（模拟）',
                    'description': '在大厅发现着火点',
                    'sensors': [
                        'virtual image'
                    ],
                    'filename_list': [  # new added
                        'fire_img.tif',
                        'fire_flamGas.gif',
                        'fire_Temperature.gif'
                    ]
                }
            ],
            'displays': [
                None
            ],
            'solves': [
                None
            ]
        },
    },
    # result 1
    {
        'crowd_counter': {
            'results': [
                {
                    'type': 'crowd',
                    'pred': False,
                    'anomaly': True,
                    'time': datetime.datetime(2021, 5, 1, 12, 20, 20),
                    'type_zh': '人群拥堵',
                    'description': '在电梯口发现人群拥堵',
                    'sensors': [
                        'virtual image'
                    ],
                    'filename_list': [
                        'crowd_32_input.avi',
                        'crowd_den_32.avi',
                        'crowd_mmv32.avi'
                    ]
                }
            ],
            'displays': [
                None
            ],
            'solves': [
                None
            ]
        },
    },
    # result 2
    {
        'gas_detector': {
            'results': [
                {
                    'type': 'gas',
                    'pred': False,
                    'anomaly': True,
                    'time': datetime.datetime(2021, 5, 1, 12, 20, 20),
                    'type_zh': '异常气体泄露（模拟）',
                    'description': '在大厅发现可燃气体泄露',
                    'sensors': [
                        'virtual image'
                    ],
                    'filename_list': [
                        'gas_CH4.gif',
                        'gas_H2S.gif',
                        'gas_CO.gif'
                    ]
                }
            ],
            'displays': [
                None
            ],
            'solves': [
                None
            ]
        },
    },
    # result 3
    {
        'video_anomaly_detector': {
            'results': [
                {
                    'type': 'vad',
                    'pred': False,
                    'anomaly': True,
                    'time': datetime.datetime(2021, 5, 1, 12, 20, 20),
                    'type_zh': '行为异常：骑自行车',
                    'description': '大厅处发现异常物体：自行车',
                    'sensors': [
                        'virtual image'
                    ],
                    'filename_list': [
                        'vad_raw_0.gif',
                        'vad_mse_0.gif',
                        'vad_score_0.gif'
                    ]
                }
            ],
            'displays': [
                None
            ],
            'solves': [
                None
            ]
        },
    },
    # result 4
    {
        'video_anomaly_detector': {
            'results': [
                {
                    'type': 'vad',
                    'pred': False,
                    'anomaly': True,
                    'time': datetime.datetime(2021, 5, 1, 12, 20, 20),
                    #'time': '2021-05-21-20:22:05'
                    'type_zh': '行为异常：跑动',
                    'description': '在上行尾处发现异常行为：跑动',
                    'sensors': [
                        'virtual image'
                    ],
                    'filename_list': [
                        'vad_raw_1.gif',
                        'vad_mse_1.gif',
                        'vad_score_1.gif'
                    ]
                }
            ],
            'displays': [
                None
            ],
            'solves': [
                None
            ]
        },
    },
    # result 4
    {
        'crowd_predictor': {
            'results': [
                {
                    'type': 'crowd_pred',
                    'pred': True,
                    'anomaly': True,
                    'time': datetime.datetime(2021, 5, 1, 12, 20, 20),
                    'type_zh': '拥堵',
                    'description': '预测 在 15 min 后，三号电梯口发生拥堵',
                    'sensors': [
                        'virtual image'
                    ],
                    'filename_list': [
                        'xxx.gif'
                        'xxx.gif',
                        'xxx.gif',
                        'xxx.gif'
                    ]
                }
            ],
            'displays': [
                None
            ],
            'solves': [
                None
            ]
        },
    },
]
