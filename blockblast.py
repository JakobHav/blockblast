"""
  copyright 2025, Universität Freiburg

  author: Jakob Haverkamp <jh1444@email.uni-freiburg.de>

  date: 09.06.2025

  description: Blockblast Game

"""

import pygame
from sys import exit
from random import choice, randint

import pygame.macosx
pygame.init()

width: int = 650
height: int = 900
grid_size = width * 7 / 8
rows: int = 8
cols: int = 8

FONT = pygame.font.Font('freesansbold.ttf', 39)
SMALL_FONT = pygame.font.Font('freesansbold.ttf', 22)
bl_size: float = grid_size / cols

norm_color: tuple[int, int, int] = (29, 42, 65)
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)


colors: list[tuple[int, int, int]] = [(205, 205, 0), (205, 205, 0), (0, 170, 0), (60, 20, 210), (60, 20, 210), (210, 0, 40), (180, 80, 220), (40, 210, 210)]


# --------------------------------------------------------------------------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------------------------------------------------------------------------

class Block:
    def __init__(self, x: int, y: int, color: tuple[int, int, int]):
        self.x: int = x
        self.y: int = y
        self.color: tuple[int, int, int] = color

    def draw(self, win: pygame.Surface):
        if self.color == norm_color:
            pygame.draw.rect(win, self.color, (self.x * bl_size + width / 16, self.y * bl_size + height / 8, bl_size - 1, bl_size - 1))
        else:
            color_light = (int(self.color[0] * 8 / 7), int(self.color[1] * 8 / 7), int(self.color[2] * 8 / 7))
            color_dark = (int(self.color[0] * 3 / 4), int(self.color[1] * 3 / 4), int(self.color[2] * 3 / 4))
            start: tuple[float, float] = (self.x * bl_size + width / 16, self.y * bl_size + height / 8)

            pygame.draw.polygon(win, color_light, [(start[0] + bl_size, start[1]), (start[0], start[1] + bl_size), (start[0], start[1])])
            pygame.draw.polygon(win, color_dark, [(start[0] + bl_size, start[1]), (start[0], start[1] + bl_size), (start[0] + bl_size, start[1] + bl_size)])

            pygame.draw.rect(win, self.color, (start[0] + 8, start[1] + 8, bl_size - 17, bl_size - 17))

    def preview(self, win: pygame.Surface):

        color_light = (int(self.color[0] * 8 / 7), int(self.color[1] * 8 / 7), int(self.color[2] * 8 / 7))
        color_dark = (int(self.color[0] * 3 / 4), int(self.color[1] * 3 / 4), int(self.color[2] * 3 / 4))
        start: tuple[float, float] = (self.x * bl_size / 2 + width / 16, self.y * bl_size / 2 + height / 8 + grid_size + bl_size * 1.75)

        pygame.draw.polygon(win, color_light, [(start[0] + bl_size / 2, start[1]), (start[0], start[1] + bl_size / 2), (start[0], start[1])])
        pygame.draw.polygon(win, color_dark, [(start[0] + bl_size / 2, start[1]), (start[0], start[1] + bl_size / 2), (start[0] + bl_size / 2, start[1] + bl_size / 2)])

        pygame.draw.rect(win, self.color, (start[0] + 4, start[1] + 4, bl_size / 2 - 8, bl_size / 2 - 8))

    def draw_pickup(self, win: pygame.Surface, x: float, y: float):
        color_light = (int(self.color[0] * 8 / 7), int(self.color[1] * 8 / 7), int(self.color[2] * 8 / 7))
        color_dark = (int(self.color[0] * 3 / 4), int(self.color[1] * 3 / 4), int(self.color[2] * 3 / 4))
        start: tuple[float, float] = (x, y)

        pygame.draw.polygon(win, color_light, [(start[0] + bl_size, start[1]), (start[0], start[1] + bl_size), (start[0], start[1])])
        pygame.draw.polygon(win, color_dark, [(start[0] + bl_size, start[1]), (start[0], start[1] + bl_size), (start[0] + bl_size, start[1] + bl_size)])

        pygame.draw.rect(win, self.color, (start[0] + 8, start[1] + 8, bl_size - 17, bl_size - 17))


class SingleBlock:
    def __init__(self, x: int = -1, y: int = -1, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.x: int = x
        self.y: int = y
        self.color: tuple[int, int, int] = choice(colors)
        self.members: list[Block] = [Block(self.x, self.y, self.color)]


class CUBE2(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for x in range(-1, 1):
            for y in range(-1, 1):
                self.members.append(Block(self.x + x, self.y + y, self.color))


class CUBE3(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                self.members.append(Block(self.x + x, self.y + y, self.color))


class Hori2(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for x in range(-1, 1):
            self.members.append(Block(self.x + x, self.y, self.color))


class Hori3(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for x in range(-1, 2):
            self.members.append(Block(self.x + x, self.y, self.color))


class Hori4(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for x in range(-2, 2):
            self.members.append(Block(self.x + x, self.y, self.color))


class Hori5(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for x in range(-2, 3):
            self.members.append(Block(self.x + x, self.y, self.color))


class Verti2(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for y in range(-1, 1):
            self.members.append(Block(self.x, self.y + y, self.color))


class Verti3(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for y in range(-1, 2):
            self.members.append(Block(self.x, self.y + y, self.color))


class Verti4(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for y in range(-2, 2):
            self.members.append(Block(self.x, self.y + y, self.color))


class Verti5(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = []
        for y in range(-2, 3):
            self.members.append(Block(self.x, self.y + y, self.color))


class T_UP(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = [Block(self.x, self.y, self.color), Block(self.x + 1, self.y, self.color), Block(self.x - 1, self.y, self.color), Block(self.x, self.y - 1, self.color)]


class T_DOWN(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = [Block(self.x, self.y, self.color), Block(self.x + 1, self.y, self.color), Block(self.x - 1, self.y, self.color), Block(self.x, self.y + 1, self.color)]


class T_LEFT(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = [Block(self.x, self.y, self.color), Block(self.x - 1, self.y, self.color), Block(self.x, self.y - 1, self.color), Block(self.x, self.y + 1, self.color)]


class T_RIGHT(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = [Block(self.x, self.y, self.color), Block(self.x + 1, self.y, self.color), Block(self.x, self.y - 1, self.color), Block(self.x, self.y + 1, self.color)]


class L_Norm(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = [Block(self.x, self.y, self.color), Block(self.x, self.y + 1, self.color), Block(self.x, self.y - 1, self.color), Block(self.x + 1, self.y - 1, self.color)]


class L_Mirror(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = [Block(self.x, self.y, self.color), Block(self.x, self.y + 1, self.color), Block(self.x, self.y - 1, self.color), Block(self.x - 1, self.y - 1, self.color)]


class L_Flip(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = [Block(self.x, self.y, self.color), Block(self.x, self.y + 1, self.color), Block(self.x, self.y - 1, self.color), Block(self.x + 1, self.y + 1, self.color)]


class L_MFlip(SingleBlock):
    def __init__(self, x: int = -1, y: int = -1) -> None:
        super().__init__(x, y)
        self.members: list[Block] = [Block(self.x, self.y, self.color), Block(self.x, self.y + 1, self.color), Block(self.x, self.y - 1, self.color), Block(self.x - 1, self.y + 1, self.color)]

# --------------------------------------------------------------------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------------------------------------------------------------------


def place_block(preview_blocks: list[SingleBlock], grid: list[list[Block]]):
    for bigblock in preview_blocks:
        if bigblock.y == -2:
            oldx = bigblock.x
            x, y = pygame.mouse.get_pos()
            absx: int = int((x - width / 16) // (bl_size))
            absy: int = int((y - height / 8) // (bl_size))
            out_of_bounds: bool = False
            for block in bigblock.members:
                newblockx = block.x - oldx + absx
                newblocky = block.y + absy + 1
                if not (0 <= newblockx < cols and 0 <= newblocky < cols) or not grid[newblockx][newblocky].color == norm_color:
                    out_of_bounds = True

            if not out_of_bounds:
                bigblock.x, bigblock.y = absx, absy
                for block in bigblock.members:
                    block.x = block.x - oldx + bigblock.x
                    block.y = block.y + bigblock.y + 1
                update_preview(preview_blocks)
            else:
                bigblock.y = -1
            break


def pickup_block(preview_blocks: list[SingleBlock]):
    x, y = pygame.mouse.get_pos()
    absx: int = int((x - width / 16) // (bl_size))
    absy: int = int((y - height / 8) // (bl_size))
    if 8 <= absy <= 10:
        absx = int((x - width / 16) // (bl_size / 2))
        for bigblock in preview_blocks:
            if bigblock.y == -1:
                if abs(bigblock.x - absx) <= 2:
                    bigblock.y = -2
    elif (width * 13 / 16 < x < width * 13 / 16 + bl_size * 1.15 and height / 32 < y < height / 32 + bl_size / 2.3):
        reset_preview(preview_blocks)


def check_cols_rows(grid: list[list[Block]]) -> int:
    rowsdone: list[int] = list(range(rows))
    colsdone: list[int] = list(range(cols))
    for x in range(cols):
        for y in range(rows):
            if grid[x][y].color == norm_color:
                if x in colsdone:
                    colsdone.remove(x)

    for y in range(rows):
        for x in range(cols):
            if grid[x][y].color == norm_color:
                if y in rowsdone:
                    rowsdone.remove(y)

    for y in rowsdone:
        for x in range(cols):
            grid[x][y].color = norm_color

    for x in colsdone:
        for y in range(rows):
            grid[x][y].color = norm_color

    match (len(colsdone), len(rowsdone)):
        case 0, 0:
            return 0
        case 1, 0:
            return randint(51, 149)
        case 0, 1:
            return randint(51, 149)
        case 0, x:
            return int((100 * 1.7**(x - 1)))
        case x, 0:
            return int((100 * 1.7**(x - 1)))
        case _, _:
            return (100 * len(colsdone) * len(rowsdone) + randint(51, 149))


def update_grid(grid: list[list[Block]], preview_blocks: list[SingleBlock]):
    for bigblock in preview_blocks:
        if bigblock.y == -1:  # Preview Blocks
            for block in bigblock.members:
                block.preview(window)
        elif bigblock.y == -2:  # Picked Up Blocks
            for block in bigblock.members:
                block.draw_pickup(window, pygame.mouse.get_pos()[0] + bl_size * (block.x - bigblock.x - 0.5), pygame.mouse.get_pos()[1] + bl_size * (block.y + 0.5))
        else:
            for block in bigblock.members:
                grid[block.x][block.y] = block
            preview_blocks.remove(bigblock)


def reset_preview(preview_blocks: list[SingleBlock]):
    preview_blocks.clear()
    fill_preview(preview_blocks)


def update_preview(preview_blocks: list[SingleBlock]):
    empty = True
    for bigblock in preview_blocks:
        if bigblock.y == -1 or bigblock.y == -2:
            empty = False
    if empty:
        fill_preview(preview_blocks)


def check_space_left(preview_blocks: list[SingleBlock], grid: list[list[Block]]) -> bool:
    for bigblock in preview_blocks:
        for x in range(cols):
            for y in range(rows):
                if check_fits_in(bigblock, grid, x, y):
                    return True
    return False


def check_fits_in(bigblock: SingleBlock, grid: list[list[Block]], x: int, y: int) -> bool:
    oldx = bigblock.x
    out_of_bounds: bool = False
    for block in bigblock.members:
        newblockx = block.x - oldx + x
        newblocky = block.y + y + 1
        if not (0 <= newblockx < cols and 0 <= newblocky < cols) or not grid[newblockx][newblocky].color == norm_color:
            out_of_bounds = True
    return not out_of_bounds


def fill_preview(preview_blocks: list[SingleBlock]):
    for nr in range(3):
        block: SingleBlock
        match(randint(0, 18)):
            case 0:
                block = SingleBlock(2 + nr * 5, -1)
            case 1:
                block = Hori2(2 + nr * 5, -1)
            case 2:
                block = Hori3(2 + nr * 5, -1)
            case 3:
                block = Hori4(2 + nr * 5, -1)
            case 4:
                block = Hori5(2 + nr * 5, -1)
            case 5:
                block = Verti2(2 + nr * 5, -1)
            case 6:
                block = Verti3(2 + nr * 5, -1)
            case 7:
                block = Verti4(2 + nr * 5, -1)
            case 8:
                block = Verti5(2 + nr * 5, -1)
            case 9:
                block = T_UP(2 + nr * 5, -1)
            case 10:
                block = T_DOWN(2 + nr * 5, -1)
            case 11:
                block = T_LEFT(2 + nr * 5, -1)
            case 12:
                block = T_RIGHT(2 + nr * 5, -1)
            case 13:
                block = CUBE2(2 + nr * 5, -1)
            case 14:
                block = CUBE3(2 + nr * 5, -1)
            case 15:
                block = L_Norm(2 + nr * 5, -1)
            case 16:
                block = L_Flip(2 + nr * 5, -1)
            case 17:
                block = L_Flip(2 + nr * 5, -1)
            case 18:
                block = L_MFlip(2 + nr * 5, -1)
        preview_blocks.append(block)


def render_view(grid: list[list[Block]], preview_blocks: list[SingleBlock], score: int):
    window.fill((56, 99, 168))
    pygame.draw.rect(window, (19, 32, 45), (width / 16, height / 8, grid_size, grid_size))
    for x in range(cols):
        for y in range(rows):
            box = grid[x][y]
            box.draw(window)

    update_grid(grid, preview_blocks)
    window.blit(FONT.render(f"{score}", True, (222, 222, 222)), (width / 16 + grid_size / 2 - len(str(score)) * 10, height / 16))
    pygame.draw.rect(window, (19, 32, 45), (width * 13 / 16, height / 32, bl_size * 1.15, bl_size / 2.3))
    window.blit(SMALL_FONT.render("RESET", True, (222, 222, 222)), (width * 13 / 16 + 2, height / 32 + 5))


# --------------------------------------------------------------------------------------------------------------------------------------------
# Main Function
# --------------------------------------------------------------------------------------------------------------------------------------------

def main():
    global width, height, bl_size, grid_size

    grid: list[list[Block]] = []
    clock = pygame.time.Clock()
    runnin: bool = True
    score: int = 0

    preview_blocks: list[SingleBlock] = []

    for x in range(cols):
        arr: list[Block] = []
        for y in range(rows):
            arr.append(Block(x, y, norm_color))
        grid.append(arr)

    fill_preview(preview_blocks)

    while runnin:
        width, height = window.get_size()
        grid_size = width * 7 / 8
        bl_size = grid_size / cols

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pickup_block(preview_blocks)
            if event.type == pygame.MOUSEBUTTONUP:  # Block Placed
                place_block(preview_blocks, grid)
                render_view(grid, preview_blocks, score)
                score += check_cols_rows(grid)
                while not check_space_left(preview_blocks, grid):
                    reset_preview(preview_blocks)
                pygame.display.flip()
                clock.tick(60)

        render_view(grid, preview_blocks, score)

        pygame.display.flip()
        clock.tick(60)


main()
