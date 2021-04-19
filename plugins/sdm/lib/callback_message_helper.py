import re

ACCESS_REQUEST_GRANT_REGEX = "^yes ([a-z0-9]+)$"

class CallbackMessageHelper:
    def __init__(self, log, admin_ids, grant_access_request_fn):
        self.__log = log
        self.__admin_ids = admin_ids
        self.__grant_access_request = grant_access_request_fn

    def execute(self, message):
        if self.__is_valid_access_request_grant(message):
            access_request_id = self.__get_access_request_id(message)
            self.__grant_access_request(access_request_id)

    def __is_valid_access_request_grant(self, message):
        message_from_admin = message.frm in self.__admin_ids
        valid_grant_pattern = re.match(ACCESS_REQUEST_GRANT_REGEX, message.body, flags=re.I)
        is_valid_access_request_grant = message_from_admin and valid_grant_pattern
        self.__log.error(f"message_body: {message.body} sender id: {message.frm} admin_ids: {self.__admin_ids} is_valid_access_request_grant: {is_valid_access_request_grant}")
        return is_valid_access_request_grant

    def __get_access_request_id(self, message):
        return re.sub(ACCESS_REQUEST_GRANT_REGEX, "\\1", message.body, flags=re.I)
