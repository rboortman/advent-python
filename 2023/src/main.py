import os
import sys
import importlib
import requests
import functools
from dotenv import load_dotenv

load_dotenv()


def get_input(day: int) -> str:
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    INPUT_FOLDER = f"{DIR_PATH}/../inputs"

    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)

    if os.path.exists(f"{INPUT_FOLDER}/day_{day}.txt"):
        return open(f"{INPUT_FOLDER}/day_{day}.txt", "r").read()
    
    print(f"{INPUT_FOLDER}/day_{day}.txt", os.path.exists(f"{INPUT_FOLDER}/day_{day}.txt"))

    url = f"https://adventofcode.com/2023/day/{day}/input"
    session_cookie = os.getenv("AOC_SESSION")
    headers = {"User-Agent": "github.com/rboortman/advent-python by ron@techforce1.nl"}

    response = requests.get(url, cookies={"session": session_cookie}, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching input for day {day}.")
        sys.exit(1)

    input = response.text.strip()
    with open(f"{INPUT_FOLDER}/day_{day}.txt", "w") as f:
        f.write(input)

    return input


def send_answer(day, level, answer):
    url = f"https://adventofcode.com/2023/day/{day}/answer"
    session_cookie = os.getenv("AOC_SESSION")
    headers = {"User-Agent": "github.com/rboortman/advent-python by ron@techforce1.nl"}

    response = requests.post(
        url,
        cookies={"session": session_cookie},
        headers=headers,
        data={"level": level, "answer": answer},
        allow_redirects=False,
    )

    if response.status_code == 302:
        print("Answer was already submitted!")
        sys.exit(0)

    print(response.text)


def print_all_answers():
    days = []
    for day in range(1, 26):
        try:
            module = importlib.import_module(f"solutions.day_{day:02}")
            days.append((module.Assignment(), get_input(day), day))
        except ModuleNotFoundError:
            continue

    solutions = [day.timed_solve(input) + (day_index,) for (day, input, day_index) in days]
    solutions = [(solution[0][0], round(solution[0][1] * 1000000)/1000, solution[1][0], round(solution[1][1] * 1000000)/1000, solution[2]) for solution in solutions]

    maxes = functools.reduce(
        lambda acc, cur: (
            max(acc[0], len(str(cur[0]))),
            max(acc[1], len(str(cur[1]))),
            max(acc[2], len(str(cur[2]))),
            max(acc[3], len(str(cur[3]))),
        ),
        solutions,
        ((0, 9, 0, 9)),
    )

    sum_maxes = sum(maxes)
    dash_size = sum_maxes + 6 + 8 + 8 - 2
    print('/' + ('-' * dash_size) + '\\')
    print(f'| Day    | {'Silver'.ljust(maxes[0], ' ')} | {'Time (ms)'.ljust(maxes[1], ' ')} | {'Gold'.ljust(maxes[2], ' ')} | {'Time (ms)'.ljust(maxes[3], ' ')} |')
    print('|' + ('-' * 8) + '+' + ('-' * (maxes[0] + 2)) + '+' + ('-' * (maxes[1] + 2)) + '+' + ('-' * (maxes[2] + 2)) + '+' + ('-' * (maxes[3] + 2)) + '|')
    for (silver, s_time, gold, g_time, day) in solutions:
        print(f'| Day {str(day).rjust(2, ' ')} | {str(silver).rjust(maxes[0], " ")} | {str(s_time).rjust(maxes[1], " ")} | {str(gold).rjust(maxes[2], " ")} | {str(g_time).rjust(maxes[3], " ")} |')
    print('\\' + ('-' * dash_size) + '/')


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print_all_answers()
        sys.exit(0)

    day_arg = args[0]
    day_arg_normalized = day_arg
    if len(args[0]) == 1:
        day_arg_normalized = '0' + day_arg_normalized

    try:
        module = importlib.import_module(f"solutions.day_{day_arg_normalized}")
    except ModuleNotFoundError:
        print(f"No module found for day {day_arg}.")
        sys.exit(1)

    day = module.Assignment()
    (silver, gold) = day.solve(get_input(day_arg))

    to_send = input("Which answer would you like to commit? (silver/gold/none) ")

    match to_send.strip().lower():
        case ("s" | "silver"):
            (level, answer) = (1, silver)
        case ("g" | "gold"):
            (level, answer) = (2, gold)
        case ("n" | "none"):
            print("Ok, goodbye.")
            sys.exit(0)
        case _:
            print(f"'{to_send}' is an invalid option, goodbye.")
            sys.exit(0)

    send_answer(day_arg, level, answer)
