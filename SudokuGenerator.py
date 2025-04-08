import random
from typing import List

class SudokuGenerator:
    def __init__(self, difficulty: str = "medium"):
        """
        :param difficulty: "easy", "medium", or "hard"
        """
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = difficulty.lower()
        
        # Set empty cells based on difficulty
        if self.difficulty == "easy":
            self.empty_cells = random.randint(36, 44)  # ~40-50% empty
        elif self.difficulty == "hard":
            self.empty_cells = random.randint(52, 60)  # ~60-70% empty
        else:  # medium
            self.empty_cells = random.randint(45, 51)  # ~50-60% empty

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Check if placing num at board[row][col] is valid"""
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def fill_board(self) -> bool:
        """Backtracking-based board filler"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid(i, j, num):
                            self.board[i][j] = num
                            if self.fill_board():
                                return True
                            self.board[i][j] = 0
                    return False
        return True

    def remove_cells(self):
        """Randomly remove cells to create a puzzle"""
        count = self.empty_cells
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i, j in positions:
            if count == 0:
                break
            if self.board[i][j] != 0:
                self.board[i][j] = 0
                count -= 1

    def generate(self) -> str:
        """Generate the puzzle and return it as a single-line string like:
        '.3..7....6..195...'"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board()
        self.remove_cells()

        # Convert to single-line string with dots for empty cells
        puzzle_str = ""
        for row in self.board:
            for val in row:
                puzzle_str += "." if val == 0 else str(val)
        return puzzle_str

    def print_puzzle(self, puzzle_str: str):
        """Print the puzzle in a readable 9x9 format"""
        for i in range(0, 81, 9):
            print(puzzle_str[i:i+9])

# Example usage
if __name__ == "__main__":
    print("Easy Puzzle:")
    easy_gen = SudokuGenerator(difficulty="easy")
    easy_puzzle = easy_gen.generate()
    easy_gen.print_puzzle(easy_puzzle)
    
    print("\nMedium Puzzle:")
    medium_gen = SudokuGenerator(difficulty="medium")
    medium_puzzle = medium_gen.generate()
    medium_gen.print_puzzle(medium_puzzle)
    
    print("\nHard Puzzle:")
    hard_gen = SudokuGenerator(difficulty="hard")
    hard_puzzle = hard_gen.generate()
    hard_gen.print_puzzle(hard_puzzle)
