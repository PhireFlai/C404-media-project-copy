# API Documentation

## URL: /api/signup/
### Method: POST

### When the API endpoint should be used
- Use this endpoint to register a new user.

### How the API endpoint should be used
- Send a POST request to `/api/signup/` with the new user's data in the request body.

### Why the API endpoint should or should not be used
- Use this endpoint to register a new user.

### Request
- **Method**: POST
- **URL**: `/api/signup/`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: 
  ```json
  {
    "username": "existingUser",
    "password": "securePassword"
  }
  ```

### JSON Fields in Response
- **id**: `string` (UUID) - The unique identifier of the author.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the author.
- **token**: `string` - The token of the current session
  - **Example**: `777f47dec51c104ccde9476ed3f4fab7370e07b`
  - **Purpose**: Authenication for the user login
- **username**: `string` - The username of the author.
  - **Example**: `Testuser`
  - **Purpose**: The display name of the author.

### Example
```bash
POST /api/login/
-H "Content-Type: application/json"
-d '{
      "username": "existingUser",
      "password": "securePassword"
    }'
```
#### Response
```bash 
{"token":"a777f47dec51c104ccde9476ed3f4fab7370e07b",
"user_id":"04f511c8-5cfe-4414-a125-e4a879188d38",
"username":"newUser"}
```
## URL: /api/login/
### Method: POST

### When the API endpoint should be used
- Use this endpoint to log in an existing user.

### How the API endpoint should be used
- Send a POST request to `/api/login/` with the user's credentials in the request body.

### Why the API endpoint should or should not be used
- Use this endpoint to log in an existing user.

### Request
- **Method**: POST
- **URL**: `/api/login/`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: 
  ```json
  {
    "username": "existingUser",
    "password": "securePassword"
  }
  ```
### JSON Fields in Response
- **id**: `string` (UUID) - The unique identifier of the author.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the author.
- **token**: `string` - The token of the current login session
  - **Example**: `777f47dec51c104ccde9476ed3f4fab7370e07b`
  - **Purpose**: Authenication for the user login
- **username**: `string` - The username of the author.
  - **Example**: `Testuser`
  - **Purpose**: The display name of the author.

### Example
```bash
POST /api/login/
-H "Content-Type: application/json"
-d '{
      "username": "existingUser",
      "password": "securePassword"
    }'
```
#### Response
```bash 
{
    "token":"a777f47dec51c104ccde9476ed3f4fab7370e07b",
    "user_id":"04f511c8-5cfe-4414-a125-e4a879188d38",
    "username":"newUser"
}
```

## URL: /api/authors/
### Method: GET
### Description: Retrieve a list of all authors.

### When the API endpoint should be used
- Use this endpoint when you need to fetch a list of all authors in the system.

### How the API endpoint should be used
- Send a GET request to `/api/authors/`.

### Why the API endpoint should or should not be used
- Use this endpoint to get a comprehensive list of all authors, including their basic information such as username, email, profile picture

### Request
- **Method**: GET
- **URL**: `/api/authors/`
- **Headers**: None required

### JSON Fields in Response
- **id**: `string` (UUID) - The unique identifier of the author.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the author.
- **username**: `string` - The username of the author.
  - **Example**: `Testuser`
  - **Purpose**: The display name of the author.
- **profile_picture**: `string` (URL) - The URL to the author's profile picture.
  - **Example**: `http://127.0.0.1:8000/media/profile_pictures/1493e30c-b8a6-467b-b78e-cb76529a040f.png`
  - **Purpose**: The profile picture of the author.


### Example
```bash
GET /api/authors/
```
### Response
```bash
[
    {
        "id": "d2d7dea6-5708-40a5-b89a-324b89b226d9",
        "username": "Testuser",
        "profile_picture": null,

    },
    {
        "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
        "username": "admin",
        "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/1493e30c-b8a6-467b-b78e-cb76529a040f.png",

    },
    # ... More user objects
]
```


## URL: /api/authors/{AUTHOR_SERIAL}/
### Method: GET, PUT
### Description: Retrieve a given user based on their AUTHOR_SERIAL id or update their information

### When the API endpoint should be used
- **GET**: Use this endpoint to retrieve the profile information of a specific author.
- **PUT**: Use this endpoint to update the profile information of a specific author.

### How the API endpoint should be used
- **GET**: Send a GET request to `/api/authors/{AUTHOR_SERIAL}/` with the author's UUID.
- **PUT**: Send a PUT request to `/api/authors/{AUTHOR_SERIAL}/` with the author's UUID and the updated profile data in the request body. currently only supports usernames

### Why the API endpoint should or should not be used
- **GET**: Use this endpoint to fetch the profile information of a specific author.
- **PUT**: Use this endpoint to update the profile information of a specific author. The user must be authenticated and authorized.

### Request
#### GET
- **Method**: GET
- **URL**: `/api/authors/{AUTHOR_SERIAL}/`
- **Headers**: None required

#### PUT
- **Method**: PUT
- **URL**: `/api/authors/{AUTHOR_SERIAL}/`
- **Headers**: 
  - `Authorization: Token yourToken`
  - `Content-Type: application/json`
- **Body**: 
  ```json
  {
    "newUsername": "updatedUsername"
  }
  ```
  
### JSON Fields in Response
- **id**: `string` (UUID) - The unique identifier of the author.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the author.
- **username**: `string` - The username of the author.
  - **Example**: `Testuser`
  - **Purpose**: The display name of the author.
- **profile_picture**: `string` (URL) - The URL to the author's profile picture.
  - **Example**: `http://127.0.0.1:8000/media/profile_pictures/1493e30c-b8a6-467b-b78e-cb76529a040f.png`
  - **Purpose**: The profile picture of the author.


### Example 1
```bash
GET /api/authors/123e4567-e89b-12d3-a456-426614174000/
```
#### Response
```bash
{
    "id": "d2d7dea6-5708-40a5-b89a-324b89b226d9",
    "username": "Testuser",
    "profile_picture": null,
},
```

### Example 2
```bash
PUT /api/authors/123e4567-e89b-12d3-a456-426614174000/
-H "Authorization: Token yourToken"
-H "Content-Type: application/json"
-d '{
      "newUsername": "updatedUsername"
    }'
```
#### Response
```bash
{
  "message": "Username updated successfully"
}
```


## URL: /api/authors/{userId}/update-picture/
### Method: PUT
### View: updateUserProfile
### Name: update-user-profile

### When the API endpoint should be used
- Use this endpoint to update the profile picture of a specific author.

### How the API endpoint should be used
- Send a PUT request to `/api/authors/{userId}/update-picture/` with the author's UUID and the new profile picture in the request body.

### Why the API endpoint should or should not be used
- Use this endpoint to update the profile picture of a specific author. The user must be authenticated and authorized.

### Request
- **Method**: PUT
- **URL**: `/api/authors/{userId}/update-picture/`
- **Headers**: 
  - `Authorization: Token yourToken`
  - `Content-Type: multipart/form-data`
- **Body**: 
  ```form-data
  {
    "profile_picture": "path/to/new/profile_picture.jpg"
  }
  ```

### JSON Fields in Response
- **message**: `string` - informs the client whether the request was sucessful.
  - **Example**: `Profile picture updated successfully`
  - **Purpose**: informs the user of the success of updating the image
  
### Example 1
```bash
PUT /api/authors/123e4567-e89b-12d3-a456-426614174000/update-picture/
-H "Authorization: Token yourToken"
-H "Content-Type: multipart/form-data"
-F "profile_picture=@path/to/new/profile_picture.jpg"
```

#### Response
```bash
{
  "message": "Profile picture updated successfully"
}
```