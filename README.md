# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked_twins method works by the deduction that if there are two boxes with the
same two possible values in a unit, then one of the box must have one of the value and the other box
has the other value. This means we can remove these two values from possible values of their peer boxes.
We hence add the naked_twins function call to the reduce_puzzle method, after calls to the eliminate
and only_choice. This way, the DFS starts with a large search space (each box has many possible values),
applies local constraints enforced by the three techniques (elimination, only choice, naked twins) to reduce the search space.
As we enforce each constraint in sequence, other parts of the board are affected and have new constraints. This works
in a loop until the board is stalled and no longer updates boxes. And when it's stalled and if no solution is found,
the DFS backs up the search tree and tries the next possible value for a box.
This ends when the puzzle is solved or when it found no solution exists (return False).

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The way we solve the diagonal sudoku is almost the same as the regular one. So answer above still
 applies. The only difference is that we expand the unitlist to include two diagonal units.
 By doing so, when the program executes the three techniques, it automatically checks that row,
 column, square, diagonals requirements are all satisfied.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

