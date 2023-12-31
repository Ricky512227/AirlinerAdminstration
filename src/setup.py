from setuptools import setup

setup(
    name="PyPortalAdminstration",
    version="v1",
    packages=[
        "proto_def",
        "proto_def.token_proto_v1",
        "pyportal_common",
        "pyportal_common.db_handlers",
        "pyportal_common.app_handlers",
        "pyportal_common.util_handlers",
        "pyportal_common.error_handlers",
        "pyportal_common.logging_handlers",
        "pyportal_common.grpc_service_handlers",
        "pyportal_common.grpc_service_handlers.grpc_client_handler",
        "pyportal_common.grpc_service_handlers.grpc_server_handler",
        "pyportal_common.kafka_service_handlers",
        "pyportal_common.kafka_service_handlers.consumer_handlers",
        "pyportal_common.kafka_service_handlers.producer_handlers",
        "usermanagement_service",
        "usermanagement_service.users",
        "usermanagement_service.users.request_handlers",
        "usermanagement_service.users.response_handlers",
        "usermanagement_service.utils",
        "usermanagement_service.views",
        "usermanagement_service.models",
        "usermanagement_service.user_management_grpc",
        "tokenmanagement_service",
        "tokenmanagement_service.grpc",
        "tokenmanagement_service.utils",
        "tokenmanagement_service.views",
        "tokenmanagement_service.models",
        "tokenmanagement_service.tokens",
    ],
    package_dir={"": "src"},
    url="https://github.com/Ricky512227/AirlinerAdminstration/tree/main",
    license="kamal",
    author="kamalsaidevarapalli",
    author_email="kamalsaidevarapalli@gmail.com",
    description="self exploration",
)
