import time
import math
import busio
import analogio
from board import GP1, GP0
import board
import adafruit_mpu6050
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

# Setup I2C and MPU6050
i2c = busio.I2C(GP1, GP0)
mpu = adafruit_mpu6050.MPU6050(i2c)
left = analogio.AnalogIn(board.A0)
right = analogio.AnalogIn(board.A1)

yaw = 0
last_time = time.monotonic()

while True:
    ax, ay, az = mpu.acceleration
    gx, gy, gz = mpu.gyro  
    current_time = time.monotonic()
    dt = current_time - last_time
    last_time = current_time
    roll = int(math.atan2(ay, az) * 180 / math.pi)
    pitch = int(math.atan2(-ax, math.sqrt(ay*ay + az*az)) * 180 / math.pi)
    yaw += gz * dt * 180 / math.pi
    m = Mouse(usb_hid.devices)
    m.move(-pitch,roll)
    if left.value>50000 and right.value>50000:
        m.press(Mouse.MIDDLE_BUTTON)
    elif left.value>50000:
        m.press(Mouse.LEFT_BUTTON)
    elif right.value>50000:
        m.press(Mouse.RIGHT_BUTTON)
    else:
        m.release_all()
    print(left.value)
    print(right.value) 
    time.sleep(0.1)
