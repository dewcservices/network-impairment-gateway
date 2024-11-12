from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository

# | Environment | Delay (ms) |Jitter (ms) | Loss (%) | Corruption (%) | Description |
# |---|---|---|---|---|---|
# | Disconnected | 3000 ms | 700 ms | 70% | 10% |	Severely impaired network, very high latency, packet loss, and corruption. |
# | Disrupted | 1500 ms | 400 ms |	40% | 5% | Unstable network with high latency, packet loss, and occasional corruption. |
# | Intermittent | 800 ms |	200 ms | 20% | 2% | Moderate latency with frequent disconnections, but not fully disconnected. |
# | Limited | 300 ms | 50 ms | 5% | 0.5% | Low-bandwidth but relatively stable network with minor delays and occasional packet loss. |

## Clean Environment Settings
# In a clean network, there are no artificial delays, jitter, packet loss, or corruption.

# Delay: 0 ms
# Jitter: 0 ms
# Delay Correlation: 0%
# Loss: 0%
# Loss Interval: 0 ms
# Loss Correlation: 0%
# Corruption: 0%


def seed_clean_env(repo: IEnvironmentRepository):
    repo.create(
        title="Clean",
        description="No network impairment; ideal conditions with no delay, loss, or corruption.",
        netem_delay_time=0,  # 0 ms delay
        netem_delay_jitter=0,  # 0 ms jitter
        netem_delay_correlation=0,  # 0% correlation
        netem_loss_percentage=0.0,  # 0% packet loss
        netem_loss_interval=0,  # 0 ms loss interval
        netem_loss_correlation=0,  # 0% loss correlation
        netem_corrupt_percentage=0.0,  # 0% corruption
        netem_corrupt_correlation=0,  # 0% corruption correlation
    )


## Disconnected (Severe connectivity loss)
# This simulates a scenario where the network is barely functional or completely cut off intermittently, with high latency, packet loss, and corruption.

# Delay: 3000 ms
# Jitter: 700 ms
# Delay Correlation: 90%
# Loss: 100%
# Loss Interval: 50 ms
# Loss Correlation: 95%
# Corruption: 10%
# Corruption Correlation: 20%


def seed_disconnected_env(repo: IEnvironmentRepository):
    repo.create(
        title="Disconnected",
        description="Severely impaired network, very high latency, packet loss, and data corruption.",
        netem_delay_time=3000,  # 3000 ms delay
        netem_delay_jitter=700,  # 700 ms jitter
        netem_delay_correlation=90,  # 90% correlation
        netem_loss_percentage=70.0,  # 70% packet loss
        netem_loss_interval=50,  # 50 ms loss interval
        netem_loss_correlation=95,  # 95% loss correlation
        netem_corrupt_percentage=10.0,  # 10% packet corruption
        netem_corrupt_correlation=20,  # 20% corruption correlation
    )


## Disrupted (Unreliable and unstable connection)
# A disrupted environment simulates an unreliable network where there are frequent issues, but not as extreme as in the disconnected state.

# Delay: 1500 ms
# Jitter: 400 ms
# Delay Correlation: 70%
# Loss: 40%
# Loss Interval: 100 ms
# Loss Correlation: 60%
# Corruption: 5%
# Corruption Correlation: 15%


def seed_disrupted_env(repo: IEnvironmentRepository):
    repo.create(
        title="Disrupted",
        description="Unstable network with high latency, packet loss, and occasional corruption.",
        netem_delay_time=400,  # 1500 ms delay
        netem_delay_jitter=200,  # 400 ms jitter
        netem_delay_correlation=70,  # 70% correlation
        netem_loss_percentage=20.0,  # 40% packet loss
        netem_loss_interval=100,  # 100 ms loss interval
        netem_loss_correlation=40,  # 60% loss correlation
        netem_corrupt_percentage=5.0,  # 5% corruption
        netem_corrupt_correlation=15,  # 15% corruption correlation
    )


## Intermittent (Connection that cuts in and out frequently)
# An intermittent environment simulates frequent disconnections with moderate latency and packet loss.


# Delay: 800 ms
# Jitter: 200 ms
# Delay Correlation: 50%
# Loss: 20%
# Loss Interval: 200 ms
# Loss Correlation: 40%
# Corruption: 2%
# Corruption Correlation: 5%
def seed_intermittent_env(repo: IEnvironmentRepository):
    repo.create(
        title="Intermittent",
        description="Network with moderate latency and frequent drops, but not fully disconnected.",
        netem_delay_time=250,  # 800 ms delay
        netem_delay_jitter=150,  # 200 ms jitter
        netem_delay_correlation=50,  # 50% correlation
        netem_loss_percentage=15.0,  # 20% packet loss
        netem_loss_interval=200,  # 200 ms loss interval
        netem_loss_correlation=40,  # 40% loss correlation
        netem_corrupt_percentage=2.0,  # 2% corruption
        netem_corrupt_correlation=5,  # 5% corruption correlation
    )


##Limited (Low bandwidth, moderate stability)
# A limited environment simulates a relatively stable but slow network with low bandwidth and minor issues.


# Delay: 300 ms
# Jitter: 50 ms
# Delay Correlation: 30%
# Loss: 5%
# Loss Interval: 500 ms
# Loss Correlation: 10%
# Corruption: 0.5%
# Corruption Correlation: 2%
def seed_limited_env(repo: IEnvironmentRepository):
    repo.create(
        title="Limited",
        description="Low-bandwidth but stable network with minor delays and occasional packet loss.",
        netem_delay_time=150,  # 300 ms delay
        netem_delay_jitter=100,  # 50 ms jitter
        netem_delay_correlation=30,  # 30% correlation
        netem_loss_percentage=0.0,  # 5% packet loss
        netem_loss_interval=500,  # 500 ms loss interval
        netem_loss_correlation=10,  # 10% loss correlation
        netem_corrupt_percentage=0.5,  # 0.5% corruption
        netem_corrupt_correlation=2,  # 2% corruption correlation
    )
