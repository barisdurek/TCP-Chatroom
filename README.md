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

## Running the program
### Needed installations before using:
#### pip install names
* For random name generation, used the library 'names'. 
* In project, client enters a nickname. If it is taken, server assigns a random nickname to this client.

#### pip install keyboard
* I didn't prefer user to press enter for an input. Therefore with this library, if the server user want to close server, just need to press 'q' on keyboard.
<br>
  
* To run the program, just start the server and then start the clients. Program files don't get any additional arguments.
First run the server:
```
python server.py
py server.py
```
and then the client:
```
python client.py
py server.py
```
* And these are what you should see in the console when the programs run:
![Ekran görüntüsü 2025-04-22 163706](https://github.com/user-attachments/assets/3cdf68d9-77b4-40a1-b223-3f5ba6898b70)
![Ekran görüntüsü 2025-04-22 163740](https://github.com/user-attachments/assets/9283c8d1-5798-4345-abfb-2ca3b31601d9)
![Ekran görüntüsü 2025-04-22 163753](https://github.com/user-attachments/assets/566fece3-f872-4bd0-b811-14c69a7081da)
![Ekran görüntüsü 2025-04-22 163805](https://github.com/user-attachments/assets/d68fc5a8-fccc-4aed-b7d8-ec3c2ece0449)
