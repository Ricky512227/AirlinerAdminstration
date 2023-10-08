# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import src.proto_def.token_proto_v1.token_pb2 as token__pb2


class UserValidationForTokenGenerationServiceStub(object):
    """buf:lint:ignore SERVICE_SUFFIX
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A user_management_grpc.Channel.
        """
        self.ValidateUserCredentials = channel.unary_unary(
                '/UserValidationForTokenGenerationService/ValidateUserCredentials',
                request_serializer=token__pb2.TokenRequestMessage.SerializeToString,
                response_deserializer=token__pb2.TokenResponseMessage.FromString,
                )


class UserValidationForTokenGenerationServiceServicer(object):
    """buf:lint:ignore SERVICE_SUFFIX
    """

    def ValidateUserCredentials(self, request, context):
        """buf:lint:ignore RPC_REQUEST_STANDARD_NAME
        buf:lint:ignore RPC_RESPONSE_STANDARD_NAME
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserValidationForTokenGenerationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ValidateUserCredentials': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateUserCredentials,
                    request_deserializer=token__pb2.TokenRequestMessage.FromString,
                    response_serializer=token__pb2.TokenResponseMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'UserValidationForTokenGenerationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserValidationForTokenGenerationService(object):
    """buf:lint:ignore SERVICE_SUFFIX
    """

    @staticmethod
    def ValidateUserCredentials(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserValidationForTokenGenerationService/ValidateUserCredentials',
            token__pb2.TokenRequestMessage.SerializeToString,
            token__pb2.TokenResponseMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
