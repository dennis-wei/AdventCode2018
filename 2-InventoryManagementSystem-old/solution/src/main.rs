use std::io::prelude::*;
use std::fs::File;

use std::collections::HashMap;

fn main() {
    let mut file = File::open("data/input.txt").expect("Unable to open the file");
    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Unable to read the file");
    let lines = contents.split("\n");
    let frequencies = lines.map(|x| get_char_frequency(x));
    let inv_frequencies = frequencies.map(|x| invert_frequencies(x));
    let num_with_two: u32 = inv_frequencies.clone().map(|x| match x.contains_key(&2) {
        true => 1,
        false => 0
    }).sum();
    let num_with_three: u32 = inv_frequencies.clone().map(|x| match x.contains_key(&3) {
        true => 1,
        false => 0
    }).sum();
    println!("There are {} ids with a character that occurs twice", num_with_two);
    println!("There are {} ids with a character that occurs thrice", num_with_three);
    println!("The answer to Part 1 is {}", num_with_three * num_with_two);
}

fn get_char_frequency(id: &str) -> HashMap<char, u32> {
    let mut frequency: HashMap<char, u32> = HashMap::new();
    for c in id.chars() {
        *frequency.entry(c).or_insert(0) += 1
    }
    return frequency;
}

fn invert_frequencies(freq_map: HashMap<char, u32>) -> HashMap<u32, Vec<char>> {
    let mut inv_freq_map: HashMap<u32, Vec<char>> = HashMap::new();

    for (k, v) in freq_map {
        inv_freq_map.entry(v).or_insert_with(Vec::new).push(k)
    }

    return inv_freq_map;
}
