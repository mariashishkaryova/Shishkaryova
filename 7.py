import RPi.GPIO as gpio
import time
from matplotlib import pyplot as plt

gpio.setmode(gpio.BCM)
leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
bits = len(dac)
levels = 2 ** bits
maxvoltage = 3.3
comp = 14
troyka = 13
gpio.setup(troyka, gpio.OUT)
gpio.setup(comp, gpio.IN)
gpio.setup(dac, gpio.OUT)
gpio.setup(leds, gpio.OUT)


def decimal2binary(a):
    return [int(elem) for elem in bin(a)[2:].zfill(8)]


def adc():
    value_res = 0
    temp_value = 0
    for i in range(8):
        pow2 = 2 ** (8 - i - 1)
        temp_value = value_res + pow2
        signal = decimal2binary(temp_value)
        gpio.output(dac, signal)
        time.sleep(0.005)
        compval = gpio.input(comp)
        if compval == 0:
            value_res = value_res + pow2
    return value_res


try:
    time_start = time.time()
    count = 0
    data = []
    all_time = []
    voltage = 0
    gpio.output(troyka, 1)
    print('Зарядка конденсатора')
    while voltage <= 203:
        voltage = adc()
        print(voltage)
        data.append(voltage / 256 * 3.3)
        time.sleep(0)
        count += 1
        gpio.output(leds, decimal2binary(voltage))
        all_time.append(time.time() - time_start)
    gpio.output(troyka, 0)
    print('РАЗРЯДКА конденсатора')

    while voltage >= 193:
        voltage = adc()
        print(voltage)
        data.append(voltage / 256 * 3.3)
        time.sleep(0)
        count += 1
        gpio.output(leds, decimal2binary(voltage))
        all_time.append(time.time() - time_start)

    time_end = time.time()
    time_total = time_end - time_start
    print('Графики')

    plt.plot(all_time, data)
    plt.xlabel('секунды')
    plt.ylabel('напряжение')
    print('запись в файл')

    with open('data.txt', 'w') as f:
        for i in data:
            f.write(str(i) + '\n')
    with open('settings.txt', 'w') as f:
        f.write('частота дискретизации ' + str(1 / time_total * count) + 'Гц' + "\n")
        f.write('Шаг квантования = 0.0129 В')
    print('завершение программы')
finally:
    gpio.output(leds, 0)
    gpio.output(dac, 0)
    gpio.cleanup()
    plt.show()
