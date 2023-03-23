# -*- coding:utf-8 -*-

# %gui qt
#プロット関係のライブラリ
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np
import serial
from serial.tools import list_ports
import sys
import datetime
import csv
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
sh = logging.StreamHandler(sys.stdout)
logger.addHandler(sh)

# フォーマッタを定義する（第一引数はメッセージのフォーマット文字列、第二引数は日付時刻のフォーマット文字列）
# fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%dT%H:%M:%S")
fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%dT%H:%M:%S")
# フォーマッタをハンドラに紐づける
sh.setFormatter(fmt)

DATA_NUM = 6
SAMPLE_NUM = 1000
YRANGE_MIN = -2000
YRANGE_MAX = 2000

exec_time = datetime.datetime.now()
save_filename = 'data/forklift_acc/{}.csv'.format(exec_time.strftime('%Y%m%d%H%M%S'))


def select_port():
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.timeout = 1

    ports = list_ports.comports()
    devices = [info.device for info in ports]

    if len(devices) == 0:
        logger.warning("error: device not found")
        return None
    elif len(devices) == 1:
        logger.warning("only found %s" % devices[0])
        ser.port = devices[0]
    else:
        # ポートが複数見つかった場合それらを表示し選択させる
        for i in range(len(devices)):
            print("input %3d: open %s" % (i, devices[i]))
        print("input number of target port >> ", end="")
        num = int(input())
        ser.port = devices[num]

    # 開いてみる
    try:
        ser.open()
        return ser
    except Exception:
        logger.warning("error when opening serial %s" % ser.port)
        return None


class PlotWindow:
    def __init__(self):
        self.ser = select_port()
        self.axi_num = DATA_NUM  # データ数
        self.colors = [(255, 0, 0), (0, 255, 0), (255, 255, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]
        # プロット初期設定
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle(u"リアルタイムプロット")    # プロットのタイトル
        self.plt = self.win.addPlot()   # プロットのビジュアル関係
        self.plt.setYRange(YRANGE_MIN, YRANGE_MAX)    # y軸の上限、下限の設定
        self.curve = list()
        for i in range(self.axi_num):
            self.curve.append(self.plt.plot(pen=self.colors[i]))    # プロットデータを入れる場所
        self.sample_num = SAMPLE_NUM

        # アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1)    # 10msごとにupdateを呼び出し

        # UART受信データ(data)
        self.data = np.zeros((1, self.axi_num + 1))
        logger.info(self.data)
        # for i in range(self.axi_num + 1):
        #     self.data.append([0])   # 空データの挿入

    def update(self):
        # データの読み取り
        recv = self.ser.readline()
        if recv:
            # print(recv)
            str_value = recv.decode('utf-8')
            # print(str_value)
            str_rsp = str_value.strip()    # 文字列に含まれる空白を削除
            values = str_rsp.split(',')    # カンマで分割
            # print(value)
            sensor_value = [float(s) for s in values]
            logger.debug(sensor_value)
            # with open('data/forklift_acc/{}.csv'.format(exec_time.strftime('%Y%m%d%H%M%S')), 'a') as f:
            #     dt_now = datetime.datetime.now()
            #     writer = csv.writer(f)
            #     writer.writerow([dt_now] + sensor_value)
            # # 16進数2桁のデータ2つを一気にデコード
            # ReceData = np.frombuffer(ReceData,dtype=np.uint8)
            sen_val = sensor_value[:self.axi_num]
            sen_val.append(datetime.datetime.now())
            self.data = np.append(self.data, np.array([sen_val]), axis=0)
            # for i, val in enumerate(sensor_value):
            #     if i > self.axi_num:
            #         break
            #     self.data[i + 1].append(val)
            now_data_len = self.data.shape[0]
            if now_data_len > self.sample_num * 10:
                logger.debug("========= save ===========")
                extract = self.data[:self.sample_num * 9]
                with open(save_filename, 'a') as f_handle:
                    np.savetxt(f_handle, extract, fmt='%s', delimiter=',')
                self.data = np.delete(self.data, slice(self.sample_num * 9), 0)
                # with open('data/forklift_acc/{}.csv'.format(exec_time.strftime('%Y%m%d%H%M%S')), 'a') as f:
                #     writer = csv.writer(f)

                #     for d in self.data:
                #         del d[:self.sample_num * 95]
                # del self.data[0]

            # lmax = max(self.data)
            # lmin = min(self.data)
            # self.plt.setYRange(lmin, lmax)
            self.plt.setXRange(now_data_len - self.sample_num, now_data_len)
            for i, cur in enumerate(self.curve):
                cur.setData(list(self.data[:, i]))
            # self.ser.write(bytearray([70])) #デバック用送信器


if __name__ == "__main__":
    plotwin = PlotWindow()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec()

    with open(save_filename, 'a') as f_handle:
        np.savetxt(f_handle, plotwin.data, fmt='%s', delimiter=',')
                    
