use std::io::prelude::*;
use std::fs::File;
use std::collections::VecDeque;
use std::collections::HashSet;
use std::collections::HashMap;

use std::time::Instant;

fn main() {
    let test1 = file_to_string("data/test_input1.txt");
    assert!(part1(&test1, true) == 17);

    let test2 = file_to_string("data/test_input2.txt");
    assert!(part1(&test2, true) == 5);

    let test3 = file_to_string("data/test_input3.txt");
    assert!(part1(&test3, true) == 3);

    let actual = file_to_string("data/input.txt");
    let now = Instant::now();
    println!("\nPart 1: {}", part1(&actual, false));
    println!("In total, Part 1 took {}.{:03} seconds",
        now.elapsed().as_secs(),
        now.elapsed().subsec_millis()
    );
}

fn file_to_string(filename: &str) -> String {
    let mut file = File::open(filename).expect("Unable to open the file");
    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Unable to read the file");
    return contents;
}

fn print_grid(grid: &Vec<Vec<(i32, i32)>>) -> () {
    for row in grid {
        for elem in row {
            let char_idx = elem.0;
            let ascii_code = (char_idx + 96) as u8;
            let ascii_char = ascii_code as char;
            // print!("({}, {})", ascii_char, elem.1);
            print!("{}", ascii_char);
        }
        println!("");
    }
}

fn string_to_coord(input: &str) -> (i32, i32) {
    let coord_vec: Vec<i32> = (*input).split(", ")
        .map(|x| x.parse::<i32>().unwrap())
        .collect();

    return (coord_vec[0], coord_vec[1]);
}

fn part1(test_contents: &str, do_print: bool) -> i32 {
    let test_coords = test_contents.split("\n")
        .map(|x| string_to_coord(&x));

    let orig_x = test_coords.clone()
        .map(|x| x.0)
        .max()
        .unwrap() + 2;

    let expanded_x = test_coords.clone()
        .map(|x| x.0)
        .max()
        .unwrap() + 2 + 2;

    let orig_y = test_coords.clone()
        .map(|x| x.1)
        .max()
        .unwrap() + 2;

    let expanded_y = test_coords.clone()
        .map(|x| x.1)
        .max()
        .unwrap() + 2 + 2;

    let mut orig_grid = vec![
        vec![
            (0, -2); orig_x as usize
        ]; orig_y as usize
    ];

    let mut expanded_grid = vec![
        vec![
            (0, -2); expanded_x as usize
        ]; expanded_y as usize
    ];

    let expanded_test_coords = test_coords.clone()
        .map(|x| (x.0 + 1, x.1 + 1));
    
    let orig_grid_counts = populate_grid(
        &mut orig_grid,
        &test_coords.clone().collect(),
        orig_x,
        orig_y
    );

    let expanded_grid_counts = populate_grid(
        &mut expanded_grid,
        &expanded_test_coords.clone().collect(),
        expanded_x,
        expanded_y
    );

    let orig_grid_set = orig_grid_counts.iter().collect::<HashSet<_>>();
    let expanded_grid_set = expanded_grid_counts.iter().collect::<HashSet<_>>();

    let unchanged_items: HashSet<_> = orig_grid_set.intersection(&expanded_grid_set).collect();
    println!("\nUNCHANGED:");
    println!("{:?}", unchanged_items);
    if do_print == true {
        println!("\nORIG:");
        print_grid(&orig_grid);
        println!("\nEXPANDED:");
        print_grid(&expanded_grid);
        println!("\nUNCHANGED:");
        println!("{:?}", unchanged_items);
    }

    return unchanged_items.iter()
        .map(|x| *(x.1))
        .max().unwrap_or(0)
}

fn populate_grid(
    grid: &mut Vec<Vec<(i32, i32)>>,
    source_coords: &Vec<(i32, i32)>,
    max_x: i32,
    max_y: i32
) -> HashMap<i32, i32> {
    for (i, c) in source_coords.clone().iter().enumerate() {
        set_grid(&mut *grid, *c, ((i + 1) as i32, 0));
    }

    let mut coord_queue: VecDeque<(i32, i32)> = VecDeque::new();
    let mut navigated: HashSet<(i32, i32)> = HashSet::new();

    for c in source_coords.clone() {
        let adjacent_points = get_adjacent_points(&c, max_x, max_y);
        for p in adjacent_points {
            coord_queue.push_back(p);
            navigated.insert(p);
        }
    }

    while coord_queue.len() > 0 {
        let p1 = coord_queue.pop_front().unwrap();

        // All adjacent values
        let mut has_value: HashSet<i32> = HashSet::new();
        let mut set_value = (-3i32, -3i32);
        let mut min_dist = max_y + max_x;

        for p2 in get_adjacent_points(&p1, max_x, max_y) {
            let grid_value = get_grid(&grid, p2);
            // println!("p1: {:?}, p2: {:?}", p1, p2);

            // Already equidistant from something
            if grid_value.0 == -1 {
                set_value = (-1i32, grid_value.1 + 1);
                break;
            // Unseen grid cell
            } else if grid_value.1 == -2 {
                if !navigated.contains(&p2) {
                    coord_queue.push_back(p2);
                    navigated.insert(p2);
                }
            } else {
                let dist = grid_value.1 + 1;
                if dist == min_dist {
                    has_value.insert(grid_value.0);
                } else if dist < min_dist {
                    has_value.clear();
                    has_value.insert(grid_value.0);
                    min_dist = dist;
                }
            }
        }

        if has_value.len() > 1 {
            set_value = (-1i32, min_dist);
        } else if has_value.len() == 1 {
            let set_value_list: Vec<&i32> = has_value
                .iter()
                .collect();
            set_value = (*set_value_list[0], min_dist);
        }

        set_grid(&mut *grid, p1, set_value)
    }

    let mut counts = HashMap::new();
    for row in grid.clone() {
        for elem in row.clone() {
            *counts.entry(elem.0).or_insert(0) += 1;
        }
    }

    return counts;
}

fn set_grid(
    grid: &mut Vec<Vec<(i32, i32)>>,
    coord: (i32, i32),
    value: (i32, i32)
) -> () {
    grid[coord.1 as usize][coord.0 as usize] = value;
}

fn get_grid(
    grid: &Vec<Vec<(i32, i32)>>,
    coord: (i32, i32)
) -> (i32, i32) {
    return grid[coord.1 as usize][coord.0 as usize];
}

fn get_adjacent_points(
    &c: &(i32, i32),
    max_x: i32,
    max_y: i32
) -> Vec<(i32, i32)> {
    let mut adjacent_points = Vec::new();
    if c.1 + 1 < max_y {
        adjacent_points.push((c.0, c.1 + 1));
    }

    if c.1 - 1 >= 0 {
        adjacent_points.push((c.0, c.1 - 1));
    }

    if c.0 + 1 < max_x {
        adjacent_points.push((c.0 + 1, c.1));
    }

    if c.0 - 1 >= 0 {
        adjacent_points.push((c.0 - 1, c.1));
    }
    return adjacent_points;
}
