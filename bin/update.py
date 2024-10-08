import re
from serial.tools import list_ports
import subprocess
import sys
import time

# nuitka.bat --standalone --show-progress --show-memory --onefile --output-dir=out update.py
while (True):
    ports = list(list_ports.comports())
    port = None
    for i in range(len(ports)):
        port = list(ports[i])
        if (re.match("USB VID:PID=303A:1001", port[2])):
            port = port[0]
            break
    if port == None:
        print("未找到INFRARED设备,请安装驱动或检查设备是否插入！")
        time.sleep(1)
        continue

    print("检测到INFRARED,升级开始...")
    cmd = "./esptool.exe --chip auto --port {} --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode qio --flash_freq 80m --flash_size detect  0x0000 ./bootloader.bin 0x8000 ./partitions.bin 0xe000 ./boot_app0.bin 0x10000 ./firmware.bin 0x2D0000 ./littlefs.bin".format(
        port)
    p = subprocess.Popen(cmd, stdout=sys.stdout)
    p.communicate()
    print("升级成功！按任意键退出。")
    input()
