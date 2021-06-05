# -*- coding:utf-8 -*-

# %gui qt
#プロット関係のライブラリ
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import serial
import sys


class PlotWindow:
    def __init__(self):
        # プロット初期設定
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle(u"リアルタイムプロット")
        self.plt = self.win.addPlot()   # プロットのビジュアル関係
        self.plt.setYRange(-5000000, 5000000)    # y軸の上限、下限の設定
        self.curve = self.plt.plot()    # プロットデータを入れる場所
        self.sample_num = 2048

        self.ser = serial.Serial(port='/dev/cu.usbmodem2123201', baudrate=115200, timeout=1)

        # アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)    # 10msごとにupdateを呼び出し

        # UART受信データ(data)
        self.data = [0]

    def update(self):            
        # データの読み取り
        recv = self.ser.readline()
        if recv:
            # print(recv)
            str_value = recv.decode('utf-8')
            value = str_value.strip()            # 文字列に含まれる空白を削除
            # print(value)
            sensor_value = int(value)

            # # 16進数2桁のデータ2つを一気にデコード
            # ReceData = np.frombuffer(ReceData,dtype=np.uint8)

            self.data.append(sensor_value)
            if len(self.data) > self.sample_num:
                del self.data[0]

            # lmax = max(self.data)
            # lmin = min(self.data)
            # self.plt.setYRange(lmin, lmax)
            self.curve.setData(self.data)   # プロットデータを格納
            # self.ser.write(bytearray([70])) #デバック用送信器


if __name__ == "__main__":
    plotwin = PlotWindow()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

# # https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_sgskip.html
# # https://matplotlib.org/gallery/animation/simple_anim.html


# import tkinter

# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.figure import Figure
# import matplotlib.animation as animation

# import numpy as np

# import serial


# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate


# def init():  # only required for blitting to give a clean slate.
#     line.set_ydata(np.sin(x))
#     return line,


# def animate(i):
#     line.set_ydata(np.sin(x + i))  # update the data.
#     return line,


# root = tkinter.Tk()
# root.wm_title("Embedding in Tk anim")

# fig = Figure()
# # FuncAnimationより前に呼ぶ必要がある
# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

# x = np.arange(0, 3, 0.01)  # x軸(固定の値)
# l = np.arange(0, 8, 0.01)  # 表示期間(FuncAnimationで指定する関数の引数になる)
# plt = fig.add_subplot(111)
# plt.set_ylim([-1.1, 1.1])
# line, = plt.plot(x, np.sin(x))

# ani = animation.FuncAnimation(fig, animate, l, init_func=init, interval=10, blit=True,)

# toolbar = NavigationToolbar2Tk(canvas, root)
# canvas.get_tk_widget().pack()

# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack()

# tkinter.mainloop()