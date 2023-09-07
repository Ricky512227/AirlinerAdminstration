import sys
from src.airliner_grpc import token_pb2_grpc
from src.airliner_grpc import token_pb2
from google.protobuf.json_format import MessageToJson
from src.registration_service.controllers.registration_controller import check_user_credentials
from src.registration_service import registration_app_logger



class UserValidationForTokenGenerationService(token_pb2_grpc.UserValidationForTokenGenerationServicer):
    def ValidateUserCredentials(self, request, context):
        token_res_message = None
        try:
            registration_app_logger.info("Received request from client ::\n{0}".format(request))
            metadata = dict(context.invocation_metadata())
            registration_app_logger.info("Metadata :: {0}".format(metadata))
            token_res_message = token_pb2.TokenResMessage()
            data = check_user_credentials(request.userid)
            registration_app_logger.info("Received response after trigger rpc :: {0}".format(data))
            token_res_message.userid = str(data[0])
            token_res_message.isvalid = True
            json_str = MessageToJson(token_res_message)
            json_str_oneline = json_str.replace("\n", " ")
            registration_app_logger.info(f"Sending response back to gRPC client :: {json_str_oneline}")
        except Exception as ex:
            registration_app_logger.error("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
            print("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
        return token_res_message

