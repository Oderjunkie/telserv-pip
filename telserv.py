import threading
import socket
import os
class CommandLine:
    def __init__(self, con, addr):
        self.con = con
        self.addr = addr
        self.style = {
            'bold': False,
            'italic': False,
            'underline': False,
            'strike': False,
            'blink': False,
            'color': 0
        }
    def bbtoans(self, stringbb):
        string = '\x1b[m'
        idx = 0
        change = False
        style = self.style
        while idx<len(stringbb):
            change = False
            if stringbb[idx:idx+3]=='[b]':
                style['bold'] = True
                change = True
                idx+=3
            if stringbb[idx:idx+4]=='[/b]':
                style['bold'] = False
                change = True
                idx+=4
            if stringbb[idx:idx+3]=='[i]':
                style['italic'] = True
                change = True
                idx+=3
            if stringbb[idx:idx+4]=='[/i]':
                style['italic'] = False
                change = True
                idx+=4
            if stringbb[idx:idx+3]=='[u]':
                style['underline'] = True
                change = True
                idx+=3
            if stringbb[idx:idx+4]=='[/u]':
                style['underline'] = False
                change = True
                idx+=4
            if stringbb[idx:idx+3]=='[s]':
                style['strike'] = True
                change = True
                idx+=3
            if stringbb[idx:idx+4]=='[/s]':
                style['strike'] = False
                change = True
                idx+=4
            if stringbb[idx:idx+7]=='[blink]':
                style['blink'] = True
                change = True
                idx+=7
            if stringbb[idx:idx+8]=='[/blink]':
                style['blink'] = False
                change = True
                idx+=8
                print('stringbb', stringbb[idx+9])
            if stringbb[idx:idx+7]=='[color=' and stringbb[idx+9]==']':
                style['color'] = stringbb[idx+7:idx+9]
                change = True
                idx+=10
            if stringbb[idx:idx+8]=='[/color]':
                style['color'] = 0
                change = True
                idx+=8
            if change:
                string+='\x1b[m'
                if style['bold']: string+='\x1b[1m'
                if style['italic']: string+='\x1b[3m'
                if style['underline']: string+='\x1b[4m'
                if style['strike']: string+='\x1b[9m'
                if style['blink']: string+='\x1b[5m'
                if style['color']: string+='\x1b[{}m'.format(style['color'])
            else:
                string+=stringbb[idx]
                idx+=1
        self.style = style
        return string
    def printnonew(self, string):
        return self.con.send(string.encode())
    def print(self, string):
        return self.printnonew('{}\r\n'.format(string))
    def printbbnonew(self, string):
        return self.printnonew(self.bbtoans(string))
    def printbb(self, string):
        return self.print(self.bbtoans(string))
    def printfile(self, file):
        return self.con.send(open(file, 'rb').read())
    def input(self, delim='\r\n'):
        stdin = ''
        length = len(delim)
        dat = self.con.recv(length).decode()
        if delim==' ': return dat
        while dat!=delim:
            stdin += dat
            dat = self.con.recv(length).decode()
        return stdin
    def inputhidden(self, censor=' ', delim='\r\n'):
        stdin = ''
        length = len(delim)
        dat = self.con.recv(length).decode()
        #self.printnonew('\x1b[D{}'.format(censor))
        if delim==' ': return dat
        while dat!=delim:
            self.printnonew('\x1b[D{}'.format(censor))
            stdin += dat
            dat = self.con.recv(length).decode()
        return stdin
    def quit(self):
        self.con.close()
class TelnetServer:
    def __init__(self, func=lambda:None, port=23):
        self.port = port
        self.func = func
    def __repr__(self):
        return 'TelnetServer({})'.format(self.port)
    def __str__(self):
        return self.__repr__()
    def start(self):
        sock = socket.socket()
        sock.bind(('',self.port))
        def listen():
            while True:
                sock.listen(5)
                threading.Thread(target=self.func, args=(CommandLine(*sock.accept()),)).start()
        threading.Thread(target=listen, args=()).start()
    def test(self):
        os.system('telnet {}'.format(socket.gethostbyname(socket.gethostname())))
def load(file):
    return open(file, 'r').read()
