import pygame
import os
import neat
import random
import time 
pygame.font.init()
width = 580
height = 700

'''pygame.init()
screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h'''

print(width)
print(height)

# GETTING IMAGES 
bird_img = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

stat_font = pygame.font.SysFont('comicsans', 30)
gameover_font = pygame.font.SysFont('arial', 40)
#CONSTANTS 

class bird :
    imgs = bird_img
    max_rot = 25
    rot_vel = 25 
    animation_time = 1

    def __init__(self,x,y) :
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.height = self.y
        self.vel = 0
        self.img_count = 0
        self.img = self.imgs[0]

    def jump(self) :
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self) :
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.7 *self.tick_count**2
        if d>= 16 :
            d =16

        if d < 0 :
            d -= 2

        self.y = self.y + d
        if d < 0 or self.y < self.height + 50 :
            if self.tilt < self.max_rot :
                self.tilt = self.max_rot
        else :
            if self.tilt > -90 :
                self.tilt -= self.rot_vel


    def draw(self,win) :

        self.img_count += 1

        
        if self.img_count <= self.animation_time :
            self.img = self.imgs[0]
        elif self.img_count <= self.animation_time*2 :
            self.img = self.imgs[1]
        elif self.img_count <= self.animation_time*3 :
             self.img = self.imgs[2]

        elif self.img_count <= self.animation_time*4 :
             self.img = self.imgs[1]     

        elif self.img_count >= self.animation_time*4 + 1:
            self.img = self.imgs[0]
            self.img_count = 0


        if self.tilt <= -80 : 
            self.img = self.imgs[1]
            self.img_count = self.animation_time*2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)

        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center )
        win.blit(rotated_img,new_rect.topleft)
        

    def get_mask(self) :
        return pygame.mask.from_surface(self.img)
    


class pipe :
    gap = 300
    vel = 10

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 190
        self.top = 0
        self.top = 0
        self.pipe_top = pygame.transform.flip(pipe_img, False, True)
        self.pipe_bottom = pipe_img
        self.passed = False
        self.set_height()

    def set_height(self) :
        self.height = random.randrange(40,360)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self) :
        self.x -= self.vel

    def draw(self,win):
        win.blit(self.pipe_top, (self.x,self.top))
        win.blit(self.pipe_bottom, (self.x,self.bottom))

    def collide(self, bird) :
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)
        """returns none if dont collide"""

        if t_point or b_point :
            return True
        return False

class base :
    vel = 5
    width = base_img.get_width()
    img = base_img

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.width <0 :
            self.x1 = self.x2 + self.width
        if self.x2 + self.width <0 :
            self.x2 = self.x1 + self.width

    def draw(self,win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))

def draw_window(win,bird,pipes,base,score):
    win.blit(bg_img,(5,-250))
    for pipe in pipes :
        pipe.draw(win)
    text = stat_font.render("Score:" + str(score),1, (255,255,255) )
    win.blit(text,(50,50))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()


def main() :
    birdi = bird(230,250)
    Base = base(560)
    pipes = [pipe(600)]
    win = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    score = 0
    
    run = True
    game_over = False
    while run :
        clock.tick(30)
        for event in pygame.event.get() :
            if event.type== pygame.QUIT :
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over :
                        main()
                    else :
                        birdi.jump()
        
        if not game_over :

            birdi.move() 
            Base.move()
            add_Pipe = False
            rem = []
            for Pipe in pipes:
                Pipe.move()
                if Pipe.collide(birdi):
                   
                    game_over = True

                if Pipe.x + Pipe.pipe_top.get_width() < 0 :
                    rem.append(Pipe)
                if not Pipe.passed and Pipe.x < birdi.x :
                    Pipe.passed = True
                    add_Pipe = True
                

            

        if add_Pipe :
            score += 1
            pipes.append(pipe(600))

        for r in rem :
            pipes.remove(r)

        if birdi.y + birdi.img.get_height() > 570 :
            
            game_over = True
            #run = False
            #print("Done")
            #pygame.quit()

               
        draw_window(win, birdi, pipes,Base,score)    

        if game_over:
            text = gameover_font.render("Game Over! Press Space to Restart", 1, (0, 0, 0))
            win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            pygame.display.update()    
    pygame.quit()
    quit()

main()




    










