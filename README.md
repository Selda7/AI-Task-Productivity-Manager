# AI Task Productivity Manager

A smart task management web app built with Streamlit that helps users organize tasks, track productivity, and analyze work patterns using simple AI logic.

---

## Features

- Add tasks with name, type, date, and duration  
- View all tasks and mark them as completed  
- Analytics dashboard with interactive charts  
- Predict whether a task is likely to be productive  
- Modern AI / Neon styled user interface  

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn

---

## Project Structure
AI-Task-Productivity-Manager/
│

├── app.py # Main Streamlit application

├── style.css # Custom UI styles

├── requirements.txt # Project dependencies

├── .gitignore # Files ignored by Git

└── README.md # Project documentation

---

## How to Run the Project Locally

1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo-name.git
```

2. Navigate to the project folder:
cd your-repo-name

3. Install dependencies:
pip install -r requirements.txt

4. Run the app:
streamlit run app.py

---

## Analytics Overview

The analytics section provides insights into:
-Most active days
-Task distribution by type
-Task completion status

Interactive charts allow switching between visual and tabular views.

---

## AI Productivity Prediction

The app uses a simple Decision Tree model trained on task history to predict whether a task is likely to be productive based on:

-Day of the week

-Task type

---


## Notes

The tasks.csv file is generated automatically and is not included in the repository.
This project is intended for learning and productivity tracking purposes.

---

## Author

Created with passion by Selda Asaad
First complete AI-powered Streamlit project.