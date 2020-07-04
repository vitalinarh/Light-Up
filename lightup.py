res = []

class Cell:
    def __init__(self, block, bulb, lit):
        self.block = block
        self.bulb = bulb
        self.lit = lit

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
        #print(" ")
        #Print_Grid(grid, n)
        res.append(num)
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

    print(min(res))
