# Car Rental API

This project is an API for a car rental system, with the following endpoints:

- /enderecos/
- /filiais/
- /usuarios/
- /clientes/
- /veiculos/
- /alugueis/
- /alugueis/seguros/

API users who are not logged in will only be able to consult the information of the vehicles made available by the rental companies, as well as the name and address of their branches.

## Requirements
* **Python 3.9**
* **MySQL**

## Installation
### On-premises installation
1. Clone the repository on your device
2. Go to the project directory
3. Create a virtual environment on your device
> python -m venv venv 

4. Run the virtual environment, if you are using the Windows operating system, use the following command
> venv/Scripts/activate

But if you use Linux OS or MAC use the command below
> source venv/Scripts/activate
5. Install the libraries saved in the requirements.txt file, if you are using the PIP package manager you can use the following command
> pip install -r RentalAPI/requirements.txt
> pip install -r CoordinatesAPI/requirements.txt
6. Create the .env.coordinates file, in this file configure the database and API information to the microservice

Parameters | Characteristics                                       | Example
--- |-------------------------------------------------------| ---
SECRET_KEY_COORDINATES |                                                       |
COORDINATES_DATABASE_URI | Path to sqlite database file                          | sqlite:database.db
GOOGLE_MAPS_SECRET_KEY | Google secret key to access the [geocoding service](https://developers.google.com/maps/documentation/geocoding/overview?hl=pt-br) |

7. Run the file to start the database/ create an access key to be used in the main API, copy the token printed in the terminal
> python CoordinatesAPI/init_db.py 

8. Run the microservice application
> flask --app CoordinatesAPI/address run

8. Create the .env.rental file, in this file configure the database and API information to the main API

Parameters | Characteristics                | Example
--- |--------------------------------| ---
SECRET_KEY_RENTAL |                                | 
COORDINATES_API_KEY | Microservice access key, paste the access key created in step 7      |
COORDINATES_URL | URL to access the microservice | If you are running locally on port 5000, the value will be: http://127.0.0.1:5000/v1/distance/addresses
DEBUG | Boolean value                  | 0
DJANGO_ALLOWED_HOSTS |                                | Local installation: localhost 127.0.0.1 [::1]
SQL_ENGINE | Database used                  | Mysql config: django.db.backends.mysql
SQL_DATABASE | Name of the database           | rental-of-vehicles
SQL_USER | Name of the database user      |
SQL_PASSWORD | Password of the user           |
SQL_HOST |                                | Local installation: 127.0.0.1
SQL_PORT | Port used                      | Commonly used port for mysql: 3306

7. Create the database according to the settings established in the local_settings file (DATABASES.NAME)
8. Run the following command to create the API tables
> python RentalAPI/manage.py migrate
9. Start the API through this command
> python RentalAPI/manage.py runserver

