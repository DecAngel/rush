from typing import Dict, Any

import requests
import time


class Robot:
    def __init__(self, _config=None):
        if _config is None:
            _config = {
                'ip': 'cloud.gosunyun.com',
                'port': '2025',
                'header': {'Authorization': 'Basic YWRtaW46YWRtaW4='},
                'username': 'kjxm2022',
                'password': '5ae23a41c17bdfc12c17f15e8dc17aea',
                'grant_type': 'password',
                'waitout': 3,
            }
        self.url_base = f'http://{_config["ip"]}:{_config["port"]}/robotservice/'
        self.url_login = self.url_base + 'auth/login'
        self.url_move = self.url_base + 'patrol/navigateToPoint.action'
        self.url_say = self.url_base + 'device/voiceSoundtextSet.action'
        self.url_coordinate = self.url_base + 'device/findRobotStatus.action'
        self.config = _config
        try:
            a = requests.post(
                url=self.url_login,
                data={
                    'username': _config['username'],
                    'password': _config['password'],
                    'grant_type': _config['grant_type']
                },
                headers=_config['header']
            )
        except requests.ConnectionError as e:
            raise RuntimeError(f'Robot connection to {self.url_login} failed!') from e
        try:
            self.cookies = {"Admin-Token": a.json()['data']['access_token']}
        except requests.JSONDecodeError as e:
            raise RuntimeError(f'Decoding response failed! Response text: {a.text}') from e

    def post_jsonify_check(self, url: str, params: Dict[str, Any]) -> Any:
        try:
            response = requests.post(url=url, cookies=self.cookies, params=params)
        except requests.ConnectionError as e:
            raise RuntimeError(f'Robot connection to {url} failed!') from e
        try:
            response = response.json()
        except requests.JSONDecodeError as e:
            raise RuntimeError(f'Decoding response failed! Response text: {response.text}') from e
        if response['ret'] != 1:
            raise RuntimeError(f'Return code error! Error msg: {response["msg"]}')

    def navigate(self, _device_id, path):
        for x, y in path:
            self.move(_device_id, x, y)

    def comp(self, at_x, at_y, dst, err):
        return int(at_x) - err <= dst[0] <= int(at_x) + err and int(at_y) - err <= dst[1] <= int(at_y) + err

    def move(self, _device_id, x, y):
        _ = self.post_jsonify_check(self.url_move, {'deviceId': _device_id, 'posX': x, 'posY': y})
        while True:
            time.sleep(self.config['waitout'])
            cur_x, cur_y = self.get_cur_cood(_device_id)
            if self.comp(cur_x, cur_y, [x, y], 5):
                break

    def say(self, _device_id, text):
        _ = self.post_jsonify_check(self.url_say, {'deviceId': _device_id, 'soundtext': text})

    def get_cur_cood(self, _device_id):
        response = self.post_jsonify_check(self.url_coordinate, {'deviceId': _device_id})
        return response['data']['xPosition'], response['data']['yPosition']


if __name__ == '__main__':
    print('Start the test of communication!'.center(50, '='))
    robot = Robot()
    robot.say(
        _device_id=178,
        text='发生火灾，请大家尽快撤离！'
    )
