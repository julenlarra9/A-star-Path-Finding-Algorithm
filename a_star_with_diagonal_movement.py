import pygame
import math
import heapq
from queue import PriorityQueue
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
TURQUOISE = (64, 224, 208)

#make a normal pygame window [as long as a proper loop is made, it wont last long]
pygame.init()

WIDTH=800
HEIGHT=WIDTH+50
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")

#goal is to make a grid where each cube will have an identity [color based attribute, location etc]
#make a class of cubes [units of the grid]

class spot:
    def __init__(self, row, col, width, total_rows):
            self.row = row #the number based co ordinates
            self.col = col
            self.x = row * width #the proper distance based co ordinates
            self.y = col * width
            self.color = WHITE
            self.neighbors = []
            self.width = width
            self.total_rows = total_rows

    #THE CHECKING FUNCTIONS-----------------------------------------
    #returns the position of the cube in terms of row and col
    def get_pos(self):
          return self.row, self.col
    
    #check whether the spot is closed [already looked at]
    def is_closed(self):
          return self.color==RED
    
    def is_open(self):
          return self.color==GREEN
    
    #check if the spot is part of a wall
    def is_barrier(self):
          return self.color==BLACK

    #check if it is starting node
    def is_start(self):
          return self.color==ORANGE
    
    def is_end(self):
          return self.color==TURQUOISE

    
    
    def reset(self):
          self.color=WHITE
    
    #THE SETTING FUNCTIONS TO SET THE ATTRIBUTES TO THE SPOTS:----
    
    
    #make the spot closed
    def make_closed(self):
          self.color=RED
    
    def make_open(self):
          self.color=GREEN
    
    
    def make_barrier(self):
          self.color=BLACK

    def make_start(self):
          self.color=ORANGE
    
    def make_end(self):
          self.color=TURQUOISE

    #to make the path
    def make_path(self):
        self.color=PURPLE

    
    #draw the spot in window
    def draw(self,window):
          #draw the square at the particular distance based co ordinate
          pygame.draw.rect(window,self.color,rect=(self.x,self.y,self.width,self.width))
    
    def update_neighbours(self,grid):
          self.neighbors=[]
          
          if(self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier()): #can move below and below is not a barrier
               self.neighbors.append(grid[self.row+1][self.col])
          if(self.row>0 and not grid[self.row-1][self.col].is_barrier()): #can move up and up is not a barrier
               self.neighbors.append(grid[self.row-1][self.col])
          if(self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier()): #can move right and right is not a barrier
               self.neighbors.append(grid[self.row][self.col+1])
          if(self.col>0 and not grid[self.row][self.col-1].is_barrier()): #can move left and left is not a barrier
               self.neighbors.append(grid[self.row][self.col-1])
          
          if(self.row>0 and self.col<self.total_rows-1 and not (grid[self.row-1][self.col+1].is_barrier() or grid[self.row-1][self.col].is_barrier() or grid[self.row][self.col+1].is_barrier())): #can top right diagonal
               self.neighbors.append(grid[self.row-1][self.col+1])
          if(self.row>0 and self.col>0 and not (grid[self.row-1][self.col-1].is_barrier() or grid[self.row-1][self.col].is_barrier() or grid[self.row][self.col-1].is_barrier())): #can top left diagonal
               self.neighbors.append(grid[self.row-1][self.col-1])
          if(self.row<self.total_rows-1 and self.col>0 and not (grid[self.row+1][self.col-1].is_barrier() or grid[self.row+1][self.col].is_barrier() or grid[self.row][self.col-1].is_barrier())): #can bottom left diagonal
               self.neighbors.append(grid[self.row+1][self.col-1])
          if(self.row<self.total_rows-1 and self.col<self.total_rows-1 and not (grid[self.row+1][self.col+1].is_barrier() or grid[self.row][self.col+1].is_barrier() or grid[self.row+1][self.col].is_barrier())): #can bottom right diagonal
               self.neighbors.append(grid[self.row+1][self.col+1])
          

    
    def __lt__(self,other):
          return False
    

#outside the class

#the heuristic function
def heuristic(p1, p2, method='manhattan'):
    x1, y1 = p1
    x2, y2 = p2
    if method == 'manhattan':
      #returning the manhattan distance
        return abs(x1 - x2) + abs(y1 - y2)
    elif method == 'euclidean':
      #returning the euclidean distance
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    elif method == 'chebyshev':
      #returning the chebyshev distance
        return max(abs(x1 - x2), abs(y1 - y2))     
    return 0

#to make the grid in the window
def make_grid(rows,width):
    #rows:how many rows should be in the entire grid
    #width=width of the window

    grid=[]
    gap=width//rows #gives the quotient of div,  deciding the width of each block

    for i in range(rows):
        grid.append([])
        for j in range(rows): 
            Spot=spot(i,j,gap,rows)
            grid[i].append(Spot)
    
    return grid

def draw_grid(window, width,rows):
      gap=width//rows

      for i in range(rows):
            pygame.draw.line(window,GRAY,(0,i*gap),(width,i*gap))
            for j in range(rows):
                pygame.draw.line(window,GRAY,(j*gap,0),(j*gap,width))
    
    
#draw whatever told on the screen
def draw(window,grid,width,rows):
    #fill the whole screen with white 
    window.fill(WHITE)
    #draw all the spots present in grid
    for row in grid:
        for spot in row:
            spot.draw(window)

    #draw the grid
    draw_grid(window,width,rows)

    #update whatever we drawn till now
    pygame.display.update()

#helper function to identify in which cube the mouse click is situated
def get_click(pos,rows,width):
    x,y=pos
    gap=width//rows

    row_spot=x//gap
    col_spot=y//gap

    return row_spot,col_spot

def reconstruct_path(prev,current_node,draw):
     while(current_node in prev):
         current_node=prev[current_node]
         current_node.make_path()
     
     current_node.make_start() #so that after reconstruction the starting spot is not covered purple
     draw()

def draw_button(window, x, y, width, height, text, color, text_color):
    #Draws a button on the screen.
    pygame.draw.rect(window, color, (x, y, width, height))
    font = pygame.font.SysFont(None, 30)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    window.blit(text_surface, text_rect)

def is_mouse_over_button(pos, x, y, width, height):
    #Checks if the mouse is over a button."""
    return x <= pos[0] <= x + width and y <= pos[1] <= y + height

def algorithm(draw, grid, start, end):
    count = 0  # Used as a tie-breaker when f scores are equal
    open_list = []  # This will hold our priority queue
    heapq.heappush(open_list, (0, count, start))  # Push start node into the queue
    open_set_hash = {start}  # This is a set to quickly check if a node is in the open list
    prev = {}  # Dictionary to track the previous node in the path
    g_score = {spot: float("inf") for row in grid for spot in row}  # Initialize g_scores to infinity
    g_score[start] = 0  # Set the g_score of the start node to 0
    h_score = {spot: heuristic(spot.get_pos(), end.get_pos(), 'manhattan') for row in grid for spot in row}
    f_score = {spot: h_score[spot] + g_score[spot] for spot in h_score.keys()}  # f_score = g_score + h_score

    # Main loop for A* algorithm
    while open_list:
        # Check if the user has pressed exit cross
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Pop the node with the lowest f_score
        current_f, current_count, current_node = heapq.heappop(open_list)
        open_set_hash.remove(current_node)

        # If we reached the end node, reconstruct the path and exit
        if current_node == end:
            current_node.make_end()
            print("Found the end!")
            reconstruct_path(prev, current_node, draw)
            return True

        # Get the neighbors of the current node
        neigh_node = current_node.neighbors

        # Check each neighbor
        for neighbor in neigh_node:
            # Determine the cost of moving to this neighbor
            if heuristic(neighbor.get_pos(), current_node.get_pos(), 'manhattan') > 1:
                # Diagonal movement
                tentative_g_score = g_score[current_node] + 1.414  # Diagonal distance is sqrt(2)
            else:
                # Orthogonal movement
                tentative_g_score = g_score[current_node] + 1

            # If this path to the neighbor is better, update its scores
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h_score[neighbor]
                prev[neighbor] = current_node

                # If the neighbor is not in the open set, add it
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_list, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        # Mark the current node as closed
        if current_node != start:
            current_node.make_closed()

        # Update the display
        draw()

    print("No path found")
    return False

def main(window,width):
    ROWS=50
    #start and end position in the maze
    start=None
    end=None
    #algo started or not
    started=False
    #the main loop running or not
    run=True

    grid=make_grid(ROWS,width)

    # Button attributes
    button_width = 100
    button_height = 40
    button_x = (width // 2) - (button_width // 2)
    button_y = width + 10

    while run:
        draw(window,grid,width,ROWS)
        # Draw the restart button
        draw_button(window, button_x, button_y, button_width, button_height, "Restart", ORANGE, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run=False
            #once the algorithm started, the user can only quit the application
            if(started==True):
                continue
            

            #the mouse key is pressed
            if pygame.mouse.get_pressed()[0]: #the left button
                pos=pygame.mouse.get_pos()

                # Check if restart button was clicked
                if is_mouse_over_button(pos, button_x, button_y, button_width, button_height):
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    continue

                 #get the row and col number of the cube in the grid
                row,col=get_click(pos,ROWS,width)

                 #access the spot from grid
                spot=grid[row][col]

                 #draw on grid with conditions applied

                #check if the starting spot is not created yet and user has not clicked on the ending spot
                if not start and spot!=end: 
                    start=spot
                    start.make_start()

                #check if the ending spot is not created yet and user has not clicked on the starting spot
                elif not end and spot!=start:
                    end=spot
                    end.make_end()

                #if the user has not clicked on top of any of the start or end spots
                elif spot!=start and spot!=end: #also prevents drawing barrier on the start point 
                    spot.make_barrier()


            elif pygame.mouse.get_pressed()[2]: #the right click
                pos=pygame.mouse.get_pos()

                 #get the row and col number of the cube in the grid
                row,col=get_click(pos,ROWS,width)

                 #access the spot from grid
                spot=grid[row][col]
                
                spot.reset() #make the color=white

                if(spot==start):
                     start=None
                elif(spot==end):
                     end=None

            if event.type==pygame.KEYDOWN: #when a keyboard key is pressed
                 #if the key is space, and the algo has not started, start it
                 if((event.key==pygame.K_SPACE) and start and end): #make sure to have a start and end otherwise the program may crash
                      #update the neighbours of each spot
                      for row in grid:
                           for Spot in row:
                                Spot.update_neighbours(grid)
                        
                      #call the algorithm
                      #this should also be able to draw the changed o/p so passing the draw function
                      algorithm(lambda: draw(window,grid,width,ROWS),grid,start,end)
                
                 if(event.key==pygame.K_c):
                      start=None
                      end=None
                      grid=make_grid(ROWS,width)
                      
    pygame.quit()

main(WIN,WIDTH)