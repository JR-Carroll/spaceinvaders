import pygame
from pygame.locals import *
import random
import sys

# Load the invader files:
greenInvader = pygame.transform.scale(pygame.image.load('green_invader.png'), (30, 20))
redInvader = pygame.transform.scale(pygame.image.load('red_invader.png'), (30, 20))
blueInvader = pygame.transform.scale(pygame.image.load('blue_invader.png'), (30, 20))
yellowInvader = pygame.transform.scale(pygame.image.load('yellow_invader.png'), (30, 20))

INVADERS = 10
INVADERS_COLORS = {'red': redInvader,
                   'green': greenInvader,
                   'blue': blueInvader,
                   'yellow': yellowInvader}

# Invader mapping
INVADER_LOOKUP = {1: 'red',
                  2: 'green',
                  3: 'blue',
                  4: 'yellow'}

# SCREENRECT = Rect(0, 0, 640, 480)
STARS = 250
STAR_COLORS = {'white': (255, 255, 255),
               'black': (0, 0, 0),
               'blue': (0, 0, 255),
               'green': (0, 255, 0),
               'red': (255, 0, 0)}

# Invader layouts
invaderMap1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               [1, 3, 3, 3, 3, 3, 3, 3, 3, 2],
               [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

invaderMap2 = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
               [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
               [2, 1, 2, 2, 2, 1, 2, 2, 2, 1],
               [2, 2, 1, 2, 2, 2, 1, 2, 2, 1]]

invaderMap3 = [[2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2],
               [1, 2, 3, 3, 3, 3, 3, 3, 3, 2, 1],
               [2, 3, 2, 1, 2, 1, 1, 2, 1, 2, 3]]

# Cache of all the invader positions.
allInvaderMaps = (invaderMap1, invaderMap2, invaderMap3)

# Base class for invaders
class Invader(pygame.sprite.Sprite):
    def __init__(self, position, color="green"):
        pygame.sprite.Sprite.__init__(self)

        self.screen = pygame.display.get_surface().get_rect()
        self.old = (0, 0, 0, 0)
        self.image = INVADERS_COLORS.get(color).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # State-machine for keeping track of vertical vs horizontal movement
        self.moveOptions = ("left", "right", "down")
        self.lastMove = None
        self.lastHoriz = None

        # Counter/timer for keeping track of when to move
        self.moveNow = 0

    def moveInvader(self):
        """
        Helper method for determining if the invader needs to move.
        """
        self.moveNow += 1

        if(self.moveNow > 50):
            ## Move the invader down
            if(self.lastMove is None or self.lastMove is "left"
                    or self.lastMove is "right"):
                _move_ = self.verticalSlide()
                self.lastMove = _move_

            ## Move the invader left/right
            elif(self.lastMove is "down"):
                _move_ = self.horizontalSlide(self.lastMove)
                self.lastMove = _move_
            self.moveNow = 0

    def verticalSlide(self):
        """
        Used to move the invaders down
        """

        self.old = self.rect
        self.rect = self.rect.move([0, 10])
        return "down"

    def horizontalSlide(self, lastMove):
        """
        Used to move the invaders left/right
        """

        if(self.lastHoriz is None or self.lastHoriz is "left"):
            _leftORRight_ = 10
            _move_ = "right"
        elif(self.lastHoriz is "right"):
            _leftORRight_ = -10
            _move_ = "left"

        self.old = self.rect
        self.rect = self.rect.move([_leftORRight_, 0])
        self.lastHoriz = _move_
        return _move_

def main():
    # Start Pygame.
    pygame.init()

    # Make it full screen.
    modes = pygame.display.list_modes()
    screen = pygame.display.set_mode((modes[2]), pygame.FULLSCREEN)
    # pygame.FULLSCREEN
    pygame.display.set_caption('Space Invaders Screen Saver - By J. R. Carroll 2013')

    # Make a black background.
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0, 0, 0))

    # Keep track of sprites.
    # allSprites = pygame.sprite.RenderUpdates()

    # Keep track of time.
    clock = pygame.time.Clock()

    # Display text on the screen that says "you didn't say the magic words"
    # Register a font and size with pygame.  Very important!
    font = pygame.font.Font(None, 50)

    # The text we want displayed!
    warning = font.render("Nuh-uh-uh... you didn't say the magic words!", 1,
                         (100, 100, 100))
    textpos = warning.get_rect()
    textpos.centerx = background.get_rect().centerx

    # Blit the background and all that's drawn to it!
    background.blit(warning, textpos)

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
        pygame.draw.circle(background, star_color, (randX, randY), 0)

    # background.blit(background, (0,0))
    screen.blit(background, (0, 0))

    # Draw some invaders!
    allInvaders = []

    firstRowInvader = 100
    spaceInvaderRowHeight = 50

    for marchingLine in random.choice(allInvaderMaps):
        firstInvader = 350
        spaceInvaderWidth = 50

        for newInvader in marchingLine:
            invader = Invader((firstInvader, firstRowInvader), INVADER_LOOKUP.get(newInvader))
            allInvaders.append(invader)
            firstInvader += spaceInvaderWidth

        firstRowInvader += spaceInvaderRowHeight

    # for invader in range(0, INVADERS, 1):
    #     randX = random.randint(0, modes[0][0])
    #     randColor = random.choice(INVADERS_COLORS.keys())
    #     invader = Invader((randX, 100), randColor)
    #     allInvaders.append(invader)
        # background.blit(invader.image, (randX, 100))

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
                        invader.moveInvader()
                        screen.blit(background, invader.old, invader.old)
                        screen.blit(invader.image, invader.rect)
                        pygame.display.update([invader.old, invader.rect])

    # return Sprites
    # allSprites.clear(screen, background)

    # redraw the sprites
    # allSprites.update()

    # maintain frame rate
    # dirty = allSprites.draw(screen)
    # pygame.display.update(dirty)

    # maintain frame rate
    clock.tick(90)


if __name__ == '__main__':
    main()
