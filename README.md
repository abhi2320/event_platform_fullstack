# Event Management Platform

### Overview

This full-stack event management platform enables users to create, manage, and view events with real-time updates. It provides user authentication, event creation tools, and live attendee updates. The platform is deployed using free-tier hosting services.


Live Demo

Frontend (React.js): [Event Management Platform](https://event-platform-fullstack.vercel.app/login)

Backend (Flask): [Event API](https://event-platform-fullstack.onrender.com)

GitHub Repository: [GitHub Repo](https://github.com/abhi2320/event_platform_fullstack)


### Features

Frontend (React.js)

Secure user authentication with JWT-based login and registration

Event dashboard displaying upcoming and past events

Event creation with title, description, date, and time

Real-time attendee list updates via WebSockets

Fully responsive design optimized for desktop and mobile devices

### Backend (Flask + MongoDB Atlas)

JWT-based authentication system

Complete CRUD operations for event management with user validation

WebSockets for real-time attendee updates using Flask-SocketIO

MongoDB Atlas as the primary database for scalability and performance


### Deployment

Frontend: Hosted on Vercel

Backend: Hosted on Render

Database: Managed with MongoDB Atlas

WebSockets: Real-time updates using Flask-SocketIO and Socket.IO on React

## Installation & Setup

### Clone the Repository

git clone https://github.com/abhi2320/event_platform_fullstack.git
cd event_platform_fullstack

### Backend Setup (Flask)

cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

Create a .env file inside backend/ with the following:

MONGO_URI=<your-mongodb-uri>
JWT_SECRET=<your-secret-key>

Run the Flask server:
python app.py

### Frontend Setup (React.js)
cd frontend
npm install


Create a .env file inside frontend/ with the following:

REACT_APP_BACKEND_URL=https://event-platform-fullstack.onrender.com


Run the React application:

npm start

### Deployment Steps

## Frontend Deployment (Vercel)

Push the frontend code to GitHub.

Connect the repository to Vercel.

Set REACT_APP_BACKEND_URL=https://event-platform-fullstack.onrender.com in Vercel Environment Variables.

Deploy the application.

## Backend Deployment (Render)

Push the backend code to GitHub.

Connect the repository to Render.

Set environment variables (MONGO_URI, JWT_SECRET) in Render Environment Variables.

Deploy the application.

### Future Improvements

Better UI/UX

Integration of Google OAuth for authentication

Support for event image uploads using Cloudinary

Advanced event filtering and search functionality

Implementation of a dark mode toggle