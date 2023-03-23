# -*- coding:utf-8 -*-

# %gui qt
#プロット関係のライブラリ
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import serial
from serial.tools import list_ports
import sys
import datetime
import csv

DATA_NUM = 2
SAMPLE_NUM = 4000
YRANGE_MIN = 0
YRANGE_MAX = 4096

exec_time = datetime.datetime.now()


def select_port():
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.timeout = 1

    ports = list_ports.comports()
    devices = [info.device for info in ports]

    if len(devices) == 0:
        print("error: device not found")
        return None
    elif len(devices) == 1:
        print("only found %s" % devices[0])
        ser.port = devices[0]
    else:
        # ポートが複数見つかった場合それらを表示し選択させる
        for i in range(len(devices)):
            print("input %3d: open %s" % (i, devices[i]))
        print("input number of target port >> ",end="")
        num = int(input())
        ser.port = devices[num]

    # 開いてみる
    try:
        ser.open()
        return ser
    except:
        print("error when opening serial %s" % ser.port)
        return None


class PlotWindow:
    def __init__(self):
        self.ser = select_port()
        self.axi_num = DATA_NUM  # データ数
        self.colors = [(255, 0, 0), (0, 255, 0), (255, 255, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]
        # プロット初期設定
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle(u"リアルタイムプロット")
        self.plt = self.win.addPlot()   # プロットのビジュアル関係
        self.plt.setYRange(YRANGE_MIN, YRANGE_MAX)    # y軸の上限、下限の設定
        self.curve = list()
        for i in range(self.axi_num):
            self.curve.append(self.plt.plot(pen=self.colors[i]))    # プロットデータを入れる場所
        # self.curve2 = self.plt.plot(pen=(0,255,0))    # プロットデータを入れる場所
        self.sample_num = SAMPLE_NUM

        # self.ser = serial.Serial(port='/dev/cu.usbmodem2123201', baudrate=115200, timeout=1)

        # アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1)    # 10msごとにupdateを呼び出し

        # UART受信データ(data)
        self.data = list()
        for i in range(self.axi_num):
            self.data.append([0])

    def update(self):            
        # データの読み取り
        recv = self.ser.readline()
        if recv:
            # print(recv)
            str_value = recv.decode('utf-8')
            # print(str_value)
            rstr = str_value.strip()            # 文字列に含まれる空白を削除
            values = rstr.split(',')
            # print(value)
            sensor_value = [float(s) for s in values]
            print(sensor_value)
            with open('data/sht31/{}.csv'.format(exec_time.strftime('%Y%m%d%H%M%S')), 'a') as f:
                dt_now = datetime.datetime.now()
                writer = csv.writer(f)
                writer.writerow([dt_now] + sensor_value)
            # # 16進数2桁のデータ2つを一気にデコード
            # ReceData = np.frombuffer(ReceData,dtype=np.uint8)

            for i, val in enumerate(sensor_value):
                if i > self.axi_num - 1:
                    break
                self.data[i].append(val)

            now_data_len = len(self.data[0])
            if now_data_len > self.sample_num * 10:
                for d in self.data:
                    del d[:self.sample_num * 5]
                # del self.data[0]

            # lmax = max(self.data)
            # lmin = min(self.data)
            # self.plt.setYRange(lmin, lmax)
            self.plt.setXRange(now_data_len - self.sample_num, now_data_len)
            for i, cur in enumerate(self.curve):
                cur.setData(self.data[i])
            # self.ser.write(bytearray([70])) #デバック用送信器


if __name__ == "__main__":
    plotwin = PlotWindow()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
