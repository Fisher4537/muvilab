# -*- coding: utf-8 -*-

import os
import subprocess
import sys
from annotator import Annotator
from download import Downloader

'''This example downloads a youtube video from the Olympic games, splits it into
several clips and let you annotate it'''

# Set up local
if __name__ == "__main__":
    demo_folder = '.'
    clips_folder = os.path.join(demo_folder, 'clips')
    tags_folder = os.path.join(demo_folder, 'tag')
    video_folder = os.path.join(demo_folder, 'video')
    video_name = sys.argv[1]
    video_path = os.path.join(video_folder, video_name)

    tag_file_name = os.path.basename(video_name).split('.')[0] + '.json'
    tag_file_path = os.path.join(tags_folder, tag_file_name)

    # setup remote
    hackathon_user = 'hackathon'
    hackathon_ip = '40.113.146.95'
    board_path = os.path.join('/mnt3/', 'board')
    board_url = hackathon_user + '@' + hackathon_ip + ':' + board_path
    server = hackathon_user + '@' + hackathon_ip
    url = server + ':' + os.path.join(board_path, '102', 'centrale', 'PotatoWedges', video_name)


    # Create the folders
    if not os.path.exists(demo_folder):
        os.mkdir(demo_folder)
    if not os.path.exists(clips_folder):
        os.mkdir(clips_folder)

    # Download from youtube: "Women's Beam Final - London 2012 Olympics"
    if not os.path.isfile(video_path):
        downloader = Downloader(url, video_folder)
        downloader.start()
        downloader.join()
    else:
        print('Video {} is ready to be tagged'.format(video_path))

    # Initialise the annotator
    annotator = Annotator([
        {'name': 'background', 'color': (0, 255, 0)},
        {'name': 'ignore', 'color': (0, 0, 255)},
        {'name': 'food', 'color': (0, 255, 255)}],
        clips_folder, sort_files_list=True, N_show_approx=100, screen_ratio=16/9,
        image_resize=1, loop_duration=None, annotation_file=tag_file_path)

    # Split the video into clips
    print('Generating clips from the video...')
    annotator.video_to_clips(video_path, clips_folder, clip_length=15, overlap=0, resize=0.5)

    # Run the annotator
    annotator.main()
