# Implementation Notes

## Modes

- Unified mode: Both uplink and downlink have the same settings
- Uplink/Downlink mode: where the uplink and downlink have custom settings

## Configuration


```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Network Impairment Gateway tc Configuration Schema",
  "type": "object",
  "properties": {
    "interface": {
      "type": "string",
      "description": "Network interface to apply the tc configuration (e.g., eth0, eth1)",
      "enum": ["eth0", "eth1"]
    },
    "ip-address": {
      "type": "string",
      "description": "IP address of the interface",
      "format": "ipv4"
    },
    "uplink": {
        "type": "object",
        "qdisc-class": {
            "type": "string",
        },
        "hbt": {
            "description": "HTB settings for uplink bandwidth",    
            "$ref": "#/definitions/htb-bandwidth"
        },
        "netem": {
            "description": "HTB settings for uplink (outgoing) traffic",
            "$ref": "#/definitions/netem"
        }
    },
    "downlink": {
        "type": "object",
        "qdisc-class": {
            "type": "string",
        },
        "hbt": {
            "description": "HTB settings for uplink bandwidth",    
            "$ref": "#/definitions/htb-bandwidth"
        },
        "netem": {
            "description": "HTB settings for uplink (outgoing) traffic",
            "$ref": "#/definitions/netem"
        }
    },
  },
  "required": ["uplink", "downlink"],
  "additionalProperties": false
}
```

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HTB Bandwidth Schema",
  "type": "object",
  "properties": {
    "rate": {
        "type": "object",
        "properties": {
            "value": {
                "type": "integer",
                "description": "The guaranteed minimum bandwidth",
                "minimum": 1
            },
            "unit": {
                "type": "string",
                "description": "Unit of bandwidth (e.g., kbit, mbit, gbit)",
                "enum": ["kbit", "mbit", "gbit"]
            }
        },
        "required": ["value", "unit"]
    },
    "ceil": {
        "type": "object",
        "properties": {
        "value": {
            "type": "integer",
            "description": "The maximum bandwidth limit",
            "minimum": 1
        },
        "unit": {
            "type": "string",
            "description": "Unit of bandwidth (e.g., kbit, mbit, gbit)",
            "enum": ["kbit", "mbit", "gbit"]
        }
        },
        "required": ["value", "unit"]
    }
  },
  "required": ["rate", "ceil"]
}
```



```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Netem Configuration Schema",
  "type": "object",
  "properties": {
    "delay": {
      "type": "object",
      "description": "Configures delay and jitter settings.",
      "cmd": "delay {delay.time.value}{delay.time.unit} {delay.jitter.value}{delay.jitter.unit} {delay.correlation.value}{delay.correlation.unit}",
      "properties": {
        "time": {
          "type": "object",
          "properties": {
            "value": {
              "type": "integer",
              "description": "Fixed delay value.",
              "minimum": 0,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of delay (e.g., ms).",
              "enum": ["ms"]
            }
          },
          "required": ["value", "unit"]
        },
        "jitter": {
          "type": "object",
          "properties": {
            "value": {
              "type": "integer",
              "description": "Jitter (variable delay) value.",
              "minimum": 0,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of jitter (e.g., ms).",
              "enum": ["ms"]
            }
          },
          "required": ["value", "unit"]
        },
        "correlation": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Correlation for delay and jitter.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of correlation (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        }
      },
      "required": ["time"]
    },
    "loss": {
      "type": "object",
      "description": "Configures packet loss settings.",
      "cmd": "loss {loss.percentage.value}{loss.percentage.unit} {loss.interval.value}{loss.interval.unit} {loss.correlation.value}{loss.correlation.unit}",
      "properties": {
        "percentage": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Percentage of packet loss.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of packet loss (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        },
        "interval": {
          "type": "object",
          "properties": {
            "value": {
              "type": "integer",
              "description": "Interval between packet loss events.",
              "minimum": 0,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of interval (e.g., ms).",
              "enum": ["ms"]
            }
          },
          "required": ["value", "unit"]
        },
        "correlation": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Correlation for packet loss events.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of correlation (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        }
      },
      "required": ["percentage"]
    },
    "reorder": {
      "type": "object",
      "description": "Configures packet reordering settings.",
      "cmd": "reorder {reorder.percentage.value}{reorder.percentage.unit} {reorder.correlation.value}{reorder.correlation.unit} {reorder.gap.value}{reorder.gap.unit}",
      "properties": {
        "percentage": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Percentage of packet reordering.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of packet reordering (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        },
        "correlation": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Correlation for packet reordering events.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of correlation (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        },
        "gap": {
          "type": "object",
          "properties": {
            "value": {
              "type": "integer",
              "description": "Gap between reordered packets.",
              "minimum": 0,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of gap (e.g., packets).",
              "enum": ["packets"]
            }
          },
          "required": ["value", "unit"]
        }
      },
      "required": ["percentage"]
    },
    "duplicate": {
      "type": "object",
      "description": "Configures packet duplication settings.",
      "cmd": "duplicate {duplicate.percentage.value}{duplicate.percentage.unit} {duplicate.correlation.value}{duplicate.correlation.unit}",
      "properties": {
        "percentage": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Percentage of packet duplication.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of packet duplication (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        },
        "correlation": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Correlation for packet duplication.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of correlation (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        }
      },
      "required": ["percentage"]
    },
    "corrupt": {
      "type": "object",
      "description": "Configures packet corruption settings.",
      "cmd": "corrupt {corrupt.percentage.value}{corrupt.percentage.unit} {corrupt.correlation.value}{corrupt.correlation.unit}",
      "properties": {
        "percentage": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Percentage of packet corruption.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of packet corruption (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        },
        "correlation": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Correlation for packet corruption.",
              "minimum": 0,
              "maximum": 100,
              "default": 0
            },
            "unit": {
              "type": "string",
              "description": "Unit of correlation (percentage).",
              "enum": ["%"]
            }
          },
          "required": ["value", "unit"]
        }
      },
      "required": ["percentage"]
    }
  },
  "required": [],
  "additionalProperties": false
}
```

### Add

```sh
# Add root qdisc to eth0
tc qdisc add dev {interface} root handle 1: htb default 30
# Create uplink class (2 Mbps)
tc class add dev {interface} parent 1: classid {uplink.qdisc-class} htb rate {uplink.rate} ceil {uplink.ceil}
# Create downlink class (5 Mbps)
tc class add dev {interface} parent 1: classid {downlink.qdisc-class} htb rate {downlink.rate} ceil {downlink.ceil}
# Filter for uplink traffic
# Any traffic that matches the source IP filter (e.g., traffic originating from 192.168.1.100) will be classified as uplink traffic
tc filter add dev {interface} protocol ip parent 1: prio 1 u32 match ip src {ip-address}/32 flowid {uplink.qdisc-class}
# Filter for downlink traffic
# Any traffic that matches the destination IP filter (e.g., traffic destined for 192.168.1.100) will be classified as downlink traffic
tc filter add dev {interface} protocol ip parent 1: prio 1 u32 match ip dst {ip-address}/32 flowid {downlink.qdisc-class}
# Apply netem for uplink traffic (100ms delay, 10% loss)
tc qdisc add dev {interface} parent {uplink.qdisc-class} handle 10: netem delay {delay.settings} loss {loss.settings} ...
# Apply netem for downlink traffic (50ms delay, 5% loss)
tc qdisc add dev {interface} parent {downlink.qdisc-class} handle 20: netem delay {delay.settings} loss {loss.settings} ...
```

### Update/Change

#### Bandwidth

```sh
tc class change dev {interface} parent 1: classid {qdisc-class} htb rate {rate} ceil {ceil}
```

#### netem

uplink [handle 10:]
```sh
tc qdisc change dev {interface} parent {qdisc-class} handle 10: netem delay {delay.settings} loss {loss.settings} ...
```

uplink [handle 20:]
```sh
tc qdisc change dev {interface} parent {qdisc-class} handle 20: netem delay {delay.settings} loss {loss.settings} ...
```

### Remove/Delete


```sh
tc qdisc del dev {interface} root
```

- This command deletes the root qdisc (and all the associated classes, filters, and qdiscs) for the network interface eth0. When the root qdisc is deleted, it automatically removes all the traffic control rules and configurations applied to that interface, including any htb, netem, and filters.

This will effectively reset the traffic control settings for eth0, clearing all bandwidth limitations and network impairment rules.




