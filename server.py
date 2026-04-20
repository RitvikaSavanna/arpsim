import socket
PORT = 9999
BUF = 1000

clients = []          
trusted = [          
    ("192.168.1.1", "00:aa:00:00:01"),
    ("192.168.1.10", "00:aa:00:00:10"),
]
dai_enabled = True

def find_by_ip(ip):
    for c in clients:
        if c["ip"] == ip:
            return c
    return None

def check_trusted(ip, mac):
    for t_ip, t_mac in trusted:
        if t_ip == ip:
            return mac == t_mac
    return True 

def handle_message(sock,data,addr):
    msg=data.decode().strip()
    parts=msg.split()
    if not parts:
        return
    t = parts[0]
    if t == "R":
        if len(parts)!= 3:
            return
        ip,mac=parts[1],parts[2]
        exists=find_by_ip(ip)
        if exists:
            exists["mac"] = mac
            exists["addr"] = addr
        else:
            clients.append({"ip": ip, "mac": mac, "addr": addr})
        print(f"[SERVER] REGISTER {ip} -> {mac} FROM {addr}")
        return

    if t=="Q":
        q, target_ip, src_ip, src_mac=parts
        print(f"[SERVER] ARP REQUEST from {src_ip} asking for {target_ip}")

        target = find_by_ip(target_ip)
        if not target:
            print("[SERVER] No match for", target_ip)
            return

        
        reply = f"A {target['ip']} {target['mac']} {src_ip} {src_mac}"
        sock.sendto(reply.encode(), addr)
        print(f"[SERVER] Sent ARP_REPLY: {reply}")
        return

    if t == "A":
        a, src_ip, src_mac, dst_ip, dst_mac=parts
        print(f"[SERVER] ARP_REPLY {src_ip} -> {src_mac} for {dst_ip}")

   
        if dai_enabled and not check_trusted(src_ip, src_mac):
            print("[SERVER] DAI BLOCKED SPOOFED ARP")
            return

        dest = find_by_ip(dst_ip)
        if dest:
            sock.sendto(data, dest["addr"])
            print("[SERVER] Forwarded ARP_REPLY to", dst_ip)
        return

   
    if t == "P":
        p, dst_ip, dst_mac, src_ip = parts[:4]
        payload = " ".join(parts[4:])
        print(f"[SERVER] PACKET from {src_ip} -> {dst_ip}: {payload}")

      
        if dai_enabled and not check_trusted(dst_ip, dst_mac):
            print("[SERVER] DAI DROPPED PACKET → MAC mismatch!")
            return

        dest = find_by_ip(dst_ip)
        if not dest:
            print("[SERVER] Destination unknown.")
            return

        if dest["mac"] != dst_mac:
            print("[SERVER] Destination MAC mismatch. Drop.")
            return

        sock.sendto(data, dest["addr"])
        print("[SERVER] Delivered packet to", dst_ip)


def main():
    print("=== Python ARP/DAI Server Running ===")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORT))
    while True:
        data, addr = sock.recvfrom(BUF)
        handle_message(sock, data, addr)

if __name__ == "__main__":
    main()
