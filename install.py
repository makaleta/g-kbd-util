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


def paths(service_name, is_user=False):
    if is_user:
        return {
            "service": f"/etc/systemd/user/{service_name}.service",
            "files": f"/usr/local/etc/{service_name}",
        }
    else:
        return {
            "service": f"/etc/systemd/system/{service_name}.service",
            "files": f"/opt/{service_name}",
        }

def install_service(service_file: str, directory: str, paths: dict):
    os.system(f"cp {service_file} {paths['service']}")
    os.makedirs(f"{paths['files']}", exist_ok=True)
    for file in os.listdir(directory):
        if file.endswith(".sh") or file.endswith(".py"):
            os.system(f"cp {os.path.join(directory, file)} {paths['files']}")

def install_systemd_service(directory: str, enable: bool):
    service_file = find_service_file(directory)
    service_name = os.path.splitext(os.path.basename(service_file))[0]
    cpaths = paths(service_name)
    install_service(service_file, directory, cpaths)
    os.system("systemctl daemon-reload")
    print(f"Systemd service '{service_name}' installed successfully.")
    if enable:
        os.system(f"systemctl enable {service_name}")
        os.system(f"systemctl restart {service_name}")
        print(f"Systemd service '{service_name}' enabled, and started successfully.")

def install_systemd_user_service(directory: str, enable: bool):
    service_file = find_service_file(directory)
    service_name = os.path.splitext(os.path.basename(service_file))[0]
    cpaths = paths(service_name, True)
    install_service(service_file, directory, cpaths)
    print(f"Systemd user service '{service_name}' installed successfully.")
    if enable:
        print("user service not enabled, run the following command to enable it:")
        print(f"systemctl --user daemon-reload")
        print(f"systemctl --user enable {service_name}")
        print(f"systemctl --user restart {service_name}")


def uninstall_systemd_service(directory: str):
    service_file = find_service_file(directory)
    service_name = os.path.splitext(os.path.basename(service_file))[0]
    cpaths = paths(service_name)
    os.system(f"systemctl stop {service_name}")
    os.system(f"systemctl disable {service_name}")
    os.system(f"rm {cpaths['service']}")
    os.system(f"rm -rf {cpaths['files']}")
    os.system("systemctl daemon-reload")
    print(f"Systemd service '{service_name}' uninstalled successfully.")

def uninstall_systemd_user_service(directory: str):
    service_file = find_service_file(directory)
    service_name = os.path.splitext(os.path.basename(service_file))[0]
    cpaths = paths(service_name)
    os.system(f"rm {cpaths['service']}")
    os.system(f"rm -rf {cpaths['files']}")
    print(f"Systemd user service '{service_name}' uninstalled successfully.")



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
    parser.add_argument(
        "directory", help="Path to the directory containing the service file"
    )
    parser.add_argument(
        "--uninstall", action="store_true", help="Uninstall the service"
    )
    parser.add_argument(
        "--enable", action="store_true", help="Start the service on boot"
    )
    args = parser.parse_args()
    issudo()

    directory = args.directory
    user_directory = directory + "/user"
    if args.uninstall:
        uninstall_systemd_service(directory)
        if os.path.exists(user_directory):
            uninstall_systemd_user_service(user_directory)
    ensure_810_led_installed()
    install_systemd_service(directory, args.enable)
    if os.path.exists(user_directory):
        install_systemd_user_service(user_directory, args.enable)
