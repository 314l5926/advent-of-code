# binary ops with a little help from claude
# Cell types stored in lower 4 bits
EMPTY = 0
WALL = 1
OBSTACLE = 2
# Directions stored in lower 4 bits for guard position
UP = 3
RIGHT = 4
DOWN = 5
LEFT = 6

# Direction visited flags use upper 4 bits
VISITED_UP = 0x80     # 10000000
VISITED_RIGHT = 0x40  # 01000000
VISITED_DOWN = 0x20   # 00100000
VISITED_LEFT = 0x10   # 00010000
VISITED_MASK = 0xF0   # 11110000
CELL_MASK = 0x0F      # 00001111

def parse_map(input_map: str) -> tuple[bytearray, int, int]:
    """Convert the string input map into a bytearray using our bit representation."""
    lines = [line.strip() for line in input_map.strip().split('\n')]
    height = len(lines)
    width = len(lines[0])
    grid = bytearray(width * height)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            pos = y * width + x
            if char == '#':
                grid[pos] = WALL
            elif char == '^':
                grid[pos] = UP
            elif char == '>':
                grid[pos] = RIGHT
            elif char == 'v':
                grid[pos] = DOWN
            elif char == '<':
                grid[pos] = LEFT
            elif char == 'O':
                grid[pos] = OBSTACLE
            else:  # '.'
                grid[pos] = EMPTY

    return grid, width, height

def find_guard_start(grid: bytearray, width: int) -> tuple[int, int, int]:
    """Find the guard's starting position and direction."""
    for i, cell in enumerate(grid):
        cell_type = cell & CELL_MASK
        if cell_type in (UP, RIGHT, DOWN, LEFT):
            return i // width, i % width, cell_type
    return -1, -1, -1

def get_next_position(pos: int, direction: int, width: int) -> int:
    """Calculate the next position index based on current position and direction."""
    row = pos // width
    col = pos % width

    if direction == UP:
        new_row = row - 1
        new_col = col
    elif direction == RIGHT:
        new_row = row
        new_col = col + 1
    elif direction == DOWN:
        new_row = row + 1
        new_col = col
    else:  # LEFT
        new_row = row
        new_col = col - 1

    if new_col < 0 or new_col >= width:
        return -1
    return new_row * width + new_col

def turn_right(direction: int) -> int:
    """Return the new direction after turning right."""
    directions = (UP, RIGHT, DOWN, LEFT)
    return directions[(directions.index(direction) + 1) % 4]

def is_valid_position(pos: int, width: int, height: int) -> bool:
    """Check if the position index is within the grid."""
    if pos < 0:
        return False
    row = pos // width
    return 0 <= row < height

def get_visited_bit(direction: int) -> int:
    """Get the bit position for marking visited from this direction."""
    return {
        UP: VISITED_UP,
        RIGHT: VISITED_RIGHT,
        DOWN: VISITED_DOWN,
        LEFT: VISITED_LEFT
    }[direction]

def is_obstacle(cell: int) -> bool:
    """Check if a cell is a wall or placed obstacle."""
    cell_type = cell & CELL_MASK
    return cell_type in (WALL, OBSTACLE)

def get_reachable_positions(grid: bytearray, start_pos: int, start_direction: int, width: int, height: int) -> set[int]:
    """Get all positions the guard can reach in the original path."""
    reachable = {start_pos}
    current_pos = start_pos
    direction = start_direction

    while True:
        next_pos = get_next_position(current_pos, direction, width)

        # Check if we've left the map
        if not is_valid_position(next_pos, width, height):
            break

        # Check if there's an obstacle ahead
        if is_obstacle(grid[next_pos]):
            # Add the position where we turn
            reachable.add(current_pos)
            direction = turn_right(direction)
        else:
            # Move forward and add the new position
            current_pos = next_pos
            reachable.add(current_pos)

    return reachable

def detect_loop(grid: bytearray, start_pos: int, start_direction: int, width: int, height: int) -> bool:
    """
    Simulate guard movement and detect if it forms a loop.
    Uses the high bits of each cell to mark visited directions.
    """
    current_pos = start_pos
    direction = start_direction

    while True:
        direction_bit = get_visited_bit(direction)
        if grid[current_pos] & direction_bit:
            return True  # Loop detected

        # Mark this direction as visited
        grid[current_pos] |= direction_bit

        next_pos = get_next_position(current_pos, direction, width)
        if not is_valid_position(next_pos, width, height):
            return False

        if is_obstacle(grid[next_pos]):
            direction = turn_right(direction)
        else:
            current_pos = next_pos

def find_loop_positions(input_map: str) -> int:
    """Find all positions where placing an obstruction creates a loop."""
    original_grid, width, height = parse_map(input_map)

    # Find guard's starting position
    start_y, start_x, direction = find_guard_start(original_grid, width)
    if start_y == -1:
        return 0

    start_pos = start_y * width + start_x

    # Get reachable positions
    reachable = get_reachable_positions(original_grid, start_pos, direction, width, height)

    # Debug print
    def print_grid_with_reachable():
        for y in range(height):
            row = ""
            for x in range(width):
                pos = y * width + x
                cell = original_grid[pos] & CELL_MASK
                if pos in reachable:
                    if cell == EMPTY:
                        row += 'X'
                    elif cell == WALL:
                        row += '#'
                    elif cell in (UP, RIGHT, DOWN, LEFT):
                        row += '^>v<'[cell - UP]
                    else:
                        row += 'O'
                else:
                    if cell == EMPTY:
                        row += '.'
                    elif cell == WALL:
                        row += '#'
                    elif cell in (UP, RIGHT, DOWN, LEFT):
                        row += '^>v<'[cell - UP]
                    else:
                        row += 'O'
            print(row)

    print("Map with reachable positions marked as X:")
    print_grid_with_reachable()

    loop_count = 0
    # Test each reachable position
    for pos in reachable:
        if (original_grid[pos] & CELL_MASK) != EMPTY or pos == start_pos:
            continue

        # Create a fresh copy of the grid for each test
        test_grid = bytearray(original_grid)
        test_grid[pos] = OBSTACLE

        if detect_loop(test_grid, start_pos, direction, width, height):
            loop_count += 1

    return loop_count


with open("/home/user/workspace/advent/day6.txt", "r") as f:
    test_input = f.read()

result = find_loop_positions(test_input)
print(f"Number of possible obstruction positions: {result}")
