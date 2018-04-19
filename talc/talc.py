import os
import sys
import re

import numpy as np
import pandas as pd
from pytube import YouTube
import av

def get_metadata(name=None):
    metadata = pd.read_csv(os.path.join(_get_script_directory(), '..', 'data', 'index.csv'))
    if name is None:
        return metadata
    else:
        index_mask = metadata['Name'] == name
        if np.any(index_mask):
            return metadata[index_mask].iloc[0]
        else:
            print("{} does not exist in the TALC dataset".format(name))
            return None

def get_audio_list():
    destination = _get_audio_files_destination()
    _create_destination_directory(destination)

    audio_list = []
    metadata = get_metadata()
    for index, item in metadata.iterrows():
        audio_list.append((item['Name'], _get_or_download(destination, item)))

    return audio_list

def get_audio_filepath(name):
    destination = _get_audio_files_destination()
    _create_destination_directory(destination)

    item = get_metadata(name)
    if item is None:
        return None
    else:
        return _get_or_download(destination, item)

def get_time_annotations(name, seconds=True):
    times_pattern = re.compile('^(\\d{1,2}\\:\\d{1,2}\\:\\d{1,2})\\s(\\d{1,2}\\:\\d{1,2}\\:\\d{1,2})')
    time_pattern = re.compile('(\\d{1,2})\\:(\\d{1,2})\\:(\\d{1,2})')

    item = get_metadata(name)
    if item is None:
        return None
    else:
        txt_filename = '{}.txt'.format(item['File'])
        txt_fullpath = os.path.join(_get_script_directory(), '..', 'data', txt_filename)

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


def _create_destination_directory(destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

def _get_script_directory():
    return os.path.dirname(os.path.realpath(__file__))

def _get_audio_files_destination():
    return (os.path.join(os.getcwd(), os.environ['TALC_AUDIO_DIRECTORY']) if 'TALC_AUDIO_DIRECTORY' in os.environ
            else os.path.join(_get_script_directory(), '..', '.audio'))

def _get_or_download(destination, item):
    wav_filename = '{}.wav'.format(item['File'])
    wav_fullpath = os.path.join(destination, wav_filename)

    if not os.path.exists(wav_fullpath):
        # do not write info and error messages to stdout/stderr
        devnull = open(os.devnull, 'w')
        stdout, stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = devnull, devnull

        yt = YouTube(item['Link'])

        # download first available audio stream
        stream = yt.streams.filter(only_audio=True).first()
        output_file = os.path.join(destination, stream.default_filename)
        stream.download(output_path=destination)

        # convert the stream into standard format, i.e. Mono PCM 16b Little Endian with 22.05kHz sampling rate
        input = av.open(output_file)
        output = av.open(wav_filename, 'w')
        resampler = av.AudioResampler('s16', 1, 22050)

        stream = output.add_stream('pcm_s16le', 22050)
        stream.layout = 'mono'
        stream.channels = 1

        for frame in input.decode(audio=0):
            frame = resampler.resample(frame)

            for packet in stream.encode(frame):
                output.mux(packet)

        for packet in stream.encode():
            output.mux(packet)

        # write output file
        output.close()

        # remove temporary file
        os.remove(output_file)

        # restore stdout and stderr
        sys.stdout, sys.stderr = stdout, stderr

    return wav_fullpath
