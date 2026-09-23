import serial
import time

stm32 = serial.Serial("COM4", 9600, timeout=2)

time.sleep(1)

stm32.write(b"Hello\r\n")

stm32.close()