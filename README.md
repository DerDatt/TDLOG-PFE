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

---

## Generating model fields from CSV (`generate_model_fields.py`)

When form fields change (e.g. a new field in the CSV), you can generate the **accounts** model code automatically.

### Steps

1. **Edit the CSV** (optional)  
   Field definitions are in **`backend/appPFE/field_data.csv`** (columns: `name`, `field_type`, e.g. `CharField`, `ImageField`, `BooleanField`, `ChoiceField`).

2. **Run the script** (from the **project root**, not inside `backend/`):
   ```bash
   python generate_model_fields.py
   ```
   This creates **`generated_fields.txt`** in the project root.

3. **Copy into the model**  
   - Open **`backend/accounts/models.py`**.  
   - In the **`MyUser`** class, paste the *generated lines* from `generated_fields.txt` (or replace existing fields).  
   - Do not copy comment lines (`# --- ...`); only lines like  
     `field_name = models.CharField(...)` etc.  
   - Adjust system fields (`username`, `is_active`, `is_staff`) and e.g. `Photo_portrait` (ImageField) manually if needed.

4. **Apply migrations**
   ```bash
   cd backend
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

In short: **CSV → `generate_model_fields.py` → `generated_fields.txt` → paste content into `backend/accounts/models.py` (MyUser) → `makemigrations` + `migrate`.**

---

## Project structure (overview)

| Folder/File | Description |
|-------------|-------------|
| **backend/** | Django project. Contains `manage.py`, apps, and settings. |
| **backend/accounts/** | Custom user model (`MyUser`) and all form fields for the PFE Annuel; registration/profile. |
| **backend/appPFE/** | Main app: login, document form, PDF generation. Reads `field_data.csv` to build the form. |
| **backend/mysite/** | Django project config: `settings.py`, `urls.py`, admin customisation, WSGI/ASGI. |
| **backend/welcomePage/** | Home page with links to app, admin, etc. |
| **backend/pdf_creation/** | LaTeX PDF generation: template and `generate_text.py` fill placeholders from user data. |
| **backend/db_management/** | Scripts for DB access and PDF generation (e.g. tests, generation outside the web app). |
| **backend/auto_translation/** | Translation (e.g. FR↔EN) via OpenAI. |
| **backend/media/** | Uploaded files (e.g. images), including `media/images/` for portrait photos. |
| **backend/templates/** | Global admin templates (base_site, change_list, index). |
| **generate_model_fields.py** | Script in project root: reads `backend/appPFE/field_data.csv`, writes **`generated_fields.txt`** for copying into the model. |
| **generated_fields.txt** | Output of `generate_model_fields.py` – paste into `backend/accounts/models.py` (MyUser). |
| **.env** | Local environment (not in Git). Contains e.g. `OPENAI_API_KEY`. Create from `.env.example`. |

---

## Other notes

- **Admin:** Only **accounts** models are visible; default auth and other apps are hidden in admin.
- **Login/registration:** Handled by **appPFE** (`/appPFE/login/`), not the accounts URLs.
- **PDF:** Generated from form data and the LaTeX template in `pdf_creation/generate_text.py`.
