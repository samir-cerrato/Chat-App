# Samir Cerrato
#!/usr/bin/python3

#
# COMP 332
# Chat client
#
# Example usage:
#
#   python3 chat_client.py <chat_host> <chat_port>
#

import socket
import sys
import threading


class ChatClient:

    def __init__(self, chat_host, chat_port):
        self.chat_host = chat_host
        self.chat_port = chat_port
        self.username = input("Enter username: ")
        self.start()

    def start(self):

        # Open connection to chat
        try:
            chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            chat_sock.connect((self.chat_host, self.chat_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ")
            if chat_sock:
                chat_sock.close()
            sys.exit(1)

        threading.Thread(target=self.write_sock, args=(chat_sock,)).start()
        threading.Thread(target=self.read_sock, args=(chat_sock,)).start()

    def write_sock(self, sock):

        # Fill this out
        print("In write sock")
        while True:
            message = input(f"{self.username}:>>")
            message_length = f"{len(message)}"
            message_header = self.username + ":" + message_length + "\r\n\r\n" + message
            data = message_header.encode('utf-8')

            try:
                sock.sendall(data)
            except Exception as e:
                print("Error sending message:", e)
                break


    def read_sock(self, sock):

        # Fill this out
        print("In read sock")
        buffer = b''
        while True:
            bin_message = sock.recv(1024)
            if bin_message == b'':
                return
            buffer += bin_message

            try:
                str_data = buffer.decode('utf-8')
                idx = str_data.index('.')
                msg_length = int(str_data[:idx])
                if msg_length <= len(str_data[idx:]):
                    message = str_data[idx + 1:idx + msg_length + 1]
                    buffer = buffer[idx + msg_length + 1:]
                    print(message)
            except ValueError as e:
                pass


def main():

    print (sys.argv, len(sys.argv))
    chat_host = 'localhost'
    chat_port = 50007

    if len(sys.argv) > 1:
        chat_host = sys.argv[1]
        chat_port = int(sys.argv[2])

    chat_client = ChatClient(chat_host, chat_port)

if __name__ == '__main__':
    main()
