Necessary features:
1. Login and Registration
2. Ability to create multiple ToDo lists, and add tasks in each list
3. Ability to edit (edit the name of the list) and delete lists
4. Ability to edit/delete individual tasks in a list
5. Ability to change status of a task in a list, i.e. done/not done

Additional features:
1. Option to reset password (use question/answers instead of eamil)
2. Add GitHub Actions to run tests on pushes and pull requests
3. Add GitHub Actions to test docker build of the app

databases needed:
1. Userdb: for user registration and login
- id (primary key, unique, not null)
- username (varchar, length 16)
- password (varchar, length 32)
-> for reset password, create a Questionsdb that will contain an id and
    a corresponding question
-> then, can create a MemorableAnswerdb that will contain user_id,
    question_id, and answer (varchar, length 128)

2. ToDoListdb: for info on to do lists
- id (primary key, unique, not null)
- user_id (foreign key): to map ownership of todo lists with users
- list_name (varchar 16)

3. Tasksdb: for info on individual tasks
- id (primary key, unique, not null)
- todolist_id (foreign key): to map which task belongs to which list
- task_text (varchar, length 128)
- status (bool)
