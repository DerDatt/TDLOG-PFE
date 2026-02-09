# TDLOG-PFE

Django project for the **Annuel des PFE** (Projet de Fin d'Études): student forms, PDF export (LaTeX), login/registration, and admin.

---

## Setup

1. **Environment**
   - Copy `.env.example` to `.env` and add your **OPENAI_API_KEY** (for auto-translation).
   - Activate your virtual environment, then:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Django**
   ```bash
   cd backend
   python manage.py migrate
   python manage.py runserver
   ```
   - Home: `http://127.0.0.1:8000/`
   - App (login/form): `http://127.0.0.1:8000/appPFE/`
   - Admin: `http://127.0.0.1:8000/admin/`

3. **Create an admin user (superuser)**  
   To log in to the Django admin site, create a superuser:
   ```bash
   cd backend
   python manage.py createsuperuser
   ```
   You will be prompted for username and password. Use these credentials at `http://127.0.0.1:8000/admin/`.

---

## How to Update the Form Structure (e.g. if fields are changed/added/removed)

**This section is for you if you want to modify the form that users fill out** (for example: add/remove fields, change types, or update field options). The following guide explains how to regenerate the underlying model fields to reflect your changes.

### Steps

1. **Edit the CSV with Field Definitions**  
   All form field definitions are stored in **`backend/appPFE/field_data.csv`**. You can add or modify fields there (columns: `name`, `field_type` such as `CharField`, `ImageField`, `BooleanField`, `ChoiceField`).

2. **Regenerate the Model Fields**  
   From the **`backend`** directory, run:
   ```bash
   cd backend
   python generate_model_fields.py
   ```
   This creates **`backend/generated_fields.txt`** with Python model field lines based on the CSV.

3. **Update the User Model**  
   - Open **`backend/accounts/models.py`**.
   - In the **`MyUser`** class, copy the lines (excluding comments) from **`backend/generated_fields.txt`** into the class, replacing or updating fields as necessary.
   - Only copy actual model field lines (e.g., `field_name = models.CharField(...)`) and avoid comment lines (`# --- ...`).

4. **Apply Migrations to Update the Database**
   ```bash
   cd backend
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

**Summary:**  
Edit **`backend/appPFE/field_data.csv`** → from **`backend`** run **`python generate_model_fields.py`** → copy from **`backend/generated_fields.txt`** into **`backend/accounts/models.py`** (class `MyUser`) → run **`makemigrations`** and **`migrate`**.


---

## Project structure (overview)

| Folder/File | Description |
|-------------|-------------|
| **backend/** | Django project. Contains `manage.py`, apps, and settings. |
| **backend/accounts/** | Custom user model (`MyUser`) and all form fields for the PFE Annuel; registration/profile. |
| **backend/appPFE/** | Main app: login, document form, PDF generation. Reads `field_data.csv` to build the form. |
| **backend/mysite/** | Django project config: `settings.py`, `urls.py`, admin customisation, WSGI/ASGI. |
| **backend/welcomePage/** | Home page with links to app, admin. |
| **backend/pdf_creation/** | LaTeX PDF generation: template and `generate_text.py` fill placeholders from user data. |
| **backend/auto_translation/** ⟶ Translation (e.g. FR→EN) via OpenAI. |
| **backend/media/** | Uploaded files (images), including `media/images/` for portrait photos. |
| **backend/templates/** | Global admin templates (base_site, change_list, index). |
| **backend/generate_model_fields.py** | Script: reads `appPFE/field_data.csv`, writes **`backend/generated_fields.txt`**. Run from `backend`. |
| **backend/generated_fields.txt** | Output of `generate_model_fields.py` – copy into `backend/accounts/models.py` (MyUser). |
| **.env** | Local environment (not in Git). Contains e.g. `OPENAI_API_KEY`. Create from `.env.example`. |

---

## Other notes

- **Admin:** Only **accounts** models are visible; default auth and other apps are hidden in admin.
- **Login:** Handled by **appPFE** (`/appPFE/login/`), not the accounts URLs.
- **PDF:** Generated from form data and the LaTeX template in `pdf_creation/generate_text.py`.
- **Testing – fill form with default data:** In **`backend/appPFE/utils.py`**, in `save_form_data_to_user`, you can **uncomment** the line `fill_user_with_default_data(user, form_class, post_data, files)`. If you then save `utils.py`, the changes are applied directly without restarting the server. Then, when you click **Save** on the document form on the website, all fields are filled with default sample data (useful for testing PDF generation or the form without typing). Remember to comment it out again for normal use.

--- 

## Future Work

- **Testing & reliability:** User inputs should be tested against malicious or adversarial input (e.g. injection attempts or unexpected control sequences) and handled safely to prevent unintended behavior or security issues.
- **Account management:** Password reset functionality is currently not available. A future improvement would be to allow administrators to securely reset user passwords.
- **Deployment & security:** Currently, the website runs only locally. Future work should include deploying it to a server and improving security to protect user data and communications.