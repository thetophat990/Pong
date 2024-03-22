import pygame
from random import random

class Colors:
    FG_COLOR = (255,255,255)
    LEFT = (255, 0, 0)
    RIGHT = (0, 0, 255)
    BG_COLOR = (0,0,0)
    
class Config:
    WINDOW_DIMENSIONS = (600,400) #x,y 600,400
    PADDLE_DIMENSIONS = (WINDOW_DIMENSIONS[0] //  40,WINDOW_DIMENSIONS[1] // 4)
    PADDLE_EDGE_OFFSET = 15
    BALL_RADIUS = 7
    STARTING_VELOCITY_RANGE = 5
    SPEED_INCREMENT_VAL = 0.001
    CONTROLES = {
        "left_up" : pygame.K_w,
        "left_down" : pygame.K_s,
        "right_up" : pygame.K_UP,
        "right_down" : pygame.K_DOWN,
        "reset" : pygame.K_r
    }
    
    FONT = None
    FONT_SIZE = 50
    WINDOW_NAME = "pong!"
    
    CENTER_DIMENSIONS = (WINDOW_DIMENSIONS[0] // 2, WINDOW_DIMENSIONS[1] // 2)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, paddle_dim, x, y, col) -> None:
        super().__init__()
        self.dims = [x, y]
        
        self.image = pygame.Surface(paddle_dim)
        self.image.fill(col)
        self.rect = self.image.get_rect(topleft=self.dims)
        
    def update(self, y) -> None:
        self.dims[1] += y
        self.rect.y = self.dims[1]

    
class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, window_dims, center_dims) -> None:
        super().__init__()
        
        self.radius = radius
        self.window_dims = window_dims
        self.center_dims = center_dims
        self.dims = self.center_dims
        
        self.random_velocity = lambda: [random() * Config.STARTING_VELOCITY_RANGE - 1 for _ in range(2)]
        
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius))
        pygame.draw.circle(self.image, Colors.FG_COLOR, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect().topleft = self.dims
        self.veloc = self.random_velocity()
        
    def update(self, sprites, score) -> None:
        self.dims = [x + y for x, y in zip(self.dims, self.veloc)]
        self.rect = self.image.get_rect(topleft=self.dims)
        
        if self.dims[1] <= 0 or self.dims[1] >= self.window_dims[1]:
            self.veloc = [self.veloc[0], self.veloc[1] * -1]

        if self.dims[0] <= 0:
            score[0] += 1
            self.dims = self.center_dims
            self.veloc = self.random_velocity()
            
        if self.dims[0] >= self.window_dims[0]:
            score[1] += 1
            self.dims = self.center_dims
            self.veloc = self.random_velocity()
            
        for sprite in sprites:
            if self.rect.colliderect(sprite.rect):
                self.veloc = [self.veloc[0] * -1, self.veloc[1]]
                
        self.veloc = [e + Config.SPEED_INCREMENT_VAL if e >= 0 else e - Config.SPEED_INCREMENT_VAL for e in self.veloc]
                
def run():
    score = [0, 0]
    pygame.init()
    
    screen = pygame.display.set_mode(Config.WINDOW_DIMENSIONS)
    font = pygame.font.Font(Config.FONT, Config.FONT_SIZE)
    pygame.display.set_caption(Config.WINDOW_NAME)
    clock = pygame.time.Clock()
    
    sprites = pygame.sprite.Group()
    
    Lpaddle = Paddle(Config.PADDLE_DIMENSIONS, Config.PADDLE_EDGE_OFFSET,
                     Config.CENTER_DIMENSIONS[1] - (Config.PADDLE_DIMENSIONS[1] // 2), Colors.LEFT)
    
    Rpaddle = Paddle(Config.PADDLE_DIMENSIONS, Config.WINDOW_DIMENSIONS[0] - Config.PADDLE_DIMENSIONS[0] - Config.PADDLE_EDGE_OFFSET,
                     Config.CENTER_DIMENSIONS[1] - (Config.PADDLE_DIMENSIONS[1] // 2), Colors.RIGHT)
    
    ball = Ball(Config.BALL_RADIUS, Config.WINDOW_DIMENSIONS, Config.CENTER_DIMENSIONS)
    
    sprites.add(Lpaddle, Rpaddle, ball)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        
        if keys[Config.CONTROLES["left_up"]]:
            Lpaddle.update(-2)
        elif keys[Config.CONTROLES["left_down"]]:
            Lpaddle.update(2)
        if keys[Config.CONTROLES["right_up"]]:
            Rpaddle.update(-2)
        elif keys[Config.CONTROLES["right_down"]]:
            Rpaddle.update(2)
            
        if keys[Config.CONTROLES["reset"]]:
            run()
        
            
        screen.fill(Colors.BG_COLOR)
        
        pygame.draw.line(screen, Colors.FG_COLOR, (Config.CENTER_DIMENSIONS[0], 0), (Config.CENTER_DIMENSIONS[0], Config.WINDOW_DIMENSIONS[1]))
        
        ball.update((Lpaddle, Rpaddle), score)
        
        lscore = font.render(str(score[0]), True, Colors.LEFT)
        rscore = font.render(str(score[1]), True, Colors.RIGHT)
        
        screen.blit(lscore, (Config.CENTER_DIMENSIONS[0] // 2 - lscore.get_width() // 2, 2 + lscore.get_height() // 2))
        screen.blit(rscore, ((Config.CENTER_DIMENSIONS[0] // 2) + Config.CENTER_DIMENSIONS[0] - rscore.get_width() // 2,
                             2 + lscore.get_height() // 2))       
        
        sprites.draw(screen) 

        pygame.display.flip()

        clock.tick(60)   
    
    quit()

if __name__ == "__main__":
    run()
