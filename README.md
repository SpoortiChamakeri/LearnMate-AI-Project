# FoodShare – AI Food Waste Management (Student Prototype)

## Features
- Food donation form with SQLite storage
- NGO registration
- NGO dashboard
- Demo donation claim workflow
- Responsive interface and basic validation

## Run on Windows / VS Code
1. Extract this ZIP and open the `FoodShare_AI_Project` folder in VS Code.
2. In the terminal run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
Or skip activation and use `py -m pip install -r requirements.txt` then `py app.py`.

Open http://127.0.0.1:5000

## Pages
- Home / donate: /
- NGO registration: /ngo/register
- NGO dashboard: /ngo/dashboard
- About: /about
- Health check: /health

## Demo
Submit a donation, register an NGO with a unique email, open the dashboard and claim the donation.

## Important project honesty note
This is a working educational prototype. Matching/claiming is rule-based; there is no trained machine-learning model and no live Botpress connection included. Describe those as future enhancements unless you separately integrate and test them. Before real deployment, add authentication, authorization, CSRF protection, NGO verification, food-safety checks and production hosting.