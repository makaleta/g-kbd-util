#!/usr/bin/env python3

import os
import sys
import argparse

def find_service_file(directory: str) -> str:
    directory_path = os.path.abspath(directory)
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        sys.exit(1)
    service_file = None
    for file in os.listdir(directory_path):
        if file.endswith(".service"):
            service_file = os.path.join(directory_path, file)
            break
    if service_file is None:
        print(f"No service file found in directory '{directory_path}'.")
        sys.exit(1)
    return service_file

def install_systemd_service(directory:str, enable: bool):
    service_file = find_service_file(directory)
    service_name = os.path.splitext(os.path.basename(service_file))[0]
    systemd_path = f"/etc/systemd/system/{service_name}.service"
    os.system(f"cp {service_file} {systemd_path}")
    os.makedirs(f"/opt/{service_name}", exist_ok=True)
    for file in os.listdir(directory):
        if file.endswith(".sh"):
            os.system(f"cp {os.path.join(directory, file)} /opt/{service_name}")
    os.system("systemctl daemon-reload")
    print(f"Systemd service '{service_name}' installed successfully.")
    if enable:
        os.system(f"systemctl enable {service_name}")
        os.system(f"systemctl restart {service_name}")
        print(f"Systemd service '{service_name}' enabled, and started successfully.")
    sys.exit(0)

def uninstall_systemd_service(directory: str):
    service_file = find_service_file(directory)
    service_name = os.path.splitext(os.path.basename(service_file))[0]
    systemd_path = f"/etc/systemd/system/{service_name}.service"
    os.system(f"systemctl stop {service_name}")
    os.system(f"systemctl disable {service_name}")
    os.system(f"rm {systemd_path}")
    os.system(f"rm -rf /opt/{service_name}")
    os.system("systemctl daemon-reload")
    print(f"Systemd service '{service_name}' uninstalled successfully.")
    sys.exit(0)

def issudo():
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

def ensure_810_led_installed():
    if not os.path.exists("/lib/systemd/system/g810-led-reboot.service"):
        print("810-led is not installed. Please install it first.")
        print("sudo apt install g810-led")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Path to the directory containing the service file")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall the service")
    parser.add_argument("--enable", action="store_true", help="Start the service on boot")
    args = parser.parse_args()
    issudo()

    directory = args.directory
    if args.uninstall:
        uninstall_systemd_service(directory)
    ensure_810_led_installed()
    install_systemd_service(directory, args.enable)