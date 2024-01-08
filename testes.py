import requests
import os
from dotenv import load_dotenv
from json import loads


load_dotenv()


data = {
    "start_address": {
        "street": "Rua Estela Marani Smecelato",
        "number": 288,
        "district": "Projeto 100",
        "city": "Mococa",
        "state": "SP",
        "country": "Brasil"
    },
    "end_address": {
        "street": "Rua Dr. Pedro de Toledo",
        "number": 150,
        "district": "Centro",
        "city": "Caconde",
        "state": "SP",
        "country": "Brasil"
    }
}


headers = {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJuYW1lIjoiUmVudGFsIG9mIHZlaGljbGVzIn0.iNJnatSG19yOAGsaQbLVBNHceUJqaOLrNE5MIl_cZGI"}

response = requests.get(os.getenv("COORDINATES_PATH"), json=data, headers=headers)

distance = loads(response.content)['distance'] / 1000

print(distance)
