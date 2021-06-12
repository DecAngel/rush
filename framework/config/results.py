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
# import datetime


results_dict_list = [
    # result 0
    {
        'fire_detector': {
            'results': [
                {
                    'type': 'fire',
                    'anomaly': True,
                    'pred': False,  # new added
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    'type_zh': '火灾（模拟）',
                    'description': '在大厅发现着火点',
                    'sensors': [
                        '摄像头51',
                        '易燃气体检测传感器04',
                        '温度计03'
                    ],
                    'filename_list': [  # new added
                        'fire_img.tif',
                        'fire_flamGas.mp4',
                        'fire_Temperature.mp4'
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
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    'type_zh': '人群拥堵',
                    'description': '在电梯口发现人群拥堵',
                    'sensors': [
                        '摄像头32',
                        '毫米波传感器02',
                    ],
                    'filename_list': [
                        'crowd_32_input.mp4',
                        'crowd_den_32.mp4',
                        'crowd_mmv32.mp4'
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
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    'type_zh': '异常气体泄露（模拟）',
                    'description': '在大厅发现可燃气体泄露',
                    'sensors': [
                        '红外甲烷传感器02',
                        '硫化氢传感器02',
                        '温度计03'
                    ],
                    'filename_list': [
                        'gas_CH4.mp4',
                        'gas_H2S.mp4',
                        'gas_CO.mp4'
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
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    'type_zh': '行为异常：骑自行车',
                    'description': '大厅处发现异常物体：自行车',
                    'sensors': [
                        '摄像头32'
                    ],
                    'filename_list': [
                        'vad_raw_0.mp4',
                        'vad_mse_0.mp4',
                        'vad_score_0.mp4'
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
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    #'time': '2021-05-21-20:22:05'
                    'type_zh': '行为异常：跑动',
                    'description': '在上行尾处发现异常行为：跑动',
                    'sensors': [
                        '摄像头51'
                    ],
                    'filename_list': [
                        'vad_raw_1.mp4',
                        'vad_mse_1.mp4',
                        'vad_score_1.mp4'
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
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    'type_zh': '拥堵',
                    'description': '预测 在 15 min 后，三号电梯口发生拥堵',
                    'sensors': [
                        '摄像头33',
                        'tmp',
                    ],
                    'filename_list': [
                        'xxx.mp4'
                        'xxx.mp4',
                        'xxx.mp4',
                        'xxx.mp4'
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
