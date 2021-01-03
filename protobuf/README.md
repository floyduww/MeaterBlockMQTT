meater_block.proto is compiled with:
```
protoc -I=. --python_out=. meater_block.proto
```
It generates ***meater_block_pb2.py***

I must say reverse engineering these is a real blast (aka Pain in the Ass).

Main documentation used for how to use Google Protocol Buffers was: https://developers.google.com/protocol-buffers/docs/pythontutorial
