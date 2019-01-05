#******************************************
# Game Name: Super Breakout Supreme Edition
# Creators Name: Dustin Meckley         
# File: super_breakout_supreme_edition.py
#******************************************

# -------------------------------------------------------
# Importing modules for pygame, sys, and random:
# -------------------------------------------------------
import pygame, sys, random                          # pygame for pygame module use, sys for the command line input from user use, and random for the random number generation.                                                             
from pygame.locals import *                         # All modules are imported from pygame.locals directory, importing all from the directory.                                                 

# -------------------------------------
# Display Window Size Constants:
# -------------------------------------
WIDTH = 1400                                            # Constant WIDTH declaration and initialization for the display window width.
HEIGHT = 750                                           # Constant HEIGHT declaration and initialization for the display window height.
SCREEN_SIZE = (WIDTH, HEIGHT)       # Constant SCREEN_SIZE declaration containing both the WIDTH & HEIGHT contstant for the display window as arguments.     

# -------------------
# Color Constants:
# -------------------
AQUA = (0, 255, 255)
BLACK = (0, 0, 0)	
BLUE = (0, 0, 255)
FUCHIA = (255, 0, 255) 
GREY = (128, 128, 128)
GREEN = (0, 128, 0)                                     # Paddle color.
LIME = (0, 255, 0)
MAROON = (128, 0, 0)
NAVY_BLUE = (0, 0, 128)                           # Display background color.
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)                                        
SILVER = (192, 192, 192)                            
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)                             # Ball color.
YELLOW = (255, 255, 0)                             # Block color.

# -------------------------
# Game State Constants:
# -------------------------
STATE_BALL_IN_PADDLE = 0                # STATE_BALL_IN_PADDLE constant for when the ball is in the paddle.
STATE_PLAYING = 1                               # STATE_PLAYING constant for when the game is actively being played.
STATE_WON = 2                                       # STATE_WON constant for when the game has been won.
STATE_GAME_OVER = 3                         # STATE_GAME_OVER constant for when the game is over.

# ---------------------------
# Game Object Constants:
# ---------------------------
BRICK_WIDTH   = 100                                               # BRICK_WIDTH constant for the width of the bricks.
BRICK_HEIGHT  = 30                                                # BRICK_HEIGHT constant for the height of the bricks.
BRICK_ROW = 8                                                         # BRICK_ROW constant for the amount of bricks in a row. Up to down.
BRICK_COL = 12                                                        # BRICK_COL constant for the amount of bricks in a col. Left to right.
PADDLE_WIDTH  = 80                                              # PADDLE_WIDTH constant for the width of the paddle.
PADDLE_HEIGHT = 12                                              # PADDLE_HEIGHT constant for the height of the paddle.
BALL_DIAMETER = 16                                              # BALL_DIAMETER constant for the diameter of the ball.
BALL_RADIUS   = BALL_DIAMETER // 2                 # BALL_RADIUS constant for the radius of the ball.

# ----------------------------------
# Game Object Limit Constants:
# ----------------------------------
MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH            # The maximum x direction value that the paddle can go in the display window of the game.
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10              # The constant y value that the paddle must be throughout the display window of the game.
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER             # The maximum x direction value that the ball can go in the display window of the game.
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER             # The maximum y direction value that the ball can go in the display window of the game.

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                                                               Breakout class definition:
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Breakout:                                                     
# Function to initiate Breakout class with self:
    def __init__(self):                                                                     
        
        pygame.init()                                                                                                                       # Initiate pygame module
        
        # Creating screen display and setting the caption to the window:
        self.screen = pygame.display.set_mode(SCREEN_SIZE)                                                  # pygame.display.set_mode(resolution=(0,0), flags=0, depth=0): return Surface                                                 
        pygame.display.set_caption('Super Breakout Supreme Edition by Dustin Meckley')         # pygame.display.set_caption(title, icontitle=None): return None     

        # Creating an object to help track time                                          
        self.clock = pygame.time.Clock()                                                                                        # pygame.time.Clock(): return Clock                                                   

        # Creating a new Font object for score_card and display_message functions:
        if pygame.font:                                                                                            
            self.font = pygame.font.Font(None,30)                                                                            # pygame.font.Font(object or filename, size): return Font                                                                                           
        else:                                                                               
            self.font = None                                                                

        # Function call to init_game() function:   
        self.init_game()                                                                    

# ----------------------------------
# Function to initiate the game:     
# ----------------------------------
    def init_game(self):                                                                    
        # Setting initial score_card values:
        self.lives = 3                                                                 
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        # Opening the file to store the score computation to:
        self.file = open(r'Score.txt', 'a')                        # Opening the Score.txt file for score input.
        
        # Creating paddle and ball images.               
        self.paddle = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)                                              # pygame.Rect(left, top, width, height): return Rect:                  
        self.ball = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)             # pygame.Rect(left, top, width, height): return Rect:   
        self.ball_vel = [8,-8]                                                                                                                                                   # Ball velocity object list [x = 8, y = -8]. Controls speed of the ball movement.    
        self.paddle_vel = 10                                                                                                                                                    # Paddle velocity object. x = 10. Controls speed of the paddles movement

        # Function call to create_bricks() function: 
        self.create_bricks()                                                            
        
# --------------------------------------------------------------------
# Function for creation of the bricks into a list for access later:    
# --------------------------------------------------------------------  
    def create_bricks(self):                                                                
        y_offset = 75                                                                                                                                           # y_offset of bricks from the origin of the screen: Vertical Offset.                                                                          
        self.bricks = []                                                                                                                                        # Creation of empty list object self.bricks to store bricks in.                                                                    
        for i in range(BRICK_ROW):                                                                                                                # Laying out the brick rows. Vertical.                                                          
            x_offset = 35                                                                                                                                      # x_offset of bricks from the origin of the screen: Horizontal Offset.                                                                  
            for j in range(BRICK_COL):                                                                                                             # Laying out the brick cols. Horizontal.
                self.bricks.append(pygame.Rect(x_offset,y_offset,BRICK_WIDTH,BRICK_HEIGHT))             # pygame.Rect(left, top, width, height): return Rect:   
                x_offset += BRICK_WIDTH + 10                                                                                                 # Incrementing the x_offset for display of the bricks from the list                                                  
            y_offset += BRICK_HEIGHT + 5                                                                                                     # Incrementing the y_offset for display of the bricks from the list 
            
# --------------------------------------------------------------------------------------------
# Function for drawing of the bricks onto the screen surface within window display:  
# --------------------------------------------------------------------------------------------
    def draw_bricks(self):                                                                    
        for brick in self.bricks:                                                                                           # Accessing the list object self.bricks to draw the bricks onto surface of screen.                                                        
            pygame.draw.rect(self.screen, YELLOW, brick)                                               # pygame.draw.rect(Surface, color, Rect, width=0): return Rect                                          
            
# --------------------------------------------------------------
# Function for paddle movement within window display:  
# --------------------------------------------------------------                                                                                                                                                                   
    def move_paddle(self):                                                                                                            
        keys = pygame.key.get_pressed()                                                                          # pygame.key.get_pressed(): return bools 
        
        # Paddle -x movement velocities:
        if keys[pygame.K_LEFT]:                                                                                     # Left arrow key pressed                                                          
            self.paddle.left -= self.paddle_vel                                                                    # Move paddle to the left                                                         
            if self.paddle.left < 0:                                                                                       # If paddle exceeds left side of screen                                                    
                self.paddle.left = 0                                                                                        # then set it back to 0.                                                   
        # Paddle +x movement velocities:
        if keys[pygame.K_RIGHT]:                                                                                  # Right arrow key pressed                                                         
            self.paddle.left += self.paddle_vel                                                                   # Move paddle to the right                                                          
            if self.paddle.left > MAX_PADDLE_X:                                                          # If paddle exceeds right side of screen                                            
                self.paddle.left = MAX_PADDLE_X                                                          # then set it back to the maximum paddle x coordinate.
    
        # Start of game:
        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:     # Space key pressed and self.state == 0                                                                                                                               
            self.state = STATE_PLAYING                                                                       # then set self.state == 1
        # End of game:
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):          # Return key pressed and self.state == 2 or 3    
            self.init_game()                                                                                                                                                     # then call function to initiate game.                                                                   
            
# -----------------------------------------------------------
# Function for ball movement within window display:
# -----------------------------------------------------------            
    def move_ball(self):
        # Starting the ball movement:
        self.ball.left += self.ball_vel[0]                          # x direction ball movement = self.ball_vel[0], Starting ball movement to the left                          
        self.ball.top  += self.ball_vel[1]                         # y direction ball movement = self.ball_vel[1], Starting ball movement to bounce off of paddle.           

        # Ball x direction velocities:
        # -x (left) side limits:
        if self.ball.left <= 0:                                             # if self.ball.left <= 0                                    
            self.ball.left = 0                                                # then set self.ball.left = 0                                    
            self.ball_vel[0] = -self.ball_vel[0]                  # and set self.ball_vel[0] = -self.ball_vel[0] which reverses the direction of the ball back towards the right.
        # +x (right) side limits:
        elif self.ball.left >= MAX_BALL_X:                  # elif self.ball.left >= MAX_BALL_X                       
            self.ball.left = MAX_BALL_X                        # then set self.ball.left = MAX_BALL_X                                           
            self.ball_vel[0] = -self.ball_vel[0]                  # and set self.ball_vel[0] = -self.ball_vel[0] which reverses the direction of the ball back towards the left.
            
        # Ball y direction velocities:
        # - y (top) side limits:
        if self.ball.top < 0:                                               # if self.ball.top < 0                                       
            self.ball.top = 0                                               # then set self.ball.top = 0                                       
            self.ball_vel[1] = -self.ball_vel[1]                 # and set self.ball_vel[1] = -self.ball_vel[1] which reverses the direction of the ball back towards the bottom.
            
# ---------------------------------------------------------------------
# Function for detecting collisions of ball to bricks and paddle:
# ---------------------------------------------------------------------
    def collisions(self):
        # Collision ball to bricks:
        for brick in self.bricks:                                                        
            if self.ball.colliderect(brick):                        # Rect.colliderect(Rect): return bool
                self.score += 3                                           # if ball collides with bricks then increment score by 5
                self.ball_vel[1] = -self.ball_vel[1]            # and set self.ball_vel[1] = -self.ball_vel[1] which reverses the direction of the ball back towards the bottom.           
                self.bricks.remove(brick)                           # and remove the brick from the list self.bricks                                                     
                break
                    
        # List of bricks empty- game won:
        if len(self.bricks) == 0:                                       # if the list self.bricks == 0                            
            self.state = STATE_WON                              # then change the self.state == 2.

        # Collision ball to paddle:  
        if self.ball.colliderect(self.paddle):                                          # Rect.colliderect(Rect): return bool                       
            self.ball.top = PADDLE_Y - BALL_DIAMETER                # if ball collides with paddle then set self.ball.top = PADDLE_Y - BALL_DIAMETER             
            self.ball_vel[1] = -self.ball_vel[1]                                       # and set self.ball_vel[1] = -self.ball_vel[1] which reverses the direction of the ball back towards the top.
        # Ball passes paddle:
        elif self.ball.top > self.paddle.top:                                           # elif ball passes paddle by self.ball.top > self.paddle.top                           
            self.lives -= 1                                                                       # then decrement lives by 1                                       
            if self.lives > 0:                                                                    # if lives is greater than 0                                     
                self.state = STATE_BALL_IN_PADDLE                        # then continue the game by setting self.state == 0                    
            else:                                                                                      # otherwise end the game by                  
                self.state = STATE_GAME_OVER                                 # setting self.state == 3 
                
# ---------------------------------------------------------------
# Function for printing the score and lives onto the screen:
# ---------------------------------------------------------------
    def score_card(self):                                           
        if self.font:
            font_score = self.font.render("SCORE: " + str(self.score), False, WHITE)         # Font.render(text, antialias, color, background=None): return Surface             
            font_lives = self.font.render("LIVES: " + str(self.lives), False, WHITE)            # Font.render(text, antialias, color, background=None): return Surface             
            self.screen.blit(font_score, (WIDTH / 4, 5))                                                        # Surface.blit(source, dest, area=None, special_flags = 0): return Rect                                     
            self.screen.blit(font_lives, (WIDTH - WIDTH / 4, 5))                                        # Surface.blit(source, dest, area=None, special_flags = 0): return Rect
            
# -------------------------------------------------------
# Function for printing the messages on the screen:
# -------------------------------------------------------         
    def display_message(self, message):                                     
        if self.font:                                                   
            size = self.font.size(message)                                                                              # Font.size(text): return (width, height)                                             
            font_surface = self.font.render(message,False, WHITE)                                    # Font.render(text, antialias, color, background=None): return Surface        
            x = (SCREEN_SIZE[0] - size[0]) / 2                                                                 # Message display x coordinate location                        
            y = (SCREEN_SIZE[1] - size[1]) / 2                                                                 # Message display y coordinate location                        
            self.screen.blit(font_surface, (x,y))                                                                    # Surface.blit(source, dest, area=None, special_flags = 0): return Rect
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                               Main function to start game execution and call other functions:
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def main(self):
        while 1:            
            for event in pygame.event.get():                                                                        # pygame.event.get(): return Eventlist
                if event.type == pygame.QUIT:
                    sys.exit
    
            # Limits the runtime speed of the game by 50 frames per second:  
            self.clock.tick(50)                                                                                             # Clock.tick(framerate=0): return milliseconds
            
            # Fills the screen Surface with a solid color:
            self.screen.fill(NAVY_BLUE)                                                                         # Surface.fill(color, rect=None, special_flags=0): return Rect
            
            # Function call to move_paddle() function:
            self.move_paddle()
            
            # State Playing the Game:
            if self.state == STATE_PLAYING:                                                                 # if self.state == 1                                    
                self.move_ball()                                                                                          # then call the function move_ball()                                            
                self.collisions()                                                                                           # and call the function collisions
                
            # State Ball in the Paddle:
            elif self.state == STATE_BALL_IN_PADDLE:                                            # elif self.state == 0                          
                self.ball.left = self.paddle.left + self.paddle.width / 2                               # then set self.ball.left = self.paddle.left + self.paddle.width / 2         
                self.ball.top  = self.paddle.top - self.ball.height                                         # and set self.ball.top  = self.paddle.top - self.ball.height and display message to continue. 
                self.display_message("PRESS SPACE TO LAUNCH THE BALL")         # Function call to display_message() function:
                
            # State Game Over:
            elif self.state == STATE_GAME_OVER:                                                                                                         # elif self.state == 3 then display message game over.
                self.file.write(str(self.score) + '\n')                                                                                                               # Writing the highest score of the game to the Score.txt fill.                                          
                self.file.close()                                                                                                                                              # Closing  the file used to store the score computation.
                self.file = open(r'C:\p\Score.txt', 'r')            # Opening the self.file object to read from the file.
                array = []                                                                                                                                                       # List named array to store the file highest score values at.
                for i in self.file:                                                                                                                                             # for loop to append the values from the file into the list named array.
                    tokens = i.split(',')                                                                                                                                     # Removing the token , that sepearates the values within the file for preparation of appending to the list. 
                    array.append(max(int(t) for t in tokens[:]))                                                                                               # Appending the values from the file into the list removing the tokens. 
                max_value = max(array)                                                                                                                               # Storing the maximum value from the list named array into variable named max-value.
                game_over_string = "GAME OVER! - HIGHEST SCORE: " + str(max_value)                                          # Creating a string for when the game is over and the player has lost to send to message display.
                self.display_message(game_over_string)                                                                                                     # Calling the function display_message and sending the game_over_string over in the argument list. 
                
            # State Game Won:
            elif self.state == STATE_WON:                                                                                                                        # elif self.state == 2 then display message you won the game.                                      
                self.file.write(str(self.score) + '\n')                                                                                                                # Writing the highest score of the game to the Score.txt fill.
                self.file.close()                                                                                                                                               # Closing  the file used to store the score computation:
                self.file = open(r'C:\p\Score.txt', 'r')             # Opening the self.file object to read from the file.
                array = []                                                                                                                                                         # List named array to store the file highest score values at.
                for i in self.file:                                                                                                                                               # for loop to append the values from the file into the list named array.
                    tokens = i.split(',')                                                                                                                                        # Removing the token , that sepearates the values within the file for preparation of appending to the list. 
                    array.append(max(int(t) for t in tokens[:]))                                                                                                  # Appending the values from the file into the list removing the tokens. 
                max_value = max(array)                                                                                                                                  # Storing the maximum value from the list named array into variable named max-value.
                winner_winner_chicken_dinner_string = "YOU WON! - HIGHEST SCORE: " + str(max_value)                 # Creating a string for when the game is over and the player has won to send to message display
                self.display_message(winner_winner_chicken_dinner_string)                                                                       # Calling the function display_message and sending the winner_winner_chicken_dinner_string over in the argument list. 
                
            # Function call to draw_bricks() function:   
            self.draw_bricks()                                                                                              

            # Draw the paddle to the screen surface:
            pygame.draw.rect(self.screen, GREEN, self.paddle)                               # pygame.draw.rect(Surface, color, Rect, width=0): return Rect                             

            # Draw the ball to the screen surface:
            # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)

            # Function call to score_card() function:
            self.score_card()                                                                                                   

            # Updates the full display Surface to the screen:
            pygame.display.flip()                                                                           # pygame.display.flip(): return None 
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------           
#                                                                       Function call for the Breakout Class objects and for the Main Function:
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    Breakout().main()
