import socket
import threading
from datetime import datetime # it shows the time information belong to your system
from time import sleep # just to improve readability of the program on console
import names # library for random name generation to use as a nickname
import keyboard # for getting keyboard input

host = 'localhost'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host, port))
server.listen()

clients = []
nicknames = []
private_chats = {}

# in periodic time slices(here it setted every 5 seconds), displays(monitors) the connection infos like client count, total messages
def display_info():
    while True:
        user_count = len(nicknames)
        if user_count >= 1: # if there is no client, meaningless to display information
            print("\n* There are", user_count, "active clients")
            with open("messages.txt", "r") as msg_file:
                print("* There are", msg_file.read().count("\n"), "total group chat messages processed") # counts how many lines are in messages.txt for the number of general messages
            with open("private_messages.txt", "r") as prv_file:
                print("* There are", prv_file.read().count("\n"), "total private chat messages processed") # counts how many lines are in private_messages.txt for private message count
            sleep(5)
            
# for the time information when logging and displaying the messages. 
def time(): 
    now = datetime.now()
    print(now)

# saves the clients group chat messages into the file "messages.txt". creates if there is no such a file
def chat_save(client, message):
    index = clients.index(client)
    nickname = nicknames[index]
    message_text = message.decode('utf-8')  
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("messages.txt", "a", encoding="utf-8") as msg_file:
        msg_file.write(f"{timestamp}: {message_text}\n") # nickname is included already in the message. therefore did not need to add client here again
        
'''       
# if user want to close the server, can press 'q'
def close_server():
    while True:
        if keyboard.is_pressed('q'): 
            print("Server clossing")
            
            for client in clients:
                client.close()
            server.close()
'''

# sends the messages to all the clients
def broadcast(message):
    for client in clients:
        client.send(message)
        
# directs the program with commands got from the clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == "/quit": # makes quit process for the client
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)  
                nicknames.remove(nickname)  
                client.close()  
                broadcast(f"{nickname} left the chat".encode('utf-8')) 
                print(f"{nickname} has closed the connection")
                break  
            
            elif message.decode('utf-8') == "/users": # user want to see all active users, so sends the elements of list nicknames
                users_list = "\n".join(nicknames)
                client.send(f"{users_list}".encode('utf-8'))      
                continue 
            
            elif message.decode('utf-8') == "/exit":
                if client in private_chats:
                    partner = private_chats[client]
                    del private_chats[client]
                    del private_chats[partner]
                    client.send("Private chat has closed".encode('utf-8'))
                    partner.send("The other client has closed the private chat.".encode('utf-8'))
                continue 
            
            elif message.decode('utf-8').startswith("/pm "):
                target_name = message.decode('utf-8').split("/pm ")[1].strip()
                if target_name in nicknames:
                    target_index = nicknames.index(target_name)
                    target_client = clients[target_index]
                    private_chats[client] = target_client
                    private_chats[target_client] = client
                    sender_name = nicknames[clients.index(client)]
                    client.send(f"* Private messaging started with {target_name}\n* You can enter '/exit' to close the private messaging".encode('utf-8'))
                    target_client.send(f"* {sender_name} has started the private messaging\n* You can enter '/exit' to close the private messaging".encode('utf-8'))
                else:
                    client.send("There is no such a user".encode('utf-8'))
                continue  
            
            elif client in private_chats:
                sender_name = nicknames[clients.index(client)]
                target = private_chats[client]
                receiver_name = nicknames[clients.index(target)]
                timestamp = datetime.now().strftime("[%H:%M:%S]")
                msg = f"[Private] {timestamp} {sender_name}: {message.decode('utf-8')}"

                target.send(msg.encode('utf-8'))
                client.send(f"[Private to {receiver_name}] {timestamp} {sender_name}: {message.decode('utf-8')}".encode('utf-8'))

                with open("private_messages.txt", "a", encoding="utf-8") as prv_file:
                    prv_file.write(f"{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} {sender_name} - {receiver_name}: {message.decode('utf-8')}\n")
                continue
                
            broadcast(message) # if it is not the spesific commands, send all the client the messages
            chat_save(client, message) # save them into txt file
            
        except:
            if client in clients:
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                nicknames.remove(nickname)
                if client in private_chats:
                    partner = private_chats[client]
                    del private_chats[partner]
                    del private_chats[client]
                    partner.send("User has left the private messaging".encode('utf-8'))
                client.close()
                broadcast(f"{nickname} left the chat!".encode('utf-8'))
            break
 
# client connection and nickname assignment       
def receive():
    while True:
        client, address = server.accept()
        print("Connected with", str(address))
        
        client.send('NICK'.encode('utf-8')) # sends NICK to client to make client aware of that nickname is sended
        nickname = client.recv(1024).decode('utf-8')
        
        if nickname not in nicknames:
            nicknames.append(nickname)
            clients.append(client)  
        
        else:
            nickname = names.get_first_name()
            client.send(f'NICK_CHANGE:{nickname}'.encode('utf-8')) # sends NICK_CHANGE to client to make client aware of that nickname is already in use so differnt nickname assigned
            
            nicknames.append(nickname)
            clients.append(client) 

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('utf-8'))
        client.send('Connected to the server'.encode('utf-8'))
        
        # starting the server thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
   
if __name__ == "__main__":  
    print("* Server has started to listening")
    sleep(1)
    #print("You can press 'q' to stop the server whenever you want")
    
    info_thread = threading.Thread(target=display_info, daemon=True) # main function of the server starts as a thread, so the monitoring the info part also starts working as a thread 
    info_thread.start()
    
    #close_thread = threading.Thread(target=close_server, daemon=True)
    #close_thread.start()
    
    receive()