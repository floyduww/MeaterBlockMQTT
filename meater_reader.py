#!/usr/bin/python3
import socket
import binascii
import re
import paho.mqtt.client as mqtt
import math
from string import Template

temp_regex = r"08 ([a-f0-9]{2} ){2}10 [a-f0-9]{2} [a-f0-9]{2} 18"
parts_split = r"1a [a-f0-9]{2} 0a"


# convert an excess 128 hex byte to int
def convertHex(hex):
    incrementor = int(hex[0:2], 16) - 128
    count = int(hex[3:5], 16)
    return ((count*128) + incrementor)


def convertHex2(hex):
    incrementor = int(hex[0:2], 16) - 128
    count = int(hex[3:5], 16)
    return (((count*128) + incrementor) * 2)


def toCelsius(value):
    return (float(value))/32.0


def toFahrenheit(value):
    return ((toCelsius(value)*9)/5)+32.0


def on_publish(client, userdata, mid):
    return True


# mqtt setup and connect
mqttc = mqtt.Client()
mqttc.on_publish = on_publish
mqttc.connect("MQTT.HOSTNAME", 1883, 60)

# udp socket to listen to
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 7878))

# mqtt topics
topicCook = Template("meater/probe/$id/cook")
topicBattery = Template("meater/probe/$id/battery")
topicMeatType = Template("meater/probe/$id/meatType")
topicTargetTemp = Template("meater/probe/$id/targetTemp")
topicMeat = Template("meater/probe/$id/meat")
topicAmbient = Template("meater/probe/$id/ambient")
topicCookName = Template("meater/probe/$id/cookName")

while(1):
    m = s.recvfrom(4096)
    print("-----------------")
    print('len(m)='+str(len(m)))
    print('len(m[0])='+str(len(m[0])))
    print('len(m[1])='+str(len(m[1])))
    print(m[1])

    hex_string = "".join("%02x " % b for b in m[0])

    # break apart to block(0) and probes(1-4)
    parts = re.split(parts_split, hex_string)

    for part in parts:

        if part[-27:][0:2] == "08":  # this is a probe
            version = part[-24:]
            v_b = bytes.fromhex(version)
            id = v_b.decode("ASCII")[-1]

            print("Probe : {id} ({version})".format(id=id, version=v_b.decode("ASCII")[0:-2]))
            print("\t" + part)
            cooking = part[97:99]  # byte 33
            battery = int(part[67:69])  # byte 23

            print("\tCook : " + cooking)
            mqttc.publish(topicCook.substitute(id=id), cooking, qos=0, retain=True)

            print("\tBatt : {level}".format(level=battery))
            mqttc.publish(topicBattery.substitute(id=id), battery, qos=0, retain=True)

            if cooking != "00":
                targetTempHex = part[103:108]  # bytes 35-36
                targetTemp = math.floor(toFahrenheit(convertHex2(targetTempHex)))
                meatTypeHex = part[112:114]  # bytes 38 or 38/39

                cookNamePos = 0
                if part[115:117] == "2a":
                    cookNameLenthHex = part[118:120]
                    cookNamePos = 40
                elif part[118:120] == "2a":
                    cookNameLenthHex = part[121:123]
                    cookNamePos = 41
                    meatTypeHex = part[112:117]  # bytes 38 or 38/39

                cookNameLenthInt = int(cookNameLenthHex, 16)
                if cookNameLenthInt > 0:
                    print("\tCookLen : " + str(cookNameLenthInt))

                    cookNameStart = cookNamePos*3
                    cookNameEnd = cookNamePos*3 + cookNameLenthInt*3
                    cookNameHex = part[cookNameStart:cookNameEnd]
                    cookNameBytes = bytes.fromhex(cookNameHex)
                    cookName = cookNameBytes.decode("ASCII")
                else:
                    cookName = meatTypeHex

                print("\tName : " + cookName)
                mqttc.publish(topicCookName.substitute(id=id), cookName, qos=0, retain=True)

                print("\tType : " + meatTypeHex)
                mqttc.publish(topicMeatType.substitute(id=id), meatTypeHex, qos=0, retain=True)

                print("\tTarg : " + str(targetTemp))
                mqttc.publish(topicTargetTemp.substitute(id=id), str(targetTemp), qos=0, retain=True)


            else:
                mqttc.publish(topicCookName.substitute(id=id), '', qos=0, retain=True)
                mqttc.publish(topicMeatType.substitute(id=id), '00', qos=0, retain=True)
                mqttc.publish(topicTargetTemp.substitute(id=id), 0, qos=0, retain=True)

            matches = re.finditer(temp_regex, part, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                meatF = toFahrenheit(convertHex(match.group()[3:8]))
                ambF = toFahrenheit(convertHex(match.group()[12:17]))

                print("\tmeat : {temp} {hex} {tempF}F".format(temp=convertHex(match.group()[3:8]), hex=match.group()[3:8], tempF=meatF))
                mqttc.publish(topicMeat.substitute(id=id), math.floor(meatF), qos=0, retain=True)

                print("\tamb  : {temp} {hex} {tempF}F".format(temp=convertHex(match.group()[12:17]), hex=match.group()[12:17], tempF=ambF))
                mqttc.publish(topicAmbient.substitute(id=id), math.floor(ambF), qos=0, retain=True)

        elif part[-30:][0:2] == "09":   # this is the block
            version = part[-27:]
            v_b = bytes.fromhex(version)
            print("Block SW Version : " + v_b.decode("ASCII"))
            print("\t" + part)
