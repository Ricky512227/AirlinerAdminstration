import sys
import grpc
from src.airliner_grpc import token_pb2_grpc
from src.airliner_grpc import token_pb2

def TokenGrpcRequestPreparation(userid, username, passcode):
    tokoen_req_message = token_pb2.TokenReqMessage()
    tokoen_req_message.userid = "1"
    tokoen_req_message.username = "kamal"
    tokoen_req_message.passcode = "Ishi#06041995"
    print("Request Created  :: {0}".format(tokoen_req_message))
    return tokoen_req_message


def init_grpc_token_client(serverIp, serverport):
    grpc_client_status = False
    tokenstub = None
    try:
        tokenchannel = grpc.insecure_channel(serverIp + ":" + serverport)
        tokenstub = token_pb2_grpc.UserValidationForTokenGenerationStub(tokenchannel)
        print("Created Stub and assigned to the channel :: {0}".format(tokenstub))
        grpc_client_status = True
    except Exception as ex:
        print("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
    finally:
        return tokenstub, grpc_client_status


def trigger_request(tokenstub, data_to_send):
    resp_status = False
    resp_data = None
    try:
        resp_data = tokenstub.ValidateUserCredentials(data_to_send)
        print("Received Response from grpc :: {0}".format(resp_data))
        resp_status= True
    except grpc.RpcError as ex:
        print("Error occurred :: {0}\tLine No:: {1}".format(ex.debug_error_string(), sys.exc_info()[2].tb_lineno))
    except Exception as ex:
        print("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
    finally:
        return resp_data, resp_status




