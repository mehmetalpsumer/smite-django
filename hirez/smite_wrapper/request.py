import aiohttp
import sys
import hashlib

from datetime import datetime


class Request:
    """Class for all of the outgoing requests from the library. An instance of
    this is created by the Client class. Do not initialise this yourself.

    Parameters
    ----------
        client : Client
            An initialised Client object
        session : [optional] aiohttp.ClientSession
            Custom client session to use with aiohttp's outgoing requests

    """
    def __init__(self, client, *, session=None):
        self.client = client
        self.headers = {"User-Agent": "smite_wrapper/1.0 [Python/{0.major}.{0.minor} aiohttp/{1}]".format(
            sys.version_info, aiohttp.__version__
        )}

        self.session = client.loop.run_until_complete(self._create_connection())
        self._active_session = None

    async def _create_connection(self):
        return aiohttp.ClientSession(loop=self.client.loop, headers=self.headers)

    def _create_signature(self, method_name):
        """Generates a new MD5 hashed signature

        Parameters
        ----------
        method_name : str
            The method that will be called.

        """
        now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        signature = hashlib.md5(self.client.dev_id.encode('utf-8') + method_name.encode('utf-8') +
                                self.client.auth_key.encode('utf-8') + now.encode('utf-8')).hexdigest()
        return signature

    async def make_request(self, endpoint, call, *, method='GET', params=[], no_auth=False,
                           session=None, bypass_session_test=False):
        """Makes an outgoing web request to an API and returns the result as JSON

        Parameters
        ----------
        endpoint : str
            The base API endpoint to make a call to.
        call : str
            The API endpoint to make a call to.
        method : [optional] str
            Override the method used to make HTTP requests.
            By default, this is GET.
        params : [optional] list
            Parameters to send with the request, in order
        no_auth : [optional] bool
            Specifies if the request requires authentication.
        bypass_session_test : [optional] bool
            Specifies if we should bypass the check and tests for sessions.

        Returns
        -------
        list or dict
            JSON data returned from the request

        """
        if no_auth is False:
            if bypass_session_test is False:
                if not self._active_session or not self._test_session(endpoint, self._active_session):
                    self._active_session = await self._create_session(endpoint)
            ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            sig = self._create_signature(call)
            call = call + 'Json'
            if self._active_session is not None:
                to_join = [endpoint, call, self.client.dev_id, sig, self._active_session.get('session_id'), ts]
                if params:
                    to_join += params
            else:
                to_join = [endpoint, call, self.client.dev_id, sig, ts]
                if params:
                    to_join += params
            url = "/".join(to_join)
        else:
            call = call + 'Json'
            to_join = [endpoint, call]
            if params:
                to_join += params
            url = "/".join(to_join)

        async with self.session.request(method, url) as req:
            if req.status != 200:
                raise ConnectionError("There was a problem with your request. Returned HTTP {0.status}, "
                                      "using {0.method} -> {0.url}".format(req))
            json = await req.json()

        if json is None:
            raise TypeError("Result wasn't JSON. Using {0.method} -> {0.url}".format(req))

        try:
            ret_msg = json['ret_msg']
            if 'exception' in ret_msg.lower():
                raise ConnectionError(ret_msg)
        except TypeError:  # was a list instead, which is okay
            pass
        return json

    async def _test_session(self, endpoint, session=None):
        """Tests a session to ensure that it is still active

        Parameters
        ----------
        endpoint : str
            The base API endpoint to make a call to.
        session : dict
            The session to test against the API.

        Returns
        -------
        bool
            Indicates if the test was successful or not

        """
        if session is None:
            # do nothing
            return

        res = await self.make_request(endpoint, 'testsession', bypass_session_test=True)
        if 'successful' in res:
            return True
        else:
            return False

    async def _create_session(self, endpoint):
        """Creates a new session

        Parameters
        ----------
        endpoint : str
            The base API endpoint to make a call to.

        Returns
        -------
        dict
            JSON data returned from the request

        """
        res = await self.make_request(endpoint, 'createsession', bypass_session_test=True)
        return res
