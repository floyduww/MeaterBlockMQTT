#!/usr/bin/python3
from socket import *
import select
import paho.mqtt.client as mqtt
import math
from string import Template
import time
import ast
from configparser import ConfigParser
import sys,os

import protobuf.meater_block_v2_pb2

sys.path.append(os.getcwd())

UDP_IP = "255.255.255.255"


# This is to build the device broadcast string. 
thisDevice = protobuf.meater_block_v2_pb2.MeaterLink()
thisDevice.device.part1 = 21578
thisDevice.device.part2 = 12
thisDevice.device.device_type = 3
thisDevice.device.inc = 1
thisDevice.device.device_mac = 42

config = ConfigParser()

MQTT_HOSTNAME = os.getenv('MQTT_HOSTNAME')
MQTT_PORT = os.getenv('MQTT_PORT')
MQTT_USEAUTH = os.getenv('MQTT_USEAUTH')
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_TIMEOUT = os.getenv('MQTT_TIMEOUT')
MQTT_ZERO_OUT = os.getenv('MQTT_ZERO_OUT')

BLOCK_TIMEOUT = os.getenv('BLOCK_TIMEOUT')
BLOCK_UDP_PORT = os.getenv('BLOCK__UDP_PORT')
SCALE = os.getenv('SCALE')
MEAT_TABLE_FILE = os.getenv('MEAT_TABLE_FILE')

config.read('config.ini')
if (not MQTT_HOSTNAME):
    MQTT_HOSTNAME = config.get('mqtt', 'MQTT_HOSTNAME', fallback="")
if (not MQTT_PORT):
    MQTT_PORT = config.getint('mqtt', 'MQTT_PORT',fallback=1883)
if (not MQTT_TIMEOUT):
    MQTT_TIMEOUT = config.getint('mqtt', 'MQTT_TIMEOUT',fallback=60)
if (not MQTT_USEAUTH):    
    MQTT_USEAUTH = config.getboolean('mqtt', 'MQTT_USEAUTH', fallback=False)
if (not MQTT_USERNAME):    
    MQTT_USERNAME = config.get('mqtt', 'MQTT_USERNAME', fallback="")
if (not MQTT_PASSWORD):    
    MQTT_PASSWORD = config.get('mqtt', 'MQTT_PASSWORD', fallback="")
if (not MQTT_ZERO_OUT):    
    MQTT_ZERO_OUT = config.getboolean('mqtt', 'MQTT_ZERO_OUT', fallback=False)

if (not BLOCK_TIMEOUT):
    BLOCK_TIMEOUT = config.getint('block', 'BLOCK_TIMEOUT',fallback=60)
if (not BLOCK_UDP_PORT):    
    BLOCK_UDP_PORT = config.getint('block', 'BLOCK_UDP_PORT',fallback=7878)
if (not SCALE):
    SCALE = config.get('block', 'SCALE', fallback='F')
if (not MEAT_TABLE_FILE):
    MEAT_TABLE_FILE = config.get('block', 'MEAT_TABLE_FILE', fallback="meat_table.txt")

def probe_data(probe,battery):
    probeArr = {}

    print(battery.battery)

    probeArr["batt"] =  int(battery.battery)
  #  probeArr["sig"] = probe.ble_signal
   

    if  hasattr(probe.part3,'cook_stage') :
        
        cook_stage = probe.part3.cook_stage
    else :
        cook_stage = 0
    
    probeArr["cooking"] = "0" + str(cook_stage)
    probeArr["m_temp"] = math.floor(toScale(probe.current_temps.m_temp_raw))  
    probeArr["a_temp"] = math.floor(toScale(probe.current_temps.a_temp_raw))
    probeArr["est_time_rem"] = timeRemInMin(probe.current_temps.est_time_rem_raw)
    probeArr["targ_temp"] = 0
    probeArr["cook_name"] = ""
    probeArr["meat_type"] = ""

    if(cook_stage != 0):
        probeArr["targ_temp"] = math.floor(toScale(probe.part3.targ_temp_raw))
        probeArr["meat_type"] = probe.part3.meat_type_int
        
        if (len(probe.part3.cook_name) > 0):
            probeArr["cook_name"] = probe.part3.cook_name
        else:
            if probeArr["meat_type"] in dictionary.keys():
                probeArr["cook_name"] = dictionary[probeArr["meat_type"]]
            else:
                probeArr["cook_name"] = probeArr["meat_type"]                

    return probeArr
    

def toCelsius(value):
    return (float(value))/64.0


def toFahrenheit(value):
    return ((toCelsius(value)*9)/5)+32.0


def toScale(value):
    global SCALE

    if SCALE == 'F':
        return toFahrenheit(value)
    else:
        return toCelsius(value)


def timeRemInMin(value):
    
    timeRem = math.ceil(value / (2*60))
    return timeRem


def on_publish(client, userdata, mid):
    return True


def on_disconnect(mqttc, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.\nError Code: " + str(rc) + "\nReconnecting...")
        mqttc.reconnect()
    else:
        print("Disconnected successfully")

def on_connect(mqttc, userdata, rc, something):
    print("Connected to " + MQTT_HOSTNAME + " successfully")        


def sendBlockOn():
    mqttc.publish(topicBlockStatus, "on", qos=0, retain=True)

    return 1


def sendBlockOff(blockStatus):
    if blockStatus:
        mqttc.publish(topicBlockStatus, "off", qos=0, retain=True)

        if(MQTT_ZERO_OUT):
            id = 1
            mqttc.publish(topicMeat.substitute(id=id), "0", qos=0, retain=True)
            mqttc.publish(topicAmbient.substitute(id=id), "0", qos=0, retain=True)
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

    meater_link = protobuf.meater_block_v2_pb2.MeaterLink()
    print(packet[0].hex())
    meater_link.ParseFromString(packet[0])
    print("---meater_link---")
    print(meater_link)
    print(meater_link.SerializeToString().hex())
 
    if (meater_link.HasField('linkData')):
        print("I have data")
      
    else:
        return False   # THIS IS FOR TESTING
        # this is for the handshake when using a meater or meater+
        # some_int needs a more descriptive variable name
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

    versions = [] 
    versions = meater_link.linkData.part3.versions

    batteries = []
    batteries = meater_link.linkData.part3.batteryInfo

    mqttc.publish(topicBlockPower, str(block_power), qos=0, retain=True)


    

    probe_num = int(versions[1].split('_')[1]) 
    pos = 1

    for probe in meater_link.linkData.part3.probe:
         
       #  if (probe.connected):
         probes[probe_num] = probe_data(probe, batteries[pos])
         probe_num = probe_num + 1
         pos = pos + 1

    for id in probes:
        probe = probes[id]

        print("publish")
        print(probe)
        mqttc.publish(topicCook.substitute(id=id), probe["cooking"], qos=0, retain=True)
        mqttc.publish(topicBattery.substitute(id=id), probe["batt"], qos=0, retain=True)
        mqttc.publish(topicCookName.substitute(id=id), probe["cook_name"], qos=0, retain=True)
        mqttc.publish(topicMeatType.substitute(id=id), probe["meat_type"], qos=0, retain=True)
        mqttc.publish(topicTargetTemp.substitute(id=id), probe["targ_temp"], qos=0, retain=True)
        mqttc.publish(topicMeat.substitute(id=id), probe["m_temp"], qos=0, retain=True)
        mqttc.publish(topicAmbient.substitute(id=id), probe["a_temp"], qos=0, retain=True)
        mqttc.publish(topicTimeRem.substitute(id=id), probe["est_time_rem"], qos=0, retain=True)


# mqtt setup and connect
mqttc = mqtt.Client()
mqttc.on_publish = on_publish
mqttc.on_disconnect = on_disconnect
mqttc.on_connect = on_connect
if (MQTT_USEAUTH):
    mqttc.username_pw_set(username=MQTT_USERNAME,password=MQTT_PASSWORD)
mqttc.connect(MQTT_HOSTNAME, MQTT_PORT, 300)

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
topicTimeRem =  Template("meater/probe/$id/estTimeRem")
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
