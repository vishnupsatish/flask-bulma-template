# Flask and Bulma Template

This code is a template for the back-end framework Flask and the front-end framework Bulma.

It is based on YouTuber Corey Schafer's Flask series. It also does NOT follow the application factory pattern; in my opinion, it is better this way.

This template is well-organized and is split into folders and files which contain code for specific uses.

## Features
- Accounts
- Login
- Log out
- Confirmation emails
- Password reset
- Simple database models
- Simple forms

## Installation
1. Clone the repository by running ```git clone https://github.com/vishnupsatish/flask-bulma-template```
2. Change the name of the directory to your project name by running ```mv flask-bulma-template [new_name]```
3. Go to the directory by running ```cd flask-bulma-template```
4. Ensure you have Python and virtualenv installed
5. Create a new virtual environment with the name ```venv``` by running ```virtualenv venv``` or ```python3 -m virtualenv venv```
6. Install the required Python modules by running ```pip install -r requirements.txt```
7. Set ```DATABASE_URL``` to ```sqlite:///site.db``` if you want to use SQLite
    - If you're not using SQLite, set it to your database's URL
8. Change all "placeholder" values to custom values (Ctrl+F "placeholder", non-case-sensitive, make sure not to change anything in ```application/forms```)
    - This includes your secret key, email username, email password, etc. for sending confirmation and password reset emails
9. Run the Flask application by running ```python3 run.py```
10. In a browser, go to ```http://localhost:5000```
11. If needed, in ``run.py``, change ```debug=False``` to ```debug=True``` to enable auto-reload

Note: if you are using Windows you may need to replace ```python3``` with ```python```

