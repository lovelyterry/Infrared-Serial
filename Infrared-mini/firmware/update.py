import re
from serial.tools import list_ports
import subprocess
import sys
import time


# Windows 适用
try:
    import msvcrt

    def getch():
        return msvcrt.getch().decode("utf-8")

# Unix/Linux/macOS 适用
except ImportError:
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)  # 设置终端为 raw 模式，禁用回显
            char = sys.stdin.read(1)  # 读取一个字符
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # 还原终端设置
        return char

# nuitka.bat --standalone --show-progress --show-memory --onefile --output-dir=out update.py
while True:
    ports = list(list_ports.comports())
    port = None
    for i in range(len(ports)):
        port = list(ports[i])
        if (re.match("USB VID:PID=303A:1001", port[2])):
            port = port[0]
            break
    if port == None:
        print("未找到INFRARED设备,请安装驱动或检查设备是否插入！")
        print("是否安装驱动？按Y安装驱动，按C重试，按其他键退出")
        cmdChar = getch()
        if (cmdChar == "Y" or cmdChar == "y"):
            cmd = ".\idf-env.exe driver install --espressif"
            p = subprocess.Popen(cmd, stdout=sys.stdout)
            p.communicate()
        elif (cmdChar == "C" or cmdChar == "c"):
            continue
        else:
            exit()
    else:
        print("检测到INFRARED,升级开始...")
        cmd = "./esptool.exe --chip auto --port {} --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode qio --flash_freq 80m --flash_size detect  0x0000000 ./bootloader.bin 0x0008000 ./partitions.bin 0x0001e000 ./boot_app0.bin 0x0020000 ./firmware.bin 0x002FB000 ./littlefs.bin".format(
            port)
        p = subprocess.Popen(cmd, stdout=sys.stdout)
        p.communicate()
        print("升级成功!")
        time.sleep(3)
        exit()
