import argparse     # https://docs.python.org/3.10/library/argparse.html?highlight=argparse
import socket       # https://docs.python.org/3.10/library/socket.html?highlight=socket#module-socket
import shlex        # https://docs.python.org/3.10/library/shlex.html?highlight=shlex
import subprocess   # https://docs.python.org/3.10/library/subprocess.html?highlight=subprocess
import sys          # https://docs.python.org/3.10/library/subprocess.html?highlight=subprocess
import textwrap     # https://docs.python.org/3.10/library/subprocess.html?highlight=subprocess
import threading    # https://docs.python.org/3.10/library/threading.html?highlight=threading#module-threading


class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # SO_REUSEADDR = http://www.unixguide.net/network/socketfaq/4.11.shtml
        # SOL_SOCKET = https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html
            # The SOL_SOCKET link is a good explination for both options


    #! This was a bug in the book, the book did not have the "self" argument first
    def execute(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return
        output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
        return output.decode()


    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()


    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
            
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    buffer = input('NetCat# > ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated the session')
            self.socket.close()
            sys.exit()


    def listen(self):
        # print(f'In listen')
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            # print(f'In listen True')
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            # print(f'client_thread {client_thread}')
            client_thread.start()


    def handle(self, client_socket):
        if self.args.execute:
            print(f'In handle {self.args.execute}')
            output = self.execute(self.args.execute)
            client_socket.send(output.encode())
            
        elif self.args.upload:
            print(f'In upload {self.args.upload}')
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as file:
                file.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
            
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    #! Bug in the books code, had to decode the buffer 
                    prompt = 'NetCat# > '
                    prompt = prompt.encode()
                    #! The send needed to be encoded
                    client_socket.send(prompt)
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = self.execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'Server killed {e}')
                    self.socket.close()
                    sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="BHP NetCat", formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent('''Example:
        netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload a file
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
        netcat.py -t 192.168.1.108 -p 5555 # connect to the server
    '''))

parser.add_argument('-c', '--command', action='store_true', help='command shell')
parser.add_argument('-e', '--execute', help='execute specified command')
parser.add_argument('-l', '--listen', action='store_true', help='listen')
parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
parser.add_argument('-u', '--upload', help='upload file')

args = parser.parse_args()
if args.listen:
    buffer = ''
else:
    buffer = sys.stdin.read()

NetCat = NetCat(args, buffer.encode())
NetCat.run()