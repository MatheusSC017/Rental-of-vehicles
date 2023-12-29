from random import choice, randrange
from copy import deepcopy
import json
import faker
from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Permission, ContentType
from address.models import Address
from client.models import Client
from staff.models import StaffMember
from branch.models import Branch
from vehicle.models import Vehicle, VehicleClassification
from validate_docbr import CPF, CNH, RENAVAM
from unidecode import unidecode
from ..models import Rental, Insurance, AdditionalItems, RentalAdditionalItem

fake = faker.Faker('pt_BR')
cpf_generator = CPF()
cnh_generator = CNH()
renavam_generator = RENAVAM()


class InsuranceViewSetTestCase(APITestCase):
    @staticmethod
    def json_generator():
        data = {}
        for _ in range(randrange(3, 8)):
            data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
        return json.dumps(data)

    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')

        username = self.fake.first_name().replace(' ', '_') + str(randrange(10000, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com.br'),
            password=username
        )

        content_type = ContentType.objects.get_for_model(Insurance)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.insurance = Insurance.objects.create(
            title=' '.join(self.fake.words(nb=2)),
            coverage=self.json_generator(),
            price=randrange(100, 2000) / 100
        )

        self.list_url = reverse('Insurances-list')
        self.detail_url = reverse('Insurances-detail', kwargs={'pk': self.insurance.pk})

    def test_request_to_insurances_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_insurance_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'title': ' '.join(self.fake.words(nb=2)),
            'coverage': self.json_generator(),
            'price': randrange(100, 2000) / 100
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_request_to_insurance_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_insurance_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'title': ' '.join(self.fake.words(nb=2)),
            'coverage': self.json_generator(),
            'price': randrange(100, 2000) / 100
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_insurance_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)


class AdditionalItemsViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')

        username = self.fake.first_name().replace(' ', '_') + str(randrange(10000, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com.br'),
            password=username
        )

        content_type = ContentType.objects.get_for_model(AdditionalItems)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        address = Address.objects.create(
            cep=self.fake.postcode(),
            state=self.fake.estado_sigla(),
            city=self.fake.city(),
            district=self.fake.bairro(),
            street=self.fake.street_name(),
            number=self.fake.building_number()
        )

        self.branch = Branch.objects.create(
            name=self.fake.street_name(),
            opening_hours_start=str(randrange(5, 13)) + ':00:00',
            opening_hours_end=str(randrange(5, 13) + 8) + ':00:00',
            address=address
        )

        self.additional_item = AdditionalItems.objects.create(
            name=' '.join(self.fake.words(nb=2)),
            daily_cost=randrange(100, 2000) / 100,
            stock=randrange(1, 5),
            branch=self.branch
        )

        self.list_url = reverse('AdditionalItems-list')
        self.detail_url = reverse('AdditionalItems-detail', kwargs={'pk': self.additional_item.pk})

    def test_request_to_additional_items_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_additional_items_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'name': ' '.join(self.fake.words(nb=2)),
            'daily_cost': randrange(100, 2000) / 100,
            'branch': self.branch.pk
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_request_to_additional_items_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_additional_items_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'name': ' '.join(self.fake.words(nb=2)),
            'daily_cost': randrange(100, 2000) / 100,
            'branch': self.branch.pk
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_additional_items_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)


class RentalViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        def json_generator():
            data = {}
            for _ in range(randrange(3, 8)):
                data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
            return json.dumps(data)

        usernames = [fake.first_name().replace(' ', '_') + str(randrange(10000, 99999)) for _ in range(2)]
        self.user_staff, user_client = [User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com.br'),
            password=username
        ) for username in usernames]

        content_type = ContentType.objects.get_for_model(Rental)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user_staff.user_permissions.add(permission)

        addresses = [Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        ) for _ in range(4)]

        self.client_user = Client.objects.create(
            user=user_client,
            cpf=cpf_generator.generate(),
            rg=fake.rg(),
            cnh=cnh_generator.generate(),
            gender=choice(('M', 'F', 'N')),
            age=randrange(18, 99),
            finance=randrange(500, 30000),
            phone=fake.cellphone_number()[4:],
            address=addresses[0]
        )

        branch = Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start=str(randrange(5, 13)) + ':00:00',
            opening_hours_end=str(randrange(5, 13) + 8) + ':00:00',
            address=addresses[1]
        )

        staffmember = StaffMember.objects.create(
            user=self.user_staff,
            cpf=cpf_generator.generate(),
            rg=fake.rg(),
            gender=choice(('M', 'F', 'N')),
            age=randrange(18, 99),
            salary=randrange(500, 30000),
            phone=fake.cellphone_number()[4:],
            address=addresses[2],
            branch=branch
        )

        classification = VehicleClassification.objects.create(
            title=' '.join(fake.words(nb=3)),
            daily_cost=randrange(500, 5000) / 100
        )

        year_manufacture = randrange(1960, 2020)
        vehicle = Vehicle.objects.create(
            type=choice('MC'),
            brand=' '.join(fake.words(nb=1)),
            model=' '.join(fake.words(nb=2)),
            year_manufacture=year_manufacture,
            model_year=year_manufacture + randrange(0, 5),
            mileage=float(randrange(0, 2000)),
            renavam=renavam_generator.generate(),
            license_plate=fake.license_plate().replace('-', ''),
            chassi=str(randrange(11111111111111111, 99999999999999999)),
            fuel=choice('GEDH'),
            fuel_tank=randrange(15, 50),
            engine=' '.join(fake.words()),
            color=fake.color_name(),
            other_data=json_generator(),
            available=True,
            branch=branch,
            classification=classification
        )

        insurance = Insurance.objects.create(
            title=' '.join(fake.words(nb=2)),
            coverage=json_generator(),
            price=randrange(100, 2000) / 100
        )

        self.additional_items = [AdditionalItems.objects.create(
            name=' '.join(fake.words(nb=2)),
            daily_cost=randrange(100, 2000) / 100,
            stock=randrange(5, 10),
            branch=branch
        ) for _ in range(3)]

        rental = Rental.objects.create(
            vehicle=vehicle,
            staff=staffmember,
            client=self.client_user,
            status='A',
            outlet_branch=branch,
            appointment_date=str(timezone.now() + timezone.timedelta(days=10))[:10],
            requested_days=3,
            rent_deposit=150,
            daily_cost=classification.daily_cost,
            additional_daily_cost=0.,
            insurance=insurance
        )
        rental.driver.set([self.client_user, ])

        self.rental_additional_items = [RentalAdditionalItem.objects.create(
            rental=rental,
            additional_item=item,
            number=randrange(1, 2)
        ) for item in self.additional_items[:2]]

        self.data = {
            'vehicle': vehicle.renavam,
            'client': self.client_user.cpf,
            'status': 'L',
            'appointment_date': str(timezone.now() + timezone.timedelta(days=1))[:10],
            'requested_days': 3,
            'rent_deposit': 150,
            'driver': [self.client_user.cpf, ],
            'additional_items': [{"additional_item": self.additional_items[0].pk, "number": 1}]
        }

        self.list_url = reverse('Rentals-list')
        self.detail_url = reverse('Rentals-detail', kwargs={'pk': rental.pk})

    def test_request_to_rental_list(self) -> None:
        self.client.force_login(self.user_staff)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_rental_creation(self) -> None:
        response = self.create_rent(self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_request_to_rental_detail(self) -> None:
        self.client.force_login(self.user_staff)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_rental_update(self) -> None:
        data = deepcopy(self.data)
        data['status'] = 'A'
        data['appointment_date'] = str(timezone.now() + timezone.timedelta(days=20))[:10]
        self.client.force_login(self.user_staff)
        response = self.client.put(self.detail_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_rental_delete(self) -> None:
        self.client.force_login(self.user_staff)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data)

    def test_function_check_to_calculate_additional_daily_cost(self) -> None:
        data = deepcopy(self.data)
        additional_items = [(item, randrange(1, 4)) for item in self.additional_items]
        data['additional_items'] = list(map(lambda i: {"additional_item": i[0].pk, "number": i[1]}, additional_items))
        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(Rental.objects.count(), 2)

        add_items = [add_item['additional_item_id'] for add_item
                     in Rental.objects.all()[1].additional_items.values()]
        self.assertEqual(set(add_items), {add_item.pk for add_item in self.additional_items})

        add_daily_cost = Rental.objects.all()[1].additional_daily_cost
        self.assertEqual(add_daily_cost, sum((add_item[0].daily_cost * add_item[1]
                                              for add_item in additional_items)))

    def test_rental_creation_with_rented_status(self) -> None:
        response = self.create_rent(self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(Rental.objects.count(), 2)
        self.assertEqual(Rental.objects.all()[1].status, 'L')
        self.assertEqual(Rental.objects.all()[1].appointment_date, None)

    def test_rental_creation_with_scheduled_status(self) -> None:
        data = deepcopy(self.data)
        data['status'] = 'A'
        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(Rental.objects.count(), 2)
        self.assertEqual(Rental.objects.all()[1].status, 'A')
        self.assertNotEqual(Rental.objects.all()[1].appointment_date, None)

    def test_rental_creation_with_scheduled_status_and_without_appointament_date(self) -> None:
        data = deepcopy(self.data)
        data['status'] = 'A'
        data['appointment_date'] = ''
        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

    def test_rental_creation_with_scheduled_status_and_wrong_appointament_date(self) -> None:
        data = deepcopy(self.data)
        data['status'] = 'A'
        data['appointment_date'] = str(timezone.now() - timezone.timedelta(days=3))[:10]
        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

    def test_stock_update_of_additional_items_when_creating_rent(self) -> None:
        data = deepcopy(self.data)
        additional_items = [(item, randrange(1, 4)) for item in self.additional_items]
        data['additional_items'] = list(map(lambda item: {"additional_item": item[0].pk,
                                                          "number": item[1]}, additional_items))

        current_stock = [item.stock for item in self.additional_items]

        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(Rental.objects.count(), 2)

        add_items = [add_item['additional_item_id'] for add_item
                     in Rental.objects.all()[1].additional_items.values()]
        self.assertEqual(set(add_items), {add_item.pk for add_item in self.additional_items})

        new_stock = [item.stock for item in AdditionalItems.objects.all()]
        for i, stock in enumerate(new_stock):
            self.assertEqual(stock, current_stock[i] - additional_items[i][1])

    def test_stock_update_of_additional_items_when_updating_rent(self) -> None:
        data = deepcopy(self.data)
        additional_items = [(item, randrange(1, 4)) for item in self.additional_items[1:]]
        data['status'] = 'A'
        data['additional_items'] = list(map(lambda item: {"additional_item": item[0].pk,
                                                          "number": item[1]}, additional_items))

        current_stock = [item.stock for item in self.additional_items]
        old_additional_items = [item.number for item in self.rental_additional_items]

        self.client.force_login(self.user_staff)
        response = self.client.put(self.detail_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(Rental.objects.count(), 1)

        add_items = [add_item[0].pk for add_item
                     in additional_items]
        self.assertEqual(set(add_items), set(add_items))

        new_stock = [item.stock for item in AdditionalItems.objects.all()]
        self.assertEqual(new_stock[0], current_stock[0] + old_additional_items[0])
        self.assertEqual(new_stock[1], current_stock[1] + old_additional_items[1] - additional_items[0][1])
        self.assertEqual(new_stock[2], current_stock[2] - additional_items[1][1])

    def create_rent(self, data) -> Response:
        self.client.force_login(self.user_staff)
        return self.client.post(self.list_url, data=data, format='json')
