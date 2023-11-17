import pygame, random
from time import perf_counter as timer
start_time = timer()
print()
running = True
black = (0,0,0)
GREY = (100,100,100)
gsize = 3
spacing = 25 # cell box width
factor = 1 # change this to two for a fun time!
lw = 3 # line width
redc = (220,0,50)
dark_red = (150,0,0)
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial',14)

class Graphy:
    def __init__(self,gsize):
        self.gsize = gsize
        self.order = [] #{i:0 for i in range(self.gsize**2)}
        self.walls = {i:[1,1,1,1] for i in range(self.gsize**2)}
        self.visited = {i:0 for i in range(self.gsize**2)}
        self.available = {i:[] for i in range(self.gsize**2)}
        self.neighbor_pattern = ((-1,0),(0,1),(1,0),(0,-1))
        self.cells = [[i+j*self.gsize for i in range(self.gsize)] for j in range(self.gsize)]
        #Create the neighbor dictionary
        for i in range(self.gsize):
            for j in range(self.gsize):
                for k,val in enumerate(self.neighbor_pattern):
                    if 0 <= i+val[0] < self.gsize and 0 <= j+val[1] < self.gsize:
                        self.available[j+i*self.gsize].append(self.cells[i+val[0]][j+val[1]])
        #generate the maze
        self.path = self.generate()
        #self.walls[0][3] = 0
        #self.walls[self.gsize**2-1][1] = 0
        self.complete = False
        self.starttimme = timer()
        self.endtime = timer()
        self.time_elapsed = 0

    def has_unvisited_neighbors(self,cell):
        """has_unvisited_neighbors: checks input cell for any unvisited neighbors"""
        county = 0
        for i in self.available[cell]:
            if self.visited[i] == 0:
                county += 1
        return county

    def get_coords(self,cell):
        """get_coords: returns the row and col of the cell number input, TESTED """
        for i,row in enumerate(self.cells):
            if cell in row:
                return i,row.index(cell)

    def reduce_available(self,cell):
        """reduce_available: removes cell from self.available """
        ##### NEEDS WORK #####################
        for i in self.available:
            if cell in self.available[i]:
                self.available[i].remove(cell)
        #pass

    def remove_wall(self,new,cur):
        """remove_wall: removes an entry in the self.walls list, TESTED """
        new_row,new_col = self.get_coords(new)
        cur_row,cur_col = self.get_coords(cur)
        wall_index_cur = self.neighbor_pattern.index((new_row-cur_row,new_col-cur_col))
        wall_index_new = self.neighbor_pattern.index((cur_row-new_row,cur_col-new_col))
        self.walls[new][wall_index_new] = 0
        self.walls[cur][wall_index_cur] = 0

    def get_cell(self,row,col):
        """ converts player coords into cell block # """
        cellx_index = int((col-spacing-5)/spacing)
        celly_index = int((row-spacing-5)/spacing)
        #print(cellx_index,celly_index)
        #print('hi',len(self.walls[][]))
        wall_index = self.cells[cellx_index][celly_index]
        return wall_index

    def generate(self):
        """generate: generates depth first maze """
        counter = 0
        start_cell = 0
        stack = [start_cell]
        current = start_cell
        self.visited[start_cell] = 1
        self.reduce_available(start_cell)
        while len(stack) > 0:
            current = stack.pop()
            if self.has_unvisited_neighbors(current) > 0:
                counter += 1
                stack.append(current)
                for i in range(random.randint(0,10)):
                    random.shuffle(self.available[current])
                last = self.available[current].pop()
                self.remove_wall(last,current)
                self.visited[last] = 1
                self.reduce_available(current)
                stack.append(last)
                if current not in self.order:
                    self.order.append(last)
        return stack

    def draw_walls(self):
        """draw_wall: draws the walls on the screens, takes self as only input"""
        # rect is (left, top, width, height)
        counter = 0
        loc = range(spacing,self.gsize*factor*spacing+spacing,factor*spacing)
        for j in loc:
            for i in loc:
                if self.walls[counter][0]==1:
                    pygame.draw.line(screen,GREY,(i,j),(i+spacing,j),lw)
                if self.walls[counter][1]==1:
                    pygame.draw.line(screen,GREY,(i+spacing,j),(i+spacing,j+spacing),lw)
                if self.walls[counter][2]==1:
                    pygame.draw.line(screen,GREY,(i,j+spacing),(i+spacing,j+spacing),lw)
                if self.walls[counter][3]==1:                    
                    pygame.draw.line(screen,GREY,(i,j),(i,j+spacing),lw)
                counter += 1
    
    def draw_cell(self,cell):
        """ draws only the immediate cell """
        xi,yi = self.get_coords(cell)
        xi = xi*spacing + spacing
        yi = yi*spacing + spacing
        for i in self.walls[cell]:
            if self.walls[cell][0]==1:
                pygame.draw.line(screen,GREY,(yi,xi),(yi+spacing,xi),lw)
            if self.walls[cell][1]==1:
                pygame.draw.line(screen,GREY,(yi+spacing,xi),(yi+spacing,xi+spacing),lw)
            if self.walls[cell][2]==1:
                pygame.draw.line(screen,GREY,(yi,xi+spacing),(yi+spacing,xi+spacing),lw)
            if self.walls[cell][3]==1:                    
                pygame.draw.line(screen,GREY,(yi,xi),(yi,xi+spacing),lw)

    def draw_hallway(self,cell):
        """ recursively draws hallways in the four cardinal directions """
        self.draw_cell(cell)
        self.draw_top_hallway(cell)
        self.draw_right_hallway(cell)
        self.draw_bottom_hallway(cell)
        self.draw_left_hallway(cell)

    def draw_top_hallway(self,cell):
        """ recursively draws top hallway """
        self.draw_cell(cell)
        if self.walls[cell][0] == 0:
            self.draw_top_hallway(cell-self.gsize)
            pass

    def draw_right_hallway(self,cell):
        """ recursively draws right hallway """
        self.draw_cell(cell)
        if self.walls[cell][1] == 0:
            self.draw_right_hallway(cell+1)
            pass

    def draw_bottom_hallway(self,cell):
        """ recursively draws bottom hallway """
        self.draw_cell(cell)
        if self.walls[cell][2] == 0:
            self.draw_bottom_hallway(cell+self.gsize)
            pass

    def draw_left_hallway(self,cell):
        """ recursively draws left hallway """
        self.draw_cell(cell)
        if self.walls[cell][3] == 0:
            self.draw_left_hallway(cell-1)
            pass


    def __str__(self):
        """ pretty print function """
        sqrd = self.gsize**2
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        if 1 == 1:
            for i in range(self.gsize):
                for j in range(self.gsize):
                    print(f"{self.cells[i][j]:5}",end='')
                print()
        if 1==0:
            for i,j in self.available.items():
                print(f"{i:3},{j:13},{str(self.visited[i]):20}")
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        return ''


loop_size = 10

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Pathfinders")
screen.fill(black)
g1 = Graphy(loop_size)
xst = spacing*(loop_size) + 5
yst = spacing*(loop_size) + 5
osx = int(xst)
osy = int(yst)
xy_index = g1.cells[loop_size-1][loop_size-1]
mpath = [loop_size**2]
thek = 0
reachedend = False

timer_start = timer()
timer_end = 0
time_elapsed = 0

while running:
    pygame.display.flip()
    event = pygame.event.wait()
    #for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        screen.fill(black)
        del g1
        g1 = Graphy(loop_size)
        pygame.display.update()
        osx = int(xst)
        osy = int(yst)
        xy_index = g1.cells[loop_size-1][loop_size-1]
        pygame.draw.rect(screen,redc,(xst,yst,15,15))
        mpath =[loop_size**2-1]
        reachedend = False
        time_start = timer()
        #print(g1)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if thek == 1:
                thek = 0
            else:
                thek = 1
            print(thek)
        if event.key == pygame.K_UP:
            if g1.walls[g1.get_cell(osx,osy)][0] == 0:
                osy -= spacing
                xy_index = xy_index - loop_size
        if event.key == pygame.K_DOWN:
            if g1.walls[g1.get_cell(osx,osy)][2] == 0:
                osy += spacing
                xy_index = xy_index + loop_size
        if event.key == pygame.K_LEFT:
            if g1.walls[g1.get_cell(osx,osy)][3] == 0:
                osx -= spacing
                xy_index = xy_index - 1
        if event.key == pygame.K_RIGHT:
            if g1.walls[g1.get_cell(osx,osy)][1] == 0:
                osx += spacing
                xy_index = xy_index + 1
        #print(xy_index)
        screen.fill(black)
        pygame.draw.rect(screen,dark_red,(osx,osy,15,15))
    
    # draws all of  the  dots in place
    for i in range(spacing,g1.gsize*spacing+2*spacing,spacing):
        for j in range(spacing,g1.gsize*spacing+2*spacing,spacing):
            pygame.draw.rect(screen,GREY,(i,j,2,2))
    if xy_index == 0:
        reachedend = True
    
    #draw the surrounding cells
    g1.draw_cell(xy_index)
    g1.draw_hallway(xy_index)
    if thek == 1:
        g1.draw_walls()
    if reachedend == True:
        g1.draw_walls()
        timer_end = timer()
        time_elapsed = timer_end-timer_start
        print(time_elapsed)
    #pygame.display.update()
    #break

    text = font.render(f"time_elapsed: {time_elapsed.__round__(1):4}",False,BLUE)
    screen.blit(text,(10,10))
    clock.tick(30)

pygame.quit()


end_time = timer()
time_dif = end_time - start_time
print(round(time_dif,2))


'''
image manipulation
full stack web app with docker
full oauth2 spec server - OIDC compliant - using JSON web tokens
sudoku solver
pulling online data - apache airflow - save to a data store - extract,transform,load,analysis
'''


