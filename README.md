# fs-lima  Mentorship Platform

This is a Django-powered web application that provides a complete environment for managing a mentorship program. Users can sign up as either mentors or mentees, create profiles, and connect with each other.

-----

## ✨ Features

  * **User Authentication**: Secure user registration and login system.
  * **Profile Management**: Users can create and update their profiles. Mentees can upload profile images.
  * **`[Feature 3]`**: `[Describe another key feature of your project]`
  * **`[Feature 4]`**: `[Describe another key feature of your project]`
  * **Django Admin**: Full administrative interface to manage users, profiles, and other data.

-----

## 🛠️ Technology Stack

  * **Backend**: Python, Django
  * **Database**: SQLite3 (for development)
  * **Image Handling**: Pillow

-----

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

  * Python 3.10+
  * Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/efdourado/fs-lima.git
    cd fs-lima
    ```

2.  **Create and activate a virtual environment:**

      * On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
      * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Apply the database migrations:**

    ```bash
    python manage.py migrate
    ```

2.  **Create a superuser to access the admin panel:**

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to create your admin user.

3.  **Start the development server:**

    ```bash
    python manage.py runserver
    ```

4.  **Open your browser** and navigate to `http://127.0.0.1:8000/` to see the application running.

      * The admin panel is available at `http://127.0.0.1:8000/admin/`.