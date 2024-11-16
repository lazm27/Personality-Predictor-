import socket
from threading import Thread
import re
import sqlite3
import subprocess
# Connect to SQLite database

subprocess.run(['python', 'delete.py'])

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
def create_connection():
    return sqlite3.connect('datasets/messages.db')
def listen_for_client(cs):
    conn = create_connection()
    cursor = conn.cursor()
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
# Run the second Python file
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
            sender, message = msg.split(": ", 1)
            dt, name= sender.split("]", 1)

            #pattern = r"\[(.*?)\]"
            clean_message = re.sub(r'.?\[.*$', '', message)
            print(dt)
            # Find all matches of the pattern in the text
            #matches = re.findall(pattern, dt)
            #for match in matches:
            #    dt=match
            #print(dt)
            #print(name.strip())
            #print(message)
            timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
            match = re.search(timestamp_pattern, dt)
            
            cursor.execute('''INSERT INTO messages (datetime, user_name, message_content)
                      VALUES (?, ?, ?)''', (match.group(0), name.strip().lower(), clean_message))

            # Commit changes and close the connection
            conn.commit()
            
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())
    cursor.close()
    conn.close()

while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
        # close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
