# EAM Asset Hierarchy

---


## Description

This project was born as a help utility that can be useful when you trying to handle 
Oracle OEBS EAM Module. 

Especially the Asset Hierarchy. 

For now it's show you asset hierarchy and easy navigate through it.
For speeding this process all data can be downloaded to local SQLLite database.

---

## Prerequisites

1. Access to an Oracle OEBS APPS schema with read/write access.
2. Python 3.5 installation.

---


## Installation

1. Clone this repo.
2. Change current folder to `project_folder/ahi` 
3. Make .env file and define Oracle database parameters in it. 
You can find the example [here](ahi/env_example.txt)
4. Make new pipenv virtual environment and install all dependencies by command: `pipenv install`
4. Activate virtual environment: `pipenv shell`
5. Run Django migrate: `python manage.py migrate`
6. Init Oracle DB objects by: `python manage.py init_oebs`

---

## Usage

1. Change current folder to `project_folder/ahi` 
2. Activate virtual environment: `pipenv shell`
3. Run dev-server: `python manage.py runserver 0.0.0.0:8000`
4. Open url [localhost:8000](http://localhost:8000)
5. Select the root asset and hit **Submit**. Uncheck **Is sync hierarchy**
if you want to use local SQLLite database.
6. The Haul Truck icon means the Asset Number, 
the Gear icon means Rebuildable Number.
7. Press CTRL-C to stop dev-server

---

## Licence 

The Licence can be found [here](LICENSE.mit)

---

## Contributing

As and open source project AHI welcomes contribution of all forms. 
Please contact me by email in profile.







