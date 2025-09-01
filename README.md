# Campus Connect

A web platform for university students to discover events and join study groups. Built with Flask (Python) and Bootstrap for responsive design.

## Features

### 📅 Campus Event Management
- Create and browse university events
- Filter events by category (Academic, Social, Sports, Workshop, etc.)
- View event details including date, time, location, and organizer
- Simple event creation form

### 👥 Study Group Finder
- Create study groups for different subjects
- Join existing study groups (with member limits)
- See group members and meeting schedules
- Group leader management system

### 🔐 User Management
- Simple registration and login system
- User profiles with course and year information
- Personal dashboard showing your activities

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **Icons**: Font Awesome

## Installation & Setup

### Prerequisites
- Python 3.7+ installed
- Basic command line knowledge

### Step 1: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
# Start the development server
python app.py
```

### Step 3: Access the Platform
Open your web browser and go to: `http://localhost:5000`

## Usage Guide

### Getting Started
1. **Register**: Create a new account with your university information
2. **Login**: Sign in to access full features
3. **Explore**: Browse existing events and study groups

### Creating Events
1. Click "Create Event" from the navigation menu
2. Fill in event details (title, date, location, category)
3. Submit to make it visible to all students

### Joining Study Groups
1. Browse study groups on the "Study Groups" page
2. Click "Join Group" if there are available spots
3. You'll be added as a member and can see other participants

### Creating Study Groups
1. Click "Create Study Group" from the navigation menu
2. Set up group details (subject, meeting time, max members)
3. You automatically become the group leader
4. Other students can then join your group

## Project Structure

```
CampusConnect/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── events.html
│   └── ...
├── static/             # CSS, JS, images
│   ├── css/style.css
│   └── js/app.js
└── campus_connect.db   # SQLite database (created automatically)
```

## Database Models

### User
- Username, email, full name
- Course and year of study
- Created events and study groups

### Event
- Title, description, date/time
- Location and category
- Creator and timestamps

### StudyGroup
- Name, subject, description
- Meeting schedule and location
- Member list and capacity

## Customization Ideas

### Easy Enhancements
- Add profile pictures
- Email notifications for new events/groups
- Event RSVP system
- Study group messaging
- Search functionality

### Advanced Features
- Calendar integration
- Mobile app version
- University-specific customization
- Admin dashboard
- Analytics and reporting

## Troubleshooting

### Common Issues

1. **Module not found errors**
   - Make sure all requirements are installed: `pip install -r requirements.txt`

2. **Database errors**
   - Delete `campus_connect.db` file and restart the app to reset database

3. **Port already in use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

4. **CSS/JS not loading**
   - Clear browser cache or try hard refresh (Ctrl+Shift+R)

## Development

### Adding New Features
1. Create new routes in `app.py`
2. Add corresponding HTML templates
3. Update navigation in `base.html`
4. Test functionality

### Database Changes
- Modify models in `app.py`
- Delete existing database file to recreate schema
- For production, use proper database migrations

## Contributing

This is an educational project. Feel free to:
- Add new features
- Improve the UI/UX
- Fix bugs
- Add tests
- Improve documentation

## License

Open source - feel free to use and modify for educational purposes.

## University Problem Solving

This platform addresses several common university challenges:

- **Information Scatter**: Centralizes event information
- **Study Isolation**: Connects students with similar academic interests
- **Social Connection**: Facilitates meeting classmates and forming study partnerships
- **Time Management**: Helps students find and organize study sessions
- **Resource Sharing**: Enables collaborative learning through study groups

Perfect for universities in Africa and other regions where students need better tools for academic collaboration and campus engagement!
