import pygame
import copy

res = []
number_selected = 0

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

GRID_HEIGHT = 400
GRID_WIDTH = 400

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 400

def check_user_solution(grid, solution, n):
    for row in range(n):
        for col in range(n):
            if grid[row][col].selected == 1 and solution[row][col].bulb == 1:
                pass
            elif grid[row][col].block == 1:
                pass
            elif grid[row][col].selected == 0 and solution[row][col].bulb == 1:
                return False
            elif grid[row][col].selected == 1 and solution[row][col].bulb == 0:
                return False
    return True

def placeLightBulb(grid, pos):

    global number_selected

    if pos[0] < GRID_WIDTH and pos[1] < GRID_HEIGHT:

        line = n * pos[1] // GRID_HEIGHT
        col = n * pos[0] // GRID_WIDTH

        if grid[line][col].selected == 0:
            grid[line][col].selected = 1
            number_selected += 1
        else:
            grid[line][col].selected = 0
            number_selected -= 1

    return grid

def drawGrid(grid, n):
    x, y = 0,0
    w = GRID_WIDTH / n

    for row in grid:

        for col in row:

            rect = pygame.Rect(x, y, w, w)

            if col.selected == 1 and col.block == 0:
                pygame.draw.rect(SCREEN, WHITE, rect, 0)
                pygame.draw.rect(SCREEN, RED, rect, 2)
            elif col.block == 0:
                pygame.draw.rect(SCREEN, WHITE, rect, 0)
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
            else:
                pygame.draw.rect(SCREEN, BLACK, rect, 0)
                pygame.draw.rect(SCREEN, WHITE, rect, 1)

            x += w
        y += w
        x = 0

def drawText(message, x, y):

    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(message, True, GREEN, BLUE)

    textRect = text.get_rect()
    textRect.center = (x, y)

    SCREEN.blit(text, textRect)

class Cell:
    def __init__(self, block, bulb, lit):
        self.block = block
        self.bulb = bulb
        self.lit = lit
        self.selected = 0

def Print_Grid(grid, n):
    for i in range(n):
        for j in range(n):
            # print(grid[i][j].block, end="(")
            if grid[i][j].block == 1:
                print("X", end="")
            elif grid[i][j].bulb == 1:
                print("L", end="")
            elif grid[i][j].lit > 0:
                print("O", end="")
            else:
                print("-", end="")
        print(" ")

def Check(grid, n):

    for i in range(n):
        for j in range(n):
            if grid[i][j].block == 0:
                if grid[i][j].lit > 0 or grid[i][j].bulb == 1:
                    continue
                else:
                    return False
    return True

def Manage_Lights(grid, line, column, n, on_off):

    grid[line][column].bulb = on_off

    for i in range(column, -1, -1):
        if grid[line][i].block == 0:
            grid[line][i].lit += on_off
        else:
            break

    for i in range(column, n, 1):
        if grid[line][i].block == 0:
            grid[line][i].lit += on_off
        else:
            break

    for i in range(line, -1, -1):
        if grid[i][column].block == 0:
            grid[i][column].lit += on_off
        else:
            break

    for i in range(line, n, 1):
        if grid[i][column].block == 0:
            grid[i][column].lit += on_off
        else:
            break

    return grid

def Solve(grid, n, num, column, line):

    # base case
    if Check(grid, n) == True:
        solution = []
        solution.append(num)
        copy_grid = copy.deepcopy(grid)
        solution.append(copy_grid)
        res.append(solution)
        return

    if column == n:
        column = 0
        line += 1

    if line < n:
        # light bulb up
        grid = Manage_Lights(grid, line, column, n, 1)
        Solve(grid, n, num + 1, column + 1, line)

        # light bulb off
        grid = Manage_Lights(grid, line, column, n, -1)
        Solve(grid, n, num, column + 1, line)

if __name__=="__main__":

    line = input()
    n = int(line)
    grid = [[] for i in range(n)]

    for i in range(n):
        for j in range(n):
            line = input()
            is_block = int(line)
            grid[i].append(Cell(is_block, 0, 0))

    Solve(grid, n, 0, 0, 0)

    solution = float('inf')

    for i in res:
        if solution > i[0]:
            solution = i[0]

    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Light Up')
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:

        drawGrid(grid, n)
        drawText('Check Solution - Press "A" ', 130, 420)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                grid = placeLightBulb(grid, pos)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:

                    SCREEN.fill(pygame.Color("black"))

                    check = False
                    flag = 0

                    if solution == number_selected:
                        for i in res:
                            if i[0] == solution:
                                check = check_user_solution(grid, i[1], n)
                                if check == True:
                                    flag = 1

                        if flag == 1:
                            drawText('Solution Checked - Correct', 135, 450)
                        else:
                            drawText('Solution Checked - Try Again', 135, 450)

                    else:
                        drawText('Solution Checked - Try Again', 135, 450)

        pygame.display.update()
