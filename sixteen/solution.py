from collections import namedtuple
from pathlib import Path
import queue

Coord = namedtuple('Coord', ['x', 'y'])
 
def load_maze(file_path: Path) -> tuple[dict, Coord, Coord]:
    """
    Return maze, start, end.
    Bottom left can be indexed with maze[0,0]
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Reverse the lines to make [0,0] the bottom-left
    lines = [line.strip() for line in lines][::-1]

    # Initialize grid and variables for S and E positions
    grid = {}
    start_position = None
    end_position = None

    # Create the grid and identify S and E positions
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S':
                start_position = Coord(x, y)
            elif char == 'E':
                end_position = Coord(x, y)
            grid[x, y] = 0 if char in {'.', 'S', 'E'} else 1

    if start_position is None or end_position is None:
        raise ValueError
    
    return grid, start_position, end_position

def neighbours(maze: dict, current: Coord) -> list[tuple[str,Coord]]:
    """
    Returns list of coords which could be moved to next
    There are a maximum of 4 moves, as can only move
    orthogonally.
    """
    available_coords = []

    if maze[current.x, current.y+1] == 0:
        available_coords.append(("up", Coord(current.x, current.y+1)))

    if maze[current.x, current.y-1] == 0:
        available_coords.append(("down", Coord(current.x, current.y-1)))

    if maze[current.x-1, current.y] == 0:
        available_coords.append(("left", Coord(current.x-1, current.y)))

    if maze[current.x+1, current.y] == 0:
        available_coords.append(("right", Coord(current.x+1, current.y)))

    return available_coords

def solve_dijkstra(maze, start, end):
    """
    Implementation of dijkstra, following video below
    https://www.youtube.com/watch?v=GazC3A4OQTE
    """
    open_set = queue.PriorityQueue()
    done = set()
    open_set.put((0, start, "right")) # (cost, coord, direction)
    while open_set.qsize() != 0:
        current = open_set.get()
        current_cost = current[0]
        current_coord = current[1]
        current_direction = current[2]
        if current_coord == end:
            return current_cost
        for next_direction, next_coord in neighbours(maze, current_coord):
            if next_coord in done:
                continue
            if next_direction == current_direction:
                cost = 1
            else: 
                cost = 1001
            open_set.put((current_cost+cost, next_coord, next_direction))
        done.add(current_coord)
            

def main():
    maze_file = Path("maze.txt")
    maze, start, end = load_maze(maze_file)
    print(solve_dijkstra(maze, start, end))
    

if __name__ == "__main__":
    main()
