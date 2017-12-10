import os
import re

import numpy as np
import pandas as pd
from pytube import YouTube

def get_metadata():
    return pd.read_csv(os.path.join(_get_script_directory(), 'data', 'index.csv'))

def get_audio_list():
    destination = _get_audio_files_destination()
    _create_destination_directory(destination)

    audio_list = []
    data_info = get_metadata()
    for index, item in data_info.iterrows():
        audio_list.append((item['Name'], _get_or_download(destination, item)))

    return audio_list

def get_audio_filepath(name):
    destination = _get_audio_files_destination()
    _create_destination_directory(destination)

    data_info = get_metadata()
    index_mask = data_info['Name'] == name
    if np.any(index_mask):
        return _get_or_download(destination, data_info[index_mask].iloc[0])
    else:
        print('"{}" was not found in dataset'.format(name))
        return None

def get_time_annotations(name, seconds=True):
    times_pattern = re.compile('^(\\d{1,2}\\:\\d{1,2}\\:\\d{1,2})\\s(\\d{1,2}\\:\\d{1,2}\\:\\d{1,2})')
    time_pattern = re.compile('(\\d{1,2})\\:(\\d{1,2})\\:(\\d{1,2})')

    data_info = get_metadata()
    index_mask = data_info['Name'] == name
    if np.any(index_mask):
        txt_filename = '{}.txt'.format(data_info[index_mask].iloc[0]['File'])
        txt_fullpath = os.path.join(_get_script_directory(), 'data', txt_filename)

        times_list = []
        with open(txt_fullpath) as file_handle:
            for line in file_handle:
                matched = times_pattern.match(line)
                if matched is not None:
                    if seconds:
                        start_match = time_pattern.match(matched.group(1))
                        end_match = time_pattern.match(matched.group(2))

                        start = int(start_match.group(3)) + 60 * int(start_match.group(2)) + 60 * 60 * int(start_match.group(1))
                        end = int(end_match.group(3)) + 60 * int(end_match.group(2)) + 60 * 60 * int(end_match.group(1))

                        times_list.append((start, end))
                    else:
                        times_list.append((matched.group(1), matched.group(2)))

        return times_list
    else:
        print('"{}" was not found in dataset'.format(name))
        return None


def _create_destination_directory(destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

def _get_script_directory():
    return os.path.dirname(os.path.realpath(__file__))

def _get_audio_files_destination():
    return (os.path.join(os.getcwd(), os.environ['TALC_AUDIO_DIRECTORY']) if 'TALC_AUDIO_DIRECTORY' in os.environ
            else os.path.join(os.path.dirname(os.path.realpath(__file__)), '.audio'))

def _get_or_download(destination, item):
    wav_filename = '{}.wav'.format(item['File'])
    wav_fullpath = os.path.join(destination, wav_filename)

    if not os.path.exists(wav_fullpath):
        print('Downloading "{}"'.format(item['Name']))
        yt = YouTube(item['Link'])
        # download first available audio stream
        stream = yt.streams.filter(only_audio=True).first()
        output_file = os.path.join(destination, stream.default_filename)
        stream.download(output_path=destination)  # from pytube 7.0.19 it will be possible to specify custom filename as well
        # convert the stream into standard format, i.e. Mono PCM 16b Little Endian with 22.05kHz sampling rate
        # TODO: this is not perfect solution, there should be a convenient wrapper around ffmpeg (or other library)
        os.system('ffmpeg -i "{input}" -acodec pcm_s16le -ac 1 -ar 22050 {output} &> /dev/null'.format(input=output_file, output=wav_fullpath))
        os.remove(output_file)

    return wav_fullpath
