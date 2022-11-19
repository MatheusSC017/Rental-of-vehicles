from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User, Permission, ContentType
from ..models import Insurance, AdditionalItems
from random import randrange
import faker
import json


class InsuranceTestCase(APITestCase):
    @staticmethod
    def json_generator():
        fake = faker.Faker('pt_BR')
        data = dict()
        for _ in range(randrange(3, 8)):
            data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
        return json.dumps(data)

    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')

        username = self.fake.first_name() + str(randrange(10000, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=username + '@email.com.br',
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

    def test_request_to_insurances_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_insurance_creation(self):
        self.client.force_login(self.user)
        data = {
            'title_insurance': ' '.join(self.fake.words(nb=2)),
            'coverage_insurance': self.json_generator(),
            'price_insurance': randrange(100, 2000) / 100
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_insurances_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_insurance_update(self):
        self.client.force_login(self.user)
        data = {
            'title_insurance': ' '.join(self.fake.words(nb=2)),
            'coverage_insurance': self.json_generator(),
            'price_insurance': randrange(100, 2000) / 100
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_insurance_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdditionalItemsTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')

        username = self.fake.first_name() + str(randrange(10000, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=username + '@email.com.br',
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

    def test_request_to_additional_items_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_additional_items_creation(self):
        self.client.force_login(self.user)
        data = {
            'name_additionalitems': ' '.join(self.fake.words(nb=2)),
            'daily_cost_additionalitems': randrange(100, 2000) / 100
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_additional_items_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_additional_items_update(self):
        self.client.force_login(self.user)
        data = {
            'name_additionalitems': ' '.join(self.fake.words(nb=2)),
            'daily_cost_additionalitems': randrange(100, 2000) / 100
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_additional_items_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
