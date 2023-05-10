
import pygame
import random
import pygame.mixer

COLS = 18
ROWS = 18
CELL = 25
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

#COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN  = (0,255,0)

class Player(pygame.sprite.Sprite):  #this class is used to give characterstics of the player
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([CELL, CELL])
        self.image.fill((255, 20, 20))
        self.image = pygame.image.load("Super-mario-Image-path").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None
        self.exit_block = None
        self.level_complete = False
        self.level = 0
    
    def changespeed(self, x, y):
        ''' Change the speed fo the player '''
        self.change_x +=x
        self.change_y += y

    def update(self):
        """ Update the player position """
        # Move left/right
        self.rect.x += self.change_x

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= WIDTH - CELL:
            self.rect.x = WIDTH - CELL

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
        
        # Move up/down
        self.rect.y += self.change_y

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= HEIGHT - CELL:
            self.rect.y = HEIGHT - CELL

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        exit_touch = pygame.sprite.spritecollide(self, self.exit_block, False)
        if len(exit_touch) > 0:
            self.level_complete = True
            self.level = self.level + 1
            self.rect.x = 0
            self.rect.y = 0


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([CELL, CELL])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def generate_maze():
    maze = [[0 for x in range(COLS)] for y in range(ROWS)]
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    stack = [(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))]

    while len(stack) > 0:
        (cx, cy) = stack[-1] #cx cy stores all the visited cells
        maze[cy][cx] = 1
        # find a new cell to add
        nlst = [] # list of available neighbors
        for i in range(4):
            nx = cx + dx[i]; ny = cy + dy[i]
            if nx >= 0 and nx < COLS and ny >= 0 and ny < ROWS:
                if maze[ny][nx] == 0:
                    # of occupied neighbors must be 1
                    ctr = 0
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if ex >= 0 and ex < COLS and ey >= 0 and ey < ROWS:
                            if maze[ey][ex] == 1: ctr += 1
                    if ctr == 1: nlst.append(i)
        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]
            stack.append((cx, cy))
        else: stack.pop()
    
    # Add an exit
    finished = False
    while not finished:
        exit_row = random.randint(0, ROWS - 1)
        if maze[exit_row][COLS - 1] == 1:
            maze[exit_row][COLS - 1] = 2
            finished = True


    return maze

def music():  #it provides a BGM
    pygame.init()
    pygame.mixer.music.load("MP3-FILE-PATH")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(2.0)

def main():
    number_of_levels =10
    level = 0
    pygame.display.set_caption("MAZE RUNNER")
    master_maze = []   
    for x in range(number_of_levels): 
        master_maze.append(generate_maze())
    music() 
    # draw the maze
    win = pygame.display.set_mode((WIDTH, HEIGHT)) 
    clock = pygame.time.Clock()
    FPS = 150
    
    player = Player(0,0)
    
    while level < number_of_levels-1:
        all_sprites = pygame.sprite.Group()
        walls = pygame.sprite.Group()
        exit_block = pygame.sprite.Group()
        level = player.level
        player.walls = walls
        player.exit_block = exit_block
        player.level_complete = False
        print("Level: ",level)

        '''for c in range(ROWS):
            for d in range(COLS):
                print (str(master_maze[level][c][d]) + ",", end="")
            print()'''
        

        exit_cell = (0,0)

        for x in range(ROWS):
            for y in range(COLS):
                if master_maze[level][x][y] == 1:
                    all_sprites.add(Square(y * CELL, x * CELL, BLACK))
                elif master_maze[level][x][y] == 2:
                    exit_block.add(Square(y * CELL, x * CELL,GREEN))
                    all_sprites.add(Square(y * CELL, x * CELL, GREEN))
                else:
                    walls.add(Square(y * CELL, x * CELL, WHITE))

        all_sprites.add(player)
        
        
        running = True
        while running:   
                                                    
            for event in pygame.event.get():           
                if event.type == pygame.QUIT:
                    running = False
                    level = number_of_levels
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.changespeed(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        player.changespeed(1, 0)
                    if event.key == pygame.K_UP:
                        player.changespeed(0, -1)
                    if event.key == pygame.K_DOWN:
                        player.changespeed(0, 1)
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.changespeed(1, 0)
                    if event.key == pygame.K_RIGHT:
                        player.changespeed(-1, 0)
                    if event.key == pygame.K_UP:
                        player.changespeed(0, 1)
                    if event.key == pygame.K_DOWN:
                        player.changespeed(0, -1)
                    
            all_sprites.update()
            if player.level_complete:
                running = False
            
            win.fill(WHITE)
            all_sprites.draw(win)
            pygame.display.update()
            clock.tick(FPS)


    print("Thank you for playing my game")

if __name__ == "__main__":
    main()