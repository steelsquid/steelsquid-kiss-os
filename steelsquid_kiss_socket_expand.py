#!/usr/bin/python -OO


'''
Controll steelsquid kiss os with simle socket commands
Use this to expand functionality...

@organization: Steelsquid
@author: Andreas Nilsson
@contact: steelsquid@gmail.com
@change: 2013-10-25 Created
'''


import steelsquid_kiss_socket_connection
import steelsquid_utils
import socket
import sys
import select
import thread
import os
import time

class SteelsquidKissSocketExpand(steelsquid_kiss_socket_connection.SteelsquidKissSocketServer):


    def __init__(self, is_server, port=22222):
        '''
        Constructor
        '''
        super(SteelsquidKissSocketExpand, self).__init__(is_server, port)

 


