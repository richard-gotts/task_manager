# Task Manager

This program is a task manager application which has been extended and refactored from an initial simple task management system.

### Existing Features

- Login using username and password stored in .txt file
- Read in tasks from existing .txt file on startup
- Register a new user
- Add a task (username, title, description, due date, date assigned, completed)
- View all tasks
- View tasks assigned to current logged in user
- Display statistics (number of users and tasks)

### Updates

- Existing functionality moved from main body to a set of functions, improving readability
- Issue of registering duplicate users fixed
- Option to edit tasks assigned to current user (mark as complete, reassign task, change due date)
- Functionality added to automatically update .txt file with these changes
- Option to generate task overview report with data regarding the status of tasks managed by the application
- Option to generate user overview report with data regarding allocation of tasks to users registered with the application and the status of tasks managed by application for each user
- Display statistics function modified to read in information directly from .txt files
- Control flow improved for better user experience
- Code checked for style consistency and descriptive variable names
- Thorough documentation added
