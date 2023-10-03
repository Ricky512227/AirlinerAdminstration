# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: token.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0btoken.proto\"I\n\x13TokenRequestMessage\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x10\n\x08passcode\x18\x03 \x01(\t\"7\n\x14TokenResponseMessage\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x0f\n\x07isvalid\x18\x02 \x01(\x08\x32s\n\'UserValidationForTokenGenerationService\x12H\n\x17ValidateUserCredentials\x12\x14.TokenRequestMessage\x1a\x15.TokenResponseMessage\"\x00\x62\x06proto3')



_TOKENREQUESTMESSAGE = DESCRIPTOR.message_types_by_name['TokenRequestMessage']
_TOKENRESPONSEMESSAGE = DESCRIPTOR.message_types_by_name['TokenResponseMessage']
TokenRequestMessage = _reflection.GeneratedProtocolMessageType('TokenRequestMessage', (_message.Message,), {
  'DESCRIPTOR' : _TOKENREQUESTMESSAGE,
  '__module__' : 'token_pb2'
  # @@protoc_insertion_point(class_scope:TokenRequestMessage)
  })
_sym_db.RegisterMessage(TokenRequestMessage)

TokenResponseMessage = _reflection.GeneratedProtocolMessageType('TokenResponseMessage', (_message.Message,), {
  'DESCRIPTOR' : _TOKENRESPONSEMESSAGE,
  '__module__' : 'token_pb2'
  # @@protoc_insertion_point(class_scope:TokenResponseMessage)
  })
_sym_db.RegisterMessage(TokenResponseMessage)

_USERVALIDATIONFORTOKENGENERATIONSERVICE = DESCRIPTOR.services_by_name['UserValidationForTokenGenerationService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TOKENREQUESTMESSAGE._serialized_start=15
  _TOKENREQUESTMESSAGE._serialized_end=88
  _TOKENRESPONSEMESSAGE._serialized_start=90
  _TOKENRESPONSEMESSAGE._serialized_end=145
  _USERVALIDATIONFORTOKENGENERATIONSERVICE._serialized_start=147
  _USERVALIDATIONFORTOKENGENERATIONSERVICE._serialized_end=262
# @@protoc_insertion_point(module_scope)
