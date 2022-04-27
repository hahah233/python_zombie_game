"""
Sliding Puzzle Game
Assignment 1
Semester 1, 2021
CSSE1001/CSSE7030
"""



# Replace these <strings> with your name, student number and email address.
__author__ = "<zhe Sun>, <46676243>"
__email__ = "<s4667624@student.uq.edu.au>"

from a1_support import *
from typing import Optional, List

def swap_position(puzzle:str,from_index:int,to_index:int) -> str:
    """
    Swap the position of the elements in the puzzle string by the parameters.
    
    Parameters:
        puzzle (str): the str to be swapped the position.
        from_index (int),to_index (int): the number of elements to be swapped.
    
    Returns:
        (str): a str have been swapped position from puzzle.
    """
    temp = list(puzzle)
    temp[from_index],temp[to_index] = temp[to_index],temp[from_index]
    swapped_position = ''.join(temp)# Turn the list into a string
    return swapped_position

def shuffle_puzzle(solution: str) -> str:
    """
    Shuffle a puzzle solution to produce a solvable sliding puzzle.

    Parameters:
        solution (str): a solution to be converted into a shuffled puzzle.

    Returns:
        (str): a solvable shuffled game with an empty tile at the
                   bottom right corner.

    References:
        - https://en.wikipedia.org/wiki/15_puzzle#Solvability
        - https://www.youtube.com/watch?v=YI1WqYKHi78&ab_channel=Numberphile

    Note: This function uses the swap_position function that you have to
              implement on your own. Use this function when the swap_position
              function is ready
    """
    shuffled_solution = solution[:-1]

    # Do more shuffling for bigger puzzles.
    swaps = len(solution) * 2
    for _ in range(swaps):
        # Pick two indices in the puzzle randomly.
        index1, index2 = random.sample(range(len(shuffled_solution)), k=2)
        shuffled_solution = swap_position(shuffled_solution, index1, index2)
    return shuffled_solution + EMPTY
        
def check_win(puzzle: str, solution: str) -> bool:
    """
    Check if you win in the game by compare the puzzle and solution.
    
    Parameters:
        puzzle (str),solution (str): two strs to be compared.
    
    Returns:
        (True) If the last element of puzzle is the same as the solution or 
          empty, and the other elements are both the same.
        (False) Other situations.
    """
    i=len(puzzle)-1
    if puzzle[i] == ' ' or puzzle[i] == solution[i]:
        while i != 0:
            i -= 1
            if puzzle[i] != solution[i]:
                return False
        return True
    else:
        return False                        

def move(puzzle: str, direction: str) -> Optional[str]:
    """
    Move the puzzle by the direction.
    
    Parameters:
        puzzle (str): a str that have a empty to be moved.
        direction (str): The direction of the empty to move.
    
    Returns:
        (str): if users can move the empty by the direction in a size*size
         grid,return the str that be moved.
        (None): can't move the empty in the grid. 
    """
    size = int(len(puzzle)**0.5)
    temp = list(puzzle)
    for i in range(len(puzzle)):
        if list(puzzle)[i] == ' ':
            emp = i # the position of the empty in the list
    # Move empty up
    if direction == 'U':
        if emp-size in range(size**2):
            temp[emp],temp[emp-size] = temp[emp-size],temp[emp]
            return(''.join(temp))
    # Move empty down
    elif direction == 'D':
        if emp+size in range(size**2):
            temp[emp],temp[emp+size] = temp[emp+size],temp[emp]
            return(''.join(temp))
    # Move empty left
    elif direction == 'L':
        if (emp-1)//size == emp//size:
            temp[emp],temp[emp-1] = temp[emp-1],temp[emp]
            return(''.join(temp))
    # Move empty right
    elif direction == 'R':
        if (emp+1)//size == emp//size:
            temp[emp],temp[emp+1] = temp[emp+1],temp[emp]
            return(''.join(temp))

def print_grid(puzzle:str) -> None:
    """
    Transform the str to a grid by changing the elements in it.
    
    Parameters:
        puzzle (str): a str have 'size**2' characters.
    """
    size=int(len(puzzle)**0.5)
    print(CORNER,size*(3*HORIZONTAL_WALL+CORNER),sep = '')
    list_puzzle=list(puzzle)
    # change the elements in the list
    for i in range(len(list_puzzle)):
        list_puzzle[i]=VERTICAL_WALL + EMPTY + list_puzzle[i] + EMPTY
    # print the elements seperately
    for i in range(0,len(puzzle),size):
        print(''.join(list_puzzle[i:i+size])+ VERTICAL_WALL,sep = '')
        print(CORNER,size*(3*HORIZONTAL_WALL + CORNER),sep = '')

def print_entire(solution:str,puzzle:str) -> None:
    """
    Print the introductions and the two grids
     
    Parameters:
      solution(str): the solution of the game
      puzzle (str): a str to be moved the empty to make it is same as
        the solution 
    """
    print('Solution:')
    print_grid(solution)
    print('\nCurrent position:')
    print_grid(puzzle)
    print() 

def operation(solution:str,puzzle:str) -> None:
    """
    The specific operating body: Users can move the empty in the puzzle
      to make the two grids are the same except for the empty or ask 
        for help or give up the game.
    """
    x = input(DIRECTION_PROMPT)
    # Ask for help
    if x == 'H':
        print(HELP_MESSAGE)
        print_entire(solution,puzzle)
        operation(solution,puzzle)
    # Move the empty in a grid
    elif x == 'U'or x == 'D'or x == 'L'or x == 'R':
        # Empty change position
        puzzle_moved=move(puzzle,x)
        # Empty change position
        if puzzle_moved is not None:
            print_entire(solution,puzzle_moved)
            if check_win(puzzle_moved,solution) == True:
                print(WIN_MESSAGE)
                end()
            else:
                operation(solution,puzzle_moved)
        # Empty doesn't change
        else:
            print(INVALID_MOVE_FORMAT.format(x))
            print_entire(solution,puzzle)
            operation(solution,puzzle)
    # Give up the game
    elif x == 'GU':
        print(GIVE_UP_MESSAGE)
        end()
    # Invalid input
    else:
        print(INVALID_MESSAGE)
        print_entire(solution,puzzle)
        operation(solution,puzzle)

def start_game() -> None:
    """
    The start of the game, generate two grids( one is the solution 
      of the game and another is a puzzle). 
    """
    size = int(input(BOARD_SIZE_PROMPT))
    solution = get_game_solution('words.txt',size)
    puzzle = shuffle_puzzle(solution)
    print_entire(solution,puzzle)
    if check_win(puzzle,solution) == True:
        print(WIN_MESSAGE)
        end()
    else:
        operation(solution,puzzle)

def end() -> None:
    """
    The process after the game: ask the player if they want to play again
    """
    x=input(PLAY_AGAIN_PROMPT)  
    if x =='Y' or x == 'y' or x == '':
        start_game()
    else:
        print(BYE)

def main():
    """
    Welcome the user and start the game
    """
    print(WELCOME_MESSAGE)
    start_game()

if __name__ == '__main__':
    main()