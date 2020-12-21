#!/usr/bin/python3
import socket
import select
import paho.mqtt.client as mqtt
import math
from string import Template
import time
import ast
from configparser import ConfigParser

config = ConfigParser()

config.read('config.ini')
MQTT_HOSTNAME = config.get('mqtt', 'MQTT_HOSTNAME')
MQTT_PORT = config.getint('mqtt', 'MQTT_PORT')
MQTT_TIMEOUT = config.getint('mqtt', 'MQTT_TIMEOUT')
BLOCK_TIMEOUT = config.getint('block', 'BLOCK_TIMEOUT')
BLOCK_UDP_PORT = config.getint('block', 'BLOCK_UDP_PORT')


def probe_data(offset, data):
    probe = {}
    big_sep = bytes.fromhex("30013a")
    big_sep2 = bytes.fromhex("30003a") # occurs rarely and not sure why

    bc = int.from_bytes(data[offset:offset+1], "little")

    probe["offset"] = offset
    probe["end"] = offset + bc + 1
    probeData = data[offset + 1: probe["end"]]

    probe["bc"] = bc
    probe["data"] = probeData

    probe["batt"] = int.from_bytes(probeData[21:22], "little")

    first_data_chunk_end = probeData.find(big_sep)
    if (first_data_chunk_end < 0):
        first_data_chunk_end = probeData.find(big_sep2)

    probe["sig"] = probeData[23:first_data_chunk_end].hex()

    begin_cook_data = first_data_chunk_end + 3

    cook_data_bc = int.from_bytes(probeData[begin_cook_data:begin_cook_data + 1], "little")
    cook_data = probeData[begin_cook_data:begin_cook_data + cook_data_bc]

    probe["cooking"] = cook_data[4:5].hex()

    temp_data_start = begin_cook_data + cook_data_bc + 2
    temp_data_bc = int.from_bytes(probeData[temp_data_start:temp_data_start + 1], "little")
    temp_data = probeData[temp_data_start + 1:temp_data_start + 1 + temp_data_bc]

    probe["m_temp"] = math.floor(toFahrenheit(convertBytes(temp_data[1:3])))
    convertBytes(temp_data[1:3])

    probe["a_temp"] = math.floor(toFahrenheit(convertBytes(temp_data[4:6])))
    convertBytes(temp_data[4:6])

    version_start = temp_data_start + temp_data_bc + 2
    version_bc = int.from_bytes(probeData[version_start:version_start + 1], "little")
    version = probeData[version_start + 1:version_start + 1 + version_bc]
    probe["version"] = version.decode("UTF-8")

    probe["targ_temp"] = 0
    probe["cook_name"] = ""
    probe["meat_type"] = ""

    if(probe["cooking"] != "00"):
        probe["targ_temp"] = math.floor(toFahrenheit(convertBytes2(cook_data[6:8])))
        if(cook_data[10:11].hex() == "2a"):
            probe["meat_type"] = cook_data[9:10].hex()
            cook_name_pos = 11
        else:
            probe["meat_type"] = cook_data[9:11].hex()
            cook_name_pos = 12

        cook_name_bc = int.from_bytes(cook_data[cook_name_pos:cook_name_pos + 1], "little")

        if cook_name_bc:
            cook_name = cook_data[cook_name_pos + 1: cook_name_pos + 1 + cook_name_bc]
            probe["cook_name"] = cook_name.decode("UTF-8")
        else:
            if probe["meat_type"] in dictionary.keys():
                probe["cook_name"] = dictionary[probe["meat_type"]]

    return probe


# convert an excess 128 byte to int
def convertBytes(data):
    incrementor = int.from_bytes(data[0:1], "little") - 128
    count = int.from_bytes(data[1:2], "little")
    return ((count*128) + incrementor)


def convertBytes2(data):
    incrementor = int.from_bytes(data[0:1], "little") - 128
    count = int.from_bytes(data[1:2], "little")
    return (((count*128) + incrementor) * 2)


def toCelsius(value):
    return (float(value))/32.0


def toFahrenheit(value):
    return ((toCelsius(value)*9)/5)+32.0


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
    print("-----------------")
    print('len(packet)='+str(len(packet)))
    print('len(packet[0])='+str(len(packet[0])))
    print('len(packet[1])='+str(len(packet[1])))
    print(packet[1])

    theData = packet[0]
    print(theData)
    hex_string = "".join("%02x " % b for b in packet[0])
    print(hex_string)

    # less than 150 assumes phone app
    if (len(packet[0]) < 150):
        print("I think this is the phone app")
        return False

    probes = {}

    block_power = theData[42:43]
    powerStatusInt = int.from_bytes(block_power, "little")
    mqttc.publish(topicBlockPower, str(powerStatusInt), qos=0, retain=True)

    probe_1_start = 61
    probes[1] = probe_data(probe_1_start, theData)

    probe_2_start = probes[1]["end"] + 3
    probes[2] = probe_data(probe_2_start, theData)

    probe_3_start = probes[2]["end"] + 3
    probes[3] = probe_data(probe_3_start, theData)

    probe_4_start = probes[3]["end"] + 3
    probes[4] = probe_data(probe_4_start, theData)

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
s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_client.setblocking(0)
s_client.bind(('', BLOCK_UDP_PORT))

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
            blockStatus = sendBlockOn()
            lastReceive = time.time()

    for s in writable:
        print("write")

    for s in exceptional:
        print("exceptional")

    if time.time() - lastReceive > BLOCK_TIMEOUT:
        blockStatus = sendBlockOff(blockStatus)
