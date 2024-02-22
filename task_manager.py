"""
The Python script provides functionality for task management, user 
registration, task assignment, viewing tasks, editing tasks, generating 
task reports, and displaying statistics.
"""

# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for the task manager in VS Code
# otherwise the program will look in your root directory for the text
# files.

# =====Importing Libraries=====
import os
from datetime import datetime, date


def reg_user():
    """
    The function `reg_user` registers a new user by prompting for a 
    unique username and password, checking for existing usernames, and 
    storing the credentials in a file.
    """

    # Request new username and check that it doesn't already exist
    while True:
        new_username = input("\nNew Username: ")
        if new_username not in username_password:
            break
        print("Already in use! Please choose a different username.")

    while True:
        # Request new password
        new_password = input("\nNew Password: ")

        # Request confirm password
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same
        if new_password == confirm_password:

            # If they are the same, add them to the user dictionary and
            # .txt file
            print("New user added.")
            username_password[new_username] = new_password

            with open("user.txt", "w", encoding="utf-8") as out_file:
                user_data = []
                for key, value in username_password.items():
                    user_data.append(f"{key};{value}")
                out_file.write("\n".join(user_data))

            break

        # Otherwise print relevant message
        print("Passwords do not match.")


def add_task():
    """
    The `add_task` function in Python prompts the user to input details 
    of a task, validates the input, and adds the task to a list and a 
    text file.
    """

    # Request username of person to whom this task will be assigned and
    # check that it exists
    while True:
        task_username = input("\nName of person assigned to task: ")
        if task_username in username_password:
            break
        print("User does not exist. Please enter a valid username.")

    # Request title and description of task
    task_title = input("Title of task: ")
    task_description = input("Description of task: ")

    # Request due date and ensure it is in correct format
    while True:
        try:
            task_due_date = input("\nDue date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date,
                                              DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified.")

    # Retrieve the current date
    curr_date = date.today()

    # Add the data to the task list and the .txt file
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    update_task_file()
    print("Task successfully added.")


def view_all():
    """
    The `view_all` function prints all tasks with an identifying number 
    and a message if there are no tasks.
    """

    # Print all tasks with an identifying number
    for task_id, task in enumerate(task_list):
        print_task(task_id, task)

    # If there are no tasks, print relevant message and break out of
    # loop
    if not task_list:
        print("\nThere are no tasks currently.")


def view_mine():
    """
    The `view_mine` function allows a user to view and interact with 
    tasks assigned to them, including marking tasks as complete and 
    editing tasks if they are not already completed.
    """

    while True:
        # Print all tasks assigned to the current user and add task ids
        # to a list
        my_task_ids = []
        for task_id, task in enumerate(task_list):
            if task["username"] == curr_user:
                print_task(task_id, task)
                my_task_ids.append(task_id)

        # If no tasks are assigned, print relevant message and break out
        # of loop
        if not my_task_ids:
            print("\nYou have no tasks assigned.")
            break

        # Request a selection from the user
        task_choice = input("""\nTo select a task, type the task ID.
Or for the main menu, type '-1'.
: """)

        # If selection is one of the user's assigned tasks, provide
        # options for the user to choose
        if task_choice.isnumeric() and int(task_choice) in my_task_ids:
            print_task(task_choice, task_list[int(task_choice)])
            while True:
                user_choice = input("""\nSelect one of the following options:
m - Mark as complete
e - Edit task
t - Select a different task
: """).lower()

                if user_choice == "m":

                    # Mark task as complete and update task file
                    # accordingly
                    task_list[int(task_choice)]["completed"] = True
                    update_task_file()
                    print("Task marked as complete.")
                    break

                if user_choice == "e" and not \
                        task_list[int(task_choice)]["completed"]:

                    # Run edit function and - when completed - update
                    # task file accordingly
                    edit_task(task_list[int(task_choice)])
                    update_task_file()
                    break

                if user_choice == "e":

                    # If task is already completed, print relevant
                    # message
                    print("Task completed - unavailable for editing.")
                    break

                if user_choice == "t":

                    # If user changes their mind, break out of loop
                    break

                print("Invalid input - please try again.\n")

        # If -1 is selected, break out of loop to return to main menu
        elif task_choice == "-1":
            break

        else:
            print("Invalid input - please try again.")


def print_task(task_id, task: dict):
    """
    The function `print_task` takes a task ID and a dictionary 
    representing a task, then prints formatted information about the 
    task.
    
    :param task_id: The `task_id` parameter is the identifier or unique 
    number associated with a specific task. It is used to distinguish 
    one task from another in a task management system or similar 
    application
    :param task: The `task` parameter is a dictionary containing 
    information about a specific task. It likely includes keys such as 
    "title", "username", "assigned_date", "due_date", and "description" 
    to store details about the task. The function `print_task` takes 
    this dictionary along with a `task
    :type task: dict
    """

    # Build a string which displays all the task information
    disp_str = f"Task: \t\t {task["title"]}\n"
    disp_str += f"Assigned to: \t {task["username"]}\n"
    disp_str += ("Date Assigned: \t "
                 f"{task["assigned_date"].strftime(DATETIME_STRING_FORMAT)}\n")
    disp_str += ("Due Date: \t "
                 f"{task["due_date"].strftime(DATETIME_STRING_FORMAT)}\n")
    disp_str += f"Task Description: \n {task["description"]}"

    # Print this information along with corresponding task id
    print("_ " * 50)
    print(f"\nTask ID: {task_id}\n" + disp_str)
    print("_ " * 50)


def edit_task(task: dict):
    """
    The function `edit_task` allows the user to reassign a task to a 
    different user or edit the due date of the task.
    
    :param task: The provided code snippet defines a function 
    `edit_task` that allows the user to edit specific details of a task 
    stored in a dictionary. The function prompts the user to select an 
    editing option ('r' for reassigning the task or 'd' for editing the 
    due date) and then performs the option.
    :type task: dict
    """

    while True:
        # Request a selection from the user
        edit_choice = input("""\nSelect one of the following options:
r - Reassign task
d - Edit due date
: """).lower()

        if edit_choice == "r":
            while True:
                # Request username to whom the task will be reassigned
                # and check that it exists
                new_user = input("\nEnter the new username for this task: ")

                if new_user in username_password:

                    # Update dictionary for this task
                    task["username"] = new_user
                    print(f"Task reassigned to {new_user}.")
                    break

                # If username doesn't exist, print relevant message
                print("Username doesn't exist! Please try again.")
            break

        if edit_choice == "d":

            # Request new due date and ensure it is in correct format
            while True:
                try:
                    new_date = input("\nNew due date of task (YYYY-MM-DD): ")
                    new_date_time = \
                        datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                    break

                except ValueError:
                    print("Invalid datetime format. Please use the format "
                          "specified.")

            # Update dictionary for this task
            task["due_date"] = new_date_time
            print("Due date successfully updated.")
            break

        print("Invalid input - please try again.")


def update_task_file():
    """
    The function `update_task_file` writes task information to a text 
    file in a specific format.
    """

    with open("tasks.txt", "w", encoding="utf-8") as file:

        # For each task, create an attributes list containing
        # information for the .txt file
        task_list_to_write = []
        for task in task_list:
            str_attrs = [
                task["username"],
                task["title"],
                task["description"],
                task["due_date"].strftime(DATETIME_STRING_FORMAT),
                task["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task["completed"] else "No"
            ]

            # Join the attributes with semi-colons and add this string
            # to a new list
            task_list_to_write.append(";".join(str_attrs))

        # Write the string for each task on a separate line in the .txt
        # file
        file.write("\n".join(task_list_to_write))


def gen_task_overview():
    """
    The function `gen_task_overview` generates a summary of task 
    completion status and writes it to a text file.
    """

    # Set variables to 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    # For each task, update variables accordingly
    for task in task_list:
        if task["completed"]:
            completed_tasks += 1
        elif datetime.today() > task["due_date"]:
            uncompleted_tasks += 1
            overdue_tasks += 1
        else:
            uncompleted_tasks += 1

    # Retrieve the total number of tasks
    total_tasks = len(task_list)

    # Calculate percentages for each variable
    try:
        pc_complete = (completed_tasks / total_tasks) * 100
        pc_incomplete = (uncompleted_tasks / total_tasks) * 100
        pc_overdue = (overdue_tasks / total_tasks) * 100

    # If there are no tasks at all, set all percentages to 0
    except ZeroDivisionError:
        pc_complete = pc_incomplete = pc_overdue = 0

    # Write information to .txt file
    date_time = datetime.today().strftime(DATETIME_STRING_FORMAT + " %H:%M")

    with open("task_overview.txt", "w", encoding="utf-8") as report_file:
        report_file.write("TASK OVERVIEW\n" + date_time + "\n" + "_" * 13 +
                          "\n")
        report_file.write(f"\nTotal number of tasks = {total_tasks}")
        report_file.write("\nTotal number of completed tasks = "
                          f"{completed_tasks} ({pc_complete:.1f}%)")
        report_file.write("\nTotal number of uncompleted tasks = "
                          f"{uncompleted_tasks} ({pc_incomplete:.1f}%)")
        report_file.write(f"\nTotal number of overdue tasks = {overdue_tasks} "
                          f"({pc_overdue:.1f}%)")


def gen_user_overview():
    """
    The function `gen_user_overview` generates a detailed overview of 
    tasks assigned to each user, including completion status and 
    overdue tasks, and writes this information to a text file.
    """

    # Retrieve the total number of users and tasks
    total_users = len(username_password)
    total_tasks = len(task_list)

    # Write general information to .txt file
    date_time = datetime.today().strftime(DATETIME_STRING_FORMAT + " %H:%M")

    with open("user_overview.txt", "w", encoding="utf-8") as report_file:
        report_file.write("USER OVERVIEW\n" + date_time + "\n" + "_" * 13 +
                          "\n")
        report_file.write(f"\nTotal number of users = {total_users}")
        report_file.write(f"\nTotal number of tasks = {total_tasks}")

        # Perform calculations for each user
        for current_user in sorted(username_password):

            # Create a list of tasks assigned to the current user in the
            # loop
            user_task_list = [task for task in task_list if task["username"]
                              == current_user]

            # Retrieve total number of tasks for that user
            user_total_tasks = len(user_task_list)

            # Set variables to 0
            completed_tasks = 0
            uncompleted_tasks = 0
            overdue_tasks = 0

            # For each task, update variables accordingly
            for user_task in user_task_list:
                if user_task["completed"]:
                    completed_tasks += 1
                elif datetime.today() > user_task["due_date"]:
                    uncompleted_tasks += 1
                    overdue_tasks += 1
                else:
                    uncompleted_tasks += 1

            # Calculate percentages for each variable
            try:
                pc_assigned = (user_total_tasks / total_tasks) * 100
                pc_completed = (completed_tasks / user_total_tasks) * 100
                pc_uncompleted = (uncompleted_tasks / user_total_tasks) * 100
                pc_overdue = (overdue_tasks / user_total_tasks) * 100

            # If user has no tasks assigned, set all percentages to 0
            except ZeroDivisionError:
                pc_assigned = pc_completed = pc_uncompleted = pc_overdue = 0

            # Write specific information for current user in loop to
            # .txt file
            report_file.write(f"\n\n> {current_user}")
            report_file.write("\nNumber of tasks assigned: "
                              f"{user_total_tasks} ({pc_assigned:.1f}%)")
            report_file.write("\nNumber of assigned tasks completed: "
                              f"{completed_tasks} ({pc_completed:.1f}%)")
            report_file.write("\nNumber of assigned tasks uncompleted: "
                              f"{uncompleted_tasks} ({pc_uncompleted:.1f}%)")
            report_file.write("\nNumber of assigned tasks overdue: "
                              f"{overdue_tasks} ({pc_overdue:.1f}%)")


def create_taskfile():
    """
    The function `create_taskfile` creates a new file named "tasks.txt" 
    if it does not already exist.
    """

    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8"):
            pass


def create_userfile():
    """
    The function `create_userfile` creates a text file named "user.txt" 
    with default user credentials if the file does not already exist.
    """

    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding="utf-8") as default_file:
            default_file.write("admin;password")


def count_lines(file):
    """
    The function `count_lines` takes a file as input and returns the 
    number of non-empty lines in the file.
    
    :param file: The `count_lines` function you provided takes a file 
    object as input and counts the number of non-empty lines in the 
    file. The function iterates over each line in the file and 
    increments the `num_lines` counter if the line is not empty (i.e., 
    not equal to "\n")
    :return: The function `count_lines` returns the number of non-empty
    lines in the file.
    """

    num_lines = 0
    for line in file:
        if line != "\n":
            num_lines += 1
    return num_lines


def display_stats():
    """
    The `display_stats` function reads the number of users and tasks 
    from text files and displays the statistics.
    """

    # Create tasks.txt and user.txt if they don't exist
    create_userfile()
    create_taskfile()

    # Count number of users and tasks listed in the .txt files
    with open("user.txt", "r", encoding="utf-8") as users:
        num_users = count_lines(users)

    with open("tasks.txt", "r", encoding="utf-8") as tasks:
        num_tasks = count_lines(tasks)

    # Display statistics
    print("\n-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")


DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
create_taskfile()

# Retrieve task information from the .txt file
with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []

# Reorganise each task string in the task data list into a dictionary
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t["username"] = task_components[0]
    curr_t["title"] = task_components[1]
    curr_t["description"] = task_components[2]
    curr_t["due_date"] = datetime.strptime(task_components[3],
                                           DATETIME_STRING_FORMAT)
    curr_t["assigned_date"] = datetime.strptime(task_components[4],
                                                DATETIME_STRING_FORMAT)
    curr_t["completed"] = task_components[5] == "Yes"

    # Add dictionary to a task list
    task_list.append(curr_t)

# =====Login Section=====
# This code reads usernames and password from the user.txt file to allow
# a user to login

# If no user.txt file, write one with a default account
create_userfile()

# Read in user data
with open("user.txt", 'r', encoding="utf-8") as user_file:
    login_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in login_data:
    username, password = user.split(';')
    username_password[username] = password

# Request login information from user
LOGGED_IN = False
while not LOGGED_IN:
    print("\nLOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")

    # Check that username exists
    if curr_user not in username_password:
        print("User does not exist")
        continue

    # Check that password matches
    if username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue

    # If checks pass, exit loop
    print("Login Successful!")
    LOGGED_IN = True

while True:
    # Present the menu to the user and request selection
    menu = input('''\nSelect one of the following options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == "r":
        reg_user()

    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine()

    elif menu == "gr":
        gen_task_overview()
        gen_user_overview()
        print("\nReports generated in local directory.")

    elif menu == "ds":
        if curr_user == "admin":

            # If the user is an admin they can display statistics about
            # number of users and tasks
            display_stats()

        else:

            # Otherwise, print relevant message
            print("\nYou must be an administrator to access statistics.")

    elif menu == "e":
        print("\nGoodbye!\n")
        break

    else:
        print("Invalid input - please try again.")
