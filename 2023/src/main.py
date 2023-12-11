import os
import sys
import importlib
import requests
from dotenv import load_dotenv

load_dotenv()

def get_input(day: int) -> str:
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    INPUT_FOLDER = f'{DIR_PATH}/../inputs'
    print(INPUT_FOLDER)
    
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)

    if os.path.exists(f'{INPUT_FOLDER}/day_{day}.txt'):
        return open(f'{INPUT_FOLDER}/day_{day}.txt', 'r').read()
    
    url = f'https://adventofcode.com/2023/day/{day}/input'
    session_cookie = os.getenv('AOC_SESSION')
    headers = {'User-Agent': 'github.com/rboortman/advent-python by ron@techforce1.nl'}
    
    response = requests.get(url, cookies={'session': session_cookie}, headers=headers)
    if response.status_code != 200:
        print(f'Error fetching input for day {day}.')
        sys.exit(1)
    
    input = response.text.strip()
    with open(f'{INPUT_FOLDER}/day_{day}.txt', 'w') as f:
        f.write(input)

    return input

def send_answer(day, level, answer):
    url = f'https://adventofcode.com/2023/day/{day}/answer'
    session_cookie = os.getenv('AOC_SESSION')
    headers = {'User-Agent': 'github.com/rboortman/advent-python by ron@techforce1.nl'}
    
    response = requests.post(url, cookies={'session': session_cookie}, headers=headers, data={'level': level, 'answer': answer}, allow_redirects=False)
    
    if response.status_code == 302:
        print("Answer was already submitted!")
        sys.exit(0)
    
    print(response.text)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        print('No arguments provided.')
        sys.exit(1)
    
    day_arg = args[0]
    day_arg_normalized = day_arg
    if len(args[0]) == 1:
        day_arg_normalized = '0' + day_arg_normalized

    try:
        module = importlib.import_module(f'solutions.day_{day_arg_normalized}')
    except ModuleNotFoundError:
        print(f'No module found for day {day_arg}.')
        sys.exit(1)
        
    day = module.Assignment()
    (silver, gold) = day.solve(get_input(day_arg))
    
    to_send = input("Which answer would you like to commit? (silver/gold/none) ")
    
    match to_send.strip().lower():
        case ('s' | 'silver'):
            (level, answer) = (1, silver)
        case ('g' | 'gold'):
            (level, answer) = (2, gold)
        case ('n' | 'none'):
            print("Ok, goodbye.")
            sys.exit(0)
        case _:
            print(f"'{to_send}' is an invalid option, goodbye.")
            sys.exit(0)
            
    send_answer(day_arg, level, answer)