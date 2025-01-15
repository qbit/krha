#! /usr/bin/env python3
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import requests
import json
import os

DBusGMainLoop(set_as_default=True)

objpath = "/krha"

os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

iface = "org.kde.krunner1"

class Runner(dbus.service.Object):
    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName("org.kde.krha", dbus.SessionBus()), objpath)
        self.api_key = os.environ.get("HA_API_KEY", "")
        self.ha_url = os.environ.get("HA_URL", "").rstrip('/')

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        if not query.startswith("ha "):
            return []

        command = query[3:]
        if not command:
            return [("ha", "Home Assistant Commands", "home", 100, 1.0, 
                     {'subtext': 'Type a command after "ha" to control Home Assistant'})]

        return [(
            command,  # data
            f"Send to Home Assistant: {command}",  # text
            "home",  # icon
            100,  # type
            1.0,  # relevance
            {'subtext': 'Press Enter to send command'}  # properties
        )]
        
    @dbus.service.method(iface, out_signature='a(sss)')
    def Actions(self):
        return [("send", "Send to Home Assistant", "home")]

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, data: str, action_id: str):
        print(data, action_id)
        if not self.api_key or not self.ha_url:
            print("Error: HA_API_KEY or HA_URL not configured")
            return
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.ha_url}/api/conversation/process",
                headers=headers,
                json={"text": data}
            )
            response.raise_for_status()
            result = response.json()
            print(f"Response from Home Assistant: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"Error sending command to Home Assistant: {e}")



runner = Runner()
loop = GLib.MainLoop()
loop.run()
