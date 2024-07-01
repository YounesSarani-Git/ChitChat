import random
from cluster import hosts

# Function to start the leader election process
def start_leader_election(server_list, myIP):
    try:
        # Exclude the current leader from the election
        server_list.remove(hosts.current_leader)
    except ValueError:
        pass
    
    try:
        my_index = server_list.index(myIP)
        if my_index < len(server_list) - 1:
            return server_list[my_index + 1]
        else:
            return server_list[0]
    except ValueError:
        return random.choice(server_list)
