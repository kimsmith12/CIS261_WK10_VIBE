# CIS261_WK10_VIBE

## Student Grade Calculator

This workspace contains `StudentGradeCalculator.py`, a Python program that manages student records.

### How to run

1. Open a terminal in `/workspaces/CIS261_WK10_VIBE`.
2. Run:
   ```bash
   python3 StudentGradeCalculator.py
   ```
3. Use the menu to:
   - add new students
   - display all student records
   - view class statistics
   - search by student name
   - save records
4. Press `ESC` to exit and save automatically.

### Data file format

The program loads and saves records from `student_grades.txt` using pipe-delimited lines.
Each line uses the format:

```
name|id|test1|test2|test3|average|grade
```

Scores and averages are formatted with 2 decimal places.

### Example session

1. Run the program:
   ```bash
   python3 StudentGradeCalculator.py
   ```
2. Choose `1` to add a student.
3. Enter values when prompted:
   - Student name
   - Student ID
   - Test 1 score
   - Test 2 score
   - Test 3 score
4. Choose `2` to display all students.
5. Choose `3` for class statistics.
6. Choose `4` to search by name.
7. Press `ESC` to save and exit.

### Expected display output

When you choose option `2`, the program prints a table like this:

```
Name                 ID            Test 1   Test 2   Test 3   Average   Grade
--------------------------------------------------------------------------
Alice Johnson        S001          88.50    92.00    79.25     86.58       B
```

### Sample file

A sample `student_grades.txt` file has been included for reference.
