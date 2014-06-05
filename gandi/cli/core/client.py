# -*- coding: utf-8 -*-
import socket
import xmlrpclib
from gandi.cli import __version__


class APICallFailed(Exception):
    """ Raise when an error occured during an api call"""

    def __init__(self, errors):
        self.errors = errors


class GandiTransport(xmlrpclib.SafeTransport):

    _user_agent = None

    def send_user_agent(self, connection):
        if not self._user_agent:
            self._user_agent = '%s %s' % (xmlrpclib.Transport.user_agent,
                                          'gandi.cli/%s' % __version__)
        connection.putheader('User-Agent', self._user_agent)


class XMLRPCClient(object):
    """ Class wrapper for xmlrpc calls to Gandi public API """

    def __init__(self, host, debug=False):
        self.debug = debug
        self.endpoint = xmlrpclib.ServerProxy(host)

    def request(self, apikey, method, *args):
        try:
            func = getattr(self.endpoint, method)
            return func(apikey, *args)
        except socket.error:
            msg = 'Gandi API service is unreachable'
            raise APICallFailed(msg)
        except xmlrpclib.Fault as err:
            msg = 'Gandi API has returned an error: %s' % err
            raise APICallFailed(msg)
        except TypeError as err:
            msg = 'An unknown error as occured: %s' % err
            raise APICallFailed(msg)
