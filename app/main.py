import subprocess

from fastapi import FastAPI

app = FastAPI()

# Function to apply tc settings
def apply_tc(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

# Apply specific settings (individually)
@app.post("/set_bandwidth/")
def set_bandwidth(interface: str, rate: str, burst: str = "32kbit"):
    command = f"sudo tc qdisc add dev {interface} root tbf rate {rate} burst {burst} latency 400ms"
    output, error = apply_tc(command)
    return {"output": output, "error": error}

@app.post("/set_latency/")
def set_latency(interface: str, delay: str, jitter: str = "0ms"):
    command = f"sudo tc qdisc change dev {interface} root netem delay {delay} {jitter}"
    output, error = apply_tc(command)
    return {"output": output, "error": error}

@app.post("/set_packet_loss/")
def set_packet_loss(interface: str, loss: str):
    command = f"sudo tc qdisc change dev {interface} root netem loss {loss}"
    output, error = apply_tc(command)
    return {"output": output, "error": error}

# Predefined profiles
@app.post("/apply_profile/")
def apply_profile(profile_name: str, interface: str):
    if profile_name == "T1_sat_comm":
        command = f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                  f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 512kbit ceil 512kbit && " \
                  f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 600ms loss 2%"
    elif profile_name == "consumer_sat_comm":
        command = f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                  f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 256kbit ceil 256kbit && " \
                  f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 800ms loss 10%"
    elif profile_name == "broadband":
        command = f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                  f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 20mbit ceil 20mbit && " \
                  f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 50ms loss 0%"
    elif profile_name == "4g":
        command = f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                  f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 10mbit ceil 10mbit && " \
                  f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 70ms loss 1%"
    else:
        return {"error": "Profile not found"}

    output, error = apply_tc(command)
    return {"output": output, "error": error}

# Apply DDIL scenarios to the bearers
@app.post("/apply_ddil/")
def apply_ddil_scenario(scenario: str, interface: str):
    if scenario == "jamming":
        command = f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                  f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 256kbit ceil 256kbit && " \
                  f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 500ms 200ms loss 40%"
    elif scenario == "cyber_attack":
        command = f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                  f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 1mbit ceil 1mbit && " \
                  f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem corrupt 5% duplicate 10%"
    elif scenario == "mobility":
        command = f"sudo tc qdisc add dev {interface} root handle 1: htb default 12 && " \
                  f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate 512kbit ceil 512kbit && " \
                  f"sudo tc qdisc add dev {interface} parent 1:1 handle 10: netem delay 600ms 400ms"
    else:
        return {"error": "Scenario not found"}

    output, error = apply_tc(command)
    return {"output": output, "error": error}
