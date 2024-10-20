from typing import Dict

from pydantic import BaseModel


class DtoToModelUtil:
    @staticmethod
    def map_object_to_dto(obj, dto_class: BaseModel, add_fields: Dict[str, any] = None):
        # Use the Pydantic model fields to dynamically extract attributes from the object
        dto_fields = dto_class.model_fields
        mapped_data = {field: getattr(obj, field, None) for field in dto_fields}

        if add_fields:
            mapped_data.update(**add_fields)
        # Validate the dictionary and return the DTO instance
        return dto_class.model_validate(mapped_data)
