import re

def process_nmap_text(text:str) -> dict:
    cleaned_text = text.strip().lower()
    # Use a lookahead so we keep the "Starting Nmap" line in each chunk
    chunks = re.split(r"(?=^nmap scan report)", cleaned_text, flags=re.MULTILINE)
    # Remove empty chunks if any
    scans = [chunk.strip() for chunk in chunks if chunk.strip()]
    objects_to_build ={}

    for scan in scans:
        ip_match = ""
        ip = ""
        tcp_ports_string = ""
        udp_ports_string = ""
        ip_match = re.search(r'\((\d{1,3}(?:\.\d{1,3}){3})\)', scan)
        ip = ip_match.group(1) if ip_match else None
        tcp_ports = re.findall(r'(\d{1,5})/(tcp)', scan)
        udp_ports = re.findall(r'(\d{1,5})/(udp)', scan)

        for tcp_port in tcp_ports:
            tcp_ports_string+=f"{tcp_port[0]}\n"

        for udp_port in udp_ports:
            udp_ports_string+=f"{udp_port[0]}\n"

        if ip != None and ip not in objects_to_build.keys():
            objects_to_build[ip] = [{"tcp_ports":tcp_ports_string,"udp_ports":udp_ports_string}]

    return objects_to_build



    




# text = '''
# Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-24 20:29 CDT
# Nmap scan report for scanme.nmap.org (45.33.32.156)
# Host is up (0.096s latency).
# Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f

# PORT   STATE SERVICE
# 22/tcp open  ssh
# 80/tcp open  http


# Nmap scan report for scanme.nmap.org (10.10.20.30)
# Host is up (0.096s latency).
# Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f

# PORT   STATE SERVICE
# 23/tcp open  telnet
# 443/tcp open  https


# Nmap scan report for scanme.nmap.org (192.168.25.10)
# Host is up (0.096s latency).
# Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f

# PORT   STATE SERVICE
# 21/tcp open  ftp
# 88/tcp open  kerberos
# '''
# print(process_nmap_text(text))


