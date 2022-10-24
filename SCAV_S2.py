import os
import time
import numpy as np


def video_trim(input_file, start='00:00:00', dur='00:10:30'):
    """
    Create a new video file with the same format as the input with duration N seconds.
    :param input_file: str
        Absolut path to the input file
    :param start: str
        Where the cut starts
    :param dur: str
        Duration of the video
    :return: str
        Path to the output file
    """
    try:
        os.remove('output.mp4')
        print('Removing existing output file')
    except FileNotFoundError:
        print('Creating output file')

    os.system('ffmpeg -i {0} -ss {1} -t {2} -c:v copy -c:a copy output.mp4'.format(input_file, start, dur))
    return os.path.abspath('output.mp4')


def yuv_histogram(input_file='/Users/alvaro/BBB_1080p_60fps.mp4'):
    """
    Display the YUV histogram from the video trimmed in exercise 1 and create a new video with both images at the same
    time.
    :param input_file: str
        Absolut path to the input file
    """
    path = video_trim(input_file, '00:09:00', '00:00:15')

    try:
        os.remove('output_hist.mp4')
        print('Removing existing output file')
    except FileNotFoundError:
        print('Creating output file')

    os.system(
        'ffmpeg -i {0} -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay" output_hist.mp4'.format(
            path))

    # OTHER OPTIONS
    # os.system('ffplay -i {0} -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay"'.format(input_file))


def resize(input_file, sizes=None, dur='00:00:15'):
    """
    Resize the BBB video into 4 different video outputs: 720p, 480p, 360x240, 160x120.
    :param input_file: str
        Absolut path to the input file
    :param sizes: numpy array
        List of all resolutions
    :param dur:
        Duration of the video
    """
    if sizes is None:
        sizes = np.array(['720p', '480p', '360x240', '160x120'])

    try:
        os.remove('output_160x120.mp4')
        os.remove('output_360x240.mp4')
        os.remove('output_480p.mp4')
        os.remove('output_720p.mp4')
        print('Removing existing output files')
    except FileNotFoundError:
        print('Creating output files')

    path = video_trim(input_file, '00:00:45', dur)
    for size in sizes:
        if size == '720p' or size == '480p':
            os.system('ffmpeg -i {0} -vf scale=-1:{2} -preset slow -crf 18 output_{2}.mp4'.format(path, size[:3], size))
        else:
            os.system('ffmpeg -i {0} -vf scale={2} -preset slow -crf 18 output_{2}.mp4'.format(path, size, size))


def mono_stereo(input_file, dur='00:00:20', to_mono=True, to_stereo=False):
    """
    Change the stereo audio into mono output and the opposite, depending on the input file
    :param input_file: str
        Absolut path to the input file
    :param dur: str
        Duration of the video
    :param to_mono: bool
    :param to_stereo: bool
    """
    path = video_trim(input_file, '00:00:45', dur)

    try:
        os.remove('output_mono.mp4')
        os.remove('output_stereo.mp4')
        print('Removing existing output files')
    except FileNotFoundError:
        print('Creating output files')

    # Change to_mono or to_stereo variable depending on the input video
    if to_mono:
        os.system('ffmpeg -i {0} -c:v copy -ac 1 output_mono.mp4'.format(path))
    elif to_stereo:
        path = '/Users/alvaro/PycharmProjects/pythonProject/output_mono.mp4'
        os.system('ffmpeg -i {0} -c:v copy -ac 2 output_stereo.mp4'.format(path))


if __name__ == '__main__':
    # You may need to change the path_to_file value in order to run the code.
    # Change it also in some functions declared above (yuv_histogram, mono_stereo)
    path_to_file = '/Users/alvaro/BBB_1080p_60fps.mp4'

    print('1. Video trim to N seconds\n'
          '2. YUV Histogram\n'
          '3. Resize video\n'
          '4. Change from mono to stereo and vice-versa')
    input_option = int(input('Choose option: '))

    if input_option == 1:
        N = int(input('Video duration (seconds): '))
        N = np.clip(N, 0, 630)
        duration = time.strftime("%H:%M:%S", time.gmtime(float(N)))
        video_trim(path_to_file, dur=duration)
    elif input_option == 2:
        yuv_histogram(path_to_file)
    elif input_option == 3:
        sizes = np.array(['720p', '480p', '360x240', '160x120'])
        resize(path_to_file, sizes)
    elif input_option == 4:
        mono_stereo(path_to_file, to_mono=False, to_stereo=True)
