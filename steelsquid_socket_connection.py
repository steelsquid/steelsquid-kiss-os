#!/usr/bin/python -OO


'''
Socket implementation of steelsquid_connection...

@organization: Steelsquid
@author: Andreas Nilsson
@contact: steelsquid@gmail.com
@license: GNU Lesser General Public License v2.1
@change: 2013-10-25 Created
'''


import steelsquid_connection
import steelsquid_utils
import socket
import sys
import select

only_once=False

class SteelsquidSocketConnection(steelsquid_connection.SteelsquidConnection):


    def __init__(self, is_server, host='localhost', port=22222):
        '''
        Constructor
        '''
        super(SteelsquidSocketConnection, self).__init__(is_server)
        self.host = host
        self.port = port


    def on_setup_client(self):
        '''
        Override this to setup the client.
        Example setup socket
        Will loop until server is stopped.
        @return: Connection object (example socket)
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        global only_once
        if steelsquid_utils.development():
            steelsquid_utils.shout("Socket Connection (Client)\n"+self.host +":"+ str(self.port), debug=True)
        else:
            if not only_once:
                only_once = True
                steelsquid_utils.shout("Socket Connection (Client)\n"+self.host +":"+ str(self.port), debug=False)
        return sock


    def on_setup_server(self):
        '''
        Override this to setup the server.
        Example setup the serversocket
        Will loop until server is stopped.
        @return: Listener object (example serversocket)
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(2)
        s.bind(('', self.port))
        s.listen(3)
        steelsquid_utils.shout("Socket Connection (Server)\nPort: "+str(self.port), debug=False)
        return s


    def on_connect(self, connection_object):
        '''
        Override this to connect to a server.
        Example connect to a socket.
        Will loop until server is stopped.
        @param connection_object: The object from on_setup_client
        @return: connection_object (the connection_object object)
        '''
        connection_object.connect((self.host, self.port))
        steelsquid_utils.shout("Socket Connection: Connected to server", debug=True)
        return connection_object


    def on_listen(self, listener_object):
        '''
        Override this to start the server listen for connection functionality.
        Example listen for clients on a socket.
        Will loop until server is stopped.
        @param listener_object: The object from on_setup_server
        @return: connection_object (None = do nothing)
        '''
        try:
            sock, _ = listener_object.accept()
            steelsquid_utils.shout("Socket Connection: Client connected", debug=True)
            return sock
        except socket.timeout:
            return None


    def on_read(self, connection_object):
        '''
        Override this to listen for data.
        Example listen for requests on socket
        @param connection_object: Read from this client
        @return: (type, command, parameters) 
                 (type = request, response, error)
                 command = None (do nothing)
        '''
        ready_to_read, ready_to_write, in_error = select.select([connection_object], [], [], 2)
        if ready_to_read:
            data = connection_object.makefile().readline()
            if not data:
                raise IOError("Connection lost")
            else:
                data_array = data.rstrip().split("|")
                if len(data_array) >= 2:
                    typ = data_array[0]
                    command = data_array[1]
                    para = data_array[2:]
                    return typ, command, para
                else:
                    return None, None, None
        else:        
            return None, None, None


    def on_write(self, the_type, connection_object, command, parameters):
        '''
        Override this to send data to host.
        Example write request on socket
        @param the_type: "request", "response", "error"
        @param connection_object: Write to this client
        @param command: The command
        @param answer_list: parameters
        @return: True = Continue
                 False = Close connection
        '''
        answ = "|".join(parameters)
        connection_object.sendall(the_type+ "|" + command + "|" + answ + "\n")
        return True


    def on_close_connection(self, connection_object, error_message):
        '''
        Override this to close the connection.
        Will also execute on connection lost or no connection
        @param server_object: The connection (Can be None)
        @param error_message: I a error (Can be None)
        '''
        steelsquid_utils.shout("Socket Connection: Connection closed\n"+ error_message, debug=True)
        connection_object.close()

    
    def on_close_listener(self, listener_object, error_message):
        '''
        Override this to close the listener.
        Will also execute on unable to listen
        @param listener_object: The listener (Can be None)
        @param error_message: I a error (Can be None)
        '''
        steelsquid_utils.shout("Socket Connection: Listener closed: " + error_message, debug=True)
        listener_object.close()

    def get_connected_ip_numbers(self):
        '''
        Get IP number of all connections.
        If this is a server it is a list of clients ip number (the list is empty if no clients is connected).
        If this is a client it is a list with one IP-number, the server IP (the list is empty if not connected to server).
        @return: List of IP number
        '''
        the_list = []
        for client in self.get_connection_objects():
            the_list.append(client.getpeername()[0])
        return the_list


    def on_get_remote_address(self, connection_object):
        '''
        Override this to do and return the adress of the remote address (IP)
        @param connection_object: The listener object to read adress from (Can be None)
        '''
        return connection_object.getpeername()[0]


    def test_request(self, remote_address, parameters):
        print "REQUEST"
        print parameters

    def test_response(self, remote_address, parameters):
        print "RESPONSE"
        print parameters

    def test_error(self, remote_address, parameters):
        print "ERROR"
        print parameters



