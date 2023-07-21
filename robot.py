import requests
import json
import time

"""
{"data":[{"angle":-0.6100539282550298,"createdAt":"2020-10-26 11:21:12","gridX":257,"gridY":225,"id":0,"mapId":"8f5c2c98-fdf8-4de9-92da-1b8d08036d9c","mapName":"shiyanshi","name":"1","type":2,"worldPose":{"orientation":{"w":0.99998582901043476,"x":0,"y":0,"z":-0.0053236996828815433},"position":{"x":1.6358933542090608,"y":0.83887951809169625,"z":0}}},{"angle":90.906558963191557,"createdAt":"2020-10-26 11:27:49","gridX":310,"gridY":229,"id":0,"mapId":"8f5c2c98-fdf8-4de9-92da-1b8d08036d9c","mapName":"shiyanshi","name":"2","type":2,"worldPose":{"orientation":{"w":0.70149063490132491,"x":0,"y":0,"z":0.71267867173484034},"position":{"x":6.9367020927384262,"y":1.2248537659469543,"z":0}}},{"angle":-160.89948152597239,"createdAt":"2020-10-26 11:28:47","gridX":311,"gridY":255,"id":0,"mapId":"8f5c2c98-fdf8-4de9-92da-1b8d08036d9c","mapName":"shiyanshi","name":"3","type":2,"worldPose":{"orientation":{"w":-0.16591270155453633,"x":0,"y":0,"z":0.98614044408637624},"position":{"x":7.0099795420898046,"y":3.867655600765505,"z":0}}},{"angle":-125.57219992779537,"createdAt":"2020-10-26 11:29:45","gridX":264,"gridY":255,"id":0,"mapId":"8f5c2c98-fdf8-4de9-92da-1b8d08036d9c","mapName":"shiyanshi","name":"4","type":2,"worldPose":{"orientation":{"w":-0.45731368744208512,"x":0,"y":0,"z":0.88930545442953579},"position":{"x":2.339771540085835,"y":3.8662307634311315,"z":0}}}],"errorCode":"","msg":"successed","successed":true}
"""

device_id = 178
config = {
    'ip': 'cloud.gosunyun.com',
    'port': '2025',
    'header': {'Authorization': 'Basic YWRtaW46YWRtaW4='},
    'username': 'kjxm2022',
    'password': '5ae23a41c17bdfc12c17f15e8dc17aea',
    'grant_type': 'password',
    'login_path': 'robotservice/auth/login',
    'waitout': 3,
    'device_id': 80163,
    # 1: 257,225; 0,0
    # 2: "x":6.9367020927384262,"y":1.2248537659469543,
    'path': [(310, 229), (311, 255), (264, 255), (257, 225)]
}


class Robot:
    def __init__(self, _config=None) -> None:
        if _config is None:
            _config = config
        url = f'http://{_config["ip"]}:{_config["port"]}/{_config["login_path"]}'
        header = _config['header']
        a = requests.post(
            url=url,
            data={
                'username': _config['username'],
                'password': _config['password'],
                'grant_type': 'password'
            },
            headers=header)
        self.config = _config
        print(json.loads(a.text))
        self.cookies = {
            "Admin-Token": json.loads(a.text)['data']['access_token']}

    def navigate(self, device_id, path):
        for x, y in path:
            self.move(device_id, x, y)

    def comp(self, at_x, at_y, dst, err):
        if int(at_x) - err <= dst[0] <= int(at_x) + err and int(at_y) - err <= dst[1] <= int(at_y) + err:
            return True
        else:
            return False

    def move(self, device_id, x, y):
        go = requests.post(
            url=f'http://{self.config["ip"]}:{self.config["port"]}/robotservice/patrol/navigateToPoint.action',
            cookies=self.cookies,
            params={'deviceId': device_id, 'posX': x, 'posY': y}
        )
        if go.status_code == 200:
            while True:
                time.sleep(self.config['waitout'])
                cur_x, cur_y = self.get_cur_cood(device_id)
                # print(cur_x, cur_y)
                if self.comp(cur_x, cur_y, [x, y], 5):
                    break
        else:
            raise RuntimeError(f'robot move request failed: {go.text}')
        # self.say(
        #     device_id=device_id,
        #     text='到达巡检点'
        # )

    def say(self, device_id, text):
        ret = requests.post(
            url=f'http://{self.config["ip"]}:{self.config["port"]}/robotservice/device/voiceSoundtextSet.action',
            cookies=self.cookies,
            params={
                'deviceId': device_id,
                'soundtext': text
            }
        )
        print(json.loads(ret.text))

    def get_cur_cood(self, device_id):
        ret = requests.get(
            url=f'http://{self.config["ip"]}:{self.config["port"]}//robotservice/device/findRobotStatus.action',
            cookies=self.cookies,
            params={'deviceId': device_id}
        )
        return(json.loads(ret.text)['data']['xPosition'], json.loads(ret.text)['data']['yPosition'])


if __name__ == '__main__':
    print('Start the test of communication!'.center(50, '='))
    robot = Robot(config)
    robot.say(
        device_id=device_id,
        text='发生火灾，请大家尽快撤离！'
    )
