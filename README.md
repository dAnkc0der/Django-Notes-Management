# Django-Notes-Management

## Installation

1. Clone this repository:
    ```bash
    git clone "Link to this repo"
    ```

2. Change directory:
    ```bash
    cd Submission-Neofi
    ```

3. Create a virtual environment:
    ```bash
    python -m venv env
    ```

4. Activate the virtual environment:
    - Windows:
    ```bash
    source ./env/Scripts/activate
    ```
    - Linux/Mac:
    ```bash
    source ./env/bin/activate
    ```

5. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

6. Start the server:
    ```bash
    python manage.py runserver
    ```

7. Access the API endpoints using Postman.

## API Endpoints

### SignUp

- Registers a new user
    - **Request**: POST `localhost:8000/signup/`
    - **Body**:
        ```json
        {
            "username": "FT3",
            "password": "abcd@12345",
            "password2": "abcd@12345",
            "email": "FT3@email.com",
            "first_name": "FT",
            "last_name": "3"
        }
        ```
    - **Response**:
        ```json
        {
            "id": 25,
            "username": "FT3",
            "email": "FT3@email.com",
            "first_name": "FT",
            "last_name": "3"
        }
        ```

### Login

- Logs in a user and generates access and refresh tokens
    - **Request**: POST `localhost:8000/login/`
    - **Body**:
        ```json
        {
            "username": "FT3",
            "password": "abcd@12345"
        }
        ```
    - **Response**:
        ```json
        {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...."
        }
        ```

### Create Note

- Creates a new note for the user
    - **Request**: POST `localhost:8000/notes/create/`
    - **Body**:
        ```json
        {
            "title": "Test-1",
            "content": "Test-1 content"
        }
        ```
    - **Response**:
        ```json
        {
            "title": "Test-1",
            "content": "Test-1 content"
        }
        ```

### Get Notes

- Returns all notes saved by a user
    - **Request**: GET `localhost:8000/notes/`
    - **Response**: List of all notes

### Get Notes By ID

- Returns a single note saved by a user
    - **Request**: GET `localhost:8000/notes/id/`
    - **Response**: Returns a single note

### Share Notes

- Allows one user to share their notes with other users provided they have been given access to
    - **Request**: POST `localhost:8000/notes/share`
    - **Body**:
        ```json
        {
            "note_id": 21, 
            "shared_with_users": [24]
        }
        ```
    - **Response**: A success message

    - **Note**: `note_id` is the ID of the note created, which can be retrieved from the "get all notes" route. `shared_with_users` is the list of user IDs to share notes with, which can be retrieved when a user is created from the signup route.

### Update Notes

- Allows a user to update their notes as well as the other users that have been granted access
    - **Request**: PUT `http://localhost:8000/notes/id/update/`
    - **Body**:
        ```json
        {
            "title": "Changed title tried by 25",
            "content": "Changed content tried by 25"
        }
        ```
    - **Response**:
        ```json
        {
            "title": "Changed title tried by 25",
            "content": "Changed content tried by 25",
            "created_at": "2024-02-19T18:56:19.994570Z",
            "updated_at": "2024-02-19T19:40:33.554775Z",
            "user": 23
        }
        ```

    - **Note**: In the request, the `id` is `note_id` retrieved from "get all notes".

### Get Version History

- Returns a list of all changes made to the notes
    - **Request**: GET `localhost:8000/notes/version-history/21/`
    - **Response**:
        ```json
        [
            {
                "timestamp": "2024-02-19T19:00:02.962581Z",
                "user": "FT2",
                "changes": {
                    "title": "Changed title tried by 24",
                    "content": "Changed content tried by 24"
                }
            },
            {
                "timestamp": "2024-02-19T18:59:49.802407Z",
                "user": "FT2",
                "changes": {
                    "title": "Changed title tried by 24",
                    "content": "Changed content tried by 24"
                }
            },
            {
                "timestamp": "2024-02-19T18:58:27.589830Z",
                "user": "FT1",
                "changes": {
                    "title": "Changed title tried by 23",
                    "content": "Changed content tried by 23"
                }
            },
            {
                "timestamp": "2024-02-19T18:56:20.018571Z",
                "user": "FT1",
                "changes": {
                    "title": "Test-1",
                    "content": "Test-1 content"
                }
            }
        ]
        ```

**NOTE:** From the steps "create note" to "get version history", perform this: ```Paste the access code generated from the above step into Postman -> Authorization -> Select Type as Bearer Token -> Paste the access code into the Token field.``` 
