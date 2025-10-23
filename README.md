

# Blood Donation System

---

A simple web-/desktop-application built with Python that manages blood donor and recipient information, enabling registration of donors, search for donors by blood group/location, and management of records.  
(The repository currently includes `app.py`, some templates, static assets, and SQLite files.)

## Table of Contents
- [About](#about)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation & Running](#installation--running)  
- [Configuration](#configuration)  
- [Project Structure](#project-structure)  
- [Database (SQLite)](#database-sqlite)  
- [Future Improvements](#future-improvements)  
- [Contributing](#contributing)  
- [License](#license)

## About  
This project aims to streamline the process of blood donation by maintaining an accessible system of donors and recipients. Donors can register their details (blood group, location, contact), and users in need of blood can search for compatible donors by group and/or city/state.

## Features  
- Donor registration (name, contact, blood group, location)  
- Search donors by blood group and/or city/state  
- (Optional) Admin view to manage donor records (if implemented)  
- Simple UI (HTML templates + static assets)  
- SQLite database(s) for storing donor / recipient information (`donor.db`, `donors.db`)  

## Tech Stack  
- **Backend**: Python (via `app.py`)  
- **Frontend**: HTML + CSS (templates located in `templates/` folder)  
- **Database**: SQLite  
- **Static Assets**: CSS, JavaScript, images in `static/` folder  

## Getting Started  
### Prerequisites  
- Python 3.x installed on your machine  
- Basic knowledge of running Python scripts  
- For web interface: a supported browser  

### Installation & Running  
1. Clone the repository:  
   ```bash
   git clone https://github.com/swayamprakashm/blood-donation-system.git
   cd blood-donation-system
   ```
2. (Optional) Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Unix/macOS  
   venv\Scripts\activate      # on Windows
   ```
3. Install dependencies (if any are listed in `requirements.txt`; if none, you may skip):

   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the database files (`donor.db`, `donors.db`) exist in the root folder and contain the required tables (or modify `app.py` to create them).
5. Run the application:

   ```bash
   python app.py
   ```
6. Open your browser and navigate to the address printed (typically `http://127.0.0.1:5000/` or similar) to access the UI.

## Configuration

* In `app.py`, you might find configuration parameters (database file names, debug mode, port).
* Modify CSS/HTML in the `static/` and `templates/` folders to adapt UI themes or add custom branding.
* If you prefer using a different database (e.g., MySQL) instead of SQLite, you’ll need to adapt the connection logic accordingly.

## Project Structure

```
blood-donation-system/
│
├── .vscode/                 # VSCode-specific settings (ignore if you use different editor)
├── instance/                # Instances, config or database folder (if any)
├── static/                  # CSS, images, JS for frontend
├── templates/               # HTML templates for web UI
├── app.py                   # Main Python application script
├── donor.db                 # SQLite database (donor details)
├── donors.db                # Another SQLite database (if used for different data)
└── README.md                # (this file)
```

## Database (SQLite)

Two SQLite files are present: `donor.db` and `donors.db`. They likely hold tables such as `Donors`, `Requests`, etc.

* Make sure to back them up before modifying.
* To inspect them, you can use SQLite browser tools (like DB Browser for SQLite).
* If you wish to reset data, just delete the `.db` file and rerun `app.py` to recreate (if logic is built in).

## Future Improvements

Here are some ideas you may consider for future development:

* Add user authentication (login for donors/recipients/admin).
* Add role-based dashboard: donor, recipient, admin.
* Enable search by blood group *and* availability, or by city/area radius.
* Send notifications (email/SMS) when blood of a certain type is requested.
* Expand database to track donation history, last donation date, eligibility.
* Add API endpoints (RESTful) for mobile or other UI clients.
* Enhance UI with modern frontend (Bootstrap, React/Vue).
* Add unit tests and CI configuration.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature/my-feature`).
5. Open a Pull Request describing your changes.
6. Please follow code style guidelines and include documentation where needed.

## Developed by
**M Swayam Prakash**

**GitHub** [https://github.com/swayamprakashm](https://github.com/swayamprakashm)




