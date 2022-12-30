"""
    Date : Fri Dec 30 2022 17:57:33 GMT+0530 (India Standard Time)
    Author : Suman Gurung
    Description : Pong Game in Python using pygame module
"""

import pygame
pygame.init()

# CONSTANTS
# window dimension 
WIDTH , HEIGHT = 700 , 500

# frame per second
FPS = 60

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (234,255,0)

# paddle dimension
PADDLE_WIDTH , PADDLE_HEIGHT = 20,100

# score font
SCORE_FONT = pygame.font.SysFont("comicsans",25)


# SETUP
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")



# Paddle 
class Paddle:
    PADDLE_COLOR = WHITE
    
    # speed of movement of paddle
    VEL = 4  
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,win):
        pygame.draw.rect(win , self.PADDLE_COLOR , (self.x,self.y,self.width,self.height))

    def move(self,up=True):
        if up:
            self.y = self.y - self.VEL
        else:
            self.y = self.y + self.VEL


# Ball
class Ball:
    
    BALL_COLOR = YELLOW

    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = 3
        self.y_vel = 3

    def draw(self,win):
        pygame.draw.circle(win,self.BALL_COLOR ,(self.x , self.y), self.radius)

    def move(self):
        self.x = self.x + self.x_vel
        self.y = self.y + self.y_vel


# Draw on window
def draw(win , paddles , ball , scores):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"Player A : {scores[0]}", 1 , WHITE)
    right_score_text = SCORE_FONT.render(f"Player B : {scores[1]}", 1 , WHITE)

    for paddle in paddles:
        paddle.draw(win)

    win.blit(left_score_text , (WIDTH//4 - 25, 30))
    win.blit(right_score_text , (WIDTH*3//4 - 35, 30))

    ball.draw(win)    
    pygame.display.update()


# paddle movement
def handle_paddle_movement(keys,left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL>=0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VEL<=HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL>=0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.VEL<=HEIGHT:
        right_paddle.move(up=False)


# ball movement
def handle_ball_movement(ball , left_paddle, right_paddle):
    
    # for top and bottom (Y)
    if ball.y - ball.radius <=0:  
        ball.y_vel *= -1 
    if ball.y + ball.radius >=HEIGHT:   
        ball.y_vel *= -1 

    # for left and right (X)
    # ball going left
    if(ball.x_vel<0):
        #if collided with paddle       
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y+left_paddle.height:
            if ball.x-ball.radius <= left_paddle.x+left_paddle.width:
                
                # change ball X-direction
                ball.x_vel *= -1   
                
                # changing Y-direction based on hit position of ball in paddle
                paddle_middle = left_paddle.y + left_paddle.height//2
                displacement_from_middle = paddle_middle - ball.y

                if displacement_from_middle<0 :
                    displacement_from_middle *= -1
                
                if(displacement_from_middle>30 and displacement_from_middle<40):
                    if ball.y_vel<0:
                        ball.y_vel = -4
                    else:
                        ball.y_vel = 4

                if(displacement_from_middle>40 and displacement_from_middle<50):
                    if ball.y_vel<0:
                        ball.y_vel = -6
                    else:
                        ball.y_vel = 6

                if(displacement_from_middle>0 and displacement_from_middle<30):
                    if ball.y_vel<0:
                        ball.y_vel = -3
                    else:
                        ball.y_vel = 3
    
    # ball going right             
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y+right_paddle.height:
            if ball.x+ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                paddle_middle = right_paddle.y + right_paddle.height//2
                displacement_from_middle = paddle_middle - ball.y

                if displacement_from_middle<0 :
                    displacement_from_middle *= -1
                
                if(displacement_from_middle>30 and displacement_from_middle<40):
                    if ball.y_vel<0:
                        ball.y_vel = -4
                    else:
                        ball.y_vel = 4

                if(displacement_from_middle>40 and displacement_from_middle<50):
                    if ball.y_vel<0:
                        ball.y_vel = -6
                    else:
                        ball.y_vel = 6

                if(displacement_from_middle>0 and displacement_from_middle<30):
                    if ball.y_vel<0:
                        ball.y_vel = -3
                    else:
                        ball.y_vel = 3

    ball.move()


# reset ball and paddle
def reset(ball , left_paddle , roght_paddle):
    if ball.x+ball.radius >=700 or ball.x - ball.radius <= 0:
        ball.x = WIDTH//2
        ball.y = HEIGHT//2


# MAIN EVENT LOOP
def main():

    left_paddle = Paddle(0 , HEIGHT//2 - PADDLE_HEIGHT//2 , PADDLE_WIDTH , PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - PADDLE_WIDTH , HEIGHT//2 - PADDLE_HEIGHT//2 , PADDLE_WIDTH , PADDLE_HEIGHT)

    ball = Ball(WIDTH//2 , HEIGHT//2 , 10)

    left_score = 0
    right_score = 0 

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        draw(WIN , [left_paddle , right_paddle] , ball , [left_score , right_score])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()  

        handle_paddle_movement(keys,left_paddle,right_paddle)
        handle_ball_movement(ball,left_paddle,right_paddle)

        if ball.x+ball.radius >= WIDTH:
            left_score+=1
            reset(ball , left_paddle,right_paddle)
        if ball.x - ball.radius <= 0:
            right_score+=1
            reset(ball,left_paddle,right_paddle)

    pygame.quit()


if __name__=="__main__":
    main()
