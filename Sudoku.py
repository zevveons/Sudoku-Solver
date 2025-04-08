import random
from typing import List, Dict, Set, Optional, Tuple, Union 


#SudokuSolver works!
class SudokuSolver:
    DIGITS = '123456789'
    ROWS = 'ABCDEFGHI'
    COLS = DIGITS

    def __init__(self):
        self.CELLS = self.cross(self.ROWS, self.COLS)
        self.UNITS = ([self.cross(self.ROWS, c) for c in self.COLS] +
                      [self.cross(r, self.COLS) for r in self.ROWS] +
                      [self.cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
        self.UNITS_OF = {cell: [unit for unit in self.UNITS if cell in unit] for cell in self.CELLS}
        self.PEERS = {cell: set(sum(self.UNITS_OF[cell], [])) - {cell} for cell in self.CELLS}

    def cross(self, A: str, B: str) -> List[str]:
        return [a + b for a in A for b in B]

    def grid_to_dict(self, grid: str) -> Dict[str, str]:
        chars = [c for c in grid if c in self.DIGITS or c in '0.']
        assert len(chars) == 81
        return dict(zip(self.CELLS, chars))

    def dict_to_grid(self, values: Dict[str, str]) -> str:
        return ''.join(values.get(cell, '.') for cell in self.CELLS)

    def dict_to_2d_array(self, values: Dict[str, str]) -> List[List[int]]:
        array = [[0 for _ in range(9)] for _ in range(9)]
        for cell, val in values.items():
            if val in self.DIGITS:
                row = self.ROWS.index(cell[0])
                col = self.COLS.index(cell[1])
                array[row][col] = int(val)
        return array

    def array_2d_to_dict(self, array: List[List[int]]) -> Dict[str, str]:
        values = {}
        for i, row in enumerate(array):
            for j, val in enumerate(row):
                cell = self.ROWS[i] + self.COLS[j]
                values[cell] = str(val) if val != 0 else '.'
        return values

    def pretty_print(self, grid_2d: List[List[int]]):
        for i, row in enumerate(grid_2d):
            line = ''
            for j, num in enumerate(row):
                cell = str(num) if num != 0 else '.'
                line += cell + ' '
                if j == 2 or j == 5:
                    line += '| '
            print(line.strip())
            if i == 2 or i == 5:
                print('------+-------+------')

    def solve(self, grid: str, count_techniques: bool = False) -> Optional[Union[Dict[str, str], Tuple[Dict[str, str], Set[str]]]]:
        values = self.grid_to_dict(grid)
        techniques_used = set()

        def count_technique(technique: str):
            if count_techniques:
                techniques_used.add(technique)

        def get_candidates(cell: str) -> Set[str]:
            if values[cell] in self.DIGITS:
                return {values[cell]}
            used_digits = {values[peer] for peer in self.PEERS[cell] if values[peer] in self.DIGITS}
            return set(self.DIGITS) - used_digits

        def eliminate() -> bool:
            changed = False
            for cell in self.CELLS:
                if values[cell] in self.DIGITS:
                    continue
                candidates = get_candidates(cell)
                if len(candidates) == 1:
                    values[cell] = candidates.pop()
                    count_technique("elimination")
                    changed = True
                elif not candidates:
                    return False  
            return changed

        def naked_singles() -> bool:
            changed = False
            for cell in self.CELLS:
                if values[cell] in self.DIGITS:
                    continue
                candidates = get_candidates(cell)
                if len(candidates) == 1:
                    values[cell] = candidates.pop()
                    count_technique("naked_single")
                    changed = True
            return changed

        def hidden_singles() -> bool:
            changed = False
            for unit in self.UNITS:
                for digit in self.DIGITS:
                    possible_cells = [cell for cell in unit if digit in get_candidates(cell)]
                    if len(possible_cells) == 1:
                        cell = possible_cells[0]
                        if values[cell] != digit:
                            values[cell] = digit
                            count_technique("hidden_single")
                            changed = True
            return changed

        def naked_pairs() -> bool:
            changed = False
            for unit in self.UNITS:
                unsolved = [cell for cell in unit if values[cell] not in self.DIGITS]
                candidates = {cell: get_candidates(cell) for cell in unsolved}
                
                for cell1 in unsolved:
                    if len(candidates[cell1]) != 2:
                        continue
                    for cell2 in unsolved:
                        if cell1 == cell2 or candidates[cell1] != candidates[cell2]:
                            continue
                        pair_digits = candidates[cell1]
                        for peer in (set(unit) - {cell1, cell2}):
                            peer_digits = get_candidates(peer)
                            if not peer_digits.isdisjoint(pair_digits):
                                for d in pair_digits:
                                    if d in peer_digits:
                                        get_candidates(peer).remove(d)
                                        changed = True
                        if changed:
                            count_technique("naked_pair")
                            return True
            return changed

        def is_valid() -> bool:
            for cell in self.CELLS:
                val = values[cell]
                if val in self.DIGITS:
                    for peer in self.PEERS[cell]:
                        if values[peer] == val:
                            return False
            return True

        def backtrack() -> bool:
            unfilled = [cell for cell in self.CELLS if values[cell] not in self.DIGITS]
            if not unfilled:
                return True
            
            cell = min(unfilled, key=lambda c: len(get_candidates(c)))
            for digit in sorted(get_candidates(cell)):
                values[cell] = digit
                if backtrack():
                    return True
                values[cell] = '.'
            return False

        for cell in self.CELLS:
            if values[cell] not in self.DIGITS:
                values[cell] = '.'

        changed = True
        while changed:
            changed = False
            changed |= eliminate()
            changed |= naked_singles()
            changed |= hidden_singles()
            changed |= naked_pairs()

        if not is_valid():
            return None

        if any(values[cell] not in self.DIGITS for cell in self.CELLS):
            count_technique("backtracking")
            if not backtrack():
                return None

        if count_techniques:
            return values, techniques_used
        return values



#Sudoku Solver Example working!
if __name__ == "__main__":
    solver = SudokuSolver()

    # Input grid as a string
    puzzle = (
        ".3..7...."
        "6..195..."
        ".98...6.."
        "8...6...3"
        "4..8.3..1"
        "7...2...6"
        ".6....28."
        "...419..5"
        "....8..7."
    )

    print("Puzzle:")
    solver.pretty_print(solver.dict_to_2d_array(solver.grid_to_dict(puzzle)))

    result = solver.solve(puzzle, count_techniques=True)

    if result:
        solution, techniques = result
        print("\nSolution:")
        solver.pretty_print(solver.dict_to_2d_array(solution))
        print("\nTechniques Used:", techniques)
    else:
        print("\nNo solution found.")