import datetime
import threading

from flask import Flask, Response, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_apscheduler import APScheduler

from framework.results_require import get_all_results
from framework.main import (
    init,
    one_step
)
# from server_utils import gen_VAD_frame_wrapper, gen_VAD_frames_wrapper
from server_utils import gen_VAD_frames_wrapper, save_VAD_frames_wrapper, merge_results_dict
from robot import Robot
from settings import (
    host,
    port,
    mode
)


class FlaskServer:
    def __init__(self, _host='0.0.0.0', _port=5000, _mode='display') -> None:
        super().__init__()
        assert _mode in ['display', 'run']
        self.mode = _mode
        self.file_dir = "./data/files"
        self.robot = Robot()

        if mode == 'run':
            self.models_dict = init()
        self.results_dict = dict()

        self.app = Flask(__name__)
        self.app.config['SCHEDULER_API_ENABLED'] = True
        CORS(self.app)

        scheduler = APScheduler()
        scheduler.init_app(self.app)

        self.gen_frame, self.gen_mse_frame, self.gen_score_frame = None, None, None
        # self.gen_VAD_frames = None
        # self.VAD_frame, self.VAD_score_frame = None, None
        self.step = 0

        # @scheduler.task('interval', id='one_step', seconds=20)
        # def job_one_step():
        #     self.results_dict = one_step(self.models_dict)
        #     self.gen_frame, self.gen_mse_frame, self.gen_score_frame = gen_VAD_frames_wrapper(
        #         self.results_dict['video_anomaly_detector']['results'])

        #     save_raw, save_mse, save_score = save_VAD_frames_wrapper(
        #         self.results_dict['video_anomaly_detector']['results']
        #     )
        #     print(f'step {self.step} end'.center(100, '*'))
        #     save_raw(self.step)
        #     save_mse(self.step)
        #     save_score(self.step)
        #     self.step += 1

        # @scheduler.task('interval', id='VAD_display', seconds=0.5)
        # def job_one_step():
        #     if self.gen_VAD_frames is not None:
        #         (self.VAD_frame, self.VAD_score_frame) = self.gen_VAD_frames()
        #         print(1)

        @self.app.route("/")
        def index():
            print(self.results_dict)
            return str(self.results_dict)

        # @self.app.route('/VAD_video_feed')
        # def VAD_video_feed():
        #     """Video streaming route. Put this in the src attribute of an img tag."""
        #     return Response(
        #         self.gen_frame(),
        #         # self.VAD_frame,
        #         # mimetype='image/png'
        #         mimetype='multipart/x-mixed-replace; boundary=frame'
        #     )

        # @self.app.route('/VAD_mse_feed')
        # def VAD_mse_feed():
        #     """Video streaming route. Put this in the src attribute of an img tag."""
        #     return Response(
        #         self.gen_mse_frame(),
        #         # self.VAD_frame,
        #         # mimetype='image/png'
        #         mimetype='multipart/x-mixed-replace; boundary=frame'
        #     )

        # @self.app.route('/VAD_score_feed')
        # def VAD_score_feed():
        #     """Video streaming route. Put this in the src attribute of an img tag."""
        #     return Response(
        #         self.gen_score_frame(),
        #         # self.VAD_score_frame,
        #         # mimetype='image/png'
        #         mimetype='multipart/x-mixed-replace; boundary=frame'
        #     )

        # @self.app.route('/test')
        # def test():
        #     """Video streaming home page."""
        #     return render_template('index.html')

        @self.app.route('/anomalies', methods=['GET', 'POST'])
        def get_anomaly():
            assert self.mode in ['run', 'display']
            results_dict = dict()
            if self.mode == 'run':
                for model_name, data in self.results_dict.items():
                    results_dict[model_name] = dict()
                    results_dict[model_name]['results'] = list(map(
                        lambda result: {
                            'time': datetime.datetime.now(),
                            'type': result['type'],
                            'anomaly': result['anomaly'],
                            'sensors': result['sensors']
                        }, data['results'])
                    )
                    results_dict[model_name]['displays'] = data['displays']
                    results_dict[model_name]['solves'] = data['solves']
            elif self.mode == 'display':
                results_dict = self.results_dict
            return jsonify(results_dict)

        @self.app.route("/download/<filename>", methods=['GET'])
        def download_file(filename):
            # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
            directory = self.file_dir
            return send_from_directory(directory, filename, as_attachment=True)

        scheduler.start()
        monitoring_thread = threading.Thread(target=self.monitoring_loop)
        monitoring_thread.start()
        self.app.run(host=_host, port=_port)

    def job_one_step(self):
        if self.mode == 'run':
            new_results_dict = one_step(self.models_dict)
            # self.gen_frame, self.gen_mse_frame, self.gen_score_frame = gen_VAD_frames_wrapper(
            #     self.results_dict['video_anomaly_detector']['results'])

            # save_raw, save_mse, save_score = save_VAD_frames_wrapper(
            #     self.results_dict['video_anomaly_detector']['results']
            # )
            # save_raw(self.step)
            # save_mse(self.step)
            # save_score(self.step)
            print(new_results_dict.keys())
            print(f'step {self.step} end'.center(100, '*'))
        else:
            new_results_dict = get_all_results()

        self.step += 1
        self.results_dict = merge_results_dict(
            self.results_dict, new_results_dict
        )
        print('Detect a new anomaly!'.center(50, '-'))
        sensor_key = list(new_results_dict.keys())[0]
        print(new_results_dict[sensor_key]["results"][-1])
        print('-'*50)

    def monitoring_loop(self):
        while True:
            input(f'Press enter to continue')
            print('Begin to process new data', datetime.datetime.now())
            self.job_one_step()
            print('End', datetime.datetime.now())


if __name__ == '__main__':
    flask_server = FlaskServer(host, port, mode)
