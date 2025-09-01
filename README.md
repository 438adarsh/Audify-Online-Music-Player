# Audify 🎵

**Audify** is a Django-based music management and streaming web application, hosted on [Render](https://musicplayer-72yq.onrender.com/accounts/login/).  
It allows users to upload, manage, and listen to songs while giving admins the ability to manage user access.

> A simple, elegant way to enjoy and manage your music collection online.  

## Features

- Add, edit, and delete songs.
- Play and listen to uploaded music.
- Admin can approve or deny upload access for users.
- User profile shows upload access status: Granted, Pending, or Not Granted.
- Responsive and clean interface with modals for song management.

---

## Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Database:** SQLite (default)  
- **Deployment:** Render  

---

## Screenshots

**Login Page**  
![Audify Login](https://drive.google.com/uc?export=view&id=1vCoCILNGLrhuIbAM95MLS8-1i9CkVZcu)

**Home Page**  
![Audify Home](https://drive.google.com/uc?export=view&id=1zA8fLe38dquMRhVWSqxVTQLczFq8ci1g)

**Profile Page**  
![Audify Profile](https://drive.google.com/uc?export=view&id=1C5N0ZPd3wuFZd9ePNgE_aJ-CRe1EdDcN)

**Add New Song Modal**  
![Add New Song](https://drive.google.com/uc?export=view&id=1bui9k2I_u9rJTk_wj9XL26DP5MEyGVDD)

**Music Play Screen**  
![Music Play](https://drive.google.com/uc?export=view&id=1oYJWVExSgRM6-WE1dEa7Ccg2SGr2bkAa)

---

## Usage

1. Clone the repository:  
   ```bash
   git clone https://github.com/438adarsh/musicplayer.git

2. Navigate to Project folder:
   ```bash
   cd musciplayer

3. Create a Virtual Environment (Optional but recommended)
   ```bash
   python -m venv venv

Activate the virtual Environment:
Windows: venv\Scripts\activate
MACOS/Linux: source venv/bin/activate

4. Install dependencies:
   ```bash
   pip install -r requirements.txt

5. Apply database Migrations:
   ```bash
   python manage.py migrate

6. Create a Superuser(admin):
   ```bash
   python manage.py createsuperuser

7. Run the development server locally:
   ```bash
   python manage.py runserver

8. Open the app in browser:
http://127.0.0.1:8000
