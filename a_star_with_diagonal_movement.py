import pygame
import math
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
WIN=pygame.display.set_mode((WIDTH,WIDTH))
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
def heuristic(p1,p2):
      x1,y1=p1
      x2,y2=p2
      l1_norm = abs(x1-x2) + abs(y1-y2)
      l2_norm=math.sqrt((x1-x2)**2 + (y1-y2)**2)
      #returning the manhattan distance [we can change it to euclidean, it also allows diagonal movement]
      return l1_norm

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

def algorithm(draw,grid,start,end): #here draw is passed as the lamda function with all the rquired parameters
     count=0 #in video told to be used as second priority [when f scores are equal]
     open_queue=PriorityQueue()
     #put the start in priority queue
     #each element in the queue has structure F_score,count,node
     open_queue.put((0,count,start))
     open_set_hash={start}
     #the dict containing previous node in the path
     prev={}
     #set the dictionary to hold g,h scores of each node
     g_score={spot:float("inf") for row in grid for spot in row}
     g_score[start]=0
     
     h_score={spot: heuristic(spot.get_pos(),end.get_pos()) for row in grid for spot in row}
     f_score={spot: h_score[spot]+g_score[spot]  for spot in h_score.keys()}

     #untill we check all the elements in pq
     while(open_queue.empty() !=True):
          #check if the user has pressed exit cross
          for event in pygame.event.get():
               if event.type==pygame.QUIT:
                    pygame.quit()
            
          #popped the topmost node [with least f score]
          current_node=open_queue.get()[2]
          open_set_hash.remove(current_node)
          
          #to stop the algorithm
          if(current_node==end):
               current_node.make_end()
               print("found the end!!")
               reconstruct_path(prev,current_node,draw)
               return True
          
          #get the neighbours
          neigh_node=current_node.neighbors
          #HERE ALL NEIGHBOURS ARE A T DISTANCE 1 [UP,LEFT,DOWN,RIGHT]
          
          #check if the f,g,h scores of a neighbour is lower than what is in the dictionary
          for neighbour in neigh_node:
               #check if diagonal neighbour or not
               if(heuristic(neighbour.get_pos(),current_node.get_pos())>1):
                    #diagonal
                    #if less g_score update
                    if(g_score[current_node]+1.414<g_score[neighbour]):
                            g_score[neighbour]=g_score[current_node]+1.414
                            
                    #if the f score is low update and put in the queue[even after putting while popping the element with least f score will come]
                    if(g_score[current_node]+1.414+h_score[neighbour]<f_score[neighbour]):
                        f_score[neighbour]=g_score[current_node]+1.414+h_score[neighbour]
                        prev[neighbour]=current_node

                        if(neighbour not in open_set_hash):
                            count+=1
                            open_queue.put((f_score[neighbour],count,neighbour))
                            open_set_hash.add(neighbour)
                            neighbour.make_open() #these are the neighbours we did consider to look at
               else:
                   #if less g_score update
                    if(g_score[current_node]+1<g_score[neighbour]):
                            g_score[neighbour]=g_score[current_node]+1
                            
                    #if the f score is low update and put in the queue[even after putting while popping the element with least f score will come]
                    if(g_score[current_node]+1+h_score[neighbour]<f_score[neighbour]):
                        f_score[neighbour]=g_score[current_node]+1+h_score[neighbour]
                        prev[neighbour]=current_node


                        if(neighbour not in open_set_hash):
                            count+=1
                            open_queue.put((f_score[neighbour],count,neighbour))
                            open_set_hash.add(neighbour)
                            neighbour.make_open() #these are the neighbours we did consider to look at
               
                  

               
    
          draw()
          if(current_node!=start):
               current_node.make_closed()

     print("no path found")         
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
    
    while run:
        draw(window,grid,width,ROWS)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run=False
            #once the algorithm started, the user can only quit the application
            if(started==True):
                continue
            

            #the mouse key is pressed
            if pygame.mouse.get_pressed()[0]: #the left button
                pos=pygame.mouse.get_pos()

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