🚑 Emergency Response System (SOS Alert)

An AI-powered emergency response platform designed to accelerate accident reporting and rescue efforts.Built with React (Frontend), Flask (Backend API), and MongoDB (Database), the system supports real-time location sharing, injury reporting, and accident scene analysis for both Emergency Responders and Ambulance Drivers.

🌟 Key Features

SOS Button: Instantly alert emergency services with your location.

Accident Scene Reporting: Upload images and describe accident scenarios.

Emergency Responder View:

See real-time alerts with accident severity assessment.

View reported injuries and location on a map.

Ambulance Driver View:

Navigate to accident sites with live updates.

View injury reports and critical accident details.

Smart Injury Analysis: Automatically assess accident severity based on uploaded data.

🏐 Tech Stack

Frontend

Backend

Database

ReactJS

Flask

MongoDB Atlas

Frontend: React 18, TailwindCSS, React Router

Backend: Python Flask API with location & image processing

Database: MongoDB for real-time accident and user data

🖥️ Project Views

SOS Button View

Accident Report View

Emergency Responder Dashboard







📸 Add your screenshots inside a /screenshots/ folder in your repo.

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/your-username/sos-emergency-system.git
cd sos-emergency-system

2. Frontend Setup (React)

cd frontend
npm install
npm run dev

Runs locally on http://localhost:5173

3. Backend Setup (Flask)

cd backend
pip install -r requirements.txt
python app.py

Runs locally on http://localhost:5000

4. Environment Variables

Create .env files in frontend and backend directories.

Frontend (frontend/.env)

VITE_API_URL=http://localhost:5000

Backend (backend/.env)

MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key

📚 API Endpoints

Method

Endpoint

Description

POST

/api/sos

Send SOS alert with location & injury details

GET

/api/alerts

Fetch active SOS alerts

POST

/api/upload

Upload accident scene image

GET

/api/alerts/:id

Get accident details by ID

📈 Future Enhancements

AI-based injury severity detection from images

Real-time ambulance location tracking

SMS/Call API integration for non-app users

Admin panel for monitoring all incidents

🤝 Contributing

Pull requests are welcome!For major changes, please open an issue first to discuss what you would like to change.

📄 License

This project is licensed under the MIT License.See the LICENSE file for details.
