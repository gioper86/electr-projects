from pynput import keyboard
import paho.mqtt.client as mqtt #import the client1
broker_address="192.168.1.95"

client = mqtt.Client("macGio")
client.connect(broker_address)

keys = {
    "w": False,
    "s": False,
    "d": False,
    "a": False,
}

def on_press(key):
    try:
        if key.char in keys and not keys[key.char]:
            keys[key.char] = True
            publish_message(key.char, "pressed")
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    try:
        print('{0} released'.format(key))
        if key.char in keys:
            keys[key.char] = False
        if key == keyboard.Key.esc:
            # Stop listener
            return False
    except AttributeError:
        print('special key {0} pressed'.format(key))            

def publish_message(key, action):
    actions = {
        ("w", "pressed"): "top",
        ("s", "pressed"): "bottom",
        ("d", "pressed"): "right",
        ("a", "pressed"): "left",
    }

    if (key, action) in actions:
        client.publish("servoCamera", actions[(key,action)])

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
