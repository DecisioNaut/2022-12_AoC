from typing import Tuple, List


def read_data(file: str) -> Tuple[List[str]]:

    raw_elves_moves, raw_my_moves = [], []

    with open("./puzzles/day_02/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            moves = line.strip().split()
            raw_elves_moves.append(moves[0])
            raw_my_moves.append(moves[1])

    return raw_elves_moves, raw_my_moves


def translate_elves_moves(raw_elves_moves: List[str]) -> List[str]:
    elves_moves = []
    for raw_elves_move in raw_elves_moves:
        if raw_elves_move == "A":
            elves_moves.append("Rock")
        elif raw_elves_move == "B":
            elves_moves.append("Paper")
        elif raw_elves_move == "C":
            elves_moves.append("Scissors")
        else:
            raise ValueError(raw_elves_move)
    return elves_moves


def translate_my_moves(raw_my_moves: List[str]) -> List[str]:
    my_moves = []
    for raw_my_move in raw_my_moves:
        if raw_my_move == "X":
            my_moves.append("Rock")
        elif raw_my_move == "Y":
            my_moves.append("Paper")
        elif raw_my_move == "Z":
            my_moves.append("Scissors")
        else:
            raise ValueError(raw_my_move)
    return my_moves


def calculate_score(elves_move: str, my_move: str) -> int:
    if my_move == "Rock":
        if elves_move == "Rock":
            return 1 + 3
        elif elves_move == "Paper":
            return 1 + 0
        elif elves_move == "Scissors":
            return 1 + 6
        else:
            raise ValueError(elves_move)
    elif my_move == "Paper":
        if elves_move == "Rock":
            return 2 + 6
        elif elves_move == "Paper":
            return 2 + 3
        elif elves_move == "Scissors":
            return 2 + 0
        else:
            raise ValueError(elves_move)
    elif my_move == "Scissors":
        if elves_move == "Rock":
            return 3 + 0
        elif elves_move == "Paper":
            return 3 + 6
        elif elves_move == "Scissors":
            return 3 + 3
        else:
            raise ValueError(elves_move)
    else:
        raise ValueError(my_move)


def main():
    raw_elves_moves, raw_my_moves = read_data("part_1_data.txt")
    print("raw_elves_moves", raw_elves_moves)
    print("raw_my_moves", raw_my_moves)

    elves_moves = translate_elves_moves(raw_elves_moves)
    my_moves = translate_my_moves(raw_my_moves)

    print("raw_elves_moves", elves_moves)
    print("raw_my_moves", my_moves)

    scores = []

    for elves_move, my_move in zip(elves_moves, my_moves):

        score = calculate_score(elves_move, my_move)
        print(elves_move, my_move, score)

        scores.append(score)

    print("Total score", sum(scores))


if __name__ == "__main__":
    main()
