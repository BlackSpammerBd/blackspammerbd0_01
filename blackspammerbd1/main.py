#!/usr/bin/env python3

import sys
import os
import random
import string
import requests
import base64

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# সার্ভারের কনফিগারেশন
SERVER_PORT = 48491
SERVER_URL = f"http://127.0.0.1:{SERVER_PORT}"

def generate_connection_code():
    return ''.join(random.choices(string.digits, k=8))

def start():
    code = generate_connection_code()
    print(f"{GREEN}[+] Your connection code: {code}{RESET}")
    # প্রয়োজনে এখানে সার্ভার শুরু করার কোড যোগ করুন
    return code

def connect(code):
    print(f"{CYAN}[+] Attempting to connect using code: {code}{RESET}")
    try:
        response = requests.post(f"{SERVER_URL}/connect", json={"connection_code": code})
        if response.status_code == 200:
            print(f"{GREEN}[+] Connection successful: {response.json()}{RESET}")
        else:
            print(f"{RED}[-] Connection failed: {response.text}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error connecting: {e}{RESET}")

def list_all():
    print(f"{YELLOW}[+] Listing all files and folders...{RESET}")
    try:
        response = requests.get(f"{SERVER_URL}/list")
        if response.status_code == 200:
            files = response.json().get("files", [])
            for item in files:
                print(f"  - {item}")
        else:
            print(f"{RED}[-] Failed to retrieve list: {response.text}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")

def download_item(item_name):
    print(f"{CYAN}[+] Downloading: {item_name}{RESET}")
    try:
        response = requests.get(f"{SERVER_URL}/download/{item_name}")
        if response.status_code == 200:
            data = base64.b64decode(response.json().get("data", ""))
            with open(item_name, "wb") as f:
                f.write(data)
            print(f"{GREEN}[+] Downloaded '{item_name}' successfully.{RESET}")
        else:
            print(f"{RED}[-] Download failed: {response.text}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")

def upload_item(item_name):
    print(f"{CYAN}[+] Uploading: {item_name}{RESET}")
    try:
        with open(item_name, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        response = requests.post(f"{SERVER_URL}/upload", json={"item": item_name, "data": data})
        if response.status_code == 200:
            print(f"{GREEN}[+] Uploaded '{item_name}' successfully.{RESET}")
        else:
            print(f"{RED}[-] Upload failed: {response.text}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")

def main():
    if len(sys.argv) < 2:
        print(f"{YELLOW}Usage: bsb -start | -connect <code> | -list all | -download <name> | -upload <name>{RESET}")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "-start":
        start()
    elif cmd == "-connect":
        if len(sys.argv) < 3:
            print(f"{RED}[-] Please provide a connection code.{RESET}")
        else:
            connect(sys.argv[2])
    elif cmd == "-list" and len(sys.argv) == 3 and sys.argv[2] == "all":
        list_all()
    elif cmd == "-download":
        if len(sys.argv) < 3:
            print(f"{RED}[-] Please specify the item name to download.{RESET}")
        else:
            download_item(sys.argv[2])
    elif cmd == "-upload":
        if len(sys.argv) < 3:
            print(f"{RED}[-] Please specify the item name to upload.{RESET}")
        else:
            upload_item(sys.argv[2])
    else:
        print(f"{RED}[-] Unknown command.{RESET}")

if __name__ == "__main__":
    main()
