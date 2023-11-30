import websocket
import json
from notifypy import Notify

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
    
if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://server.meower.org/", on_message=on_message, on_close=on_close)
    ws.run_forever()
