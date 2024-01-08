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
1. Clone the repository on your device
2. Create a virtual environment on your device
> python -m venv venv
3. Run the virtual environment, if you are using the Windows operating system, use the following command
> venv/Scripts/activate

But if you use Linux OS or MAC use the command below
> source venv/Scripts/activate
5. Install the libraries saved in the requirements.txt file, if you are using the PIP package manager you can use the following command
> pip install -r requirements.txt
4. Create the local_settings.py file in the **setup/** directory, in this file configure the database and API information such as SECRET_KEY_RENTAL, DEBUG, ALLOWED_HOSTS, SQL_ENGINE, SQL_DATABASE, SQL_USER, SQL_PASSWORD, SQL_HOST and SQL_PORT 
5. Create the database according to the settings established in the local_settings file (DATABASES.NAME)
6. Run the following command to create the API tables
> python manage.py migrate

