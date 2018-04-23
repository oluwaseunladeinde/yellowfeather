import json

from .utils import DecimalEncoder

class Response(object):
    """
    The ResponseModel Class encapsulates the request response in JSON format.
    """
    def __init__(self):
        """
        Constructor
        """
        super(Response, self).__init__()
        self.response = {}
        self.data = {}
        self.status_code = 0

    def add_param(self, key_str, value_str):
        """
        Adds a key/value pair to the Response dict payload
        """
        print("Adding %s as key for %s" % (key_str, value_str))
        self.data[key_str] = value_str

    def add_message(self, msgtxt, title=None):
        """
        Used to pass a message to the response. A wrapper for resp.add_param('message', 'message text goes here')
        :param txt:
        :return:
        """
        self.data['message'] = msgtxt
        if title:
            self.data['message_title'] = title

    def passed(self):
        """
        Set the status of the response as success i.e. HTTP200
        """
        self.response['status'] = 'success'
        self.status_code = 200

    def failed(self):
        """
        Set the status of the response to failed i.e. HTTP200 but failed
        attempt at the response result.
        :return:
        """
        self.response['status'] = 'fail'
        self.status_code = 400

    def error(self):
        """
        Set the status of the response to failed i.e. HTTP404
        :return:
        """
        self.response['status'] = 'error'

    def no_params(self, message=None):
        """
        Set the status of the response to failed i.e. HTTP404
        :return:
        """
        self.response['status'] = 'fail'
        self.status_code = 400
        if message:
            self.data['message'] = message
        else:
            self.data['message'] = 'No paramaters was sent or the construct of the parameter is invalid. Please verify.'
        self.data['message_title'] = 'No Parameters'


    def no_token(self):
        """
        No token was found or given
        :return:
        """
        self.response['status'] = 'error'
        self.data['message'] = "No Request Token was found or the Request Token sent was invalid. You probably have not logged in"


    def missing_params(self, message=None):
        """
        Set the status of the response to failed i.e. HTTP404
        :return:
        """
        self.response['status'] = 'error'
        if message:
            self.data['message'] = message
        else:
            self.data['message'] = 'There are missing paramters in your request. Please verify.'


    def failed_api_call(self, message=None):
        """
        If a call to an external API fails, this method is a
        response wrapper to the API Consumer (Web UI, Postman etc.)
        :return:
        """
        self.response['status'] = 'error'
        if message:
            self.data['message'] = message
        else:
            self.data['message'] = 'Call to the API failed. Check your paramters and try again.'

    def set_error_message(self, mssgString):
        """

        :param mssgString:
        :return:
        """
        self.response['message'] = mssgString

    def get_response(self, isdecimal=True):
        """

        :return:
        """
        self.response['data'] = self.data
        #json_resp = json.dumps(self.response)
        #print('################### serializing Decimal ', self.response)
        if isdecimal:
            json_resp = json.dumps(self.response, cls=DecimalEncoder)
        else:
            json_resp = json.dumps(self.response)
        return json_resp

    def print_result(self):
        """

        :return:
        """
        json_resp = json.dumps(self.response)
        print('--> JSON Response', json_resp)
