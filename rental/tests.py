from django.test import TestCase
from datetime import date, timedelta
from . import validators


class ValidationsTestCase(TestCase):
    def test_initial_state_value_of_rental(self):
        initial_values = ['A', 'L', 'C', 'D']
        output_values = list()
        for inital_value in initial_values:
            output_values.append(validators.valid_rental_states_on_create(inital_value))
        self.assertEqual(output_values, [True, True, False, False])

    def test_update_state_value_of_rental(self):
        old_values = new_values = ['A', 'L', 'C', 'D']
        expected_output_values = [
            [True, True, True, False],
            [False, True, False, True],
            [False, False, False, False],
            [False, False, False, False],
        ]
        for i, old_value in enumerate(old_values):
            output_values = [validators.valid_rental_states_on_update(old_value, new_value) for new_value in new_values]
            self.assertEqual(output_values, expected_output_values[i])

    def test_appointament_update_or_cancelation(self):
        today = date.today()
        entry_dates = [
            today + timedelta(days=5),
            today + timedelta(days=3),
            today,
            today - timedelta(days=3),
            today - timedelta(days=5),
        ]

        expected_response = [True, False, False, False, False]

        for entry, response in zip(entry_dates, expected_response):
            self.assertEqual(validators.valid_appointment_update_or_cancellation(entry), response)
