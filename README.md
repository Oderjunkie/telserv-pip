TelServ - A BBS python library.
============

Overview
--------
  ---

TelServ is a python 3.x library designed to make hosting Telnet servicies/BBses easier.

Usage
-----
 ---

#### Getting it
   ---
TelServ can be installed via PiP.
```bash
pip install telserv==0.1
```

#### Using it
   ---
Simply import the library:
```python
import telserv as tel
```
And that's it!

##### Start coding
   ---
The way TelServ works is creating a server object and passing in a "main" function that contains the code for the BBS. like this:
```python
def main(line):
    # Code goes here...
server = tel.TelnetServer(main)
```
Notice that the main function takes an argument: "line", the _line_ variable is what allows you to interact with the command _line_.

The type of the line argument is `CommandLine`, and here are all of it's functions:
```python
def main(line):
    line.print('line.print prints the text passed in as an argument, And it also supports ANSI sequences.')
    
    line.printnonew('line.printnonew is the same as line.print, except it does not add the newline at the end.\r\n')
    
    line.printbb('[b]line.printbb[/b] prints [b][color=31]BB[/color][color=34]code[/color]![/b]')
    
    # line.printbbnonew is self-explanitory.
    
    # line.printfile('directory\\of\\ansi\\art.ans')
    
    line.printbb('[b]Username: [color=31]')
    username = line.input() # Take input and stop when recieving '\r\n' which is the return key. ( '\r\n' is the default if there's no argument. )
    
    line.printbb('[/color]Password: [color=34]')
    password = line.inputhidden('*') # Take input just like line.input() but display each character as an asterisk.
    
    line.printbb('[/color][color=33]Logged in![/color]')

server = tel.TelnetServer(main)
server.start()
```
