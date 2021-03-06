"""
Boardgame with minigames! (needs a better title)
Ben Life & Oliver Song
HooHacks 2021
Built on PyGame and Gamebox
Gamebox was built by Luther Tychonievich (tychonievich@virginia.edu)
"""

import pygame
import gamebox
import random

camera = gamebox.Camera(1000, 700)
miniGames = ["ClickingRainbow", "Maze", "AstroidDodge", "CrossStreet", "PatternRepeat"]
random.shuffle(miniGames)
miniGame = None
gamePaused = True
currentIndex = 0
num_of_rolls = 0
rollingActive = False
final_roll = None
miniGameIndex = 0

astroid_timer = 10
astroid_tick_counter = 0
astroid_player_speed = 15
astroids = [
    gamebox.from_image(0, 0, "asteroid.png"),
    gamebox.from_image(500, 0, "asteroid.png"),
    gamebox.from_image(1000, 0, "asteroid.png"),
    gamebox.from_image(0, 900, "asteroid.png"),
    gamebox.from_image(500, 900, "asteroid.png"),
    gamebox.from_image(1000, 900, "asteroid.png"),
]
astroid_player = gamebox.from_image(500, 350, "astronaut2.png")


def setAstroidSpeeds():
    for astroid in astroids:
        astroid.speedx = random.choice([random.randint(-20, -5), random.randint(5, 20)])
        astroid.speedy = random.randint(-20, 20)


setAstroidSpeeds()

repeatGameRed = gamebox.from_color(0, 0, "forestgreen", 500, 350)
repeatGameRed.topleft = (0, 0)
repeatGameGreen = gamebox.from_color(500, 0, "orange", 500, 350)
repeatGameGreen.topright = (1000, 0)
repeatGameBlue = gamebox.from_color(0, 350, "blue", 500, 350)
repeatGameBlue.bottomleft = (0, 700)
repeatGamePurple = gamebox.from_color(500, 350, "purple", 500, 350)
repeatGamePurple.bottomright = (1000, 700)
repeatGameBoxes = [repeatGameRed, repeatGameGreen, repeatGameBlue, repeatGamePurple]
repeatGameOrder = None
repeatGameLevel = 0
repeatGameIndex = 0
repeatGameUserTurn = False
repeatGameShowMarked = False
repeatGameShowAll = False
repeatGameNumUserClicks = 0


MPObjects = []

board_space_coords = []
for i in range(1, 13):
    board_space_coords.append((1, i))
for i in range(2, 5):
    board_space_coords.append((i, 12))
for i in range(12, 5, -1):
    board_space_coords.append((5, i))
board_space_coords.append((4, 6))
for i in range(6, 0, -1):
    board_space_coords.append((3, i))
for i in range(3, 8):
    board_space_coords.append((i, 1))
for i in range(1, 13):
    board_space_coords.append((7, i))
board_space_coords.append((8, 12))
board_space_coords.append((9, 12))
for i in range(12, 6, -1):
    board_space_coords.append((10, i))
board_space_coords.append((11, 7))
board_space_coords.append((12, 7))
for i in range(7, 2, -1):
    board_space_coords.append((13, i))
board_space_coords.append((14, 3))
for i in range(3, 13):
    board_space_coords.append((15, i))
board_space_coords.append((16, 12))
board_space_coords.append((17, 12))
for i in range(12, 0, -1):
    board_space_coords.append((18, i))
for i in range(18, 10, -1):
    board_space_coords.append((i, 1))

# Clicking rainbow minigame
CRDirections = gamebox.from_text(500, 50, 'Touch the boxes in the order of rainbow colors!', 40, "Black")
CRObjects = {1: [gamebox.from_image(random.randint(50, 500), random.randint(50, 300), "redgem.png"), 1, False],
             2: [gamebox.from_image(random.randint(500, 950), random.randint(300, 650), "orangegem.png"), 2, False],
             3: [gamebox.from_image(random.randint(50, 500), random.randint(50, 300), "yellowgem.png"), 3, False],
             4: [gamebox.from_image(random.randint(500, 950), random.randint(300, 650), "greengem.png"), 4, False],
             5: [gamebox.from_image(random.randint(50, 500), random.randint(50, 300), "bluegem.png"), 5, False],
             6: [gamebox.from_image(random.randint(500, 950), random.randint(300, 650), "purplegem.png"), 6, False],
             7: [gamebox.from_image(100, 100, "astronaut2.png"), "black", False]}
mouse1 = 0

# Maze Minigame
MazeObjects = [gamebox.from_color(0, 350, "gray33", 20, 700),
               gamebox.from_color(60, 200, "gray33", 100, 20),
               gamebox.from_color(200, 175, "gray33", 20, 350),
               gamebox.from_color(200, 350, "gray33", 230, 20),
               gamebox.from_color(97, 500, "gray33", 20, 300),
               gamebox.from_color(200, 600, "gray33", 20, 300),
               gamebox.from_color(303, 500, "gray33", 20, 300),
               gamebox.from_color(400, 525, "gray33", 20, 350),
               gamebox.from_color(500, 100, "gray33", 20, 350),
               gamebox.from_color(310, 100, "gray33", 200, 20),
               gamebox.from_color(310, 200, "gray33", 20, 190),
               gamebox.from_color(500, 500, "gray33", 20, 300),
               gamebox.from_color(600, 175, "gray33", 20, 350),
               gamebox.from_color(600, 360, "gray33", 200, 20),
               gamebox.from_color(700, 500, "gray33", 20, 300),
               gamebox.from_color(705, 250, "gray33", 200, 20),
               gamebox.from_color(850, 150, "gray33", 350, 20),
               gamebox.from_color(800, 525, "gray33", 20, 350),
               gamebox.from_color(900, 525, "gray33", 20, 350),
               gamebox.from_color(1000, 350, "gray33", 20, 700)]
mazePlayer = gamebox.from_image(50, 100, "astronaut2.png")
destination = gamebox.from_image(900, 50, "gearwrench1.png")

# Cross Street minigame
streetObjects = {1: [gamebox.from_image(200, random.randint(50, 700), "rocket.png"), 10],
                 2: [gamebox.from_image(300, random.randint(50, 700), "rocket.png"), 30],
                 3: [gamebox.from_image(500, random.randint(50, 700), "rocket.png"), 20],
                 4: [gamebox.from_image(600, random.randint(50, 700), "rocket.png"), 10],
                 5: [gamebox.from_image(800, random.randint(50, 700), "rocket.png"), 40],
                 6: [gamebox.from_image(900, random.randint(50, 700), "rocket.png"), 15]}
streets = [gamebox.from_image(200, 350, "road1.png"),
           gamebox.from_image(300, 350, "road1.png"),
           gamebox.from_image(500, 350, "road1.png"),
           gamebox.from_image(600, 350, "road1.png"),
           gamebox.from_image(800, 350, "road1.png"),
           gamebox.from_image(900, 350, "road1.png"),
           ]
streetPlayer = gamebox.from_image(50, 100, "astronaut2.png")
streetPlayerHealth = 200
streetPlayerDirections = gamebox.from_text(500, 600, 'Avoid the moving objects and cross to the other side!', 40,
                                           "Black")
streetPlayerHealthText = gamebox.from_text(350, 50, 'Health:', 40, "Black")
streetPlayerHealthBar = gamebox.from_color(500, 50, "blue", streetPlayerHealth, 30)
streetPlayerHealthBarMissing = gamebox.from_color(500, 50, "red", 200, 30)


def displayStartScreen():
    camera.draw(gamebox.from_image(500, 350, "backgroundGame2.png"))
    camera.draw("Press Enter to Begin", 48, "white", 500, 250)


def drawMainBoard():
    for coord in board_space_coords:
        outer_box = gamebox.from_color(coord[0] * 50 + 25, coord[1] * 50 + 25, "black", 50, 50)
        inner_box = gamebox.from_color(coord[0] * 50 + 26, coord[1] * 50 + 26, "white", 46, 46)
        camera.draw(outer_box)
        camera.draw(inner_box)


def tick(keys):
    global gamePaused, miniGame, currentIndex, num_of_rolls, rollingActive, final_roll, mouse1, streetPlayerHealth
    global astroid_timer, astroid_timer, astroids, astroid_tick_counter
    global repeatGameOrder, repeatGameLevel, repeatGameUserTurn, repeatGameIndex, repeatGameShowAll
    global repeatGameShowMarked, repeatGameNumUserClicks, miniGameIndex

    if gamePaused:
        displayStartScreen()
        if pygame.K_RETURN in keys:
            gamePaused = False
            keys.clear()
    else:
        if miniGame is None:  # main game active
            camera.draw(gamebox.from_image(500, 350, "backgroundGame1.png"))
            drawMainBoard()

            currentX = board_space_coords[currentIndex][0]
            currentY = board_space_coords[currentIndex][1]

            camera.draw(gamebox.from_image(75, 75, "green_star.png"))
            camera.draw(gamebox.from_image(11 * 50 + 25, 75, "gold_star.png"))
            camera.draw(gamebox.from_image(currentX * 50 + 25, currentY * 50 + 25, "red_circle.png"))

            camera.draw(gamebox.from_color(13 * 50, 10 * 50, "white", 100, 100))

            if final_roll is not None:
                camera.draw(str(final_roll), 48, "black", 13 * 50, 10 * 50)
                camera.draw("Click to Play a Minigame", 24, "white", 13 * 50, 11 * 50 + 25)
            else:
                camera.draw("Click to Roll", 24, "white", 13 * 50, 11 * 50 + 25)

            if rollingActive:
                if num_of_rolls < 60:
                    temp_roll = random.randint(1, 6)
                    camera.draw(str(temp_roll), 48, "black", 13 * 50, 10 * 50)
                    num_of_rolls += 1
                else:
                    final_roll = random.randint(1, 6)
                    num_of_rolls = 0
                    rollingActive = False

            if camera.mouseclick:
                if final_roll is None:
                    rollingActive = True
                else:
                    miniGameIndex += 1
                    if miniGameIndex >= len(miniGames):
                        miniGameIndex = 0
                        random.shuffle(miniGames)
                    miniGame = miniGames[miniGameIndex]
                    currentIndex += final_roll
                    final_roll = None
                    rollingActive = False
                keys.clear()

            if pygame.K_RIGHT in keys:
                currentIndex += 1
                if currentIndex >= len(board_space_coords):
                    print("Game Won!")
                    currentIndex = 0
                    gamePaused = True

        if miniGame == "ClickingRainbow":  # minigame 1
            camera.clear('grey')
            camera.draw(CRDirections)
            if pygame.K_w in keys:
                CRObjects[7][0].y -= 10
            if pygame.K_s in keys:
                CRObjects[7][0].y += 10
            if pygame.K_a in keys:
                CRObjects[7][0].x -= 10
            if pygame.K_d in keys:
                CRObjects[7][0].x += 10
            for object in CRObjects:
                if CRObjects[object][2] == False:
                    camera.draw(CRObjects[object][0])
                if CRObjects[7][0].touches(CRObjects[object][0]) and object != 7:
                    if CRObjects[object][1] == mouse1 + 1:
                        CRObjects[object][2] = True
                        mouse1 = mouse1 + 1
            if CRObjects[6][2] == True:
                miniGame = None
                for object in CRObjects:
                    CRObjects[object][2] = False
                mouse1 = 0
                keys.clear()
        if miniGame == "Maze":
            camera.clear('grey')
            if pygame.K_w in keys:
                mazePlayer.y -= 10
            if pygame.K_s in keys:
                mazePlayer.y += 10
            if pygame.K_a in keys:
                mazePlayer.x -= 10
            if pygame.K_d in keys:
                mazePlayer.x += 10
            if mazePlayer.x < 0:
                mazePlayer.x = 0
            if mazePlayer.x > 1000:
                mazePlayer.x = 1000
            if mazePlayer.y < 0:
                mazePlayer.y = 0
            if mazePlayer.y > 700:
                mazePlayer.y = 700
            for wall in MazeObjects:
                camera.draw(wall)
                if mazePlayer.touches(wall):
                    mazePlayer.speedx = 0
                    mazePlayer.speedy = 0
                    mazePlayer.move_to_stop_overlapping(wall)
            camera.draw(mazePlayer)
            camera.draw(destination)
            if mazePlayer.touches(destination):
                miniGame = None
                keys.clear()
                mazePlayer.x = 50
                mazePlayer.y = 100
        if miniGame == "CrossStreet":
            camera.clear('grey')
            if pygame.K_w in keys:
                streetPlayer.y -= 10
            if pygame.K_s in keys:
                streetPlayer.y += 10
            if pygame.K_a in keys:
                streetPlayer.x -= 10
            if pygame.K_d in keys:
                streetPlayer.x += 10
            if streetPlayer.x < 0:
                streetPlayer.x = 0
            if streetPlayer.x > 1000:
                streetPlayer.x = 1000
            if streetPlayer.y < 0:
                streetPlayer.y = 0
            if streetPlayer.y > 700:
                streetPlayer.y = 700
            if streetPlayer.x > 970:
                miniGame = None
                keys.clear()
                streetPlayerHealth = 200
                streetPlayer.x = 50
                streetPlayer.y = 100
            if streetPlayerHealth <= 0:
                streetPlayer.x = 50
                streetPlayer.y = 100
                streetPlayerHealth = 200
            for street in streets:
                camera.draw(street)
            for streetObject in streetObjects:
                streetObjects[streetObject][0].speedy = streetObjects[streetObject][1]
                streetObjects[streetObject][0].move_speed()
                if streetObjects[streetObject][0].y > 800:
                    streetObjects[streetObject][0].y = -100
                camera.draw(streetObjects[streetObject][0])
                if streetObjects[streetObject][0].touches(streetPlayer):
                    streetPlayerHealth -= 10
            streetPlayerHealthBar = gamebox.from_color(500, 50, "blue", streetPlayerHealth, 30)
            camera.draw(streetPlayerHealthBarMissing)
            camera.draw(streetPlayerHealthBar)
            camera.draw(streetPlayer)
            camera.draw(streetPlayerDirections)
            camera.draw(streetPlayerHealthText)

        if miniGame == "AstroidDodge":
            camera.clear("black")
            camera.draw(str(astroid_timer), 48, "red", 18 * 50, 50)
            astroid_tick_counter += 1

            if pygame.K_w in keys:
                astroid_player.y -= astroid_player_speed
            elif pygame.K_s in keys:
                astroid_player.y += astroid_player_speed
            elif pygame.K_a in keys:
                astroid_player.x -= astroid_player_speed
            elif pygame.K_d in keys:
                astroid_player.x += astroid_player_speed

            if astroid_player.x < 0:
                astroid_player.x = 0
            elif astroid_player.x > 1000:
                astroid_player.x = 1000
            elif astroid_player.y < 0:
                astroid_player.y = 0
            elif astroid_player.y > 700:
                astroid_player.y = 700
            camera.draw(astroid_player)
            for astroid in astroids:
                astroid.move_speed()
                if astroid.x < 0:
                    astroid.x += 1050
                elif astroid.x > 1050:
                    astroid.x -= 1050
                if astroid.y < 0:
                    astroid.y += 950
                elif astroid.y > 950:
                    astroid.y -= 950
                camera.draw(astroid)
                if astroid_player.touches(astroid):
                    astroid_timer = 10
                    camera.clear("red")
                    astroid_player.x = 500
                    astroid_player.y = 305

            if astroid_tick_counter % 28 == 0:
                astroid_timer -= 1

            if astroid_timer <= 0:
                miniGame = None
                astroid_timer = 10
                astroid_player.x = 500
                astroid_player.y = 305
                setAstroidSpeeds()

        if miniGame == "PatternRepeat":
            camera.clear("white")
            if repeatGameOrder is None:
                repeatGameOrder = []
                repeatGameNumUserClicks, repeatGameIndex, repeatGameLevel = 0, 0, 0
                for i in range(5):
                    repeatGameOrder.append(random.randint(0, 3))
                repeatGameShowAll, repeatGameShowMarked = True, True
            else:
                if repeatGameShowAll:
                    repeatGameBoxes[0].color = "forestgreen"
                    repeatGameBoxes[1].color = "orange"
                    repeatGameBoxes[2].color = "blue"
                    repeatGameBoxes[3].color = "purple"
                    for box in repeatGameBoxes:
                        camera.draw(box)
                    camera.display()
                    pygame.time.wait(1000)
                    repeatGameShowAll = False
                elif repeatGameShowMarked:
                    repeatGameBoxes[repeatGameOrder[repeatGameIndex]].color = "black"
                    for box in repeatGameBoxes:
                        camera.draw(box)
                    camera.display()
                    pygame.time.wait(1000)
                    repeatGameShowAll, repeatGameShowMarked = True, False
                    if repeatGameIndex < repeatGameLevel:
                        repeatGameIndex += 1
                        repeatGameShowAll, repeatGameShowMarked = True, True
                else:
                    if camera.mouseclick:
                        areaClicked = None
                        clickX = camera.mousex
                        clickY = camera.mousey
                        if clickX < 500 and clickY < 350:
                            areaClicked = 0
                            repeatGameBoxes[0].color = "black"
                        elif clickX > 500 and clickY < 350:
                            areaClicked = 1
                            repeatGameBoxes[1].color = "black"
                        elif clickX < 500 and clickY > 350:
                            areaClicked = 2
                            repeatGameBoxes[2].color = "black"
                        elif clickX > 500 and clickY > 350:
                            areaClicked = 3
                            repeatGameBoxes[3].color = "black"

                        for box in repeatGameBoxes:
                            camera.draw(box)
                        camera.display()
                        pygame.time.wait(1000)
                        repeatGameBoxes[0].color = "forestgreen"
                        repeatGameBoxes[1].color = "orange"
                        repeatGameBoxes[2].color = "blue"
                        repeatGameBoxes[3].color = "purple"
                        for box in repeatGameBoxes:
                            camera.draw(box)
                        camera.display()

                        if areaClicked != repeatGameOrder[repeatGameNumUserClicks]:
                            camera.clear("red")
                            camera.display()
                            pygame.time.wait(400)
                            repeatGameOrder = None
                        else:
                            repeatGameNumUserClicks += 1
                            if repeatGameNumUserClicks > repeatGameLevel:
                                repeatGameShowAll, repeatGameShowMarked = True, True
                                repeatGameLevel += 1
                                repeatGameNumUserClicks, repeatGameIndex = 0, 0
                                if repeatGameLevel >= 5:
                                    repeatGameOrder = None
                                    miniGame = None

            for box in repeatGameBoxes:
                camera.draw(box)

    camera.display()


pygame.display.set_caption("Space Race!")
icon = logo = pygame.image.load("astronaut2.png")
pygame.display.set_icon(logo)
ticks = 30
gamebox.timer_loop(ticks, tick)
