import random
import sys
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
options_move_speed = open("data/options/move_speed.txt", "r")
move_speed = int(options_move_speed.read())
options_move_speed.close()
FPS = 120

# scoreboard
score_xy = (444, 70)
checkbox_xy = (318, 68)
# sound checkbox
sound_xy = (563, 9)
# settings
score_interval = 100
bonus = 10
penalty_interval = 200
# read time limit from saved text file
options_time_limit = open("data/options/time_limit.txt", "r")
time_limit = int(options_time_limit.read())
options_time_limit.close()
sound_on = True

# colors
white = (255, 255, 255)
black = (0, 0, 0)
dark_gray = (169, 169, 169)
red = (255, 0, 0)
green = (0, 64, 0)
blue = (0, 0, 255)

# initialize pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

# initialize other stuff
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Garbage Collector', )
clock = pygame.time.Clock()

# load images
icon = pygame.image.load('images/icon.png')
title_screen = pygame.image.load('images/title_screen.png')
leaderboard_screen = pygame.image.load('images/leaderboard_screen.png')
options_screen = pygame.image.load('images/options_screen.png')
about_screen = pygame.image.load('images/about_screen.png')
pause_screen = pygame.image.load('images/pause_screen.png')
game_over_screen = pygame.image.load('images/game_over_screen.png')
trash_icon = pygame.image.load('images/trash_bag.png')
treasure_icon = pygame.image.load('images/treasure.png')
sound_on_image = pygame.image.load('images/sound_on.png')
sound_off_image = pygame.image.load('images/sound_off.png')
selected = pygame.image.load('images/selected.png')
garbage_can = pygame.image.load('images/garbagecan.png')
paper = pygame.image.load('images/paper.png')
banana = pygame.image.load('images/banana.png')
pizza = pygame.image.load('images/pizza.png')
banner = pygame.image.load('images/fixed_banner.png')
unchecked = pygame.image.load('images/unchecked.png')
checkmark = pygame.image.load('images/checkmark.png')
blue_gem = pygame.image.load('images/blue_gem.png')
red_gem = pygame.image.load('images/red_gem.png')
coin = pygame.image.load('images/coin.png')

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
    # pizza
    elif type == 3:
        gameDisplay.blit(pizza, (x, y))

# place treasure of given type at given x, y
def treasure(x, y, type):
    # blue gem
    if type == 1:
        gameDisplay.blit(blue_gem, (x, y))
    # red gem
    elif type == 2:
        gameDisplay.blit(red_gem, (x, y))
    # coin
    elif type == 3:
        gameDisplay.blit(coin, (x, y))

# place garbage can at given x, y
def garbage(x, y):
    gameDisplay.blit(garbage_can, (x, y))

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def update_score(new_score):
    score_font = pygame.font.Font('freesansbold.ttf', 24)
    surface, rectangle = text_objects("%d" % new_score, score_font, black)
    gameDisplay.blit(surface, score_xy)

# handles updating leaderboard
def update_leaderboard(score):
    leaderboard = open("data/leaderboard.txt", "r+")
    scores = leaderboard.readlines()
    inserted = False
    for x in range(0, 5):
        # compare the int values of the scores
        if score > int(scores[x]):
            # insert the score in the right place
            inserted = True
            scores.insert(x, "%s\n" % score)
            break
    # change scores back to strings with newlines
    for y in range(0, 5):
        scores[y] = "%s" % scores[y]
    # delete the lowest score (6th) and handle edge case of score 0
    if int(score) > 0 and inserted:
        scores = scores[:-1]
    # delete contents of leaderboard.txt
    leaderboard.seek(0)
    leaderboard.truncate()
    leaderboard.close()
    # append new data to leaderboard.txt
    leaderboard = open("data/leaderboard.txt", "a")
    leaderboard.writelines(scores)
    leaderboard.close()

# handles leaderboard screen
def leaderboard_loop():
    # open leaderboard file
    leaderboard = open("data/leaderboard.txt", "r")
    scores = leaderboard.readlines()
    leaderboard.close()
    score_heights = [270, 320, 370, 420, 470]

    gameDisplay.blit(leaderboard_screen, (0, 0))

    surface = [0, 0, 0, 0, 0, 0]
    rectangle = [0, 0, 0, 0, 0, 0]
    leaderboard_font = pygame.font.Font('freesansbold.ttf', 32)
    for x in range(0, 5):
        # use [:-1] to delete the newline character \n
        surface[x], rectangle[x] = text_objects("%s" % scores[x][:-1], leaderboard_font, red)
        rectangle[x].center = (display_width / 2, score_heights[x])
        gameDisplay.blit(surface[x], rectangle[x])

    while True:

        for event in pygame.event.get():
            # if x button is clicked
            if event.type == pygame.QUIT:
                # quit game
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # main menu: (148, 518) to (447, 577)
                if pygame.mouse.get_pos()[0] >= 148 and pygame.mouse.get_pos()[0] <= 447 and \
                        pygame.mouse.get_pos()[1] >= 518 and pygame.mouse.get_pos()[1] <= 577:
                    leaderboard.close()
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    game_loop(False)

        pygame.display.update()
        clock.tick(FPS)

# handles game over screen
def game_over_loop(score, num_trash, num_treasure, largest_combo):

    update_leaderboard(score)

    # display score
    game_over_font = pygame.font.Font('freesansbold.ttf', 60)
    stats_font = pygame.font.Font('freesansbold.ttf', 50)
    surface1, rectangle1 = text_objects("%d" % score, game_over_font, red)
    rectangle1.center = (display_width / 2, (display_height / 3) + 10)
    surface2, rectangle2 = text_objects("Final Score:", game_over_font, red)
    rectangle2.center = (display_width / 2, (display_height / 4) - 10)
    surface3, rectangle3 = text_objects("x %d" % num_trash, stats_font, green)
    surface4, rectangle4 = text_objects("x %d" % num_treasure, stats_font, dark_gray)
    surface5, rectangle5 = text_objects("%d" % largest_combo, stats_font, blue)
    rectangle5.center = ((display_width / 2) + 180, (display_height / 2) + 55)

    while True:
        for event in pygame.event.get():
            # if x button is clicked
            if event.type == pygame.QUIT:
                # quit game
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # play again: (150, 400) to (449, 459)
                if pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                    pygame.mouse.get_pos()[1] >=400 and pygame.mouse.get_pos()[1] <= 459:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    game_loop(True)
                # main menu: (150, 320) to (449, 379)
                elif pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                     pygame.mouse.get_pos()[1] >= 470 and pygame.mouse.get_pos()[1] <= 529:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    game_loop(False)

        gameDisplay.blit(game_over_screen, (0, 0))
        gameDisplay.blit(surface1, rectangle1)
        gameDisplay.blit(surface2, rectangle2)
        gameDisplay.blit(surface3, (185, 253))
        gameDisplay.blit(surface4, (420, 253))
        gameDisplay.blit(surface5, rectangle5)
        gameDisplay.blit(trash_icon, (100, 245))
        gameDisplay.blit(treasure_icon, (345, 250))
        pygame.display.update()
        clock.tick(FPS)

# reads option file and
# takes in unopened file
def overwrite_option(type, new_val):
    # if time limit option
    if type == 1:
        file = open("data/options/time_limit.txt", "w")
    # if move speed option
    elif type == 2:
        file = open("data/options/move_speed.txt", "w")
    file.seek(0)
    file.write("%s" % new_val)
    file.close()

# reads the option file
def read_option(type):
    # if time limit option
    if type == 1:
        file = open("data/options/time_limit.txt", "r")
    # if move speed option
    elif type == 2:
        file = open("data/options/move_speed.txt", "r")
    old_val = int(file.readlines()[0])
    file.close()
    return old_val

# handles options screen
def option_loop():

    gameDisplay.blit(options_screen, (0, 0))
    choice1 = read_option(1)
    choice2 = read_option(2)

    while True:
        for event in pygame.event.get():
            # if x button is clicked
            if event.type == pygame.QUIT:
                # quit game
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # main menu: (148, 518) to (447, 577)
                if pygame.mouse.get_pos()[0] >= 148 and pygame.mouse.get_pos()[0] <= 447 and \
                                pygame.mouse.get_pos()[1] >= 518 and pygame.mouse.get_pos()[1] <= 577:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    title_loop()
                # time limit set to 10 seconds: (90, 300) to (209, 329)
                if pygame.mouse.get_pos()[0] >= 90 and pygame.mouse.get_pos()[0] <= 209 and \
                                pygame.mouse.get_pos()[1] >= 300 and pygame.mouse.get_pos()[1] <= 329:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    overwrite_option(1, 10)
                    choice1 = 10

                # time limit set to 30 seconds: (240, 300) to (359, 329)
                if pygame.mouse.get_pos()[0] >= 240 and pygame.mouse.get_pos()[0] <= 359 and \
                                pygame.mouse.get_pos()[1] >= 300 and pygame.mouse.get_pos()[1] <= 329:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    overwrite_option(1, 30)
                    choice1 = 30

                # time limit set to 30 seconds: (390, 300) to (509, 329)
                if pygame.mouse.get_pos()[0] >= 390 and pygame.mouse.get_pos()[0] <= 509 and \
                                pygame.mouse.get_pos()[1] >= 300 and pygame.mouse.get_pos()[1] <= 329:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    overwrite_option(1, 60)
                    choice1 = 60
                # move speed set to slow (5): (90, 380) to (209, 409)
                if pygame.mouse.get_pos()[0] >= 90 and pygame.mouse.get_pos()[0] <= 209 and \
                                pygame.mouse.get_pos()[1] >= 380 and pygame.mouse.get_pos()[1] <= 409:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    overwrite_option(2, 5)
                    choice2 = 5

                # move speed set to medium (10): (240, 380) to (359, 409)
                if pygame.mouse.get_pos()[0] >= 240 and pygame.mouse.get_pos()[0] <= 359 and \
                                pygame.mouse.get_pos()[1] >= 380 and pygame.mouse.get_pos()[1] <= 409:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    overwrite_option(2, 10)
                    choice2 = 10

                # move speed set to fast: (390, 380) to (509, 409)
                if pygame.mouse.get_pos()[0] >= 390 and pygame.mouse.get_pos()[0] <= 509 and \
                                pygame.mouse.get_pos()[1] >= 380 and pygame.mouse.get_pos()[1] <= 409:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    overwrite_option(2, 15)
                    choice2 = 15

        gameDisplay.blit(options_screen, (0, 0))
        # display properly selected cursor for time limit
        if choice1 == 10:
            gameDisplay.blit(selected, (90, 300))
        elif choice1 == 30:
            gameDisplay.blit(selected, (240, 300))
        elif choice1 == 60:
            gameDisplay.blit(selected, (390, 300))
        # display properly selected cursor for move speed
        if choice2 == 5:
            gameDisplay.blit(selected, (90, 380))
        elif choice2 == 10:
            gameDisplay.blit(selected, (240, 380))
        elif choice2 == 15:
            gameDisplay.blit(selected, (390, 380))

        pygame.display.update()
        clock.tick(FPS)

# handles about screen
def about_loop():
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
                    if sound_on:
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
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    game_loop(True)
                # leaderboard: (150, 320) to (449, 379)
                elif pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                    pygame.mouse.get_pos()[1] >= 320 and pygame.mouse.get_pos()[1] <= 379:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    leaderboard_loop()

                # options: (150, 390) to (449, 449)
                elif pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                    pygame.mouse.get_pos()[1] >= 390 and pygame.mouse.get_pos()[1] <= 449:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    option_loop()

                # about: (150, 460) to (449, 519)
                elif pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[0] <= 449 and \
                     pygame.mouse.get_pos()[1] >= 460 and pygame.mouse.get_pos()[1] <= 519:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    about_loop()

        gameDisplay.blit(title_screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

# handles countdown before game start
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
    if sound_on:
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
    if sound_on:
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
    if sound_on:
        ding.play()

# handles pause screen
def pause_loop():
    pause_count = 0
    while True:

        for event in pygame.event.get():
            # if x button is clicked
            if event.type == pygame.QUIT:
                # quit game
                sys.exit()
            # if pause is called again, leave pause menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return pause_count
            # if resume game button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # resume: (100, 310) to (499, 359)
                if pygame.mouse.get_pos()[0] >= 100 and pygame.mouse.get_pos()[0] <= 499 and \
                    pygame.mouse.get_pos()[1] >= 310 and pygame.mouse.get_pos()[1] <= 359:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    return pause_count
                # restart: (100, 380) to (499, 429)
                if pygame.mouse.get_pos()[0] >= 100 and pygame.mouse.get_pos()[0] <= 499 and \
                    pygame.mouse.get_pos()[1] >= 380 and pygame.mouse.get_pos()[1] <= 429:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    game_loop(True)
                # quit to main menu: (100, 450) to (499, 499)
                if pygame.mouse.get_pos()[0] >= 100 and pygame.mouse.get_pos()[0] <= 499 and \
                    pygame.mouse.get_pos()[1] >= 450 and pygame.mouse.get_pos()[1] <= 499:
                    if sound_on:
                        click.play()
                    time.sleep(0.2)
                    game_loop(False)
        gameDisplay.blit(pause_screen, (50, 50))
        pygame.display.update()
        clock.tick(FPS)
        # handles the delay in game_loop() since pausing still runs the clock
        pause_count += clock.get_time()


def game_loop(skip_title):

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
    game_sound_on = True

    trash_on_screen = False
    treasure_on_screen = False

    trash_done_moving = True
    treasure_done_moving = True
    trash_move_count = 0
    treasure_move_count = 0

    current_time = 0

    game_score = 0
    num_trash = 0
    num_treasure = 0
    largest_combo = 0

    time.sleep(0.2)

    if not skip_title:
        # start title loop
        title_loop()

    countdown_loop()

    # read options and apply them
    time_limit = read_option(1)
    move_speed = read_option(2)

    start_time = pygame.time.get_ticks()
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
                    if event.key == pygame.K_ESCAPE:
                        start_time += pause_loop()
                    if event.key == pygame.K_s:
                        game_sound_on = not game_sound_on
                    if event.key == pygame.K_LEFT:
                        x_change = -move_speed
                    elif event.key == pygame.K_RIGHT:
                        x_change = move_speed
                    elif event.key == pygame.K_UP:
                        y_change = -move_speed
                    elif event.key == pygame.K_DOWN:
                        y_change = move_speed

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
                        x_change += move_speed
                    if event.key == pygame.K_RIGHT:
                        x_change -= move_speed
                    if event.key == pygame.K_UP:
                        y_change += move_speed
                    if event.key == pygame.K_DOWN:
                        y_change -= move_speed

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

        # handles time clock
        if (current_time - start_time) < time_limit * 1000:
            current_time = pygame.time.get_ticks()
            time_limit_font = pygame.font.Font('freesansbold.ttf', 60)
            time_elapsed = math.floor((current_time - start_time) / 1000)
            surface, rectangle = text_objects("%d" % (time_limit - time_elapsed), time_limit_font, red)
            rectangle.center = (display_width / 2, 36)
            gameDisplay.blit(surface, rectangle)

        else:
            game_over_loop(game_score, num_trash, num_treasure, largest_combo)


        # handles sound toggle
        if game_sound_on:
            gameDisplay.blit(sound_on_image, sound_xy)
        else:
            gameDisplay.blit(sound_off_image, sound_xy)

        # handles toggle checkbox
        if treasure_toggle_on:
            gameDisplay.blit(checkmark, checkbox_xy)
        else:
            gameDisplay.blit(unchecked, checkbox_xy)

        # spawns trash
        if not trash_on_screen:
            trash_x = random.randint(0, 575)
            trash_y = random.randint(100, 575)
            trash_choice = random.randint(1, 3)
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

            # update stats
            num_trash += 1
            if previous_success:
                combo += 1
            if combo > largest_combo:
                largest_combo = combo
            previous_success = True

            if game_sound_on:
                ding.play()

        # only if treasure is toggled on
        if treasure_toggle_on:

            # spawns treasure
            if not treasure_on_screen:
                treasure_x = random.randint(0, 575)
                treasure_y = random.randint(100, 575)
                treasure_choice = random.randint(1, 3)
                while treasure_x + 25 > trash_x and treasure_x < trash_x + 25:
                    treasure_x = random.randint(0, 575)
                while treasure_y + 25 > trash_y and treasure_y < trash_y + 25:
                    treasure_y = random.randint(100, 575)
                treasure(treasure_x, treasure_y, treasure_choice)
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

                # update stats
                num_treasure += 1
                previous_success = False
                combo = 0

                if game_sound_on:
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

game_loop(False)
pygame.quit()
quit()