def get_hash_value (curr_state):
    hash_value = 0
    for i in range(3):
        for j in range(3):
            hash_value = hash_value*10 + curr_state[i][j]
        
    return hash_value

def compute_manhattan_distance(curr_state, gaol_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            found = False
            for m in range(3):
                for n in range(3):
                    if gaol_state[i][j] == curr_state[i][j]:
                        distance += abs(i-m) + abs(j-n)
                        found = True
                        break
                if found:
                    break
            
    return distance
                        