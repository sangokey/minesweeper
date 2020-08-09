# Author: Sang Ok Suh
# Date: 08/08/2020
# Description: Minesweeper game with User Interface

# Followed these pygame tutorials for reference:
# http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
# https://www.youtube.com/watch?v=zMN9kRLD1DA&list=PLQVvvaa0QuDdLkP8MrOXLe_rKuf6r80KO&index=6

import pygame
import random
import pygame.font
import math
import sys

# --------------------IMAGES---------------------------------
# Img for bombs, flag
bomb_img = pygame.image.load('images/bomb.png')
bomb_img = pygame.transform.scale(bomb_img, (17, 17))

bombx_img = pygame.image.load("images/bombx.png")
bombx_img = pygame.transform.scale(bombx_img, (17, 17))

flag_img = pygame.image.load('images/flag.png')
flag_img = pygame.transform.scale(flag_img, (20, 20))

thumbs_up = pygame.image.load('images/thumbsup.png')
thumbs_up = pygame.transform.scale(thumbs_up, (27, 27))

thumbs_down = pygame.image.load('images/thumbsdown.png')
thumbs_down = pygame.transform.scale(thumbs_down, (27, 27))

crown = pygame.image.load('images/crown.png')
crown = pygame.transform.scale(crown, (27, 27))
# ---------------------------------------------------------


# -----------COLORS------------
white = (255, 255, 255)
gray = (211, 211, 211)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (65, 105, 225)
brightred = (240, 128, 128)
brightblue = (135, 206, 250)
gray = (192, 192, 192)
green = (0, 255, 0)
light_green = (173,255,47)
# ------------------------------


# -----------Grid Dimensions----------------
width = 20
height = 20
margin = 5
# -------------------------------------------


# ----------Pygame Initialization----------------------
# Initialize pygame
pygame.init()

# Title of Game
pygame.display.set_caption("Minesweeper by Sang Ok Suh")

# Size of Screen
display_width = 600
display_height = 500
size = (display_width, display_height)
screen = pygame.display.set_mode(size)

# Manage Screen Updates
clock = pygame.time.Clock()
# ------------------------------------------------------

# -----------FONTS---------------
largeText = pygame.font.SysFont('Arial.ttf', 80)
choiceText = pygame.font.SysFont('Arial.ttf', 30)
descriptionText = pygame.font.SysFont('Arial.ttf', 18)
font = pygame.font.SysFont('Arial', 15, True)
# -------------------------------


def screen_size(page):

    if page == "Intro":
        display_width = 600
        display_height = 500

    elif page == "Easy":
        display_width = 232
        display_height = 330

    elif page == "Hard":
        display_width = 410
        display_height = 500

    size = (display_width, display_height)
    screen = pygame.display.set_mode(size)


# Intro Button Function
def button(msg, x, y, w, h, i, a, fontsize, xcorrection, ycorrection):

    difficultyText = pygame.font.SysFont('Arial.ttf', fontsize)

    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    if (x <= mouse[0] <= x + w) and (y <= mouse[1] <= y + h):
        pygame.draw.rect(screen, a, [x, y, w, h])
        if click[0] == 1:

            if msg == "Easy" or msg == "Hard":
                start_game(msg)

            elif msg == "Menu":
                screen_size("Intro")
                game_intro()

            elif msg == "Exit":
                sys.exit()

    else:
        pygame.draw.rect(screen, i, [x, y, w, h])

    screen.blit(difficultyText.render(msg, True, white), (x + xcorrection, y + ycorrection))


# Intro Screen
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(white)
        screen.blit(largeText.render("Minesweeper", True, black), (130, 50))

        screen.blit(choiceText.render("Choose a difficulty", True, black), (210, 260))

        button("Easy", 100, 300, 150, 50, blue, brightblue, 50, 35, 10)
        button("Hard", 350, 300, 150, 50, red, brightred, 50, 35, 10)

        screen.blit(descriptionText.render("9x9, 10 bombs", True, black), (135, 355))
        screen.blit(descriptionText.render("16x16, 40 bombs", True, black), (380, 355))

        pygame.display.update()
        clock.tick(60)


# Grid Creation
def create_grid(difficulty):

    if difficulty == "Easy":
        grid_coordinates = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        bomb = 10
    elif difficulty == "Hard":
        grid_coordinates = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        bomb = 40

    grid = []
    for row in range(len(grid_coordinates)):
        grid.append([])
        for column in range(len(grid_coordinates)):
            grid[row].append(0)

    while bomb != 0:
        bomb_x = random.randint(0,len(grid_coordinates)-1)
        bomb_y = random.randint(0, len(grid_coordinates)-1)

        if grid[bomb_x][bomb_y] != "b":
            grid[bomb_x][bomb_y] = "b"
            bomb -= 1

    return grid


# Getting the coordinates of all adjacent cells
def get_adjacent_cells(i, j):

    adjacent_indices = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i + 1, j),
                        (i + 1, j + 1)]

    return adjacent_indices


# Counter for the number of adjacent cell with bombs
def bomb_counter(x, y, grid, grid_coordinates):

    # Bomb Counter set to 0
    bomb_cell = 0

    # Get All Adjacent Cells
    adjacent_cells = get_adjacent_cells(x, y)

    # Loop through all 8 adjacent cells
    for i in range(8):

        # Store row and col
        adjacent_row = adjacent_cells[i][0]
        adjacent_col = adjacent_cells[i][1]

        # If row and column are within grid
        if adjacent_row in grid_coordinates and adjacent_col in grid_coordinates:

            # If bomb is in adjacent cell
            if grid[adjacent_row][adjacent_col] == "b" or grid[adjacent_row][adjacent_col] == "bf":

                # Increment bomb counter
                bomb_cell += 1

    # return the number of adjacent cells with bombs
    return bomb_cell


# Function that searches adjacent cells when an empty cell without bomb is clicked.
# Also assigns empty (no adjacent bomb cells) or # of adjacent bomb cells.
def assign_empty_cell_value(row, col, grid, grid_coordinates):

    bomb_count = bomb_counter(row, col, grid, grid_coordinates)

    # If there are adjacent bomb cells
    if bomb_count != 0:

        # Assign bomb_count value to cell location
        grid[row][col] = bomb_count

    # If no adjacent bomb cells
    if bomb_count == 0:

        # Assign value "e" for empty
        grid[row][col] = "e"

        # Get adjacent cells for "e" cells
        empty_adjacent = get_adjacent_cells(row, col)

        # Loop through adjacent cells
        for i in range(8):

            # Store row and col
            adjacent_row = empty_adjacent[i][0]
            adjacent_col = empty_adjacent[i][1]

            # If row and column are within grid and cell value is not-clicked
            if (adjacent_row in grid_coordinates) and (adjacent_col in grid_coordinates):
                if grid[adjacent_row][adjacent_col] == 0 or grid[adjacent_row][adjacent_col] == "f":
                    assign_empty_cell_value(adjacent_row, adjacent_col, grid, grid_coordinates)


# Start game function
def start_game(difficulty):

    extra_xmargin = 0
    extra_ymargin = 0

    # Set new screen_size depending on difficulty
    screen_size(difficulty)

    # Status
    status = "current"

    # Create Grid Based on Difficulty
    grid = create_grid(difficulty)

    # Flags based on difficulty
    if difficulty == "Easy":
        flags = 10
        grid_coordinates = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        extra_margin = 0

    elif difficulty == "Hard":
        flags = 40
        grid_coordinates = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        extra_xmargin = 100
        extra_ymargin = 170

    # Timer to track time
    timer = 0
    dt = 0

    # Loop Counter
    done = False

    # Main Game Loop
    while not done:

        # Get user event
        for event in pygame.event.get():

            # If user clicks close
            if event.type == pygame.QUIT:

                sys.exit()

            # If user clicks the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Get the position of mouse click
                pos = pygame.mouse.get_pos()

                # Change the x/y coordinates to grid coordinates
                column = pos[0] // (width + margin)
                row = (pos[1] // (height + margin)) - 2

                # Reset Game
                if 95 + extra_xmargin <= pos[0] <= 120 and 10 <= pos[1] <= 45:
                    start_game(difficulty)

                # If game is going
                if status == "current" and row in grid_coordinates and column in grid_coordinates:

                    # Start timer
                    if timer == 0:
                        timer = 0.001

                    # If click was left click
                    if event.button == 1:
                        # If clicked cell is bomb
                        if grid[row][column] == "b":

                            # Change value to b_found
                            grid[row][column] = "b_found"

                        # If clicked on un-clicked space without bomb
                        elif grid[row][column] == 0:

                            assign_empty_cell_value(row, column, grid, grid_coordinates)

                    # If player right clicks to mark flag
                    elif event.button == 3:

                        # If player marked empty cell
                        if grid[row][column] == 0:

                            # Assign f
                            grid[row][column] = "f"
                            flags -= 1

                        # Reversing flag to empty
                        elif grid[row][column] == "f":
                            grid[row][column] = 0
                            flags += 1

                        # If player right clicked bomb location
                        elif grid[row][column] == "b":

                            # Assign bf
                            grid[row][column] = "bf"
                            flags -= 1

                        # Reverse bf to b
                        elif grid[row][column] == "bf":
                            grid[row][column] = "b"
                            flags += 1

        # --------- Game Design -----------------

        if timer != 0 and status == "current":
            timer += dt

        # Empty Cell Counter
        empty_cell_counter = 0

        # Set Screen Background
        screen.fill(black)

        # Remaining Flags Display
        pygame.draw.rect(screen, gray, [10+extra_xmargin, 10, 65, 35])
        flagfont = pygame.font.SysFont('arialblack', 30)
        screen.blit(flagfont.render(str(flags), True, red), (25+extra_xmargin, 6))

        # Reset/Game Status Button Display
        pygame.draw.rect(screen, gray, [95+extra_xmargin, 10, 35, 35])
        if status == "current":
            screen.blit(thumbs_up, (99+extra_xmargin, 13))
        elif status == "Lost":
            screen.blit(thumbs_down, (99+extra_xmargin, 13))
        elif status == "Won":
            screen.blit(crown, (99+extra_xmargin, 13))

        # Time Display
        pygame.draw.rect(screen, gray, [150+extra_xmargin, 10, 65, 35])
        flagfont = pygame.font.SysFont('arialblack', 25)
        screen.blit(flagfont.render(str(math.floor(timer)), True, red), (155+extra_xmargin, 9))

        # Menu Button
        button("Menu", 10+extra_xmargin, 290+extra_ymargin, 90, 30, green, light_green, 35, 12, 5)

        # Exit Button
        button("Exit", 130+extra_xmargin, 290+extra_ymargin, 90, 30, red, brightred, 35, 18, 5)

        # Check if won
        for row in range(len(grid_coordinates)):
            for column in range(len(grid_coordinates)):

                if grid[row][column] == 0 or grid[row][column] == "f":
                    empty_cell_counter += 1

        if empty_cell_counter == 0:
            status = "Won"

        # Draw grid
        for row in range(len(grid_coordinates)):
            for column in range(len(grid_coordinates)):
                color = gray

                # If bomb is found, set color to red
                if grid[row][column] == "b_found":
                    color = red
                    status = "Lost"

                # If empty was clicked, set color to white
                elif grid[row][column] == "e":
                    color = white

                pygame.draw.rect(screen, color, [(margin + width) * column + margin,
                                                 (margin + height) * row + margin + 50,
                                                 width,
                                                 height])

                # Number of adjacent bomb cells
                if grid[row][column] in (1, 2, 3, 4, 5, 6, 7, 8):
                    screen.blit(font.render(str(grid[row][column]), True, blue), ((margin + width) * column + 11,
                                                                                  (margin + height) * row + 6 + 50))

                # Flag Graphics
                if grid[row][column] == "f" or grid[row][column] == "bf":
                    screen.blit(flag_img, ((margin + width) * column + 7, (margin + height) * row + 6 + 50))

                # If game over
                if status == "Lost":

                    # Reveal all bombs
                    if grid[row][column] == "b_found" or grid[row][column] == "b":
                        screen.blit(bomb_img, ((margin + width) * column + 7, (margin + height) * row + 6 + 50))

                    # Reveal all incorrect flags
                    if grid[row][column] == "f":
                        screen.blit(bombx_img, ((margin + width) * column + 7, (margin + height) * row + 6 + 50))

                if status == "Won":

                    if grid[row][column] == "b":
                        screen.blit(flag_img, ((margin + width) * column + 7, (margin + height) * row + 6 + 50))

        dt = clock.tick(60) / 1000

        # --- Update the screen ---
        pygame.display.flip()


game_intro()
pygame.quit()
quit()