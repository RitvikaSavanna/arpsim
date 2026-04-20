# 🌐 ARP & Dynamic ARP Inspection (DAI) Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Networking](https://img.shields.io/badge/Networking-ARP%20Simulation-green)
![Security](https://img.shields.io/badge/Security-DAI-orange)
![Sockets](https://img.shields.io/badge/Sockets-UDP-purple)
![Status](https://img.shields.io/badge/Status-Working%20Prototype-success)
![License](https://img.shields.io/badge/License-MIT-green)

A **Python-based networking simulation** that demonstrates how **ARP (Address Resolution Protocol)** works and how **Dynamic ARP Inspection (DAI)** prevents ARP spoofing attacks.

This project simulates a small network using **UDP sockets**, allowing multiple clients to communicate via a central server.

---

## 🎯 Features

### 🌐 ARP Simulation

* Register clients with IP ↔ MAC mapping
* Send ARP requests (`Q`)
* Receive ARP replies (`A`)
* Maintain ARP cache on client side

### 🛡️ Security — DAI (Dynamic ARP Inspection)

* Validates ARP replies against trusted mappings
* Blocks spoofed ARP responses
* Prevents malicious packet delivery

### 💻 Client Capabilities

* ARP cache management (dynamic + static entries)
* Send packets to other clients
* Simulate ARP spoofing attacks
* View ARP table

### 🧪 Attack Simulation

* Perform **ARP spoofing**
* Observe how DAI blocks malicious behavior

---

## 🧠 Core Concepts

* ARP Protocol (Request/Reply)
* ARP Cache Management
* ARP Spoofing / Poisoning
* Dynamic ARP Inspection (DAI)
* UDP Socket Programming
* Client-Server Architecture

---

## 🗂️ Project Structure

```id="arp-structure"
project/
│
├── server.py     # ARP + DAI server
├── client.py     # Client with ARP cache
└── README.md
```

---

## ⚙️ Tech Stack

* **Language:** Python
* **Libraries:**

  * socket (UDP communication)
  * threading (client listener)
  * time

---

## 🚀 Getting Started

### 1. Clone the repository

```bash id="clone-arp"
git clone https://github.com/your-username/arp-dai-simulator.git
```

### 2. Run the server

```bash id="run-server"
python server.py
```

### 3. Run clients (in separate terminals)

```bash id="run-client"
python client.py <ip> <mac> [server_ip]
```

Example:

```bash
python client.py 192.168.1.2 00:aa:00:00:02
```

---

## 🖥️ Commands (Client)

| Command                         | Description          |
| ------------------------------- | -------------------- |
| `register`                      | Register with server |
| `arp <ip>`                      | Send ARP request     |
| `send <ip> <msg>`               | Send packet          |
| `static <ip> <mac>`             | Add static ARP entry |
| `spoof <target_ip> <victim_ip>` | Simulate ARP attack  |
| `show`                          | Display ARP cache    |
| `exit`                          | Exit client          |

---

## 🔄 How It Works

### 🧾 ARP Flow

1. Client sends ARP request
2. Server checks registry
3. Server replies with MAC
4. Client updates ARP cache

### ⚠️ Spoofing Scenario

* Attacker sends fake ARP reply
* Without DAI → victim cache poisoned
* With DAI → server blocks spoof

---

## 🔐 DAI Logic

* Server maintains **trusted IP–MAC mappings**
* Incoming ARP replies are validated
* If mismatch → ❌ packet dropped

---

## ⚠️ Limitations

* Simulation only (not real network layer)
* No GUI (CLI-based interaction)
* Limited scalability (basic architecture)

---

## 🔮 Future Improvements

* 🖥️ GUI for visualization
* 📊 Packet flow diagrams
* 🌐 Multi-network simulation
* 🔍 Logging & analytics
* 🧠 ML-based anomaly detection

---


