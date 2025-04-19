import tkinter as tk
import time
from link import Serial, Tcp

serial = Serial()
tcp = Tcp("192.168.4.1")
port = serial

# nuitka.bat --standalone --show-progress --windows-disable-console --enable-plugin=tk-inter --show-memory --onefile --output-dir=out main.py


def show_temperature():
    try:
        port.send(b"blackbody read\r\n")
        time.sleep(0.3)
        data = port.recv()
        if data is not None:
            # 解码并去除多余空白字符
            decoded_data = data.decode().strip()
            # 拆分字符串并转换为浮点数，保留两位小数
            num1, num2 = map(lambda x: round(
                float(x), 2), decoded_data.split())
            label.config(text=f"校准前: {num1}°C\r\n校准后: {num2}°C")
        root.after(1000, show_temperature)
    except Exception as e:
        root.after(1000, show_temperature)


def show_output(message, color=None):
    output_label.config(text=message, fg=color)


def clear_respoonse():
    show_output("")


def button1_action():
    port.send(b"blackbody reset\r\n")
    time.sleep(0.3)
    temp = port.recv()
    if temp == b"success\r\n":
        show_output("执行成功", "green")
    else:
        show_output("执行失败", "red")
    root.after(1000, clear_respoonse)


def button2_action():
    port.send(b"blackbody 50\r\n")
    time.sleep(0.3)
    temp = port.recv()
    if temp == b"success\r\n":
        show_output("执行成功", "green")
    else:
        show_output("执行失败", "red")
    root.after(1000, clear_respoonse)


def button3_action():
    port.send(b"blackbody 100\r\n")
    time.sleep(0.3)
    temp = port.recv()
    if temp == b"success\r\n":
        show_output("执行成功", "green")
    else:
        show_output("执行失败", "red")
    root.after(1000, clear_respoonse)


def button4_action():
    port.send(b"calibrate\r\n")
    time.sleep(0.3)
    temp = port.recv()
    if temp == b"success\r\n":
        show_output("执行成功", "green")
    else:
        show_output("执行失败", "red")
    root.after(1000, clear_respoonse)


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title("黑体温度校准助手")
    root.geometry("300x300")

    # 创建显示温度的标签
    label = tk.Label(root, text="校准前: --°C\r\n校准后: --°C", font=("Arial", 14))
    label.pack(pady=10)

    # 创建输出信息的标签（移动到按钮上方）
    output_label = tk.Label(root, text="", font=("Arial", 12))
    output_label.pack(pady=10)

    # 创建按钮，并增加间隔和调整宽度
    button1 = tk.Button(root, text="清空黑体数据", command=button1_action, width=15)
    button1.pack(pady=5)

    button2 = tk.Button(root, text="50℃", command=button2_action, width=15)
    button2.pack(pady=5)

    button3 = tk.Button(root, text="100℃", command=button3_action, width=15)
    button3.pack(pady=5)

    button3 = tk.Button(root, text="一致性校准", command=button4_action, width=15)
    button3.pack(pady=5)

    # 启动温度刷新
    show_temperature()
    # 运行主循环
    root.mainloop()
