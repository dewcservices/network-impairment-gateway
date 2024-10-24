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
        interface: str,
        ip_address: str,
        uplink_qdisc_class: str,
        downlink_qdisc_class: str,
        uplink_direction: str,
        downlink_direction: str,
        uplink_netem_handle: str,
        downlink_netem_handle: str,
    ):
        self.repo = repo
        self.bearer_repo = bearer_repo
        self.env_repo = env_repo
        self.process_svc = process_svc
        self.ip_address = ip_address
        self.interface = interface
        self.uplink_qdisc_class = uplink_qdisc_class
        self.uplink_direction = uplink_direction
        self.downlink_qdisc_class = downlink_qdisc_class
        self.downlink_direction = downlink_direction
        self.uplink_netem_handle = uplink_netem_handle
        self.downlink_netem_handle = downlink_netem_handle

    def get(self) -> SystemStateDTO:
        return SystemStateAdapter.SystemStateToDTO(self.repo.get())

    def set_impairment(self, payload: SystemStateDTO) -> ResponseDTO:
        state = self.repo.get()

        self.repo.set(bearer_id=payload.bearer_id, env_id=payload.environment_id)
        # TODO - Add the service to get the setting for the bearer and environment, then produce the tc commands
        bearer = self.bearer_repo.get_by_id_eager(payload.bearer_id)
        env = self.env_repo.get_by_id_eager(payload.environment_id)
        env_netem: EnvironmentNetem = env.environment_netem

        if state.bearer_id == -1 or state.environment_id == -1:
            # create root qdisc
            self.process_svc.call(
                TrafficControlAdapter.create_root_qdisc(interface=self.interface)
            )

        for link in bearer.bearer_links:
            # Explicitly cast link to BearerLink
            link = cast(BearerLink, link)
            bearer_link_netem = cast(BearerLinkNetem, link.bearer_link_netem)
            bearer_link_hbt = cast(BearerLinkHBT, link.bearer_link_hbt)
            qdisc_class = "not-set"
            direction = "not-set"
            handle = "not-set"
            if link.link_type_id == LinkTypes.UPLINK.value:
                qdisc_class = self.uplink_qdisc_class
                direction = self.uplink_direction
                handle = self.uplink_netem_handle
            elif link.link_type_id == LinkTypes.DOWNLINK.value:
                qdisc_class = self.downlink_qdisc_class
                direction = self.downlink_direction
                handle = self.downlink_netem_handle

            if state.bearer_id == -1 or state.environment_id == -1:
                self.create_bearer_link(
                    bearer_link_hbt=bearer_link_hbt,
                    bearer_link_netem=bearer_link_netem,
                    env_netem=env_netem,
                    qdisc_class=qdisc_class,
                    filter_direction=direction,
                    netem_handle=handle,
                )
                return ResponseDTO(msg="Impairment created", isError=False)

            if state.bearer_id != payload.bearer_id:
                # TODO update bandwidth
                self.update_hbt(
                    bearer_link_hbt=bearer_link_hbt, qdisc_class=qdisc_class
                )

            if (
                state.bearer_id != payload.bearer_id
                or state.environment_id != payload.environment_id
            ):
                # TODO update netem
                self.update_netem(
                    bearer_link_netem=bearer_link_netem,
                    env_netem=env_netem,
                    qdisc_class=qdisc_class,
                    netem_handle=handle,
                )

        return ResponseDTO(msg="Impairment updated", isError=False)

    def update_hbt(
        self,
        bearer_link_hbt: BearerLinkHBT,
        qdisc_class: str,
    ):
        self.process_svc.call(
            TrafficControlAdapter.update_hbt(
                interface=self.interface,
                class_id=qdisc_class,
                rate=bearer_link_hbt.rate,
                ceil=bearer_link_hbt.ceil,
            )
        )

    def update_netem(
        self,
        bearer_link_netem: BearerLinkNetem,
        env_netem: EnvironmentNetem,
        qdisc_class: str,
        netem_handle: str,
    ):
        self.process_svc.call(
            TrafficControlAdapter.update_netem(
                interface=self.interface,
                class_id=qdisc_class,
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
                    bearer_link_netem.loss_correlation + env_netem.loss_correlation
                ),
                corrupt_percentage=env_netem.corrupt_percentage,
                corrupt_correlation=env_netem.corrupt_correlation,
                handle=netem_handle,
            )
        )

    def create_bearer_link(
        self,
        bearer_link_hbt: BearerLinkHBT,
        bearer_link_netem: BearerLinkNetem,
        env_netem: EnvironmentNetem,
        qdisc_class: str,
        filter_direction: str,
        netem_handle: str,
    ) -> bool:

        self.process_svc.call(
            TrafficControlAdapter.create_htb_class(
                interface=self.interface,
                rate=bearer_link_hbt.rate,
                ceil=bearer_link_hbt.ceil,
                class_id=qdisc_class,
            )
        )

        self.process_svc.call(
            TrafficControlAdapter.create_netem_qdisc(
                interface=self.interface,
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
                    bearer_link_netem.loss_correlation + env_netem.loss_correlation
                ),
                corrupt_percentage=env_netem.corrupt_percentage,
                corrupt_correlation=env_netem.corrupt_correlation,
                class_id=qdisc_class,
                handle=netem_handle,
            )
        )

        self.process_svc.call(
            TrafficControlAdapter.create_filter(
                interface=self.interface,
                flow_id=qdisc_class,
                ip_addr=self.ip_address,
                direction=filter_direction,
            )
        )

    def delete_htb_netem_qdiscs(self) -> ResponseDTO:
        return ResponseDTO(msg="htb and netem qdisc added", isError=False)
