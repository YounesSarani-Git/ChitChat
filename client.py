import socket
import threading
import os
from time import sleep
from cluster import hosts, ports, send_multicast

# Create a new thread and start it
def create_and_start_thread(target, args):
    new_thread = threading.Thread(target=target, args=args)
    new_thread.daemon = True  # Daemon threads exit when the main program exits
    new_thread.start()

# Function to send messages to the server
def send_messages_to_server():
    global sock 
    while True:
        message = input("Type your message: ")  # Read message from user
        try:
            sock.send(message.encode(hosts.unicode))  # Send message to the server
        except Exception as e:
            print(f"Error while sending message: {e}")
            break

# Function to receive messages from the server
def receive_messages_from_server():
    global sock  
    while True:
        try:
            received_data = sock.recv(hosts.buffer_size)  # Receive data from the server
            if received_data:
                print(received_data.decode(hosts.unicode))  # Print the received message
            else:
                print("\nServer closed. Please try again later.")
                sock.close()
                establish_connection_to_server_leader()  # Reconnect to the server leader
                break
        except Exception as e:
            print(f"Server closed unexpectedly. Please try again later. Error: {e}")
            sock.close()
            establish_connection_to_server_leader()  # Reconnect to the server leader
            break

# Function to establish a connection to the server leader
def establish_connection_to_server_leader():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_exists = send_multicast.send_join_request_to_chat_server()  # Check if server exists
    if server_exists:
        server_leader_address = (hosts.current_leader, ports.server_port)
        print(f'The Server Leader is: {server_leader_address}')
        sock.connect(server_leader_address)  # Connect to the server leader
        sock.send('JOIN'.encode(hosts.unicode))  # Send JOIN message to the server
        print("You have joined the ChitChat Room.\nYou can start chatting.")
    else:
        print("Please try joining the ChitChat Room again later.")
        os._exit(0)

# Main function
if __name__ == '__main__':
    establish_connection_to_server_leader()  # Establish initial connection
    create_and_start_thread(send_messages_to_server, ())  # Start sending thread
    create_and_start_thread(receive_messages_from_server, ())  # Start receiving thread
    while True:
        sleep(1)  # Keep the main thread alive
