
class AorcState:
    def __init__(self):
        self.cust_name = ""
        self.bus_org_id = ""
        self.is_marvel_order = False
        self.is_dm_order = False
        self.is_aorc_capitalized = False
        self.nokia_entry_nbr = 0
        self.next_hop_id = "192.168.192.168"
        self.prefixes = []
        
        self.config_exception_file = '''/home/cjensen/bin/stuff/ddos2_exceptions'''
        self.config_v14_command_file = '''/home/cjensen/bin/stuff/ddos2_v14_command_push'''
        self.config_quick_push = '''/home/cjensen/bin/stuff/ddos2_quick_push'''
        self.config_save_file = '''/home/cjensen/bin/stuff/save'''
        self.config_pid_file = '''/home/cjensen/bin/stuff/ddos2_script.pid'''
        self.config_policy_name = "ddos2-dynamic-check"

        pass
