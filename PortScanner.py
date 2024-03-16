#!/usr/bin/env python3
import socket
import re
import subprocess

def check_ip(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', ip])
        return True
    except subprocess.CalledProcessError:
        return False

ip_add_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
port_range_pattern = re.compile(r"([0-9]+)-([0-9]+)")
port_min = 0
port_max = 65535

open_ports = []

while True:
    ip_add_entered = input("\nPlease enter the IP address that you want to scan: ")
    if ip_add_pattern.match(ip_add_entered):
        print(f"{ip_add_entered} is a valid IP address")
        break
    else:
        print("Invalid IP address format. Please try again.")

while True:
    print("Please enter the range of ports you want to scan in format: <int>-<int> (e.g., 60-120)")
    port_range = input("Enter port range: ")
    port_range_valid = port_range_pattern.match(port_range.replace(" ", ""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break
    else:
        print("Invalid port range format. Please try again.")

if check_ip(ip_add_entered):
    for port in range(port_min, port_max + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip_add_entered, port))
                if result == 0:
                    open_ports.append(port)
        except socket.error:
            pass
else:
    print("IP address is down or unreachable.")

if open_ports:
    print(f"\nOpen ports on {ip_add_entered}:")
    for port in open_ports:
        print(f"Port {port} is open.")
else:
    print(f"No open ports found on {ip_add_entered}.")
