# Importing the things we use
import pygame
from pygame import mixer
import random
import math

pygame.init()  # Initializing pygame

screen = pygame.display.set_mode((1280, 720))  # Creating the game window

# Adding the name of the window & the logo of the game
pygame.display.set_caption('The Purrfection challenge')
icon = pygame.image.load("Cat/cat_move_right.png")
pygame.display.set_icon(icon)

# Creating the image for the bullet, the background and the cat
bullet_img = pygame.image.load("bulletImg.png")
background = pygame.image.load("background.png")

# Initialising variables
cat_sit = pygame.image.load("Cat/cat_sit.png")
cat_move_right = pygame.image.load("Cat/cat_move_right.png")
cat_move_left = pygame.image.load("Cat/cat_move_left.png")
cat_shoot_right = pygame.image.load("Cat/cat_shoot_right.png")
cat_shoot_left = pygame.image.load("Cat/cat_shoot_left.png")
cat_img = cat_sit
cat_offset = 32
cat_X, cat_Y = 608, 600
cat_change_X, cat_change_Y = 0, 0
cat_speed = 2.0

bullet_state = 'ready'  # bullet state created to show bullet only when mouse pressed
bullet_offset = 25
bullet_X, bullet_Y = cat_X + (cat_offset - bullet_offset), cat_Y + (cat_offset - bullet_offset)
bullet_speed_X, bullet_speed_Y = 0, 0

high_score_file = open("high_score.txt", "r+")

if high_score_file.readline() == "":
    high_score_file.write("0"), high_score_file.close()

high_score_file = open("high_score.txt", "r+")
high_score = int(high_score_file.readline())
high_score_file.close()

score = 0
shots_fired, shot_accuracy = 0, 0
lives_left = 7

num_of_dogs = 4
dog_speed = 2.25
dog_offset = 32
dog_img = []  # [] means empty array/list
dog_X = []
dog_Y = []
dog_shot = False

for i in range(num_of_dogs):
    dog_img.append(pygame.image.load("dog.png"))
    dog_X.append(random.randint(0, 1280)), dog_Y.append(random.randint(0, 200))


def reset_variables():  # Procedure to reset all changing variables
    global new_high_score, game_over, num_of_dogs, dog_speed, shot_accuracy, shots_fired, score
    global lives_left, cat_X, cat_Y, cat_speed, bullet_X, bullet_Y, cat_X, cat_Y, bullet_state
    new_high_score, game_over = False, False

    if num_of_dogs > 4:
        for n in range(4, num_of_dogs):
            dog_X.pop(4), dog_Y.pop(4), dog_img.pop(4)
    dog_speed = 2.25
    num_of_dogs = 4
    for index in range(num_of_dogs):
        dog_X[index], dog_Y[index] = random.randint(0, 1280), random.randint(0, 200)

    shot_accuracy, shots_fired, score = 0, 0, 0
    lives_left = 7

    cat_X, cat_Y = 608, 600
    cat_speed = 2.0
    bullet_X, bullet_Y = cat_X + (cat_offset - bullet_offset), cat_Y + (cat_offset - bullet_offset)
    bullet_state = "ready"


# Adding the background music for the first song
song_id = random.randint(1, 5)  # Generates random song between 1 and 5 inclusive
mixer.music.load("bg_songs/" + "bg_song_" + str(song_id) + ".mp3")
mixer.music.play(fade_ms=1000), mixer.music.set_volume(0.1)
last_song_id = song_id


def play_new_song():  # Procedure to generate a new song
    global song_id, last_song_id
    if not mixer.music.get_busy():  # Checks if the last song is not being played
        mixer.music.unload()

        song_id = random.randint(1, 5)
        while song_id == last_song_id:
            song_id = random.randint(1, 5)

        mixer.music.load("bg_songs/" + "bg_song_" + str(song_id) + ".mp3")
        mixer.music.play(fade_ms=1000), mixer.music.set_volume(0.1)
        last_song_id = song_id


def play_sound_effect(sound_name, volume):  # procedure to play sound effects
    sound_effect = mixer.Sound("sound_effects/" + sound_name + "_sound_effect.mp3")
    sound_effect.play(0)
    sound_effect.set_volume(volume)


def increase_difficulty():  # Procedure to make the game harder
    global num_of_dogs, dog_img, dog_X, dog_Y, dog_speed, cat_speed
    num_of_dogs += 1
    dog_img.append(pygame.image.load("dog.png"))
    dog_X.append(random.randint(0, 1280))
    dog_Y.append(random.randint(0, 200))
    dog_speed += 0.2
    cat_speed += 0.25


font_small, font_big = pygame.font.Font("Arcade.ttf", 50), pygame.font.Font("Arcade.ttf", 80)


def display_text(x, y, InString, size):  # Procedure to display the text on screen
    if size == "small":
        OutString = font_small.render(InString, True, (255, 255, 0))
        screen.blit(OutString, (x, y))
    elif size == "big":
        OutString = font_big.render(InString, True, (255, 255, 0))
        text_width = OutString.get_width()
        screen.blit(OutString, (((1280 - text_width) // 2), y))  # // means DIV


def istouch(x1, y1, x2, y2, trigger_dist):  # Function to find distance between 2 objects using distance formula
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < trigger_dist:
        return True
    else:
        return False


def get_angle(fixed_element_X, fixed_element_Y, moving_element_X, moving_element_Y):
    # Function to calculate angle between 2 elements

    if abs(moving_element_X - fixed_element_X) == 0:  # to avoid run-time error caused by a division by 0
        if moving_element_Y < fixed_element_Y:  # AAAHAHAGAGGAHAHAGGAHAHAGGA
            angle = math.pi / 2
        else:
            angle = 3 * math.pi / 2
    else:
        angle = math.atan(abs(moving_element_Y - fixed_element_Y) / abs(moving_element_X - fixed_element_X))
        if moving_element_X < fixed_element_X and moving_element_Y < fixed_element_Y:
            angle = math.pi - angle
        elif moving_element_X < fixed_element_X and moving_element_Y > fixed_element_Y:
            angle = math.pi + angle
        elif moving_element_X > fixed_element_X and moving_element_Y > fixed_element_Y:
            angle = 2 * math.pi - angle
    return angle


def fire_bullet(x, y):  # Procedure to display bullet image only when mouse pressed
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x, y))


def display_cat(x, y):  # Procedure to display cat image
    screen.blit(cat_img, (x, y))


def display_dog(x, y, j):  # Procedure to display images of the dogs
    screen.blit(dog_img[j], (x, y))


def make_button(name, buttonX, buttonY):
    globals()[name + f"_button_up"] = pygame.image.load("buttons/" + name + "_button_up.png")
    globals()[name + f"_button_down"] = pygame.image.load("buttons/" + name + "_button_down.png")
    globals()[name + f"_button"] = globals()[name + f"_button_up"]
    globals()[name + f"_buttonX"] = buttonX
    globals()[name + f"_buttonY"] = buttonY
    globals()[name] = False


make_button("Start", 390, 200)
make_button("Next_song", 390, 300)
make_button("Meow", 390, 400)
make_button("Leave", 390, 500)


def find_button(x, y, game_started):
    global Start_buttonX, Start_buttonY, Leave_buttonX, Leave_buttonY, Next_song_buttonX, Next_song_buttonY, \
        Meow_buttonX, Meow_buttonY, Resume_buttonX, Resume_buttonY
    if game_started:
        if x in range(Next_song_buttonX, Next_song_buttonX + 500) and y in range(Next_song_buttonY,
                                                                                 Next_song_buttonY + 75):
            return "next"
        if x in range(Resume_buttonX, Resume_buttonX + 500) and y in range(Resume_buttonY, Resume_buttonY + 75):
            return "resume"
        if x in range(Restart_buttonX, Restart_buttonX + 500) and y in range(Restart_buttonY, Restart_buttonY + 75):
            return "restart"
        if x in range(Meow_buttonX, Meow_buttonX + 500) and y in range(Meow_buttonY, Meow_buttonY + 75):
            return "meow"
    else:
        if x in range(Start_buttonX, Start_buttonX + 500) and y in range(Start_buttonY, Start_buttonY + 75):
            return "start"
        if mouseX in range(Leave_buttonX, Leave_buttonX + 500) and mouseY in range(Leave_buttonY,
                                                                                   Leave_buttonY + 75):
            return "leave"
        if x in range(Next_song_buttonX, Next_song_buttonX + 500) and y in range(Next_song_buttonY,
                                                                                 Next_song_buttonY + 75):
            return "next"
        if x in range(Meow_buttonX, Meow_buttonX + 500) and y in range(Meow_buttonY, Meow_buttonY + 75):
            return "meow"


before_game = True
clock = pygame.time.Clock()
count = 0
in_game = False

dog_X[1], dog_Y[1] = 1280, 650
cat_X, cat_Y = 0, 650
bullet_X, bullet_Y = cat_X + 7, cat_Y + 7
bullet_speed_X = 6
dog_speed_X = 2
while before_game:
    clock.tick(120)

    play_new_song()

    screen.blit(background, (0, 0))

    screen.blit(Start_button, (Start_buttonX, Start_buttonY))
    screen.blit(Leave_button, (Leave_buttonX, Leave_buttonY))
    screen.blit(Next_song_button, (Next_song_buttonX, Next_song_buttonY))
    screen.blit(Meow_button, (Meow_buttonX, Meow_buttonY))

    display_cat(cat_X, cat_Y)
    display_dog(dog_X[1], dog_Y[1], 1)

    cat_img = cat_sit

    fire_bullet(bullet_X, bullet_Y)
    bullet_X += bullet_speed_X
    dog_X[1] -= dog_speed_X
    if bullet_X >= dog_X[1]:
        bullet_X = cat_X + 7
        dog_X[1] = 1300
        cat_X = 0
        cat_img = cat_shoot_right
        bullet_speed_X = random.uniform(6, 8)
        dog_speed_X = random.uniform(4, 8)

    if Start:
        Start_button = Start_button_up

        count += 1
        if count == 20:
            reset_variables()

            before_game = False
            in_game = True
    if Leave:
        Leave_button = Leave_button_up
        count += 1
        if count == 20:
            exit()
    if Next_song:
        Next_song_button = Next_song_button_up
        mixer.music.stop()
        Next_song = False
    if Meow:
        Meow_button = Meow_button_up
        play_sound_effect("meow", 0.1)
        Meow = False

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            button = find_button(mouseX, mouseY, False)
            if button == "start":
                Start_button = Start_button_down
                play_sound_effect("Click", 1)
            if button == "leave":
                Leave_button = Leave_button_down
            if button == "next":
                Next_song_button = Next_song_button_down
                play_sound_effect("Click", 1)
            if button == "meow":
                Meow_button = Meow_button_down
        if event.type == pygame.MOUSEBUTTONUP:
            if button == "start":
                Start = True
            if button == "leave":
                Leave = True
            if button == "next":
                Next_song = True
            if button == "meow":
                Meow = True
        if event.type == pygame.QUIT:
            exit()

    display_text(None, 60, "Purrfection Challenge", "big")
    pygame.display.update()

# Initialization of important boolean variables
mouse_down, game_over, new_high_score, pause = False, False, False, False

clock = pygame.time.Clock()  # to control TPS

Next_song_buttonX = 390
Next_song_buttonY = 600

make_button("Resume", 390, 300)
make_button("Restart", 390, 500)

count = 0

while in_game:  # everything inside this loop keeps repeating

    clock.tick(120)
    screen.blit(background, (0, 0))
    display_cat(cat_X, cat_Y)
    play_new_song()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Closes the loop if user presses X in top right
            in_game = False

        if event.type == pygame.MOUSEBUTTONDOWN and bullet_state != 'fire' and not pause:
            if event.button == 1 or event.button == 3:
                shots_fired += 1
                fire_bullet(bullet_X, bullet_Y)
                play_sound_effect("shot_fired", 0.2)

                # Special thanks to 🎉 FLOWERY SUBWAY 🎉 for the help in this part
                mouseX, mouseY = event.pos
                theta = get_angle(cat_X + (cat_offset - bullet_offset), cat_Y + (cat_offset - bullet_offset),
                                  mouseX - bullet_offset, mouseY - bullet_offset)
                bullet_speed_Y = 40 * math.sin(theta) * -1
                bullet_speed_X = 40 * math.cos(theta)
        if event.type == pygame.KEYDOWN:
            if not pause:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    cat_change_X = -cat_speed
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    cat_change_X = cat_speed
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    cat_change_Y = cat_speed
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    cat_change_Y = -cat_speed

            if event.key == pygame.K_ESCAPE and not game_over:
                pause = not pause

        if event.type == pygame.KEYUP:
            # Stops the cat moving after user removes hand from keyboard

            if (event.key == pygame.K_a or event.key == pygame.K_LEFT or
                    event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                cat_change_X = 0
            if (event.key == pygame.K_s or event.key == pygame.K_DOWN or
                    event.key == pygame.K_w or event.key == pygame.K_UP):
                cat_change_Y = 0

            if event.key == pygame.K_SPACE and game_over:
                pygame.mixer.stop()
                reset_variables()  # Resetting variables when cat loses or when player restarts

    for i in range(num_of_dogs):
        cat_hurt = istouch(cat_X + cat_offset, cat_Y + cat_offset,
                           dog_X[i] + dog_offset, dog_Y[i] + dog_offset, 50)

        if cat_hurt:
            lives_left = lives_left - 1
            if lives_left == 0:
                game_over = True
                play_sound_effect("game_over", 0.35)

                if shots_fired != 0:
                    shot_accuracy = (score / shots_fired) * 100
                if score > high_score:
                    new_high_score = True
                    high_score = score
                    high_score_file = open("high_score.txt", "w+")
                    high_score_file.write(str(high_score)), high_score_file.close()

                # kicking the cat, the dog and the bullet out of the screen boundaries when cat loses
                bullet_X, bullet_Y = -10000, -10000
                cat_X, cat_Y = -10000, -10000
                dog_speed = 1500
            elif lives_left > 0:
                play_sound_effect("cat_hurt", 0.45)
                dog_X[i], dog_Y[i] = random.randint(0, 1280), random.randint(0, 200)

        if bullet_state == "fire":
            dog_shot = istouch(bullet_X + bullet_offset, bullet_Y + bullet_offset,
                               dog_X[i] + dog_offset, dog_Y[i] + dog_offset, 45)
        if dog_shot and not game_over:
            dog_shot = False

            play_sound_effect("dog_hit", 0.07)

            bullet_state = "ready"
            bullet_X, bullet_Y = cat_X + (cat_offset - bullet_offset), cat_Y + (cat_offset - bullet_offset)

            dog_X[i], dog_Y[i] = random.randint(0, 1280), random.randint(0, 200)

            score += 1
            if score % 20 == 0:
                increase_difficulty()

        if not pause:
            alpha = get_angle(cat_X, cat_Y, dog_X[i], dog_Y[i])
            dog_speed_Y = dog_speed * math.sin(alpha)
            dog_speed_X = dog_speed * math.cos(alpha) * -1
        else:
            dog_speed_X, dog_speed_Y = 0, 0

        dog_X[i] += dog_speed_X
        dog_Y[i] += dog_speed_Y
        display_dog(dog_X[i], dog_Y[i], i)

    if bullet_state == "fire":
        fire_bullet(bullet_X, bullet_Y)

        if mouseX > cat_X:  # Changes the image of cat to the cat shooting
            cat_img = cat_shoot_right
        else:
            cat_img = cat_shoot_left
    else:
        bullet_X, bullet_Y = cat_X + (cat_offset - bullet_offset), cat_Y + (cat_offset - bullet_offset)
        cat_img = cat_sit  # Returns the image back to the original

    if bullet_Y < 0 or bullet_Y > 720 or bullet_X < 0 or bullet_X > 1280:  # Checks if the bullet left the screen
        bullet_state = "ready"

    if (cat_change_X != 0 or cat_change_Y != 0) and (bullet_state != "fire"):
        if cat_change_X < 0:
            cat_img = cat_move_right
        else:
            cat_img = cat_move_left

    if pause:
        display_text(None, 60, "Game Paused", "big")

        screen.blit(Next_song_button, (Next_song_buttonX, Next_song_buttonY))
        screen.blit(Resume_button, (Resume_buttonX, Resume_buttonY))
        screen.blit(Restart_button, (Restart_buttonX, Restart_buttonY))
        screen.blit(Meow_button, (Meow_buttonX, Meow_buttonY))

        if not mouse_down:
            if Resume:
                Resume_button = Resume_button_up
                count += 1
                if count == 1:
                    play_sound_effect("Click", 1)
                if count == 20:
                    pause = False
                    Resume = False
                    count = 0
            if Meow:
                Meow_button = Meow_button_up
                play_sound_effect("meow", 0.1)
                Meow = False
            if Restart:
                Restart_button = Restart_button_up
                count += 1
                if count == 1:
                    play_sound_effect("Click", 1)
                if count == 20:
                    Restart = False
                    pause = False
                    count = 0
                    reset_variables()
            if Next_song:
                Next_song_button = Next_song_button_up
                mixer.music.stop()
                Next_song = False
                play_sound_effect("Click", 1)
        if pygame.mouse.get_pressed()[0]:
            mouse_down = True
            mouseX, mouseY = pygame.mouse.get_pos()
            button = find_button(mouseX, mouseY, True)
            if button == "resume":
                Resume_button = Resume_button_down
                Resume = True
            if button == "meow":
                Meow_button = Meow_button_down
                Meow = True
            if button == "restart":
                Restart_button = Restart_button_down
                Restart = True
            if button == "next":
                Next_song_button = Next_song_button_down
                Next_song = True
        else:
            mouse_down = False
    elif not game_over:
        display_text(10, 680, "Lives left : " + str(lives_left), "small")
        display_text(10, 10, "Score : " + str(score), "small")
        display_text(10, 45, "High Score : " + str(high_score), "small")

        cat_X += cat_change_X
        cat_Y += cat_change_Y

        bullet_X += bullet_speed_X
        bullet_Y += bullet_speed_Y

        # Keeping the cat inside boundaries of screen
        if cat_X <= 0:
            cat_X = 0
        elif cat_X >= 1216:  # The reason 1216 is used instead of 1280 is to account for the size of image
            cat_X = 1216
        if cat_Y <= 0:
            cat_Y = 0
        elif cat_Y >= 656:
            cat_Y = 656

        if not pygame.mouse.get_focused():
            pause = True
    else:
        display_text(None, 60, "Game Over", "big")
        display_text(None, 550, "Press the Spacebar to play again", "big")
        display_text(None, 170, "Score : " + str(score), "big")
        display_text(None, 270, "Accuracy : " + str(int(shot_accuracy)) + "%", "big")
        if new_high_score:
            display_text(None, 400, "NEW HIGH SCORE!!!", "big")

    pygame.display.update()  # Updating the screen so changes occur

# YENJOY
