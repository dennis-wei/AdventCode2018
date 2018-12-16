use std::vec::Vec;
use std::time::Instant;

fn generate_recipes(recipes: &mut Vec<usize>, num_recipes: usize) -> () {
    let mut elf1_index: usize = 0;
    let mut elf2_index: usize = 1;
    while recipes.len() < num_recipes {
        let score1: usize = recipes[elf1_index];
        let score2: usize = recipes[elf2_index];
        let newscore1: usize = (score1 + score2) / 10;
        let newscore2: usize = (score1 + score2) % 10;

        if newscore1 != 0 {
            recipes.push(newscore1);
        }
        recipes.push(newscore2);

        elf1_index = (elf1_index + score1 + 1) % recipes.len();
        elf2_index = (elf2_index + score2 + 1) % recipes.len();
        // println!("After update, elf 1 is {} and elf 2 is {}", elf1_index, elf2_index)
    }
}

fn get_scores(recipes: &Vec<usize>, start_index: usize) -> usize {
    let mut agg: usize = 0;
    for i in (start_index)..(start_index + 10) {
        agg *= 10;
        // println!("Adding digit {}", recipes[i]);
        agg += recipes[i];
    }

    // println!("Final agg is {}", agg);
    return agg;
}

fn get_last_n(recipes: &Vec<usize>, n: usize) -> String {
    if recipes.len() < n {
        return String::from("");
    }
    let mut agg = String::with_capacity(n);
    for i in (recipes.len() - n)..(recipes.len()) {
        agg.push(std::char::from_digit(recipes[i] as u32, 10).unwrap());
    }

    // println!("Last n is {}", agg);

    return agg;
}

fn generate_recipes_part2(
    recipes: &mut Vec<usize>,
    input: String
) -> usize {
    let mut elf1_index: usize = 0;
    let mut elf2_index: usize = 1;
    let input_length = input.len();
    // println!("Length of {} is {}", input, input_length);
    loop {
        let score1: usize = recipes[elf1_index];
        let score2: usize = recipes[elf2_index];
        let newscore1: usize = (score1 + score2) / 10;
        let newscore2: usize = (score1 + score2) % 10;

        if newscore1 != 0 {
            recipes.push(newscore1);
            let last_n = get_last_n(recipes, input_length);
            if last_n == input {
                break;
            }
        }
        recipes.push(newscore2);
        let last_n = get_last_n(recipes, input_length);
        if last_n == input {
            break;
        }

        elf1_index = (elf1_index + score1 + 1) % recipes.len();
        elf2_index = (elf2_index + score2 + 1) % recipes.len();
        // println!("After update, elf 1 is {} and elf 2 is {}", elf1_index, elf2_index)
    }

    // println!("Found {} after {} recipes", input, recipes.len() - input_length);
    return recipes.len() - input_length;
}

fn part1(input: usize) -> usize {
    let mut recipes = vec![3, 7];
    generate_recipes(&mut recipes, input + 10);
    return get_scores(&recipes, input);
}

fn part2(input: String) -> usize {
    let mut recipes = vec![3, 7];
    return generate_recipes_part2(&mut recipes, input);
}

fn test() {
    println!("Running Tests");
    assert!(part1(9) == 5158916779);
    assert!(part1(5) == 0124515891);
    assert!(part1(18) == 9251071085);
    assert!(part1(2018) == 5941429882);
    assert!(part2(String::from("51589")) == 9);
    assert!(part2(String::from("01245")) == 5);
    assert!(part2(String::from("92510")) == 18);
    assert!(part2(String::from("59414")) == 2018);
    println!("Finished Tests\n");
}

fn main() {
    test();
    let part1_start = Instant::now();
    println!("Answer to Part 1 is: {}", part1(293801));
    println!("Part 1 took {}.{:03} seconds",
        part1_start.elapsed().as_secs(),
        part1_start.elapsed().subsec_millis()
    );
    let part2_start = Instant::now();
    println!("Answer to Part 2 is: {}", part2(String::from("293801")));
    println!("Part 2 took {}.{:03} seconds",
        part2_start.elapsed().as_secs(),
        part2_start.elapsed().subsec_millis()
    );
}
