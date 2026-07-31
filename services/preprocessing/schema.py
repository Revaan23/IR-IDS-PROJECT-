"""
schema.py
----------
Enterprise Schema Definition for IR-IDS

Defines:
✓ Column Mapping
✓ Required Columns
✓ Numeric Columns
✓ Label Mapping
"""

# =============================================================================
# Column Mapping
# =============================================================================

COLUMN_MAPPING = {

    "Dst Port": "destination_port",
    "Src Port": "source_port",
    "Protocol": "protocol",
    "Timestamp": "timestamp",
    "Flow Duration": "flow_duration",

    "Tot Fwd Pkts": "total_forward_packets",
    "Tot Bwd Pkts": "total_backward_packets",

    "TotLen Fwd Pkts": "total_forward_bytes",
    "TotLen Bwd Pkts": "total_backward_bytes",

    "Flow Byts/s": "flow_bytes_per_sec",
    "Flow Pkts/s": "flow_packets_per_sec",

    "Flow IAT Mean": "flow_iat_mean",
    "Flow IAT Std": "flow_iat_std",
    "Flow IAT Max": "flow_iat_max",
    "Flow IAT Min": "flow_iat_min",

    "Fwd IAT Tot": "forward_iat_total",
    "Bwd IAT Tot": "backward_iat_total",

    "Label": "label"

}

# =============================================================================
# Required Columns
# =============================================================================

REQUIRED_COLUMNS = [

    "Label"

]

# =============================================================================
# Numeric Columns
# =============================================================================

NUMERIC_COLUMNS = [

    "destination_port",
    "source_port",
    "protocol",

    "flow_duration",

    "total_forward_packets",
    "total_backward_packets",

    "total_forward_bytes",
    "total_backward_bytes",

    "flow_bytes_per_sec",
    "flow_packets_per_sec",

    "flow_iat_mean",
    "flow_iat_std",
    "flow_iat_max",
    "flow_iat_min",

    "forward_iat_total",
    "backward_iat_total"

]

# =============================================================================
# Label Mapping
# =============================================================================

LABEL_MAPPING = {

    "BENIGN": "BENIGN",
    "Benign": "BENIGN",
    " benign ": "BENIGN",

    "FTP-BruteForce": "FTP_BRUTEFORCE",
    "SSH-Bruteforce": "SSH_BRUTEFORCE",

    "DoS attacks-Hulk": "DOS_HULK",
    "DoS attacks-GoldenEye": "DOS_GOLDENEYE",
    "DoS attacks-Slowloris": "DOS_SLOWLORIS",
    "DoS attacks-SlowHTTPTest": "DOS_SLOWHTTPTEST",

    "DDoS attacks-LOIC-HTTP": "DDOS_LOIC_HTTP",
    "DDoS attacks-LOIC-UDP": "DDOS_LOIC_UDP",

    "SQL Injection": "SQL_INJECTION",
    "Brute Force -Web": "WEB_BRUTEFORCE",
    "Brute Force -XSS": "WEB_XSS",

    "Infilteration": "INFILTERATION",

    "Bot": "BOT"
}