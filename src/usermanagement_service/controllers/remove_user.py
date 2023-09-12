import sys
from sqlalchemy.exc import SQLAlchemyError
from flask import request, make_response
from src.usermanagement_service.models.user_model import UsersModel
from src.usermanagement_service import user_management_app_logger,del_user_headers_schema, usermanager
from src.admin_common.admin_error_handling import PyPortalAdminInvalidRequestError, PyPortalAdminInternalServerError, \
    PyPortalAdminNotFoundError
# from src.usermanagement_service.utils.util_helpers import is_userid_exists


def deregister_user(userid):
    try:
        user_management_app_logger.info('REQUEST ==> Received Endpoint for the request:: {0}'.format(request.endpoint))
        user_management_app_logger.info('REQUEST ==> Received url for the request :: {0}'.format(request.url))
        if request.method == 'DELETE':
            rec_req_headers = dict(request.headers)
            user_management_app_logger.info("Received Headers from the request :: {0}".format(rec_req_headers))
            ''' 
                1. Find the missing headers, any schema related issue related to headers in the request
                2. If any missing headers or schema related issue , send the error response back to client.
                3. Custom error response contains the information about headers related to missing/schema issue, with status code as 400,BAD_REQUEST
            '''
            del_header_result = usermanager.generate_req_missing_params(rec_req_headers, del_user_headers_schema)
            if len(del_header_result.keys()) != 0:
                invalid_header_err_res = PyPortalAdminInvalidRequestError(message="Request Headers Missing",
                                                                          error_details=del_header_result,
                                                                          logger=user_management_app_logger)
                return invalid_header_err_res.send_resposne_to_client()

            del_user_management_session = usermanager.get_session_from_conn_pool()
            if del_user_management_session is None:
                invalid_req_err_res = PyPortalAdminInternalServerError(message="Create Session Failed",
                                                                       logger=user_management_app_logger)
                return invalid_req_err_res.send_response_to_client()
            try:
                ''' 1. Delete the user record from the database using the primary key userid
                    2. Converting the database model of user to defined user and serialize to json
                    3. Using the serialize , Generating the success custom response , headers  '''
                get_user_instance = del_user_management_session.query(UsersModel).get(userid)
                if get_user_instance is None:
                    usr_not_found_err_res = PyPortalAdminNotFoundError(message="Retrieved user doesn't exists", logger=user_management_app_logger)
                    return usr_not_found_err_res.send_response_to_client()
                user_management_app_logger.info("Found user with the id in the db :: {0}".format(userid))
                del_user_management_session.query(UsersModel).filter(UsersModel.ID == userid).delete()
                del_user_management_session.commit()
                del_usr_response = make_response('')
                del_usr_response.headers['Cache-Control'] = 'no-cache'
                del_usr_response.status_code = 204
                user_management_app_logger.info("Prepared success response and sending back to client  {0}:: [STARTED]".format(del_usr_response))
                return del_usr_response
            except SQLAlchemyError as ex:
                usermanager.rollback_session(sessionname=del_user_management_session)
                print("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
                db_err_res = PyPortalAdminInternalServerError(message="Database Error", logger=user_management_app_logger)
                return db_err_res.send_response_to_client()
            except Exception as ex:
                usermanager.rollback_session(sessionname=del_user_management_session)
                print("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
                internal_err_res = PyPortalAdminInternalServerError(message="Internal Server Error",
                                                                    logger=user_management_app_logger)
                return internal_err_res.send_response_to_client()
            finally:
                usermanager.close_session(sessionname=del_user_management_session)

    except Exception as ex:
        print("Error occurred :: {0}\tLine No:: {1}".format(ex, sys.exc_info()[2].tb_lineno))
        invalid_req_err_res = PyPortalAdminInternalServerError(message="Unknown error caused", logger=user_management_app_logger)
        return invalid_req_err_res.send_response_to_client()
