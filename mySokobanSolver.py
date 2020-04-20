
'''

    2020 CAB320 Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.


You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and results in a fail for the test of your code.
This is not negotiable! 


'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban

import math

from sokoban import Warehouse
# Checking if I can edit.
from search import astar_graph_search as astar_graph
from sokoban import find_2D_iterator

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
convert_2d_array converts warehouse to 2d array
params
warehouse = a warehouse object
'''
def convert_2d_array(warehouse):
    # get string representation
    warehouse_str = str(warehouse)
    # convert warehouse string into 2D array
    warehouse_2d = [list(line) for line in warehouse_str.split('\n')]
    # convert 2D array back into string
    #warehouse_str = '\n'.join([''.join(line) for line in warehouse_2d])
    return warehouse_2d
    
def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the puzzle with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE"
    #raise NotImplementedError

    #scan offset walls for rows
    #used in rule 2 to see if to connect taboo cells
    #params
    #warehouse_array = 2d array of warehouse
    #x1, x2 = x locations to scan to
    #y = collum scan takes place on
    def scan_offset_wall_x(warehouse_array, x1, x2, y):
        top = 0
        down = 0
        for i in range(x1+1,x2-1):
            if(warehouse_array[y][i] != ' '):
                return False
            if warehouse_array[y+1][i] != '#':
                down = 1
                #print("down "+str(i)+' '+str(y))
            if warehouse_array[y-1][i] != '#':
                top = 1
                #print("top "+str(i)+' '+str(y))
            if(top == 1):
                if(down == 1):
                    #print("here")
                    return False
                 
        for i in range(x1,x2):
            #print(str(i)+' '+str(y))
            if(warehouse_array[y+1][i] != '#' and warehouse_array[y-1][i] != '#'):
                return False
        #print("end")
        return True
    #scan offset walls for collumns
    #used in rule 2 to see if to connect taboo cells
    #params
    #warehouse_array = 2d array of warehouse
    #y1, y2 = y locations to scan to
    #x = row scan takes place on
    def scan_offset_wall_y(warehouse_array, y1, y2, x):
        right = 0
        left = 0
        #print("offset start "+str(y1)+' '+str(y2)+' '+str(x))
        for i in range(y1+1,y2-1):
            if(warehouse_array[i][x] != ' '):
                return False
            if warehouse_array[i][x+1] != '#':
                right = 1
                #print("right "+str(i)+' '+str(x))
            if warehouse_array[i][x-1] != '#':
                left = 1
                #print("left "+str(i)+' '+str(x))
            if(right == 1):
                if(left == 1):
                    #print("here")
                    return False
        for i in range(y1,y2):
            #print(str(i)+' '+ str(x))
            if(warehouse_array[i][x+1] != '#' and warehouse_array[i][x-1] != '#'):
                return False
        #print("end")    
        return True
    #rule 1 scan for corner cells
    #params
    #warehouse_2d = a 2d array of warehouse
    def Taboo_rule_1(warehouse_2d):
        #apply rule 1 - mark corner taboo cells
        for y in range(len(warehouse_2d)-1):
            temp = 0 # used to find wall_start and end
            wall_count = 0 #used to keep track of index
            wall_start = 0#1st wall on x axis
            wall_end = 0#last wall on x axis
            wall_start_y = 0#1st wall on y axis
            wall_end_y = 0#last wall on y axis
            
            for x in range(len(warehouse_2d[y])):
                #set wall start and end on x axis
                temp = temp +1#temperary varable to find start and end wall
                if warehouse_2d[y][x] == '#':
                    wall_end = temp+1
                if warehouse_2d[y][x] == '#' and wall_start == 0:
                    wall_start = temp
                
            for x in range(len(warehouse_2d[y]) - 1):
                wall_start_y = -1
                wall_end_y = 0
                for y2 in range(len(warehouse_2d)):
                    #set wall start and end on y axis
                    if warehouse_2d[y2][x] == '#':
                        wall_end_y = y2
                    if warehouse_2d[y2][x] == '#' and wall_start_y == -1:
                        wall_start_y = y2
                wall_count = wall_count + 1
                if is_corner_cell(warehouse_2d, x, y) == True:
                    #print taboo cells and check if between first and last of each wall
                    if warehouse_2d[y][x] != '#' or 'X' or '.' or '!' or '*':
                        #print(str(wall_start_y)+' '+str(wall_end_y)+' '+str(x))
                        if wall_start >= wall_count:
                            pass
                        elif wall_end <= wall_count:
                            pass
                        elif wall_start_y > y:
                            pass
                        elif wall_end_y < y:
                            pass
                        else:
                            warehouse_2d[y][x] = taboo
        return warehouse_2d
    #connect taboo cells from rule 1 if applicable
    #params
    #warehouse_2d = a 2d array of warehouse
    def Taboo_rule_2(warehouse_2d):
        #apply rule 2 
        for y in range(len(warehouse_2d)):
            #check x axis points 
            temp_taboo_x1 = 0#used to hold tabbo cell locations that are being checked
            temp_taboo_x2 = 0
            temp_taboo_y1 = 0
            temp_taboo_y2 = 0
            for x in range(len(warehouse_2d[y])):
                if warehouse_2d[y][x] == taboo and temp_taboo_x1 == 0:
                    temp_taboo_x1 = x
                    temp_taboo_y1 = y
                elif warehouse_2d[y][x] == taboo and temp_taboo_x1 != 0:
                    temp_taboo_x2 = x                  
                if temp_taboo_x1 != 0 and temp_taboo_x2 !=0:
                    if(scan_offset_wall_x(warehouse_2d, temp_taboo_x1, temp_taboo_x2, y)):
                        for i in range(temp_taboo_x1, temp_taboo_x2):
                            if(warehouse_2d[y][i] == ' '):    
                                warehouse_2d[y][i] = taboo_temp
                    temp_taboo_x1 = 0
                    temp_taboo_x2 = 0

        for x in range(len(warehouse_2d[y])):
            #check y axis points 
            temp_taboo_x1 = 0#used to hold tabbo cell locations that are being checked
            temp_taboo_x2 = 0
            temp_taboo_y1 = 0
            temp_taboo_y2 = 0
            for y in range(len(warehouse_2d)):
                if warehouse_2d[y][x] == taboo and temp_taboo_y1 == 0:
                    temp_taboo_x1 = x
                    temp_taboo_y1 = y
                elif warehouse_2d[y][x] == taboo and temp_taboo_y1 != 0:
                    temp_taboo_y2 = y                  
                if temp_taboo_y1 != 0 and temp_taboo_y2 !=0:
                    if(scan_offset_wall_y(warehouse_2d, temp_taboo_y1, temp_taboo_y2, x)):
                        for i in range(temp_taboo_y1+1, temp_taboo_y2):
                            #print(str(i))
                            if(warehouse_2d[i][x] == ' '):
                                warehouse_2d[i][x] = taboo_temp
                    temp_taboo_y1 = 0
                    temp_taboo_y2 = 0    
        return warehouse_2d
            
    #check if corner cell
    #params
    #warehouse_array = 2d array of warehouse
    #x = target collum location
    #y = target row location
    def is_corner_cell(warehouse_array, x, y):
        #check if cell is in corner
        if warehouse_array[y][x] == '#':
            return False
        if warehouse_array[y][x] == ' ':
            up = 0
            down = 0
            left = 0
            right = 0
            if warehouse_array[y - 1][x] == '#':
                up = 1
            if warehouse_array[y + 1][x] == '#':
                down = 1
            if warehouse_array[y][x + 1] == '#':
                right = 1
            if warehouse_array[y][x - 1] == '#':
                left = 1
            #if up + right == 2 or up + left == 2 or down + right == 2 or down + left:
            if up + left >= 2:
                return True
            elif down + right >= 2:
                return True
            elif down + left >= 2:
                return True
            elif up + right >= 2:
                return True
            else:
                return False
    # some constants
    squares_to_remove = ['$', '@']
    target_squares = ['.', '!', '*']
    wall = '#'
    taboo = 'X'
    taboo_temp = 'x'#used to determine cells that are taboo but done need to have calculations applied 
    # get string representation
    warehouse_str = str(warehouse)
    # remove objects that aren't walls or targets
    for char in squares_to_remove:
        warehouse_str = warehouse_str.replace(char, ' ')
    # convert warehouse string into 2D array
    warehouse_2d = [list(line) for line in warehouse_str.split('\n')]
    # 1 corner squares == taboo
    warehouse_2d = Taboo_rule_1(warehouse_2d)            
    # 2 tabbo squares == edges that dont indent
    warehouse_2d = Taboo_rule_2(warehouse_2d)
    #convert taboo temp to taboo
    for char in squares_to_remove:
        warehouse_str = warehouse_str.replace(char, ' ')                                  
    # convert 2D array back into string
    warehouse_str = '\n'.join([''.join(line) for line in warehouse_2d])
    # remove the remaining target_squares
    for char in target_squares:
        warehouse_str = warehouse_str.replace(char, ' ')
    #covert taboo temp to taboo
    for char in taboo_temp:
        warehouse_str = warehouse_str.replace(char, taboo)
    return warehouse_str
    #function still might include cells outside warehouse if there is no
    #direct line of sight to outside/or unwalled direction
    


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    
    def __init__(self, warehouse,macro,taboo):
        self.warehouse = warehouse
        self.initial = warehouse
        self.macro = macro
        # specify the goal
        warehouse_string = str(warehouse)
        self.goal = warehouse_string.replace("$", " ").replace(".", "*").replace("@", " ")
        #self.goal = warehouse.goal

        #specify if to calculate taboo cells
        self.allow_taboo_push = taboo

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        # Extract the warehouse
        current_warehouse = sokoban.Warehouse()
        warehouse_str = str(state)
        current_warehouse.extract_locations(warehouse_str.split(sep="\n"))
        
        # If taboo cells haven't been computed, compute them.
        warhouse_list = taboo_cells(current_warehouse).split("\n")
        bad_cells = None
        up = "up"
        down = "down"
        left = "left"
        right = "right"
        offset_states = [(-1, 0), (1, 0), (0, -1), (0, 1)]#left right up down
        possible_actions = []
        if self.allow_taboo_push == True:
            if bad_cells is None:
                bad_cells = set(find_2D_iterator(warhouse_list, "X"))
        else:
            bad_cells = None
        
        # Find every box, and every direction it can be pushed.
            #cant be taboo cells
            #walls
            #another box
            #player can reach box
            #return list of possible actions in current state
            # could use a .append like in sliding puzzel
            # return list of this format((3,4),'Left')
        if self.macro == True:
            for box in current_warehouse.boxes:
                for offset in offset_states:
                    push_loc = []#location of player if a push is to happen
                    for i in range(0, len(box)):
                        push_loc.append(box[i] + offset[i])
                    if push_loc != bad_cells:
                        if push_loc !=  current_warehouse.walls:
                            if push_loc != current_warehouse.boxes:
                                #if can_go_there(current_warehouse, push_loc):
                                if True:
                                    if(offset == (-1,0)):
                                        possible_actions.append([box,left])
                                    if(offset == (1,0)):
                                        possible_actions.append([box,right])
                                    if(offset == (0,-1)):
                                        possible_actions.append([box,up])
                                    if(offset == (0,1)):
                                        possible_actions.append([box,down])
                                    #print(str(possible_actions)+"  possible actions")

            print(str(possible_actions)+"  possible actions")
            print("____________")
        elif self.macro == False:
            for players in current_warehouse.worker:
                for offset in offset_states:
                    push_loc = []#location of player if a push is to happen
                    for i in range(0, len(players)):
                        push_loc.append(players[i] + offset[i])
                    if push_loc != bad_cells:
                        if push_loc !=  current_warehouse.walls:
                            if push_loc != current_warehouse.boxes:
                                if(offset == [-1,0]):
                                    possible_actions.append([left])
                                if(offset == [1,0]):
                                    possible_actions.append([right])
                                if(offset == [0,-1]):
                                    possible_actions.append([up])
                                if(offset == [0,1]):
                                    possible_actions.append([down])
        elif self.macro == None:
            print(str("something went wrong/self.macro doesnt work the way i think"))
                        

        
        return possible_actions
        #raise NotImplementedError
    
##    def result(self, state, action):
##        print("---result-----")
##        print(str(state))
##        print(str(action))
##        # Extract the warehouse state space
##        state_space = sokoban.Warehouse()
##        warehouse_str = str(state)
##        state_space.extract_locations(warehouse_str.split(sep="\n"))
##        box_loc = action[0]
##        if box_loc in state_space.boxes:
##            if action[1] == 'Right':
##                move = 1, 0
##                state_space.worker = box_loc
##                state_space.boxes.remove(box_loc)
##                state_space.boxes.append(box_loc[0] + move[0], box_loc[1] + move[1])
##                return action, str(state_space)
##            if action[1] == 'Left':
##                move = -1, 0
##                state_space.worker = box_loc
##                state_space.boxes.remove(box_loc)
##                state_space.boxes.append(box_loc[0] + move[0], box_loc[1] + move[1])
##                return action, str(state_space)
##            if action[1] == 'Up':
##                move = 0, -1
##                state_space.worker = box_loc
##                state_space.boxes.remove(box_loc)
##                state_space.boxes.append(box_loc[0] + move[0], box_loc[1] + move[1])
##                return action, str(state_space)
##            if action[1] == 'Down':
##                move = 0, 1
##                state_space.worker = box_loc
##                state_space.boxes.remove(box_loc)
##                state_space.boxes.append(box_loc[0] + move[0], box_loc[1] + move[1])
##                return action, str(state_space)
##            else:
##                return ('No Action')
##        else:
##            return ('Error')
    def result(self, state, action):
        print("---result-----")
        print(str(state))
        print(str(action))
        # Extract the warehouse
        current_warehouse = sokoban.Warehouse()
        warehouse_str = str(state)
        current_warehouse.extract_locations(warehouse_str.split(sep="\n"))
        
        box = action[0]
        if box in current_warehouse.boxes:
            # Remove the old box, set the worker to the position, and add the
            # new box position. This moves the box with the worker.
            offset = "default"
            if action[1] == "left":
                offset = (-1,0)
            if action[1] == "right":
                offset = (1,0)
            if action[1] == "up":
                offset = (0,-1)
            if action[1] == "down":
                offset = (0,1)
            print(str(offset) +" offset test")
            current_warehouse.worker = box
            current_warehouse.boxes.remove(box)
            current_warehouse.boxes.append(add_tuples(box, offset))
            return offset, str(current_warehouse)
        raise NotImplementedError
    def goal_test(self, state):
        # Check that the state warehouse has all targets filled.
        return str(state) == self.goal
##
##    def value(self, state):
##        return 1  # Changes have a cost of 1

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE
    # Convert warehouse object to two-dimensional list
    warehouse_2d = convert_2d_array(warehouse)
    
    # Index (zero indexing) the position (column, row) of the worker ('@' or '!') in the warehouse  
    worker_col, worker_row = warehouse.worker # worker location to update
       
    # Remove worker to show natural state space
    if warehouse_2d[worker_row] [worker_col] == '!':
        warehouse_2d[worker_row] [worker_col] = '.'
    else:
        warehouse_2d[worker_row] [worker_col] = ' '

    # Index (zero indexing) the position (column, row) of the boxes ('$' or '*') in the warehouse
    box_locs = ((),)*len(warehouse.boxes)
    for box_loc in box_locs:
        box_locs = warehouse.boxes
                
    # Remove boxes to show natural state space
    for box_loc in box_locs:
        if warehouse_2d[box_loc[1]] [box_loc[0]] == '*':
            warehouse_2d[box_loc[1]] [box_loc[0]] = '.'
        else:
            warehouse_2d[box_loc[1]] [box_loc[0]] = ' '
    
    # Loop for action sequence  
    for i in range(len(action_seq)):   
    
        # Action 'right' = worker_loc [row, col+1]      
        if action_seq[i] == 'Right':   
            if (worker_col+1, worker_row) in warehouse.walls:
                return 'Impossible' # if "go to cell" is a wall - Impossible
            elif (worker_col+1, worker_row) in warehouse.boxes:
                if (worker_col+2, worker_row) not in warehouse.walls and (worker_col+2, worker_row) not in warehouse.boxes:
                    warehouse.boxes.remove((worker_col+1, worker_row))
                    warehouse.boxes.append((worker_col+2, worker_row))
                    worker_col += 1 # if "go to cell" is a box and "go to cell + 1" is not a wall or box - Legal move
                else:
                    return 'Impossible' # if "go to cell" is a box and "go to cell + 1" is a wall or a box - Impossible
            else:
                worker_col += 1 # if "go to cell" is not a wall and is not a box - Legal move
            
        # Action 'left' = worker_loc [row, col-1]             
        if action_seq[i] == 'Left':   
            if (worker_col-1, worker_row) in warehouse.walls:
                return 'Impossible' # if "go to cell" is a wall - Impossible
            elif (worker_col-1, worker_row) in warehouse.boxes:
                if (worker_col-2, worker_row) not in warehouse.walls and (worker_col-2, worker_row) not in warehouse.boxes:
                    warehouse.boxes.remove((worker_col-1, worker_row))
                    warehouse.boxes.append((worker_col-2, worker_row))
                    worker_col -= 1 # if "go to cell" is a box and "go to cell + 1" is not a wall or box - Legal move
                else:
                    return 'Impossible' # if "go to cell" is a box and "go to cell + 1" is a wall or a box - Impossible
            else:
                worker_col -= 1 # if "go to cell" is not a wall and is not a box - Legal move
            
        # Action 'up' = worker_loc [row-1, col]
        if action_seq[i] == 'Up':
            if (worker_col, worker_row-1) in warehouse.walls:
                return 'Impossible' # if "go to cell" is a wall - Impossible
            elif (worker_col, worker_row-1) in warehouse.boxes:
                if (worker_col, worker_row-2) not in warehouse.walls and (worker_col, worker_row-2) not in warehouse.boxes:
                    warehouse.boxes.remove((worker_col, worker_row-1))
                    warehouse.boxes.append((worker_col, worker_row-2))
                    worker_row -= 1 # if "go to cell" is a box and "go to cell + 1" is not a wall or box - Legal move 
                else:
                    return 'Impossible' # if "go to cell" is a box and "go to cell + 1" is a wall or a box - Impossible 
            else:
                worker_row -= 1 # if "go to cell" is not a wall and is not a box - Legal move
            
        # Action 'down' = worker_loc [row+1, col]         
        if action_seq[i] == 'Down':
            if (worker_col, worker_row+1) in warehouse.walls:
                return 'Impossible' # if "go to cell" is a wall - Impossible
            elif (worker_col, worker_row+1) in warehouse.boxes:
                if (worker_col, worker_row+2) not in warehouse.walls and (worker_col, worker_row+2) not in warehouse.boxes:
                    warehouse.boxes.remove((worker_col, worker_row+1))
                    warehouse.boxes.append((worker_col, worker_row+2))
                    worker_row += 1 # if "go to cell" is a box and "go to cell + 1" is not a wall or box - Legal move
                else:
                    return 'Impossible' # if "go to cell" is a box and "go to cell + 1" is a wall or a box - Impossible
            else:
                worker_row += 1 # if "go to cell" is not a wall and is not a box - Legal move
        
    # Update warehouse with new locations
                
    # If "go to cell" is legal AND "go to cell" == target square worker_loc = index of "go to cell" AND '!' 
    if warehouse_2d[worker_row] [worker_col] == '.':
        warehouse_2d[worker_row] [worker_col] = '!'
    else: # If "go to cell" is legal worker_loc = index of "go to cell"
        warehouse_2d[worker_row] [worker_col] = '@'
        
    # Populate box_locs with updated locations from warehouse.boxes
    for box_loc in box_locs: 
    # if box new location is a target square change * 
        if warehouse_2d[box_loc[1]] [box_loc[0]] == '.':
            warehouse_2d[box_loc[1]] [box_loc[0]] = '*'
        else: # if box new location is not a target square $
            warehouse_2d[box_loc[1]] [box_loc[0]] = '$'
    
    # Convert 2D array back into string
    warehouse_str = '\n'.join([''.join(line) for line in warehouse_2d])
    
    return warehouse_str
    
    


    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.
    
    In this scenario, the cost of all (elementary) actions is one unit.
    
    @param warehouse: a valid Warehouse object
    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    #macro = [((1, 3), 'Right'), ((1, 4), 'Right')] # List of macro actions
    #puzzle_t2 = ("<Node "+str(warehouse))
    #print(str(warehouse)+"\n_________")
    puzzle_t2 = (str(warehouse))
    wh = Warehouse()    
    wh.from_string(puzzle_t2)
    macro = solve_sokoban_macro(wh)
    #print(str(macro))
    
    warehouse_str = str(warehouse)
    goal_state = warehouse_str.replace("$", " ").replace(".", "*")
    elem_actions = [] # list of elementary actions
    
    # Check if already in goal state
    if warehouse_str == goal_state:
        return elem_actions
    
    if macro == 'Impossible':
        return 'Impossible'
    
    for path_step in macro:
        target_box = path_step[0]
        push_direction = path_step[1]
        if push_direction == 'Right':
            offset = (-1, 0)
        elif push_direction == 'Left':
            offset = (1, 0)
        elif push_direction == 'Up':
            offset = (0, 1)
        elif push_direction == 'Down':
            offset = (0, -1)    
        worker_pos = add_tuples(target_box, offset)
                            
        def h(n):
            state = n.state
            #print(str(state))
            current_warehouse = sokoban.Warehouse()
            #worker_pos = add_tuples(target, offset)
            warehouse_str = str(state)
            current_warehouse.extract_locations(warehouse_str.split(sep="\n"))
            h = 0
            for box in current_warehouse.boxes: #box
                
                h += math.sqrt(((worker_pos[1] - box[1])**2) + ((worker_pos[0] - box[0])**2))
            return h
                       
        frontier = search.astar_graph_search(macro_sokoban_test(wh), h)
        #print(str(frontier))
                                
        if frontier is None:
            return 'Impossible'
                               
        for node in frontier.path():
            if node.action == (0, 1):
                #direction = 'Down'
                elem_actions.append('Down')
            elif node.action == (0, -1):
                #direction = 'Up'
                elem_actions.append('Up')
            elif node.action == (1, 0):
                #direction = 'Right'
                elem_actions.append('Right')
            elif node.action == (-1, 0):
                #direction = 'Left'
                elem_actions.append('Left')
                                                    
        # add the actual push action
        elem_actions.append(push_direction)
                                               
        # move target box to new position
        
        warehouse.boxes.remove(flip_tuple(target_box))
            
        if push_direction == "Down":
            offset = (0, 1)
        elif push_direction == "Up":
            offset = (0, -1)
        elif push_direction == "Right":
            offset = (1, 0)
        elif push_direction == "Left":
            offset = (-1, 0)
        new_box_loc = add_tuples(flip_tuple(target_box), offset)
        warehouse.boxes.append(new_box_loc)
                                                                    
        # move worker to new position
        warehouse.worker = flip_tuple(target_box)
                                                                    
    return elem_actions

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

offset_states = [(-1, 0), (1, 0), (0, -1), (0, 1)]#left right up down in x,y form
#add elements of 2x1 list
#turple1/2 = 2x1 list to add
def add_tuples(tuple1, tuple2):
        return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]
#flip turple elements in 2x1 list
    #a = 2x1 list
def flip_tuple(a):
    return a[1], a[0]
    
class CGT_sokoban_test(search.Problem):
#class used to solve can go there function        
    def __init__(self, warehouse,dst):
        # Extract the warehouse
        current_warehouse = sokoban.Warehouse()
        warehouse_str = str(warehouse)
        current_warehouse.extract_locations(warehouse_str.split(sep="\n"))
        
        self.initial = current_warehouse.worker
        self.boxes = current_warehouse.boxes
        self.walls = current_warehouse.walls
        self.goal = dst
        self.warehouse = current_warehouse
        self.Pass = False
    #returns a list of possible actions
    def actions(self, state):
         possible_actions = []
         for offset in offset_states:
            new_state = add_tuples(state, offset)
            # Check that the location isn't a wall or box
            if new_state not in self.boxes:  #boxes
                if new_state not in self.walls: #wall
                    possible_actions.append(offset)
         return possible_actions
    def result(self, state, action):
        # The result is the old state, with the action applied.
        new_state = add_tuples(state, action)
        if new_state == self.goal :
            self.Pass = True
        return new_state
    def goal_test(self, state):
        #check if goal is reached/achieved
        if(state == flip_tuple(self.goal)):
            return True
        else:
            return False
        raise NotImplementedError()
    

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    # specify heuristic
    def h(n):
        state = n.state
        # distance = sqrt(xdiff^2 + ydiff^2). Basic distance formula heuristic.
        return math.sqrt(((state[1] - dst[1]) ** 2)
                         + ((state[0] - dst[0]) ** 2))
    # Extract the warehouse
    current_warehouse = sokoban.Warehouse()
    # get string representation
    warehouse_str = str(warehouse)
    current_warehouse.extract_locations(warehouse_str.split(sep="\n"))
    # execute a*_graph_search to solve the puzzle
    node = search.astar_graph_search(CGT_sokoban_test(current_warehouse,dst),h)
    # If a node was found, this is a valid destination
    if node == None:
        return False
    return True
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class macro_sokoban_test(search.Problem):
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.initial = warehouse
        # specify the goal
        warehouse_string = str(warehouse)
        self.goal = warehouse_string.replace("$", " ").replace(".", "*").replace("@", " ")
        self.path = []
    def actions(self, state):
        # Extract the warehouse
        current_warehouse = sokoban.Warehouse()
        warehouse_str = str(state)
        current_warehouse.extract_locations(warehouse_str.split(sep="\n"))
        
        # If taboo cells haven't been computed, compute them.
        warhouse_list = taboo_cells(current_warehouse).split("\n")
        bad_cells = None
        up = "Up"
        down = "Down"
        left = "Left"
        right = "Right"
        offset_states = [(-1, 0), (1, 0), (0, -1), (0, 1)]#left right up down
        possible_actions = []
        if bad_cells is None:
                bad_cells = set(find_2D_iterator(warhouse_list, "X"))
        else:
            bad_cells = None
        push_loc = []#location of player if a push is to happen
        #find all pish locations 
        for box in current_warehouse.boxes:
            for offset in offset_states:
                push_loc.append((add_tuples(box, offset),box,offset))
        #check cells at push location
        for element in push_loc:      
            if element[0] not in bad_cells:#taboo cells
                if element[0] not in  current_warehouse.walls:#walls
                    if element[0] not in current_warehouse.boxes:#boxes
                        if(element[2] == (-1,0)):
                            possible_actions.append([element[1],left])
                        if(element[2] == (1,0)):
                            possible_actions.append([element[1],right])
                        if(element[2] == (0,-1)):
                            possible_actions.append([element[1],up])
                        if(element[2] == (0,1)):
                            possible_actions.append([element[1],down])
        return possible_actions 
        raise NotImplementedError()
    def result(self, state, action):
        current_warehouse = sokoban.Warehouse()
        warehouse_str = str(state)
        current_warehouse.extract_locations(warehouse_str.split(sep="\n"))
        box = action[0]
        if box in current_warehouse.boxes:
            # Remove the old box, set the worker to the position, and add the
            # new box position. This moves the box with the worker.
            if(action[1] == "Left"):
                offset = (-1,0)
            if(action[1] == "Right"):
                offset = (1,0)
            if(action[1] == "Up"):
                offset = (0,-1)
            if(action[1] == "Down"):
                offset = (0,1)
            #
            current_warehouse.worker = box
            current_warehouse.boxes.remove(box)
            current_warehouse.boxes.append(add_tuples(box, offset))
            self.path.append((action))
            return str(current_warehouse)
        raise NotImplementedError()
    def goal_test(self, state):
        # Check that the state warehouse has all targets filled.
        new_state = str(state)
        new_state = new_state.replace('@', ' ')
        return new_state == self.goal
        raise NotImplementedError()
    
def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 
    
    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    In this scenario, the cost of all (macro) actions is one unit. 

    @param warehouse: a valid Warehouse object

    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    #
    # specify heuristic
    def h(n):
        state = n.state
        #print(str(state))
        current_warehouse = sokoban.Warehouse()
        warehouse_str = str(state)
        current_warehouse.extract_locations(warehouse_str.split(sep="\n"))
        h = 0
        for target in current_warehouse.targets:
            for box in current_warehouse.boxes:             
                h += math.sqrt(((box[1] - target[1])**2) + ((box[0] - target[0])**2))
        return h
    macro_puzzle = macro_sokoban_test(warehouse)
    Path = search.astar_graph_search(macro_puzzle,h)

    #extract path steps
    #print(str(Path))
    if Path == None:
        return "Impossible"    
    path_steps = Path.path()
    path_steps = [e.action for e in path_steps]
    path_steps.pop(0)
    #covert to format required
    #flip box possition
    #change box position to tuple from list
    for step in path_steps:
        step[0] = flip_tuple(step[0])
    for count in range(0, len(path_steps)):
        path_steps[count] = tuple(path_steps[count]) 
    # when the puzzle cannot be solved SokobanPuzzle returns 'Impossible' 
    if Path == None:
        return "Impossible"
    else:
        return path_steps
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.
    
    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.
    
    The ith box is initially at position 'warehouse.boxes[i]'.
        
    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.
    
    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)

    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

