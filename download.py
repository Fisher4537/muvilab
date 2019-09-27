import os
import subprocess
from threading import Thread
from queue import Queue


USER = "hackathon"
IP = "40.135.146.95"
BOARD_PATH = os.path.join("/mnt3/", "board")
BOARD_URL = USER+"@"+IP+":"+BOARD_PATH


class Downloader(Thread):
    def __init__(self, url, dest_folder='.'):
        Thread.__init__(self)
        self.url = url
        self.destination_folder = dest_folder

    def run(self):
        try:
            cmd = "scp {} {}".format(self.url, self.destination_folder).split()
            print("command: {}".format(str(cmd)))
            print('Downloading {} to {} ...'.format(self.url, self.destination_folder))
            subprocess.call(cmd)
        finally:
            if os.path.isfile(self.destination_folder):
                print('Download completed!')
            else:
                print('[ERROR] Download failed! ({})'.format(self.destination_folder))


def get_url_list(server, cams=None, disps=None, foods=None):
    queue = Queue()
    for cam in cams:
        for disp in disps:
            for food in foods:
                cmd = 'ssh {} '.format(server).split() + ["ls {}".format(os.path.join(BOARD_PATH, cam, disp, food))]
                try:
                    remote_video_str = subprocess.check_output(cmd)
                    for name in str(remote_video_str)[2:-4].split('\\n'):
                        queue.put(os.path.join(server, BOARD_PATH, cam, disp, food, name))
                except subprocess.CalledProcessError:
                    print("[WARNING] Fail to download {}".format(os.path.join(server, BOARD_PATH, cam, disp, food)))
                    continue


