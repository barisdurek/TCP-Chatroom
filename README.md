# TCP Chatroom Terminal Application
It is a multi-user and multi-threaded chat system built with Python sockets. This terminal-based chat application allows real-time public and private messaging, supports nickname assignment, message logging, and basic system monitoring.
## Features
* Unique nickname enforcement (auto-generated if duplicate)
* Public chat with message broadcasting
* Private messaging
* Message logging for both public and private chats
* Timestamped messages
* Real-time client monitoring (user count, message count)

### Logging:
* Public messages are saved to messages.txt
* Private messages are saved to private_messages.txt
* Log files contain timestamps, sender info, and message content.

### Server monitoring:
Every 5 seconds, the server displays:
* Number of currently connected users
* Number of total messages sent in public chat
* Number of total private messages

## Needed installations before using 
#### pip install names
* For random name generation, I used a library 'names'. 
* In project, client enters a nickname. If it is taken, server assigns a random nickname to this client with the library 'names'.

#### pip install keyboard
* I didn't want user to press enter for an input. Therefore with this library, if the server user want to close server, just need to press 'q' on keyboard.


## Running the program
* To run the code, just start the server and then start the clients. Code files don't get any additional arguments.
* First run the server:

```
python server.py  
```
and then:
```
python client.py
```