import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)


def to_bin(num):
    return [int(i) for i in bin(int(num)[2:].zfill(8))]


def value(num):
    '{:.4f}'.format((int(num) / 2**8) * 3.3)


def if_float(num):
    num = [str(i) for i in num]
    if num.count('.') == 1:
        tar = num.index('.')
        num.pop(tar)
        if num[0] == '-':
            num.pop(0)
        num = str(''.join(num))
        if num.isdigit():
            return True
    return False


def if_negative(num):
    num = str(num)
    if num[0] == '-':
        if num[1:].isdigit():
            return True
    return False


try:
    while True:
        key = input("Введите целое число от 0 до 255 ")
        if key.isdigit():
            if int(key) > 255:
                print("Ваше число больше, чем 255")
            else:
                GPIO.output(dac, to_bin(key))
            print(value(key))
    else:
        if str(key) == 'q':
            break
        elif if_float(key):
            print("Ваше число не целое")
        elif if_negative(key):
            print("Ваше число отрицательное")
        else:
            print("Вы ввели не число")
            


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()