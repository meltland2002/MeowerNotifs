import websocket
import json
from notifypy import Notify
import threading
import time

def on_message(ws, message):
    # print(message)
    j = json.loads(message)
    if j["val"]=="I:112 | Trusted Access enabled":
        ws.send(json.dumps({"cmd": "direct", "val": "meower"}))
        print("Connected to Meower!")
        return 0
    try:
        ismsg = True if j["val"]["post_origin"]=="home" else False
    except:
        ismsg = False
    if not ismsg:
        return 0
    notif = Notify()
    isdiscord = True if j["val"]["u"]=="Discord" else False
    if isdiscord:
        notif.title = j["val"]["p"].split(": ")[0]
        notif.message = j["val"]["p"].split(": ")[1]
    else:
        notif.title = j["val"]["u"]
        notif.message = j["val"]["p"]
    notif.icon = "meower.png"
    notif.send()
    
def on_close(ws, close_status_code, close_msg):
   notif = Notify()
   notif.title = "Uh-oh"
   notif.message = "We've lost connection to Meower."
   notif.icon = "meower.png"
   notif.send()
   print("Lost connection!")
   
def ping(ws):
    print("Pinger active!")
    time.sleep(7.5)
    ws.send(json.dumps({"cmd": "ping", "val": ""}))
    
if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://server.meower.org/", on_message=on_message, on_close=on_close)
    pinger = threading.Thread(target=ping, args=(ws,), daemon=True)
    pinger.start()
    ws.run_forever()
