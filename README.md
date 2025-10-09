# Top Clinic
A web platform where patients can register, schedule appointments with doctors, and communicate via messages. Admins or doctors can manage appointments and patient data.

---

## Project Setup

### 1. Set Up the Environment
- Initialize a virtual environment:
  ```bash
  python -m venv venv
  ```
- Activate the virtual environment on Windows:
  ```bash
  venv\Scripts\activate
  ```
- Install Django:
  ```bash
  python -m pip install Django
  ```
- Install Gunicorn:
  ```bash
  python -m pip install gunicorn
  ```
- Update pip:
  ```bash
  python.exe -m pip install --upgrade pip
  ```
- Create requirements file
  ```bash
  pip freeze > requirements.txt
  ```

- Install npm/node and verify current version
  ```bash
  npm install -g npm
  node -v
  npm -v
  ```

  - Install Bootstrap 5
  ```bash
  pip install django-bootstrap-v5
  ```

- Install Bootstrap Icons
  ```bash
  npm i bootstrap-icons
  ```

### 2. Start Project
  - Create project:
  ```bash
  django-admin startproject top_clinic /Workspace/top_clinic
  ```
  <!-- This command creates the required folder/files for the project-->

### 3. Start App
  - Create App:
  ```bash
  python manage.py startapp top_clinic_app
  ```
  <!-- This command creates the required folder/files for the app -->

### 4. Connect to a postgreSQL database
- Update settings.py [django Documentation - DATABASES](https://docs.djangoproject.com/en/5.2/ref/settings/#databases)
  ```python
  DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydatabase",
        "USER": "mydatabaseuser",
        "PASSWORD": "mypassword",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
  }
  ```

### 5. Create superuser
- Add missing tables
  ```bash
  python manage.py makemigrations
  ```
  <!-- This command detects changes to the database and preps Django to update the changes.
      The updates are not applied at this point -->
  ```bash
  python manage.py migrate
  ```
  <!-- This command the migrations will take effect -->

- Create superuser
  ```bash
  python manage.py createsuperuser
  ```

 - Run local development server:
  ```bash
  python manage.py runserver
  ```

## Documentation
- [How to install Django on Windows](https://docs.djangoproject.com/en/5.2/howto/windows/)
- [Python.gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [VisualStudioCode.gitignore](https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore)
- [w3schools - Django](https://www.w3schools.com/django/)
- [Get Started with Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Mockaroo - Generate Mock Data](https://www.mockaroo.com/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Download Node.js](https://nodejs.org/en/download)
- [Downloading and installing Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

### Images
- [Image Resizer](https://imageresizer.com/)
- [Create Logo](https://www.canva.com/)
- [Convert to favicon](https://favicon.io/favicon-converter/)
- [DeepAI - AI Image Generator](https://deepai.org/)
- [ChatGPT - AI Image Generator](https://chatgpt.com/)