

import random, pygame, sys
from pygame.locals import *

FPS = 30
windowwidth = 600
windowheight = 500

tilesize = 80
leveltilesize = 160

BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
RED =           (255,   0,   0)
PURPLE =        (255,   0, 255)
DARKSLATEGRAY = ( 49,  79,  79)
NEW =           (  3, 150, 100)
LIGHTGRAY =     (105, 105, 105)
ORANGERED =     (255,  69,   0)
MAROON =        (176,  48,  96)
DEEPPINK =      (255,  20, 147)
DARKVIOLET =    (148,   0, 211)
YELLOW =        (255, 255,   0)
HOTPINK =       (255, 105, 180)
PERU =          (205, 133,  65)

bgcolor = (255, 218, 165) 
openbgcolor = WHITE
levelbgcolor = LIGHTGRAY
leveltilecolor = BLACK
tilecolor = WHITE
textcolor = BLACK
boardercolor = BLACK


basicfontsize = 40
basicfontsize1 = 100

buttoncolor = WHITE
buttontextcolor = BLACK
messagecolor = BLACK



UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'




def main():
       global FPSCLOCK, displaysurf, BASICFONT, boardwidth, boardheight, xmargin, ymargin, level, windowwidth, windowheight
 
       pygame.init()
       soundObj = pygame.mixer.Sound('WhatsApp Audio 2017-08-16 at 8.49.20 PM.mpeg')
       FPSCLOCK = pygame.time.Clock()

       BASICFONT = pygame.font.Font('freesansbold.ttf', basicfontsize)
       
       displaysurf = pygame.display.set_mode((windowwidth,windowheight))
       pygame.display.set_caption('SLIDE_PUZZLE ;)')

       boardwidth = 3
       boardheight = 3

       xmargin = int((windowwidth - (tilesize*boardwidth + (boardwidth - 1))) / 2)
       ymargin = int((windowheight - (tilesize*boardheight + (boardheight - 1))) / 2)

       
       opening()
       
       level = leveling()
       
       boardwidth = 3
       boardheight = 3
       

       
       mainboard = getrandomisedboard(40)
       solvedboard = getsolvedboard()
       
       displaysurf.fill(bgcolor)
       left, top  = (0, 0)
       pygame.draw.rect(displaysurf, boardercolor, (left + 10, top+10, windowwidth-20, windowheight-20), 10)
   
       while True:
            left, top = (0,0)
            displaysurf.fill(bgcolor)
            pygame.draw.rect(displaysurf, boardercolor, (left + 10, top+10, windowwidth-20, windowheight-20), 10)
            #pygame.display.update()
            shift = None
            message = ''
            if mainboard == solvedboard :
                 pygame.time.wait(500)
                 gamewonanimation(mainboard)
                 mainboard = getrandomisedboard(40)
            
            drawboard(mainboard)

            ifquit()
            for event in pygame.event.get():
                 if event.type == MOUSEBUTTONUP:
                      
                      
                      spotx, spoty = getspotclicked(mainboard, event.pos[0], event.pos[1])
                      if (spotx,spoty) != (None, None) :
                           
                      
                             blankx, blanky = getblankposition(mainboard)
                             if spotx == blankx + 1 and spoty == blanky:
                                   shift = LEFT
                             elif spotx == blankx - 1 and spoty == blanky:
                                   shift = RIGHT
                             elif spotx == blankx and spoty == blanky + 1:
                                   shift = UP
                             elif spotx == blankx and spoty == blanky-1:
                                   shift = DOWN
                


                 elif event.type == KEYUP:
                      if event.key in (K_LEFT, K_a) and isvalid(mainboard, LEFT):
                             shift = LEFT
                      elif event.key in (K_RIGHT,K_d) and isvalid(mainboard, RIGHT):
                             shift = RIGHT
                      elif event.key in (K_DOWN, K_s) and isvalid(mainboard, DOWN):
                             shift = DOWN
                      elif event.key in (K_UP, K_w) and isvalid(mainboard, UP):
                             shift = UP
               

               

            if shift:
                 soundObj.play()
                 shiftanimation(shift, mainboard, 15)
                 
                 
                 soundObj.stop()
                 makemove(shift, mainboard)

            pygame.display.update()
            FPSCLOCK.tick(FPS)




def gamewonanimation(board):
      left, top = getlefttop(2,2)
      drawboard(board)

      if level == 'monalisa':
           
           img = pygame.image.load('monalisa9.jpeg')
           displaysurf.blit(img,(left,top))

      elif level == 'dogs':
            img = pygame.image.load('dogs9.png')
            displaysurf.blit(img,(left,top))

      elif level == 'night':
            img = pygame.image.load('night9.png')
            displaysurf.blit(img,(left,top))

      elif level == 'ghost':
            img = pygame.image.load('ghost9.png')
            displaysurf.blit(img,(left,top))

      elif level == 'number':
            pygame.draw.rect(displaysurf, tilecolor, (left, top, tilesize, tilesize))
 
            textsurf = BASICFONT.render("9", True, textcolor)
            textrect = textsurf.get_rect()
            textrect.center = left + int(tilesize / 2), top + int(tilesize / 2)

            displaysurf.blit(textsurf,textrect)

      pygame.display.update()
      pygame.time.wait(3000)
      displaysurf.fill(bgcolor)
      img = pygame.image.load('giphy.gif')
      displaysurf.blit(img,(160, 120))
      pygame.display.update()
      pygame.time.wait(5000)



def getrandomisedboard(total):
       
       
       board = getsolvedboard()
       drawboard(board)
       pygame.display.update()
       pygame.time.wait(2000)
       lastmove = None
       for i in range(total):
            
            move = getrandommove(board,lastmove)
            shiftanimation(move,board,30)
            makemove(move, board)
            lastmove = move
            
       return board          
       


def getrandommove(board, lastmove = None):
       validmoves = [UP, DOWN, LEFT, RIGHT]
       if lastmove == UP or not isvalid(board, DOWN):
            validmoves.remove(DOWN)
       if lastmove == DOWN or not isvalid(board, UP):
            validmoves.remove(UP)
       if lastmove == LEFT or not isvalid(board, RIGHT):
            validmoves.remove(RIGHT)
       if lastmove == RIGHT or not isvalid(board, LEFT):
            validmoves.remove(LEFT)

       return random.choice(validmoves)

       
def getsolvedboard():
       
       k = 1
       board = []
       for i in range(boardwidth):
            k = i + 1
            column = []
            for j in range(boardheight):
                 column.append(k)
                 k = k + boardwidth
            board.append(column)
            #k = k - boardwidth*(boardheight-1) + boardwidth - 1
       board[boardheight-1][boardwidth-1] = None
       return board 


def ifquit():
       for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
       for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                 pygame.quit()
                 sys.exit()
            pygame.event.post(event)


def getblankposition(board):
       for i in range(boardheight):
            for j in range(boardwidth):
                 if board[i][j] == None:
                      return (i,j)


def isvalid(board, shift): 
 
       blankx, blanky = getblankposition(board)
       return (shift == UP and blanky != (boardheight - 1)) or (shift == DOWN and blanky != 0) or (shift == LEFT and blankx != (boardwidth-1)) or (shift == RIGHT and blankx != 0)


def makemove(shift, board):
       
       blankx, blanky = getblankposition(board)
       if shift == LEFT :
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx+1][blanky], board[blankx][blanky];
       elif shift == RIGHT :
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx-1][blanky], board[blankx][blanky];
       elif shift == UP :
            board[blankx][blanky], board[blankx][blanky+1] = board[blankx][blanky+1], board[blankx][blanky];
       elif shift == DOWN :
            board[blankx][blanky], board[blankx][blanky-1] = board[blankx][blanky-1], board[blankx][blanky];



def getlefttop(x, y):
       left = xmargin + (x*tilesize) + x - 1;
       top = ymargin + y*tilesize + y - 1;
       return (left,top)
 

def getspotclicked(board,x,y):
       for i in range(boardheight):
            for j in range(boardwidth):
                 left, top = getlefttop(i, j)
                 tilerect = pygame.Rect(left, top, tilesize, tilesize)
                 if tilerect.collidepoint(x,y):
                      return (i,j)
       return (None,None)


def drawboard(board):
       displaysurf.fill(bgcolor)
       
       pygame.draw.rect(displaysurf, BLACK, (0, 0, windowwidth, windowheight), 50)
       for i in range(boardheight):
            for j in range(boardwidth):
                 if board[i][j]:
                      
                      drawtile(i, j, board[i][j])
       left, top = getlefttop(0,0)
       width = boardwidth*tilesize
       height = boardheight*tilesize
 
       pygame.draw.rect(displaysurf, boardercolor, (left - 7, top - 7, width +14, height + 14), 8)

    
def drawtile(i, j, number, a = 0, b = 0):
       left, top = getlefttop(i,j)
       if level == 'number':
            pygame.draw.rect(displaysurf, tilecolor, (left+a, top+b, tilesize, tilesize))
 
            textsurf = BASICFONT.render(str(number), True, textcolor)
            textrect = textsurf.get_rect()
            textrect.center = left + int(tilesize / 2)+a, top + int(tilesize / 2)+b

            displaysurf.blit(textsurf,textrect)
       else:
            imgload(number, left, top, a, b)
            #displaysurf.blit(img,(left+a,top+b))


def imgload(number, left, top, a, b):
       if number == 1 and level == 'dogs':
            img = pygame.image.load('dogs1.png')
            displaysurf.blit(img,(left+a,top+b))
            
       elif number == 2 and level == 'dogs':
            img = pygame.image.load('dogs2.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 3 and level == 'dogs':
            img = pygame.image.load('dogs3.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 4 and level == 'dogs':
            img = pygame.image.load('dogs4.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 5 and level == 'dogs':
            img = pygame.image.load('dogs5.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 6 and level == 'dogs':
            img = pygame.image.load('dogs6.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 7 and level == 'dogs':
            img = pygame.image.load('dogs7.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 8 and level == 'dogs':
            img = pygame.image.load('dogs8.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 1 and level == 'monalisa':
            img = pygame.image.load('monalisa1.jpeg')
            displaysurf.blit(img,(left+a,top+b))
            
       elif number == 2 and level == 'monalisa':
            img = pygame.image.load('monalisa2.jpeg')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 3 and level == 'monalisa':
            img = pygame.image.load('monalisa3.jpeg')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 4 and level == 'monalisa':
            img = pygame.image.load('monalisa4.jpeg')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 5 and level == 'monalisa':
            img = pygame.image.load('monalisa5.jpeg')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 6 and level == 'monalisa':
            img = pygame.image.load('monalisa6.jpeg')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 7 and level == 'monalisa':
            img = pygame.image.load('monalisa7.jpeg')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 8 and level == 'monalisa':
            img = pygame.image.load('monalisa8.jpeg')
            displaysurf.blit(img,(left+a,top+b))
       elif number == 1 and level == 'night':
            img = pygame.image.load('night1.png')
            displaysurf.blit(img,(left+a,top+b))
            
       elif number == 2 and level == 'night':
            img = pygame.image.load('night2.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 3 and level == 'night':
            img = pygame.image.load('night3.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 4 and level == 'night':
            img = pygame.image.load('night4.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 5 and level == 'night':
            img = pygame.image.load('night5.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 6 and level == 'night':
            img = pygame.image.load('night6.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 7 and level == 'night':
            img = pygame.image.load('night7.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 8 and level == 'night':
            img = pygame.image.load('night8.png')
            displaysurf.blit(img,(left+a,top+b))
 
       elif number == 1 and level == 'ghost':
            img = pygame.image.load('ghost1.png')
            displaysurf.blit(img,(left+a,top+b))
            
       elif number == 2 and level == 'ghost':
            img = pygame.image.load('ghost2.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 3 and level == 'ghost':
            img = pygame.image.load('ghost3.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 4 and level == 'ghost':
            img = pygame.image.load('ghost4.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 5 and level == 'ghost':
            img = pygame.image.load('ghost5.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 6 and level == 'ghost':
            img = pygame.image.load('ghost6.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 7 and level == 'ghost':
            img = pygame.image.load('ghost7.png')
            displaysurf.blit(img,(left+a,top+b))

       elif number == 8 and level == 'ghost':
            img = pygame.image.load('ghost8.png')
            displaysurf.blit(img,(left+a,top+b))


def shiftanimation(shift, board, animationspeed):
       blankx, blanky = getblankposition(board)
       if shift == UP:
            movex = blankx
            movey = blanky + 1
       elif shift == DOWN:
            movex = blankx
            movey = blanky - 1
       elif shift == LEFT:
            movex = blankx + 1
            movey = blanky
       elif shift == RIGHT:
            movex = blankx - 1
            movey = blanky

       drawboard(board)
       basesurf = displaysurf.copy()
       
       movel, movet = getlefttop(movex,movey)
       
       pygame.draw.rect(basesurf, bgcolor, (movel, movet, tilesize, tilesize))  
       k = animationspeed
       for i in range(0, tilesize+8, animationspeed):
            ifquit()
            displaysurf.blit(basesurf,(0,0))
            if shift == UP:
                 drawtile(movex, movey, board[movex][movey],0,-i)
            
            if shift == DOWN:
                 drawtile(movex,movey, board[movex][movey],0,i)
            if shift == LEFT:
                 drawtile(movex, movey, board[movex][movey], -i, 0)
            if shift == RIGHT:
                 drawtile(movex, movey, board[movex][movey], i, 0)
            

            pygame.display.update()
            FPSCLOCK.tick(FPS)
       
       


def maketext(text, color, backcolor, top, left):
       textsurf = BASICFONT.render(text, True, color, backcolor)
       textrect = textsurf.get_rect()
       textrect.topleft = (top, left)
       return (textsurf, textrect)



def opening():

       displaysurf.fill(openbgcolor)
       
       arr = []
       cnt = 0
       for i in range(0, windowheight+1, 100):
            for j in range(0, windowwidth+1, 100):
                 arr.append([i,j])
                 cnt += 1
       colors = []

       for i in range(40):
            a1 = random.randint(0,255)
            a2 = random.randint(0,255)
            a3 = random.randint(0,255)
            colors.append([a1,a2,a3])
       
       
       for i in range(cnt):
            
            color = random.choice(colors)
            left, top = random.choice(arr)  
            arr.remove([left,top])   
            pygame.draw.rect(displaysurf, color, (left, top, 100, 100))
            pygame.display.update()
            pygame.time.wait(50)
       
       textsurf, textrect = maketext('SLIDE PUZZLE', messagecolor, openbgcolor, 150, 200)
       displaysurf.blit(textsurf, textrect)
     
       pygame.display.update()
       pygame.time.wait(2000)



def leveling():
       displaysurf.fill(levelbgcolor)
       
       x = int((windowwidth - 3 * leveltilesize) / 4)
       y = int((windowheight - 3 * leveltilesize) / 4)
       while True:
            img1 = pygame.image.load('dogs.jpeg')
            displaysurf.blit(img1,(x,y))
            
            img2 = pygame.image.load('monalisa.jpeg')
            displaysurf.blit(img2,(x,3*y + 2*leveltilesize))

            img3 = pygame.image.load('night.jpeg')
            displaysurf.blit(img3,(3*x + 2 * leveltilesize,y))
            
            img4 = pygame.image.load('ghost.jpeg')
            displaysurf.blit(img4,(3*x + 2 * leveltilesize,3*y + 2*leveltilesize))

            img5 = pygame.image.load('number.jpeg')
            displaysurf.blit(img5,(2*x + leveltilesize,int((windowheight-leveltilesize)/2)))

            box1rect = pygame.Rect(x,y, leveltilesize, leveltilesize)
            box2rect = pygame.Rect(x,3*y + 2*leveltilesize, leveltilesize, leveltilesize)
            box3rect = pygame.Rect(3*x + 2 * leveltilesize,y, leveltilesize, leveltilesize)
            box4rect = pygame.Rect(3*x + 2 * leveltilesize,3*y + 2*leveltilesize, leveltilesize, leveltilesize)
            box5rect = pygame.Rect(2*x + leveltilesize,int((windowheight-leveltilesize)/2), leveltilesize, leveltilesize)

            ifquit()
            pygame.display.update()

            for event in pygame.event.get():
                 if event.type == MOUSEBUTTONUP:
                      
                      if box1rect.collidepoint(event.pos):
                           return 'dogs'
                      elif box2rect.collidepoint(event.pos):
                           return 'monalisa'
                      elif box3rect.collidepoint(event.pos):
                           return 'night'
                      elif box4rect.collidepoint(event.pos):
                           return 'ghost'
                      elif box5rect.collidepoint(event.pos):
                           return 'number'
                      
               
      



if __name__ == '__main__':
       main()


