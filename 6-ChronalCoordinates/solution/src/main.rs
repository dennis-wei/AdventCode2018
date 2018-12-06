extern crate itertools;

use std::io::prelude::*;
use std::fs::File;
use std::collections::VecDeque;
use std::collections::HashSet;
use std::collections::HashMap;
use itertools::Itertools;

use std::time::Instant;

fn main() {
    let mut test_file = File::open("data/test_input.txt").expect("Unable to open the file");
    let mut test_contents = String::new();
    test_file.read_to_string(&mut test_contents).expect("Unable to read the file");
    assert!(part1(&test_contents) == 17);

    // let mut file = File::open("data/input.txt").expect("Unable to open the file");
    // let mut contents = String::new();
    // file.read_to_string(&mut contents).expect("Unable to read the file");
    let now = Instant::now();
    // println!("Part 1: {}", part1(&contents));
    println!("\nIn total, Part 1 took {}.{:03} seconds",
        now.elapsed().as_secs(),
        now.elapsed().subsec_millis()
    );
}

fn print_grid(grid: &Vec<Vec<(i32, i32)>>) -> () {
    for row in grid {
        for elem in row {
            let char_idx = elem.0;
            let ascii_code = (char_idx + 96) as u8;
            let ascii_char = ascii_code as char;
            print!("{}", ascii_char)
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

fn get_taxi_cab(p1: (i32, i32), p2: (i32, i32)) -> i32 {
    let x_dist = (p1.0 - p2.0).abs();
    let y_dist = (p1.1 - p2.1).abs();
    return x_dist + y_dist;
}

fn part1(test_contents: &str) -> i32 {
    let test_coords = test_contents.split("\n")
        .map(|x| string_to_coord(&x));

    let max_taxicab = test_coords.clone().combinations(2)
        .map(|x| get_taxi_cab(x[0], x[1]))
        .max()
        .unwrap();
    
    println!("max_taxicab: {}", max_taxicab);

    let max_x = test_coords.clone()
        .map(|x| x.0)
        .max()
        .unwrap() + 1;
            // + 2 * max_taxicab;

    let bounded_x = test_coords.clone()
        .map(|x| x.0)
        .max()
        .unwrap() + 1;
    
    let max_y = test_coords.clone()
        .map(|x| x.1)
        .max()
        .unwrap() + 1;
            // + 2 * max_taxicab;

    let bounded_y = test_coords.clone()
        .map(|x| x.1)
        .max()
        .unwrap() + 1;


    println!("max_x: {}, max_y: {}", max_x, max_y);
    println!("bounded_x: {}, bounded_y: {}", bounded_x, bounded_y);
    let mut grid = vec![
        vec![
            (0, 0); max_x as usize
        ]; max_y as usize
    ];

    // let new_test_coords = test_coords.clone()
    //     .map(|x| (x.0 + max_taxicab, x.1 + max_taxicab));

    let new_test_coords = test_coords.clone()
        .map(|x| (x.0, x.1));

    // let mut items_touched = 0;
    for (i, c) in new_test_coords.clone().enumerate() {
        // println!("adding {}, {}, {} to grid", i + 1, c.0, c.1);
        set_grid(&mut grid, c, ((i + 1) as i32, 0));
        // items_touched = i + 1;
    }

    let mut coord_queue: VecDeque<(i32, i32)> = VecDeque::new();
    let mut navigated: HashSet<(i32, i32)> = HashSet::new();
    
    for c in new_test_coords.clone() {
        let adjacent_points = get_adjacent_points(&c, max_x, max_y);
        for p in adjacent_points {
            coord_queue.push_back(p);
            navigated.insert(p);
        }
    }

    while coord_queue.len() > 0 {
        let p1 = coord_queue.pop_front().unwrap();
        println!("Handling {:?}", p1);
        // items_touched += 1;
        // println!("items_touched: {}", items_touched);
        let mut has_value: HashSet<i32> = HashSet::new();
        let mut set_value = (-2i32, -2i32);
        let mut min_dist = max_y + max_x;

        for p2 in get_adjacent_points(&p1, max_x, max_y) {
            let grid_value = get_grid(&grid, p2);
            if p1.0 == 0 && p1.1 == 4 {
                has_value = HashSet::new();
                println!("{:?}: {:?}", p2, grid_value);
            }
            if grid_value.0 == -1 {
                set_value = (-1i32, grid_value.1 + 1);
                break;
            } else if grid_value.0 != 0 {
                let dist = grid_value.1 + 1;
                if dist == min_dist {
                    has_value.insert(grid_value.0);
                } else if dist < min_dist {
                    has_value = HashSet::new();
                    has_value.insert(grid_value.0);
                    min_dist = dist;
                }
            } else {
                if !navigated.contains(&p2) {
                    println!("Adding {:?} to queue", p2);
                    coord_queue.push_back(p2);
                    navigated.insert(p2);
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

        println!("Setting distance of {}", set_value.1);
        set_grid(&mut grid, p1, set_value)
    }

    println!("");
    print_grid(&grid);

    let mut counts = HashMap::new();
    for row in grid.clone() {
        for elem in row.clone() {
            *counts.entry(elem.0).or_insert(0) += 1;
        }
    }

    let best_area = counts.iter()
        .filter(|x| *(x.1) < bounded_x * bounded_y)
        .filter(|x| *(x.0) > 0)
        .map(|x| x.1)
        .max().unwrap(); 

    println!("{:?}", counts);
    return *best_area;
}

fn set_grid(
    grid: &mut Vec<Vec<(i32, i32)>>,
    coord: (i32, i32),
    value: (i32, i32)
) -> () {
    // println!("{:?}", coord);
    grid[coord.1 as usize][coord.0 as usize] = value;
}

fn get_grid(
    grid: &Vec<Vec<(i32, i32)>>,
    coord: (i32, i32)
) -> (i32, i32) {
    // println!("{:?}", coord);
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