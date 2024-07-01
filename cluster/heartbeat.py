import socket
import sys
from time import sleep
from cluster import hosts, ports, leader_election, send_multicast

# Function to send heartbeat signals to the current leader
def send_heartbeat():
    while True:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5)

        # Check the current leader
        host_address = (hosts.current_leader, ports.server_port)

        # Wait 5 seconds before sending the heartbeat signal
        sleep(0.5)

        # Try to connect to the leader to send the heartbeat signal
        try:
            sock.connect(host_address)
            #print(f'[HEARTBEAT] Reply from Leader {hosts.current_leader}', file=sys.stderr)

        except:
            print(f'[HEARTBEAT] Leader {hosts.current_leader} failed', file=sys.stderr)
            hosts.is_leader_crashed = True
            # Start leader election
            new_leader = leader_election.start_leader_election(hosts.server_list, hosts.myIP)
            hosts.current_leader = new_leader
            hosts.has_network_changed = True
            print(f'[HEARTBEAT] New Leader is {hosts.current_leader}', file=sys.stderr)
            # Send multicast message about new leader
            send_multicast.send_update_to_multicast_group()

        finally:
            sock.close()
