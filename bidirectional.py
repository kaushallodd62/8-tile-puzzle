from copy import deepcopy
from utility import *

class Bi_Directional_Search:
    # Constructor
    def __init__ (self):
        # initial and goal state
        self.initial_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

        # current state of forward motion and backward motion
        self.curr_state_forward = []
        self.curr_state_backward = []

        # path from src and dest to intersecting node
        self.src_path = []
        self.dest_path = []

        # fringe lists (stores state, mahattan_distance, parent hash value)
        self.src_fringe = {}
        self.dest_fringe = {}

        # expanded lists
        self.src_expanded = {}
        self.dest_expanded = {}

        # storing hash value of initial and goal state
        self.initial_state_hash_value = -1
        self.goal_state_hash_value = -1

        # stores the hash value of the intersecting node
        self.intersecting_node_hash_value = []

    # Prompting the user to input initial state
    def input_initial_state(self):
        print("8-tile Puzzle Solver")
        print("Input the intial state 2D matrix. Use 0 as blank")
        for i in range(3):
            self.initial_state[i][0], self.initial_state[i][1], self.initial_state[i][2] = map(int, input().split())
        if self.validate_initial_state():
            self.initial_state_hash_value = get_hash_value(self.initial_state)
            self.goal_state_hash_value = get_hash_value(self.goal_state)
            return True
        else:
            return False
        
    def validate_initial_state(self):
        initial_state = []
        for i in range(3):
            for j in range(3):
                initial_state.append(self.initial_state[i][j])

        # checking if there are unique values in the matrix
        if len(set(initial_state)) != 9:
            print("Please provide unique numbers from 1 to 8 (inclusive)")
            return False
        
        # checking if the number of inversions is even
        inversions = 0
        for i in range(9):
            for j in range(i+1, 9):
                if initial_state[i] != 0 and initial_state[j] != 0 and initial_state[i] > initial_state[j]:
                    inversions += 1 
        if inversions%2 != 0:
            print("Number of inversions is odd. Please provide valid initial state")
            return False

        return True
    
    def search(self):
        self.curr_state_forward = deepcopy(self.initial_state)
        self.curr_state_backward = deepcopy(self.goal_state)

        self.src_fringe[get_hash_value(self.curr_state_forward)] = [self.curr_state_forward, compute_manhattan_distance(self.curr_state_forward, self.goal_state), -1]
        self.dest_fringe[get_hash_value(self.curr_state_backward)] = [self.curr_state_backward, compute_manhattan_distance(self.curr_state_backward, self.initial_state), -1]

        while not self.intersecting_nodes():

            # perform forward search
            self.expand_forward()
            self.change_forward_state()

            # perform backward search
            self.expand_backward()
            self.change_backward_state()
        
        self.print_path()

    def intersecting_nodes(self):
        found = False

        for forward_node in self.src_expanded.keys():
            if forward_node in self.dest_expanded.keys():
                self.intersecting_node_hash_value = forward_node
                found = True
                break

        return found
    
    # expands curr_state_forward
    def expand_forward(self):
        # Finding the position of 0 (blank cell)
        xpos, ypos = -1, -1
        found = False
        for i in range(3):
            for j in range(3):
                if self.curr_state_forward[i][j] == 0:
                    xpos = i
                    ypos = j
                    found = True
                    break
            if found:
                break
        
        curr_hash_value = get_hash_value(self.curr_state_forward)

        # Blank moves up
        if xpos != 0:
            new_state = deepcopy(self.curr_state_forward)
            # swapping blank with cell on top
            new_state[xpos][ypos], new_state[xpos-1][ypos] = new_state[xpos-1][ypos], new_state[xpos][ypos]

            new_hash_value = get_hash_value(new_state)

            if new_hash_value not in self.src_expanded:
                self.src_fringe[new_hash_value] = [deepcopy(new_state), compute_manhattan_distance(new_state, self.goal_state), curr_hash_value]
        
        # Blank goes right
        if ypos != 2:
            new_state = deepcopy(self.curr_state_forward)
            # swapping blank with cell on the right
            new_state[xpos][ypos], new_state[xpos][ypos+1] = new_state[xpos][ypos+1], new_state[xpos][ypos]

            new_hash_value = get_hash_value(new_state)

            if new_hash_value not in self.src_expanded:
                self.src_fringe[new_hash_value] = [deepcopy(new_state), compute_manhattan_distance(new_state, self.goal_state), curr_hash_value]
            
        # Blank goes down
        if xpos != 2:
            new_state = deepcopy(self.curr_state_forward)
            # swapping blank with cell on top
            new_state[xpos][ypos], new_state[xpos+1][ypos] = new_state[xpos+1][ypos], new_state[xpos][ypos]

            new_hash_value = get_hash_value(new_state)

            if new_hash_value not in self.src_expanded:
                self.src_fringe[new_hash_value] = [deepcopy(new_state), compute_manhattan_distance(new_state, self.goal_state), curr_hash_value]
            
         # Blank goes left
        if ypos != 0:
            new_state = deepcopy(self.curr_state_forward)
            # swapping blank with cell on the right
            new_state[xpos][ypos], new_state[xpos][ypos-1] = new_state[xpos][ypos-1], new_state[xpos][ypos]

            new_hash_value = get_hash_value(new_state)

            if new_hash_value not in self.src_expanded:
                self.src_fringe[new_hash_value] = [deepcopy(new_state), compute_manhattan_distance(new_state, self.goal_state), curr_hash_value]
            
        # insert into expanded list
        self.src_expanded[get_hash_value(self.curr_state_forward)] = [deepcopy(self.curr_state_forward), self.src_fringe[get_hash_value(self.curr_state_forward)][2]]
        # delete from fringe list
        del self.src_fringe[get_hash_value(self.curr_state_forward)]

    # assigning curr_state_forward to the closest state in the fringe list
    def change_forward_state(self):
        closest_state_hash_value = -1
        min_manhattan_distance = 999999
        
        for i in self.src_fringe:
            if self.src_fringe[i][1] < min_manhattan_distance:
                min_manhattan_distance = self.src_fringe[i][1]
                closest_state_hash_value = i
            
        self.curr_state_forward = deepcopy(self.src_fringe[closest_state_hash_value][0])

    # expands curr_state_backward
    def expand_backward(self):
        # Finding the position of 0 (blank cell)
        xpos, ypos = -1, -1
        found = False
        for i in range(3):
            for j in range(3):
                if self.curr_state_backward[i][j] == 0:
                    xpos = i
                    ypos = j
                    found = True
                    break
            if found:
                break
        
        curr_hash_value = get_hash_value(self.curr_state_backward)

        # Blank moves up
        if xpos != 0:
            new_state = deepcopy(self.curr_state_backward)
            # swapping blank with cell on top
            new_state[xpos][ypos], new_state[xpos-1][ypos] = new_state[xpos-1][ypos], new_state[xpos][ypos]

            new_hash_value = get_hash_value(new_state)

            if new_hash_value not in self.dest_expanded:
                self.dest_fringe[new_hash_value] = [deepcopy(new_state), compute_manhattan_distance(new_state, self.goal_state), curr_hash_value]
        
        # Blank goes right
        if ypos != 2:
            new_state = deepcopy(self.curr_state_backward)
            # swapping blank with cell on the right
            new_state[xpos][ypos], new_state[xpos][ypos+1] = new_state[xpos][ypos+1], new_state[xpos][ypos]

            new_hash_value = get_hash_value(new_state)

            if new_hash_value not in self.dest_expanded:
                self.dest_fringe[new_hash_value] = [deepcopy(new_state), compute_manhattan_distance(new_state, self.goal_state), curr_hash_value]
            
        # Blank goes down
        if xpos != 2:
            new_state = deepcopy(self.curr_state_backward)
            # swapping blank with cell on top
            new_state[xpos][ypos], new_state[xpos+1][ypos] = new_state[xpos+1][ypos], new_state[xpos][ypos]

            new_hash_value = get_hash_value(new_state)

            if new_hash_value not in self.dest_expanded:
                self.dest_fringe[new_hash_value] = [deepcopy(new_state), compute_manhattan_distance(new_state, self.goal_state), curr_hash_value]
            
         # Blank goes left
        if ypos != 0:
            new_state = deepcopy(self.curr_state_backward)
            # swapping blank with cell on the right
            new_state[xpos][ypos], new_state[xpos][ypos-1] = new_state[xpos][ypos-1], new_state[xpos][ypos]

            new_hash_value = get_hash_value(new_state)

            if new_hash_value not in self.dest_expanded:
                self.dest_fringe[new_hash_value] = [deepcopy(new_state), compute_manhattan_distance(new_state, self.goal_state), curr_hash_value]
            
        # insert into expanded list
        self.dest_expanded[get_hash_value(self.curr_state_backward)] = [deepcopy(self.curr_state_backward), self.dest_fringe[get_hash_value(self.curr_state_backward)][2]]
        # delete from fringe list
        del self.dest_fringe[get_hash_value(self.curr_state_backward)]

    # assigning curr_state_backward to the closest state in the fringe list
    def change_backward_state(self):
        closest_state_hash_value = -1
        min_manhattan_distance = 999999
        
        for i in self.dest_fringe:
            if self.dest_fringe[i][1] < min_manhattan_distance:
                min_manhattan_distance = self.dest_fringe[i][1]
                closest_state_hash_value = i
            
        self.curr_state_forward = deepcopy(self.dest_fringe[closest_state_hash_value][0])
    
    # prints the solution path
    def print_path(self):
        # backtracking and storing src path
        hash_value = self.intersecting_node_hash_value
        while hash_value != -1:
            self.src_path.append(self.src_expanded[hash_value])
            hash_value = self.src_expanded[hash_value][1]

        # backtracking and storing dest path
        hash_value = self.intersecting_node_hash_value
        while hash_value != -1:
            self.dest_path.append(self.dest_expanded[hash_value])
            hash_value = self.dest_expanded[hash_value][1]
        
        # print src path
        for i in self.src_path.reverse():
            print(i)
        
        # print dest path
        for i in self.dest_path[1:]:
            print(i)

        
if __name__ == '__main__':
    obj = Bi_Directional_Search()
    if obj.input_initial_state():
        obj.search()
