import socket
import threading
import time

PORT = 9999
BUF = 1000

arp_cache = []   # list of dict {ip, mac, static}

def add_arp(ip, mac, static=False):
    for e in arp_cache:
        if e["ip"] == ip:
            if e["static"]:
                print("[CLIENT] STATIC prevents overwrite:", ip)
                return
            e["mac"] = mac
            print("[CLIENT] Updated ARP:", ip, "->", mac)
            return

    arp_cache.append({"ip": ip, "mac": mac, "static": static})
    print("[CLIENT] Added ARP:", ip, "->", mac, "(static)" if static else "")

def lookup_arp(ip):
    for e in arp_cache:
        if e["ip"] == ip:
            return e["mac"]
    return None

def show_arp():
    print("=== Local ARP Cache ===")
    for e in arp_cache:
        print(f"{e['ip']} -> {e['mac']} {'(STATIC)' if e['static'] else ''}")

def recv_thread(sock, my_ip):
    while True:
        data, addr = sock.recvfrom(BUF)
        msg = data.decode().strip()
        parts = msg.split()

        if parts[0] == "A": 
            _, src_ip, src_mac, dst_ip, _ = parts
            if dst_ip == my_ip:
                print(f"[CLIENT] ARP_REPLY: {src_ip} is {src_mac}")
                add_arp(src_ip, src_mac)

        elif parts[0] == "P": 
            _, dst_ip, dst_mac, src_ip = parts[:4]
            payload = " ".join(parts[4:])
            if dst_ip == my_ip:
                print(f"[CLIENT] PACKET from {src_ip}: {payload}")

def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python client.py <my_ip> <my_mac> [server_ip]")
        return

    my_ip = sys.argv[1]
    my_mac = sys.argv[2]
    server_ip = sys.argv[3] if len(sys.argv) > 3 else "127.0.0.1"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 0))

    serv = (server_ip, PORT)

    threading.Thread(target=recv_thread, args=(sock, my_ip), daemon=True).start()

    print(f"=== Client {my_ip}/{my_mac} connected to {server_ip}:{PORT} ===")
    print("Commands: register | arp <ip> | send <ip> <msg> | static <ip> <mac> | spoof <target_ip> <victim_ip> | show | exit")

    while True:
        cmd = input("cmd> ").strip().split()

        if not cmd:
            continue

        if cmd[0] == "register":
            msg = f"R {my_ip} {my_mac}"
            sock.sendto(msg.encode(), serv)
            print("[CLIENT] Registered.")

        elif cmd[0] == "arp":
            if len(cmd) != 2:
                print("Usage: arp <ip>")
                continue
            target = cmd[1]
            msg = f"Q {target} {my_ip} {my_mac}"
            sock.sendto(msg.encode(), serv)

        elif cmd[0] == "send":
            if len(cmd) < 3:
                print("Usage: send <ip> <msg>")
                continue
            dst = cmd[1]
            payload = " ".join(cmd[2:])
            mac = lookup_arp(dst)
            if not mac:
                print("No ARP entry. Run arp first.")
                continue
            msg = f"P {dst} {mac} {my_ip} {payload}"
            sock.sendto(msg.encode(), serv)

        elif cmd[0] == "static":
            if len(cmd) != 3:
                print("Usage: static <ip> <mac>")
                continue
            add_arp(cmd[1], cmd[2], static=True)

        elif cmd[0] == "spoof":
            if len(cmd) != 3:
                print("Usage: spoof <target_ip> <victim_ip>")
                continue
            target_ip = cmd[1]
            victim_ip = cmd[2]
            msg = f"A {target_ip} {my_mac} {victim_ip} 00:00:00:00:00:00"
            sock.sendto(msg.encode(), serv)
            print("[CLIENT] Sent spoofed ARP reply.")

        elif cmd[0] == "show":
            show_arp()

        elif cmd[0] == "exit":
            break

        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
