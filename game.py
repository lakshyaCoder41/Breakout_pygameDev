import pygame
import random
pygame.init()

Win_width=800
Win_height=500
win=pygame.display.set_mode((Win_width,Win_height))
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

hitblock = pygame.mixer.Sound('bullet.wav')

bricks=[pygame.image.load("bricks/blue_block.png"),pygame.image.load("bricks/red_block.png"),pygame.image.load("bricks/yellow_block.png"),pygame.image.load("bricks/purple_block.png"),pygame.image.load("bricks/green_block.png")]

pygame.display.set_caption('Breakout by @lakshya')
clock=pygame.time.Clock()


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y,randbrick):
        pygame.sprite.Sprite.__init__(self)
        self.image =bricks[randbrick]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('paddle.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.velocity=5
        self.rect.center = (x, y)

    def move_left(self):
        if self.rect.x>self.velocity:
            self.rect.x -= 20

    def move_right(self):
        #below 100 is paddle width
        if self.rect.x<Win_width-100-self.velocity:
            self.rect.x += 20


class Ball(pygame.sprite.Sprite):
    velocity = 8
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.direction_x = 1
        self.direciton_y = 1
        self.image = pygame.image.load('ball.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width=32

    def flip_direction_x(self):
        self.direction_x *= -1

    def flip_direction_y(self):
        self.direciton_y *= -1

    def leaves_screen_bottom(self):
        if self.rect.x < 0 or self.rect.x > Win_width:
            self.flip_direction_x()
        if self.rect.y -(self.width//2)< 0:
            self.flip_direction_y()

        return self.rect.y > Win_height

    def move(self):
        self.rect.x += self.velocity * self.direction_x
        self.rect.y += self.velocity * self.direciton_y

def intro():
    font = pygame.font.SysFont('comicsans', 50, True)
    run=True
    while run:
        clock.tick(60)
        text1= font.render("Breakout by @lakshya", True, (255,0, 0))
        text2= font.render("Press Enter to continue...", True, (0,128, 0))
        win.blit(text1,(175,220))
        win.blit(text2,(175,275))


        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        if keys[pygame.K_RETURN]:
            breakout()
            run =False





def breakout():
    player=Player(250,470)
    ball=Ball(250,250)

    block_list=pygame.sprite.Group()
    player_list=pygame.sprite.Group()
    ball_list=pygame.sprite.Group()
    all_sprite=pygame.sprite.Group()

    player_list.add(player)
    ball_list.add(ball)
    all_sprite.add(player)
    all_sprite.add(ball)

    for i in range(0, 10, 2):
        for j in range(0, 3):
            randbrick=random.randint(0,4)
            block = Block(70 + i * 70, 50 + j * 50,randbrick)
            block_list.add(block)
            all_sprite.add(block)


    score = 0
    score_surface = None
    black=(0,0,0)
    font = pygame.font.SysFont('comicsans', 30, True)
    #main loop
    run=True
    while run:
        clock.tick(60)

        win.fill(black)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()

        if keys[pygame.K_RIGHT]:
            player.move_right()

        if keys[pygame.K_ESCAPE]:
            run = False

        if pygame.sprite.collide_mask(ball, player):
            ball.flip_direction_y()

        collided_blocks = pygame.sprite.groupcollide(
            block_list, ball_list, True, False, pygame.sprite.collide_mask)
            #above pygame.sprite.groupcollide  arguments
            # first group1 items
            # second group2 items
            # third boolean if True then on colliding items of group1 and group2 group1 item will vanish
            # fourth boolean if True then on colliding items of group1 and group2 group2 item will vanish
            # collide_mask
        if collided_blocks:
            hitblock.play()
            ball.flip_direction_y()
            score += len(collided_blocks)

        if score_surface is None or collided_blocks:
            score_surface = font.render(
                'Score: %d' % (score), False, (255,0,0))

        ball.move()
        if ball.leaves_screen_bottom():
            # reset the ball position
            ball.rect.x = 200
            ball.rect.y = 300

        all_sprite.update()
        all_sprite.draw(win)
        win.blit(score_surface, (50, 450))
        pygame.display.update()
        clock.tick(60)

intro()
