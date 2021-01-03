#!/usr/bin/python3
from socket import *
import select
import paho.mqtt.client as mqtt
import math
from string import Template
import time
import ast
from configparser import ConfigParser

import protobuf.meater_block_pb2

UDP_IP = "255.255.255.255"

# This is build the device broadcast string.  Needs to be customized with mac, dev type, sw version etc.
MAC_HEX = "bfbaa9282d75990f"
DEV_TYPE = "Py Meater V0.01"  # (14 bytes available w/o doing calculations)
DEV_TYPE_HEX = "5079204d65617465722056302e3031"
SW_VERSION_HEX = "322e35"
MESSAGE = "0a1308caa801100c1801200129" + MAC_HEX + "12460a28d01734191dc7f8d26b55c48be005b30c199f436383e2b5331aa0f176215aa44200e31aaeb62525671002220f" + DEV_TYPE_HEX + "2a03" + SW_VERSION_HEX + "32023131"

#mat# MESSAGE = "0a1308caa801100c18012001299a6d69faf160f829122d0a102cefe737917820ee7f7ddccba116115e1002220e476f6f676c6520506978656c20352a03322e3532023131"
msg_as_byte = bytearray.fromhex(MESSAGE) 

config = ConfigParser()

config.read('config.ini')
MQTT_HOSTNAME = config.get('mqtt', 'MQTT_HOSTNAME')
MQTT_PORT = config.getint('mqtt', 'MQTT_PORT')
MQTT_TIMEOUT = config.getint('mqtt', 'MQTT_TIMEOUT')
BLOCK_TIMEOUT = config.getint('block', 'BLOCK_TIMEOUT')
BLOCK_UDP_PORT = config.getint('block', 'BLOCK_UDP_PORT')
SCALE = "F"


def probe_data(probe):
    probeArr = {}

    probeArr["batt"] = probe.battery

    probeArr["sig"] = probe.ble_signal


    probeArr["cooking"] = "0" + str(probe.cook_data.cook_stage)

    probeArr["m_temp"] = math.floor(toScale(probe.current_temps.m_temp_raw))  

    probeArr["a_temp"] = math.floor(toScale(probe.current_temps.a_temp_raw))

    probeArr["version"] = probe.sw_version
    probeArr["targ_temp"] = 0
    probeArr["cook_name"] = ""
    probeArr["meat_type"] = ""

    if(probe.cook_data.cook_stage != 0):
        probeArr["targ_temp"] = math.floor(toScale(probe.cook_data.targ_temp_raw * 2))
        probeArr["meat_type"] = probe.cook_data.meat_type_int
        
        if (len(probe.cook_data.cook_name) > 0):
            probeArr["cook_name"] = probe.cook_data.cook_name
        else:
            if probeArr["meat_type"] in dictionary.keys():
                probeArr["cook_name"] = dictionary[probeArr["meat_type"]]
            else:
                probeArr["cook_name"] = probeArr["meat_type"]                

    return probeArr

def toCelsius(value):
    return (float(value))/32.0


def toFahrenheit(value):
    return ((toCelsius(value)*9)/5)+32.0


def toScale(value):
    global SCALE

    if SCALE == 'F':
        return toFahrenheit(value)
    else:
        return toCelsius(value)


def on_publish(client, userdata, mid):
    return True


def on_disconnect(mqttc, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        mqttc.reconnect()
    else:
        print("Disconnected successfully")


def sendBlockOn():
    mqttc.publish(topicBlockStatus, "on", qos=0, retain=True)

    return 1


def sendBlockOff(blockStatus):
    if blockStatus:
        mqttc.publish(topicBlockStatus, "off", qos=0, retain=True)
        print("blockOff")

    return 0


def processPacket(packet):
    global blockStatus
    global lastReceive

    print("-----------------")
    print('len(packet)='+str(len(packet)))
    print('len(packet[0])='+str(len(packet[0])))
    print('len(packet[1])='+str(len(packet[1])))
    print(packet[1])

    block2 = protobuf.meater_block_pb2.MeaterLink()
    block2.ParseFromString(packet[0])
    print("---block2---")
    print(block2)
    print(packet[0].hex())
    print(block2.SerializeToString().hex())

    # check byte 9.  (01 for phone, 02 for block)
    # check if byte 21 is '1a', I think this means 'I have data'
    if (block2.linkData):
        print("I have data")
    else:
        print("Move along")
        return False

    blockStatus = sendBlockOn()
    lastReceive = time.time()

    probes = {}

    block_power = block2.linkData.part3.blockInfo.power
    mqttc.publish(topicBlockPower, str(block_power), qos=0, retain=True)

    probe_num = 0
    for probe in block2.linkData.part3.probe:
         probe_num = probe_num + 1
         probes[probe_num] = probe_data(probe)

    for id in probes:
        probe = probes[id]
        print(probe)
        mqttc.publish(topicCook.substitute(id=id), probe["cooking"], qos=0, retain=True)
        mqttc.publish(topicBattery.substitute(id=id), probe["batt"], qos=0, retain=True)
        mqttc.publish(topicCookName.substitute(id=id), probe["cook_name"], qos=0, retain=True)
        mqttc.publish(topicMeatType.substitute(id=id), probe["meat_type"], qos=0, retain=True)
        mqttc.publish(topicTargetTemp.substitute(id=id), probe["targ_temp"], qos=0, retain=True)
        mqttc.publish(topicMeat.substitute(id=id), probe["m_temp"], qos=0, retain=True)
        mqttc.publish(topicAmbient.substitute(id=id), probe["a_temp"], qos=0, retain=True)


# mqtt setup and connect
mqttc = mqtt.Client()
mqttc.on_publish = on_publish
mqttc.on_disconnect = on_disconnect
mqttc.connect(MQTT_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)

# udp socket to listen to
s_client = socket(AF_INET, SOCK_DGRAM)
s_client.setblocking(0)
s_client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) 
s_client.bind(('', BLOCK_UDP_PORT))

# send initial broadcast
s_client.sendto(msg_as_byte, (UDP_IP,BLOCK_UDP_PORT))

# mqtt topics
topicCook = Template("meater/probe/$id/cook")
topicBattery = Template("meater/probe/$id/battery")
topicMeatType = Template("meater/probe/$id/meatType")
topicTargetTemp = Template("meater/probe/$id/targetTemp")
topicMeat = Template("meater/probe/$id/meat")
topicAmbient = Template("meater/probe/$id/ambient")
topicCookName = Template("meater/probe/$id/cookName")
topicBlockStatus = "meater/block/status"
topicBlockPower = "meater/block/power"

mqttc.loop_start()

inputs = [s_client]
outputs = []
socket_timeout = 1

lastReceive = time.time()
lastSend = time.time()
blockStatus = 1


file = open("meat_table.txt", "r")

contents = file.read()
dictionary = ast.literal_eval(contents)

file.close()

while(1):
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs, socket_timeout)
    for s in readable:
        if s is s_client:
            data = s.recvfrom(1024)
            processPacket(data)


    for s in writable:
        print("write")

    for s in exceptional:
        print("exceptional")

    if time.time() - lastSend > 15:
        s_client.sendto(msg_as_byte, (UDP_IP,BLOCK_UDP_PORT))
        lastSend = time.time()

    if time.time() - lastReceive > BLOCK_TIMEOUT:
        blockStatus = sendBlockOff(blockStatus)
