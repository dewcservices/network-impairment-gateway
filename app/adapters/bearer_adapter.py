from app.dtos.bearer_dtos import BearerDetailsDTO, BearerDTO
from app.entities.models import Bearer


class BearerAdapter:

    @staticmethod
    def BearerToBearerDTO(bearer: Bearer) -> BearerDTO:
        return BearerDTO.model_validate(bearer)

    @staticmethod
    def BearerToBearerDetailsDTO(bearer: Bearer) -> BearerDetailsDTO:
        return BearerDetailsDTO.model_validate(bearer)

    @staticmethod
    def BearerDTOToBearer(dto: BearerDTO) -> Bearer:
        # Convert Pydantic BearerDTO to SQLAlchemy Bearer using .dict() and **kwargs
        bearer_dict = dto.model_dump()

        # Convert img (HttpUrl type) to string if necessary
        if "img" in bearer_dict and bearer_dict["img"] is not None:
            bearer_dict["img"] = str(bearer_dict["img"])

        # Create and return SQLAlchemy Bearer model
        return Bearer(**bearer_dict)
