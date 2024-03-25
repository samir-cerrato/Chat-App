# Samir Cerrato
#!/usr/bin/python3
#
# COMP 332
# Chat server
#
# Usage:
#   python3 chat_server.py <host> <port>
#

import socket
import sys
import threading

class ChatProxy():

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1
        self.chat_list = {}
        self.chat_id = 0
        self.lock = threading.Lock()
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
        except OSError as e:
            print ("Unable to open server socket")
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for user connection
        while True:
            conn, addr = server_sock.accept()
            self.add_user(conn, addr)
            thread = threading.Thread(target = self.serve_user,
                    args = (conn, addr, self.chat_id))
            thread.start()

    def add_user(self, conn, addr):
        print ('User has connected', addr)
        self.chat_id = self.chat_id + 1
        self.lock.acquire()
        self.chat_list[self.chat_id] = (conn, addr)
        self.lock.release()

    def read_data(self, conn):

        # Fill this out
        print("In read data")
        buffer = b''
        while True:
            # Read from socket
            bin_message = conn.recv(1024)
            if bin_message == b'':
                return ['', '', 1]  # Indicates client disconnection

            buffer += bin_message

            try:
                # Get message length
                str_data = buffer.decode('utf-8')
                idx = str_data.index('.')
                msg_length = int(str_data[:idx])

                # Check whether full message received
                if msg_length <= len(str_data[idx:]):
                    message = str_data[:idx + msg_length + 1]
                    buffer = buffer[idx + msg_length + 1:]
                    return [message, buffer, 0]  # 0 indicates successful message retrieval

            except ValueError as e:
                pass

    def send_data(self, user, data):
        self.lock.acquire()
        bin_message = data.encode('utf-8')
        
        # Fill this out
        print("In send data")

        try:
        # Send message to all users except the sender
            for i in self.chat_list:
                if i != user:
                    entry = self.chat_list[i]
                    conn = entry[0]
                    conn.sendall(bin_message)
        except Exception as e:
            print("Error sending data:", e)
        finally:
            self.lock.release()


    def cleanup(self, conn):
        self.lock.acquire()

        # Fill this out
        print("In cleanup")
        try: 
            for chat_id, (connection, addr) in self.chat_list.items():
                if connection == conn:
                    print(f"Cleaning up user: {addr}")
                    conn.close()
                    del self.chat_list[chat_id]
                    break
        except Exception as e:
            print("Error cleaning up:", e)
        finally:
            self.lock.release()

    def serve_user(self, conn, addr, user):

        # Fill this out
        print("In serve user")
        try:
            while True:
                data = self.read_data(conn)
                if not data:
                    break
                print("Received from", addr, ":", data)
                self.send_data(user, data)
        finally:
            self.cleanup(conn)


def main():

    print (sys.argv, len(sys.argv))
    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    chat_server = ChatProxy(server_host, server_port)

if __name__ == '__main__':
    main()
