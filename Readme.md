# Connectify API Documentation

This document provides an overview of the API endpoints for our application, detailing the routes and their respective functions.<br> [Click here to view the swagger docs](https://connectify-backend-t3b4.onrender.com)

## Authentication Routes

### `POST /api/v1/signup`
- **Description:** This route is used to register a new user.
<details>
<summary>Details</summary>

- **Request Body:**<br>
    **Form Data:**
  - `email` (str): Email address of the user
  - `password` (str): Password for the user
  - `username` (str): First name of the user
  - `image` (File): Image for the profile pic [Optional]
</details>

### `POST /api/v1/login`
- **Description:** This route is used to login a user.
<details>
<summary>Details</summary>
- **Request Body:**<br>
    **Form Data:**
  - `email` (str): Email address of the user
  - `password` (str): Password for the user
</details>

### `POST /api/v1/logout`
- **Description:** This route is used to logout a user.
<details>
<summary>Details</summary>

- **Authorization:** Bearer
- **Required:** Yes
</details>

### `POST /api/v1/verify`
- **Description:** Sends an email to the user with the OTP to verify the email.
<details>
<summary>Details</summary>

- **Authorization:** Bearer
- **Required:** Yes
- 
</details>

### `POST /api/v1/otp`
- **Description:** Verifies the OTP sent to the user's email.
<details>
<summary>Details</summary>

- **Authorization:** Bearer
- **Required:** Yes
- **Query Paramters**
    - `otp` (str): OTP sent to the user's email
    - `email` (str): Email of the user who received the OTP
</details>

## Google Auth

### `POST /api/v1/google/login`
- **Description:** This route is used to login a user using Google.
- **Note:** Navigate to the `/api/v1/google/login` route to login using Google as the documentation doesn't support Google OAuth.

### `POST /api/v1/google/auth`
- **Description:** This route is used for Google redirect URI.
<details>
<summary>Details</summary>

- **Note:** You don't need to navigate here.
</details>

## User Routes

### `GET /api/v1/user`
- **Description:** This route is used to retrieve a list of all users.
<details>
<summary>Details</summary>

- **Authorization:** Bearer (Optional)
- **Response Model:** `List[schemas.UserDetails]`
- **Status Code:** 200 (OK)
</details>

### `PATCH /api/v1/update/{old_email}`
- **Description:** This route is used to update a user's information.
<details>
<summary>Details</summary>

- **Authorization:** Bearer (Required)
- **Path Parameter:**
  - `old_email` (str): Current email of the user
- **Request Body:**
  - `new_email` (str): New email address for the user (optional)
- **Dependencies:**
  - `get_current_user`: Ensures the user is authenticated
  - `verify_token`: Validates the access token
- **Response Model:** `schemas.UserSignUp`
- **Status Code:** 200 (OK)
</details>

### `DELETE /api/v1/delete`
- **Description:** This route is used to delete a user.
<details>
<summary>Details</summary>


- **Authorization:** Bearer (Required)
- **Dependencies:**
  - `get_current_user`: Ensures the user is authenticated
- **Response Model:** None (empty response)
- **Status Code:** 200 (OK)
</details>

### `POST /api/v1/profile`
- **Description:** This route is used to upload a profile picture for a user.
<details>
<summary>Details</summary>

- **Authorization:** Bearer (Required)
- **Path Parameter:**
  - `email` (str): Email of the user
- **Request Body:**
  - `img` (UploadFile): Image file to upload
- **Dependencies:**
  - `get_current_user`: Ensures the user is authenticated
- **Response Model:** None (empty response)
- **Status Code:** 200 (OK)
</details>

## Friends Routes

**Authorization: Bearer (Required)**<br>
**Dependency: Depends(get_current_user)** (on all routes)

### `POST /api/v1/friends/add`
- **Description:** This route is used to send a friend request to another user.
<details>
<summary>Details</summary>

- **Request Body:**
  - `friend_email` (str): Email of the friend to add
  - `user_email` (str): Email of the current user
- **Response Model:** None (empty response)
- **Status Code:** 200 (OK)
</details>

### `POST /api/v1/friends/accept`
- **Description:** This route is used to accept a friend request.
<details>
<summary>Details</summary>

- **Request Body:**
  - `friend_email` (str): Email of the friend who sent the request
  - `user_email` (str): Email of the current user
- **Response Model:** None (empty response)
- **Status Code:** 200 (OK)
</details>

### `GET /api/v1/friends`
- **Description:** This route is used to retrieve a list of the current user's friends.
<details>
<summary>Details</summary>

- **Query Parameter (optional):**
  - `email` (str): Email of the user (to retrieve their friend list)
- **Response Model:** `List[Friend]`
- **Status Code:** 200 (OK)
</details>

### `GET /api/v1/friends/requests`
- **Description:** This route is used to retrieve a list of friend requests sent to the current user.
<details>
<summary>Details</summary>

- **Response Model:** `List[FriendRequest]`
- **Status Code:** 200 (OK)
</details>

### `DELETE /api/v1/friends/requests/remove`
- **Description:** This route is used to remove a friend request.
<details>
<summary>Details</summary>

- **Path Parameter:**
  - `friend_email` (str): Email of the friend to remove the request from
- **Query Parameter:**
  - `user_email` (str): Email of the current user
- **Response Model:** None (empty response)
- **Status Code:** 200 (OK)
</details>

### `DELETE /api/v1/friends/remove`
- **Description:** This route is used to remove a friend.
<details>
<summary>Details</summary>


- **Path Parameter:**
  - `friend_email` (str): Email of the friend to remove
- **Query Parameter:**
  - `user_email` (str): Email of the current user
- **Response Model:** None (empty response)
- **Status Code:** 200 (OK)
</details>

## Comments Routes

**Authorization: Bearer (Required)** (on all routes)

### `POST /api/v1/posts/comments/create`
- Description This route is used to create a comment on a post.
<details>
<summary>Details</summary>


- Request Body:
  - `post_id` (str): ID of the post to comment on
  - `content` (str): Content of the comment
</details>

### `GET /api/v1/posts/comments/read/{post_id}`
- **Description:** This route is used to retrieve all comments on a post.
<details>
<summary>Details</summary>


- **Path Parameter:**
  - `post_id` (str): ID of the post to retrieve comments for
</details>

### `PATCH /api/v1/posts/comments/update/{comment_id}`
- **Description:** This route is used to update a comment.
<details>
<summary>Details</summary>


- Path Parameter:
  - `comment_id` (str): ID of the comment to update
- Form Data:
  - `content` (str): New content for the comment
  - `commented_by` (str): Email of the user who commented
  - `post_id` (str): ID of the post the comment belongs to
</details>

### `DELETE /api/v1/posts/comments/delete/{comment_id}`
- **Description:** This route is used to delete a comment.
<details>
<summary>Details</summary>

- Path Parameter:
  - `comment_id` (str): ID of the comment to delete
</details>
