from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import RentalAdditionalItem


def update_additional_items_relationship(rental, additional_items_data) -> None:
    """
    This function will be to update the relationship between additional item and rent
    :param rental: Get an instance of the Rental model class
    :param additional_items_data: Get data for new rental additional items
    :return: None
    """
    new_additional_items_data = [item['additional_item'] for item in additional_items_data]

    for current_item in rental.additional_items.all():
        # If the current additional item is not present in the list of new additional items, it must be deleted
        if current_item.additional_item not in new_additional_items_data:
            update_stock_additional_items(additional_item=current_item.additional_item,
                                          ld_items_number=current_item.number)
            current_item.delete()
        # if it is present in the list of additional new items, the quantity value must be updated
        else:
            new_data = [item for item in additional_items_data if item['additional_item'] ==
                        current_item.additional_item][0]
            # The code in the line below deletes the updated record from the list of additional new items
            additional_items_data = [item for item in additional_items_data if item['additional_item']
                                     != current_item.additional_item]

            update_stock_additional_items(additional_item=current_item.additional_item,
                                          items_number=new_data['number'],
                                          old_items_number=current_item.number)

            current_item.number = new_data['number']
            current_item.save()

    # The last step will be to create new relationships for rent and additional items
    create_additional_items_relationship(rental, additional_items_data)


def create_additional_items_relationship(rental, additional_items_data) -> None:
    """
    This function will be to create the relationship between additional item and rent
    :param rental: Get an instance of the Rental model class
    :param additional_items_data: Get data for create rental additional items
    :return: None
    """
    for additional_item in additional_items_data:
        update_stock_additional_items(additional_item=additional_item['additional_item'],
                                      items_number=additional_item['number'])
        RentalAdditionalItem.objects.create(rental=rental, **additional_item)


def inventory_update_for_rental_devolution_or_cancellation(rental) -> None:
    """
    This function will be used to update the stock when there is a devolution or cancellation of the rent
    :param rental: Get an instance of the Rental model class
    :return: None
    """
    for item in rental.additional_items.all():
        update_stock_additional_items(additional_item=item.additional_item,
                                      old_items_number=item.number)


def update_stock_additional_items(additional_item, items_number=0, old_items_number=0):
    """
    This function will be used to update the stock of an additional item
    :param additional_item: Get an instance of the AdditionalItem model class
    :param items_number: Gets the new amount of items that will be rented
    :param old_items_number: Gets the old amount of items that was being rented
    :return: None
    """
    additional_item.stock = additional_item.stock - items_number + old_items_number
    if additional_item.stock < 0:
        raise ValidationError(_('Order number for additional item is greater than stock'))
    additional_item.save()
