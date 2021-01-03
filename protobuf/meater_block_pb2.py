# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: meater_block.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='meater_block.proto',
  package='meater_link',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12meater_block.proto\x12\x0bmeater_link\"^\n\nMeaterLink\x12\'\n\x06\x64\x65vice\x18\x01 \x02(\x0b\x32\x17.meater_link.DeviceData\x12\'\n\x08linkData\x18\x03 \x01(\x0b\x32\x15.meater_link.LinkData\"[\n\nDeviceData\x12\r\n\x05part1\x18\x01 \x01(\x05\x12\r\n\x05part2\x18\x02 \x01(\x05\x12\x13\n\x0b\x64\x65vice_type\x18\x03 \x01(\x05\x12\x0b\n\x03inc\x18\x04 \x01(\x05\x12\r\n\x05part5\x18\x05 \x01(\x06\"L\n\x08LinkData\x12\r\n\x05part1\x18\x01 \x01(\x05\x12\r\n\x05part2\x18\x02 \x01(\x05\x12\"\n\x05part3\x18\x03 \x01(\x0b\x32\x13.meater_link.Probes\"V\n\tBlockInfo\x12\r\n\x05part1\x18\x01 \x01(\x06\x12\r\n\x05power\x18\x02 \x01(\r\x12\r\n\x05part3\x18\x03 \x01(\r\x12\r\n\x05part4\x18\x04 \x01(\r\x12\r\n\x05part5\x18\x05 \x01(\t\"V\n\x06Probes\x12!\n\x05probe\x18\x01 \x03(\x0b\x32\x12.meater_link.Probe\x12)\n\tblockInfo\x18\x03 \x01(\x0b\x32\x16.meater_link.BlockInfo\"\xdf\x01\n\x05Probe\x12\r\n\x05part1\x18\x01 \x01(\x06\x12\r\n\x05part2\x18\x02 \x01(\x06\x12\x14\n\x0cprobe_id_num\x18\x03 \x01(\x05\x12\x0f\n\x07\x62\x61ttery\x18\x04 \x01(\x05\x12\x12\n\nble_signal\x18\x05 \x01(\x05\x12\r\n\x05part6\x18\x06 \x01(\x05\x12(\n\tcook_data\x18\x07 \x01(\x0b\x32\x15.meater_link.CookData\x12\x30\n\rcurrent_temps\x18\x08 \x01(\x0b\x32\x19.meater_link.CurrentTemps\x12\x12\n\nsw_version\x18\t \x01(\t\"\xc4\x01\n\x08\x43ookData\x12\x0f\n\x07num_adj\x18\x01 \x01(\x05\x12\x12\n\ncook_stage\x18\x02 \x01(\x05\x12\x15\n\rtarg_temp_raw\x18\x03 \x01(\x05\x12\x15\n\rmeat_type_int\x18\x04 \x01(\x05\x12\x11\n\tcook_name\x18\x05 \x01(\t\x12\x43\n\x16\x62lock2sub1sub1sub1sub1\x18\x06 \x01(\x0b\x32#.meater_link.Block2Sub1Sub1Sub1Sub1\x12\r\n\x05part7\x18\x07 \x01(\x06\"p\n\x0c\x43urrentTemps\x12\x12\n\nm_temp_raw\x18\x01 \x01(\x05\x12\x12\n\na_temp_raw\x18\x02 \x01(\x05\x12\x13\n\x0bpk_temp_raw\x18\x03 \x01(\x05\x12\r\n\x05part4\x18\x04 \x01(\x05\x12\x14\n\x0c\x63ook_counter\x18\x05 \x01(\x05\"E\n\x16\x42lock2Sub1Sub1Sub1Sub1\x12\r\n\x05part1\x18\x01 \x01(\x05\x12\r\n\x05part2\x18\x02 \x01(\x05\x12\r\n\x05part3\x18\x03 \x01(\x05'
)




_MEATERLINK = _descriptor.Descriptor(
  name='MeaterLink',
  full_name='meater_link.MeaterLink',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='meater_link.MeaterLink.device', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='linkData', full_name='meater_link.MeaterLink.linkData', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=129,
)


_DEVICEDATA = _descriptor.Descriptor(
  name='DeviceData',
  full_name='meater_link.DeviceData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='part1', full_name='meater_link.DeviceData.part1', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part2', full_name='meater_link.DeviceData.part2', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device_type', full_name='meater_link.DeviceData.device_type', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='inc', full_name='meater_link.DeviceData.inc', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part5', full_name='meater_link.DeviceData.part5', index=4,
      number=5, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=222,
)


_LINKDATA = _descriptor.Descriptor(
  name='LinkData',
  full_name='meater_link.LinkData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='part1', full_name='meater_link.LinkData.part1', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part2', full_name='meater_link.LinkData.part2', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part3', full_name='meater_link.LinkData.part3', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=224,
  serialized_end=300,
)


_BLOCKINFO = _descriptor.Descriptor(
  name='BlockInfo',
  full_name='meater_link.BlockInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='part1', full_name='meater_link.BlockInfo.part1', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='power', full_name='meater_link.BlockInfo.power', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part3', full_name='meater_link.BlockInfo.part3', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part4', full_name='meater_link.BlockInfo.part4', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part5', full_name='meater_link.BlockInfo.part5', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=302,
  serialized_end=388,
)


_PROBES = _descriptor.Descriptor(
  name='Probes',
  full_name='meater_link.Probes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='probe', full_name='meater_link.Probes.probe', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blockInfo', full_name='meater_link.Probes.blockInfo', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=390,
  serialized_end=476,
)


_PROBE = _descriptor.Descriptor(
  name='Probe',
  full_name='meater_link.Probe',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='part1', full_name='meater_link.Probe.part1', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part2', full_name='meater_link.Probe.part2', index=1,
      number=2, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='probe_id_num', full_name='meater_link.Probe.probe_id_num', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='battery', full_name='meater_link.Probe.battery', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ble_signal', full_name='meater_link.Probe.ble_signal', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part6', full_name='meater_link.Probe.part6', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cook_data', full_name='meater_link.Probe.cook_data', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='current_temps', full_name='meater_link.Probe.current_temps', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sw_version', full_name='meater_link.Probe.sw_version', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=479,
  serialized_end=702,
)


_COOKDATA = _descriptor.Descriptor(
  name='CookData',
  full_name='meater_link.CookData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_adj', full_name='meater_link.CookData.num_adj', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cook_stage', full_name='meater_link.CookData.cook_stage', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='targ_temp_raw', full_name='meater_link.CookData.targ_temp_raw', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='meat_type_int', full_name='meater_link.CookData.meat_type_int', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cook_name', full_name='meater_link.CookData.cook_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='block2sub1sub1sub1sub1', full_name='meater_link.CookData.block2sub1sub1sub1sub1', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part7', full_name='meater_link.CookData.part7', index=6,
      number=7, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=705,
  serialized_end=901,
)


_CURRENTTEMPS = _descriptor.Descriptor(
  name='CurrentTemps',
  full_name='meater_link.CurrentTemps',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='m_temp_raw', full_name='meater_link.CurrentTemps.m_temp_raw', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='a_temp_raw', full_name='meater_link.CurrentTemps.a_temp_raw', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pk_temp_raw', full_name='meater_link.CurrentTemps.pk_temp_raw', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part4', full_name='meater_link.CurrentTemps.part4', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cook_counter', full_name='meater_link.CurrentTemps.cook_counter', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=903,
  serialized_end=1015,
)


_BLOCK2SUB1SUB1SUB1SUB1 = _descriptor.Descriptor(
  name='Block2Sub1Sub1Sub1Sub1',
  full_name='meater_link.Block2Sub1Sub1Sub1Sub1',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='part1', full_name='meater_link.Block2Sub1Sub1Sub1Sub1.part1', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part2', full_name='meater_link.Block2Sub1Sub1Sub1Sub1.part2', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part3', full_name='meater_link.Block2Sub1Sub1Sub1Sub1.part3', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1017,
  serialized_end=1086,
)

_MEATERLINK.fields_by_name['device'].message_type = _DEVICEDATA
_MEATERLINK.fields_by_name['linkData'].message_type = _LINKDATA
_LINKDATA.fields_by_name['part3'].message_type = _PROBES
_PROBES.fields_by_name['probe'].message_type = _PROBE
_PROBES.fields_by_name['blockInfo'].message_type = _BLOCKINFO
_PROBE.fields_by_name['cook_data'].message_type = _COOKDATA
_PROBE.fields_by_name['current_temps'].message_type = _CURRENTTEMPS
_COOKDATA.fields_by_name['block2sub1sub1sub1sub1'].message_type = _BLOCK2SUB1SUB1SUB1SUB1
DESCRIPTOR.message_types_by_name['MeaterLink'] = _MEATERLINK
DESCRIPTOR.message_types_by_name['DeviceData'] = _DEVICEDATA
DESCRIPTOR.message_types_by_name['LinkData'] = _LINKDATA
DESCRIPTOR.message_types_by_name['BlockInfo'] = _BLOCKINFO
DESCRIPTOR.message_types_by_name['Probes'] = _PROBES
DESCRIPTOR.message_types_by_name['Probe'] = _PROBE
DESCRIPTOR.message_types_by_name['CookData'] = _COOKDATA
DESCRIPTOR.message_types_by_name['CurrentTemps'] = _CURRENTTEMPS
DESCRIPTOR.message_types_by_name['Block2Sub1Sub1Sub1Sub1'] = _BLOCK2SUB1SUB1SUB1SUB1
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MeaterLink = _reflection.GeneratedProtocolMessageType('MeaterLink', (_message.Message,), {
  'DESCRIPTOR' : _MEATERLINK,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.MeaterLink)
  })
_sym_db.RegisterMessage(MeaterLink)

DeviceData = _reflection.GeneratedProtocolMessageType('DeviceData', (_message.Message,), {
  'DESCRIPTOR' : _DEVICEDATA,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.DeviceData)
  })
_sym_db.RegisterMessage(DeviceData)

LinkData = _reflection.GeneratedProtocolMessageType('LinkData', (_message.Message,), {
  'DESCRIPTOR' : _LINKDATA,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.LinkData)
  })
_sym_db.RegisterMessage(LinkData)

BlockInfo = _reflection.GeneratedProtocolMessageType('BlockInfo', (_message.Message,), {
  'DESCRIPTOR' : _BLOCKINFO,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.BlockInfo)
  })
_sym_db.RegisterMessage(BlockInfo)

Probes = _reflection.GeneratedProtocolMessageType('Probes', (_message.Message,), {
  'DESCRIPTOR' : _PROBES,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.Probes)
  })
_sym_db.RegisterMessage(Probes)

Probe = _reflection.GeneratedProtocolMessageType('Probe', (_message.Message,), {
  'DESCRIPTOR' : _PROBE,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.Probe)
  })
_sym_db.RegisterMessage(Probe)

CookData = _reflection.GeneratedProtocolMessageType('CookData', (_message.Message,), {
  'DESCRIPTOR' : _COOKDATA,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.CookData)
  })
_sym_db.RegisterMessage(CookData)

CurrentTemps = _reflection.GeneratedProtocolMessageType('CurrentTemps', (_message.Message,), {
  'DESCRIPTOR' : _CURRENTTEMPS,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.CurrentTemps)
  })
_sym_db.RegisterMessage(CurrentTemps)

Block2Sub1Sub1Sub1Sub1 = _reflection.GeneratedProtocolMessageType('Block2Sub1Sub1Sub1Sub1', (_message.Message,), {
  'DESCRIPTOR' : _BLOCK2SUB1SUB1SUB1SUB1,
  '__module__' : 'meater_block_pb2'
  # @@protoc_insertion_point(class_scope:meater_link.Block2Sub1Sub1Sub1Sub1)
  })
_sym_db.RegisterMessage(Block2Sub1Sub1Sub1Sub1)


# @@protoc_insertion_point(module_scope)
