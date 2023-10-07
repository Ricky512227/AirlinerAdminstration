import os
import sys
from dotenv import load_dotenv
from src.pyportal_common.logging_handlers.base_logger import LogMonitor
from src.pyportal_common.app_handlers.app_manager import AppHandler
from src.pyportal_common.db_handlers.db_manager import DataBaseHandler
from src.usermanagement_service.models.user_model import Base

try:
    # Set the registration service directory as the current dir
    currentDir = os.getcwd()
    print("Current Directory :: {0}".format(currentDir))
    # Enable/Disable the env file path according to the environment,Read Schema Files of headers/requests for all the diff operations.
    user_management_env_filepath = os.path.join(currentDir, ".env.dev")
    reg_user_req_schema_filepath = os.path.join(currentDir, "schemas/requests/register_user/req_schema.json")
    req_headers_schema_filepath = os.path.join(currentDir, "schemas/headers/reg_headers_schema.json")
    getuser_headers_schema_filepath = os.path.join(currentDir, "schemas/headers/getuser_headers_schema.json")
    del_user_headers_schema_filepath = os.path.join(currentDir, "schemas/headers/del_user_headers_schema.json")

    # user_management_env_filepath = os.path.join(currentDir, "src/usermanagement_service/.env.prod")
    # reg_user_req_schema_filepath = os.path.join(currentDir, "src/usermanagement_service/schemas/requests/register_user/req_schema.json")
    # req_headers_schema_filepath = os.path.join(currentDir, "src/usermanagement_service/schemas/headers/reg_headers_schema.json")
    # getuser_headers_schema_filepath = os.path.join(currentDir, "src/usermanagement_service/schemas/headers/getuser_headers_schema.json")
    # del_user_headers_schema_filepath = os.path.join(currentDir, "src/usermanagement_service/schemas/headers/del_user_headers_schema.json")

    print("Loading Env File path :: {0}".format(user_management_env_filepath))
    # Load the env file.
    loaded = load_dotenv(user_management_env_filepath)
    if loaded:
        print("Environment variables file loaded from :: {0} ".format(user_management_env_filepath))
        # Setting the env variable and binding to the application.
        FLASK_ENV = os.environ.get("FLASK_ENV")
        DEBUG = os.environ.get("DEBUG")
        JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
        FLASK_APP = os.environ.get("FLASK_APP")

        USER_MANAGEMENT_SERVER_IPADDRESS = os.environ.get("USER_MANAGEMENT_SERVER_IPADDRESS")
        USER_MANAGEMENT_SERVER_PORT = os.environ.get("USER_MANAGEMENT_SERVER_PORT")
        USER_MANAGEMENT_GRPC_SERVER_IP = os.environ.get("USER_MANAGEMENT_GRPC_SERVER_IP")
        USER_MANAGEMENT_GRPC_SERVER_PORT = os.environ.get("USER_MANAGEMENT_GRPC_SERVER_PORT")
        USER_MANAGEMENT_GRPC_MAX_WORKERS = int(os.environ.get("USER_MANAGEMENT_GRPC_MAX_WORKERS"))

        SERVICE_NAME = os.environ.get("SERVICE_NAME")
        DB_DRIVER_NAME = os.environ.get("DB_DRIVER_NAME")
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_IPADDRESS = os.environ.get("DB_IPADDRESS")
        DB_PORT = int(os.environ.get("DB_PORT"))
        DB_NAME = os.environ.get("DB_NAME")
        POOL_SIZE = int(os.environ.get("POOL_SIZE"))
        MAX_OVERFLOW = int(os.environ.get("MAX_OVERFLOW"))
        POOL_RECYCLE = int(os.environ.get("POOL_RECYCLE"))
        POOL_TIMEOUT = int(os.environ.get("POOL_TIMEOUT"))
        RETRY_INTERVAL = int(os.environ.get("RETRY_INTERVAL"))
        MAX_RETRIES = int(os.environ.get("MAX_RETRIES"))

        # Initialize the logger for the user_management service
        user_management_logger = LogMonitor("usermanagement").logger
        usermanager = AppHandler(logger_instance=user_management_logger)

        usermanager_app = usermanager.create_app_instance()
        usermanager_app.config["FLASK_ENV"] = FLASK_ENV
        usermanager_app.config["DEBUG"] = DEBUG
        usermanager_app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
        usermanager_app.config["FLASK_APP"] = FLASK_APP




        usermanager_app.config["USER_MANAGEMENT_SERVER_IPADDRESS"] = USER_MANAGEMENT_SERVER_IPADDRESS
        usermanager_app.config["USER_MANAGEMENT_SERVER_PORT"] = USER_MANAGEMENT_SERVER_PORT

        usermanager_app.config["USER_MANAGEMENT_GRPC_SERVER_IP"] = USER_MANAGEMENT_GRPC_SERVER_IP
        usermanager_app.config["USER_MANAGEMENT_GRPC_SERVER_PORT"] = USER_MANAGEMENT_GRPC_SERVER_PORT
        usermanager_app.config["USER_MANAGEMENT_GRPC_MAX_WORKERS"] = USER_MANAGEMENT_GRPC_MAX_WORKERS
        # Load and Validate Schema Files which are read.
        req_headers_schema_status, req_headers_schema = usermanager.read_json_schema(req_headers_schema_filepath)
        getuser_headers_schema_status, getuser_headers_schema = usermanager.read_json_schema(
            getuser_headers_schema_filepath)
        del_user_headers_schema_status, del_user_headers_schema = usermanager.read_json_schema(
            del_user_headers_schema_filepath)
        reg_user_req_schema_status, reg_user_req_schema = usermanager.read_json_schema(reg_user_req_schema_filepath)

        if usermanager_app is None:
            print("App creation failed")
            sys.exit()
        # Create the blueprint for the user_management service
        usermanager_bp = usermanager.create_blueprint_instance()
        # Create the jwt_manager for the user_management service
        usermanager_app_jwt = usermanager.bind_jwt_manger_to_app_instance(app_instance=usermanager_app)

        usermanager_db_obj = DataBaseHandler(logger_instance=user_management_logger, db_driver=DB_DRIVER_NAME,
                                             db_user=DB_USER, db_ip_address=DB_IPADDRESS, db_password=DB_PASSWORD,
                                             db_port=DB_PORT, db_name=DB_NAME, db_pool_size=POOL_SIZE,
                                             db_pool_max_overflow=MAX_OVERFLOW, db_pool_recycle=POOL_RECYCLE,
                                             db_pool_timeout=POOL_TIMEOUT, retry_interval=RETRY_INTERVAL,
                                             max_retries=MAX_RETRIES, base=Base)
        # Create a database engine
        user_management_db_engine, is_engine_created = usermanager_db_obj.create_db_engine_for_service(
            app_instance=usermanager_app)
        # If the engine doesn't create, then go for retry  of max_retries=3 with retry_delay=5.
        if is_engine_created:
            # If the engine is created then check the connection for the status of th db.
            if usermanager_db_obj.check_db_connectivity_and_retry(db_engine=user_management_db_engine):
                # If the connection  health is connected, then initialise the database for the particular service.
                if usermanager_db_obj.create_database_for_service():
                    # If the connection  health is connected, then create the tables for the services which was defined in the models.
                    if usermanager_db_obj.create_tables_associated_to_db_model(db_engine=user_management_db_engine):
                        # Bind the application with the sqlAlchemy.
                        user_management_SQLAlchemy = usermanager_db_obj.bind_db_app(app_instance=usermanager_app)
                        # Bind the application with the migrations
                        user_management_migrate = usermanager_db_obj.migrate_db_bind_app(app_instance=usermanager_app,
                                                                                         app_db=user_management_SQLAlchemy)
                        # Initialize/Create a pool of connections for the service
                        user_management_connection_pool = usermanager_db_obj.create_pool_of_connections(
                            db_engine=user_management_db_engine)

                        user_management_session_maker = usermanager_db_obj.create_session_maker_to_connectio_pool(
                            db_engine=user_management_db_engine, connection_pool=user_management_connection_pool)

                        # Display the  pool of connections for the service which was initialized
                        usermanager_db_obj.display_pool_info(connection_pool=user_management_connection_pool)
                        ''' 
                        To create and initialize the views, we need to 
                            - attach the routes to the created blueprint
                            - register the blueprint
                        '''
                        from src.usermanagement_service.views.create_user import register_user

                        # from src.usermanagement_service.views.fetch_user import get_user_info
                        # from src.usermanagement_service.views.remove_user import deregister_user
                        usermanager_bp.route('/api/v1/airliner/registerUser', methods=['POST'])(register_user)
                        # usermanager_bp.route('/api/v1/airliner/getUser/<int:userid>', methods=['GET'])(get_user_info)
                        # usermanager_bp.route('/api/v1/airliner/deleteUser/<int:userid>', methods=['DELETE'])(deregister_user)

                        usermanager.register_blueprint_for_service(app_instance=usermanager_app,
                                                                   blueprint_instance=usermanager_bp)
                        usermanager.display_registered_blueprints_for_service(app_instance=usermanager_app)

                        from src.pyportal_common.grpc_handlers.grpc_server_handler.grpc_base_server import \
                            PyPortalGrpcBaseServer
                        from src.proto_def.token_proto_v1.token_pb2_grpc import \
                            add_UserValidationForTokenGenerationServiceServicer_to_server
                        from src.usermanagement_service.user_management_grpc.user_grpc_server import UserValidationForTokenGenerationService

                        my_grpc_server = PyPortalGrpcBaseServer(logger_instance=user_management_logger, grpc_server_ip="127.0.0.1", grpc_server_port=50051, max_workers_for_service=4)
                        my_grpc_server.bind_ip_port_server()
                        if my_grpc_server is not None:
                            my_grpc_server.bind_rpc_method_server(
                                name_service_servicer_to_server=add_UserValidationForTokenGenerationServiceServicer_to_server,
                                name_service=UserValidationForTokenGenerationService
                            )




                        # Create/Initialise the user_management_grpc server for the user_management service
                        # server = user_management_grpc.server(futures.ThreadPoolExecutor(max_workers=4))
                        # print("server :: {0}".format(server))
                        # user_management_logger.info("Created GRPC server with the workers of max :: {0}".format(USER_MANAGEMENT_GRPC_MAX_WORKERS))
                        # token_pb2_grpc.add_UserValidationForTokenGenerationServiceServicer_to_server(UserValidationForTokenGenerationService(), server)
                        # user_management_logger.info("Registered GRPC server to the server :: {0}".format("UserValidationForTokenGenerationService"))
                        # server.add_insecure_port(usermanager_app.config["USER_MANAGEMENT_GRPC_SERVER_IP"] + ":" + usermanager_app.config["USER_MANAGEMENT_GRPC_SERVER_PORT"])
                        # user_management_logger.info("Starting GRPC server for the Token-User service with the IP & PORT:: {0}:{1}".format(usermanager_app.config["USER_MANAGEMENT_GRPC_SERVER_IP"], usermanager_app.config["USER_MANAGEMENT_GRPC_SERVER_PORT"]))

    else:
        print("File not found or not loaded :: {0} ".format(user_management_env_filepath))
except Exception as ex:
    print("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
