class PC():
    '''PC class that defines PC objects in a network'''
    def __init__(self):
            self.ip = ""
            self.tcp_ports = []
            self.udp_ports = []
            self.name =""

    def get_ip(self):
          return self.ip
    
    def get_tcp_ports(self):
          return self.tcp_ports
    
    def get_udp_ports(self):
          return self.udp_ports
    
    def get_name(self):
          return self.name
    

    def set_ip(self, ip):
          self.ip = ip
    
    def set_tcp_ports(self, tcp_ports):
          self.tcp_ports = tcp_ports
    
    def set_udp_ports(self, udp_ports):
          self.udp_ports = udp_ports
    
    def set_name(self, name):
          self.name = name

    def add_tcp_port(self, port):
          self.tcp_ports.append(port)

    def add_udp_port(self, port):
          self.udp_ports.append(port)