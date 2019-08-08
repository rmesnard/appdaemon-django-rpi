import datetime
import appdaemon.plugins.mqtt.mqttapi as mqtt

class HAMqtt(mqtt.Mqtt):
    def initialize(self):
        self.set_namespace('mqtt')
