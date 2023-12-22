import tkinter as tk
from tkinter import ttk
import serial
import threading
from serial.tools import list_ports


class SerialAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("串口调试助手")
        self.root.geometry("650x540")

        self.serial_port = None
        self.receive_data = tk.StringVar()
        self.send_data = tk.StringVar()

        # 左侧串口设置与接收设置、发送设置
        self.create_serial_settings_frame()
        self.create_receive_settings_frame()
        self.create_send_settings_frame()

        # 右侧接收数据与发送数据
        self.create_receive_data_frame()
        self.create_send_data_frame()

    def toggle_auto_scroll(self):
        # 切换自动滚屏的函数
        if self.auto_scroll_var.get():
            self.receive_text.yview(tk.END)
        else:
            self.receive_text.yview(tk.MOVETO, 0)

    def create_serial_settings_frame(self):
        frame = ttk.LabelFrame(self.root, text="串口设置")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # 获取可用的串口号
        available_ports = [port.device for port in serial.tools.list_ports.comports()]

        # 串口号选择下拉框
        self.serial_port_var = tk.StringVar()
        serial_port_label = ttk.Label(frame, text="串口号：")
        serial_port_combobox = ttk.Combobox(frame, textvariable=self.serial_port_var, values=available_ports)
        serial_port_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        serial_port_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 添加波特率、校验位、数据位、停止位等设置项
        # 注意：这里的控件变量需要在整个类中都能访问到，因此使用 self.
        self.baud_rate_var = tk.StringVar(value="9600")
        self.parity_var = tk.StringVar(value="N")
        self.data_bits_var = tk.StringVar(value="8")
        self.stop_bits_var = tk.StringVar(value="1")

        baud_rate_label = ttk.Label(frame, text="波特率：")
        baud_rate_combobox = ttk.Combobox(frame, textvariable=self.baud_rate_var, values=["9600", "115200"])
        parity_label = ttk.Label(frame, text="校验位：")
        parity_combobox = ttk.Combobox(frame, textvariable=self.parity_var, values=["N", "O", "E"])
        data_bits_label = ttk.Label(frame, text="数据位：")
        data_bits_combobox = ttk.Combobox(frame, textvariable=self.data_bits_var, values=["8", "7", "6"])
        stop_bits_label = ttk.Label(frame, text="停止位：")
        stop_bits_combobox = ttk.Combobox(frame, textvariable=self.stop_bits_var, values=["1", "1.5", "2"])

        baud_rate_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        baud_rate_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        parity_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        parity_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        data_bits_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        data_bits_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        stop_bits_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        stop_bits_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        connect_button = ttk.Button(frame, text="打开连接", command=self.toggle_serial_connection)
        connect_button.grid(row=5, column=0, columnspan=2, pady=5)

    def create_receive_settings_frame(self):
        frame = ttk.LabelFrame(self.root, text="接收设置", width=20, height=60, borderwidth=2, relief="groove")
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.receive_mode_var = tk.StringVar()
        self.auto_newline_var = tk.BooleanVar()
        self.auto_scroll_var = tk.BooleanVar()

        receive_mode_label = ttk.Label(frame, text="接收模式：")
        receive_mode_combobox = ttk.Combobox(frame, textvariable=self.receive_mode_var, values=["ASCII", "HEX"])
        auto_newline_checkbox = ttk.Checkbutton(frame, text="自动换行", variable=self.auto_newline_var)
        auto_scroll_checkbox = ttk.Checkbutton(frame, text="自动滚屏", variable=self.auto_scroll_var)

        receive_mode_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        receive_mode_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        auto_newline_checkbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        auto_scroll_checkbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def create_send_settings_frame(self):
        frame = ttk.LabelFrame(self.root, text="发送设置", width=10, height=60, borderwidth=2, relief="groove")
        frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.send_mode_var = tk.StringVar()
        self.auto_escape_var = tk.BooleanVar()
        self.auto_return_var = tk.BooleanVar()
        self.auto_send_extra_var = tk.BooleanVar()
        self.send_interval_var = tk.StringVar()

        send_mode_label = ttk.Label(frame, text="发送模式：")
        send_mode_combobox = ttk.Combobox(frame, textvariable=self.send_mode_var, values=["ASCII", "HEX"])
        auto_escape_checkbox = ttk.Checkbutton(frame, text="自动解析转义符", variable=self.auto_escape_var)
        auto_return_checkbox = ttk.Checkbutton(frame, text="AT指令自动回车", variable=self.auto_return_var)
        auto_send_extra_checkbox = ttk.Checkbutton(frame, text="自动发送附加位", variable=self.auto_send_extra_var)
        send_interval_label = ttk.Label(frame, text="循环周期(ms)：")
        send_interval_entry = ttk.Entry(frame, textvariable=self.send_interval_var)

        send_mode_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        send_mode_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        auto_escape_checkbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        auto_return_checkbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        auto_send_extra_checkbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        send_interval_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        send_interval_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    def create_receive_data_frame(self):
        # frame = ttk.LabelFrame(self.root, text="接收设置", width=20, height=60, borderwidth=2, relief="groove")
        # frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        frame = ttk.LabelFrame(self.root, text="接收数据", width=200, height=200, borderwidth=2)
        frame.grid(row=0, column=1, rowspan=2, padx=8, pady=8, sticky="nsew")

        self.receive_text = tk.Text(frame, wrap=tk.WORD, state=tk.DISABLED, height=13, width=40)
        auto_scroll_checkbox = ttk.Checkbutton(frame, text="自动滚屏", variable=self.auto_scroll_var,
                                               command=self.toggle_auto_scroll)

        self.receive_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        auto_scroll_checkbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        clear_button = ttk.Button(frame, text="清空接收区", command=self.clear_receive_text)
        clear_button.grid(row=1, column=0, padx=4, pady=4)

    def create_send_data_frame(self):
        frame = ttk.LabelFrame(self.root, text="发送数据", width=300, height=300, borderwidth=2, relief="groove")
        frame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        frame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.send_text = tk.Text(frame, wrap=tk.WORD, height=15, width=40)
        self.send_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        send_button = ttk.Button(frame, text="发送", command=self.send_data)
        send_button.grid(row=1, column=0, padx=5, pady=5)

        clear_button = ttk.Button(frame, text="清空发送区", command=self.clear_send_text)
        clear_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        # 添加循环周期的选项并换行显示

    #   send_interval_label = ttk.Label(frame, text="循环周期(ms)：")
    #   send_interval_entry = ttk.Entry(frame, textvariable=self.send_interval_var)

    #  send_interval_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    #  send_interval_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    def send_data(self):
        text = self.send_text.get("1.0", tk.END).strip()
        data = text.encode("utf-8")
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(data)
            except Exception as e:
                print(f"发送数据时发生错误：{e}")

    def clear_receive_text(self):
        self.receive_text.configure(state=tk.NORMAL)
        self.receive_text.delete("1.0", tk.END)
        self.receive_text.configure(state=tk.DISABLED)

    def clear_send_text(self):
        self.send_text.delete("1.0", tk.END)

    def toggle_serial_connection(self):
        if self.serial_port is None:
            # 打开串口连接
            try:
                self.serial_port = serial.Serial(
                    port=self.serial_port_var.get(),
                    baudrate=int(self.baud_rate_var.get()),
                    parity=self.parity_var.get(),
                    bytesize=int(self.data_bits_var.get()),
                    stopbits=int(self.stop_bits_var.get())
                )
                self.receive_text.config(state=tk.NORMAL)  # 允许接收数据
                threading.Thread(target=self.start_receive_thread, daemon=True).start()
            except Exception as e:
                tk.messagebox.showerror("错误", f"无法打开串口：{e}")
        else:
            # 关闭串口连接
            self.serial_port.close()
            self.serial_port = None
            self.receive_text.config(state=tk.DISABLED)  # 禁止接收数据

    def start_receive_thread(self):
        while self.serial_port and self.serial_port.is_open:
            try:
                data = self.serial_port.read(1)
                if data:
                    # 处理接收到的数据并显示在接收文本框中
                    self.process_received_data(data)
            except Exception as e:
                print(f"接收数据时发生错误：{e}")
                break

    def process_received_data(self, data):
        # 处理接收到的数据的函数
        # TODO: 根据接收设置的不同，处理ASCII码或HEX格式的数据

        def send_data(self):
            data = self.send_text.get("1.0", tk.END).encode("utf-8")
            if self.serial_port and self.serial_port.is_open:
                try:
                    self.serial_port.write(data)
                except Exception as e:
                    print(f"发送数据时发生错误：{e}")

        def toggle_auto_scroll(self):
            # 切换自动滚屏的函数
            if self.auto_scroll_var.get():
                self.receive_text.yview(tk.END)
            else:
                self.receive_text.yview(tk.MOVETO, 0)


if __name__ == "__main__":
    root = tk.Tk()
    app = SerialAssistant(root)
    root.mainloop()
