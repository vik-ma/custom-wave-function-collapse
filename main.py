import pygame
import random
from tile import Tile
from button import Button
from pattern import Pattern

pygame.init()

WIDTH = 800
HEIGHT = 640

clock = pygame.time.Clock()
FPS = 60

ROWS = 50
COLS = 50
TILE_WIDTH = 4
TILE_HEIGHT = 4

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (175, 175, 175)
LIGHTGREY = (213, 213, 213)

UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)
UP_LEFT = (-1, -1)
UP_RIGHT = (1, -1)
DOWN_LEFT = (-1, 1)
DOWN_RIGHT = (1, 1)
directions = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

tile_group = pygame.sprite.Group()

def draw_window():
    screen.fill(GREY)


sample_pixel_array = [
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, BLACK),
    (WHITE, BLACK, GREY, BLACK),
    (WHITE, BLACK, BLACK, BLACK)
    ]

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            tile = Tile(TILE_WIDTH, TILE_HEIGHT, (col * TILE_WIDTH + 50), (row * TILE_HEIGHT + 50), sample_pixel_array)
            tile_group.add(tile)
    tile_group.draw(screen)


def draw_tile():
    tile = Tile(TILE_WIDTH, TILE_HEIGHT, (0 * TILE_WIDTH + 50), (0 * TILE_HEIGHT + 50), sample_pixel_array)
    tile_group.add(tile)

    rotated_array = get_rotated_pix_array(sample_pixel_array)
    tile2 = Tile(TILE_WIDTH, TILE_HEIGHT, (0 * TILE_WIDTH + 50), (1 * TILE_HEIGHT + 50), rotated_array[1])
    tile3 = Tile(TILE_WIDTH, TILE_HEIGHT, (1 * TILE_WIDTH + 50), (0 * TILE_HEIGHT + 50), rotated_array[2])
    tile4 = Tile(TILE_WIDTH, TILE_HEIGHT, (1 * TILE_WIDTH + 50), (1 * TILE_HEIGHT + 50), rotated_array[3])

    tile_group.add(tile2)
    tile_group.add(tile3)
    tile_group.add(tile4)

    tile_group.draw(screen)

def get_rotated_pix_array(pix_array):
    rotated_pix_array_270 = tuple(zip(*pix_array[::-1]))
    rotated_pix_array_180 = tuple(zip(*rotated_pix_array_270[::-1]))
    rotated_pix_array_90 = tuple(zip(*rotated_pix_array_180[::-1]))
    pix_array = tuple(pix_array)
    return (pix_array, rotated_pix_array_90, rotated_pix_array_180, rotated_pix_array_270)

def get_pix_array_patterns(pix_array):
    pattern_size = 2 #2x2
    pattern_list = []
    occurence_weights = {}
    probability = {}

    for row in range(TILE_WIDTH - (pattern_size - 1)):
        for col in range(TILE_HEIGHT - (pattern_size -1)):
            pattern = []
            for pix in pix_array[row:row+pattern_size]:
                pattern.append(pix[col:col+pattern_size])
            pattern_rotations = get_rotated_pix_array(pattern)
        
            for rotation in pattern_rotations:
                if rotation not in occurence_weights:
                    occurence_weights[rotation] = 1
                else:
                    occurence_weights[rotation] += 1
            
            pattern_list.extend(pattern_rotations)
        
    unique_pattern_list = []
    for pattern in pattern_list:
        if pattern not in unique_pattern_list:
            unique_pattern_list.append(pattern)
    pattern_list = unique_pattern_list

    sum_of_weights = 0
    for weight in occurence_weights:
        sum_of_weights += occurence_weights[weight]

    for pattern in pattern_list:
        probability[pattern] = occurence_weights[pattern] / sum_of_weights

    pattern_list = [Pattern(pattern) for pattern in pattern_list]
    occurence_weights = {pattern:occurence_weights[pattern.pix_array] for pattern in pattern_list}
    probability = {pattern:probability[pattern.pix_array] for pattern in pattern_list}

    return pattern_list, occurence_weights, probability

def get_valid_directions(position):
    x, y = position
    
    valid_directions = []

    if x == 0:
        valid_directions.extend([RIGHT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_RIGHT])
        elif y == ROWS-1:
            valid_directions.extend([UP, UP_RIGHT])
        else:
            valid_directions.extend([DOWN, DOWN_RIGHT, UP, UP_RIGHT])
    elif x == COLS-1:
        valid_directions.extend([LEFT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_LEFT])
        elif y == ROWS-1:
            valid_directions.extend([UP, UP_LEFT])
        else:
            valid_directions.extend([DOWN, DOWN_LEFT, UP, UP_LEFT])
    else:
        valid_directions.extend([LEFT, RIGHT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_LEFT, DOWN_RIGHT])
        elif y == ROWS-1:
            valid_directions.extend([UP, UP_LEFT, UP_RIGHT])
        else: 
            valid_directions.extend([UP, UP_LEFT, UP_RIGHT, DOWN, DOWN_LEFT, DOWN_RIGHT])
    
    return valid_directions

def draw_patterns(pix_array):
    patterns = get_pix_array_patterns(pix_array)[0]
    for col in range(len(patterns)):
        tile = Tile(2, 2, (col * 2 + 50), 50, patterns[col].pix_array)
        tile_group.add(tile)
    tile_group.draw(screen)

make_grid_button = Button(WHITE, 600, 50, 150, 40, "Make Grid", BLACK, LIGHTGREY)
test_button = Button(WHITE, 600, 550, 150, 40, "TEST", BLACK, LIGHTGREY)
draw_test_button = Button(WHITE, 600, 450, 150, 40, "DRAW TEST", BLACK, LIGHTGREY)

def main():
    run = True

    is_grid_drawn = False

    draw_test = False

    while run:
        clock.tick(FPS)
        draw_window()
        pygame.draw.rect(screen, BLACK, (49, 49, COLS * TILE_WIDTH + 2, ROWS * TILE_HEIGHT + 2), 1)

        # draw_tile()

        if is_grid_drawn:
            draw_grid()
        
        if make_grid_button.draw(screen):
            is_grid_drawn = True


        if draw_test:
            draw_patterns(sample_pixel_array)

        if draw_test_button.draw(screen):
            draw_test = True


        if test_button.draw(screen):
            print(get_valid_directions((0,0)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()