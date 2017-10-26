import platform
import time
import usb.core
import usb.util
import cv2

class Armageddon(object):
    """
    Based on https://github.com/codedance/Retaliation
    """
    DOWN = 0x01
    UP = 0x02
    LEFT = 0x04
    RIGHT = 0x08
    FIRE = 0x10
    STOP = 0x20

    def __init__(self):
        self._get_device()
        self._detach_hid()
        self.DEVICE.set_configuration()

    def _get_device(self):
        self.DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)

    def _detach_hid(self):
        if "Linux" == platform.system():
            try:
                self.DEVICE.detach_kernel_driver(0)
            except Exception, e:
                pass

    def send_cmd(self, cmd):
        self.DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])

    def send_move(self, cmd, duration_ms):
        self.send_cmd(cmd)
        time.sleep(duration_ms / 1000.0)
        self.send_cmd(self.STOP)

instance = Armageddon()
cv2.namedWindow('StormLauncher Controls')
cv2.moveWindow('StormLauncher Controls', 100, 100)
img_controls = cv2.imread('controls.png',0)
continue_flag = True
while(continue_flag):
  cmd_type = 0

  cv2.imshow('StormLauncher Controls', img_controls)
  key = cv2.waitKey(0)

  #print("Key: " + str(key))

  if(key == 113):
    continue_flag = False
  if key == 119:
    cmd = instance.UP
  elif key == 97:
    cmd = instance.LEFT
  elif key == 100:
    cmd = instance.RIGHT
  elif key == 115:
    cmd = instance.DOWN
  elif key == 120:
    cmd = instance.STOP
  elif key == 32:
    cmd = instance.FIRE
    cmd_type = 1

  if cmd_type == 0:
    instance.send_move(cmd, 20)
  else:
    instance.send_cmd(cmd)