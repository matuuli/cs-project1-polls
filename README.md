## Installation

Clone the repository and enter the project directory.

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install the required Python packages:

pip install -r requirements.txt

Run the database migrations:

python3 manage.py migrate

Start the development server:

python3 manage.py runserver
