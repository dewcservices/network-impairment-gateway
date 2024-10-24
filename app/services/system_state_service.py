import subprocess

from app.adapters.system_state_adapter import SystemStateAdapter
from app.adapters.traffic_control_adapter import TrafficControlAdapter
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
from app.services.interfaces.isystem_state_service import ISystemStateService


class SystemStateService(ISystemStateService):

    def __init__(
        self,
        repo: ISystemStateRepository,
        bearer_repo: IBearerRepository,
        env_repo: IEnvironmentRepository,
        interface: str,
        ip_address: str,
        uplink_qdisc_class: str,
        downlink_qdisc_class: str,
    ):
        self.repo = repo
        self.bearer_repo = bearer_repo
        self.env_repo = env_repo
        self.ip_address = ip_address
        self.interface = interface
        self.uplink_qdisc_class = uplink_qdisc_class
        self.downlink_qdisc_class = downlink_qdisc_class

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
            # create
            subprocess.call(
                TrafficControlAdapter.create_root_qdisc(interface=self.interface)
            )
            # set uplink
            uplink_bearer: BearerLink = bearer.bearer_links[0]
            uplink_bearer_hbt: BearerLinkHBT = uplink_bearer.bearer_link_hbt
            subprocess.call(
                TrafficControlAdapter.create_htb_class(
                    interface=self.interface,
                    rate=uplink_bearer_hbt.rate,
                    ceil=uplink_bearer_hbt.ceil,
                    class_id=self.uplink_qdisc_class,
                )
            )
            uplink_bearer_netem: BearerLinkNetem = uplink_bearer.bearer_link_netem

            subprocess.call(
                TrafficControlAdapter.create_netem_qdisc(
                    interface=self.interface,
                    delay_time=(uplink_bearer_netem.delay_time + env_netem.delay_time),
                    delay_jitter=(
                        uplink_bearer_netem.delay_jitter + env_netem.delay_jitter
                    ),
                    delay_correlation=(
                        uplink_bearer_netem.delay_correlation
                        + env_netem.corrupt_correlation
                    ),
                    loss_percentage=(
                        uplink_bearer_netem.loss_percentage + env_netem.loss_percentage
                    ),
                    loss_interval=(
                        uplink_bearer_netem.loss_interval + env_netem.loss_interval
                    ),
                    loss_correlation=(
                        uplink_bearer_netem.loss_correlation
                        + env_netem.loss_correlation
                    ),
                    corrupt_percentage=env_netem.corrupt_percentage,
                    corrupt_correlation=env_netem.corrupt_correlation,
                    class_id=self.uplink_qdisc_class,
                )
            )

            subprocess.call(
                TrafficControlAdapter.create_filter(
                    interface=self.interface,
                    flow_id=self.uplink_qdisc_class,
                    ip_addr=self.ip_address,
                    direction="src",
                )
            )

            # set downlink
            downlink_bearer: BearerLink = bearer.bearer_links[1]
            downlink_bearer_hbt: BearerLinkHBT = downlink_bearer.bearer_link_hbt
            subprocess.call(
                TrafficControlAdapter.create_htb_class(
                    interface=self.interface,
                    rate=downlink_bearer_hbt.rate,
                    ceil=downlink_bearer_hbt.ceil,
                    class_id=self.downlink_qdisc_class,
                )
            )

            downlink_bearer_netem: BearerLinkNetem = downlink_bearer.bearer_link_netem

            subprocess.call(
                TrafficControlAdapter.create_netem_qdisc(
                    interface=self.interface,
                    delay_time=(
                        downlink_bearer_netem.delay_time + env_netem.delay_time
                    ),
                    delay_jitter=(
                        downlink_bearer_netem.delay_jitter + env_netem.delay_jitter
                    ),
                    delay_correlation=(
                        downlink_bearer_netem.delay_correlation
                        + env_netem.corrupt_correlation
                    ),
                    loss_percentage=(
                        downlink_bearer_netem.loss_percentage
                        + env_netem.loss_percentage
                    ),
                    loss_interval=(
                        downlink_bearer_netem.loss_interval + env_netem.loss_interval
                    ),
                    loss_correlation=(
                        downlink_bearer_netem.loss_correlation
                        + env_netem.loss_correlation
                    ),
                    corrupt_percentage=env_netem.corrupt_percentage,
                    corrupt_correlation=env_netem.corrupt_correlation,
                    class_id=self.uplink_qdisc_class,
                )
            )

            subprocess.call(
                TrafficControlAdapter.create_filter(
                    interface=self.interface,
                    flow_id=self.downlink_qdisc_class,
                    ip_addr=self.ip_address,
                    direction="dst",
                )
            )

            return ResponseDTO(msg="Impairment created", isError=False)

        if state.bearer_id != payload.bearer_id:
            # TODO update bandwidth
            pass

        if (
            state.bearer_id != payload.bearer_id
            or state.environment_id != payload.environment_id
        ):
            # TODO update netem
            pass

        return ResponseDTO(msg="Impairment updated", isError=False)

    def delete_htb_netem_qdiscs(self) -> ResponseDTO:
        return ResponseDTO(msg="htb and netem qdisc added", isError=False)
