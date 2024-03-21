# FastAPI Blog API

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

Welcome to the FastAPI Blog API project! This project demonstrates proficiency in building RESTful APIs with FastAPI, implementing user authentication and authorization using JWT, managing CRUD operations for blog data, implementing pagination and sorting of blog content, and following best practices for code structure and API architecture.

## Features

- User authentication and authorization using JWT
- CRUD operations for blog data (Create, Read, Update, Delete)
- Pagination and sorting of blog content
- Dockerized API deployment

## Technology Stack

- Python
- FastAPI
- Pydantic
- MongoDB
- Docker

## Project Structure

The project follows a structured folder layout:
```
root
├── config
│   └── database.py
├── models
│   └── user.py
├── routes
│   ├── authentication.py
│   └── blogs.py
├── main.py
├── docker-compose.yml
└── Dockerfile
```
# API Endpoints

## Authentication

### Register User
- **URL:** `/register`
- **Method:** POST
- **Description:** Registers a new user with the system.
- **Request Body:**
  - `username` (string, required): User's username.
  - `email` (string, required): User's email address.
  - `password` (string, required): User's password.
  - `tags` (list of strings, optional): Additional user tags.

### Generate Access Token
- **URL:** `/token`
- **Method:** POST
- **Description:** Generates an access token for user authentication.
- **Request Body:**
  - `username` (string, required): User's username.
  - `password` (string, required): User's password.
- **Response Body:**
  - `access_token` (string): JWT access token.
  - `token_type` (string): Type of token (Bearer).

### Login User
- **URL:** `/login`
- **Method:** POST
- **Description:** Logs in a user and returns an access token for authentication.
- **Request Body:**
  - `username` (string, required): User's username.
  - `password` (string, required): User's password.
- **Response Body:**
  - `access_token` (string): JWT access token.
  - `token_type` (string): Type of token (Bearer).

### Update User Profile
- **URL:** `/profile`
- **Method:** PUT
- **Description:** Updates the profile information of the authenticated user.
- **Request Body:** 
  - `email` (string, optional): New email address.
  - `full_name` (string, optional): New full name.
  - `tags` (list of strings, optional): New tags to add to user profile.

### Add Tags to User Profile
- **URL:** `/tags/add`
- **Method:** POST
- **Description:** Adds tags to the profile of the authenticated user.
- **Request Body:**
  - `tags` (list of strings): Tags to add to user profile.

### Remove Tags from User Profile
- **URL:** `/tags/remove`
- **Method:** POST
- **Description:** Removes specified tags from the profile of the authenticated user.
- **Request Body:**
  - `tags` (list of strings): Tags to remove from user profile.

## Blogs

### Create Blog
- **URL:** `/blogs/`
- **Method:** POST
- **Description:** Creates a new blog post.
- **Request Body:**
  - `title` (string): Title of the blog post.
  - `content` (string): Content of the blog post.
  - `tags` (list of strings, optional): Tags associated with the blog post.

### Retrieve All Blogs
- **URL:** `/blogs/`
- **Method:** GET
- **Description:** Retrieves all blog posts with pagination and sorting options.
- **Query Parameters:**
  - `page` (integer, optional): Page number for pagination (default: 1).
  - `page_size` (integer, optional): Number of items per page (default: 10).
  - `sort_by` (string, optional): Field to sort by (default: "created_at").
  - `sort_order` (string, optional): Sort order (asc or desc, default: "desc").

### Retrieve Blog by Title
- **URL:** `/blogs/{title}`
- **Method:** GET
- **Description:** Retrieves a specific blog post by its title.

### Update Blog by Title
- **URL:** `/blogs/{title}`
- **Method:** PUT
- **Description:** Updates a specific blog post by its title.
- **Request Body:**
  - `title` (string): New title for the blog post.
  - `content` (string): New content for the blog post.
  - `tags` (list of strings, optional): New tags associated with the blog post.

### Delete Blog by Title
- **URL:** `/blogs/{title}`
- **Method:** DELETE
- **Description:** Deletes a specific blog post by its title.

### Retrieve Blogs by User Tags
- **URL:** `/blogs/tags`
- **Method:** GET
- **Description:** Retrieves all blog posts associated with tags of the authenticated user.

