
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import serial
from serial.tools import list_ports


class DiscountTimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Timer Discount Challenge")
        self.root.geometry("760x650")

        self.ser = None
        self.connected = False

        title = tk.Label(
            root,
            text="SMART TIMER DISCOUNT CHALLENGE",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=15)

        # UART connection
        connection_frame = ttk.LabelFrame(root, text="UART Connection")
        connection_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(connection_frame, text="COM Port:").grid(
            row=0, column=0, padx=5, pady=10
        )

        self.port_var = tk.StringVar()
        self.port_box = ttk.Combobox(
            connection_frame,
            textvariable=self.port_var,
            width=12,
            state="readonly"
        )
        self.port_box.grid(row=0, column=1, padx=5)

        ttk.Button(
            connection_frame,
            text="Refresh",
            command=self.refresh_ports
        ).grid(row=0, column=2, padx=5)

        ttk.Label(connection_frame, text="Baud Rate:").grid(
            row=0, column=3, padx=5
        )

        self.baud_var = tk.StringVar(value="115200")
        self.baud_box = ttk.Combobox(
            connection_frame,
            textvariable=self.baud_var,
            values=["9600", "57600", "115200", "209700"],
            width=10
        )
        self.baud_box.grid(row=0, column=4, padx=5)

        self.connect_button = ttk.Button(
            connection_frame,
            text="Connect",
            command=self.toggle_connection
        )
        self.connect_button.grid(row=0, column=5, padx=5)

        # Result display
        result_frame = ttk.LabelFrame(root, text="Challenge Result")
        result_frame.pack(fill="x", padx=20, pady=10)

        self.time_label = tk.Label(
            result_frame,
            text="Time: ---.--- s",
            font=("Arial", 18)
        )
        self.time_label.pack(pady=5)

        self.error_label = tk.Label(
            result_frame,
            text="Error: ---.--- s",
            font=("Arial", 18)
        )
        self.error_label.pack(pady=5)

        self.discount_label = tk.Label(
            result_frame,
            text="Discount: ---",
            font=("Arial", 26, "bold"),
            fg="blue"
        )
        self.discount_label.pack(pady=10)

        # UART receive window
        log_frame = ttk.LabelFrame(root, text="UART Receive")
        log_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.log = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=("Consolas", 11)
        )
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

        # UART send
        send_frame = ttk.Frame(root)
        send_frame.pack(fill="x", padx=20, pady=10)

        self.send_entry = ttk.Entry(send_frame)
        self.send_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.send_entry.bind(
            "<Return>", lambda event: self.send_data()
        )

        ttk.Button(
            send_frame,
            text="Send",
            command=self.send_data
        ).pack(side="left", padx=5)

        ttk.Button(
            send_frame,
            text="Clear",
            command=self.clear_log
        ).pack(side="left", padx=5)

        ttk.Button(
            send_frame,
            text="Demo Test",
            command=self.demo_test
        ).pack(side="left", padx=5)

        self.refresh_ports()
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def refresh_ports(self):
        ports = [p.device for p in list_ports.comports()]
        self.port_box["values"] = ports

        if ports:
            self.port_var.set(ports[0])
        else:
            self.port_var.set("")

    def toggle_connection(self):
        if self.connected:
            self.disconnect()
        else:
            try:
                if not self.port_var.get():
                    messagebox.showwarning(
                        "Warning", "Please select a COM port."
                    )
                    return

                self.ser = serial.Serial(
                    self.port_var.get(),
                    int(self.baud_var.get()),
                    timeout=0.2
                )

                self.connected = True
                self.connect_button.config(text="Disconnect")
                self.append_log("Connected to " + self.port_var.get())

                threading.Thread(
                    target=self.read_serial,
                    daemon=True
                ).start()

            except Exception as e:
                messagebox.showerror("Connection Error", str(e))

    def disconnect(self):
        self.connected = False

        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass

        self.ser = None
        self.connect_button.config(text="Connect")
        self.append_log("Disconnected")

    def read_serial(self):
        while self.connected:
            try:
                if self.ser and self.ser.is_open:
                    data = self.ser.readline().decode(
                        "utf-8", errors="replace"
                    )

                    if data:
                        self.root.after(
                            0, self.process_data, data
                        )

            except Exception:
                self.root.after(0, self.disconnect)
                break

    def process_data(self, data):
        self.append_log(data.rstrip("\r\n"))

        for line in data.splitlines():
            line = line.strip()

            if line.startswith("Time:"):
                self.time_label.config(text=line)

            elif line.startswith("Error:"):
                self.error_label.config(text=line)

            elif line.startswith("Discount:"):
                value = line.split(":", 1)[1].strip()

                if value == "5":
                    text = "5 OFF (50% OFF)"
                    color = "green"
                elif value == "7":
                    text = "7 OFF (30% OFF)"
                    color = "orange"
                else:
                    text = "10 OFF (NO DISCOUNT)"
                    color = "red"

                self.discount_label.config(
                    text=text, fg=color
                )

    def append_log(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def send_data(self):
        if not self.connected or not self.ser:
            messagebox.showwarning(
                "Warning", "UART is not connected."
            )
            return

        text = self.send_entry.get()

        try:
            self.ser.write((text + "\n").encode("utf-8"))
            self.append_log("TX: " + text)
            self.send_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Send Error", str(e))

    def clear_log(self):
        self.log.delete("1.0", tk.END)

    def demo_test(self):
        self.process_data(
            "\r\nTime: 10.032 s\r\n"
            "Error: 0.032 s\r\n"
            "Discount: 5\r\n"
        )

    def close_window(self):
        self.disconnect()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DiscountTimerGUI(root)
    root.mainloop()
