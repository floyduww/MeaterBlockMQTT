# MeaterBlock to mqtt
I wanted to get the block info into Home Assistant.  Easiest way to to take the udp packet and resend over mqtt.

This project works but is still in it's infancy, so your milage may vary. 


## Usage
requires python3-protobuf, python3-paho-mqtt, protobuf-compiler

copy config_default.ini to config.ini  
in config.ini change <MQTT_HOSTNAME> to the IP or FQDN of your MQTT server  
build the protobuf library file(must be done each time you update from github):  
```
protoc -I=protobuf --python_out=protobuf meater_block.proto
```
run the program with (requires python3):
```
python meater_reader_buf.py
```
Note: meater_reader_v2.py and meater_link.py have been depricated.

### Sources

https://tvwbb.com/threads/meater-wire-free-probe-intergration.71564/

https://www.scadacore.com/tools/programming-calculators/online-hex-converter/

https://github.com/nathanfaber/meaterble

https://community.home-assistant.io/t/meater-thermometer/130501/40


### udp packet Breakdown
Important bytes with the first 3 removed for probes compared to what [lkspencer](https://tvwbb.com/members/lkspencer.41726/) found.  This has to do with how I split the udp packet.
These positions are approximate.  I found after initial inspection that that 

Below are ramblings on my decoding of the UDP packet.

Then the temperature parts are found using mathing the regex by [lkspencer](https://tvwbb.com/members/lkspencer.41726/)

Below each line represents the output from 1 probe at a point in time.  Multiple lines are to compare between different outputs within the same stage

Not Cooking
```
bc                                                                                  bc -- -- -- -- -- -- -|    bc -- -- -- -- -- -- -- -- -- -- -- -|    bc -- -- -- -- -- -- -- -|
     probe mac address -- -|     block mac address -- -|    p#    bat   sig   ?  -|       adj   on    temp           m tmp    a tmp    pt    ?     ct       probe version  -| _  p#
3b 09 1a a0 f1 76 21 5a a4 42 11 d0 17 34 19 1d c7 f8 d2 18 02 20 06 28 53 30 01 3a 07 08 00 10 00 18 90 07 42 0c 08 a6 05 10 a6 05 18 00 20 01 28 00 4a 08 76 31 2e 30 2e 35 5f 32
39 09 6b 55 c4 8b e0 05 b3 0c 11 d0 17 34 19 1d c7 f8 d2 18 03 20 08 28 39 30 01 3a 07 08 00 10 00 18 90 07 42 0a 08 74    10 74    18 00 20 01 28 00 4a 08 76 31 2e 30 2e 35 5f 33 
   sp                         sp                         sp    sp    sp    sp          sp    sp    sp       sp    sp       
```

Cooking  
```
                                                                                       bc -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                               -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -|       
bc (rest of packet)                                                                                                        bc -- -- -- -- -- -- -- -- -|                                                                                     bc -- -- -- -- -- -- -- -- -- -- -- -- -- -|    bc -- -- -- -- -- -- -- -|
      probe mac address -- -|    block mac address -- -|    p#    bat   sig      ?  -|       adj   on    temp     mt             Cook Name-- -- -- -- -- -|                         ?- -- -- -- -- -- -- -- -|    session number?-- -- -|          m tmp    a tmp    pt -|    ?     ct -|       probe version  -| _  p#
5c 09 00 e3 1a ae b6 25 25 67 11 d0 17 34 19 1d c7 f8 d2 18 04 20 07 28 37    30 01 3a 26 08 04 10 01 18 f3 08 20 0f    2a 09 62 72 69 73 6b 65 74 20 31                            32 07 08 05 10 01 18 d8 04 39 9d dd 85 55 60 3d d3 60 42 0e 08 b0 05 10 b0 05 18 b0 05 20 01 28 b0 0d 4a 08 76 31 2e 30 2e 35 5f 34
52 09 1a a0 f1 76 21 5a a4 42 11 d0 17 34 19 1d c7 f8 d2 18 02 20 06 28 4f    30 01 3a 1d 08 01 10 01 18 95 07 20 11    2a 00                                                       32 07 08 05 10 01 18 d8 04 39 ab 78 ee 71 9a 2f aa 60 42 0d 08 b6 05 10 b6 05 18 b8 05 20 01 28 19    4a 08 76 31 2e 30 2e 35 5f 32
53 09 1a a0 f1 76 21 5a a4 42 11 d0 17 34 19 1d c7 f8 d2 18 02 20 06 28 51    30 01 3a 1d 08 01 10 01 18 95 07 20 11    2a 00                                                       32 07 08 05 10 01 18 d8 04 39 ab 78 ee 71 9a 2f aa 60 42 0e 08 b6 05 10 b6 05 18 b8 05 20 01 28 87 0e 4a 08 76 31 2e 30 2e 35 5f 32
59 09 1a a0 f1 76 21 5a a4 42 11 d0 17 34 19 1d c7 f8 d2 18 02 20 06 28 4f    30 01 3a 23 08 02 10 01 18 95 07 20 11    2a 06 63 75 73 74 6f 6d                                     32 07 08 05 10 01 18 d8 04 39 ab 78 ee 71 9a 2f aa 60 42 0e 08 b6 05 10 b6 05 18 b8 05 20 01 28 db 0e 4a 08 76 31 2e 30 2e 35 5f 32
52 09 00 e3 1a ae b6 25 25 67 11 d0 17 34 19 1d c7 f8 d2 18 04 20 07 28 39    30 01 3a 1d 08 01 10 01 18 a1 06 20 57    2a 00                                                       32 07 08 05 10 01 18 d8 04 39 32 97 43 b0 08 b3 6b 60 42 0d 08 c4 05 10 c4 05 18 c4 05 20 01 28 21    4a 08 76 31 2e 30 2e 35 5f 34
66 09 19 9f 43 63 83 e2 b5 33 11 d0 17 34 19 1d c7 f8 d2 18 01 20 08 28 95 01 30 01 3a 2f 08 02 10 02 18 f1 0b 20 26    2a 12 70 6f 72 6b 20 73 68 6f 75 6c 64 65 72 20 6c 65 66 74 32 07 08 05 10 01 18 d8 04 39 e4 f8 cd 0d 17 54 1f 60 42 0e 08 98 01 10 b4 13 18 98 01 20 01 28 a7 08 4a 08 76 31 2e 30 2e 35 5f 31 
64 09 1a a0 f1 76 21 5a a4 42 11 d0 17 34 19 1d c7 f8 d2 18 02 20 08 28 99 01 30 01 3a 2d 08 02 10 02 18 f1 0b 20 96 01 2a 0f 70 6f 72 6b 20 42 75 74 74 20 72 69 67 68 74          32 07 08 05 10 01 18 d8 04 39 10 64 83 18 1f 84 00 60 42 0e 08 8e 01 10 f6 12 18 8e 01 20 01 28 a0 03 4a 08 76 31 2e 30 2e 35 5f 32
   sp                         sp                         sp    sp    sp       sp          sp    sp    sp       sp       sp                                                          sp    sp    sp    sp       sp                         sp    sp       sp       sp       sp    sp       sp
   09                         11                         18    20    28       30                                                                                                                                                          42                                              4a
                                                                                          08    10    18       20       2a                                                          32                         39                               08       10       18       20    28 
                                                                                                                                                                                          08    10    18                
```

probe warmer than ambient? This looks like finished w/o 2a Cook Name bc
```
bc (rest of packet)                                                                 bc -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -|           bc -- -- -- -- -- -- -- -- -- -- -- -- -|      bc -- -- -- -- -- -- -- -|
      probe mac address -- -|    block mac address -- -|    p#    bat   sig   ?  -|       adj   on    temp     session number?-- -- -|                 m tmp    a tmp    pt -|     ?    ct         probe version  -| _  p#
45 09 19 9f 43 63 83 e2 b5 33 11 d0 17 34 19 1d c7 f8 d2 18 01 20 07 28 79 30 01 3a 10 08 04 10 00 18 90 07 39 a9 c3 c3 df 7c 21 ed 60        42 0d 08 d0 08 10 e8 08 18 ff 0f 20 01 28 00   4a 08 76 31 2e 30 2e 35 5f 31
45 09 19 9f 43 63 83 e2 b5 33 11 d0 17 34 19 1d c7 f8 d2 18 01 20 06 28 73 30 01 3a 10 08 04 10 00 18 90 07 39 a9 c3 c3 df 7c 21 ed 60        42 0d 08 fc 05 10 88 06 18 ff 0f 20 01 28 00   4a 08 76 31 2e 30 2e 35 5f 31

   sp                         sp                         sp    sp    sp    sp          sp    sp    sp       sp                                sp    sp       sp    sp          sp    sp      sp   
```

Finished cooking 
```
bc (rest of packet)                                                                    bc -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -|    bc -- -- -- -- -- -- -- -- -- -- -- -- -- -|       bc -- -- -- -- -- -- -- -|
                                                                                                                  bc
      probe mac address -- -|    block mac address -- -|    p#    bat   sig   |bigSep|       adj   on    temp           session number?-- -- -|          m tmp    a tmp    pt -|    ?     ct          probe version  -| _  p#
48 09 00 e3 1a ae b6 25 25 67 11 d0 17 34 19 1d c7 f8 d2 18 04 20 07 28 39    30 01 3a 12 08 05 10 00 18 f3 08 2a 00 39 9d dd 85 55 60 3d d3 60 42 0e 08 b6 05 10 b6 05 18 ff 0f 20 01 28 bc 18    4a 08 76 31 2e 30 2e 35 5f 34
47 09 19 9f 43 63 83 e2 b5 33 11 d0 17 34 19 1d c7 f8 d2 18 01 20 07 28 a5 01 30 01 3a 0f 08 1c 10 00 18 00          39 e4 f8 cd 0d 17 54 1f 60 42 0f 08 b0 05 10 b0 05 18 ff 0f 20 01 28 e7 e4 02 4a 08 76 31 2e 30 2e 35 5f 31 
44 09 1a a0 f1 76 21 5a a4 42 11 d0 17 34 19 1d c7 f8 d2 18 02 20 06 28 37    30 00 3a 0f 08 20 10 00 18 00          39 10 64 83 18 1f 84 00 60 42 0d 08 b8 05 10 b8 05 18 ff 0f 20 01 28 00       4a 08 76 31 2e 30 2e 35 5f 32 
   sp                         sp                         sp    sp    sp       sp    sp    sp    sp    sp       sp    sp                         sp    sp       sp       sp       sp                sp  
```

`30 01 3a` is a big seperator
`30 00 3a` is a big seperator

`bc` - byte count  
`sp` - seperator

`probe mac` - (8 bytes)  
`block mac` - (8 bytes)  
`p#` - (1 byte) probe number  
`bat` - (1 byte) battery  (range 1-9)
`sig` - (1 or 2 byte) bluetooth signal  
`adj` - (1 byte) number of adjustments that have been made to the cook (not 100% sure but that's what it appears to be related to)  
`on` - (1 byte) this is the hex value indicating if the probe has an active cook going or not where 00 is no cook and anything else means it has a cook (I've seen 01, 02(cookint, 04(resting?, 05, 06)  
`temp` - (2 bytes) target temperature  
`mt` - (1 or 2 bytes) meat type  
`m tmp` - (1 or 2 bytes) meat temperature  
`a tmp` - (1 or 2 bytes) ambient temperature  
`pt` - (2 bytes) peak probe temperature (I think)   
`ct` - (var bytes) cook time - how long the cook has been going for. NOTE: this is also a little endian excess-128 value like the probe temperatures.  
`Cook name` - (var bytes) custom cook name that overides meat name on display  
`session number` - (8 bytes) unique session id for the cook  
`probe version` - (var bytes) version of the probe SW with the probe number at the end

Cook broken up with major seperators as first byte  
64 (byte count)   
`09` 1a a0 f1 76 21 5a a4 42  
`11` d0 17 34 19 1d c7 f8 d2  
`18` 02 20 08 28 99 01  
`30` 01 3a 2d 08 02 10 02 18 f1 0b 20 96 01 2a 0f 70 6f 72 6b 20 42 75 74 74 20 72 69 67 68 74  
`32` 07 08 05 10 01 18 d8 04  
`39` 10 64 83 18 1f 84 00 60  
`42` 0e 08 8e 01 10 f6 12 18 8e 01 20 01 28 a0 03  
`4a` 08 76 31 2e 30 2e 35 5f 32 

###### Cooking Stages  
01 - unknown  
02 - cooking  
03 - remove from heat  
04 - resting  
05 - unknown  
06 - ready

#### mqtt topics  
meater/probe/{id}/meatType  
meater/probe/{id}/targetTemp  
meater/probe/{id}/cook  
meater/probe/{id}/cookName  
meater/probe/{id}/battery  
meater/probe/{id}/meat  
meater/probe/{id}/ambient  
meater/block/status  
meater/block/power  

#### Block info packet
```
                                                                  bc1                                                                           bc -- -- -- -- -- -- -- -- -|
                           dev   inc   |- id                   -1 --                               block mac address -- -|    Pwr                  sw version- -- -- -- -- -| 
0a 13 08 ca a8 01 10 0c 18 02 20 64 29 d0 17 34 19 1d c7 f8 d2 1a db 02 08 00 10 03 1a 1c 1a 1a 09 d0 17 34 19 1d c7 f8 d2 10 64 18 02 20 01 2a 09 76 2e 32 2e 30 2e 33 2e 39                                                                                                   
0a 13 08 ca a8 01 10 0c 18 02 20 0f 29 d0 17 34 19 1d c7 f8 d2 1a 9e 02 08 00 10 03 1a 1c 1a 1a 09 d0 17 34 19 1d c7 f8 d2 10 66 18 02 20 01 2a 09 76 2e 32 2e 30 2e 33 2e 39
                  sp    sp    sp    sp                                                                                     sp                sp
```
`bc1` - 
`bc` - byte count  
`sp` - seperator

`dev` - device meaterblock(02), phone (01) ?
`inc` - goes up every push, just rolls over  
`bc1` - byte count of probe data  
`pwr` - 66 on USB, <= 64 on batt  


#### Phone app
```
                                                                  bc rest of packet
                           dev   inc   |-                   -|    bc    bc |-                      |- probe id          -| |- probe id          -| |- probe id          -| |- probe id          -|          bc |- Phone type                             -|    bc |-ver -|    bc |? ?|          
0a 13 08 ca a8 01 10 0c 18 01 20 05 29 af ba a9 28 2d 75 99 0f 12 46 0a 28 d0 17 34 19 1d c7 f8 d2 6b 55 c4 8b e0 05 b3 0c 19 9f 43 63 83 e2 b5 33 1a a0 f1 76 21 5a a4 42 00 e3 1a ae b6 25 25 67 10 02 22 0f 47 6f 6f 67 6c 65 20 50 69 78 65 6c 20 33 61 2a 03 32 2e 35 32 02 31 31 
0a 13 08 ca a8 01 10 0c 18 01 20 01 29 9a 6d 69 fa f1 60 f8 29 12 2d 0a 10 2c ef e7 37 91 78 20 ee 7f 7d dc cb a1 16 11 5e                                                                         10 02 22 0e 47 6f 6f 67 6c 65 20 50 69 78 65 6c 20 35    2a 03 32 2e 35 32 02 31 31 
0a 13 08 ca a8 01 10 0c 18 01 20 04 29 af ba a9 28 2d 75 99 0f 12 3e 0a 20 d0 17 34 19 1d c7 f8 d2 6b 55 c4 8b e0 05 b3 0c 1a a0 f1 76 21 5a a4 42 00 e3 1a ae b6 25 25 67                         10 02 22 0f 47 6f 6f 67 6c 65 20 50 69 78 65 6c 20 33 61 2a 03 32 2e 35 32 02 31 31 
0a 13 08 ca a8 01 10 0c 18 01 20 0b 29 af ba a9 28 2d 75 99 0f 12 3e 0a 20 d0 17 34 19 1d c7 f8 d2 6b 55 c4 8b e0 05 b3 0c 1a a0 f1 76 21 5a a4 42 00 e3 1a ae b6 25 25 67                         10 02 22 0f 47 6f 6f 67 6c 65 20 50 69 78 65 6c 20 33 61 2a 03 32 2e 35 32 02 31 31 
0a 13 08 ca a8 01 10 0c 18 01 20 5a 29 af ba a9 28 2d 75 99 0f 12 3e 0a 20 d0 17 34 19 1d c7 f8 d2 6b 55 c4 8b e0 05 b3 0c 1a a0 f1 76 21 5a a4 42 00 e3 1a ae b6 25 25 67                         10 02 22 0f 47 6f 6f 67 6c 65 20 50 69 78 65 6c 20 33 61 2a 03 32 2e 35 32 02 31 31 
                  sp    sp    sp    sp                         sp    sp                                                                                                                            sp    sp                                                 sp             sp  
```
`bc` - byte count  
`sp` - seperator

`dev` - meaterblock (02), phone (01) ?
`inc` - goes up every push, just rolls over  
`ver` - Phone app version #  
`??`  - not sure if this is an id like probe id or a verion sub number  
`probe mac` - bluetooth id of the probe
`app id` - bluetooth id of the phone

```
                                                                  bc rest of packet
                           dev   inc   |- phone mac         -|    bc    bc |- app id ?          -| |- probe mac         -|          bc |- Phone type                          -|    bc |-ver -|    bc |? ?|          
0a 13 08 ca a8 01 10 0c 18 01 20 01 29 9a 6d 69 fa f1 60 f8 29 12 2d 0a 10 2c ef e7 37 91 78 20 ee 7f 7d dc cb a1 16 11 5e 10 02 22 0e 47 6f 6f 67 6c 65 20 50 69 78 65 6c 20 35 2a 03 32 2e 35 32 02 31 31 
0a 13 08 ca a8 01 10 0c 18 01 20 01 29 9a 6d 69 fa f1 60 f8 29 12 2d 0a 10 2c ef e7 37 91 78 20 ee 7f 7d dc cb a1 16 11 5e 10 02 22 0e 47 6f 6f 67 6c 65 20 50 69 78 65 6c 20 35 2a 03 32 2e 35 32 02 31 31
0a 13 08 ca a8 01 10 0c 18 01 20 01 29 e5 d7 48 7a 62 b8 13 3f 12 2f 0a 10 2c ef e7 37 91 78 20 ee 7f 7d dc cb a1 16 11 5e 10 02 22 0e 47 6f 6f 67 6c 65 20 50 69 78 65 6c 20 33 2a 05 32 2e 34 2e 31 32 02 31 31 
```
`bc` - byte count  
`sp` - seperator

`dev` - meaterblock (02), phone (01) ?
`inc` - goes up every push, just rolls over  
`ver` - Phone app version #  
`??`  - not sure if this is an id like probe id or a verion sub number  
`probe mac` - bluetooth id of the probe
`app id` - bluetooth id of the phone

### Handshake

This is what I know so far.

Seems the phone app (v2.5) when using Meater or Meater+ will broadcast it's presence on UDP 7878. In this broadcast it sends what it's 'mac' is and the probe macs that it knows about.

When this app sees that broadcast it will put those macs into a request broadcast.  It will then broadcast out asking if anyone can send it that data.

The phone app then starts directly sending the probe data to this app.

This app must also repeat the broadcast request at least about every 30 seconds as a keep alive to keep the phone app sending data too it
