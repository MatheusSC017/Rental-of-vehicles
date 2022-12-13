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
from ..models import Rental, Insurance, AdditionalItems
from random import choice, choices, randrange
from validate_docbr import CPF, CNH, RENAVAM
from copy import deepcopy
from unidecode import unidecode
import faker
import json


class InsuranceViewSetTestCase(APITestCase):
    @staticmethod
    def json_generator():
        fake = faker.Faker('pt_BR')
        data = dict()
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
            title_insurance=' '.join(self.fake.words(nb=2)),
            coverage_insurance=self.json_generator(),
            price_insurance=randrange(100, 2000) / 100
        )

        self.list_url = reverse('Insurances-list')
        self.detail_url = reverse('Insurances-detail', kwargs={'pk': self.insurance.pk})

    def test_request_to_insurances_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_insurance_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'title_insurance': ' '.join(self.fake.words(nb=2)),
            'coverage_insurance': self.json_generator(),
            'price_insurance': randrange(100, 2000) / 100
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_request_to_insurance_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_insurance_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'title_insurance': ' '.join(self.fake.words(nb=2)),
            'coverage_insurance': self.json_generator(),
            'price_insurance': randrange(100, 2000) / 100
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

        self.additional_item = AdditionalItems.objects.create(
            name_additionalitems=' '.join(self.fake.words(nb=2)),
            daily_cost_additionalitems=randrange(100, 2000) / 100
        )

        self.list_url = reverse('AdditionalItems-list')
        self.detail_url = reverse('AdditionalItems-detail', kwargs={'pk': self.additional_item.pk})

    def test_request_to_additional_items_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_additional_items_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'name_additionalitems': ' '.join(self.fake.words(nb=2)),
            'daily_cost_additionalitems': randrange(100, 2000) / 100
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_request_to_additional_items_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_additional_items_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'name_additionalitems': ' '.join(self.fake.words(nb=2)),
            'daily_cost_additionalitems': randrange(100, 2000) / 100
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_additional_items_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)


class RentalViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')
        cpf = CPF()
        cnh = CNH()
        renavam = RENAVAM()

        def json_generator():
            data = dict()
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
            cep_address=fake.postcode(),
            state_address=fake.estado_sigla(),
            city_address=fake.city(),
            district_address=fake.bairro(),
            street_address=fake.street_name(),
            number_address=fake.building_number()
        ) for _ in range(4)]

        self.client_user = Client.objects.create(
            user_client=user_client,
            cpf_person=cpf.generate(),
            rg_person=fake.rg(),
            cnh_client=cnh.generate(),
            gender_person=choice(('M', 'F', 'N')),
            age_person=randrange(18, 99),
            finance_client=randrange(500, 30000),
            phone_person=fake.cellphone_number()[4:],
            address_person=addresses[0]
        )

        branch = Branch.objects.create(
            name_branch=fake.street_name(),
            opening_hours_start_branch=str(randrange(5, 13)) + ':00:00',
            opening_hours_end_branch=str(randrange(5, 13) + 8) + ':00:00',
            address_branch=addresses[1]
        )

        staffmember = StaffMember.objects.create(
            user_staffmember=self.user_staff,
            cpf_person=cpf.generate(),
            rg_person=fake.rg(),
            gender_person=choice(('M', 'F', 'N')),
            age_person=randrange(18, 99),
            salary_staffmember=randrange(500, 30000),
            phone_person=fake.cellphone_number()[4:],
            address_person=addresses[2],
            branch_staffmember=branch
        )

        daily_cost = randrange(500, 5000) / 100
        classification = VehicleClassification.objects.create(
            title_classification=' '.join(fake.words(nb=3)),
            daily_cost_classification=daily_cost
        )

        year_manufacture = randrange(1960, 2020)
        vehicle = Vehicle.objects.create(
            type_vehicle=choice('MC'),
            brand_vehicle=' '.join(fake.words(nb=1)),
            model_vehicle=' '.join(fake.words(nb=2)),
            year_manufacture_vehicle=year_manufacture,
            model_year_vehicle=year_manufacture + randrange(0, 5),
            mileage_vehicle=float(randrange(0, 2000)),
            renavam_vehicle=renavam.generate(),
            license_plate_vehicle=fake.license_plate().replace('-', ''),
            chassi_vehicle=str(randrange(11111111111111111, 99999999999999999)),
            fuel_vehicle=choice('GEDH'),
            fuel_tank_vehicle=randrange(15, 50),
            engine_vehicle=' '.join(fake.words()),
            color_vehicle=fake.color_name(),
            other_data_vehicle=json_generator(),
            available_vehicle=choices([True, False], weights=(90, 10))[0],
            branch_vehicle=branch,
            classification_vehicle=classification
        )

        insurance = Insurance.objects.create(
            title_insurance=' '.join(fake.words(nb=2)),
            coverage_insurance=json_generator(),
            price_insurance=randrange(100, 2000) / 100
        )

        self.additional_items = [AdditionalItems.objects.create(
            name_additionalitems=' '.join(fake.words(nb=2)),
            daily_cost_additionalitems=randrange(100, 2000) / 100
        ) for _ in range(3)]

        rental = Rental.objects.create(
            vehicle_rental=vehicle,
            staff_rental=staffmember,
            client_rental=self.client_user,
            status_rental='A',
            outlet_branch_rental=branch,
            appointment_date_rental=str(timezone.now() + timezone.timedelta(days=10))[:10],
            requested_days_rental=3,
            rent_deposit_rental=150,
            daily_cost_rental=daily_cost,
            additional_daily_cost_rental=0.,
            insurance_rental=insurance
        )
        rental.driver_rental.set([self.client_user, ])

        self.data = {
            'vehicle_rental': vehicle.renavam_vehicle,
            'client_rental': self.client_user.cpf_person,
            'status_rental': 'L',
            'appointment_date_rental': str(timezone.now() + timezone.timedelta(days=1))[:10],
            'requested_days_rental': 3,
            'rent_deposit_rental': 150,
            'driver_rental': self.client_user.pk,
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
        data['status_rental'] = 'A'
        data['appointment_date_rental'] = str(timezone.now() + timezone.timedelta(days=20))[:10]
        self.client.force_login(self.user_staff)
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_rental_delete(self) -> None:
        self.client.force_login(self.user_staff)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg=response.data)

    def test_function_check_to_calculate_additional_daily_cost(self) -> None:
        data = deepcopy(self.data)
        data['additional_items_rental'] = list(map(lambda i: i.pk, self.additional_items))
        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(Rental.objects.count(), 2)

        add_items = [add_item.get('id') for add_item in Rental.objects.all()[1].additional_items_rental.values()]
        self.assertEqual(set(add_items), set([add_item.pk for add_item in self.additional_items]))

        add_daily_cost = Rental.objects.all()[1].additional_daily_cost_rental
        self.assertEqual(add_daily_cost, sum([add_item.daily_cost_additionalitems
                                              for add_item in self.additional_items]))

    def test_rental_creation_with_rented_status(self) -> None:
        response = self.create_rent(self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(Rental.objects.count(), 2)
        self.assertEqual(Rental.objects.all()[1].status_rental, 'L')
        self.assertEqual(Rental.objects.all()[1].appointment_date_rental, None)

    def test_rental_creation_with_scheduled_status(self) -> None:
        data = deepcopy(self.data)
        data['status_rental'] = 'A'
        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(Rental.objects.count(), 2)
        self.assertEqual(Rental.objects.all()[1].status_rental, 'A')
        self.assertNotEqual(Rental.objects.all()[1].appointment_date_rental, None)

    def test_rental_creation_with_scheduled_status_and_without_appointament_date(self) -> None:
        data = deepcopy(self.data)
        data['status_rental'] = 'A'
        data['appointment_date_rental'] = ''
        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

    def test_rental_creation_with_scheduled_status_and_wrong_appointament_date(self) -> None:
        data = deepcopy(self.data)
        data['status_rental'] = 'A'
        data['appointment_date_rental'] = str(timezone.now() - timezone.timedelta(days=3))[:10]
        response = self.create_rent(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

    def create_rent(self, data) -> Response:
        self.client.force_login(self.user_staff)
        return self.client.post(self.list_url, data=data)
