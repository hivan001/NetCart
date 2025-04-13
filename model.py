import sys,os
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
        self.path = self.resource_path("results/network_db.json")

    def get_ids(self):
        data = self.read_db()
        ids = []
        for db_object in data["resources"]:
            for key,value in db_object.items():
                if key == "id":
                    ids.append(value)
        return ids

    def get_index_by_id(self,object_id):
        data = self.read_db()
        for index,db_object in enumerate(data["resources"]):
            for key,value in db_object.items():
                if key == "id" and value == object_id:
                    return index

    def update_field(self, object_id, field_name, field_data):
        data = self.read_db()
        object_index = self.get_index_by_id(object_id)
        data["resources"][object_index][field_name] = field_data

        self.write_db(data)

    
    def generate_object_id(self):
        ids = self.get_ids()
        return max(ids) + 1
    

              
    def add_pc(self, ip="", tcp_ports="", udp_ports="", name=""):
        data = self.read_db()
        pc = PC()
        object_id = self.generate_object_id()
        data["resources"].append(
            {       "id": object_id,
                    "resource_type":"workstation",
                    "ip": pc.ip,
                    "tcp_ports": pc.tcp_ports,
                    "udp_ports": pc.udp_ports,
                    "name": pc.name
            }

         )

        self.write_db(data)


    def remove_resource(self, object_id):
        data = self.read_db()
        for index, db_object in enumerate(data["resources"]):
            for key,value in db_object.items():
                if key == "id" and object_id == value:
                    data["resources"].pop(index)

        self.write_db(data)


    def add_server(self, ip="", tcp_ports="", udp_ports="", name=""):
        data = self.read_db()
        server = Server()
        object_id = self.generate_object_id()
        data["resources"].append(
            {       "id": object_id,
                    "resource_type":"server",
                    "ip": server.ip,
                    "tcp_ports": server.tcp_ports,
                    "udp_ports": server.udp_ports,
                    "name": server.name
            }

         )

        self.write_db(data)

    def resource_path(self,relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.abspath(relative_path)


    def write_db(self,data):
        try:
            with open(self.path, "w") as file:
                json.dump(data, file, indent=4)
        except:
            print("NetCart Error: Error writing changes to model.")

    def read_db(self):
        try:
            with open(self.path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("NetCart Error: JSON File not found.")
        except json.JSONDecodeError:
            print("NetCart Error: Unable to load JSON file.")

        return {}  # Return empty dict if there was an error



