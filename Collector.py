import random
import sys
import os
import pygame
import time
import math

# display
display_width = 600
display_height = 600

# garbage can
garbage_width = 50
garbage_height = 50

# trash
trash_width = 25
trash_height = 25

# treasure
treasure_width = 25
treasure_height = 25
dist = 10

FPS = 120

# scoreboard
score_xy = (444, 70)
checkbox_xy = (318, 68)
# settings
score_interval = 100
bonus = 10
penalty_interval = 200
time_limit = 60

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# initialize pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

# initialize other stuff
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Garbage Collector')
clock = pygame.time.Clock()

# load images
icon = pygame.image.load('images/icon.png')
title_screen = pygame.image.load('images/title_screen.png')
about_screen = pygame.image.load('images/about_screen.png')
garbage_can = pygame.image.load('images/garbagecan.png')
paper = pygame.image.load('images/paper.png')
banana = pygame.image.load('images/banana.png')
banner = pygame.image.load('images/fixed_banner.png')
unchecked = pygame.image.load('images/unchecked.png')
checkmark = pygame.image.load('images/checkmark.png')
small_gem = pygame.image.load('images/small_gem.png')

# load sounds
ding = pygame.mixer.Sound('sounds/ding.wav')
hit = pygame.mixer.Sound('sounds/hit.wav')
click = pygame.mixer.Sound('sounds/click.wav')

# place trash of given type at given x, y
def trash(x, y, type):
    # crumpled paper
    if type == 1:
        gameDisplay.blit(paper, (x, y))
    # banana
    elif type == 2:
        gameDisplay.blit(banana, (x, y))

# place treasure of given type at given x, y
def treasure(x, y, type):
    # small gem
    if type == 1:
        gameDisplay.blit(small_gem, (x, y))

# place garbage can at given x, y
def garbage(x, y):
    gameDisplay.blit(garbage_can, (x, y))

def update_score(new_score):
    score_font = pygame.font.Font('freesansbold.ttf', 24)
    surface, rectangle = text_objects("%d" % new_score, score_font, black)
    gameDisplay.blit(surface, score_xy)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 80)
    TextSurf, TextRect = text_objects(text, large_text, black)
    TextRect.center = (display_width / 2, display_height / 2)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    time.sleep(2)

    game_loop()

def RIP():
    message_display('Game Over')

def about():
    while True:
        for event in pygame.event.get():
            # if x button is clicked
            if event.type == pygame.QUIT:
                # quit game
                sys.exit()
            # if back to main menu button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # main menu: (150, 460) to (449, 519)
                if pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                    pygame.mouse.get_pos()[1] >=460 and pygame.mouse.get_pos()[1] <= 519:
                    click.play()
                    time.sleep(0.2)
                    return
        gameDisplay.blit(about_screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

# handles start menu, runs before game_loop()
def title_loop():
    while True:
        for event in pygame.event.get():
            # if x button is clicked
            if event.type == pygame.QUIT:
                # quit game
                sys.exit()
            # handles start menu buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                # start game: (150, 250) to (449, 309)
                if pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                    pygame.mouse.get_pos()[1] >= 250 and pygame.mouse.get_pos()[1] <= 309:
                    click.play()
                    time.sleep(0.2)
                    return
                # leaderboard: (150, 320) to (449, 379)
                elif pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                    pygame.mouse.get_pos()[1] >= 320 and pygame.mouse.get_pos()[1] <= 379:
                    click.play()
                # options: (150, 390) to (449, 449)
                elif pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                    pygame.mouse.get_pos()[1] >= 390 and pygame.mouse.get_pos()[1] <= 449:
                    click.play()
                # about: (150, 460) to (449, 519)
                elif pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                     pygame.mouse.get_pos()[1] >= 460 and pygame.mouse.get_pos()[1] <= 519:
                    click.play()
                    time.sleep(0.2)
                    about()


        gameDisplay.blit(title_screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

def countdown_loop():
    start_time = pygame.time.get_ticks()
    countdown_time = 0
    while (countdown_time - start_time) < 1000:
        gameDisplay.fill(white)
        countdown_font = pygame.font.Font('freesansbold.ttf', 100)
        surface, rectangle = text_objects("3", countdown_font, red)
        rectangle.center = (display_width / 2, display_height / 2)
        gameDisplay.blit(surface, rectangle)
        pygame.display.update()
        clock.tick(FPS)

        countdown_time = pygame.time.get_ticks()
    click.play()
    while (countdown_time - start_time) < 2000 and (countdown_time - start_time) >= 1000:
        gameDisplay.fill(white)
        countdown_font = pygame.font.Font('freesansbold.ttf', 100)
        surface, rectangle = text_objects("2", countdown_font, red)
        rectangle.center = (display_width / 2, display_height / 2)
        gameDisplay.blit(surface, rectangle)
        pygame.display.update()
        clock.tick(FPS)

        countdown_time = pygame.time.get_ticks()
    click.play()
    while (countdown_time - start_time) < 3000 and (countdown_time - start_time) >= 2000:
        gameDisplay.fill(white)
        countdown_font = pygame.font.Font('freesansbold.ttf', 100)
        surface, rectangle = text_objects("1", countdown_font, red)
        rectangle.center = (display_width / 2, display_height / 2)
        gameDisplay.blit(surface, rectangle)
        pygame.display.update()
        clock.tick(FPS)

        countdown_time = pygame.time.get_ticks()
    ding.play()

def game_loop():

    # garbage can starting position
    x = (display_width * 0.5)
    y = (display_height * 0.5)

    # set window icon
    pygame.display.set_icon(icon)

    x_change = 0
    y_change = 0

    first_four_runs = True
    count = 0
    combo = 0
    previous_success = False

    treasure_toggle_on = True

    trash_on_screen = False
    treasure_on_screen = False

    trash_done_moving = True
    trash_move_count = 0
    treasure_done_moving = True
    treasure_move_count = 0

    game_score = 0

    time.sleep(0.2)

    # start title loop
    title_loop()

    countdown_loop()

    # main game loop
    while True:

        for event in pygame.event.get():

            # if x button is clicked
            if event.type == pygame.QUIT:
                # quit game
                sys.exit()
            # prints events to console (for debug)
            print(event)

            # handles key presses
            if event.type == pygame.KEYDOWN:
                if not first_four_runs:
                    if event.key == pygame.K_x:
                        treasure_toggle_on = not treasure_toggle_on
                    if event.key == pygame.K_LEFT:
                        x_change = -dist
                    elif event.key == pygame.K_RIGHT:
                        x_change = dist
                    elif event.key == pygame.K_UP:
                        y_change = -dist
                    elif event.key == pygame.K_DOWN:
                        y_change = dist

            keys = pygame.key.get_pressed()

            # if opposite keys are both pressed, cancel out movement
            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                x_change = 0
            if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
                y_change = 0

            # handles key releases
            if event.type == pygame.KEYUP:
                if not first_four_runs:
                    if event.key == pygame.K_LEFT:
                        x_change += dist
                    if event.key == pygame.K_RIGHT:
                        x_change -= dist
                    if event.key == pygame.K_UP:
                        y_change += dist
                    if event.key == pygame.K_DOWN:
                        y_change -= dist

        # modify x and y of garbage can
        x += x_change
        y += y_change

        # buffer
        if first_four_runs:
            count += 1
            if count == 4:
                first_four_runs = False

        # build screen
        gameDisplay.fill(white)
        garbage(x, y)
        gameDisplay.blit(banner, (0, 0))

        # handle scoreboard
        score_font = pygame.font.Font('freesansbold.ttf', 24)
        surface, rectangle = text_objects("%d" % game_score, score_font, black)
        gameDisplay.blit(surface, score_xy)

        # handle time clock


        # handles toggle checkbox
        if treasure_toggle_on:
            gameDisplay.blit(checkmark, checkbox_xy)
        else:
            gameDisplay.blit(unchecked, checkbox_xy)

        # spawns trash
        if not trash_on_screen:
            trash_x = random.randint(0, 575)
            trash_y = random.randint(100, 575)
            trash_choice = random.randint(1, 2)
            if not first_four_runs:
                if treasure_toggle_on:
                    while treasure_x + 25 > trash_x and treasure_x < trash_x + 25:
                        trash_x = random.randint(0, 575)
                    while treasure_y + 25 > trash_y and treasure_y < trash_y + 25:
                        trash_y = random.randint(100, 575)
                else:
                    trash_x = random.randint(0, 575)
                    trash_y = random.randint(100, 575)
            trash(trash_x, trash_y, trash_choice)
            trash_on_screen = True

        # if trash still exists, keep drawing it
        else:
            # handles trash movement
            if trash_done_moving:
                trash_move_choice = random.randint(1, 4)
                trash_done_moving = False
            if trash_move_choice == 1:
                trash_x += 2
                trash_move_count += 1
            elif trash_move_choice == 2:
                trash_x -= 2
                trash_move_count += 1
            elif trash_move_choice == 3:
                trash_y += 2
                trash_move_count += 1
            else:
                trash_y -= 2
                trash_move_count += 1

            if trash_move_count == 20:
                trash_done_moving = True
                trash_move_count = 0

            # handles trash boundaries
            if trash_x < 0:
                trash_x = 0
            elif trash_x + trash_width > display_width:
                trash_x = display_width - trash_width
            if trash_y < 100:
                trash_y = 100
            elif trash_y + trash_height > display_height:
                trash_y = display_height - trash_height
            trash(trash_x, trash_y, trash_choice)

        # if trash can and trash touch
        if trash_x + trash_width > x and trash_x < x + garbage_width \
                and trash_y + trash_height > y and trash_y < y + garbage_height:
            game_score += (score_interval + (bonus * combo))
            trash_on_screen = False
            update_score(game_score)
            if previous_success:
                combo += 1
            previous_success = True

            ding.play()

            time.sleep(0.1)

        # only if treasure is toggled on
        if treasure_toggle_on:

            # spawns treasure
            if not treasure_on_screen:
                treasure_x = random.randint(0, 575)
                treasure_y = random.randint(100, 575)
                treasure_choice = random.randint(1, 1)
                while treasure_x + 25 > trash_x and treasure_x < trash_x + 25:
                    treasure_x = random.randint(0, 575)
                while treasure_y + 25 > trash_y and treasure_y < trash_y + 25:
                    treasure_y = random.randint(100, 575)
                treasure(treasure_x, treasure_y, 1)
                treasure_on_screen = True

            # if treasure still exists, keep drawing it
            elif treasure_on_screen:

                # handles treasure movement
                if treasure_done_moving:
                    treasure_move_choice = random.randint(1, 4)
                    treasure_done_moving = False
                if treasure_move_choice == 1:
                    treasure_x += 5
                    treasure_move_count += 1
                elif treasure_move_choice == 2:
                    treasure_x -= 5
                    treasure_move_count += 1
                elif treasure_move_choice == 3:
                    treasure_y += 5
                    treasure_move_count += 1
                else:
                    treasure_y -= 5
                    treasure_move_count += 1

                # once treasure moves 20 times in one direction, switch directions
                if treasure_move_count == 20:
                    treasure_done_moving = True
                    treasure_move_count = 0

                # handles treasure boundaries
                if treasure_x < 50:
                    treasure_x = 50
                elif treasure_x + treasure_width > display_width - 50:
                    treasure_x = display_width - treasure_width - 50
                if treasure_y < 150:
                    treasure_y = 150
                elif treasure_y + treasure_height > display_height - 50:
                    treasure_y = display_height - treasure_height - 50
                treasure(treasure_x, treasure_y, treasure_choice)

            # if trash can and treasure touch
            if treasure_x + treasure_width > x and treasure_x < x + garbage_width \
                    and treasure_y + treasure_height > y and treasure_y < y + garbage_height:
                game_score -= penalty_interval
                # if score goes below 0, set it to 0
                if game_score < 0:
                    game_score = 0
                treasure_on_screen = False
                update_score(game_score)

                previous_success = False
                combo = 0

                hit.play()

                time.sleep(0.1)


        # handles border rules
        if x < 0:
            x = 0
        if x > display_width - garbage_width:
            x = display_width - garbage_width
        if y < 100:
            y = 100
        if y > display_height - garbage_height:
            y = display_height - garbage_height

        ''' Formal title
        title_text = pygame.font.Font('freesansbold.ttf', 50)
        text_surface, text_rect = text_objects("Garbage Collector", title_text, (0, 64, 0))
        text_rect.center = (display_width / 2, 50)
        gameDisplay.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.font.get_fonts()'''

        # update the screen
        pygame.display.update()
        clock.tick(FPS)

game_loop()
pygame.quit()
quit()