import pygame
from pygame.locals import *
import random
import sys

# Load the invader files:
greenInvader = pygame.transform.scale(pygame.image.load('green_invader.png'), (30, 20))
redInvader = pygame.transform.scale(pygame.image.load('red_invader.png'), (30, 20))
blueInvader = pygame.transform.scale(pygame.image.load('blue_invader.png'), (30, 20))
yellowInvader = pygame.transform.scale(pygame.image.load('yellow_invader.png'), (30, 20))

INVADERS = 20
INVADERS_COLORS = {'red': redInvader,
                   'green': greenInvader,
                   'blue': blueInvader,
                   'yellow': yellowInvader}

SCREENRECT = Rect(0, 0, 640, 480)
STARS = 250
STAR_COLORS = {'white': (255, 255, 255),
               'black': (0, 0, 0),
               'blue': (0, 0, 255),
               'green': (0, 255, 0),
               'red': (255, 0, 0)}


class Invader(pygame.sprite.Sprite):
    def __init__(self, position, color="green"):
        pygame.sprite.Sprite.__init__(self)

        self.screen = pygame.display.get_surface().get_rect()
        self.old = (0, 0, 0, 0)
        self.image = INVADERS_COLORS.get(color)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def horizontalSlide(self):
        self.old = self.rect
        self.rect = self.rect.move([0, 1])


def main():
    # Start Pygame.
    pygame.init()

    # Make it full screen.
    modes = pygame.display.list_modes()
    screen = pygame.display.set_mode(modes[0], FULLSCREEN)
    pygame.display.set_caption('Space Invaders Screen Saver - By J. R. Carroll 2013')

    # Make a black background.
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0, 0, 0))

    # Keep track of sprites.
    all = pygame.sprite.RenderUpdates()

    # Keep track of time.
    clock = pygame.time.Clock()

    # Display text on the screen that says "you didn't say the magic words"
    # Register a font and size with pygame.  Very important!
    font = pygame.font.Font(None, 100)

    # The text we want displayed!
    warning = font.render("Nuh-uh-uh... you didn't say the magic words!", 1,
                         (255, 255, 255))
    textpos = warning.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(warning, textpos)

    # Blit the background and all that's drawn to it!
    screen.blit(background, (0, 0))

    # Draw the stars.
    for star in range(0, STARS, 1):
        randColor = random.randint(1, 50)
        if randColor == 1:
            star_color = STAR_COLORS.get('red')
        elif randColor == 2:
            star_color = STAR_COLORS.get('blue')
        else:
            star_color = STAR_COLORS.get('white')

        randX = random.randint(0, modes[0][0])
        randY = random.randint(0, modes[0][1])
        pygame.draw.circle(screen, star_color, (randX, randY), 0)

    # Draw some invaders!
    allInvaders = []
    for invader in range(0, INVADERS, 1):
        randX = random.randint(0, modes[0][0])
        randColor = random.choice(INVADERS_COLORS.keys())
        invader = Invader((randX, 100), randColor)
        allInvaders.append(invader)
        screen.blit(invader.image, (randX, 100))

    # Update the game and draw the scene
    pygame.display.update()
    pygame.time.set_timer(26, 1)

    slide = True
    # Main Game loop!
    while True:
        for event in pygame.event.get():
            if event.type == QUIT \
                or (event.type == KEYDOWN and
                    event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == 26:

                if slide is True:
                    for invader in allInvaders:
                        blank = pygame.Surface((invader.rect.width, invader.rect.height))
                        blank.fill((0, 0, 0, 0))
                        invader.horizontalSlide()
                        screen.blit(blank, invader.old)
                        screen.blit(invader.image, invader.rect)
                        pygame.display.update([invader.rect])
                        if invader.

    # return Sprites
    all.clear(screen, background)

    # redraw the sprites
    all.update()

    # maintain frame rate
    dirty = all.draw(screen)
    pygame.display.update(dirty)

    # maintain frame rate
    clock.tick(90)


def magicword():
    # Display text on the screen that describes that magic key combinations
    # Register a font and size with pygame!  Very important
    font = pygame.font.Font(None, 15)
    # The text we want displayed!
    warning = font.render("Nuh-uh-uh... you didn't say the magic word!", 1,
                         (255, 255, 255))
    textpost = warning.get_rect()
    textpost.centerx = background.get_rect().centerx
    background.blit(warning, textpos)


def allMove(allInvaders):
    for invader in allInvaders:
        invader.horizontalSlide()

if __name__ == '__main__':
    main()
