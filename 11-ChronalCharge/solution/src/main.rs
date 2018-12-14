use std::i32::MIN;

fn get_cell_value(x: usize, y: usize, serial_number: usize) -> i32 {
    let rack_id = x + 10;
    let inter1 = rack_id * y + serial_number;
    let mut inter2 = inter1 * rack_id;
    for _i in 0..2 {
        inter2 /= 10;
    }

    let res = ((inter2 % 10) as i32) - 5;
    // println!("Grid value for {}, {} is {}", x, y, res);
    return res;
}

fn calculate_meta_value(x: usize, y: usize, serial_number: usize, square_size: usize) -> i32 {
    let mut sum: i32 = 0;
    for i in 0..(square_size) {
        for j in 0..(square_size) {
            sum += get_cell_value(x + i, y + j, serial_number)
        }
    }

    return sum;
}

fn part1(serial_number: usize) -> (i32, (usize, usize)) {
    const ARRAY_DIMS: usize = 300;

    let mut curr_max = MIN;
    let mut curr_best_coord: (usize, usize) = (0, 0);
    for y in 0..(ARRAY_DIMS - 3) {
        for x in 0..(ARRAY_DIMS - 3) {
            let result = calculate_meta_value(x, y, serial_number, 3);
            // meta_grid[y][x] = result;
            if result > curr_max {
                curr_max = result;
                curr_best_coord = (x, y);
            }
        }
    }

    return (curr_max, curr_best_coord);
}

fn get_new_meta_grid(
    x: usize,
    y: usize,
    s: usize,
    grid: &[[i32; 300]; 300],
    meta_grid: &[[i32; 300]; 300]
    // grid: &[[i32; 3]; 3],
    // meta_grid: &[[i32; 3]; 3]
) -> i32 {
    let mut sum = (*meta_grid)[y][x];
    // println!("Original value is {} at {}, {} for size {}", sum, x, y, s);
    for i in 0..s {
        let res = (*grid)[y + i][x + s - 1];
        // println!("Adding {}, {}: {}", x + s - 1, y + i, res);
        sum += res;
    }

    for i in 0..(s - 1) {
        let res = (*grid)[y + s - 1][x + i];
        // println!("Adding {}, {}: {}", x + i, y + s - 1, res);
        sum += res;
    }

    return sum;
}

fn part2(serial_number: usize) -> (i32, (usize, usize), usize) {
    // const ARRAY_DIMS: usize = 3;
    const ARRAY_DIMS: usize = 300;

    let mut grid: [[i32; ARRAY_DIMS]; ARRAY_DIMS] = [[0; ARRAY_DIMS]; ARRAY_DIMS];
    let mut meta_grid: [[i32; ARRAY_DIMS]; ARRAY_DIMS] = [[0; ARRAY_DIMS]; ARRAY_DIMS];

    let mut curr_max = MIN;
    let mut curr_best_coord: (usize, usize) = (0, 0);
    let mut curr_best_size: usize = 1;

    for y in 0..ARRAY_DIMS {
        for x in 0..ARRAY_DIMS {
            let result = get_cell_value(x, y, serial_number);
            grid[y][x] = result;
            meta_grid[y][x] = result;
            if result > curr_max {
                curr_max = result;
                curr_best_coord = (x, y);
            }
        }
    }

    // print_grid(&meta_grid);

    for s in 2..(ARRAY_DIMS + 1) {
        println!("Handling size {}", s);
        for y in 0..(ARRAY_DIMS - s + 1) {
            for x in 0..(ARRAY_DIMS - s + 1) {
                let result = get_new_meta_grid(x, y, s, &grid, &meta_grid);
                // println!("Result for ({}, {}) at size {}: {}", x, y, s, result);
                meta_grid[y][x] = result;
                if result > curr_max {
                    curr_max = result;
                    curr_best_coord = (x, y);
                    curr_best_size = s;
                }
            }
        }
        
        // print_grid(&meta_grid);
    }

    println!("{}, {:?}, {}", curr_max, curr_best_coord, curr_best_size);
    return (curr_max, curr_best_coord, curr_best_size);
}

fn print_grid(grid: &[[i32; 3]; 3]) {
    for y in 0..3 {
        for x in 0..3 {
            print!("{} ", grid[y][x]);
        }
        println!("");
    }
}

fn main() {
    // assert!(get_cell_value(3, 5, 8) == 4);
    // assert!(get_cell_value(122, 79, 57) == -5);
    // assert!(get_cell_value(217, 196, 39) == 0);
    // assert!(get_cell_value(101, 153, 71) == 4);
    // assert!(part1(18) == (29, (33, 45)));
    // assert!(part1(42) == (30, (21, 61)));
    // println!("Solution to Part 1 is: {:?}", part1(4151));
    // assert!(part2(18) == (113, (90, 269), 16));
    // assert!(part2(42) == (119, (232, 251), 12));
    println!("Solution to Part 2 is: {:?}", part2(4151));
    // part2(50);
}
