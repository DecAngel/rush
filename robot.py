import requests
import json
import time


device_id = 178
config = {
    'ip': '183.6.189.130',
    'port': '2025',
    'header': {'Authorization': 'Basic YWRtaW46YWRtaW4='}, 'username': 'kjxm2022', 'password': '5ae23a41c17bdfc12c17f15e8dc17aea', 'grant_type': 'password',
    'login_path': 'robotservice/auth/login',
    'waitout': 10,
    'device_id': 178
}


class Robot:
    def __init__(self, config=config) -> None:
        url = f'http://{config["ip"]}:{config["port"]}/{config["login_path"]}'
        header = config['header']
        a = requests.post(
            url=url,
            data={
                'username': config['username'],
                'password': config['password'],
                'grant_type': 'password'
            },
            headers=header)
        self.config = config
        self.cookies = json.loads(a.text)['data']['access_token']

    def comp(self, at_x, at_y, dst, err):
        if int(at_x) - err <= dst[0] <= int(at_x) + err and int(at_y) - err <= dst[1] <= int(at_y) + err:
            return True
        else:
            return False

    def move(self, device_id, x, y):
        go = requests.post(
            url=self.config['ip'] +
            '/robotservice/patrol/navigateToPoint.action',
            cookies=self.cookies,
            params={'deviceId': device_id, 'posX': x, 'posY': y}
        )
        print(go)
        while True:
            time.sleep(self.config['waitout'])
            cur_x, cur_y = self.get_cur_cood(device_id)
            print(cur_x, cur_y)
            if self.comp(cur_x, cur_y, [x, y], 5):
                break
        self.say(
            device_id=device_id,
            text='到达巡检点'
        )

    def say(self, device_id, text):
        ret = requests.post(
            url=self.config['ip'] +
            '/robotservice/device/voiceSoundtextSet.action',
            cookies=self.cookies,
            params={
                'deviceId': device_id,
                'soundtext': text
            }
        )

    def get_cur_cood(self, device_id):
        ret = requests.get(
            url=self.config['ip'] +
            '/robotservice/device/findRobotStatus.action',
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
