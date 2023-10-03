import sys
from src.usermanagement_service import usermanager_app, user_management_logger, my_grpc_server

if __name__ == "__main__":
    try:
        my_grpc_server.start_base_server()
        user_management_logger.info("Bound USER-MANAGEMENT-SERVICE at IP-ADDRESS:PORT :: {0}:{1}".format(usermanager_app.config['USER_MANAGEMENT_SERVER_IPADDRESS'], usermanager_app.config['USER_MANAGEMENT_SERVER_PORT']))
        user_management_logger.info("Started the USER-MANAGEMENT server ...")
        user_management_logger.info("Application is ready to server traffic.")
        usermanager_app.run(host=usermanager_app.config["USER_MANAGEMENT_SERVER_IPADDRESS"], port=usermanager_app.config["USER_MANAGEMENT_SERVER_PORT"])

    except Exception as ex:
        user_management_logger.error("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
        print("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
