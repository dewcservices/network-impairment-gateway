from typing import List

from app.adapters.environment_adapter import EnvironmentAdapter
from app.dtos.environment_dtos import EnvironmentDTO
from app.dtos.response_dtos import ResponseDTO
from app.exception.request_processing_exception import RequestProcessingException
from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository
from app.services.interfaces.ienvironment_service import IEnvironmentService


class EnvironmentService(IEnvironmentService):
    def __init__(self, repo: IEnvironmentRepository):
        self.repo = repo

    def get_all(self) -> List[EnvironmentDTO]:
        list = self.repo.get_all()
        return EnvironmentAdapter.EnvironmentsToEnvironmentDetailsDTOs(list)

    def get(self, env_id: int) -> EnvironmentDTO:
        env = self.repo.get_by_id_eager(env_id)
        if env is None:
            raise RequestProcessingException(
                status_code=404, detail=f"Environment id {env_id} not found"
            )
        return EnvironmentAdapter.EnvironmentToEnvironmentDTO(env)

    def validateEnvironmentDtoObjects(self, dto: EnvironmentDTO):

        if dto.netem is None:
            raise RequestProcessingException(
                status_code=400,
                detail="Failed to create environment as netem settings have not been provided",
            )

        if dto.netem.corrupt is None:
            raise RequestProcessingException(
                status_code=400,
                detail="Failed to create environment as netem corruption settings have not been provided",
            )

        if dto.netem.delay is None:
            raise RequestProcessingException(
                status_code=400,
                detail="Failed to create environment as netem delay settings have not been provided",
            )

        if dto.netem.loss is None:
            raise RequestProcessingException(
                status_code=400,
                detail="Failed to create environment as netem loss settings have not been provided",
            )

    def create(self, dto: EnvironmentDTO) -> ResponseDTO:

        self.validateEnvironmentDtoObjects(dto=dto)

        env = self.repo.create(
            title=dto.title,
            description=dto.description,
            netem_delay_time=dto.netem.delay.time,
            netem_delay_jitter=dto.netem.delay.jitter,
            netem_delay_correlation=dto.netem.delay.correlation,
            netem_corrupt_correlation=dto.netem.corrupt.correlation,
            netem_corrupt_percentage=dto.netem.corrupt.percentage,
            netem_loss_correlation=dto.netem.loss.correlation,
            netem_loss_interval=dto.netem.loss.interval,
            netem_loss_percentage=dto.netem.loss.percentage,
        )

        if not env:
            raise RequestProcessingException(
                status_code=404, detail=f"Failed to create Environment {dto.title}"
            )
        return ResponseDTO(msg="environment created", isError=False)

    def update(self, env_id: int, dto: EnvironmentDTO) -> ResponseDTO:
        self.validateEnvironmentDtoObjects(dto=dto)
        # TODO: implement Env Netem Update approach in repo and this service
        self.repo.update(id=env_id, title=dto.title, description=dto.description)

        return ResponseDTO(msg="environment updated", isError=False)

    def delete(self, env_id: int) -> ResponseDTO:
        self.repo.delete(env_id)
        return ResponseDTO(msg="environment deleted", isError=False)
