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


results_dict_list = [
    # result 0
    {
        'fire_detector': {
            'results': [
                {
                    'type': 'fire',
                    'anomaly': True,
                    'pred': False,  # new added
                    'time': '',
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
                    'time': '',
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
                    'time': '',
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
                    'time': '',
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
                    'time': '',
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
                    'type': 'vad',
                    'pred': False,
                    'anomaly': True,
                    'time': '',
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
