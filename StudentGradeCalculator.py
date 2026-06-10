#!/usr/bin/env python3
"""
Student Grade Calculator

Program purpose:
- Manage student records including test scores and calculated grades.

Data structure:
- Option A: list of dictionaries.
- Each record stores: name, id, test1, test2, test3, average, grade.

File format:
- Pipe-delimited records saved in student_grades.txt.
- Format: name|id|test1|test2|test3|average|grade

This program uses a list of dictionaries so each student record is easy to
format, save, and load from a pipe-delimited text file.
"""
import os
import sys
import termios
import tty
from typing import Any, Dict, List

DATA_FILE = "student_grades.txt"


def getch() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def calculate_average(scores: List[float]) -> float:
    return round(sum(scores) / len(scores), 2)


def letter_grade(avg: float) -> str:
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def load_records() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []

    records: List[Dict[str, Any]] = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Skipping malformed line {line_number} in {DATA_FILE}.")
                    continue
                name, student_id, t1, t2, t3, avg, grade = parts
                try:
                    records.append({
                        "name": name,
                        "id": student_id,
                        "test1": float(t1),
                        "test2": float(t2),
                        "test3": float(t3),
                        "average": float(avg),
                        "grade": grade,
                    })
                except ValueError:
                    print(f"Skipping invalid numeric data on line {line_number}.")
                    continue
    except OSError as error:
        print(f"Error loading records from {DATA_FILE}: {error}")
    return records


def save_records(records: List[Dict[str, Any]]) -> None:
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            for record in records:
                file.write(
                    f"{record['name']}|{record['id']}|"
                    f"{record['test1']:.2f}|{record['test2']:.2f}|{record['test3']:.2f}|"
                    f"{record['average']:.2f}|{record['grade']}\n"
                )
    except OSError as error:
        print(f"Error saving records to {DATA_FILE}: {error}")


def input_score(prompt: str) -> float:
    while True:
        user_input = input(prompt).strip()
        try:
            score = float(user_input)
            if 0 <= score <= 100:
                return round(score, 2)
            print("Enter a score between 0 and 100.")
        except ValueError:
            print("Invalid number. Please enter a valid score.")


def add_student(records: List[Dict[str, Any]]) -> None:
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    student_id = input("Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return

    test1 = input_score("Test 1 score: ")
    test2 = input_score("Test 2 score: ")
    test3 = input_score("Test 3 score: ")
    average = calculate_average([test1, test2, test3])
    grade = letter_grade(average)

    records.append({
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade,
    })
    print(f"Added {name}: average = {average:.2f}, grade = {grade}")


def display_students(records: List[Dict[str, Any]]) -> None:
    if not records:
        print("No student records to display.")
        return

    header = f"{'Name':20} {'ID':12} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>9} {'Grade':>7}"
    print(header)
    print("-" * len(header))
    for record in records:
        print(
            f"{record['name'][:20]:20} {record['id'][:12]:12} "
            f"{record['test1']:8.2f} {record['test2']:8.2f} {record['test3']:8.2f} "
            f"{record['average']:9.2f} {record['grade']:7}"
        )


def class_statistics(records: List[Dict[str, Any]]) -> None:
    if not records:
        print("No records available for statistics.")
        return

    averages = [record["average"] for record in records]
    highest = max(averages)
    lowest = min(averages)
    class_avg = round(sum(averages) / len(averages), 2)

    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average: {lowest:.2f}")
    print(f"Class average: {class_avg:.2f}")


def search_student(records: List[Dict[str, Any]]) -> None:
    query = input("Search name (case-insensitive): ").strip().lower()
    if not query:
        print("Search term cannot be empty.")
        return

    matches = [record for record in records if query in record["name"].lower()]
    if not matches:
        print("No matches found.")
        return

    print(f"Found {len(matches)} match(es):")
    display_students(matches)


def main() -> None:
    records = load_records()
    print(f"Loaded {len(records)} record(s) from {DATA_FILE}.")

    while True:
        print("\nStudent Grade Calculator")
        print("1) Add new student record")
        print("2) Display all students")
        print("3) Class statistics")
        print("4) Search student by name")
        print("5) Save records")
        print("Press ESC to exit and save")
        print("Choose an option: ", end="", flush=True)

        choice = getch()
        if choice == "\x1b":
            print("\nExiting and saving records...")
            save_records(records)
            break

        print(choice)
        if choice == "1":
            add_student(records)
        elif choice == "2":
            display_students(records)
        elif choice == "3":
            class_statistics(records)
        elif choice == "4":
            search_student(records)
        elif choice == "5":
            save_records(records)
            print("Records saved.")
        else:
            print("Invalid option. Please choose 1-5 or press ESC to exit.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Saving records...")
        try:
            save_records(load_records())
        except Exception:
            pass
        print("Goodbye.")
