#importing libraries
import pygame
import math
import pygame
import random


pygame.init() #calling the module


#    15-112: Principles of Programming and Computer Science
#    Project: Carrom Board
#    Name      : Maimoon
#    AndrewID  : maimoons

#    File Created: 
#    Modification History:
#    Start:11/7/2016 8:00 pm   End:11/7/2016 10:00 pm
#    11/8/2016 :9:00 pm         11/8/2016:11:00 pm
#    11/10/2016 :6:00 pm        11/11/2016:5:00 am
#    11/11/2016 :5:00 pm        11/11/2016:11:00 pm
#    11/12/2016 :7:00 am        11/12/2016 :1:00 pm
#    11/14/2016: 8:00 pm        11/14/2016 :9:00 pm
#    11/17/2016 :6:00 pm        11/17/2016:11:00 pm
#    11/18/2016 :2:00 am        11/18/2016:10:00 am
#    11/20/2016 :6:00 pm        1120/2016:9:00 pm
#    11/21/2016 :7:00 pm        11/21/2016 :12:00 pm
#    11/23/2016: 7:00 pm        11/23/2016 :9:00 pm
#    11/24/2016: 7:00 pm        11/24/2016 :12:00 am
#    11/25/2016: 1:00 am        11/25/2016 :7:00 am
#    11/25/2016: 5:00 pm        11/25/2016 :12:00 am
#    11/26/2016: 12:00 am       11/25/2016 :12:00 pm
#    11/26/2016: 5:00 pm        11/25/2016 :10:00 pm




    
#This is a carrom board game.                       
############################################################CLASSES ###############################################################################################################################     
#This is the class for all the carrom pieces
#the attributes of this class includes:
        #self.y=the y cordinate of the midpoint
        #self.x=the x cordinate of the midpoint
        #self.r=the radius of the pieces
        #self.horizontal_velocity=the horizontal velocity of the pieces once it starts moving
        #self.vertical_velocity=the vertical velocity of the pieces once it starts moving
        #self.sinX=the sine of the angle between the direction vector at which the piece is moving and the horizontal
        #self.cosX=the cosine of the angle between the direction vector at which the piece is moving and the horizontal
        #self.tanX=the tangent of the angle between the direction vector at which the piece is moving and the horizontal


friction=0 #The friction is set as default to the lowest value
gameover=False #The initialising variable for the main game loop

iscomputer=False #when playing multiplayer, this is set to True #
isincomp=False
instructions=False #when the person clicks on rule, the while loop for the instructions/rules window is initialised
CollisonMade = False #For keeping track of the collision every turn


black=(0,0,0) #the colors used in the game
white=(255,255,255)
lightred=(150,0,0)
red=(255,0,0)
brown=(116,42,42)


class carrompiece(): #this is the class for all the carrom pieces   
    def __init__(self,color,y,x,r,idt="default"):
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
        self.id = idt               #the id for every piece


    # for removing pieces of this class object from a list which is passed as an input parameter
    def remove(self,moving_list):
        moving_list.remove(self)
        
    #calculates the angle between piece's  midpoint and any point on the board
    # x and y are the midpoint of any piece on the board with which the angle has to be calculated
    #tanX is the tangent of the angle between the line joining the 2 midpoints( this self piece and the colliding piece) and the horizontal
    #hypotenuse is the line joining the 2 midpoints( this self piece and the colliding piece) and the horizontal
    #cosine and sine of the same  angle are calculated based on the hypotenuse. Sine=opposite/hypotenuse, cosine=adjacent/hypotenuse   
        
    def angle(self,x,y):   
        if (x-self.x)!=0: #ensuring it is not dividing by 0
            self.tanX=float(y-self.y)/float(x-self.x) 
        hypotenuse=((y-self.y)**2+(x-self.x) **2)**0.5

        if hypotenuse!=0: #ensuring it is not dividing by 0
            self.cosX=(x-self.x)/hypotenuse
            self.sinX=(y-self.y)/hypotenuse


           
#takes the coorinates x and y through the set pos function
#sets thpse as the self x and y coordinates for the piece so that it appears to be moving with the mouse cursor
    def move_withcursor(self,x,y):  #for hovering the striker with the cursor
        self.x=x
        self.y=y
        
    #u is the initial velocity of the piece which is colliding with this self piece
    #similarly, x and y are the midpoint coordinates of the piece which is colliding with this self piece
    def move(self,u,sin,cos): #for angles between self piece and onther piece which is colliding with it
        if (x-self.x)!=0:
            self.tanX=float(y-self.y)/float(x-self.x)  #calculates the tangent of the angle between the line joining the 2 midpoints( this self piece and the colliding piece) and the horizontal
        hypotenuse=((y-self.y)**2)+((x-self.x) **2)**0.5

        self.cosX=cos
        self.sinX=sin
        
        
        self.velocity=u*(3.1/3)#calculates the velocity of this stationary self piece due to collision with a moving particle
        if self.velocity>50:  
            self.velocity=50
            
        self.horizontal_velocity=(self.velocity) *(self.sinX) #calculating the horizontal and vertical component of the velocity
        self.vertical_velocity=(self.velocity)*(self.cosX)
      
#based on the velocity of the piece that collided with this self piece, the rebound direction and velocity for that colliding piece is calculated
#return the calculated values to set as attribute of the colliding piece object
    def residual(self,u,sin,cos): #the forward velocity of the piece which collided with this self piece
        
        velocity=u*(1.0/3) 
        sinX2=-sin  
        cosX2=-cos
        tanX2=sin*1.0/cos
        
        
        return [velocity, sinX2, cosX2, tanX2] #the angles with which the colliding object should move
    
#This function is for calculating for the difference between any piece that overlaps
#So that the pieces can move away from the distance that they are overlapping with
    def difference(self,x,y):
        
        hypotenuse=((y-self.y)**2)+((x-self.x) **2)**0.5
        if hypotenuse<30: #30 is twice the radius of the ball so if their center points are closer than 
            return hypotenuse/(2.0) 
        
    
#This decreases the absolute velocity of the moving pieces based on the direction in which they are moving
#resolves the absolute velocity into horizontal and vertical components
#If the velocity is negative, it decelerates by adding the deceleration (0.5) to the velocity
#vice versa if it is positive, it decreases it by 0.5
    def deceleration(self): # decreases the absolute velocity of the self piece to 0
        global friction
        if friction==1: # if the friction is set to the lowest value, the deceleration is set to lowest value
            decel=0.25
        if friction==2:
            decel=0.5
        if friction==3:
            decel=0.75
        self.horizontal_velocity=self.velocity *(self.cosX) #calculates vertical and horizontal components
        self.vertical_velocity=self.velocity*(self.sinX)
        
        if self.velocity == 0: #if the velocity is reduced to 0, it returns from the function
            return
        
        if self.velocity>0 and self.cosX>0:  # if angle in first quadrant #moving towards North-East
            
            self.x=self.x+self.horizontal_velocity #increasing the x midpoint coordinates of this self piece
            self.y=self.y+self.vertical_velocity #increasing the y midpoint coordinates of this self piece
            self.velocity=self.velocity-decel  #decelearating the absolute velocity which affects the horizontal and vertical componenets of the velocity
            if self.velocity<0:
                self.velocity=0


        elif self.velocity>0 and self.cosX<0: #if angle in second quadrant # moving towards North-West
           
            self.x=self.x+self.horizontal_velocity #increasing the x midpoint coordinates of this self piece
            self.y=self.y+self.vertical_velocity #increasing the y midpoint coordinates of this self piece
            self.velocity=self.velocity-decel  #decelearating the absolute velocity which affects the horizontal and vertical componenets of the velocity
            if self.velocity<0:
                self.velocity=0
            
            
            
        elif self.velocity<0 and self.cosX<0: #3rd quadrant, same stuff but in this case the velocity is in negative direction
            
            self.x=self.x+self.velocity
            self.y=self.y+self.velocity
            self.velocity=self.velocity+decel
            if self.velocity>0:
                self.velocity=0
        
            


        else: #the velocity is 0 and moving in the 4th quadrant
           
            self.x=self.x+self.velocity
            self.y=self.y+self.velocity
            self.velocity=self.velocity+decel
            if self.velocity>0:
                self.velocity=0

        
                
        
        
        self.horizontal_velocity=self.velocity *(self.cosX) #calculates the horizontal component of velocity
        self.vertical_velocity=self.velocity*(self.sinX) #calculates the vertical componenet of velocity
        

        
#this checks if any piece is close to the regions of the four pockets
#and pockets/removes the piece once it is within the region
#if it pockets a black piece, the person whose turn it is gets 10 points
#if it is a white piece, the person whose turn it is gets 20 points
#the piece is only pocketed if it is any piece apart from the striker
#it checks for the closeness to the pocket by taking the midpoints of the pockets
# and checks if the distance between the midpoints of any moving piece and the pockets is less than the sum of the radius of the two
    def pocketting(self): # checks if the piece is within the vicinity of the four pockets 
        global piecelist
        pockets = [(86,84),(885,84),(885,863),(86,863)] # the midpoint coordinates of the four pockets 
        for midpoints in pockets:
            if ((self.x-midpoints[0])**2)+((self.y-midpoints[1])**2)<(15+15)**2 and ((self.x-midpoints[0])**2)+((self.y-midpoints[1])**2)>0: #checks whether within circular loci of the pockets #remember to calculate the right radius 
                if self.color==white:
                    score_list[player]=score_list[player]+20 #adds to the score the piece which is pocketed #20 pts for white #10 pts for black
                   
                if self.color==black:
                    score_list[player]=score_list[player]+10
                    
                if self.color==red:
                    score_list[player]=score_list[player]+100

                if self!=striker:
                    piecelist.remove(self) #removes the piece from the list when pocketed
                    
                
                return score_list
                
#this function checks if any moving piece is colliding with the boudaries/edges of the board
#If it either collides with the right or left edge, only the cosX reverses direction
#If it either collides with the top or bottom edge, only the sinX reverses direction
##at every collision with the boundary, it reduces friction
            
    def boundary(self):   #checks if the piece is colliding with the boundaries 
        if self.x>911 or self.x<75 : #1 #the mnax and min for the x coordinates of the game
            if self.x>911: #if going off the extreme limits, brings it back within bounds and reverses direction
                self.x=911
            else:
                self.x=75
            self.cosX = -self.cosX #reverses the direction of motion of the piece
            if self.velocity>0: #at every collision with the boundary, it reduces friction
                self.velocity=self.velocity-friction
                
            if self.velocity<0: #if the velocity is negative, it moves it up to 0
                self.velocity=self.velocity+friction
                
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)


        
        if self.y<75 or self.y>941 : #2 #the max and min for the y coordinated of the game
            
            if self.y>941:
                self.y=941
            else:
                self.y=75
                
            if self.velocity>0:#at every collision with the boundary, it reduces friction
                self.velocity=self.velocity-friction
            if self.velocity<0: #if the velocity is negative, it moves it up to 0
                self.velocity=self.velocity+friction
                
            self.sinX = -self.sinX #reverses the direction of motion of the piece
            
            self.horizontal_velocity=self.velocity *(self.cosX) #calculating the horizontal and vertical component of the velocity
            self.vertical_velocity=self.velocity*(self.sinX)
        
            
            


################################################# END OF CLASS=PIECE#############################################################################################################################
                           
        
#This is the class background which makes the background for the game
#The init of this class takes the following:
#it takes the input parameter window and the image which needs to be blitted on it
#it then loads the image passed to it
#and fills the entire window with white
        
class Background(pygame.sprite.Sprite): #setting up the window
    def __init__(self,window, imagefile):
        self.windows=window
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(imagefile).convert_alpha() #loads the image 
        window.fill(white) #fills the screen with white initially

#this is a function of the class background
#it draws circles on the window display of the game
    def draw_piece(self, piece): #for drawing pieces on the board
            pygame.draw.circle(self.windows, piece.color,(int(piece.x), int(piece.y)),piece.radius)


#this class is for drawing the forcebar on the screen
#the forbar are basically two rectangles
#one rectangle acts as a base
#and the other smaller rectangles moves over it
#the attributes include the x,y starting coordinates and the width and height of the rectangles
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

#once the attributes are set, this is for drawing the forcebar on the screen
    def draw_forcebar(self): #for drawing forcebar on the window
        global window
        pygame.draw.rect(window,self.color,[self.x,self.y,self.width,self.height])

    
#this moves the smaller forebar over the bigger rectangular base
#it does that by increasing the x coordinate of the moving rectangle by 3
#and reversing the x coordinate accordingle when it reaches the end of the base rectangle
    def move_forcebar(self): #for moving the forcebar left to right 
        
        self.x=self.x+self.dx
        if self.x> (840-50): #changing direction when the moving force bar reaches the right end
            self.dx=-self.dx

        if self.x<156: ##changing direction when the moving force bar reaches the left end
            self.dx=-self.dx
            
############################################################CLASS FOR MAIN MENU####################################################################################################################               
#This is a class for for displaying the menu buttons       
class Option:

    hovered = False
    
    def __init__(self, text, pos,font):
        self.text = text
        self.pos = pos
        self.font=font
        self.set_rect()
        self.draw()
            
    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            
            return (255, 255, 255)
        else:
            return (255, 0, 0)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
        
##############################FUNCTIONS##############################################################################################################################################################                  
#This function is when playing the single player mode
#The x postion for the striker is preset at 200
#for all the possible y positions on the column corresponding to x=200:
#It calculates the gradient i.e tanxU/L of the imaginary line formed by joining the midpoint of the striker and the midpoint of the upper and lower pockets on the right
#It also calculates the intercept(d1 and d2) to have the equations of the two imaginary lines
#Then for every piece on the board, it checks how far apart is every piece from the two lines
#It does it by calculating the perpendicular distance of the piece to the line by first calculating the equation of the perpendicular line
#The gradient of the perpendicular line is simply -1/gradient of the actual line
#The coordinates of the points at which the the line joinging the striker and the pocket, and the its perpendicular bisector line intersect are calculated
#and through pythagoras, the perpendicular distance is calculated
#shortest 1 is the point closest to the first line
#shortest 2 is the point closest to the second line
#whichever of the two is nearer is supposed to be hit
#the x and y coordinates of the piece to hit are returned
#in single player, player 0 is always the user, and player 1 is the computer

def computer(): #of the striker position
    x=150
    shortest1=10000000000000
    shortest2=10000000000000
    shortest3=10000000000000
    shortest4=10000000000000
    global piecelist
    for y in range(250,700,10):
        
        uppperpocket=[885,863]
        lowerpocket=[86,863]
        uppperpocket1=[85,83]
        lowerpocket1=[80,863]
        tanXU=float(uppperpocket[0]-y)/float(uppperpocket[1]-x)
        tanXL=float(lowerpocket[0]-y)/float(lowerpocket[1]-x)
        tanXU1=float(uppperpocket1[0]-y)/float(uppperpocket1[1]-x)
        tanXL1=float(lowerpocket1[0]-y)/float(lowerpocket1[1]-x)


        d1=y-tanXU*x  #y=mx+d  
        d2=y-tanXL*x
        d3=y-tanXU1*x  #y=mx+d  
        d4=y-tanXL1*x
        
        for i in piecelist:
            
            if i!=striker:
                a=i.y
                b=i.x
               

                c1=a+(1/tanXU)*b #y=(-1/m )x+c
                c2=a+(1/tanXL)*b
                c3=a+(1/tanXU1)*b #y=(-1/m )x+c
                c4=a+(1/tanXL1)*b
                ycoord1=((tanXU**2)/((tanXU**2)+1))*(c1-d1)+d1
                xcoord1=((tanXU**2)/((tanXU**2)+1))/(c1-d1)
                ycoord2=((tanXL**2)/((tanXL**2)+1))*(c2-d2)+d2
                xcoord2=((tanXL**2)/((tanXL**2)+1))/(c2-d2)
                ycoord3=((tanXU1**2)/((tanXU1**2)+1))*(c3-d3)+d3
                xcoord3=((tanXU1**2)/((tanXU1**2)+1))/(c3-d3)
                ycoord4=((tanXL1**2)/((tanXL1**2)+1))*(c4-d4)+d4
                xcoord4=((tanXL1**2)/((tanXL1**2)+1))/(c4-d4) 


                shortest11= (ycoord1**2)+ xcoord1**2
                
                shortest22= (ycoord2**2)+ xcoord2**2

                shortest33= (ycoord3**2)+ xcoord3**2
                
                shortest44= (ycoord4**2)+ xcoord4**2
                
                if shortest11<shortest1:
                    
                    shortest1=shortest11
                    piecetohit1=i

                if shortest22<shortest2:
                    shortest2=shortest22
                    piecetohit2=i

                if shortest33<shortest3:
                    
                    shortest3=shortest33
                    piecetohit3=i

                if shortest44<shortest4:
                    shortest4=shortest44
                    piecetohit4=i

        if len(piecelist)>1 and shortest1>shortest2 and shortest1>shortest3 and shortest1>shortest4: #checking which of the two close pieces is the closest
            piecetohit=piecetohit2

        elif len(piecelist)>1 and shortest2>shortest3 and shortest2>shortest4:
            piecetohit=piecetohit2

        elif len(piecelist)>1 and shortest3>shortest4:
            piecetohit=piecetohit3

        else :
            piecetohit=piecetohit4

            
    
    if len(piecelist)>1:
        return piecetohit.x, piecetohit.y,200,y
        
                 

#this is a function which essentially draws the board on the screen using the class 'Background' defined above
#it makes an object of the class
#and then blit the image on the screen
#then looping over the list called listofPieces passed as an input parameter, it draws the pieces on the screen
#in the end draws the striker    

def drawboard(listofPieces,striker):
    global window
    boardscreen=Background(window,"carromboard1.jpg") #loads the image via the class Background
    window.blit(boardscreen.image,[0,0]) #blits the loaded image on the white screen

    for piece in listofPieces: #draws the pices from the listofpieces list
        boardscreen.draw_piece(piece)
        
        
    boardscreen.draw_piece(striker)#draws the striker on the board



#different fonts defined for diplaying messages on the screen
smallestfont=font=pygame.font.SysFont("comicsanms",25)
smallfont=font=pygame.font.SysFont("comicsanms",40)
mediumfont=pygame.font.SysFont("comicsanms",90)

#This is a function which is essentially used to display any sort of message on screen    
def messageonscreen(message,color,x,y,font):   #for displaying score on screen

    screen_text=font.render(message, True, color)
    window.blit(screen_text, (x,y))


#This represents the main menu page where you select single or multiplayer
#it goes in to pygame main page while loop
#it calculates the cordinates of where the mouse was clicked to initialise relevant gameboard windows
#the options where it could be clicked include single player, multiplayer, and three friciton options, and the rules
def main(): #for displaying messages on screen #pygame documentation   
    intro=True #this initialises the while loop for the main menu below
    global isincomp
    global friction #for setting the friciton limit
    global instructions #initialising variable for thr rules window


    file = 'mainsound.mp3' #the sound in the background being played    
    pygame.init()   
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
    if not pygame.mixer.get_busy(): #keeps repeating the music whenever it stops
        file = 'mainsound.mp3'
        pygame.init()   
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        
    while intro: #the while loop for the main menu window
        
        for event in pygame.event.get():#keeps looking for events when the while loop is running 
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
                
        window.fill(white) #makes the background white, then loads image on it
        screen=Background(window,"home.jpg") #loads the image via the class Background
        window.blit(screen.image,[0,0]) #blits the loaded image on the white screen
        pygame.event.pump()
        
        for option in options: #This is list consisitng of objects of the class options that are essentially acts as buttons on the main page
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                for event in pygame.event.get():

                    

                    x,y = pygame.mouse.get_pos()
                    if x<500 and x>125  and y>350 and y<400:#if it is within this range, and the mouse is clicked, the three friction options are displayed
                        click=pygame.mouse.get_pressed()
                        
                        if click[0]==1:
                            options.append(Option("friction=1", (125,400),smallestfont)) #displaying friction options
                            options.append(Option("friction=2", (125,450),smallestfont))
                            options.append(Option("friction=3", (125,500),smallestfont))


                    x,y = pygame.mouse.get_pos()
                    if x<350 and x>125  and y>400 and y<450: #if it is within this range, and the mouse is clicked, the first friciton option is selected and set and all the friction options are removed from the screen
                        click=pygame.mouse.get_pressed()
                        if click[0]==1:
                            friction=1
                            length=len(options)
                            del options[length-1] #deleting friction options once a friction value is selected
                            del options[length-2]
                            del options[length-3]

                                
                    x,y = pygame.mouse.get_pos()
                    if x<350 and x>125  and y>450 and y<500:#if it is within this range, and the mouse is clicked, the second friciton option is selected and set and all the friction options are removed from the screen
                        click=pygame.mouse.get_pressed()
                        if click[0]==1:
                            friction=2
                            length=len(options)
                            del options[length-1]
                            del options[length-2]
                            del options[length-3]

                                

                    x,y = pygame.mouse.get_pos()
                    if x<350 and x>125  and y>500 and y<550:
                        click=pygame.mouse.get_pressed()
                        if click[0]==1:
                            friction=3 #if it is within this range, and the mouse is clicked, the third friciton option is selected and set and all the friction options are removed from the screen
                            length=len(options)
                            del options[length-1]
                            del options[length-2]
                            del options[length-3]

                    x,y = pygame.mouse.get_pos()
                    if x<350 and x>125 and y>125 and y<250:#if it is within this range, and the mouse is clicked, the rule/instructions window is activated
                        click=pygame.mouse.get_pressed()
                        if click[0]==1:                            
                            instructions=True                       

                    x,y = pygame.mouse.get_pos()
                    if x<350 and x>125 and y>300 and y<350: #if it is within this range, and the mouse is clicked, the multi player is activated
                        click=pygame.mouse.get_pressed()
                        if click[0]==1:
                            if friction==0:#if the value of friction is not selected, it is set as default to the lowest value
                                friction=1
                            intro=False

                    x,y = pygame.mouse.get_pos() #gets when xy cordinates of the cursor
                    if x<350 and x>125 and y>250 and y<300: #if it is within this range, and the mouse is clicked, the single player is activated
                        click=pygame.mouse.get_pressed()
                        if click[0]==1:
                            if friction==0: #if the value of friction is not selected, it is set as default to the lowest value
                                friction=1
                            intro=False #the home page while loop is set to false
                            isincomp = True #the variables for the single player are set true which initiates the single player gameboard
                            iscomputer=True
                                

                    
            else:
                option.hovered = False
            option.draw()

        messageonscreen("PRESS P TO PAUSE WHILE PLAYING THE GAME",lightred,0,600,smallfont) #displays score on the top right

#This is for displaying the rule window explaining all the rules
        if instructions:           
            instruction=Background(window,"rule.png")
            window.blit(instruction.image,[0,0])
            button("BACK",0,0,100,50,lightred,red,back)
        pygame.display.update()





        fps.tick(15)



#This function is for detecting collisions between 2 pieces
#as a result of the collisions, the function calls another function which is part of the class piece that calculates the new velocity and direction of the two pieces after collisions
#The moving_list is a list which has all the pices that are moving added to it
#It goes over every piece in the piecelist, and whichever has a non zero velocity, is moving and is added to the the moving_list
#Then every combination of moving_piece and all the pieces in the piece_list, it checks if they are colliding
#it does that by calculating the distance between the two midpoints of the two pieces through pythagoras theorem
#if the moving_piece and the piecelist piece are the same object, nothing happens( this is not a valid combination)
#if the distance is more than 2x the radius, nothing happens since they are not colliding
#else, if the distance is smaller, they are colliding so the new piece starts moving by calling the function piece.move

def collision(): #checks for collisions between pieces
    global piecelist
    global moving_list
    global iscollided
    global CollisonMade
    moving_list=[]
    i = 0
    for piece in piecelist: # has all the pieces of the game
        v=piece.velocity #finds the self velocity of the piece
        
        if v!=0: # if the piece is moving at any instance, adds it to the moving pieces list
            
            moving_list.append(piece)
    
    for moving_piece in moving_list: # goes over the pieces which are moving  
        for piece in piecelist: # for every piece which is moving, checks it with all the pieces for collision
            if piece==moving_piece:
                continue
            else:
                x1=moving_piece.x #x midpoint of the moving/colliding piece
                y1=moving_piece.y #y midpoint of the moving/colliding piece
                x2=piece.x        #x midpoint of the casual pieces
                y2=piece.y        #y midpoint of the casual pieces
                if ((x1-x2)**2)+((y1-y2)**2)>(30)**2: #checks for the circular loci, if it is within the specifc range of each other
                    
                    None#does nothing if the casual piece is not having any collision with that moving piece
                else: #if there is a collision between the moving piece and the stationary casual piece then it moves on the other series of command

                    CollisonMade = True
                    u=moving_piece.velocity  #gets the moving piece velocity at that instant
                

                    piece.move(u,moving_piece.sinX,moving_piece.cosX) #calculates how that moving piece velocity affects the stationary pieces velocity and direction
                    piece.deceleration()#starts decelerating the piece which just started moving
                    
                    
                    moving_piece.velocity=(piece.residual(u,moving_piece.sinX,moving_piece.cosX))[0] #gives back the residual speed and the residual angle at which it should move the object which collided 
                    moving_piece.sinX=(piece.residual(u,moving_piece.sinX,moving_piece.cosX))[1]
                    moving_piece.cosX=(piece.residual(u,moving_piece.sinX,moving_piece.cosX))[2]
                    moving_piece.tanX=(piece.residual(u,moving_piece.sinX,moving_piece.cosX))[3]
                    iscollided = True
                
              

#for setting the initial velocity of the striker
#based on where the forcebar was when the enter key was pressed
#the forcebar list has 13 predefined velocites
#the x coordinates of the forcebar where the enter key was pressed is rounded to the nearest 60 and then divided by 60 to have the index in the forcebar list from which it can select a velocity
#so greater the index calculated, the greater the value of the velocity is set
                    
def roundup(x):   #for rounding up  the x position of the moving force bar when the enter key is pressed
    remainder = x % 60
    
    if remainder < 30:#if below 30, rounds it down
        x = int(x / 60) * 60
    else:#if above 30, it round it up
        x = int((x + 60) / 60) * 60

    return x

#the back function for going back to the mainscreen
def back():
    global instructions
    instructions=False
############################################################################BUTTONS###############################################################################################################

#https://pythonprogramming.net/pygame-button-function-events/
def text_objects(text, font,color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

#this function is linked to the buttons on the pause screen and the gameover screen
def quitgame():
    pygame.quit()
    quit()
#This function is linked to the pause button on the main menu, the pause variable is essentially the initialising variable for the while loop which keeps the pause window running
    #turns it false when the function unpaused is called
def unpause():
    global pause
    pause=False
    
#displays pause on the screen    
def paused(text):
    
    largeText = pygame.font.SysFont("comicsansms",115)

    TextSurf, TextRect = text_objects(text, largeText,lightred)
    TextRect.center = (485,550)
    window.blit(TextSurf, TextRect)
    
#msg=the message to be displayed
    #x,y=the x,y cordinate where the button should be made
    #w,h=width,height of the button
    #on=color of the button when the mouse is over it
    #off the color of the button when the mouse is not over it
    #action=function to be called when the button is clicked once
def button(msg,x,y,w,h,on,off,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, off,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(window, on,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    window.blit(textSurf, textRect)




    


    

    
    
    
    
####################################################SETTING UP THE BOARD#########################################################################################################################                          


fps=pygame.time.Clock() #frames per second
window=pygame.display.set_mode((1200,675)) #making the display window for main menu screen on the surface
screen = pygame.display.set_mode((1200, 675))

#Make buttons which are objects of the class options, to display on the main page
options = [Option("RULES", (125, 200),smallfont),Option("CARROM BOARD", (400, 30),mediumfont), Option("SINGLE PLAYER", (125, 255),smallfont),
   Option("MULTI PLAYER", (125, 305),smallfont),Option("FRICTION", (125, 355),smallfont)]


main() #calls the main function to start the main page

window=pygame.display.set_mode((971,941)) #making the display window for the gameboard on the surface

pygame.display.flip() #updates the entire window
pygame.display.set_caption("CARROM BOARD") 
boardscreen=Background(window,"carromboard1.jpg")
window.blit(boardscreen.image,[0,0])

##############################################END OF FUNCTIONS#######################################################################################################################################
#positons all the pieces on the board initially in a circular pattern, with red piece in the center and the black and white pieces alternating
#the cordinates (476,491) are the coordinates for the red piece in the center and all the other pieces are set relative to it in a circle
#the positions are set through trignometric and polygon properties
pr=carrompiece(red,476,491,15)
pw1=carrompiece(white,476-30,491,15) #creating carrompiece instances of the class carrompiece #first circle
pw2=carrompiece(white,476+(30*(math.sin(0.52))),491+30*(math.cos(0.52)),15)
pw3=carrompiece(white,476+(30*(math.sin(0.52))),491-30*(math.cos(0.52)),15)

pw4=carrompiece(white,476-2*30*(math.sin(1.04))*(math.sin(0.52))  ,491+2*30*(math.sin(1.04))*(math.cos(0.52)),15,"pw4") #second circle
pw5=carrompiece(white,476+2*30*(math.sin(1.04))*(math.sin(0.52)),491+2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw6=carrompiece(white,476-2*30*(math.sin(1.04)),491,15)
pw7=carrompiece(white,476+2*30*(math.sin(1.04))*(math.sin(0.52)),491-2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw8=carrompiece(white,476-2*30*(math.sin(1.04))*(math.sin(0.52)),491-2*30*(math.sin(1.04))*(math.cos(0.52)),15)
pw9=carrompiece(white,476+2*30*(math.sin(1.04)),491,15)

pb1=carrompiece(black,476+30,491,15) #first circle
pb2=carrompiece(black,476-(30*(math.sin(0.52))),491-30*(math.cos(0.52)),15)
pb3=carrompiece(black,476-(30*(math.sin(0.52))),491+30*(math.cos(0.52)),15)

pb4=carrompiece(black,476,491+2*30*(math.sin(1.04)),15)  #second circle
pb5=carrompiece(black,476-2*30*(math.sin(1.04))*(math.sin(1.047)),491+2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb6=carrompiece(black,476-2*30*(math.sin(1.04))*(math.sin(1.074)),491-2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb7=carrompiece(black,476,491-2*30*(math.sin(1.04)),15)
pb8=carrompiece(black,476+2*30*(math.sin(1.04))*(math.sin(1.074)),491-2*30*(math.sin(1.04))*(math.cos(1.074)),15)
pb9=carrompiece(black,476+2*30*(math.sin(1.04))*(math.sin(1.04)),491+2*30*(math.sin(1.04))*(math.cos(1.074)),15)
striker=carrompiece(brown,300,500,15,"Striker")

#piecelist = [striker,pr,pw1,pw2,pw3,pw4,pw5,pw6,pw7,pw8,pw9,pb1,pb2,pb3,pb4,pb5,pb6,pb7,pb8,pb9] #draws both the circles of pieces
piecelist = [striker,pr,pw1,pw2,pw3,pb1,pb2,pb3] #draws one circle of pieces
#piecelist = [striker,pr]

forcebarlist=map(lambda x: x/14,[300,310,320,330,340,350,360,370,380,390,400,410,420]) #The preset initial velocity values depending on the forcebar

######################################################INTIALISING VARIABLES FOR THE MAIN LOOP##############################################################################################################################################

isVelocityS=False #for checking the velocity of the striker/ whether moving or not
gameExit=False #initialising the variable for the game loop
drawforcebar=True #so that forcebar is only drawn when all pieces stop moving
fps=pygame.time.Clock() #frames per second
moving_list=[] # an empty list for storing all the moving pieces at any instance
score_list=[0,0] #for keeping track of the scores of the two players
player=0 #initially started with player 0

forcebar=force(black,156,800,50,684)#draws the background force bar
bar=force(white,156,800,50,5)#draws the moving forcebar

hover=True #for hovering the striker with the mouse so that it can be placed anywhere
pause=False #if P is pressed, the game is paused
count=True #keeps a counter for delaying the computer's turn after the player does his turn during single player
iscollided = False
runonce = False
counter = 0 #for delaying the computer's turn
legitrunonce=True #for ensuring computer does its turn once when single player

#########################################################MAIN LOOP##################################################################################################################################


while not gameExit:#creating a gameloop

    while pause: #checking if the game is paused, if yes, stays within this loop until unpaused
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        button("Continue",150,450,100,50,lightred,red,unpause) #If the game is paused, these two buttons are displayed on the screen and either of them could be clicked
        button("Quit",750,450,100,50,lightred,red,quitgame)
        

        pygame.display.update()
        fps.tick(15)
        

    window.fill(white)#applying to surface object/screen the color
    

    drawboard(piecelist,striker) #draws all the pieces on the gameboard screen
    messageonscreen("SCORES:",black,705,60,smallfont) #displays score on the top right
    messageonscreen("Player 1:"+str(score_list[0]),black,705,90,smallfont)
    messageonscreen("Player 2:"+str(score_list[1]),black,705,120,smallfont)
    
    if drawforcebar: #draws and moves the forcebar if drawforce is True
            forcebar.draw_forcebar()
            bar.draw_forcebar()#draws the forcebar that should be moved
            bar.move_forcebar()#moves the above drawn forcebar
            
    for event in pygame.event.get(): #getter funcition for events
        if event.type==pygame.QUIT: # if pygame event type is QUIT
            gameExit=True #exiting the game while loop

        if event.type == pygame.KEYDOWN: #checking if the button p is pressed for pausing the game           
            if event.key == pygame.K_p:
                pause = True #initiates the pause while loop
                paused("PAUSE")

        if event.type == pygame.KEYDOWN and ((isincomp==False and player==1) or player==0): # if the enter key is pressed, the value for initial striker velocity is determined
            if event.key==pygame.K_RETURN:
                drawforcebar=False #no need for the forcebar on the screen now
                CollisonMade = False #no collisions have been made yet
                x=bar.x-156 #the position in which the moving bar was when the enter key was pressed
                index=roundup(x) #rounds that position to nearest 60
                index=index/60 
                u=forcebarlist[index] #compares and retrieves the intial velocity from the pre set list of initial velocities dependent on position of force bar
                
                                        
            
        if hover==True and drawforcebar==False and isVelocityS==False  and len(moving_list)==0 and ((isincomp==False and player==1 ) or (player==0)):#either player 1 in single player,or  player 0 in multi or single player # if the space bar key is pressed, the striker is placed at the position the cursor was
            x,y = pygame.mouse.get_pos() #the striker hovers/moves with cursor            
            striker.move_withcursor(x,y)
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE: #as soon as spacebar is pressed, the striker stops moving and is staionary at that position
                    hover=False
            
        if hover==False and event.type == pygame.MOUSEBUTTONUP and ((isincomp==False and player==1) or (player==0)):#either player 1 in single player,or  player 0 in multi or single player) #once the striker has been set in position, and the place where the striker should moved is clicked, if calculates the relevant info below
            file = 'sound.wav' #the sound played when the striker is moved
            pygame.init()   
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            
            x,y = pygame.mouse.get_pos() #gets the x,y position where the player wants the striker to move
            striker.velocity=u #sets the initial velocity as the u retrieved from the forcebar above
            isVelocityS=True #makes true- the striker has some velocity now
            striker.angle(x,y) #calculates the angle at which the striker should initially move depending on where the player clicked

        
    if isincomp==True and player==1 and not runonce: #once the striker has been set in position, and the place where the striker should moved is clicked, if calculates the relevant info below
        counter+=1 #increases the counter for delaying the computer's turn
        
        CollisonMade=False
        
        if legitrunonce: #the computer does it turn once, and then it is the next person's turn
            x,y,hoverx,hovery=computer(  )
            striker.x, striker.y=hoverx,hovery
            striker.angle(x,y) #calculates the angle at which the striker should initially move depending on where the player clicked
            striker.velocity = 0
            legitrunonce=False 
            
        if counter<100: #keeps a counter for delaying the computer's turn after the player does his turn during single player
            None         
        else: #once it has waited for 100 millisec, it starts the computer turn again
            file = 'sound.wav'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            
            striker.velocity=random.choice(forcebarlist) #sets the initial velocity as the u retrieved from the forcebar above
            runonce = True
            counter = 0 #resets the counter to 0 for the next computer turn
            legitrunonce=True
            isVelocityS=True #makes true- the striker has some velocity now
       
    collision() #calls the function collision every frame to check whether any of the pieces are colliding
    
    if isVelocityS: #once the striker is moving, starts decelerating it               
        striker.deceleration()

    
        
    if isVelocityS==True and striker.velocity==0: #once the striker has stopped moving, it is the next player's turn, and the forcebar reappears
        hover=True      
        if len(moving_list)==0: #once all the pices have stopped moving
            
            player=(player+1)%2 #changes the player     
            drawforcebar=True #draws the forcebar again
            
            isVelocityS=False #sets it to False since the striker is no longer moving
            runonce=False

                
        for piece in piecelist: #calculates for overlap
            for otherpiece in piecelist: #checks all the pieces in the piecelist against each other to see if any overlap. It does that by calculating the distance between their center points
                if piece!=otherpiece:
                    
                    if otherpiece.difference(piece.x,piece.y)!=None:
                        distance=otherpiece.difference(piece.x,piece.y) #if they overlap, i.e their distance is less than the radius of the two, they are moved apart
                        piece.x=piece.x+distance
                        piece.y=piece.y+distance

        if not pygame.mixer.get_busy(): #keep checking if the music has stopped playing so it replay it
            file = 'mainsound.mp3'
            pygame.init()   
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

    
    
    for pieces in moving_list: #for every piece that is moving, checks whether it is striking the boundary, or is being pocketed
        scorelists=pieces.pocketting()
        pieces.deceleration()
        pieces.boundary()

       
        if pieces.velocity==0: #once the pieces have stopped moving, they are removed from the moving list
            pieces.remove(moving_list)
    

    while gameover: #if all the pieces have been pocketed, the game is over
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if score_list[0]>score_list[1]:
            playerwon="Player 1 won"
        else:
            playerwon="Player 2 won"
        paused("GAME OVER")
        messageonscreen(playerwon, black,485,700,mediumfont)
        button("Quit",750,450,100,50,lightred,red,quitgame)
        
        pygame.display.update()
        fps.tick(15)

    if len(piecelist)==1: #if only the striker is left, the game is over
        gameover=True    
    
    pygame.display.flip() #updates the entire window
    fps.tick(300)

pygame.quit() #uninitialising pygame
quit() #exits from python
