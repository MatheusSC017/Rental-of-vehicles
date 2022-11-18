# API de aluguel de veiculos

Este projeto tem como definição uma API de um sistema de uma locadora de veículos, contando com os seguintes endpoints:

- /enderecos/
- /filiais/
- /usuarios/
- /clientes/
- /veiculos/
- /alugueis/
- /alugueis/seguros/

Usuários da API que não estejam logados poderão somente consultar as informações dos veiculos disponibilizados pela locadoras, assim como o nome e o endereço das filiais da mesma.

## Requisitos
* **Python 3.9**
* **MySQL**

## Instalação
1. Clone este repositorio em seu dispositivo através do comando
> gh repo clone MatheusSC017/Rental-of-vehicles
2. Crie uma ambiente virtual em seu dispositivo
> python -m venv venv
3. Excute o ambiente virtual, caso esteja utilizando o sistema operacional windows utilize o comando a seguir
> venv/Scripts/activate

Porém se você utiliza o SO Linux ou MAC utilize o comando abaixo
> source venv/Scripts/activate
5. Instale as bibliotecas salvas no arquivo requirements.txt, caso esteja utilizando o gerenciador de pacotes PIP você poderá utilizar o comando a seguir
> pip install -r requirements.txt
4. Crie o arquivo local_settings.py no diretorio **setup/**, neste arquivo configure o banco de dados e informações da API como SECRET_KEY, DEBUG e ALLOWED_HOSTS
5. Crie a base de dados de acordo com as configurações estabelecidas no arquivo local_settings (DATABASES.NAME)
6. Execute o comando a seguir para criar as tabelas da API
> python manage.py migrate

