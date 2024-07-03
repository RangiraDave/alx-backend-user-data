# alx-backend-user-data

![meme](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2019/12/5c48d4f6d4dd8081eb48.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240703%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240703T061201Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=6a49e467cfdf47ad4eaf236c3d69aece4db041856cbcd6e73c4a20a2e13d6d9b)

## Resources

Read or watch:
- [What Is PII, non-PII, and Personal Data?](https://www.privacy.com/what-is-pii-non-pii-and-personal-data/)
- [Logging Documentation](https://docs.python.org/3/library/logging.html)
- [bcrypt Package](https://pypi.org/project/bcrypt/)
- [Logging to Files, Setting Levels, and Formatting](https://docs.python.org/3/howto/logging.html#logging-to-a-file)

## Learning Objectives

At the end of this project, you should be able to explain to anyone, without the help of Google:
- Examples of Personally Identifiable Information (PII)
- How to implement a log filter that will obfuscate PII fields
- How to encrypt a password and check the validity of an input password
- How to authenticate to a database using environment variables

## Requirements

- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All your files should end with a new line
- The first line of all your files should be exactly `#!/usr/bin/env python3`
- A `README.md` file, at the root of the folder of the project, is mandatory
- Your code should use the `pycodestyle` style (version 2.5)
- All your files must be executable
- The length of your files will be tested using `wc`
- All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
- A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
- All your functions should be type annotated

## Tasks

### 0. Regex-ing (mandatory)

Write a function called `filter_datum` that returns the log message obfuscated:

Arguments:
- `fields`: a list of strings representing all fields to obfuscate
- `redaction`: a string representing by what the field will be obfuscated
- `message`: a string representing the log line
- `separator`: a string representing by which character is separating all fields in the log line (message)

The function should use a regex to replace occurrences of certain field values.
`filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.

### 1. Log formatter (mandatory)

Update the `RedactingFormatter` class to accept a list of strings `fields` as a constructor argument.

Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for fields in `fields` should be filtered.

### 2. Create logger (mandatory)

Implement a `get_logger` function that returns a `logging.Logger` object.

The logger should be named "user_data" and only log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as the formatter.

Create a tuple `PII_FIELDS` constant at the root of the module containing the fields from `user_data.csv` that are considered PII. `PII_FIELDS` can contain only 5 fields - choose the right list of fields that are considered as "important" PIIs or information that you must hide in your logs. Use it to parameterize the formatter.

### 3. Connect to secure database (mandatory)

Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection` object).

Use the `os` module to obtain credentials from the environment.
Use the module `mysql-connector-python` to connect to the MySQL database (`pip3 install mysql-connector-python`).

### 4. Read and filter data (mandatory)

Implement a `main` function that obtains a database connection using `get_db` and retrieves all rows in the `users` table. Display each row under a filtered format.

### 5. Encrypting passwords (mandatory)

Implement a `hash_password` function that expects one string argument `password` and returns a salted, hashed password as a byte string.

Use the `bcrypt` package to perform the hashing (with `hashpw`).

### 6. Check valid password (mandatory)

Implement an `is_valid` function that expects two arguments, `hashed_password` (bytes type) and `password` (string type). Use `bcrypt` to validate that the provided password matches the hashed password.



## HappyCoding!
