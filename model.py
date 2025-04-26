import sys,os
import random
import copy
import network_objects.icon as icon
import json
from network_objects.pc import PC
from network_objects.server import Server
from process_nmap import process_nmap_text

class Model():
    '''Model class handles all backend logic to include adding or removing resources in JSON'''
    # ad_ports = ["88","464"]
    # db_ports = ["3306","5432","27017","1521","1433"]
    # web_ports = ["80","443","8080"]
    def __init__(self):
        self.path = self.get_db_path()

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
        # pc = PC()
        object_id = self.generate_object_id()
        data["resources"].append(
            {       "id": object_id,
                    "resource_type":"workstation",
                    "ip": ip,
                    "tcp_ports": tcp_ports,
                    "udp_ports": udp_ports,
                    "name": name
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
        # server = Server()
        object_id = self.generate_object_id()
        data["resources"].append(
            {       "id": object_id,
                    "resource_type":"server",
                    "ip": ip,
                    "tcp_ports": tcp_ports,
                    "udp_ports": udp_ports,
                    "name": name
            }

         )

        self.write_db(data)

    def get_db_path(self):
        if getattr(sys, 'frozen', False):  # Running as executable
            base_path = os.path.dirname(sys.executable)
        else:  # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(base_path, "network_db.json")

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
    

    def process_nmap_scan(self,text):
        objects = process_nmap_text(text)

        return objects



