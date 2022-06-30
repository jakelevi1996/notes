# Notes on Python

This is a collection of notes on Python, including useful links, useful snippets, Python implementations of algorithms, and notes on built-in and third-party modules.

TODO: migrate existing Python-related Gists into subsections of this Gist

## Contents

- [Notes on Python](#notes-on-python)
  - [Contents](#contents)
  - [Useful links](#useful-links)
  - [Useful Python snippets](#useful-python-snippets)
    - [Custon context managers using `__enter__` and `__exit__`](#custon-context-managers-using-__enter__-and-__exit__)
  - [Python implementations of algorithms](#python-implementations-of-algorithms)
    - [Find all permutations of a string](#find-all-permutations-of-a-string)
    - [Start a parallel subprocess in a new console window](#start-a-parallel-subprocess-in-a-new-console-window)
  - [Notes on built-in and third-party modules](#notes-on-built-in-and-third-party-modules)
    - [`socket`](#socket)

## Useful links

- [Python homepage](https://www.python.org/)
- [Download Python](https://www.python.org/downloads/)
- [Documentation](https://docs.python.org/3/)
  - [The Python Tutorial](https://docs.python.org/3/tutorial/index.html)
  - [The Python Standard Library](https://docs.python.org/3/library/index.html) (including all built-in modules)
    - [Built-in Functions](https://docs.python.org/3/library/functions.html)
    - [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
  - [The Python Language Reference](https://docs.python.org/3/reference/index.html)
    - [Data model](https://docs.python.org/3/reference/datamodel.html)
- [Project Euler](https://projecteuler.net/archives) (useful and interesting problems for practising numerical programming, and well-suited to Python)

## Useful Python snippets

### Custon context managers using `__enter__` and `__exit__`

Inside a class definition, defining the methods `__enter__(self)` and `__exit__(self, exc_type, exc_value, traceback)` allows that class to be used as a context manager. Note that if an exception is raised inside the context manager, the `__exit__` method will be executed before the exception is raised (or not raised, in case `__exit__` returns a true value), as described in the documentation for the `__exit__` method in the [Python data model](https://docs.python.org/3/reference/datamodel.html):

> Exit the runtime context related to this object. The parameters describe the exception that caused the context to be exited. If the context was exited without an exception, all three arguments will be None.

> If an exception is supplied, and the method wishes to suppress the exception (i.e., prevent it from being propagated), it should return a true value. Otherwise, the exception will be processed normally upon exit from this method.

This is useful EG if some clean-up code is supposed to be run after calling the `main` function, regardless of whether or not an exception is raised in `main` - the `main` function can be put inside a context manager, and the clean-up code can be put inside the `__exit__` method.

Here is a simple example of context managers and exceptions:

```python
class C:
    def __enter__(self):
        print("In enter")
    def __exit__(self, exc_type, exc_value, traceback):
        print("In exit")

with C():
    print("Inside context manager")
    raise RuntimeError()
    print("This statement is not reached")
```

Output:

```
In enter
Inside context manager
In exit
Traceback (most recent call last):
  File "~/.temp.py", line 9, in <module>
    raise RuntimeError()
RuntimeError
```

## Python implementations of algorithms

### Find all permutations of a string

Note that this could be made more efficient by storing each 2-tuple (each of which contains the prefix of a valid permutation, and the remaining choices for that permutation) as a single string.

```python
def find_permutations(s):
    """ Find all permutations of the string s. This can be performed using
    itertools.permutations, but implementing it from scratch is an interesting
    challenge. """
    # Initialise list of 2-tuples, each of which contains the prefix of a valid
    # permutation, and the remaining choices for that permutation
    prefix_choices_tuple_list = [("", s)]
    # On each iteration we increase the length of each prefix by 1, until each
    # prefix is the length of a full permutation
    for _ in range(len(s)):
        # For each tuple of a valid prefix of a perumutation and the remaining
        # choices, replace the tuple with all tuples containing the same prefix
        # extended by one of the remaining choices, and the other remaining
        # choices
        prefix_choices_tuple_list = [
            (prefix + choice, choice_list[:i] + choice_list[i+1:])
            for prefix, choice_list in prefix_choices_tuple_list
            for i, choice in enumerate(choice_list)
        ]
    # Extract and return all of the prefixes, which are now complete
    # permutations (with no remaining choices for each prefix)
    perm_list = [prefix for prefix, _ in prefix_choices_tuple_list]
    return perm_list

print(find_permutations("1234"))
# >>> ['1234', '1243', '1324', '1342', '1423', '1432', '2134', '2143', '2314',
#      '2341', '2413', '2431', '3124', '3142', '3214', '3241', '3412', '3421',
#      '4123', '4132', '4213', '4231', '4312', '4321']
```

### Start a parallel subprocess in a new console window

`create_process.py`

```python
import subprocess
import time

print("Starting new process...")

cmd = ["python", "print_slow.py"]
subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

print("This process runs in parallel...")
time.sleep(1)
print("... while the other process is running in a new console...")
time.sleep(1)
print("... and both processes are running at the same time")
```

`print_slow.py`

```python
from time import sleep

print("Console closing in ", end="\n")
for i in reversed(range(5)):
    print("%i..." % (i + 1))
    sleep(1)
```

## Notes on built-in and third-party modules

### `socket`

These notes are mostly made from the [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/) on [realpython.com](https://realpython.com/). See also the [Python documentation for the `socket` module](https://docs.python.org/3/library/socket.html).

Below are the `echo-server.py` and `echo-client.py` programs from the [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/) on [realpython.com](https://realpython.com/), demonstrating a simple client-server application which communicates using sockets:

Server program:

```python
# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
```

Client program:

```python
# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")
```

- Sockets can be used to communicate between different processes on a single PC, or different PCs connected over a network
- Sockets "originated with [ARPANET](https://en.wikipedia.org/wiki/ARPANET) in 1971 and later became an API in the [Berkeley Software Distribution (BSD)](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution) operating system released in 1983 called [Berkeley sockets](https://en.wikipedia.org/wiki/Berkeley_sockets)"
- "All modern operating systems implement a version of the Berkeley socket interface. It became the standard interface for applications running in the Internet" ([source](https://en.wikipedia.org/wiki/Berkeley_sockets))
- "The most common type of socket applications are client-server applications, where one side acts as the server and waits for connections from clients"
- In Python, after importing the `socket` module using `import socket`, a socket can be created using the [`socket.socket`](https://docs.python.org/3/library/socket.html#socket.socket) class, EG `s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
  - The first argument to `socket.socket` is `family`, which represents the "address (and protocol) families", and can be EG `socket.AF_INET` or `socket.AF_INET6`
    - `socket.AF_INET` represents the [Internet Protocol version 4 (IPv4)](https://en.wikipedia.org/wiki/IPv4) **A**ddress **F**amily
    - `socket.AF_INET6` can be used for IPv6
  - The second argument to `socket.socket` is `type`, which represents the "socket types", and can be EG `socket.SOCK_STREAM` or `socket.SOCK_DGRAM`
    - `socket.SOCK_STREAM` specifies that the default protocol used by the socket is the [Transmission Control Protocol (TCP)](https://en.wikipedia.org/wiki/Transmission_Control_Protocol), which is reliable ("packets dropped in the network are detected and retransmitted by the sender") and has in-order data delivery ("data is read by your application in the order it was written by the sender")
    - `socket.SOCK_DGRAM` can be used to specify User Datagram Protocol (UDP) sockets, which aren’t reliable, and can deliver data in a different order from that which was sent
- In a client-server socket application, in order to initialise a 2-way connection between the client and the server:
  - The server's socket object will call the `bind`, `listen`, and `accept` methods
    - The `bind(address)` method "is used to associate the socket with a specific network interface and port number"
      - The format of `address` depends on the address family of the socket
      - When the address family is `socket.AF_INET` (IPv4), `address` should be a 2-tuple containing the host and the port
      - The host "can be a hostname, IP address, or empty string"
        - "If an IP address is used, host should be an IPv4-formatted address string"
          - "The IP address 127.0.0.1 is the standard IPv4 address for the loopback interface", which can be used to connect to other sockets on the same PC, which "bypasses any local network interface hardware" (see the Wikipedia entry for [`localhost`](https://en.wikipedia.org/wiki/Localhost))
          - The 24-bit block 10.0.0.0/8 (16,777,216 addresses), 20-bit block 172.16.0.0/12 (1,048,576 addresses) and 16-bit block 192.168.0.0/16 (65,536 addresses) are reserved for addresses on the private network (see the Wikipedia entry for [Private network](https://en.wikipedia.org/wiki/Private_network))
        - "If you pass an empty string, the server will accept connections on all available IPv4 interfaces"
        - "If you use a hostname in the host portion of IPv4/v6 socket address, the program may show a non-deterministic behavior, as Python uses the first address returned from the DNS resolution... For deterministic behavior use a numeric address in host portion"
      - The port "represents the TCP port number to accept connections on from clients"
        - "It should be an integer from 1 to 65535, as 0 is reserved"
        - "Some systems may require superuser privileges if the port number is less than 1024"
    - The `listen` method "enables a server to accept connections", and makes the server's socket object a "listening" socket
      - The `listen` method has an optional backlog parameter, which "specifies the number of unaccepted connections that the system will allow before refusing new connections... If not specified, a default backlog value is chosen"
      - "If your server receives a lot of connection requests simultaneously, increasing the `backlog` value may help by setting the maximum length of the queue for pending connections"
    - The `accept()` method "blocks execution and waits for an incoming connection"
      - When a client socket connects to the server's socket object, the server's socket object's call to the `accept` method returns a 2-tuple containing:
        - A new socket object representing the connection
        - A tuple holding the address of the client
          - For IPv4 connections, the tuple holding the address of the client will contain `(host, port)`
      - Note that the new socket returned by the `accept` method is the socket that will be used to communicate with the client's socket
        - This is distinct from the listening socket that was previously created by the server (the object from which the `accept` method was called), which is a listening socket that the server can use to accept new connections
  - The client's socket object will call the `connect` method to connect to the server's socket object
    - `connect(address)` accepts an address whose format depends on the address family
    - When the address family is `socket.AF_INET` (IPv4), `address` should be a 2-tuple containing the host and the port
- The socket on the client can communicate with the socket returned by `accept` on the server EG by calling `send` and `recv`, while the original socket created on the server which called `listen` remains a listening socket
- The client and server can be on different machines connected over a local network, in which case the IP address that the server passes to `socket.bind(address)` and the IP address that the client passes to `socket.connect(address)` should both be set to the IP address of the network adapter of the *server* through which the server will communicate (EG an ethernet connection), and of course the port numbers should also match
  - The IP address of the desired network adapter can be found in `bash` using the commands `ip a` or `ifconfig`, or in Powershell using the command `ipconfig`
  - The address in the second element of the tuple returned by the `socket.accept()` method on the server will contain the IP address and port of the network adapter through which the *client* will communicate
- Both the client and the server can send bytes objects using the `send` or `sendall` methods and receive bytes using the `recv` method
- When the client has finished sending and receiving information, it can call the `socket.close()` method
  - Calling `socket.close()` on the client sends an empty bytes object to the server
  - Therefore, when the server receives an empty bytes object from the `recv` method, it may also wish to call the `socket.close()` method
  - Python `socket.socket` objects support context managers, which call the `socket.close()` method when the context manager exits, EG with the expression `with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:`, or after `conn, addr = s.accept()`, with the expression `with conn:`
- NB an entire complex Python object can be sent through a socket, by converting the Python object to a bytes object using `pickle.dumps`, sending that bytes object through the socket using `socket.sendall`/`socket.recv`, and then unpickling the bytes object using `pickle.loads` ([source](https://stackoverflow.com/a/53577447/8477566))

