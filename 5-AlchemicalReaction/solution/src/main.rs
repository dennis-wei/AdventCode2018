use std::io::prelude::*;
use std::fs::File;
use std::time::Instant;

fn main() {
    let test_string1 = "Aa";
    assert!(part1(&test_string1) == 0);
    assert!(part2(&test_string1) == 0);

    let test_string2 = "cAa";
    assert!(part1(&test_string2) == 1);
    assert!(part2(&test_string2) == 0);

    let test_string3 = "AbBa";
    assert!(part1(&test_string3) == 0);
    assert!(part2(&test_string3) == 0);

    let test_string4 = "abAB";
    assert!(part1(&test_string4) == 4);
    assert!(part2(&test_string4) == 0);

    let test_string5= "aabAAB";
    assert!(part1(&test_string5) == 6);
    assert!(part2(&test_string5) == 0);

    let test_string6 = "dabAcCaCBAcCcaDA";
    assert!(part1(&test_string6) == 10);
    assert!(part2(&test_string6) == 4);

    let mut file = File::open("data/input.txt").expect("Unable to open the file");
    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Unable to read the file");

    let part1_now = Instant::now();
    println!("Part 1: {}", part1(&contents));

    println!("In total, Part 1 took {}.{:03} seconds",
                part1_now.elapsed().as_secs(),
                part1_now.elapsed().subsec_millis()
    );

    let part2_now = Instant::now();

    println!("\nPart 2: {}", part2(&contents)); 

    println!("In total, Part 2 took {}.{:03} seconds",
                part2_now.elapsed().as_secs(),
                part2_now.elapsed().subsec_millis()
    );
}

fn part1(input: &str) -> usize {
    return implode_and_count_string(&input, &'_');
}

fn part2(input: &str) -> usize {
    let mut min = input.len();
    for c_code in 65..91 {
        let as_u8 = c_code as u8;
        let remove_char = as_u8 as char;
        let char_res = implode_and_count_string(&input, &remove_char);
        if char_res < min {
            min = char_res;
        }
    }

    return min;
}

fn implode_and_count_string(input: &str, remove: &char) -> usize {
    let chars = input.chars();
    let mut stack: Vec<char> = Vec::new();

    for c in chars {
        if c == *remove || (c as u8 - 32) == (*remove as u8) {
            continue;
        } else if stack.len() == 0 {
            stack.push(c);
        } else if equal_and_polar(&c, &stack[stack.len() - 1]) {
            stack.pop();
        } else {
            stack.push(c);
        }
    }

    return stack.len();
}

fn equal_and_polar(left_char: &char, right_char: &char) -> bool {
    let left_ascii_code: u8 = *left_char as u8;
    let right_ascii_code: u8 = *right_char as u8;

    return left_ascii_code + 32 == right_ascii_code ||
            left_ascii_code - 32 == right_ascii_code;
}