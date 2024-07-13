import pygame
from pygame.locals import *
from pygame import mixer
from random import *

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

scr_width = 1600
scr_height = 900

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption('Flappy Vector')
obstacles = []
game_speed = 10
bg_chunks = []
player_trail = []
difficulty_change = [10,40,70]
show_menu = True
best_scores = []
menu_time = 0
death_message = ''

run = True

f = open('save.txt')
best_scores = f.read().strip().split('\n')
best_scores = [int(i) for i in best_scores if i.strip() != '']
f.close()

obst_appearance = [pygame.image.load('obstacle01.png').convert_alpha(), pygame.image.load('obstacle02.png').convert_alpha(), pygame.image.load('obstacle03.png').convert_alpha(), pygame.image.load('obstacle04.png').convert_alpha(), pygame.image.load('obstacle05.png').convert_alpha(), pygame.image.load('obstacle06.png').convert_alpha(), pygame.image.load('obstacle07.png').convert_alpha()]
bg_appearance = [pygame.image.load('bg.png').convert_alpha()]
player_appearance = [pygame.image.load('player.png'), pygame.image.load('player up.png'), pygame.image.load('player down.png')]
trail_appearance = [pygame.image.load('players trail.png').convert_alpha()]
black_bg = pygame.image.load('black bg.png').convert_alpha()
button_appearance = [pygame.image.load('button01.png').convert_alpha(), pygame.image.load('button01h.png').convert_alpha()]
checkbox_appearance = [pygame.image.load('checkbox off.png').convert_alpha(), pygame.image.load('checkbox on.png').convert_alpha()]
menu_bg = pygame.image.load('menu bg.png').convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale( player_appearance[0].convert_alpha(), (50,50) )
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.direct = -1
        self.click = False
        self.playerY = 0
    def update(self):
        global score
        if pygame.mouse.get_pressed()[0] == 1 and self.click == False and score > 0.14:
            self.click = True
            if self.direct == 1:
                self.direct = -1
            else:
                self.direct = 1
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False
        if self.direct == 1:
            self.image = pygame.transform.scale( player_appearance[1].convert_alpha(), (50,50) )
            self.rect.update(self.rect.x,self.rect.y, 40, 40)
            if self.rect.centery > 10:
                self.rect.y -= game_speed
            if self.rect.centery < 18:
                self.image = pygame.transform.scale( player_appearance[0].convert_alpha(), (50,50) )
                self.rect.y = 0
                self.playerY = self.rect.y + 25
            else:
                self.playerY = self.rect.y + 50
        if self.direct == -1:
            self.image = pygame.transform.scale( player_appearance[2].convert_alpha(), (50,50) )
            self.rect.update(self.rect.x,self.rect.y, 40, 40)
            if self.rect.centery < 890:
                self.rect.y += game_speed
            if self.rect.centery > 870:
                self.image = pygame.transform.scale( player_appearance[0].convert_alpha(), (50,50) )
                self.rect.y = 850
                self.playerY = self.rect.y + 25
            else:
                self.playerY = self.rect.y
                
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,difficulty_min,difficulty):
        pygame.sprite.Sprite.__init__(self)
        self.randomness = randint(difficulty_min,difficulty)
        if self.randomness == 4 or self.randomness == 5:
            self.size = randint(120, 140)
        elif self.randomness == 6:
            self.size = randint(80, 120)
        else:
            self.size = randint(140, 240)
        if self.randomness == 6:
            self.image = pygame.transform.scale( obst_appearance[self.randomness] , (self.size, round(self.size * 1.5)) ).convert_alpha()
        else:
            self.image = pygame.transform.scale( obst_appearance[self.randomness] , (self.size, self.size) ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.rect.height = self.size - 8
        self.rect.width = self.size - 10
        if self.randomness == 4:
            self.rect.y += 450
        if self.randomness == 5:
            self.rect.y -= 450
        if self.randomness == 6:
            self.rect.height *= 1.5

    def update(self):
        self.rect.x -= game_speed
        if self.randomness == 4:
            self.rect.y -= 5
        if self.randomness == 5:
            self.rect.y += 5
        if self.randomness == 6:
            self.rect.x -= 7

class BG_chunk(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image = bg_appearance[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,0]
    def update(self):
        self.rect.x -= 4
        if self.rect.x < -1600:
            self.rect.x = 1600

class Trail(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = trail_appearance[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        self.rect.x -= game_speed

class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,button_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale( button_appearance[0] , (240, 80) ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.rect.height = 80
        self.rect.width = 240
        self.button_type = button_type
    def update(self):
        global show_menu
        global score
        global best_scores
        global menu_time
        mousepos = pygame.mouse.get_pos()
        if self.rect.x <= mousepos[0] <= self.rect.x + self.rect.width and self.rect.y <= mousepos[1] <= self.rect.y + self.rect.height:
            self.image = pygame.transform.scale( button_appearance[1] , (240, 80) ).convert_alpha()
            if pygame.mouse.get_pressed()[0] == 1:
                if self.button_type == 'menu':
                    menu_time = 0
                    best_scores.append(round(score))
                    best_scores = sorted(best_scores, reverse=True)
                    while len(best_scores) > 3:
                        best_scores.pop(-1)
                    run = True
                    show_menu = True
                    obstacles.clear()
                    player_trail.clear()
                    rungame()
                elif self.button_type == 'continue':
                    best_scores.append(round(score))
                    best_scores = sorted(best_scores, reverse=True)
                    while len(best_scores) > 3:
                        best_scores.pop(-1)
                    obstacles.clear()
                    player_trail.clear()
                    run = True
                    show_menu = False
                    rungame()
                elif self.button_type == 'play':
                    run = True
                    show_menu = False
                    rungame()
                elif self.button_type == 'quit' and menu_time > 0.2:
                    f = open('save.txt', 'w')
                    s = ''
                    for i in best_scores:
                        s += str(i) + '\n'
                    f.write(s)
                    f.close()
                    pygame.quit()
                    exit()
        else:
            self.image = pygame.transform.scale( button_appearance[0] , (240, 80) ).convert_alpha()

class BlackBG(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale( black_bg , (width, height) ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.rect.width = width
        self.rect.height = height

class Checkbox(pygame.sprite.Sprite):
    def __init__(self,x,y,goal):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale( checkbox_appearance[0] , (70,70) ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.goal = goal
    def update(self):
        global best_scores
        if len(best_scores) > 0:
            if best_scores[0] >= self.goal:
                self.image = pygame.transform.scale( checkbox_appearance[1] , (70,70) ).convert_alpha()

class MenuBG(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = menu_bg
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)

player = Player(400,450)

todisplay = pygame.sprite.Group()
todisplay.add(player)
todisplay.add(obstacles)
for i in range(4):
    bg_chunks.append(BG_chunk(-400 + i*800))
toShowBG = pygame.sprite.Group()
toShowBG.add(bg_chunks)
failure_screen = pygame.sprite.Group()
menu_screen = pygame.sprite.Group()

score = 0
font = pygame.font.Font(None, 90)
font2 = pygame.font.Font(None, 130)
font_small = pygame.font.Font(None, 45)

toShowTrail = pygame.sprite.Group()
toShowTrail.add(player_trail)
    
def rungame():
    global game_speed
    global difficulty_change
    global show_menu
    global score
    global best_scores
    global failure_screen
    global menu_screen
    global death_message
    
    game_speed = 10
    
    player = Player(400,450)
    button = Button(800,550,'continue')
    button2 = Button(800,660,'menu')
    button3 = Button(800,500,'play')
    button4 = Button(800,650,'quit')
    achieve1 = Checkbox(1200,700,45)
    achieve2 = Checkbox(1200,600,75)
    achieve3 = Checkbox(1200,500,105)
    menu_backgr = MenuBG()
    
    todisplay = pygame.sprite.Group()
    todisplay.add(player)
    todisplay.add(obstacles)
    
    if show_menu == False:
        score = 0
    font = pygame.font.Font(None, 70)
    run = True
    time = 0
    cycles = 0
    trail_timer = 0
    
    if show_menu:
        pygame.mixer.music.load('Creo - Dark Tides.mp3')
        pygame.mixer.music.play(-1, 0.0, 0)
    else:
        pygame.mixer.music.load('Creo - Aurora.mp3')
        pygame.mixer.music.play(-1, 0.0, 0)
    
    while run and not show_menu:
        clock.tick(fps)
        screen.fill(Color(250,250,230))
        time += 1 / fps
        trail_timer += 1/fps
        
        if 5.5/game_speed < time:
            if cycles < 10:
                if score < difficulty_change[0]:
                    if randint(1,10) >= 6:
                        obstacles.append(Obstacle(2000 +randint(0,100), randint(0,900),0,3))
                elif score < difficulty_change[1]:
                    obstacles.append(Obstacle(2000 +randint(0,100), randint(0,900),0,3))
                elif score < difficulty_change[2]:
                    obstacles.append(Obstacle(2000 +randint(0,50), randint(0,900),0,3))
                    if randint(1,10) >= 7:
                        obstacles.append(Obstacle(2000 +randint(100,200), randint(0,900),4,5))
                else:
                    obstacles.append(Obstacle(2000 +randint(0,50), randint(0,900),0,3))
                    if randint(1,10) >= 4:
                        obstacles.append(Obstacle(2000 +randint(100,200), randint(0,900),4,6))
            time = 0
            
        if 0.72/game_speed < trail_timer < 0.72/game_speed + 1/30:
            player_trail.append(Trail(380, player.playerY))
            todisplay.add(player_trail)
            trail_timer = 0
        if len(player_trail) > 15:
            player_trail.pop(0)
            todisplay.empty()
            todisplay.add(player)
            todisplay.add(obstacles)
            todisplay.add(player_trail)
        
        if len(obstacles) > 16:
            obstacles.pop(0)
        
        if round(score) == difficulty_change[0]:
            game_speed = 12
        if round(score) == difficulty_change[1]:
            game_speed = 13.5
        if round(score) == difficulty_change[2]:
            game_speed = 15
        
        todisplay.empty()
        todisplay.add(player)
        todisplay.add(obstacles)
        todisplay.add(player_trail)
        
        toShowBG.draw(screen)
        toShowBG.update()

        todisplay.draw(screen)
        todisplay.update()
        
        text = font2.render(f"{round(score)}", True, Color(0,0,0))
        screen.blit(text, (800 - text.get_width() / 2, 100 - text.get_height() / 2))
        text = pygame.font.Font(None, 30).render("Soundtrack: Creo - Aurora", True, Color(255,255,255))
        screen.blit(text, (10, 870 - text.get_height() / 2))
        if score < difficulty_change[0]:
            text = font_small.render("Difficulty: 1", True, Color(0,0,0))
        elif score < difficulty_change[1]:
            text = font_small.render("Difficulty: 2", True, Color(0,0,0))
        elif score < difficulty_change[2]:
            text = font_small.render("Difficulty: 3", True, Color(0,0,0))
        else:
            text = font_small.render("Difficulty: max", True, Color(0,0,0))
        screen.blit(text, (800 - text.get_width() / 2, 30 - text.get_height() / 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            death_message = choice(['Didn\'t see that coming did you :DD', 'Do you ever go outside?', 'aahh you were doing so well', 'imagine dying to a square', 'You died :C', 'You weren\'t zigzagging well enough', 'you\'re such a pro'])
            run = False
        
        score += 1 / fps
    
        pygame.display.update()

# SEE ON MENÜÜ
    while run and show_menu:
        global menu_time
        
        clock.tick(fps)
        screen.fill(Color(124, 151, 161))
        
        
        if menu_time < 1:
            menu_time += 1/fps
        
        menu_screen.empty()
        menu_screen.add(MenuBG())
        menu_screen.add(BlackBG(800,450,500,750))
        menu_screen.add(BlackBG(1380,550,460,500))
        menu_screen.add(BlackBG(1400,20,400,500))
        menu_screen.add(button3)
        menu_screen.add(button4)
        menu_screen.add(achieve1)
        menu_screen.add(achieve2)
        menu_screen.add(achieve3)
        
        menu_screen.draw(screen)
        menu_screen.update()
        
        text = pygame.font.Font(None, 60).render("Play", True, Color(255,255,255))
        screen.blit(text, (800 - text.get_width() / 2, 500 - text.get_height() / 2))
        text = pygame.font.Font(None, 60).render("Quit", True, Color(255,255,255))
        screen.blit(text, (800 - text.get_width() / 2, 650 - text.get_height() / 2))
        text = pygame.font.Font(None, 30).render("Soundtrack: Creo - Dark Tides", True, Color(255,255,255))
        screen.blit(text, (10, 870 - text.get_height() / 2))
        
        text = pygame.font.Font(None, 90).render("Flappy Vector", True, Color(255,255,255))
        screen.blit(text, (800 - text.get_width() / 2, 160 - text.get_height() / 2))
        text = pygame.font.Font(None, 60).render(f"Your last score: {round(score)}", True, Color(77, 255, 75))
        screen.blit(text, (800 - text.get_width() / 2, 360 - text.get_height() / 2))
        text = font.render("High scores", True, Color(251, 255, 128))
        screen.blit(text, (1400 - text.get_width() / 2, 40 - text.get_height() / 2))
        text = pygame.font.Font(None, 70).render("Achievements", True, Color(47, 247, 255))
        screen.blit(text, (1380 - text.get_width() / 2, 400 - text.get_height() / 2))
        text = pygame.font.Font(None, 42).render("Born to be a noob", True, Color(255,255,255))
        screen.blit(text, (1250, 700 - 18 - text.get_height() / 2))
        text = pygame.font.Font(None, 40).render("Achieve the score of 45", True, Color(47, 209, 255))
        screen.blit(text, (1250, 700 + 18 - text.get_height() / 2))
        text = pygame.font.Font(None, 42).render("Getting good", True, Color(255,255,255))
        screen.blit(text, (1250, 600 - 18 - text.get_height() / 2))
        text = pygame.font.Font(None, 40).render("Achieve the score of 75", True, Color(47, 209, 255))
        screen.blit(text, (1250, 600 + 18 - text.get_height() / 2))
        text = pygame.font.Font(None, 42).render("A+ in geometry", True, Color(255,255,255))
        screen.blit(text, (1250, 500 - 18 - text.get_height() / 2))
        text = pygame.font.Font(None, 40).render("Achieve the score of 105", True, Color(47, 209, 255))
        screen.blit(text, (1250, 500 + 18 - text.get_height() / 2))
        
        for i in range(len(best_scores)):
            text = font.render(f"({i+1})  {best_scores[i]}", True, Color(250, 245, 175))
            screen.blit(text, (1400 - text.get_width() / 2, 100 + i*50 - text.get_height() / 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                run = True
                show_menu = False
                rungame()
        
        pygame.display.update()
        
# SEE ON KAOTAMISE EKRAAN
    while True:        
        failure_screen.empty()
        failure_screen.add(BlackBG(800,500,400,600))
        failure_screen.add(button)
        failure_screen.add(button2)
        
        toShowBG.draw(screen)
        todisplay.draw(screen)
        
        failure_screen.draw(screen)
        failure_screen.update()
        
        text = pygame.font.Font(None, 90).render(death_message, True, Color(0,0,0))
        screen.blit(text, (800 - text.get_width() / 2, 130 - text.get_height() / 2))
        text = font.render(f"Game Over!", True, Color(255,255,255))
        screen.blit(text, (800 - text.get_width() / 2, 270 - text.get_height() / 2))
        text = font.render(f"Your score: {round(score)}", True, Color(255,255,255))
        screen.blit(text, (800 - text.get_width() / 2, 400 - text.get_height() / 2))
        text = pygame.font.Font(None, 60).render("Continue", True, Color(255,255,255))
        screen.blit(text, (800 - text.get_width() / 2, 550 - text.get_height() / 2))
        text = pygame.font.Font(None, 60).render("Menu", True, Color(255,255,255))
        screen.blit(text, (800 - text.get_width() / 2, 660 - text.get_height() / 2))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                best_scores.append(round(score))
                best_scores = sorted(best_scores, reverse=True)
                while len(best_scores) > 3:
                    best_scores.pop(-1)
                run = True
                show_menu = True
                obstacles.clear()
                player_trail.clear()
                rungame()
rungame()

pygame.display.quit()
pygame.quit()