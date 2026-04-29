# 🏥 SamaritanCare — Hospital Chatbot

> ⚠️ *This is a fictional hospital project built for educational purposes only.*

A full-stack hospital management chatbot built with Flask, Google Dialogflow, and MongoDB. Patients can register, book appointments with doctors, view their bookings, and submit feedback — all through a conversational chatbot interface.

---

## 🚀 Features

- **Patient Registration** — New patients can fill out an admission form with their personal and medical details. A unique User ID is auto-assigned.
- **Appointment Booking** — Patients can book appointments with doctors by specialty (Psychiatrist, Neurologist, Therapist) through the chatbot.
- **Doctor Selection** — The chatbot displays available doctors with their experience, specialization, and timings.
- **View Appointments** — Patients can view their past and upcoming appointments via the chatbot.
- **Feedback System** — A dedicated feedback form for patients to submit reviews.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| NLP | Google Dialogflow (Intent & Entity Detection) |
| Database | MongoDB Atlas |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Google App Engine |

---

## 📁 Project Structure

```
Demo/
│
├── static/
│   ├── script.js        # Chat widget logic
│   ├── style.css        # Chatbox styling
│   ├── doctor_1.png     # Doctor images
│   └── doctor_2.png
│
├── templates/
│   ├── base.html        # Main page with Dialogflow chat widget
│   ├── formt.html       # Patient registration form
│   ├── info.html        # Patient account info page
│   └── abc.html         # Feedback form
│
├── main.py              # Flask app & Dialogflow webhook
├── app.yaml             # Google App Engine config
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/samaritancare.git
cd samaritancare
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory based on `.env.example`:
```
MONGO_URI=your_mongodb_connection_string
DIALOGFLOW_AGENT_ID=your_dialogflow_agent_id
BASE_URL=your_deployed_app_url
```

### 4. Run the app locally
```bash
python main.py
```

The app will be available at `http://localhost:8080`

---

## 🗄️ MongoDB Collections

| Collection | Description |
|-----------|-------------|
| `user` | Stores patient registration details and appointments |
| `doctor` | Stores doctor profiles, specializations, and timings |
| `Sess` | Tracks active Dialogflow session and user mapping |
| `Feedback` | Stores patient feedback submissions |

---

## 🤖 Dialogflow Intents

| Intent | Description |
|--------|-------------|
| `NewAppointment` | Initiates appointment booking flow |
| `TypeofDoc` | Fetches doctors by specialization |
| `numberDoctor` | Books appointment with selected doctor |
| `ViewAppoint` | Displays patient's appointments |
| `Yes / No` | Handles appointment update confirmation |

---

## 🌐 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Main page with chatbot |
| `POST` | `/df` | Dialogflow webhook |
| `GET` | `/action1` | Patient registration form |
| `POST` | `/action2` | Handles registration submission |
| `GET` | `/feedback1` | Feedback form |
| `POST` | `/feedback2` | Handles feedback submission |

---

## ☁️ Deployment

This app is configured for **Google App Engine**. To deploy:

```bash
gcloud app deploy
```

---

## 📌 Notes

- Make sure your Dialogflow webhook URL points to your deployed `/df` endpoint
- The chatbot is integrated with **Facebook Messenger** via Dialogflow's Facebook integration
- First user ID starts from `1111`

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
