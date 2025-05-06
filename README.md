# Student Portal

A comprehensive student portal web application built with Flask, MySQL, and Bootstrap. The system offers user authentication, profile management, grade tracking, and an innovative natural language database query interface powered by Google's Gemini AI model.

![Dashboard Screenshot](https://github.com/AdarshXKumAR/Student-Portal/blob/main/dashboard.png)

## Features

- **User Authentication System**: Secure registration and login
- **Profile Management**: Update personal information
- **Grade Tracking**: View academic performance with visual indicators
- **Natural Language Database Queries**: Ask questions about data in plain English
- **Responsive Design**: Modern UI built with Bootstrap 5
- **Security**: Password hashing, session management, and protected routes

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **AI Integration**: Google Generative AI (Gemini 1.5 Pro)
- **Security**: Werkzeug for password hashing

## Screenshots

### Home Page
![Home Page](https://github.com/AdarshXKumAR/Student-Portal/blob/main/Home.png)
*The welcoming landing page for the Student Portal*

### Login Interface
![Login](https://github.com/AdarshXKumAR/Student-Portal/blob/main/Login.png)
*Clean and secure login interface*

### User Dashboard
![Dashboard](https://github.com/AdarshXKumAR/Student-Portal/blob/main/dashboard.png)
*Personalized dashboard showing user profile and grades*

### Profile Management
![Profile](https://github.com/AdarshXKumAR/Student-Portal/blob/main/profile.png)
*Interface to update personal information*

### Natural Language Database Query
![NL Database](https://github.com/AdarshXKumAR/Student-Portal/blob/main/nl_database.png)
*Innovative interface to query the database using natural language*

### Password Management
![Change Password](https://github.com/AdarshXKumAR/Student-Portal/blob/main/password.png)
*Secure interface for password updates*

## Installation

1. **Clone the repository**
   ```
   git clone https://github.com/AdarshXKumAR/Student-Portal.git
   cd Student-Portal
   ```

2. **Create and activate a virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root with:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Set up the MySQL database**
   ```
   mysql -u root -p < database_setup.sql
   ```

6. **Run the application**
   ```
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Requirements

- Python 3.8+
- MySQL
- Google Gemini API Key

## Future Enhancements

- Course registration functionality
- Academic calendar integration
- File upload for assignments
- Notifications system
- Mobile application
- Admin dashboard

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap for the responsive UI components
- Google for the Gemini AI API
- Flask community for the excellent documentation
