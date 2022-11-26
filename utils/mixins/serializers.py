from rest_framework.utils import model_meta


class GetRelationOfTheFieldMixin:
    @staticmethod
    def get_many_to_many_and_objects_fields(model) -> (list(), list()):
        info = model_meta.get_field_info(model)
        many_to_many = list()
        objects = list()
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many:
                many_to_many.append(field_name)
            else:
                objects.append(field_name)

        return many_to_many, objects
