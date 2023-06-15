import pygame
import random

pygame.init()

global slider_value
WIDTH = 450
HEIGHT = 450
m = 1
screen = pygame.display.set_mode([(WIDTH+150), (HEIGHT + 60)])
pygame.display.set_caption('Hide and Seek')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
n = 15
border = 0.3
level = []
map_img = pygame.image.load('map.png').convert_alpha()
rg_img = pygame.image.load('grandom.png').convert_alpha()
start_img = pygame.image.load('start.png').convert_alpha()
pause_img = pygame.image.load('pause.png').convert_alpha()
quit_img = pygame.image.load('quit.png').convert_alpha()
rr_img = pygame.image.load('rrandom.png').convert_alpha()
rv_img = pygame.image.load('rview.png').convert_alpha()
gv_img = pygame.image.load('gview.png').convert_alpha()
nv_img = pygame.image.load('nview.png').convert_alpha()
plus_img = pygame.image.load('rp.png').convert_alpha()
min_img = pygame.image.load('rm.png').convert_alpha()
green_drone = pygame.transform.scale(pygame.image.load('green.png'), (30, 30))
red_drone = pygame.transform.scale(pygame.image.load('red.png'), (30, 30))
line_color = (255, 255, 255)
green_x = 0
green_y = 0
red_x = [0]
red_y = [0]
# R, L, U, D
direction = 0
red_direct = [0]
red = [0]
player_line = [0]
targets = [0]
target_x = [0]
target_y = [0]
target_rect = [0]
speed = 2
r_speed = 1
normal = True
turns_allowed = [False, False, False, False]
gtarget_x = red_x
gtarget_y = red_y
target_size = 30
rv = False
gv = False
rt = [False]
moving = False
stop = False
level_rect = []
lvl_count = 0
slider_x = 350
slider_y = 470
slider_width = 200
slider_height = 10
slider_color = (200, 200, 200)
slider_handle_color = (100, 100, 100)
handle_radius = 9
handle_color = (50, 50, 50)
slider_position = slider_x
slider_value = 0
is_dragging = False

class Red:
    def __init__(self, x_coord, y_coord, target, speeds, image, direct, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 15
        self.center_y = self.y_pos + 15
        self.target = target
        self.speed = speeds
        self.img = image
        self.direction = direct
        self.id = id
        self.turns = self.check_collision()
        self.rect = self.draw()

    def draw(self):
        screen.blit(self.img, (self.x_pos, self.y_pos))
        red_rect = pygame.rect.Rect((self.x_pos + 2, self.y_pos + 2), (26,26))
        return red_rect

    def check_collision(self):
        # R, L, U, D
        num1 = (HEIGHT // 15)
        num2 = (WIDTH // 15)
        num3 = 15
        self.turns = [False, False, False, False]
        if self.center_x // 30 < 14:
            if level[self.center_y // num1][((self.center_x - num3)+5) // num2] < 1:
                self.turns[1] = True
            if level[self.center_y // num1][((self.center_x + num3)-5) // num2] < 1:
                self.turns[0] = True
            if level[((self.center_y + num3)+5) // num1][self.center_x // num2] < 1:
                self.turns[3] = True
            if level[((self.center_y - num3)-5) // num1][self.center_x // num2] < 1:
                self.turns[2] = True
            
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 1:
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 1:
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 1:
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 1:
                        self.turns[0] = True
            if self.direction == 1 or self.direction == 0:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num1) // num1][self.center_x // num2] < 1:
                        self.turns[3] = True
                    if level[(self.center_y - num1) // num1][self.center_x // num2] < 1:
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 1:
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 1:
                        self.turns[0] = True
                        
        else:
            self.turns[0] = False
            self.turns[1] = False

        return self.turns

    def move_red(self):
        # R, L, U, D
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
                self.y_pos += self.speed
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed

        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed

        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        
        return self.x_pos, self.y_pos, self.direction

def switch_target():
    check = True
    while check:
        i = random.randint(1, n-2)
        j = random.randint(1, n-2)
        if level[i][j] == 0 :
            target_x = j * 30
            target_y = i * 30
            check = False

    return target_x, target_y

def update_slider_value():
    value_range = slider_width - handle_radius * 2
    return int((slider_position - slider_x) / value_range * 2) + 1

def draw_slider():
    pygame.draw.rect(screen, slider_color, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(screen, handle_color, (slider_position, slider_y + slider_height // 2), handle_radius)
    text = font.render(f"view number {slider_value}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(200, 470))
    screen.blit(text, text_rect)
    font_small = pygame.font.Font(None, 18)
    text_beginning = font_small.render("1", True, (0, 0, 0))
    text_middle = font_small.render("2", True, (0, 0, 0))
    text_end = font_small.render("3", True, (0, 0, 0))
    screen.blit(text_beginning, (slider_x - text_beginning.get_width() // 2, slider_y + slider_height + 5))
    screen.blit(text_middle, (slider_x + slider_width // 2 - text_middle.get_width() // 2, slider_y + slider_height + 5))
    screen.blit(text_end, (slider_x + slider_width - text_end.get_width() // 2, slider_y + slider_height + 5))

def make_map():
    for i in range(n):
        row = []
        for j in range(n):
            if random.random() < border:
                row.append(1)  
            else:
                row.append(0) 
        level.append(row)

    for i in range(n):
        level[i][0] = level[i][n-1] = 1
        level[0][i] = level[n-1][i] = 1

    for i in range(n-1):
        for j in range(n-1):
            if level[i-1][j] == 0 and level[i][j-1] == 0 and level[i-1][j-1] == 0:
                level[i][j] = 1
            if level[i+1][j] == 0 and level[i][j+1] == 0 and level[i+1][j+1] == 0:
                level[i][j] = 1
            if level[i-1][j] == 0 and level[i][j+1] == 0 and level[i-1][j+1] == 0:
                level[i][j] = 1
            if level[i+1][j] == 0 and level[i][j-1] == 0 and level[i+1][j-1] == 0:
                level[i][j] = 1
        
    for i in range(n-1):
        for j in range(n-1):
            if level[i-1][j] == 0 and level[i][j-1] == 0 and level[i-1][j-1] == 1 and level[i+1][j+1] == 1 and level[i+1][j-1] == 1:
                level[i][j] = 0
            if level[i+1][j] == 0 and level[i][j+1] == 0 and level[i+1][j+1] == 1 and level[i-1][j+1] == 1 and level[i+1][j-1] == 1:
                level[i][j] = 0
            if level[i-1][j] == 0 and level[i][j+1] == 0 and level[i-1][j-1] == 1 and level[i+1][j+1] == 1 and level[i-1][j+1] == 1:
                level[i][j] = 0
            if level[i+1][j] == 0 and level[i][j-1] == 0 and level[i-1][j-1] == 1 and level[i+1][j+1] == 1 and level[i+1][j-1] == 1:
                level[i][j] = 0
            if level[i-1][j] == 0 and level[i+1][j] == 0 and level[i][j-1] == 1 and level[i][j+1] == 1:
                level[i][j] = 0
            if level[i][j-1] == 0 and level[i][j+1] == 0 and level[i-1][j] == 1 and level[i+1][j] == 1:
                level[i][j] = 0

    for i in range(n-1):
        for j in range(n-1):
            if level[i-1][j] == 0 and level[i][j-1] == 0 and level[i-1][j-1] == 0:
                level[i][j] = 1
            if level[i+1][j] == 0 and level[i][j+1] == 0 and level[i+1][j+1] == 0:
                level[i][j] = 1
            if level[i-1][j] == 0 and level[i][j+1] == 0 and level[i-1][j+1] == 0:
                level[i][j] = 1
            if level[i+1][j] == 0 and level[i][j-1] == 0 and level[i+1][j-1] == 0:
                level[i][j] = 1
    return level

def new_map():
    y = []
    z = []
    m = green_x // 30
    k = green_y // 30
    if m >= 2:
        for i in range(len(red_x)):
            y.append(0)
            z.append(0)
            y[i] = red_x[i] // 30
            z[i] = red_y[i] // 30
    else:
        y.append(red_x[0] // 30)
        z.append(red_y[0] // 30)
    for i in range(n):
        row = []
        for j in range(n):
            if random.random() < border:
                row.append(1)  
            else:
                row.append(0) 
        level.append(row)

    for i in range(n):
        level[i][0] = level[i][n-1] = 1
        level[0][i] = level[n-1][i] = 1

    for i in range(n-1):
        for j in range(n-1):
            if level[i-1][j] == 0 and level[i][j-1] == 0 and level[i-1][j-1] == 0:
                level[i][j] = 1
            if level[i+1][j] == 0 and level[i][j+1] == 0 and level[i+1][j+1] == 0:
                level[i][j] = 1
            if level[i-1][j] == 0 and level[i][j+1] == 0 and level[i-1][j+1] == 0:
                level[i][j] = 1
            if level[i+1][j] == 0 and level[i][j-1] == 0 and level[i+1][j-1] == 0:
                level[i][j] = 1
        
    level[k][m] = 0

    
    if level[k-1][m] == 0 and level[k][m-1] == 0 and level[k-1][m-1] == 0:
        level[k][m] = 0
        level[k-1][m-1] = 1
    if level[k+1][m] == 0 and level[k][m+1] == 0 and level[k+1][m+1] == 0:
        level[k][m] = 0
        level[k+1][m+1] = 1
    if level[k-1][m] == 0 and level[k][m+1] == 0 and level[k-1][m+1] == 0:
        level[k][m] = 0
        level[k-1][m+1] = 1
    if level[k+1][m] == 0 and level[k][m-1] == 0 and level[k+1][m-1] == 0:
        level[k][m] = 0
        level[k+1][m-1] = 1
    for i in range(len(red_x)):
        level[z[i]][y[i]] = 0

        if level[z[i]-1][y[i]] == 0 and level[z[i]][y[i]-1] == 0 and level[z[i]-1][y[i]-1] == 0:
            level[z[i]][y[i]] = 0
            level[z[i]-1][y[i]-1] = 1
        if level[z[i]+1][y[i]] == 0 and level[z[i]][y[i]+1] == 0 and level[z[i]+1][y[i]+1] == 0:
            level[z[i]][y[i]] = 0
            level[z[i]+1][y[i]+1] = 1
        if level[z[i]-1][y[i]] == 0 and level[z[i]][y[i]+1] == 0 and level[z[i]-1][y[i]+1] == 0:
            level[z[i]][y[i]] = 0
            level[z[i]-1][y[i]+1] = 1
        if level[z[i]+1][y[i]] == 0 and level[z[i]][y[i]-1] == 0 and level[z[i]+1][y[i]-1] == 0:
            level[z[i]][y[i]] = 0
            level[z[i]+1][y[i]-1] = 1

    for i in range(n-1):
        for j in range(n-1):
            if level[i-1][j] == 0 and level[i][j-1] == 0 and level[i-1][j-1] == 1 and level[i+1][j+1] == 1 and level[i+1][j-1] == 1:
                level[i][j] = 0
            if level[i+1][j] == 0 and level[i][j+1] == 0 and level[i+1][j+1] == 1 and level[i-1][j+1] == 1 and level[i+1][j-1] == 1:
                level[i][j] = 0
            if level[i-1][j] == 0 and level[i][j+1] == 0 and level[i-1][j-1] == 1 and level[i+1][j+1] == 1 and level[i-1][j+1] == 1:
                level[i][j] = 0
            if level[i+1][j] == 0 and level[i][j-1] == 0 and level[i-1][j-1] == 1 and level[i+1][j+1] == 1 and level[i+1][j-1] == 1:
                level[i][j] = 0
            if level[i-1][j] == 0 and level[i+1][j] == 0 and level[i][j-1] == 1 and level[i][j+1] == 1:
                level[i][j] = 0
            if level[i][j-1] == 0 and level[i][j+1] == 0 and level[i-1][j] == 1 and level[i+1][j] == 1:
                level[i][j] = 0

    for i in range(n-1):
        for j in range(n-1):
            if level[i-1][j] == 0 and level[i][j-1] == 0 and level[i-1][j-1] == 0:
                level[i][j] = 1
            if level[i+1][j] == 0 and level[i][j+1] == 0 and level[i+1][j+1] == 0:
                level[i][j] = 1
            if level[i-1][j] == 0 and level[i][j+1] == 0 and level[i-1][j+1] == 0:
                level[i][j] = 1
            if level[i+1][j] == 0 and level[i][j-1] == 0 and level[i+1][j-1] == 0:
                level[i][j] = 1
    return level

def green_view():
    num1 = (HEIGHT// 15)
    num2 = (WIDTH // 15)
    current_row = (green_y + 15) // 30
    current_col = (green_x + 15) // 30
    rect_list = []  # List to store rectangles
    count = 0  # Counter for the number of 1's
    pygame.draw.rect(screen, 'blue', [0, 0, 450, 450])
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                rect = pygame.rect.Rect((j * num2, i * num1), (30, 30))
                rect_list.append(rect)  # Add rectangle to the list
                count += 1  # Increment the count

    if level[current_row][current_col] == 0:
        pygame.draw.rect(screen, 'white', [current_col * num2, current_row * num1, 30,30])
    if level[current_row - 1][current_col] == 0:
        pygame.draw.rect(screen, 'white', [current_col * num2, ((current_row - 1)* num1) + 20, 30,10])
    else:
        pygame.draw.rect(screen, 'black', [current_col * num2, ((current_row - 1)* num1) + 20, 30,10])
    if level[current_row + 1][current_col] == 0:
        pygame.draw.rect(screen, 'white', [current_col * num2, (current_row + 1)* num1, 30,10])
    else:
        pygame.draw.rect(screen, 'black', [current_col * num2, (current_row + 1)* num1, 30,10])
    if level[current_row][current_col - 1] == 0:
        pygame.draw.rect(screen, 'white', [((current_col - 1)* num2) + 20, current_row * num1, 10,30])
    else:
        pygame.draw.rect(screen, 'black', [((current_col - 1)* num2) + 20, current_row * num1, 10,30])
    if level[current_row][current_col + 1] == 0:
        pygame.draw.rect(screen, 'white', [(current_col + 1)* num2, current_row * num1, 10,30])
    else:
        pygame.draw.rect(screen, 'black', [(current_col + 1)* num2, current_row * num1, 10,30])
    if level[current_row - 1][current_col - 1] == 0:
        pygame.draw.rect(screen, 'white', [((current_col - 1)* num2) + 20, ((current_row - 1)* num1) + 20, 10,10])
    else:
        pygame.draw.rect(screen, 'black', [((current_col - 1)* num2) + 20, ((current_row - 1)* num1) + 20, 10,10])
    if level[current_row + 1][current_col - 1] == 0:
        pygame.draw.rect(screen, 'white', [((current_col - 1)* num2) + 20, (current_row + 1)* num1, 10,10])
    else:
        pygame.draw.rect(screen, 'black', [((current_col - 1)* num2) + 20, (current_row + 1)* num1, 10,10])
    if level[current_row - 1][current_col + 1] == 0:
        pygame.draw.rect(screen, 'white', [(current_col + 1)* num2, ((current_row - 1)* num1) + 20, 10,10])
    else:
        pygame.draw.rect(screen, 'black', [(current_col + 1)* num2, ((current_row - 1)* num1) + 20, 10,10])
    if level[current_row + 1][current_col + 1] == 0:
        pygame.draw.rect(screen, 'white', [(current_col + 1)* num2, (current_row + 1)* num1, 10,10])
    else:
        pygame.draw.rect(screen, 'black', [(current_col + 1)* num2, (current_row + 1)* num1, 10,10])


    return rect_list, count

def green_view2():
    num1 = (HEIGHT// 15)
    num2 = (WIDTH // 15)
    current_row = (green_y + 15) // 30
    current_col = (green_x + 15) // 30
    rect_list = []  # List to store rectangles
    count = 0  # Counter for the number of 1's
    pygame.draw.rect(screen, 'blue', [0, 0, 450, 450])
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                rect = pygame.rect.Rect((j * num2, i * num1), (30, 30))
                rect_list.append(rect)  # Add rectangle to the list
                count += 1  # Increment the count

    if level[current_row][current_col] == 0:
        pygame.draw.rect(screen, 'white', [current_col * num2, current_row * num1, 30,30])
    if level[current_row - 1][current_col] == 0:
        pygame.draw.rect(screen, 'white', [current_col * num2, ((current_row - 1)* num1) + 10, 30,20])
    else:
        pygame.draw.rect(screen, 'black', [current_col * num2, ((current_row - 1)* num1) + 10, 30,20])
    if level[current_row + 1][current_col] == 0:
        pygame.draw.rect(screen, 'white', [current_col * num2, (current_row + 1)* num1, 30,20])
    else:
        pygame.draw.rect(screen, 'black', [current_col * num2, (current_row + 1)* num1, 30,20])
    if level[current_row][current_col - 1] == 0:
        pygame.draw.rect(screen, 'white', [((current_col - 1)* num2) + 10, current_row * num1, 20,30])
    else:
        pygame.draw.rect(screen, 'black', [((current_col - 1)* num2) + 10, current_row * num1, 20,30])
    if level[current_row][current_col + 1] == 0:
        pygame.draw.rect(screen, 'white', [(current_col + 1)* num2, current_row * num1, 20,30])
    else:
        pygame.draw.rect(screen, 'black', [(current_col + 1)* num2, current_row * num1, 20,30])
    if level[current_row - 1][current_col - 1] == 0:
        pygame.draw.rect(screen, 'white', [((current_col - 1)* num2) + 10, ((current_row - 1)* num1) + 10, 20,20])
    else:
        pygame.draw.rect(screen, 'black', [((current_col - 1)* num2) + 10, ((current_row - 1)* num1) + 10, 20,20])
    if level[current_row + 1][current_col - 1] == 0:
        pygame.draw.rect(screen, 'white', [((current_col - 1)* num2) + 10, (current_row + 1)* num1, 20,20])
    else:
        pygame.draw.rect(screen, 'black', [((current_col - 1)* num2) + 10, (current_row + 1)* num1, 20,20])
    if level[current_row - 1][current_col + 1] == 0:
        pygame.draw.rect(screen, 'white', [(current_col + 1)* num2, ((current_row - 1)* num1) + 10, 20,20])
    else:
        pygame.draw.rect(screen, 'black', [(current_col + 1)* num2, ((current_row - 1)* num1) + 10, 20,20])
    if level[current_row + 1][current_col + 1] == 0:
        pygame.draw.rect(screen, 'white', [(current_col + 1)* num2, (current_row + 1)* num1, 20,20])
    else:
        pygame.draw.rect(screen, 'black', [(current_col + 1)* num2, (current_row + 1)* num1, 20,20])
    
    return rect_list, count

def green_view3():
    num1 = (HEIGHT// 15)
    num2 = (WIDTH // 15)
    current_row = (green_y + 15) // 30
    current_col = (green_x + 15) // 30
    rect_list = []  # List to store rectangles
    count = 0  # Counter for the number of 1's
    pygame.draw.rect(screen, 'blue', [0, 0, 450, 450])
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                rect = pygame.rect.Rect((j * num2, i * num1), (30, 30))
                rect_list.append(rect)  # Add rectangle to the list
                count += 1  # Increment the count
    for i in range(-1, 2):
        for j in range(-1, 2):
            if level[current_row + i][current_col + j] == 1:
                pygame.draw.rect(screen, 'black', [(current_col + j) * num2, (current_row + i) * num1, 30, 30])
            else:
                pygame.draw.rect(screen, 'white', [(current_col + j) * num2, (current_row + i) * num1, 30, 30])
    
    return rect_list, count

def place_green():
    check = True
    while check:
        i = random.randint(1, n-2)
        j = random.randint(1, n-2)
        if level[i][j] == 0 :
            playerx = j * 30
            playery = i * 30
            check = False
    
    return playerx, playery

def place_red():
    k = green_x // 30
    l = green_y // 30
    checks = True
    while checks:
        i = random.randint(1, n-2)
        j = random.randint(1, n-2)
        if level[i][j] == 0 and i != l and j != k:
            playerx = j * 30
            playery = i * 30
            checks = False
    
    return playerx, playery    

def draw_board():
    num1 = (HEIGHT // 15)
    num2 = (WIDTH // 15)
    rect_list = []  # List to store rectangles
    count = 0  # Counter for the number of 1's
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.rect(screen, 'black', [j * num2, i * num1, 30, 30])
                rect = pygame.rect.Rect((j * num2, i * num1), (30, 30))
                rect_list.append(rect)  # Add rectangle to the list
                count += 1  # Increment the count
    
    return rect_list, count

def draw_green():
    # RIGHT, LEFT, UP, DOWN
    if direction == 0:
        screen.blit(green_drone, (green_x, green_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(green_drone, True, False), (green_x, green_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(green_drone, 90), (green_x, green_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(green_drone, 270), (green_x, green_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT// 15)
    num2 = (WIDTH // 15)
    num3 = 15
    if centerx // 30 < 14:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 1:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 1:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 1:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 1:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 1:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 1:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 1:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 1:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 1:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 1:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 1:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 1:
                    turns[0] = True

    else:
        turns[0] = False
        turns[1] = False
    

    return turns

def move_player(play_x, play_y, direct, targetx, targety):
    # r, l, u, d
    if direct == 0:
        if targetx < play_x and turns_allowed[0]:
            play_x += speed
        elif turns_allowed[0]:
            if targety < play_y and turns_allowed[3]:
                direct = 3
                play_y += speed
            elif targety > play_y and turns_allowed[2]:
                direct = 2
                play_y -= speed
        elif not turns_allowed[0]:
            if targety < play_y and turns_allowed[3]:
                direct = 3
                play_y += speed
            elif targety > play_y and turns_allowed[2]:
                direct = 2
                play_y -= speed
            elif targetx > play_x and turns_allowed[1]:
                direct = 1
                play_x -= speed
            elif turns_allowed[3]:
                direct = 3
                play_y += speed
            elif turns_allowed[2]:
                direct = 2
                play_y -= speed
            elif turns_allowed[1]:
                direct = 1
                play_x -= speed
        else:
            play_x += speed
    
    elif direct == 1:
        if targety > play_y and turns_allowed[3]:
            direct = 3
            play_y += speed
        elif targetx > play_x and turns_allowed[1]:
            play_x -= speed
        elif not turns_allowed[1]:
            if targety > play_y and turns_allowed[3]:
                direct = 3
                play_y += speed
            elif targety > play_y and turns_allowed[2]:
                direct = 2
                play_y -= speed
            elif targetx < play_x and turns_allowed[0]:
                direct = 0
                play_x += speed
            elif turns_allowed[3]:
                direct = 3
                play_y += speed
            elif turns_allowed[2]:
                direct = 2
                play_y -= speed
            elif turns_allowed[0]:
                direct = 0
                play_x += speed
        elif turns_allowed[1]:
            if targety > play_y and turns_allowed[3]:
                direct = 3
                play_y += speed
            elif targety > play_y and turns_allowed[2]:
                direct = 2
                play_y -= speed
            else:
                play_x -= speed

    elif direct == 2:
        if targetx > play_x and turns_allowed[1]:
            direct = 1
            play_x -= speed
        elif targety > play_y and turns_allowed[2]:
            play_y -= speed
        elif not turns_allowed[2]:
            if targetx < play_x and turns_allowed[0]:
                direct = 0
                play_x += speed
            elif targetx > play_x and turns_allowed[1]:
                direct = 1
                play_x -= speed
            elif targety < play_y and turns_allowed[3]:
                direct = 3
                play_y += speed
            elif turns_allowed[1]:
                direct = 1
                play_x -= speed
            elif turns_allowed[3]:
                direct = 3
                play_y += speed
            elif turns_allowed[0]:
                direct = 0
                play_x += speed
        elif turns_allowed[2]:
            if targetx < play_x and turns_allowed[0]:
                direct = 0
                play_x += speed
            elif targetx > play_x and turns_allowed[1]:
                direct = 1
                play_x -= speed
            else:
                play_y -= speed

    elif direct == 3:
        if targety < play_y and turns_allowed[3]:
            play_y += speed
        elif not turns_allowed[3]:
            if targetx < play_x and turns_allowed[0]:
                direct = 0
                play_x += speed
            elif targetx > play_x and turns_allowed[1]:
                direct = 1
                play_x -= speed
            elif targety > play_y and turns_allowed[2]:
                direct = 2
                play_y -= speed
            elif turns_allowed[2]:
                direct = 2
                play_y -= speed
            elif turns_allowed[1]:
                direct = 1
                play_x -= speed
            elif turns_allowed[0]:
                direct = 0
                play_x += speed
        elif turns_allowed[3]:
            if targetx < play_x and turns_allowed[0]:
                direct = 0
                play_x += speed
            elif targetx > play_x and turns_allowed[1]:
                direct = 1
                play_x -= speed
            else:
                play_y += speed
    
    return play_x, play_y, direct

def get_targets():
    if green_x < 275:
        runaway_x = 450
    else:
        runaway_x = 0
    if green_y < 165:
        runaway_y = 330
    else:
        runaway_y = 0

    if stop:
        red_target = (runaway_x, runaway_y)
    else:
        red_target = (green_x, green_y)
    
    return red_target

def green_target():
    ta_x = []
    ta_y = []
    l_x = []
    l_y = []
    if m >= 2:
        for i in range(-1, m-1):
            ta_x.append(0)
            ta_y.append(0)
            l_x.append(0)
            l_y.append(0)
            ta_x[i] = red_x[i]
            ta_y[i] = red_y[i]
            if ta_x[i] < green_x:
                l_x[i] = green_x - ta_x[i]
            else:
                l_x[i] = ta_x[i] - green_x
            if ta_y[i] < green_y:
                l_y[i] = green_y - ta_y[i]
            else:
                l_y[i] = ta_y[i] - green_y
        for i in range(-1, m-2):
            if l_x[i] < l_x[i+1]:
                t_x = l_x[i]
            else:
                t_x = l_x[i+1]
            if l_y[i] < l_y[i+1]:
                t_y = l_y[i]
            else:
                t_y = l_y[i+1]
    else:
        t_x = red_x[0]
        t_y = red_y[0]

    return t_x, t_y

def check_random(pl, lr, lc):
    ran = []
    for c in range(len(red)):
            ran.append(False)
            for d in range(lc):
                if pl[c].colliderect(lr[d]):
                    ran[c] = True
                    
    return ran

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


map_button = Button(460, 90, map_img, 0.1)
rg_button = Button(460, 210, rg_img, 0.1)
start_button = Button(460, 10, start_img, 0.1)
pause_button = Button(460, 50, pause_img, 0.1)
quit_button = Button(460, 410, quit_img, 0.1)
rr_button = Button(460, 250, rr_img, 0.1)
rv_button = Button(460, 290, rv_img, 0.1)
gv_button = Button(460, 330, gv_img, 0.1)
nv_button = Button(460, 370, nv_img, 0.1)
plus_button = Button(460, 130, plus_img, 0.1)
min_button = Button(460, 170, min_img, 0.1)



level = make_map()
target_x[0], target_y[0] = switch_target()
targets[0] = (target_x[0], target_y[0])
green_x, green_y = place_green()
red_x[0], red_y[0] = place_red()


run = True
while run:
    timer.tick(fps)
    screen.fill('white') 
    center_x = green_x + 15
    center_y = green_y + 15
    player_circle = pygame.draw.circle(screen, 'white', (center_x, center_y), 15, 2)
    if normal:
        level_rect, lvl_count = draw_board()
        draw_green()
    else:
        if gv:
            if slider_value == 1:
                level_rect, lvl_count = green_view()
            if slider_value == 2:
                level_rect, lvl_count = green_view2()
            if slider_value == 3:
                level_rect, lvl_count = green_view3()
            draw_green()
    if m >0:
        for i in range(len(red)):
            target_rect[i] = pygame.Rect(target_x[i], target_y[i], target_size, target_size)
        if normal:
            level_rect, lvl_count = draw_board()
            draw_green()
            for i in range(len(red)):
                red[i] = Red(red_x[i], red_y[i], targets[i], r_speed, red_drone, red_direct[i], i)
        else:
            if gv:
                if slider_value == 1:
                    level_rect, lvl_count = green_view()
                if slider_value == 2:
                    level_rect, lvl_count = green_view2()
                if slider_value == 3:
                    level_rect, lvl_count = green_view3()
                draw_green()
                for i in range(len(red)):
                    red[i] = Red(red_x[i], red_y[i], targets[i], r_speed, red_drone, red_direct[i], i)
            if rv:
                level_rect, lvl_count = draw_board()
                for i in range(len(red)):
                    red[i] = Red(red_x[i], red_y[i], targets[i], r_speed, red_drone, red_direct[i], i)
                    if not rt[i]:
                        draw_green()
        
        if m >0:
            for k in range(len(red)):
                player_line[k] = pygame.draw.line(screen, line_color, (red[k].center_x, red[k].center_y), (center_x, center_y), 2)
        for e in range(len(red)):
            rt[e] = False
        rt = check_random(player_line, level_rect, lvl_count)

                
        for a in range(len(red)):
            if rt[a]:
                if (red[a].rect.colliderect(target_rect[a])):
                    # Generate a new random position for the target
                    target_x[a], target_y[a] = switch_target()
                    targets[a] = (target_x[a], target_y[a])
            else:
                targets[a] = get_targets()
                

        for i in range(len(red)):
            if (player_circle.colliderect(red[i].rect)):
                moving = False
                pygame.draw.rect(screen, 'black', [40, 150, 370, 150], 0, 10)
                pygame.draw.rect(screen, 'white', [60, 170, 330, 110], 0, 10)
                gameover_text = font.render('Game Over! Red Wins', True, 'black')
                screen.blit(gameover_text, (110, 215))
        gtarget_x, gtarget_y = green_target()
    turns_allowed = check_position(center_x, center_y)
    if moving:
        green_x, green_y, direction = move_player(green_x, green_y, direction, gtarget_x, gtarget_y)
        for i in range(len(red)):
            red_x[i], red_y[i], red_direct[i] = red[i].move_red()
    if map_button.draw():
        moving = False
        level = []
        level = new_map()
    if rg_button.draw():
        moving = False
        green_x, green_y = place_green()
    if start_button.draw():
        moving = True
    if pause_button.draw():
        moving = False
    if quit_button.draw():
        run = False
    if rv_button.draw():
        normal = False
        rv = True
        gv = False
    if gv_button.draw():
        normal = False
        gv = True
        rv = False
    if plus_button.draw():
        m = m + 1
        red_x.append(0)
        red_y.append(0)
        red_direct.append(0)
        red_x[m-1], red_y[m-1] = place_red()
        rt.append(False)
        target_x.append(0)
        target_y.append(0)
        target_rect.append(0)
        target_x[m-1], target_y[m-1], = switch_target()
        targets.append((target_x[m-1], target_y[m-1]))
        red.append(Red(red_x[m-1], red_y[m-1], targets[m-1], r_speed, red_drone, red_direct[m-1], m-1))
        player_line.append(0)
        print(m)
    if min_button.draw():
        if m >0:
            del red[m-1]
            del red_x[m-1]
            del red_y[m-1]
            del red_direct[m-1]
            del rt[m-1]
            del targets[m-1]
            del target_rect[m-1]
            del target_x[m-1]
            del target_y[m-1]
            del player_line[m-1]
            m = m - 1
        else:
            print("help")
    if rr_button.draw():
        moving = False
        if m >0:
            for i in range(len(red)):
                red_x[i], red_y[i] = place_red()
        else:
            print("help")
    if nv_button.draw():
        normal = True
        gv = False
        rv = False
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.Rect(slider_x, slider_y, slider_width, slider_height).collidepoint(event.pos):
                    is_dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging = False
        if event.type == pygame.MOUSEMOTION:
            if is_dragging:
                slider_position = min(max(event.pos[0], slider_x), slider_x + slider_width)
    
    slider_value = update_slider_value()
    draw_slider()
    

    pygame.display.flip()
pygame.quit()