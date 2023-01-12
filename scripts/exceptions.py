class UIDNotFoundError(Exception):

    def __init__(self, status_code):
        self.status_code = status_code


class APIRequestError(Exception):

    def __init__(self, status_code):
        self.status_code = status_code


class UnkownAPIError(Exception):
    pass