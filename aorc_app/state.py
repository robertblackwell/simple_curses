import pathlib
import os

class AorcState:
    def __init__(self):
        self.cust_name = ""
        self.bus_org_id = ""
        self.is_marvel_order = False
        self.is_dm_order = False
        self.is_aorc_capitalized = False
        self.nokia_entry_nbr = 0
        self.next_hop_ip = "192.168.192.168"
        self.prefixes = []

        aorc_dir = os.path.dirname(__file__)
        self.config_exception_file_path = os.path.join(aorc_dir, "stuff/ddos2_exceptions")
        self.config_v14_command_file_path = os.path.join(aorc_dir, "stuff/ddos2_v14_command_push")
        self.config_quick_push_path = os.path.join(aorc_dir, "stuff/ddos2_quick_push")
        self.config_save_file_path = os.path.join(aorc_dir, "stuff/save")
        
        self.config_pid_file = '''/home/cjensen/bin/stuff/ddos2_script.pid'''
        self.config_policy_name = "ddos2-dynamic-check"

        self.config_exception_file = "{}".format(self.config_exception_file_path)
        self.config_v14_command_file = "{}".format(self.config_v14_command_file_path)
        self.config_quick_push_file = "{}".format(self.config_quick_push_path) 
        self.config_save_file = "{}".format(self.config_save_file_path)
        self.config_pid_file = "{}/stuff/ddos2_script.pid".format(aorc_dir)
        self.config_policy_name = "ddos2-dynamic-check"
