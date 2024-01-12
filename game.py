import pygame 
from pygame.locals import * 
import time
import random
import os 


SIZE = 32 #i want to use increments of 16/32/64
BACKGROUND_COLOUR = (255,255,255) # change later

class Apple:
    def __init__(self, parent_screen):
        self.apple = pygame.image.load("resources/apple2.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3
    
    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24) * SIZE
        self.y = random.randint(0,24) * SIZE

class Snake: 
    def __init__(self, parent_screen, length):
        self.length = length 
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block2.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def move_up(self):
        self.direction = "up"
    def move_down(self):
        self.direction = "down"
    def move_right(self):
        self.direction = "right"
    def move_left(self):
        self.direction = "left"

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
    
        self.draw()

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOUR)
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

class Game:
    def __init__(self):
        
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        pygame.init()
        self.surface = pygame.display.set_mode((screen_width-20,screen_height-20), pygame.RESIZABLE) #size of display
        self.surface.fill(BACKGROUND_COLOUR) 
        self.snake = Snake(self.surface, 7)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    def collision(self, x1, y1, x2, y2): 
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(1,self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occured"
            
    def game_over(self):
        self.surface.fill(BACKGROUND_COLOUR)
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render("Gamer Over :(", True, (0,0,0))
        self.surface.blit(line1,(200,300))
        line2 = font.render(f"Your score is: {self.snake.length}", True, (0,0,0))
        self.surface.blit(line2,(200,350))
        line3 = font.render("To play again press Enter. To exit press Escape!", True, (0,0,0))
        self.surface.blit(line3,(200,400))
        pygame.display.flip()
    
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (0,0,0))
        self.surface.blit(score,(800,10))

    def run (self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False 
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:    
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.1)

if __name__ == "__main__":
    game = Game()
    game.run()

