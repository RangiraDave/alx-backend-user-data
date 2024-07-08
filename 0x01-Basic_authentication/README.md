# Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)




# Basic Authentication API

![](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2020/5/6ccb363443a8f301bc2bc38d7a08e9650117de7c.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240708%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240708T064247Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a908643c1614c3e16ce5bdcafe1013576616e7d24b3030380752168c2d8b405d)


## Background Context
In this project, you will learn what the authentication process means and implement a Basic Authentication on a simple API.

In the industry, you should not implement your own Basic authentication system and use a module or framework that does it for you (like in Python-Flask: Flask-HTTPAuth). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

## Resources
Read or watch:
- [REST API Authentication Mechanisms](https://www.youtube.com/watch?v=501dpx2IjGY)
- [Base64 in Python](https://docs.python.org/3/library/base64.html)
- [HTTP header Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Base64 - concept](https://en.wikipedia.org/wiki/Base64)

## Learning Objectives
At the end of this project, you are expected to be able to explain to anyone, without the help of Google:

### General
- What authentication means
- What Base64 is
- How to encode a string in Base64
- What Basic authentication means
- How to send the Authorization header

## Requirements
### Python Scripts
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

## Tasks
### 0. Simple-basic-API
- Download and start your project from this [archive.zip](https://github.com/holbertonschool/0x01-Basic_authentication/archive/main.zip)

### 1. Error handler: Unauthorized
- What the HTTP status code for a request unauthorized? 401 of course!
- Edit `api/v1/app.py`:
    - Add a new error handler for this status code, the response must be:
        - a JSON: `{"error": "Unauthorized"}`
        - status code 401
        - you must use `jsonify` from Flask
    - For testing this new error handler, add a new endpoint in `api/v1/views/index.py`:
        - Route: GET `/api/v1/unauthorized`
        - This endpoint must raise a 401 error by using `abort` - Custom Error Pages

### 2. Error handler: Forbidden
- What the HTTP status code for a request where the user is authenticated but not allowed to access a resource? 403 of course!
- Edit `api/v1/app.py`:
    - Add a new error handler for this status code, the response must be:
        - a JSON: `{"error": "Forbidden"}`
        - status code 403
        - you must use `jsonify` from Flask
    - For testing this new error handler, add a new endpoint in `api/v1/views/index.py`:
        - Route: GET `/api/v1/forbidden`
        - This endpoint must raise a 403 error by using `abort` - Custom Error Pages

### 3. Auth class
- Now you will create a class to manage the API authentication.
- Create a folder `api/v1/auth`
- Create an empty file `api/v1/auth/__init__.py`
- Create the class `Auth`:
    - in the file `api/v1/auth/auth.py`
    - import `request` from `flask`
    - class name `Auth`
    - public method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` that returns `False` - `path` and `excluded_paths` will be used later, now, you don’t need to take care of them
    - public method `def authorization_header(self, request=None) -> str:` that returns `None` - `request` will be the Flask request object
    - public method `def current_user(self, request=None) -> TypeVar('User'):` that returns `None` - `request` will be the Flask request object
    - This class is the template for all authentication systems you will implement.

### 4. Define which routes don't need authentication
- Update the method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` in `Auth` that returns `True` if the path is not in the list of strings `excluded_paths`:
    - Returns `True` if `path` is `None`
    - Returns `True` if `excluded_paths` is `None` or empty
    - Returns `False` if `path` is in `excluded_paths`
    - You can assume `excluded_paths` contains string path always ending by a `/`
    - This method must be slash tolerant: `path=/api/v1/status` and `path=/api/v1/status/` must return `False` if `excluded_paths` contains `/api/v1/status/`

### 5. Request validation!
- Now you will validate all requests to secure the API:
- Update the method `def authorization_header(self, request=None) -> str:` in `api/v1/auth/auth.py`:
    - If `request` is `None`, returns `None`
    - If `request` doesn’t contain the header key `Authorization`, returns `None`
    - Otherwise, return the value of the header `request Authorization`
- Update the file `api/v1/app.py`:
    - Create a variable `auth` initialized to `None` after the CORS definition
    - Based on the environment variable `AUTH_TYPE`, load and assign the right instance of authentication to `auth`
    - if `auth`:
        - import `Auth` from `api/v1/auth/auth`
        - create an instance of `Auth` and assign it to the variable `auth`
    - Now the biggest piece is the filtering of each request. For that, you will use the Flask method `before_request`
    - Add a method in `api/v1/app.py` to handle `before_request`
        - if `auth` is `None`, do nothing
        - if `request.path` is not part of this list `['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']`, do nothing - you must use the method `require_auth` from the `auth` instance
        - if `auth.authorization_header(request)` returns `None`, raise the error 401 - you must use `abort`
        - if `auth.current_user(request)` returns `None`, raise the error 403 - you must use `abort`

### 6. Basic auth
- Create a class `BasicAuth` that inherits from `Auth`. For the moment, this class will be empty.
- Update `api/v1/app.py` to use `BasicAuth` class instead of `Auth` depending on the value of the environment variable `AUTH_TYPE`. If `AUTH_TYPE` is equal to `basic_auth`:
    - import `BasicAuth` from `api/v1/auth/basic_auth`
    - create an instance of `BasicAuth` and assign it to the variable `auth`
    - Otherwise, keep the previous mechanism with `auth` an instance of `Auth`.

### 7. Basic - Base64 part
- Add the method `def extract_base64_authorization_header(self, authorization_header: str) -> str:` in the class `BasicAuth` that returns the Base64 part of the Authorization header for a Basic Authentication:
    - Return `None` if `authorization_header` is `None`
    - Return `None` if `authorization_header` is not a string
    - Return `None` if `authorization_header` doesn’t start with Basic (with a space at the end)
    - Otherwise, return the value after Basic (after the space)

### 8. Basic - Base64 decode
- Add the method `def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:` in the class `BasicAuth` that returns the decoded value of a Base64 string `base64_authorization_header`:
    - Return `None` if `base64_authorization_header` is `None`
    - Return `None` if `base64_authorization_header` is not a string
    - Return `None` if `base64_authorization_header` is not a valid Base64 - you can use try/except
    - Otherwise, return the decoded value as UTF8 string - you can use `decode('utf-8')`

### 9. Basic - User credentials
- Add the method `def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str)` in the class `BasicAuth` that returns the user email and password from the Base64 decoded value.
    - This method must return 2 values
    - Return `None, None` if `decoded_base64_authorization_header` is `None`
    - Return `None, None` if `decoded_base64_authorization_header` is not a string
    - Return `None, None` if `decoded_base64_authorization_header` doesn’t contain `:`
    - Otherwise, return the user email and the user password - these 2 values must be separated by a `:`

### 10. Basic - User object
- Add the method `def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User')` in the class `BasicAuth` that returns the User instance based on his email and password.


## HappyCoding!
