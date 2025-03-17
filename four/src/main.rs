use std::env;
use std::fs;

// Grid that can be indexed by row, column
// [0][0], [0][1], [0][2]
// [1][0], [1][1], [1][2]
// [2][0], [2][1], [2][2]
struct Grid {
    grid: Vec<Vec<char>>,
    num_rows: usize,
    num_columns: usize,
}

const DIRECTIONS: [(i32, i32); 8] = [
    (-1, 0),  // Up
    (1, 0),   // Down
    (0, -1),  // Left
    (0, 1),   // Right
    (-1, -1), // Up-Left
    (-1, 1),  // Up-Right
    (1, -1),  // Down-Left
    (1, 1),   // Down-Right
];

fn load_grid(file_path: &str) -> Grid {
    let contents = fs::read_to_string(file_path).expect("Path should be a readable UTF-8 file");
    let grid: Vec<Vec<char>> = contents
        .lines()
        .map(|line| line.chars().collect())
        .collect();

    let num_rows = grid.len();
    let num_columns = grid[0].len();

    Grid {
        grid,
        num_rows,
        num_columns,
    }
}

fn find_starts(grid: &Grid, char: char) -> Vec<(usize, usize)> {
    let mut row = 0;
    let mut column;
    let mut starts: Vec<(usize, usize)> = Vec::new();

    while row < grid.num_rows {
        column = 0;
        while column < grid.num_columns {
            if grid.grid[row][column] == char {
                starts.push((row, column));
            }
            column += 1;
        }
        row += 1;
    }
    starts
}

fn check_direction(
    grid: &Grid,
    start: (usize, usize),
    query: &[char],
    direction: (i32, i32),
) -> bool {
    let (mut current_row, mut current_column) = start;
    for &expected_char in &query[1..] {
        let new_row = current_row as i32 + direction.0;
        let new_column = current_column as i32 + direction.1;
        if new_row < 0
            || new_column < 0
            || new_row >= grid.num_rows as i32
            || new_column >= grid.num_columns as i32
        {
            return false;
        }
        current_row = new_row as usize;
        current_column = new_column as usize;

        if grid.grid[current_row][current_column] != expected_char {
            return false;
        }
    }
    true
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Usage: ./four <file_path>");
    }

    let file_path = &args[1];
    let query: Vec<char> = "XMAS".chars().collect();

    let grid = load_grid(file_path);
    let starts = find_starts(&grid, query[0]);

    let mut total_found = 0;

    for start in starts {
        for dir in DIRECTIONS {
            if check_direction(&grid, start, &query, dir) {
                total_found += 1;
            }
        }
    }

    println!("In {file_path}, found XMAS {total_found} times!");
}
