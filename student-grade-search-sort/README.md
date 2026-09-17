# Student Grade Search & Sort System

Algorithm Design & Analysis course project, written in Java.

You enter a list of students with their scores, and the program searches and
sorts them using three classic algorithms, then compares how they perform.

1. Shows the original unsorted list
2. Finds a score with **Linear Search** on the unsorted list
3. Sorts the students by score with **Bubble Sort** (with early exit if no swaps happen)
4. Finds the same score with **Binary Search** on the sorted list
5. Prints a table comparing Big-O complexity and measured execution time

## Files

- `Student.java` – student data (name and score)
- `SortSearch.java` – bubble sort, linear search and binary search
- `Main.java` – user input, output and the performance comparison

## How to run

```
javac -d out src/Hadi1231/*.java
java -cp out Hadi1231.Main
```
