import os
from typing import Tuple
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdate
import matplotlib.ticker as mticker
from pylab import mpl
from matplotlib.font_manager import _rebuild


output_dir = './data/files'
gas_csv_list = ['./data/dataset/gas/gas_CH4.csv',
                './data/dataset/gas/gas_H2S.csv',
                './data/dataset/gas/gas_CO.csv']
fire_gas_csv = './data/dataset/fire/fire3.csv'


os.chdir('/home/yuanyu/projects/rush')
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
_rebuild()


def generate_time_list(start_time: Tuple[int], time_delta=1, steps=100):
    time_list = list()

    start_dt = datetime.datetime(*start_time)
    interval = datetime.timedelta(seconds=time_delta)
    for i in range(steps+1):
        time_list.append((start_dt + interval * i).strftime("%H:%M:%S"))
    # print(type(time_list[0]))
    return time_list


def plot_and_save_score_gif(data: pd.Series, save_path: str, yticks=np.arange(0, 1.1, 0.1), start_time=(
        2017, 1, 1, 20, 10, 10), time_delta=1, title='', unit='ppm', ylim=None, fps=1) -> animation.Animation:
    fig = plt.figure()
    ax = fig.gca()
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter(f'%d {unit}'))
    # plt.gca().xaixs.set_major_formatter(mdate.DateFormatter('%H:%M:%S'))
    plt.xlabel('时间', fontdict={'fontsize': 12})
    # plt.ylabel('ppm', fontdict={'fontsize': 12})
    for direction in ['right', 'top']:
        ax.spines[direction].set_color('none')
        # ax.spines['top'].set_color('none')

    plt.title(title, fontdict={'fontsize': 20})
    if ylim is not None:
        plt.ylim(ylim)
    # plt.yticks(yticks)
    time_list = generate_time_list(
        start_time=start_time, time_delta=time_delta, steps=len(data))
    print('time_list', len(time_list))

    def animate(i):
        # i = min(len(data)-1, i)
        tmp_data = data[:i+1]
        # plt.axis.sp
        im = plt.plot(tmp_data, color='black')
        # plt.show()

        # plt.title(data.index)
        plt.xlim(tmp_data.index[0], tmp_data.index[-1])
        plt.yticks(yticks)
        plt.xticks([0, i+1], [time_list[0], time_list[i]], fontsize=10)
        # print(i, )
    animator = animation.FuncAnimation(fig,
                                       animate,
                                       frames=len(data))
    # plt.show()
    # animator.save(save_path, writer='pillow')
    FFwriter = animation.FFMpegWriter(fps=1)
    animator.save(save_path, writer=FFwriter)


def plot_gas():
    for i, gas_csv in enumerate(gas_csv_list):
        print(gas_csv.center(50, '*'))
        gas_df = pd.read_csv(gas_csv, skipinitialspace=True, index_col=0)
        for col_index, col in gas_df.iteritems():
            print(col_index)
            title = f'{col.name} 浓度'
            save_path = f'{output_dir}/gas_{i}_{col_index}.mp4'
            yticks = np.arange(0, 101, 10)
            ylim = (-15, 100)
            plot_and_save_score_gif(col, save_path, yticks, start_time=(
                2017, 1, 1, 20, 10, 10), time_delta=1, title=title, unit='ppm', ylim=ylim)
            # break


def plot_fire_gas():
    info_dict = {
        'Temperature': {
            'title': '温度',
            'unit': '℃',
            'yticks': np.arange(0, 101, 10)
        },
        'CO2': {
            'title': 'CO2 浓度',
            'unit': 'ppm',
            'yticks': np.arange(100, 2701, 200)
        }
    }
    gas_df = pd.read_csv(fire_gas_csv, skipinitialspace=True, index_col=0)
    for col_index, col in gas_df.iteritems():
        print(col_index)
        # if col_index == 'Temperature':
        #     title = '温度'
        #     unit = '℃'
        # else:
        #     title = f'{col.name} 浓度'
        #     unit = 'ppm'
            # continue
        # yticks = np.arange(0, 101, 10)
        title = info_dict[col_index]['title']
        unit = info_dict[col_index]['unit']
        yticks = info_dict[col_index]['yticks']
        save_path = f'{output_dir}/fire_{col_index}.mp4'
        plot_and_save_score_gif(col, save_path, yticks, start_time=(
            2017, 1, 1, 20, 10, 10), time_delta=1, title=title, unit=unit)
        # break


def main():
    print('Plot gas...'.center(100, '='))
    plot_gas()
    # print('Plot fire_gas...'.center(100, '='))
    # plot_fire_gas()


if __name__ == '__main__':
    main()
