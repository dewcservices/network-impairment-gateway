from app.constants import LinkTypes
from app.repositories.interfaces.ibearer_repository import IBearerRepository


## Optus C1 (Satellite)
# Uplink: 512 kbps rate, 1 Mbps ceil
# Downlink: 1 Mbps rate, 2 Mbps ceil
# Delay: 600 ms, Jitter: 50 ms, Loss: 0.1%, Correlation: 10%
def seed_optus_c1_bearer(bearer_repo: IBearerRepository):
    bearer_optus_c1 = bearer_repo.create(
        title="Optus C1",
        description="Satellite connection for Optus C1",
        img="https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/OptusD1_SatelliteOnly.jpg/200px-OptusD1_SatelliteOnly.jpg",
    )
    # Uplink (Optus C1)
    bearer_repo.create_bearer_link(
        id=bearer_optus_c1.id,
        link_type_id=LinkTypes.UPLINK.value,
        hbt_rate="512kbit",
        hbt_ceil="1mbit",
        netem_delay_time=600,
        netem_delay_jitter=50,
        netem_loss_percentage=0.1,
        netem_loss_interval=1000,
        netem_loss_correlation=10,
    )
    # Downlink (Optus C1)
    bearer_repo.create_bearer_link(
        id=bearer_optus_c1.id,
        link_type_id=LinkTypes.DOWNLINK.value,
        hbt_rate="1mbit",
        hbt_ceil="2mbit",
        netem_delay_time=600,
        netem_delay_jitter=50,
        netem_loss_percentage=0.1,
        netem_loss_interval=1000,
        netem_loss_correlation=10,
    )


## Commercial Maritime Satellite
# Uplink: 256 kbps rate, 512 kbps ceil
# Downlink: 512 kbps rate, 1 Mbps ceil
# Delay: 750 ms, Jitter: 100 ms, Loss: 1%, Correlation: 5%
# Commercial Maritime Satellite Bearer


def seed_commercial_maritime_bearer(bearer_repo: IBearerRepository):
    bearer_com_maritime = bearer_repo.create(
        title="Commercial Maritime Satellite",
        description="Satellite connection for maritime operations",
        img="https://www.eoportal.org/api/cms/documents/163813/5807516/Alphasat_Auto36.jpeg",
    )
    # Uplink (Commercial Maritime Satellite)
    bearer_repo.create_bearer_link(
        id=bearer_com_maritime.id,
        link_type_id=LinkTypes.UPLINK.value,
        hbt_rate="256kbit",
        hbt_ceil="512kbit",
        netem_delay_time=750,
        netem_delay_jitter=100,
        netem_loss_percentage=1,
        netem_loss_interval=1000,
        netem_loss_correlation=5,
    )
    # Downlink (Commercial Maritime Satellite)
    bearer_repo.create_bearer_link(
        id=bearer_com_maritime.id,
        link_type_id=LinkTypes.DOWNLINK.value,
        hbt_rate="512kbit",
        hbt_ceil="1mbit",
        netem_delay_time=750,
        netem_delay_jitter=100,
        netem_loss_percentage=1,
        netem_loss_interval=1000,
        netem_loss_correlation=5,
    )


## 4G
# Uplink: 5 Mbps rate, 10 Mbps ceil
# Downlink: 10 Mbps rate, 50 Mbps ceil
# Delay: 50 ms, Jitter: 10 ms, Loss: 0.05%, Correlation: 2%
# 4G Bearer
def seed_4g_bearer(bearer_repo: IBearerRepository):
    bearer_4g = bearer_repo.create(
        title="4G",
        description="4G connection",
        img="https://www.eoportal.org/api/cms/documents/163813/5807516/Alphasat_Auto36.jpeg",
    )
    # Uplink (4G)
    bearer_repo.create_bearer_link(
        id=bearer_4g.id,
        link_type_id=LinkTypes.UPLINK.value,
        hbt_rate="5mbit",
        hbt_ceil="10mbit",
        netem_delay_time=50,
        netem_delay_jitter=10,
        netem_loss_percentage=0.05,
        netem_loss_interval=1000,
        netem_loss_correlation=2,
    )
    # Downlink (4G)
    bearer_repo.create_bearer_link(
        id=bearer_4g.id,
        link_type_id=LinkTypes.DOWNLINK.value,
        hbt_rate="10mbit",
        hbt_ceil="50mbit",
        netem_delay_time=50,
        netem_delay_jitter=10,
        netem_loss_percentage=0.05,
        netem_loss_interval=1000,
        netem_loss_correlation=2,
    )


##5G
# Uplink: 20 Mbps rate, 50 Mbps ceil
# Downlink: 50 Mbps rate, 200 Mbps ceil
# Delay: 10 ms, Jitter: 2 ms, Loss: 0.01%, Correlation: 1%
def seed_5g_bearer(bearer_repo: IBearerRepository):
    bearer_5g = bearer_repo.create(
        title="5G",
        description="5G connection",
        img="https://www.eoportal.org/api/cms/documents/163813/5807516/Alphasat_Auto36.jpeg",
    )
    # Uplink (5G)
    bearer_repo.create_bearer_link(
        id=bearer_5g.id,
        link_type_id=LinkTypes.UPLINK.value,
        hbt_rate="20mbit",
        hbt_ceil="50mbit",
        netem_delay_time=10,
        netem_delay_jitter=2,
        netem_loss_percentage=0.01,
        netem_loss_interval=1000,
        netem_loss_correlation=1,
    )
    # Downlink (5G)
    bearer_repo.create_bearer_link(
        id=bearer_5g.id,
        link_type_id=LinkTypes.DOWNLINK.value,
        hbt_rate="50mbit",
        hbt_ceil="200mbit",
        netem_delay_time=10,
        netem_delay_jitter=2,
        netem_loss_percentage=0.01,
        netem_loss_interval=1000,
        netem_loss_correlation=1,
    )


## Fixed Internet
# Uplink: 10 Mbps rate, 100 Mbps ceil
# Downlink: 50 Mbps rate, 500 Mbps ceil
# Delay: 10 ms, Jitter: 1 ms, Loss: 0%, Correlation: 0%
def seed_fixed_internet_bearer(bearer_repo: IBearerRepository):
    bearer_fixed = bearer_repo.create(
        title="Fixed Internet",
        description="Fixed high-speed internet connection",
        img="https://www.eoportal.org/api/cms/documents/163813/5807516/Alphasat_Auto36.jpeg",
    )
    # Uplink (Fixed Internet)
    bearer_repo.create_bearer_link(
        id=bearer_fixed.id,
        link_type_id=LinkTypes.UPLINK.value,
        hbt_rate="10mbit",
        hbt_ceil="100mbit",
        netem_delay_time=10,
        netem_delay_jitter=1,
        netem_loss_percentage=0,
        netem_loss_interval=1000,
        netem_loss_correlation=0,
    )
    # Downlink (Fixed Internet)
    bearer_repo.create_bearer_link(
        id=bearer_fixed.id,
        link_type_id=LinkTypes.DOWNLINK.value,
        hbt_rate="50mbit",
        hbt_ceil="500mbit",
        netem_delay_time=10,
        netem_delay_jitter=1,
        netem_loss_percentage=0,
        netem_loss_interval=1000,
        netem_loss_correlation=0,
    )
