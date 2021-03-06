# coding=utf-8
# author: Lan_zhijiang
# description: 启动ALR_Cloud的脚本

import sys
import threading
import argparse
import json
import socket
from main_system.log import AlrCloudLog
from network_communicator.connection_manager.websocket_server import AlrCloudWebsocketServer
sys.path.append("./network_communicator/connection_manager/")
import http_server


class AlrCloudRunInit():

    def __init__(self):

        self.basic_setting = json.load(open("./setting/cloud_setting/basic_setting.json", encoding="utf-8"))
        self.log = AlrCloudLog()
        self.ws_server = AlrCloudWebsocketServer(self.log)

        # update host ip
        self.basic_setting["hostIp"] = self.get_ip()
        json.dump(self.basic_setting, open("./setting/cloud_setting/basic_setting.json", "w", encoding="utf-8"))
        self.basic_setting = json.load(open("./setting/cloud_setting/basic_setting.json", encoding="utf-8"))

    def get_ip(self):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip

    def run(self):

        """
        启动ALR_Cloud
        :return:
        """
        print("""
            ##################################
              Hadream-AutoLearningRobotCloud
                   Author: Lan_zhijiang
            ##################################
            Github: 
              https://github.com/AutoLearningRobotHadream/ALR_Cloud
            E-mail:
              lanzhijiang@foxmail.com
        """)
        self.log.add_log(1, "###   New ALR_Cloud Log   ###", is_print=False, is_period=False)
        self.log.add_log(1, "RunInit: Start ALR_Cloud")

        # 启动HTTP+WEBSOCKET服务器-并发线程 #
        self.log.add_log(1, "RunInit: Start http and websocket server...")
        http_server_thread = threading.Thread(target=http_server.run_flask, args=(self.log,))
        websocket_server_thread = threading.Thread(target=self.ws_server.run_websocket_server, args=())
        http_server_thread.start()
        websocket_server_thread.start()

acri = AlrCloudRunInit()
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", default="normal")
args = parser.parse_args()
if args.mode == "normal":
    acri.run()
else:
    print("It's still not finished...")

