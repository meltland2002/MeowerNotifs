import websocket
import json
from notifypy import Notify
import threading
import time
import configurizer as c

config = c.load_config("meowernotif.cfg", """# A list of users to ignore, separate using semicolons (;)
ignoreList=None
# Seconds until the pinger sends another ping
pingTime=7.5
# Determines whether username should be in notification content or not
slimmed=False""", ["ignoreList"])
print("Configuration loaded: " + str(config))

def on_message(ws, message):
    # print(message)
    j = json.loads(message)
    if j["val"]=="I:112 | Trusted Access enabled":
        ws.send(json.dumps({"cmd": "direct", "val": "meower"}))
        print("Connected to Meower!")
        return 0
    try:
        ismsg = True if j["val"]["post_origin"]=="livechat" else False
    except:
        ismsg = False
    if not ismsg:
        return 0
    notif = Notify()
    isdiscord = True if j["val"]["u"]=="Discord" else False
    username = j["val"]["u"] if not isdiscord else j["val"]["p"].split(": ")[0]
    if config["ignoreList"]!=None and username in config["ignoreList"]:
        return 0
    content = j["val"]["p"] if not isdiscord else j["val"]["p"].split(": ")[1]
    notif.title = username if config["slimmed"] == False else "Meower"
    notif.message = content if config["slimmed"] == False else username + ": " + content
    notif.icon = "meower.png"
    notif.send()
    
def on_close(ws, close_status_code, close_msg):
   notif = Notify()
   notif.title = "Uh-oh." if config["slimmed"] == False else "Meower"
   notif.message = "We've lost connection to Meower." if config["slimmed"] == False else "The connection has been lost."
   notif.icon = "meower.png"
   notif.send()
   print("Lost connection...")
   
def ping(ws):
    print("Pinger active!")
    time.sleep(config["pingTime"])
    ws.send(json.dumps({"cmd": "ping", "val": ""}))
    
if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://server.meower.org/", on_message=on_message, on_close=on_close)
    pinger = threading.Thread(target=ping, args=(ws,), daemon=True)
    pinger.start()
    ws.run_forever()
