assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    res = [a+b for a in A for  b in B]
    return res

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# The two diagonal units
diag_units = [[rows[i]+cols[i] for i in range(9)]] + [[rows[8-i] + cols[i] for i in range(9)]]

# All units including the two diagonal units
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

debug = False
if debug:
    # Debugging: print all units to make sure the above variables are correct
    print(row_units)
    print(column_units)
    print(square_units)
    print(diag_units)
    print(unitlist)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    Used by the visualize_assignments method to visualize assignments
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for box1 in boxes:
        val1 = values[box1]

        if len(val1) != 2:
            continue
        for unit in units[box1]:
            twin = [peer for peer in unit if peer != box1 and values[peer] == val1]

            if len(twin):
                # Now box1 and twin are twins
                # Remove the naked twins from the possible values of their peers
                for box in unit:
                    if box not in [box1, twin[0]]:
                        for digit in val1:
                            temp = values[box].replace(digit, '')
                            assign_value(values, box, temp)
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    res = {}
    res = dict(zip(boxes, grid))
    for k in res:
        if res[k] == '.':
            res[k] = '123456789'
    return res

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[box]) for box in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)

    return

def eliminate(values):
    """
    Go through all the boxes, if a box has only a single value, remove this value from the possible values of its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    digits = '123456789'
    ones = [box for box in boxes if len(values[box]) == 1]

    for box in ones:
        for peer in peers[box]:
            temp = values[peer].replace(values[box], '')
            assign_value(values, peer, temp)

    return values
    
def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    for box in values:
        if len(values[box]) == 1:
            continue
        for unit in units[box]:
            # found = False
            peer_nums = [values[peer] for peer in unit if peer != box]
            peer_nums = ''.join(peer_nums)
            diff = set(values[box]) - set(peer_nums)

            if len(diff) == 1:
                temp = diff.pop()
                assign_value(values, box, temp)
                # found = True
                break

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate(), only_choice() and naked_twins(). If there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of all functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the Naked Twin Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def check_solved(values):
    """
    Helper function for search: checks if the sudoku is solved
    Input: A sudoku in dictionary form.
    Output: True if the sudoku is solved (all box only has one value)
    """
    solved = [box for box in boxes if len(values[box]) == 1]
    return len(solved) == 81

def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form. False if there is a box with no available values
    """

    # First, reduce the puzzle using the previous function
    res = reduce_puzzle(values)
    if not res:
        # No solution
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    min_box = None
    for box in boxes:
        if len(values[box]) > 1:
            if min_box is None or len(values[min_box]) > len(values[box]):
                min_box = box

    if min_box is None:
        if check_solved(values):
            # Then the sudoku is already fully solved
            return values
        return False

    # Now use recursion to solve each one of the resulting sudokus
    # and if one returns a value (not False), return that answer!

    cand = values[min_box]
    for digit in cand:
        values0 = values.copy()
        #values0[min_box] = digit
        assign_value(values0, min_box, digit)

        res = search(values0)
        if not res:
            continue

        if check_solved(res):
            return res

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

def test_twin():
    # A test method to verify the naked_twin method
    twin_grid = '1.4.9..68956.18.34..84.695151.....868..6...1264..8..97781923645495.6.823.6.854179'
    res = solve(twin_grid)
    display(res)

if __name__ == '__main__':
    #test_twin()

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
