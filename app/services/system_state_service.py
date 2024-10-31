from typing import cast

from app.adapters.system_state_adapter import SystemStateAdapter
from app.adapters.traffic_control_adapter import TrafficControlAdapter
from app.constants import LinkTypes
from app.dtos.response_dtos import ResponseDTO
from app.dtos.system_dtos import SystemStateDTO
from app.entities.models import (
    BearerLink,
    BearerLinkHBT,
    BearerLinkNetem,
    EnvironmentNetem,
)
from app.repositories.interfaces.ibearer_repository import IBearerRepository
from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository
from app.repositories.interfaces.isystem_state_repository import ISystemStateRepository
from app.services.interfaces.iprocess_service import IProcessService
from app.services.interfaces.isystem_state_service import ISystemStateService


class SystemStateService(ISystemStateService):

    def __init__(
        self,
        repo: ISystemStateRepository,
        bearer_repo: IBearerRepository,
        env_repo: IEnvironmentRepository,
        process_svc: IProcessService,
        uplink_interface: str,
        downlink_interface: str,
    ):
        self.repo = repo
        self.bearer_repo = bearer_repo
        self.env_repo = env_repo
        self.process_svc = process_svc
        self.uplink_interface = uplink_interface
        self.downlink_interface = downlink_interface
        self.uplink_class = "10"
        self.downlink_class = "20"

    def get(self) -> SystemStateDTO:
        return SystemStateAdapter.SystemStateToDTO(self.repo.get())

    def set_impairment(self, payload: SystemStateDTO) -> ResponseDTO:
        bearer = self.bearer_repo.get_by_id_eager(payload.bearer_id)
        env = self.env_repo.get_by_id_eager(payload.environment_id)
        # TODO - fix environment_netem db
        env_netem: EnvironmentNetem = env.environment_netem[0]

        self.delete_htb_netem_qdiscs()

        for link in bearer.bearer_links:
            # Explicitly cast link to BearerLink
            link = cast(BearerLink, link)
            bearer_link_netem = cast(BearerLinkNetem, link.bearer_link_netem)
            bearer_link_hbt = cast(BearerLinkHBT, link.bearer_link_hbt)
            interface = self.uplink_interface
            class_id = self.uplink_class
            if link.link_type_id == LinkTypes.DOWNLINK.value:
                interface = self.downlink_interface
                class_id = self.downlink_class

            self.create_bearer_link(
                interface=interface,
                bearer_link_hbt=bearer_link_hbt,
                bearer_link_netem=bearer_link_netem,
                env_netem=env_netem,
                class_id=class_id,
            )

        self.repo.set(bearer_id=payload.bearer_id, env_id=payload.environment_id)
        return ResponseDTO(
            msg=f"Impairment updated to {bearer.title} with {env.title} environment.",
            isError=False,
        )

    def create_bearer_link(
        self,
        bearer_link_hbt: BearerLinkHBT,
        bearer_link_netem: BearerLinkNetem,
        env_netem: EnvironmentNetem,
        interface: str,
        class_id: str,
    ) -> bool:
        # create root qdisc
        self.process_svc.run(
            TrafficControlAdapter.create_root_qdisc(
                interface=interface, class_id=class_id
            )
        )

        self.process_svc.run(
            TrafficControlAdapter.create_htb_class(
                interface=interface,
                class_id=class_id,
                rate=bearer_link_hbt.rate,
                ceil=bearer_link_hbt.ceil,
            )
        )

        self.process_svc.run(
            TrafficControlAdapter.create_netem_qdisc(
                interface=interface,
                class_id=class_id,
                delay_time=TrafficControlAdapter.add(
                    bearer_link_netem.delay_time, env_netem.delay_time
                ),
                delay_jitter=TrafficControlAdapter.add(
                    bearer_link_netem.delay_jitter, env_netem.delay_jitter
                ),
                delay_correlation=TrafficControlAdapter.add_percentage(
                    bearer_link_netem.delay_correlation, env_netem.corrupt_correlation
                ),
                loss_percentage=TrafficControlAdapter.add_percentage(
                    bearer_link_netem.loss_percentage, env_netem.loss_percentage
                ),
                loss_interval=TrafficControlAdapter.add(
                    bearer_link_netem.loss_interval, env_netem.loss_interval
                ),
                loss_correlation=TrafficControlAdapter.add_percentage(
                    bearer_link_netem.loss_correlation, env_netem.loss_correlation
                ),
                corrupt_percentage=env_netem.corrupt_percentage,
                corrupt_correlation=env_netem.corrupt_correlation,
            )
        )

    def delete_htb_netem_qdiscs(self) -> ResponseDTO:
        self.process_svc.run(
            cmd=TrafficControlAdapter.clear_qdisc(interface=self.uplink_interface),
            error_check=False,
        )
        self.process_svc.run(
            cmd=TrafficControlAdapter.clear_filter(interface=self.uplink_interface),
            error_check=False,
        )
        self.process_svc.run(
            cmd=TrafficControlAdapter.clear_qdisc(interface=self.downlink_interface),
            error_check=False,
        )
        self.process_svc.run(
            cmd=TrafficControlAdapter.clear_filter(interface=self.downlink_interface),
            error_check=False,
        )
        return ResponseDTO(msg="htb and netem qdisc added", isError=False)
