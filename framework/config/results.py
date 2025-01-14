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

# 每次在 flask_server.py 中更新 results_dict 后，新增的 result 将显示在前端页面中异常事件列表的顶部
results_dict_list = [
    # result 0 模拟异常
    {
        'fire_detector': {
            'results': [{
                'type':
                'fire',
                'anomaly':
                True,
                'pred':
                False,  # new added
                'time': ('', '', '', '', '', ''),
                'type_zh':
                '火灾（模拟）',
                'description':
                '在大厅发现着火点',
                'sensors': ['摄像头51', '二氧化碳浓度传感器01', '温度计03'],
                'contribution_list': [60, 25, 15],
                'filename_list': [  # new added
                    '火灾监控-3.mp4', '二氧化碳浓度传感器-3.mp4', '温度传感器-3.mp4'
                ],
                'video_title_list':
                ['', '', '']
            }],
            'displays': [None],
            'solves': [None]
        },
        'gas_detector': {
            'results': [{
                'type':
                'gas',
                'pred':
                False,
                'anomaly':
                True,
                'time': ('', '', '', '', '', ''),
                'type_zh':
                '有毒气体（甲烷）泄露（模拟）',
                'description':
                '在大厅发现甲烷泄露',
                'sensors': ['红外甲烷传感器01', '硫化氢传感器01', '一氧化碳传感器01'],
                'contribution_list': [98, 1, 1],
                'filename_list':
                ['红外甲烷传感器-1.mp4', '硫化氢传感器-1.mp4', '一氧化碳传感器-1.mp4'],
                'video_title_list':
                ['', '', '']
            }],
            'displays': [None],
            'solves': [None]
        },
    },
    # result 1 vad_0
    {
        'video_anomaly_detector': {
            'results': [{
                'type':
                'vad',
                'pred':
                False,
                'anomaly':
                True,
                'time': ('2021', '06', '13', '20', '30', '47'),
                'type_zh':
                '行为异常：推车',
                'description':
                '在下行尾发现异常行为：推车',
                'sensors': ['摄像头32'],
                'filename_list':
                ['行为异常监控-1.mp4', '异常高亮图-1.mp4', '异常得分图-1.mp4'],
                'video_title_list':
                ['', '', ''],
                'contribution_list': [100]
            }],
            'displays': [None],
            'solves': [None]
        },
    },
    # result 3 vad_1
    {
        'video_anomaly_detector': {
            'results': [{
                'type':
                'vad',
                'pred':
                False,
                'anomaly':
                True,
                'time': ('2021', '06', '13', '21', '40', '14'),
                # 'time': '2021-05-21-20:22:05'
                'type_zh':
                '行为异常：跑动',
                'description':
                '在下行尾处发现异常行为：跑动',
                'sensors': ['摄像头32'],
                'contribution_list': [100],
                'filename_list':
                ['行为异常监控-2.mp4', '异常高亮图-2.mp4', '异常得分图-2.mp4'],
                'video_title_list':
                ['', '', '']
            }],
            'displays': [None],
            'solves': [None]
        },
    },
    # result 2 crowd_32
    {
        'crowd_counter': {
            'results': [{
                'type':
                'crowd',
                'pred':
                False,
                'anomaly':
                True,
                'time': ('2021', '06', '13', '21', '45', '03'),
                'type_zh':
                '局部拥堵',
                'description':
                '在下行尾候车处发现人群拥堵',
                'sensors': [
                    '摄像头32',
                    '毫米波传感器32',
                ],
                'contribution_list': [80, 20],
                'filename_list': [
                    '站内热力图监测.mp4',  # to do
                    '人群监控-1.mp4',
                    '人群密度图估计.mp4',
                    # 'crowd_mmv32.mp4'
                    '毫米波传感器32.mp4'
                ],
                'video_title_list':
                ['', '', '']
            }],
            'displays': [None],
            'solves': [None]
        },
    },
    {
        'crowd_counter': {
            'results': [{
                'type':
                'crowd',
                'pred':
                False,
                'anomaly':
                True,
                'time': ('2021', '06', '13', '21', '45', '10'),
                'type_zh':
                '局部拥堵',
                'description':
                '在下行首候车处发现人群拥堵',
                'sensors': [
                    '摄像头32',
                    '毫米波传感器32',
                ],
                'contribution_list': [80, 20],
                'filename_list': [
                    '站内热力图监测.mp4',  # to do
                    '人群监控-1.mp4',
                    '人群密度图估计.mp4',
                    # 'crowd_mmv32.mp4'
                    '毫米波传感器32.mp4'
                ],
                'video_title_list':
                ['', '', '']
            }],
            'displays': [None],
            'solves': [None]
        },
    },
    # result 4 crowd_pred_0
    {
        'crowd_predictor': {
            'results': [{
                'type': 'crowd_pred',
                'pred': True,
                'anomaly': True,
                'time': ('2021', '06', '18', '18', '30', '00'),
                'type_zh': '拥堵预测',
                'description': '站台两侧电梯口15分钟后将发生拥堵',
                'sensors': [
                    '下行电车门01',
                    '闸机口01',
                ],
                'contribution_list': [85, 15],
                'filename_list': ['站内未来15分钟拥堵预测.mp4', '站厅下方闸机进站流量预测.mp4', '上行列车下车人数预测.mp4'],
                'video_title_list':
                ['', '', '']
            }],
            'displays': [None],
            'solves': [None]
        },
    },
]
