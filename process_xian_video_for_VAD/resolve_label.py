import datetime
from argparse import ArgumentParser

import pandas as pd


def process_one(new_df: pd.DataFrame, line: pd.Series, delta: int = 10) -> None:
    # line = new_df.iloc[line_idx]
    # print(line)
    video_name = line.loc['raw_video']
    # print(video_name)
    time_str = video_name.split('.')[0]
    time = datetime.datetime.strptime(time_str, '%Y-%m-%d_%H-%M-%S')
    start_time, end_time = datetime.datetime.strptime(
        line.loc['start_time'], '%H:%M:%S'), \
        datetime.datetime.strptime(line.loc['end_time'], '%H:%M:%S')
    start_id = (start_time-time).seconds // delta
    end_id = (end_time-time).seconds // delta

    for i in range(start_id, end_id+1):
        new_video_name = f'{time_str}_{i:0>3d}'
        new_df.loc[new_df.index.size] = [line['district'],
                                         line['date'], new_video_name, -1, -1, line['anomaly']]


def process_all(label_df: pd.DataFrame) -> pd.DataFrame:
    new_df = pd.DataFrame(
        columns=['district', 'date', 'new_video',
                 'start_frame', 'end_frame', 'anomaly']
    )
    for line_idx, line in label_df.iterrows():
        # print(line_idx)
        # print(line)
        process_one(new_df, line)

    return new_df


def main():
    parser = ArgumentParser()
    parser.add_argument('--src', '-s', type=str)
    parser.add_argument('--target', '-t', type=str)
    args = parser.parse_args()

    label_df = pd.read_csv(args.src, skipinitialspace=True)
    new_df = process_all(label_df)

    new_df.to_csv(args.target)
    print(f'Saved new csv to {args.target}!'.center(100, '='))
    print(new_df)


if __name__ == '__main__':
    main()
