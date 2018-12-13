use std::collections::HashMap;
use std::collections::VecDeque;
use std::time::Instant;

fn part1(num_players: u32, last_marble: u128) -> u128 {
    let mut circle = VecDeque::new();
    circle.push_back(0);
    let mut curr_player = 0;
    let mut player_scores: HashMap<u32, u128> = HashMap::new();
    for n in 1..(last_marble + 1) {
        if n % 23 == 0 {
            for _i in 0..7 {
                let elem = circle.pop_back().unwrap();
                circle.push_front(elem);
            }
            let removed_marble = circle.pop_back().unwrap();
            *player_scores.entry(curr_player).or_insert(0) += n + removed_marble;
            let elem = circle.pop_front().unwrap();
            circle.push_back(elem);
        } else {
            let elem = circle.pop_front().unwrap();
            circle.push_back(elem);
            circle.push_back(n);
        }
        
        curr_player = (curr_player + 1) % num_players;
    }

    return player_scores.iter()
        .map(|x| *(x.1))
        .max().unwrap();
}

fn main() {
    assert!(part1(9, 25) == 32);
    assert!(part1(10, 1618) == 8317);
    assert!(part1(13, 7999) == 146373);
    assert!(part1(17, 1104) == 2764);
    assert!(part1(21, 6111) == 54718);
    assert!(part1(30, 5807) == 37305);
    let part1_start = Instant::now();
    println!("The solution to Part 1 is: {}", part1(425, 70848));
    println!("Part 1 took {}.{:03} seconds",
        part1_start.elapsed().as_secs(),
        part1_start.elapsed().subsec_millis()
    );
    let part2_start = Instant::now();
    println!("The solution to Part 2 is: {}", part1(425, 7084800));
    println!("Part 2 took {}.{:03} seconds",
        part2_start.elapsed().as_secs(),
        part2_start.elapsed().subsec_millis()
    );
}
