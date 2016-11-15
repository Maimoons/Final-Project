import pygame
import math
import os, pygame
from pygame.locals import *
from pygame.compat import geterror


#    15-112: Principles of Programming and Computer Science
#    Project: Carrom Board
#    Name      : Maimoon
#    AndrewID  : maimoons

#    File Created: 
#    Modification History:
#    Start:10/11/2016 8:00 pm   End:10/11/2016 11:59 pm
#    11/11/2016 :12:00 am        11/11/2016:7:00 am
#    11/11/2016 :1:00 pm        11/11/2016:4:00 pm
#    11/11/2016 :10:00 pm        11/12/2016:3:00 am
#    11/12/2016 :1:00 pm        11/12/2016 :5:00 pm
#    11/12/2016: 8:00 pm          11/12/2016 :12:00 pm

    
                       
############################################################CLASSES ###############################################################################################################################     
class piece(): #this is the class for all the carrom pieces   
    def __init__(self,color,y,x,r):
        self.color=color
        self.y=y
        self.x=x
        self.radius=r
        self.horizontal_velocity=0  # the velocity in the horizontal direction
        self.vertical_velocity=0    #the velocity in the vertical direction
        self.velocity=0             #the absolute value of the velocity
        self.sinX=0                 #X is the angle between the vector joining the centerpoints of the: self piece and any piece which collides with it, and the horizontal
        self.cosX=0
        self.tanX=0


    def angle(self,x,y):   #calculates the angle between piece's  midpoint and any point on the board
        self.tanX=float(y-self.y)/float(x-self.x)
        hypotenuse=((y-self.y)**2)+((x-self.x) **2)**0.5
        self.cosX=(x-self.x)/hypotenuse
        self.sinX=(y-self.y)/hypotenuse

        if self.cosX>0 and self.sinX<0:    #changes to conventional quadrant system
            self.sinX=self.sinX *(-1)

        if self.cosX<0 and self.sinX<0:
            self.sinX=self.sinX *(-1)

        if self.cosX<0 and self.sinX>0:
            self.sinX=self.sinX *(-1)

        if self.cosX>0 and self.sinX>0:
            self.sinX=self.sinX *(-1)
            
            
       
    def move_withcursor(self,x,y):  #for hovering the striker with the cursor
        self.x=x
        self.y=y
        
    #u is the initial velocity of the piece which is colliding with this self piece
    #similarly, x and y are the midpoint coordinates of the piece which is colliding with this self piece
    def move(self,u,x,y): #for angles between self piece and onther piece which is colliding with it
        
        self.tanX=float(y-self.y)/float(x-self.x)  #calculates the tangent of the angle between the line joining the 2 midpoints( this self piece and the colliding piece) and the horizontal
        hypotenuse=((y-self.y)**2)+((x-self.x) **2)**0.5
        self.cosX=(x-self.x)/hypotenuse
        self.sinX=(y-self.y)/hypotenuse
        if self.cosX>0 and self.sinX<0:
            self.sinX=self.sinX *(-1)

        if self.cosX<0 and self.sinX<0:
            self.sinX=self.sinX *(-1)

        if self.cosX<0 and self.sinX>0:
            self.sinX=self.sinX *(-1)

        if self.cosX>0 and self.sinX>0:
            self.sinX=self.sinX *(-1)
        sinX2,cosX2,tanX2 = self.cosX,self.sinX,1/self.tanX  # sinX2=90-cosX1, cosX2=90-sinX1, tanX2=90-tanX1
        
        self.velocity=((cosX2)/(self.cosX))*(u)+(self.tanX)*((u/2)*(((sinX2)/(self.sinX))-((self.cosX *cosX2)/(self.sinX)**2))) #calculates the velocity of this stationar self piece due to collision with a moving particle
        if self.velocity>50:  
            self.velocity=0
            print self.cosX, self.sinX, self.tanX, u
            
        self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
        self.vertical_velocity=self.velocity*(self.sinX)
       

    def residual(self,u): #the backward velocity of the piece which collided with this self piece
        sinX2,cosX2,tanX2 = self.cosX,self.sinX,1/(self.tanX)  # sinX2=90-cosX1, cosX2=90-sinX1, tanX2=90-tanX1
        
        velocity=(u/2)*(((sinX2)/(self.sinX))-((self.cosX*cosX2)/(self.sinX)*2))
        
        return [velocity, sinX2, cosX2, tanX2] #the angles with which the colliding object should move

    def deceleration(self): # decreases the absolute velocity of the self piece to 0
        self.horizontal_velocity=self.velocity *(self.cosX) #calculates vertical and horizontal components
        self.vertical_velocity=self.velocity*(self.sinX)
        
        if self.velocity>0 and self.cosX>0:  # if angle in first quadrant #moving towards North-East
            print 'positive velocity'
            self.x=self.x+self.horizontal_velocity #increasing the x midpoint coordinates of this self piece
            self.y=self.y-self.vertical_velocity #increasing the y midpoint coordinates of this self piece
            self.velocity=self.velocity-0.5  #decelearating the absolute velocity which affects the horizontal and vertical componenets of the velocity
            if self.velocity<0:
                self.velocity=0


        elif self.velocity>0 and self.cosX<0: #if angle in second quadrant # moving towards North-West
            print 'positive velocity'
            self.x=self.x+self.horizontal_velocity #increasing the x midpoint coordinates of this self piece
            self.y=self.y-self.vertical_velocity #increasing the y midpoint coordinates of this self piece
            self.velocity=self.velocity-0.5  #decelearating the absolute velocity which affects the horizontal and vertical componenets of the velocity
            if self.velocity<0:
                self.velocity=0
            
            
            
        elif self.velocity<0 and self.cosX<0: # same stuff but in this case the velocity is in negative direction
            print 'negative velocity1',self.velocity
            self.x=self.x-self.velocity
            self.y=self.y+self.velocity
            self.velocity=self.velocity+0.5
            if self.velocity>0:
                self.velocity=0

            


        else:
            print 'negative velocity2',self.velocity
            self.x=self.x-self.velocity
            self.y=self.y+self.velocity
            self.velocity=self.velocity+0.5
            if self.velocity>0:
                self.velocity=0

        
                
        
        
        self.horizontal_velocity=self.velocity *(self.cosX) #calculates the horizontal component of velocity
        self.vertical_velocity=self.velocity*(self.sinX) #calculates the vertical componenet of velocity
        print math.asin(self.sinX)

        
        
    def pocketting(self): # checks if the piece is within the vicinity of the four pockets 
        global piecelist
        pockets = [(86,84),(885,84),(885,863),(86,863)] # the midpoint coordinates of the four pockets 
        for midpoints in pockets:
            if ((self.x-midpoints[0])**2)+((self.y-midpoints[1])**2)==(15+15)**2: #checks whether within circular loci of the pockets #remember to calculate the right radius 
                if self.color==white:
                    score=score_list[player]+20 #adds to the score the piece which is pocketed #20 pts for white #10 pts for black

                if self.color==black:
                    score=score_list[player]+10

                if self!=striker:
                    piecelist.remove(self) #removes the piece from the list when pocketed
                print score_list
                

    def boundary(self):   #checks if the piece is colliding with the boundaries 
        if self.x<15 and self.velocity>0 : #1
            self.cosX = -self.cosX
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)

        if self.x<15 and self.velocity<0 : #2
            self.cosX = -self.cosX
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)
            
        if self.x>(941-30) and self.velocity>0: #3  #whether colliding with the left, right walls 
            self.cosX = -self.cosX
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)

        if self.x>(941-30) and self.velocity<0: #4  #whether colliding with the left, right walls 
            self.cosX = -self.cosX
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)

            
            
            
        if self.y<15 or self.y>(971-30):
            self.sinX = -self.sinX
            self.velocity=self.velocity *(-1)
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)

            
            
##        if self.y>(971-30): #whether colliding with the top, bottom walls
##            self.vertical_velocity=self.vertical_velocity *(-1)
##            self.sinX = -self.sinX
##            self.tanX = -self.tanX
            #self.velocity = (self.horizontal_velocity**2 + self.vertical_velocity**2)**0.5
        

################################################# END OF CLASS=PIECE#######################################################################
                           
        
    
        
class Background(pygame.sprite.Sprite): #setting up the window
    def __init__(self,window, imagefile):
        self.windows=window
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(imagefile).convert_alpha() #loads the image 
        window.fill(white) #fills the screen with white initially

    def draw_piece(self, piece): #for drawing pieces on the board
        pygame.draw.circle(self.windows, piece.color,(int(piece.x), int(piece.y)),piece.radius)

class force(pygame.sprite.Sprite):  #forcebar class
    def __init__(self,color,x,y,h,w):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.color=color
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.border=5
        self.dx=3


    def draw_forcebar(self): #for drawing forcebar on the window
        global window
        pygame.draw.rect(window,self.color,[self.x,self.y,self.width,self.height])

    
    
    def move_forcebar(self): #for moving the forcebar left to right 
        
        self.x=self.x+self.dx
        if self.x> (840-50): #changing direction when the moving force bar reaches the right end
            self.dx=-self.dx

        if self.x<156: ##changing direction when the moving force bar reaches the left end
            self.dx=-self.dx
               

##############################FUNCTIONS###############################################################                    
def drawboard(listofPieces,striker):
    global window
    boardscreen=Background(window,"carromboard1.jpg") #loads the image via the class Background
    window.blit(boardscreen.image,[0,0]) #blits the loaded image on the white screen

    for piece in listofPieces: #draws the pices from the listofpieces list
        boardscreen.draw_piece(piece)
        
    boardscreen.draw_piece(striker)#draws the striker on the board


    
def messageonscreen(message,color):   #for displaying messages on screen #pygame documentation
    textSurf, textRect= text_objects(msg,color)
    textRect.center=(display_width/2),(display_height/2)
    window.blit(textSurf, textRect)

def main(): #for displaying messages on screen #pygame documentation   
    global fps
    global window
    intro=True
    while intro:
        window.fill(white)
        messageonscreen("hi",white)
        messageonscreen("kjk",black)

        pygame.display.update()
        fps.tick(15)
        
    
def collision(): #checks for collisions between pieces
    global piecelist
    global moving_list
    moving_list=[]
    i = 0
    for piece in piecelist: # has all the pieces of the game
        v=piece.velocity #finds the self velocity of the piece
        if v!=0: # if the piece is moving at any instance, adds it to the moving pieces list
            print v, "v"+str(i)
            moving_list.append(piece)

    for moving_piece in moving_list: # goes over the pieces which are moving  
        for piece in piecelist: # for every piece which is moving, checks it with all the pieces for collision
            if piece==moving_piece:
                pass
            else:
                x1=moving_piece.x #x midpoint of the moving/colliding piece
                y1=moving_piece.y #y midpoint of the moving/colliding piece
                x2=piece.x        #x midpoint of the casual pieces
                y2=piece.y        #y midpoint of the casual pieces
                if ((x1-x2)**2)+((y1-y2)**2)>(30)**2: #checks for the circular loci, if it is within the specifc range of each other
                    
                    pass #does nothing if the casual piece is not having any collision with that moving piece
                else: #if there is a collision between the moving piece and the stationary casual piece then it moves on the other series of command
                    print 'close'
                    u=moving_piece.velocity  #gets the moving piece velocity at that instant
                    piece.move(u,x1,y1) #calculates how that moving piece velocity affects the casual stationary pieces velocity and direction
                    piece.deceleration()#starts decelerating the piece which just started moving
                    moving_piece.velocity=(piece.residual(u))[0] #gives back the residual speed and the residual angles at which it should moveto the object which collided 
                    moving_piece.sinX=(piece.residual(u))[1]
                    moving_piece.cosX=(piece.residual(u))[2]
                    moving_piece.tanX=(piece.residual(u))[3]
                
'''def load_sound(name):  #for loading sounds in the game #pygame documentation
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound '''               

            
def roundup(x):   #for rounding up the x position of the moving force bar when the enter key is pressed
    remainder = x % 60
    if remainder < 30:
        x = int(x / 60) * 60
    else:
        x = int((x + 60) / 60) * 60

    return x
####################################################SETTING UP THE BOARD#########################################################################################################################                          

pygame.init() #calling the module
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
brown=(116,42,42)
window=pygame.display.set_mode((971,941)) #making the display window or the surface
pygame.display.flip() #updates the entire window
pygame.display.set_caption("CARROM BOARD")
boardscreen=Background(window,"carromboard1.jpg")
window.blit(boardscreen.image,[0,0])

##############################################END OF FUNCTIONS#######################################################################################################################################

pr=piece(red,476,491,15)
pw1=piece(white,476-30,491,15) #creating piece instances of the class piece
pw2=piece(white,476+(30*(math.sin(0.52))),491+30*(math.cos(0.52)),15)
pw3=piece(white,476+(30*(math.sin(0.52))),491-30*(math.cos(0.52)),15)
pw4=piece(white,476-2*30*(math.sin(1.04))*(math.sin(0.52)),491+2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw5=piece(white,476+2*30*(math.sin(1.04))*(math.sin(0.52)),491+2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw6=piece(white,476-2*30*(math.sin(1.04)),491,15)
pw7=piece(white,476+2*30*(math.sin(1.04))*(math.sin(0.52)),491-2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw8=piece(white,476-2*30*(math.sin(1.04))*(math.sin(0.52)),491-2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw9=piece(white,476+2*30*(math.sin(1.04)),491,15)    
pb1=piece(black,476+30,491,15)
pb2=piece(black,476-(30*(math.sin(0.52))),491-30*(math.cos(0.52)),15)
pb3=piece(black,476-(30*(math.sin(0.52))),491+30*(math.cos(0.52)),15)
pb4=piece(black,476,491+2*30*(math.sin(1.04)),15)
pb5=piece(black,476-2*30*(math.sin(1.04))*(math.sin(1.047)),491+2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb6=piece(black,476-2*30*(math.sin(1.04))*(math.sin(1.074)),491-2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb7=piece(black,476,491-2*30*(math.sin(1.04)),15)
pb8=piece(black,476+2*30*(math.sin(1.04))*(math.sin(1.074)),491-2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb9=piece(black,476+2*30*(math.sin(1.04))*(math.sin(1.04)),491+2*30*(math.sin(1.04))*(math.cos(1.074)),15)
striker=piece(brown,300,500,15)
piecelist = [striker,pr,pw1,pw2,pw3,pw4,pw5,pw6,pw7,pw8,pw9,pb1,pb2,pb3,pb4,pb5,pb6,pb7,pb8,pb9]
#piecelist = [striker,pw1]

forcebarlist=[150,155,160,165,170,175,180,185,190,195,200,210,215] #The preset initial velocity values depending on the forcebar

######################################################INTIALISING##############################################################################################################################################




#striker_sound=load_sound('sound.wav')
isVelocityS=False
gameExit=False #initialising the variable for the game loop
drawforcebar=True
fps=pygame.time.Clock() #frames per second
moving_list=[] # an empty list for storing all the moving pieces at any instance
score_list=[0,0]
player=0
forcebar=force(black,156,800,50,684)
bar=force(white,156,800,50,5)
hover=True



#########################################################MAIN LOOP##################################################################################################################################
while not gameExit:#creating a gameloop
    window.fill(white)#applying to surface object/scrren the color
    drawboard(piecelist,striker)
    
    if drawforcebar: #draws and moves the forcebar if drawforce is True
            forcebar.draw_forcebar()
            bar.draw_forcebar()
            bar.move_forcebar()
            
    for event in pygame.event.get(): #getter funcition for events
        if event.type==pygame.QUIT: # if pygame event type is QUIT
            gameExit=True #exiting the game while loop

        if event.type == pygame.KEYDOWN: # if the enter key is pressed
            if event.key==pygame.K_RETURN:
                drawforcebar=False #no need for the forcebar on the screen now
                x=bar.x-156 #the position in which the moving bar was when the enter key was pressed
                index=roundup(x) #rounds that position to nearest 60
                index=index/60
                u=forcebarlist[index] #compares and retrieves the intial velocity from the pre set list of initial velocities dependent on position of force bar
                
                                        
            
        if hover==True and drawforcebar==False and isVelocityS==False  and len(moving_list)==0: 
            x,y = pygame.mouse.get_pos() #the striker hovers/moves with cursor
            print x,y, "x and y"
            striker.move_withcursor(x,y)
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE: #as soon as spacebar is pressed, the striker stops moving and is staionary at that position
                    hover=False
            
        if hover==False and event.type == pygame.MOUSEBUTTONUP: #once the striker has been set in position, and the place where the striker should moved is clicked, if calculates the relevant info below
            #striker_sound.play()
            x,y = pygame.mouse.get_pos() #gets the x,y position where the player wants the striker to move
            striker.velocity=u #sets the initial velocity as the u retrieved from the forcebar above
            isVelocityS=True #makes true- the striker has some velocity now
            striker.angle(x,y) #calculates the angle at which the striker should initially move depending on where the player clicked

                
    if isVelocityS: #once the striker is moving, starts decelerating it       
        striker.deceleration()
        
    if isVelocityS==True and striker.velocity==0: #once the striker has stopped moving, it is the next player's turn, and the forcebar reappears
        hover=True
        drawforcebar=True
        isVelocityS=False
        player=(player+1)%2

    collision() #in every fps checks for collision

    for pieces in moving_list: #for every piece that is moving, checks whether it is striking the boundary, or is being pocketed
        if pieces.velocity==0:
            moving_list.remove(pieces)
        pieces.pocketting()
        pieces.deceleration()
        pieces.boundary()

    

            
    
    
    pygame.display.flip() #updates the entire window
    fps.tick(60)
pygame.quit() #uninitialising pygame
#quit() #exits from python
