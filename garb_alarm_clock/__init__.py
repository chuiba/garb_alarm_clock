"""Top-level package for garb-alarm-clock."""

__author__ = """chuiba"""
__email__ = 'chuibachuibachuiba@163.com'
__version__ = '0.2.1'

# -*- coding: utf-8 -*-
#from designer.MainWindow import Ui_MainWindow
try:
    from .MainWindow import Ui_MainWindow
    from . import garb
except ImportError:
    from MainWindow import Ui_MainWindow
    import garb
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import QTimer
import requests
from datetime import datetime


def get_time():
    now = datetime.now()
    return now.strftime("%Y/%m/%d %H:%M:%S")

def get_image(url):
    res = requests.get(url)
    photo = QPixmap()
    photo.loadFromData(res.content)
    return photo

def main():
    print("hello garb")

def start_gui():
    # 主程序
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    components = Ui_MainWindow()
    components.setupUi(mainwindow)

    def refresh_garb_number():
        item_id = components.item_id.text()
        name, image, avatar, surplus, quantity, number = garb.get_garb_info(item_id)

        components.number.setText(number)
        components.cur_date.setText(get_time())

    def refresh_info():
        # 更新界面显示
        item_id = components.item_id.text()
        name, image, avatar, surplus, quantity, number = garb.get_garb_info(item_id)

        components.garb_name.setText(name)
        components.avator.setPixmap(get_image(avatar))
        components.avator.setScaledContents(True)
        components.number.setText(number)
        components.cur_date.setText(get_time())
        palette = QPalette()
        pix = get_image(image)
        pix = pix.scaled(mainwindow.width(), mainwindow.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        mainwindow.setPalette(palette)

    def button_click():
        refresh_info()
        if (int(components.interval.text()) < 60):
            # 为了防止访问频率过高被封，所以默认限制为每分钟访问一次
            components.default_interval = 60
        else:
            components.default_interval = int(components.interval.text())

        mainwindow.timer.start(1000)

    def on_timer():
        interval = int(components.interval.text())
        if (interval > 0):
            interval = interval - 1
        else:
            refresh_garb_number()
            interval = components.default_interval

        components.interval.setText(str(interval))
        components.cur_date.setText(get_time())

    components.pushButton.clicked.connect(button_click)

    # 默认设置一个
    components.item_id.setText("4389")
    components.default_interval = 60

    # 刷新信息
    refresh_info()

    mainwindow.timer = QTimer(mainwindow)
    mainwindow.timer.timeout.connect(on_timer)

    # 显示
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start_gui()
