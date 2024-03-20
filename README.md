[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/TId9PLV9)

# Bank App API

The Bank App API provides backend functionality for managing user accounts, transactions, authentication, and registration in a banking application.

## Features

- **User Authentication:** Allows users to log in securely using their email and password.
- **User Registration:** Enables new users to create accounts by providing their username, email, and password.
- **User Profile Management:** Provides endpoints for retrieving, updating, and deleting user profiles.
- **Account Management:** Allows users to view their account details, create new accounts, and update or delete existing accounts.
- **Transaction Management:** Supports transaction initiation, retrieval of transaction details, and updates to transaction records.

## Routes

### User Authentication Routes
- `/login`: Renders the login page and handles user login requests.
- `/logout`: Logs out the currently authenticated user.

### User Registration Routes
- `/register`: Renders the registration page and handles user registration requests.

### User Management Routes
- `/users/me`: Retrieves the authenticated user's profile information.
- `/users/<user_id>`:
  - `PUT`: Updates the authenticated user's profile.
  - `DELETE`: Deletes the authenticated user's profile.

### Account Management Routes
- `/accounts`: 
  - `GET`: Retrieves the user's accounts.
  - `POST`: Creates a new account.
- `/accounts/<account_id>`:
  - `GET`: Retrieves details of a specific account.
  - `PUT`: Updates details of a specific account.
  - `DELETE`: Deletes a specific account.

### Transaction Management Routes
- `/transactions`:
  - `GET`: Retrieves transaction details.
  - `POST`: Initiates a new transaction.
- `/transactions/<transaction_id>`:
  - `PUT`: Updates details of a specific transaction.

## Authentication
- Authentication is required for certain routes using Flask-Login to manage user sessions.

## Data Protection
- Passwords are hashed using bcrypt for enhanced security.

## Error Handling
- Proper error handling is implemented to provide informative responses for various scenarios.

