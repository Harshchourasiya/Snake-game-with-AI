import pygame, random, sys
import tkinter as tk
from tkinter import messagebox
from ai import ai
from pygame import mixer
# Class Starts ----

# Snake player Class
class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = main_blue
        self.score = 0
    
    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length>1 and (point[0]*-1, point[1]*-1)==self.direction:
            return
        else :
            self.direction = point

    def move(self):
        current = self.get_head_position()
        x,y = self.direction
        new_pos = (((current[0]+(x*grid_size))%screen_width), (current[1]+(y*grid_size))%screen_height)
        if len(self.positions) > 2 and new_pos in self.positions[2:]:
            self.message_box("Game Over", "Play Again")
            self.reset()
        else :
            self.positions.insert(0,new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
    
    def draw(self, screen):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (grid_size,grid_size))
            pygame.draw.rect(screen, self.color, r)
            # pygame.draw.rect(screen, light_blue, r, 1)
    
    def control_key(self):
        global is_intro
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reset()
                is_intro = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
    
    def message_box(self,subject, content):
       root = tk.Tk()
       root.attributes("-topmost", True)
       root.withdraw()
       messagebox.showinfo(subject, content)
       try:
          root.destroy()
       except:
          pass
    
    def score_controller(self,screen):
        myfont = pygame.font.SysFont('freesansbold.ttf',25)
        score_title = "Score:- {}".format(self.score)
        pygame.display.set_caption(score_title)
        text = myfont.render(score_title, True, cream, main_blue)
        screen.blit(text, (0, 0))
 
# Snake Food Class
class Food(object):
    def __init__(self, positions):
        self.position = (0,0)
        self.color = cream
        self.generate_food(positions)

    def generate_food(self, positions):
        ran_x = random.randint(0, grid_width-1)
        ran_y = random.randint(0, grid_height-1)
        new_pos = ((ran_x*grid_size)%screen_width, (ran_y*grid_size)%screen_height)
        while new_pos in  positions:
           ran_x = random.randint(0, grid_width-1)
           ran_y = random.randint(0, grid_height-1)
           new_pos = ((ran_x*grid_size)%screen_width, (ran_y*grid_size)%screen_height)
        self.position = (ran_x*grid_size, ran_y*grid_size)

    def draw(self, screen):
        r = pygame.Rect((self.position[0], self.position[1]), (grid_size, grid_size))
        pygame.draw.rect(screen, self.color, r)
        # pygame.draw.rect(screen, main_blue, r, 1)

# Introduction Page Class
class Intro():
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self):
        text = self.font.render("WELCOME TO SNAKE GAME", True, cream, main_blue)
        textbox = text.get_rect()
        textbox.center = (screen_width/2, 100)
        self.screen.blit(text, textbox)

    def exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def play_button(self, mess, y):
        x = screen_width/2;
        self.text_render(mess, x, y, cream, main_blue)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        tx, ty = self.font.size(mess)
        if x-(tx/2)<mouse[0]<x+(tx/2) and y-(ty/2)<mouse[1]<y+(ty/2):
            self.text_render(mess, x,y, main_blue, cream)
            if click[0] :
               return True
        
        return False
        
    def ai_button(self, mess, y):
        global is_ai_play
        is_ai_play = self.play_button(mess,y);
        return is_ai_play        

    def text_render(self, mess, x,y, first, second):
        text = self.font.render(mess, True, first, second)
        textbox = text.get_rect()
        textbox.center = (x,y)
        self.screen.blit(text, textbox)
# Class End ----


# Methods Start ---
# Useful Methods 
def drawGrid(surface):
    r = pygame.Rect((0,0), (screen_width,screen_height))
    pygame.draw.rect(surface,dark_blue,r)

def start_game(surface,snake, food):
    snake.control_key()
    drawGrid(surface)
    snake.move()
    snake.score_controller(surface)
    if snake.get_head_position()== food.position:
        snake.length+=1
        snake.score+=1
        mixer.music.play()
        food.generate_food(snake.positions)
    snake.draw(surface)
    food.draw(surface)


# Methods End ----

# Variable Start ----
# Important Variable of the game
screen_width = 600
screen_height = 600

grid_size = 20
grid_width = screen_width/grid_size;
grid_height = screen_height/grid_size;

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

is_playing = True
is_intro = True
title = "Snake Game"

# colors
light_blue = (196, 221, 255)
dark_blue = (127, 181, 255)
main_blue = (0, 29, 110)
cream =  (254, 226, 197)
is_ai_play = False
# Variable End ----

# Main Method
def main():
    global is_intro
    pygame.init()
    mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    myfont = pygame.font.SysFont("monospace",25)
    snake = Snake()
    food = Food(snake.positions)
    intro = Intro(surface,myfont)
    mixer.music.load("audio/eat.wav")
    mixer.music.set_volume(0.7)
    drawGrid(surface)
    pygame.display.set_caption(title)
    while (is_playing):
        clock.tick(10)

        if(is_intro):
            drawGrid(surface)
            intro.draw()
            intro.exit()
            is_intro = not (intro.play_button("Play", 200) or intro.ai_button("AI Play", 350))
        else:
           start_game(surface, snake, food)
           if(is_ai_play): 
               Ai = ai(snake.direction,food.position, snake.get_head_position(), snake.positions)
               Ai.start()    
            
        screen.blit(surface, (0,0))
        pygame.display.update()




main()