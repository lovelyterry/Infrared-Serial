import re
from serial.tools import list_ports
import subprocess
import sys
import time

# nuitka.bat --standalone --show-progress --show-memory --onefile --output-dir=out update.py
ports = list(list_ports.comports())
port = None
for i in range(len(ports)):
    port = list(ports[i])
    if (re.match("USB VID:PID=303A:1001", port[2])):
        port = port[0]
        break
if port == None:
    print("未找到INFRARED设备,请安装驱动或检查设备是否插入！")
    print("是否安装驱动？按Y安装驱动，按N退出")
    if (input() == "Y"):
        cmd = ".\idf-env.exe driver install --espressif"
        p = subprocess.Popen(cmd, stdout=sys.stdout)
        p.communicate()
    input()
else:
    print("检测到INFRARED,升级开始...")
    cmd = "./esptool.exe --chip auto --port {} --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode qio --flash_freq 80m --flash_size detect  0x0000000 ./bootloader.bin 0x0008000 ./partitions.bin 0x0001e000 ./boot_app0.bin 0x0020000 ./firmware.bin 0x002FB000 ./littlefs.bin".format(
        port)
    p = subprocess.Popen(cmd, stdout=sys.stdout)
    p.communicate()
    print("升级成功!")
    time.sleep(3)