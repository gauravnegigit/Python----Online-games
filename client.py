import pygame
from network import Network
import pickle
pygame.font.init()

#screen variables
WIDTH , HEIGHT = (700 , 700)
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Client")
FPS = 60


#font variables
font = pygame.font.SysFont("ARIAL BLACK" , 50)

class Button :
    def __init__(self , text , x, y , color) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 200
        self.height = 100
    
    def draw(self , win ) :
        pygame.draw.rect(win , self.color , (self.x , self.y , self.width , self.height))
        font = pygame.font.SysFont("ARIAL BLACK" , 20)
        text = font.render(self.text , 1, (255 , 255, 255))
        win.blit(text , (self.x + round(self.width/2 - text.get_width()/2) , self.y + round(self.height/2 - text.get_height()/2)))
    
    def click(self , pos) :
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height :
            return True
        else :
            return False
        
def redraw(game , p) :
    WIN.fill((128 , 128 , 128))

    if not (game.connected()) :
        font = pygame.font.SysFont("ARIAL BLACK"  , 30)
        text = font.render('WAITING FOR PLAYER ....' , 1 , (255 , 0 , 0 ))
        WIN.blit(text , (WIDTH //2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2))

    else :    
        font = pygame.font.SysFont("ARIAL BLACK" , 30)
        text = font.render("YOUR MOVE" , 1, (0 , 255 , 255))
        WIN.blit(text , (80 , 200))

        text = font.render("OPPONENTS" , 1, (0 ,255 ,255))
        WIN.blit(text , (380 , 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        
        else :
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))
        if p == 1:
            WIN.blit(text2, (100, 350))
            WIN.blit(text1, (400, 350))
        else:
            WIN.blit(text1, (100, 350))
            WIN.blit(text2, (400, 350)) 


        for btn in btns:
            btn.draw(WIN)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]

def main() :
    run = True    
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("YOU ARE PLAYER " , player)

    while run :
        clock.tick(FPS)
        try :
            game = n.send("get")
        except :
            run = False
            print("Couldn't get the game !")
            break

        if game.bothWent() :
            redraw(game , player)
            pygame.time.delay(200)
            try :
                game = n.send("reset")
            except :
                run = False
                print("Couldn't get the game !")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(1500)
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                pos = pygame.mouse.get_pos() 
                for button in btns :
                    if button.click(pos) and game.connected() :
                        if player == 0 :
                            if not game.p1Went :
                                n.send(button.text)
                        else :
                            if not game.p2Went :
                                n.send(button.text)
        redraw(game , player)

def main_menu() :
    run = True 
    clock = pygame.time.Clock()
    while run :
        clock.tick(FPS)
        WIN.fill((128 , 128 , 128 ))
        text = font.render("Click to Play!", 1, (255,0,0))
        WIN.blit(text, (WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                run = False
                break
    
    main()
        
main_menu()
