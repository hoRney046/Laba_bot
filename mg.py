def get_map_cell(cols, rows):
    class Cell:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            self.visited = False

        def check_cell(self, x, y):
            if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
                return False
            return grid_cell[x + y * cols]

    def check_wall(grid_cell, x, y):
        if x % 2 == 0 and y % 2 == 0:
            return False
        if x % 2 == 1 and y % 2 == 1:
            return True

        if x % 2 == 0:
            grid_x = x // 2
            grid_y = (y - 1) // 2
            return grid_cell[grid_x + grid_y * cols].walls['bottom']
        else:
            grid_x = (x - 1) // 2
            grid_y = y // 2
            return grid_cell[grid_x + grid_y * cols].walls['right']

    grid_cell = [Cell(x, y) for y in range(rows) for x in range(cols)]
    current_cell = grid_cell[0]
    current_cell.visited = True


    return [check_wall(grid_cell, x, y) for y in range(rows * 2 - 1) for x in range(cols * 2 - 1)]
