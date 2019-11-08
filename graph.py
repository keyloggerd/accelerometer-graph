import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import smbus
import math
import datetime

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect

# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

fig, ax = plt.subplots()
xl, = ax.plot(np.random.rand(10), label='x')
yl, = ax.plot(np.random.rand(10), label='y')
zl, = ax.plot(np.random.rand(10), label='z')
ax.set_ylim(-1, 1)
ax.legend()

def update(data):
    xl.set_ydata(data[0])
    yl.set_ydata(data[1])
    zl.set_ydata(data[2])
    # return line,


def data_gen():
    while True:
        xs = np.arange(1, 11, dtype=np.float)
        ys = np.arange(1, 11, dtype=np.float)
        zs = np.arange(1, 11, dtype=np.float)
        for i in range(10):
            while True:
                try:
                    xs[i] = read_word_2c(0x3b) / 16384.0
                    ys[i] = read_word_2c(0x3d) / 16384.0
                    zs[i] = read_word_2c(0x3f) / 16384.0
                    break
                except IOError:
                    continue

        yield (xs, ys, zs)

ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
plt.show()
