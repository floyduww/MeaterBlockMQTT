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

import sys,os
sys.path.append(os.getcwd())

UDP_IP = "255.255.255.255"


# This is to build the device broadcast string. 
thisDevice = protobuf.meater_block_pb2.MeaterLink()
thisDevice.device.part1 = 21578
thisDevice.device.part2 = 12
thisDevice.device.device_type = 3
thisDevice.device.inc = 1
thisDevice.device.device_mac = 42

config = ConfigParser()

config.read('config.ini')
MQTT_HOSTNAME = config.get('mqtt', 'MQTT_HOSTNAME')
MQTT_PORT = config.getint('mqtt', 'MQTT_PORT',fallback=1883)
MQTT_TIMEOUT = config.getint('mqtt', 'MQTT_TIMEOUT',fallback=60)
MQTT_USEAUTH = config.getboolean('mqtt', 'MQTT_USEAUTH', fallback=False)
MQTT_USERNAME = config.get('mqtt', 'MQTT_USERNAME')
MQTT_PASSWORD = config.get('mqtt', 'MQTT_PASSWORD')

BLOCK_TIMEOUT = config.getint('block', 'BLOCK_TIMEOUT',fallback=60)
BLOCK_UDP_PORT = config.getint('block', 'BLOCK_UDP_PORT',fallback=7878)
SCALE = config.get('block', 'SCALE', fallback='F')
MEAT_TABLE_FILE = config.get('block', 'MEAT_TABLE_FILE', fallback="meat_table.txt")


def probe_data(probe):
    probeArr = {}

    probeArr["batt"] = probe.battery
    probeArr["sig"] = probe.ble_signal
    probeArr["cooking"] = "0" + str(probe.cook_data.cook_stage)
    probeArr["m_temp"] = math.floor(toScale(probe.current_temps.m_temp_raw))  
    probeArr["a_temp"] = math.floor(toScale(probe.current_temps.a_temp_raw))
    probeArr["version"] = probe.fw_version
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
        print("Meater Link Off")

    return 0


def processPacket(packet):
    global blockStatus
    global lastReceive

    global thisDevice

    print("-----------------")
    print('len(packet)='+str(len(packet)))
    print('len(packet[0])='+str(len(packet[0])))
    print('len(packet[1])='+str(len(packet[1])))
    print(packet[1])

    meater_link = protobuf.meater_block_pb2.MeaterLink()
    print(packet[0].hex())
    meater_link.ParseFromString(packet[0])
    print("---meater_link---")
    print(meater_link)
    print(meater_link.SerializeToString().hex())

    # check byte 9.  (01 for phone, 02 for block)
    # check if byte 21 is '1a', I think this means 'I have data'
    if (meater_link.HasField('linkData')):
        print("I have data")
    else:
        if (meater_link.HasField('queryData')):
            for some_int in  meater_link.queryData.some_int:
                if (some_int not in thisDevice.queryData.some_int ):
                    thisDevice.queryData.some_int.append(some_int)
        print("Move along")
        return False

    blockStatus = sendBlockOn()
    lastReceive = time.time()

    probes = {}

    block_power = meater_link.linkData.part3.blockInfo.power
    mqttc.publish(topicBlockPower, str(block_power), qos=0, retain=True)

    probe_num = 0
    for probe in meater_link.linkData.part3.probe:
         probe_num = probe_num + 1
         if (probe.connected):
            probes[probe_num] = probe_data(probe)

    for id in probes:
        probe = probes[id]
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
if (MQTT_USEAUTH):
    print ("USE AUTH")
    mqttc.username_pw_set(username=MQTT_USERNAME,password=MQTT_PASSWORD)
mqttc.connect(MQTT_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)

# udp socket to listen to
s_client = socket(AF_INET, SOCK_DGRAM)
s_client.setblocking(0)
s_client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) 
s_client.bind(('', BLOCK_UDP_PORT))

# send initial broadcast
msg_as_byte = bytearray.fromhex(thisDevice.SerializeToString().hex())
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


file = open(MEAT_TABLE_FILE, "r")

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

    if time.time() - lastSend > 5:
        msg_as_byte = bytearray.fromhex(thisDevice.SerializeToString().hex()) 
        s_client.sendto(msg_as_byte, (UDP_IP,BLOCK_UDP_PORT))
        lastSend = time.time()

    if time.time() - lastReceive > BLOCK_TIMEOUT:
        blockStatus = sendBlockOff(blockStatus)
