# FASE Backend

This is the backend for FASE (Facial Attendance Security Elevation), a Wi-Fi network access point-based attendance management solution. It's built with Django and Django REST Framework.

[Check out the companion app project.](https://github.com/thecodepapaya/fase)

## Features

- **User Management**: Handles user accounts, distinguishing between students and faculty. Authentication is integrated with Firebase.
- **Course Management**: Allows creation and management of courses, including enrolling students and assigning instructors. Students can be added to courses in bulk by uploading a CSV file.
- **Attendance Tracking**: Marks attendance by capturing and verifying a student's device and network information (SSID, BSSID, IP address) against predefined course parameters.
- **Scheduled Tasks**: Uses `APScheduler` for running scheduled jobs, for managing attendance windows.
- **Data Export**: Provides functionality to generate and export attendance data, in spreadsheet formats using `pandas` and `XlsxWriter`.
- **API**: A comprehensive RESTful API for the frontend mobile application to interact with.

## Project Structure

The project is organized into several Django apps:

- `attendance/`: Handles all the logic related to marking and recording attendance.
- `authentication/`: Manages user login and authentication using Firebase.
- `course/`: Contains models and views for courses, including student enrollment.
- `registration/`: Manages the registration of student devices and captures network information.
- `users/`: Defines the custom User model and related views.
- `meta/`: Provides metadata and download links for the mobile applications.
- `fase_backend/`: The main Django project configuration.

## API Endpoints

The primary API endpoints are available under `/api/v1/`. The main resources are:

- `/api/v1/login/`: User login.
- `/api/v1/users/`: User profiles.
- `/api/v1/courses/`: Course details.
- `/api/v1/attendance/`: Attendance records.
- `/api/v1/registration/`: Device registration.
- `/api/v1/metadata/`: App metadata.
- `/api/v1/ping/`: Health check.

There are also endpoints for generating reports (`/generate/<course_id>/`) and downloading mobile clients (`/download/apk/`, `/download/ios/`).

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd fase-backend
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    - You will need to configure database settings, Firebase credentials, and other Django settings. It is recommended to use a `.env` file with `python-decouple`.

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Future Work

As per the original project plan, a Phase 2 was envisioned to improve location verification accuracy. This phase was not implemented but was planned to include:

- **BLE Mesh Network**: Using a Bluetooth Low Energy mesh network to cross-verify that students are within the physical classroom (e.g., within a 10-15m range). This would add another layer of security and accuracy to the attendance system.
