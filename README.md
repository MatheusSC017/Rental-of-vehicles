# Car Rental API

![Linguagem mais usada](https://img.shields.io/github/languages/top/MatheusSC017/Rental-of-vehicles)
![Numero de lingaugens usadas](https://img.shields.io/github/languages/count/MatheusSC017/Rental-of-vehicles)
![Lincense](https://img.shields.io/github/license/MatheusSC017/Rental-of-vehicles)
![Tamanho do projeto](https://img.shields.io/github/languages/code-size/MatheusSC017/Rental-of-vehicles)


## Summary
* [Requirements](https://github.com/MatheusSC017/Rental-of-vehicles#requirements)
* [Structure](https://github.com/MatheusSC017/Rental-of-vehicles#structure)
* [Authentication](https://github.com/MatheusSC017/Rental-of-vehicles#authentication)
* [Installation](https://github.com/MatheusSC017/Rental-of-vehicles#installation)
  * [Quick install with Docker](https://github.com/MatheusSC017/Rental-of-vehicles#quick-install-with-docker)
  * [On-premises installation](https://github.com/MatheusSC017/Rental-of-vehicles#on-premises-installation)
  * [Enviroment files parameters](https://github.com/MatheusSC017/Rental-of-vehicles#enviroment-files-parameters)

## Requirements
* **Python 3.9**
* **MySQL**

## Structure
Regarding the available endpoints, you can view them in the Swagger documentation at this [link](https://rental-of-vehicles-66128f353f24.herokuapp.com/ui/)

You can also view the list of endpoints made available by the API through the Swagger documentation stored in the documentation folder

## Authentication
Regarding the form of authentication accepted by the API, we have three ways of using it, the first is through basic authentication (Username and password), the second is through Token authentication that allows you to log in and create a token that can be used during requests and the third is Session Authentication, native to Django

## Installation
### Quick install with Docker
#### Installation for Development mode
1. Clone the repository on your device

2. Move to the project repository

3. Create the .env.coordinates file, in this file configure the database and API information to the microservice (Guide yourself through the [environment variables](https://github.com/MatheusSC017/Rental-of-vehicles#enviroment-files-parameters) section)

4. Create the .env.rental file, in this file configure the database and API information to the main API (Guide yourself through the [environment variables](https://github.com/MatheusSC017/Rental-of-vehicles#enviroment-files-parameters) section)

5. Run the docker compose file to install the application in development mode, in this form, the basic settings have already been set and some initial data will be generated for you to test the API
> docker-compose up -d --build 

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

6. Create the .env.coordinates file, in this file configure the database and API information to the microservice (Guide yourself through the [environment variables](https://github.com/MatheusSC017/Rental-of-vehicles#enviroment-files-parameters) section)

7. Run the file to start the database 
> python CoordinatesAPI/init_db.py 

8. Run the file to create an access key to be used in the main API, copy the token printed in the terminal
> python CoordinatesAPI/create_access_token.py 

9. Run the microservice application
> flask --app CoordinatesAPI/address run

10. Create the .env.rental file, in this file configure the database and API information to the main API (Guide yourself through the [environment variables](https://github.com/MatheusSC017/Rental-of-vehicles#enviroment-files-parameters) section)

11. Create the database according to the settings established in the .env.rental file
12. Run the following command to create the API tables
> python RentalAPI/manage.py migrate
13. Start the API through this command
> python RentalAPI/manage.py runserver

### Enviroment files parameters
#### .env.coordinates

Parameters | Characteristics                                       | Example
--- |-------------------------------------------------------| ---
SECRET_KEY_COORDINATES |                                                       |
COORDINATES_DATABASE_URI | Path to sqlite database file                          | sqlite:database.db
GOOGLE_MAPS_SECRET_KEY | Google secret key to access the [geocoding service](https://developers.google.com/maps/documentation/geocoding/overview?hl=pt-br) |

#### .env.rental

Parameters | Characteristics                                                                                                                         | Example
--- |-----------------------------------------------------------------------------------------------------------------------------------------| ---
SECRET_KEY_RENTAL |                                                                                                                                         | 
COORDINATES_API_KEY | Microservice access key, paste the access key created in step 8 if you are running on-premises or just ignore if you are using docker-compose | 
COORDINATES_URL | URL to access the microservice                                                                                                          | If you are running locally on port 5000, the value will be: http://127.0.0.1:5000/v1/distance/addresses or if you are running using docker set it to http://distance-microservice:5000/v1/distance/addresses
DEBUG | Boolean value                                                                                                                           | 0
DJANGO_ALLOWED_HOSTS |                                                                                                                                         | Local installation: localhost 127.0.0.1 [::1]
SQL_ENGINE | Database used                                                                                                                           | Mysql config (Local installation/ Docker-default): django.db.backends.mysql
SQL_DATABASE | Name of the database                                                                                                                    | Docker-default: rental-of-vehicles
SQL_USER | Name of the database user                                                                                                               | Docker-default: rental_database_user
SQL_PASSWORD | Password of the user                                                                                                                    | Docker-default: rental_database_password
SQL_HOST |                                                                                                                                         | Local installation/ Docker-default: 127.0.0.1
SQL_PORT | Port used                                                                                                                               | Commonly used port for mysql (Docker-default): 3306

