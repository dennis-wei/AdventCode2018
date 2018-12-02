use std::io::prelude::*;
use std::fs::File;

use std::collections::HashMap;

use std::time::Instant;

fn main() {
    let now = Instant::now();
    let mut file = File::open("data/input.txt").expect("Unable to open the file");
    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Unable to read the file");
    let ids: Vec<&str> = contents.split("\n").collect();
    println!("There are {} IDs", ids.len());

    let frequencies = ids.clone().into_iter().map(|x| get_char_frequency(x));
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
    println!("The answer to Part 1 is {}\n", num_with_three * num_with_two);

    let num_chars = ids[0].chars().count();
    println!("Each ID is {} chars", num_chars);

    for i in 0..num_chars {
        let reduced_ids = ids.clone().into_iter().map(|x| remove_char(x.to_string(), i)).collect();
        let contains_dupe_result: (bool, String) = contains_dupe(reduced_ids);
        match contains_dupe_result {
            (true, x) => {
                println!("Answer to Part 2: common elements are {}\n", x);
                break
            },
            (false, _) => continue
        }
    }

    println!("In total, took {}.{:03} seconds", now.elapsed().as_secs(), now.elapsed().subsec_millis());
}

fn remove_char(orig_str: String, idx: usize) -> String {
    let mut new_str: String = orig_str.clone();
    new_str.remove(idx);
    return new_str;
}

fn contains_dupe(ids: Vec<String>) -> (bool, String) {
    let mut substr_counts: HashMap<String, u32> = HashMap::new();
    for id in ids.into_iter() {
        *substr_counts.entry(id).or_insert(0) += 1
    }

    let repeated: Vec<&String> = substr_counts.iter().filter(|x| *(x.1) == 2).map(|x| x.0).collect();
    if repeated.len() > 0 {
        return (true, repeated[0].to_string());
        // return (false, "".to_string());
    } else {
        return (false, "".to_string());
    }

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
