import io
import base64
import json

import numpy as np
from skimage import data, exposure, img_as_float
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


idx = 0
frames = None
anomaly_score_list = None
mse_imgs = None


# def gen_VAD_frame_wrapper(VAD_results):
#     VAD_result = VAD_results[0]
#     anomaly_score_list = VAD_result['pred']

#     # def gen_score_frame():
#     #     while True:
#     #         buf = io.BytesIO()
#     #         # print(type(anomaly_score_list))
#     #         # print(anomaly_score_list)

#     #         plt.plot(anomaly_score_list)
#     #         plt.savefig(buf, format='png')
#     #         buf.seek(0)
#     #         frame = base64.b64encode(buf.getbuffer()).decode("ascii")
#     #         # frame = base64.b64encode(img.getvalue()).decode()

#     #         # yield (b'--frame\r\n'
#     #         #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#     #         yield frame
#     def gen_score_frame():
#         global idx
#         stream = io.BytesIO()
#         while True:
#             fig = Figure()
#             axis = fig.add_subplot(1, 1, 1)
#             axis.plot(anomaly_score_list[:idx+1])
#             # axis.plot(anomaly_score_list[:])
#             idx = (idx+1) % len(anomaly_score_list)
#             FigureCanvas(fig).print_jpeg(stream)
#             stream.seek(0)
#             frame = stream.read()
#             stream.seek(0)
#             stream.truncate()
#             # yield frame
#             # FigureCanvas(fig).print_png(output)
#             # yield output.getvalue()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

#     return gen_score_frame


def gen_VAD_frames_wrapper(VAD_results):
    # print(len(VAD_results))
    global idx
    global frames
    global anomaly_score_list
    global mse_imgs
    idx = 0
    VAD_result = VAD_results[0]
    frames = VAD_result['frames']
    anomaly_score_list = VAD_result['pred']
    mse_imgs = VAD_result['mse_imgs']
    # print(len(frames))

    def gen_score_frame():
        global idx
        stream = io.BytesIO()
        while True:
            fig = Figure()
            axis = fig.add_subplot(1, 1, 1)
            axis.plot(anomaly_score_list[:idx+1])
            FigureCanvas(fig).print_jpeg(stream)
            stream.seek(0)
            frame = stream.read()
            stream.seek(0)
            stream.truncate()

            idx = (idx+1) % len(anomaly_score_list)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def gen_frame():
        global idx
        stream = io.BytesIO()
        while True:
            fig = Figure()
            axis = fig.add_subplot(1, 1, 1)
            img = frames[idx]
            # exposure.adjust_gamma(img, 0.5)
            axis.imshow(img)
            axis.axis('off')

            FigureCanvas(fig).print_jpeg(stream)
            stream.seek(0)
            frame = stream.read()
            stream.seek(0)
            stream.truncate()

            idx = (idx+1) % len(anomaly_score_list)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def gen_mse_frame():
        global idx
        stream = io.BytesIO()
        while True:
            fig = Figure()
            axis = fig.add_subplot(1, 1, 1)
            img = mse_imgs[idx]
            # exposure.adjust_gamma(img, 0.1)
            img = exposure.rescale_intensity(img)
            axis.imshow(img)
            axis.axis('off')

            FigureCanvas(fig).print_jpeg(stream)
            stream.seek(0)
            frame = stream.read()
            stream.seek(0)
            stream.truncate()

            idx = (idx+1) % len(anomaly_score_list)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # def gen_VAD_frames():
    #     global idx
    #     while True:
    #         frame, score_frame = gen_frame(), gen_score_frame()
    #         idx = (idx+1) % len(anomaly_score_list)
    #         yield (frame, score_frame)

    # return gen_VAD_frames
    return gen_frame, gen_mse_frame, gen_score_frame


class CustomJSONizer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return super().default(obj)
