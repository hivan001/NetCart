import sys
import random
import copy
import icon
import json
from pc import PC
from server import Server

class Model():
    '''Model class handles all backend logic to include adding or removing resources in JSON'''
    # ad_ports = ["88","464"]
    # db_ports = ["3306","5432","27017","1521","1433"]
    # web_ports = ["80","443","8080"]
    def __init__(self):
        self.path = "results/network_db.json"
        self.id_generator = 0

              
    def add_pc(self, ip="", tcp_ports=[], udp_ports=[], name=""):
        data = self.read_db()
        pc = PC()
        self.id_generator+=1
        data["resources"]["pcs"].append(
            {
                    "ip": pc.ip,
                    "tcp_ports": pc.tcp_ports,
                    "udp_ports": pc.udp_ports,
                    "name": pc.name
            }

         )

        self.write_db(data)


    def remove_pc(self, resource_id):
        data = self.read_db()
        data["resources"]["pcs"][0].pop(resource_id)
        self.write_db(data)


    def add_server(self, ip="", tcp_ports=[], udp_ports=[], name=""):
        data = self.read_db()
        server = Server()
        self.id_generator+=1
        data["resources"]["servers"].append(
            {
                    "ip": server.ip,
                    "tcp_ports": server.tcp_ports,
                    "udp_ports": server.udp_ports,
                    "name": server.name
            }

         )

        self.write_db(data)


    def remove_server(self, resource_id):
        data = self.read_db()
        data["resources"]["servers"][0].pop(resource_id)
        self.write_db(data)

    def write_db(self,data):
        try:
            with open(self.path, "w") as file:
                json.dump(data, file, indent=4)
        except:
            print("NetCart Error: Error writing changes to model.")

    def read_db(self):
        try:
            with open(self.path, "r") as file:
               data = json.load(file)
        except (FileNotFoundError):
            print("NetCart Error: JSON File not found.")
        except (json.JSONDecodeError):
            print("NetCart Error: Unable to load JSON file.")

        return data


