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
                        '二氧化碳浓度传感器03',
                        '温度计03'
                    ],
                    'filename_list': [  # new added
                        'fire_img.mp4',
                        'fire_CO2.mp4',
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
                    'type_zh': '局部拥堵',
                    'description': '在电梯口发现人群拥堵',
                    'sensors': [
                        '摄像头32',
                        '毫米波传感器32',
                    ],
                    'filename_list': [
                        'crowd_32_input.mp4', # to do
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
                    'type_zh': '有毒气体（甲烷）泄露（模拟）',
                    'description': '在大厅发现甲烷泄露',
                    'sensors': [
                        '红外甲烷传感器01',
                        '硫化氢传感器01',
                        '一氧化碳传感器01'
                    ],
                    'filename_list': [
                        'gas_CH4_CH4.mp4',
                        'gas_CH4_H2S.mp4',
                        'gas_CH4_CO.mp4'
                    ]
                },
                                {
                    'type': 'gas',
                    'pred': False,
                    'anomaly': True,
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    'type_zh': '有毒气体（硫化氢）泄露（模拟）',
                    'description': '在大厅发现硫化氢泄露',
                    'sensors': [
                        '硫化氢传感器02',
                        '红外甲烷传感器02',
                        '一氧化碳传感器02'
                    ],
                    'filename_list': [
                        'gas_H2S_CH4.mp4',
                        'gas_H2S_H2S.mp4',
                        'gas_H2S_CO.mp4'
                    ]
                },
                                {
                    'type': 'gas',
                    'pred': False,
                    'anomaly': True,
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    'type_zh': '有毒气体（一氧化碳）泄露（模拟）',
                    'description': '在大厅发现一氧化碳泄露',
                    'sensors': [
                        '一氧化碳传感器02'
                        '红外甲烷传感器02',
                        '硫化氢传感器02',
                    ],
                    'filename_list': [
                        'gas_CO_CH4.mp4',
                        'gas_CO_H2S.mp4',
                        'gas_CO_CO.mp4'
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
    # result 5
    {
        'crowd_predictor': {
            'results': [
                {
                    'type': 'crowd_pred',
                    'pred': True,
                    'anomaly': True,
                    'time': ('2021', '05', '01', '12', '20', '20'),
                    'type_zh': '拥堵预测',
                    'description': '预测15分钟后，三号电梯口拥堵',
                    'sensors': [
                        '闸机口01',
                        '电车门01',
                    ],
                    'filename_list': [
                        'vad_raw_0.mp4',
                        'in.mp4',
                        'out.mp4'
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
