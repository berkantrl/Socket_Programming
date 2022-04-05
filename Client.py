from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

HOST = '127.0.0.1'
PORT = 44444
BUFFERSIZE = 1024
ADDR = (HOST,PORT)
client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

def message():
    while True:
        try:
            message = client.recv(BUFFERSIZE).decode("utf8")
            msg_list.insert(tkinter.END, message)
        except:
            break

def send():
    message = msg.get()
    msg.set("")
    client.send(bytes(message, "utf8"))
    if message == "exit":
        client.close()
        app.quit()

def exit():
    msg.set("exit")
    send()

app = tkinter.Tk()
app.title("CHAT APPLİCATTİON")


msg_area = tkinter.Frame(app)
msg = tkinter.StringVar()
msg.set("Input your message...")
scrollbar = tkinter.Scrollbar(msg_area)
msg_list = tkinter.Listbox(msg_area, height=20, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side= tkinter.RIGHT, fill=tkinter.BOTH)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_area.pack()

entry_area = tkinter.Entry(app, textvariable=msg)
entry_area.bind("<Return>",send)
entry_area.pack()

send_btn = tkinter.Button(app, text="Send", command = send)
send_btn.pack()

thread = Thread(target=message)
thread.start()

tkinter.mainloop()

