import socket
import threading
from time import sleep # just to improve readability of the program on console
from datetime import datetime # it shows the time information belong to your system

host = 'localhost'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# gets the messages from server
def receive():
    global nickname
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK': # get the nickname
                client.send(nickname.encode('utf-8'))
            
            elif message.startswith('NICK_CHANGE:'): # if the nickname is already given, notify the client about new nickname
                nickname = message.split(':')[1].strip()
                print(f"Entered nickname is in use. Therefore your nickname is: {nickname}")  
            
            else: # if the message is other than nickname part, show on the console
                print(f"{datetime.now().strftime("[%H:%M:%S]")} {message}")
                
        except:
            client.close()
            break

# sends the messages to the server
def write():
    while True:
        msg = input("")  
        if msg == "/quit": # user want to quit the program       
            client.send("/quit".encode('utf-8'))
            client.close()
            break
        
        elif msg == "/users": # user want to see all active users, then can pick one of them for private messaging
            client.send("/users".encode('utf-8'))
            continue
        
        elif msg.startswith("/pm ") or msg == "/exit":
            client.send(msg.encode('utf-8'))
            continue 
        
        else:
            message = f"{nickname}: {msg}"  
            client.send(message.encode('utf-8'))

# main for getting nickname from user and starting threads
def main():
    global nickname  
    nickname = input("Enter your nickname: ") 
    
    client.connect((host, port))
    
    # starts as two different threads, one for sending and another one for receiving messages 
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

if __name__ == "__main__":
    # interface to inform user about how to use the program
    print("Welcome to the chat application")
    sleep(1)
    print("* You can enter the message '/quit' to end the connection")
    sleep(1)
    print("* You can enter '/users' to look at the list of active users")
    sleep(1)
    print("* You can enter '/pm' and then enter the name that you want private messaging\n(for example '/pm Barış' to start private messaging with the client that have the nickname 'Barış')")
    sleep(1)
    print("* You can also close the private message part by entering '/exit' and return back to group chatting")
    sleep(1)
    main()