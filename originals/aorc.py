#!/usr/bin/python3.4

# Author: Christian Jensen
# Date: 16 October 2020
# Version: 0.1.2

# v0.1.0 notes
# 12 October 2020
# Release

# v0.1.1 notes
# 16 October 2020
# Add check before sending config to devices
# Add save capability to nokia
# Data entry validation

# v0.1.2 notes
# 6 November 2020
# Updated the challenge prompts for disconnect to indicate that a Nokia ddos2_dynamic_check exists already

# v0.1.3 notes
# 28 April 2021
# Updated to verify whether the prefix list name is capitalized vs not
# Updated to verify whether the prefix list name should include MVL to indicate it is a Marvel order
# Updated prompt for customer name to include direction to enter the Marvel order number if applicable

# v0.1.4 notes
# 17 February 2022
# Updated to accept and support DM orders

import subprocess
import re
import os
import sys
import calendar
import time
import signal
import ipaddress
from subprocess import Popen, PIPE

prefix = ""
add_route = 0
duration = 1200
exception_file = '''/home/cjensen/bin/stuff/ddos2_exceptions'''
v14_command_file = '''/home/cjensen/bin/stuff/ddos2_v14_command_push'''
quick_push = '''/home/cjensen/bin/stuff/ddos2_quick_push'''
save = '''/home/cjensen/bin/stuff/save'''
pid_file = '''/home/cjensen/bin/stuff/ddos2_script.pid'''
customer_name = ""
bus_org_id = ""
list_name = ""
policy_name = "ddos2-dynamic-check"
prefix_list = ""
yesPattern = "[yY]|[yY]es"

# If debug is True then configurations will only be printed to the screen and will NOT be pushed to the devices. This also allows additional values to be exposed when operating the script.
debug = True

# One Nokia and one Juniper spare device that ROCI works with
test_devices = [
    {
        'manufacturer': 'Nokia',
        'dns': '7750-spare.par1'
    },
    {
        'manufacturer': 'Juniper',
        'dns': 'MX960-spare.hel1'
    },
]

# The PE's associated with the local centers. This array will need to be updated with devices anytime we add new local centers and/or add PE pairings with existing TMS devices.
devices = [
    {
        'manufacturer': 'Nokia',
        'dns': 'ear3.ams1',
    },
    {
        'manufacturer': 'Juniper',
        'dns': 'edge3.chi10',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr2.frf1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr3.frf1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr11.hkg3',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr12.hkg3',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr2.lax1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr3.lax1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'ear4.lon2',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr1.nyc1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'ear2.par1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr11.sap1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr12.sap1',
    },
    {
        'manufacturer': 'Juniper',
        'dns': 'edge9.sjo1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr11.sng3',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr12.sng3',
    },
    {
        'manufacturer': 'Juniper',
        'dns': 'edge3.syd1',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr11.tok4',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr2.wdc12',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr3.wdc12',
    },
    {
        'manufacturer': 'Nokia',
        'dns': 'msr1.dal1',
    }
]


# Gets the prefixes from the user
def getPrefixes():
    prefixes = []
    print("Enter prefixes below. Only one prefix per line. Please see example below:")
    print("192.168.0.0/16")
    print("10.0.0.0/8")
    print("8.39.237.128/32")
    print("Press ENTER on an empty line when you are done entering prefixes")
    print("=====================================BEGIN======================================")

    while True:
        prefix = input()
        if prefix:
            try:
                ipaddress.ip_network(prefix)
                prefixes.append(str(prefix))
            except:
                print('That entry did not match a IPv4 or IPv6 network entry with CIDR notation. Try again:\n\n')
                print("Enter prefixes below. Only one prefix per line. Please see example below:")
                print("192.168.0.0/16")
                print("10.0.0.0/8")
                print("8.39.237.128/32")
                print("Press ENTER on an empty line when you are done entering prefixes")
                print("=====================================BEGIN======================================")
        else:
            break
        if debug == True:
            print(prefixes)

    return prefixes


# Function that will handle pushing the compiled list of commands to a target device.
def push_file(msr, filename):
    pushStatic = '''roci ''' + msr + ''' -t=120 -f "''' + filename + '''" >> ''' + exception_file

    if debug == True:
        print(pushStatic)
        print("Not really pushing")
    else:
        p = subprocess.call(pushStatic, shell=True)


# Generate the configuration to create/add to a prefix list and policy as needed for Nokia devices
def add_to_prefix_list_nokia(nokia_name, prefixes, prefix_list, entry_num, next_hop, new):
    if prefix_list == "Exit":
        return 0

    open(quick_push, 'w')

    # generate the prefix-list code and store in a file
    command = '''/configure router policy-options abort\n/configure router policy-options begin'''
    update_file(quick_push, command)

    for each in prefixes:
        if ipaddress.ip_network(each).version == 4:
            command = '''\n/configure router policy-options prefix-list ''' + prefix_list + ''' prefix ''' + each + ''' longer'''
        #    elif ipaddress.ip_network(each).version == 6:
        #      command = '''\n/configure router policy-options prefix-list ''' + "ipv6-"+ prefix_list + ''' prefix ''' + each + ''' longer'''
        update_file(quick_push, command, each)

    if new:
        command = '''\n/configure router policy-options policy-statement ''' + policy_name + ''' entry ''' + entry_num + ''' description ''' + prefix_list + '''\n/configure router policy-options policy-statement ''' + policy_name + ''' entry ''' + entry_num + ''' from prefix-list ''' + prefix_list + '''\n/configure router policy-options policy-statement ''' + policy_name + ''' entry ''' + entry_num + ''' from family ipv4\n/configure router policy-options policy-statement ''' + policy_name + ''' entry ''' + entry_num + ''' action next-policy community replace ddos2-aorc ddos-global-scrubbers\n/configure router policy-options policy-statement ''' + policy_name + ''' entry ''' + entry_num + ''' action next-policy local-preference 3100100250\n/configure router policy-options policy-statement ''' + policy_name + ''' entry ''' + entry_num + ''' action next-policy next-hop ''' + next_hop
        update_file(quick_push, command)
    command = '''\n/configure router policy-options commit'''
    update_file(quick_push, command)
    print('''Updating ''' + prefix_list + ''' on ''' + nokia_name + ''' with prefix(es)\n''')
    if debug == False:
        push_file(nokia_name, quick_push)

    return 0


# Generate a configuration that creates/adds to the policy that contains the prefixes and updates the dynamic check policy when needed.
def add_to_prefix_list_juniper(juniper_name, prefixes, prefix_list, next_hop, new):
    if prefix_list == "Exit":
        return 0

    open(quick_push, 'w')

    command = '''\nedit exclusive'''
    update_file(quick_push, command)

    for each in prefixes:
        if ipaddress.ip_network(each).version == 4:
            command = '''\nset policy-options policy-statement ''' + prefix_list + ''' term BGP from route-filter ''' + each + ''' orlonger'''
        update_file(quick_push, command)

    if new:
        command = '''\nset policy-options policy-statement ''' + prefix_list + ''' term BGP then accept\nset policy-options policy-statement ''' + prefix_list + ''' term REJECT then reject\nset policy-options policy-statement ''' + policy_name + ''' term ''' + prefix_list + ''' from policy ''' + prefix_list + '''\nset policy-options policy-statement ''' + policy_name + ''' term ''' + prefix_list + ''' then local-preference 3100100250\nset policy-options policy-statement ''' + policy_name + ''' term ''' + prefix_list + ''' then community add ddos2-aorc\nset policy-options policy-statement ''' + policy_name + ''' term ''' + prefix_list + ''' then community add ddos-global-scrubbers\nset policy-options policy-statement ''' + policy_name + ''' term ''' + prefix_list + ''' then next-hop ''' + next_hop + '''\nset policy-options policy-statement ''' + policy_name + ''' term ''' + prefix_list + ''' then accept'''
        update_file(quick_push, command)
    command = '''\ncommit and-quit'''
    update_file(quick_push, command)
    print('''Updating ''' + prefix_list + ''' on ''' + juniper_name + ''' with prefix(es)\n''')
    if debug == False:
        push_file(juniper_name, quick_push)

    return 0


# Generate the configuration to remove a prefix, or prefixes, from a prefix-list on a Nokia device and update the dynamic check policy when needed.
def rem_from_prefix_list_nokia(nokia_name, prefixes, prefix_list, entry_num, next_hop, disco):
    if prefix_list == "Exit":
        return 0

    open(quick_push, 'w')
    command = '''\n/configure router policy-options abort\n/configure router policy-options begin'''
    update_file(quick_push, command)

    if disco:
        command = '''\n/configure router policy-options policy-statement ddos2-dynamic-check no entry ''' + entry_num + '''\n/configure router policy-options no prefix-list ''' + prefix_list
        update_file(quick_push, command)
    else:
        for each in prefixes:
            if ipaddress.ip_network(each).version == 4:
                command = '''\n/configure router policy-options prefix-list ''' + prefix_list + ''' no prefix ''' + each + ''' longer'''
            #      elif ipaddress.ip_network(each).version == 6:
            #        command = '''\n/configure router policy-options prefix-list ''' + "ipv6-" + prefix_list + ''' no prefix ''' + each + ''' longer'''
            update_file(quick_push, command, each)

    command = '''\n/configure router policy-options commit'''
    update_file(quick_push, command)
    print("Updating " + prefix_list + ''' on ''' + nokia_name + ''' with prefix(es)\n''')
    if debug == False:
        push_file(nokia_name, quick_push)

    return 0


# Generate the configuration to remove a prefix, or prefixes, from a prefix-list on a Juniper device and update the dynamic check policy when needed.
def rem_from_prefix_list_juniper(juniper_name, prefixes, prefix_list, next_hop, disco):
    if prefix_list == "Exit":
        return 0

    open(quick_push, 'w')
    command = '''\nedit exclusive'''
    update_file(quick_push, command)

    if disco:
        command = '''\ndelete policy-options policy-statement ddos2-dynamic-check term ''' + prefix_list + '''
delete policy-options policy-statement ''' + prefix_list
        update_file(quick_push, command)
    else:
        for each in prefixes:
            if ipaddress.ip_network(each).version == 4:
                command = '''\ndelete policy-options policy-statement ''' + prefix_list + ''' term BGP from route-filter ''' + each + ''' orlonger'''
            update_file(quick_push, command, each)

    command = '''\ncommit and-quit'''
    update_file(quick_push, command)
    print("Updating " + prefix_list + ''' on ''' + juniper_name + ''' with prefix(es)\n''')
    if debug == False:
        push_file(juniper_name, quick_push)

    return 0


# Using the busOrgID and the customer name, generate an appropriately long name to apply to the definition of our prefixes.
def list_name_generator(customer_name, bus_org_id, marvel, dm_order, uppercase):
    alpha_chars = filter(str.isalnum, customer_name)
    customer_name = "".join(alpha_chars)
    if marvel:
        list_name = bus_org_id + "-" + "MVL-" + customer_name
    elif dm_order:
        list_name = bus_org_id + "-" + "DM-" + customer_name
    else:
        list_name = bus_org_id + "-" + customer_name
    if uppercase:
        list_name = "aorc-" + list_name
        list_name = list_name.upper()
    else:
        list_name = list_name.upper()
        list_name = "aorc-" + list_name
    if len(list_name) > 31:
        list_name = list_name[:31]
    return list_name


# Writes discrete set of commands to a file to be used to push configuration changes to PE devices
def update_file(filename, command, lines=False):
    with open(filename, 'a') as the_file:
        the_file.write(command)
        the_file.close()

    if lines:
        except_f = open(exception_file, 'a')
        except_f.write("\n" + lines + "\n")
        except_f.close()

    if debug == True:
        print(command)

    return 0


def data_validation(message):
    print(message)
    while True:
        user_entry = input()
        if not user_entry:
            print("\nYou did not enter an answer. " + message)
            user_entry = True
        else:
            break
    return user_entry


# The main function
def user_menu():
    i = 0
    prefix_list = []
    pid = str(os.getpid())
    start = time.time()
    #  isNew = False
    #  isDisco = False
    route_attributes = []
    marvel = False
    dm_order = False
    uppercase = False

    choice = {
        "1": "Add prefix to prefix-list",
        "2": "Remove prefix from prefix-list",
        "3": "Exit",
    }

    subprocess.call('clear', shell=True)

    # Banner
    print("**********************************************************************************")
    print("                        _                                                      ")
    print("                       | |                                                     ")
    print("                       | |    _   _ _ __ ___   ___ _ __                        ")
    print("                       | |   | | | | '_ ` _ \ / _ \ '_ \                       ")
    print("                       | |___| |_| | | | | | |  __/ | | |                      ")
    print("                       \_____/\__,_|_| |_| |_|\___|_| |_|                      ")
    print("               ****************************************************               ")
    print("               *                      Lumen                       *               ")
    print("               *                     Security                     *               ")
    print("               *                                                  *               ")
    print("               *      DDoS 2.0 Always On Prefix List Script       *               ")
    print("               *                                                  *               ")
    print("               *                                                  *               ")
    print("               *                                                  *               ")
    print("               *    For issues with this script, please reach     *               ")
    print("               *              out to Chris Jensen                 *               ")
    print("               *                                                  *               ")
    print("               *             jensen.christian@lumen.com           *               ")
    print("               *               DL-SPIDDOSWAF@lumen.com            *               ")
    print("               ****************************************************               ")
    print("                                                                                  ")
    print("**********************************************************************************")

    #  print ('Please visit the following site for more information regarding this script:\nhttps://securitywiki.idc1.level3.com/index.php/Nocsup_Tools#Adding_.26_Removing_Static_Routes_.28Always_On.29')

    # Verify that the script isn't already running. If it is, advise the user to wait and exit.
    if os.path.isfile(pid_file):
        if debug:
            print("There's a file")
        pid_time = float(calendar.timegm(time.gmtime()) - os.path.getmtime(pid_file))
        if debug:
            print(pid_time)
        if pid_time > 600:
            if debug:
                print("Time for PID file is: " + str(pid_time))
            os.unlink(pid_file)
        else:
            fp = open(pid_file, 'r')
            pid_num = fp.readline()
            fp.close()
            checkPID = 'ps -fp ' + pid_num
            process = Popen(checkPID, shell=True, stdout=PIPE)
            stdout = process.communicate()
            if debug:
                print(stdout)
            proc_eles = str(stdout).split('\\n')
            if debug:
                print(proc_eles[1])
            if proc_eles[1] != "\', None)":
                proc_spec = proc_eles[1].split(' ')
                if debug:
                    print(proc_spec)
                proc_spec.remove('')
                print('\nThe script is in use by ' + proc_spec[
                    0] + '. Please wait a few minutes before trying to run the script again.')
                sys.exit()
            else:
                os.unlink(pid_file)

    setPidPerm = 'chown :ddosops ' + pid_file
    fo = open(pid_file, 'w')
    fo.write(pid)
    fo.close()
    Popen(setPidPerm, shell=True, stdout=PIPE)

    while True:
        isNew = False
        isDisco = False

        print("\nPlease enter the number corresponding to the choice you wish to make: \n")
        for key, value in sorted(choice.items()):
            print(key + " " + value)

        user_choice = input()

        # If the user has selected to add or remove prefixes, gather prefixes from the user
        if user_choice == "1" or user_choice == "2":

            while True:
                value = getPrefixes()
                if value == []:
                    continue
                if value != True and value != False:
                    break

            route_attributes = value
            except_f = open(exception_file, 'w')
            except_f.close()

            if user_choice == "1":
                isNew_message = "\nIs this a new install? (y/n): "
                isNew = data_validation(isNew_message)
                isNewMatch = re.match(yesPattern, isNew)
                if isNewMatch:
                    isNew = True
                else:
                    isNew = False

            if user_choice == "2":
                isDisco_message = "\nIs this a disconnect? (y/n): "
                isDisco = data_validation(isDisco_message)
                isDiscoMatch = re.match(yesPattern, isDisco)
                if isDiscoMatch:
                    isDisco = True
                else:
                    isDisco = False

            cust_name_message = "\nPlease enter the customer name, Marvel order number, or DM order number: "
            customer_name = data_validation(cust_name_message)

            bus_org_id_message = "\nPlease enter the Bus Org ID for the customer: "
            bus_org_id = data_validation(bus_org_id_message)

            if isNew == True:
                entry_num_message = "\nFor the Nokia devices, what is the next usable entry number for the ddos2-dynamic-check policy: "
                entry_num = data_validation(entry_num_message)

                next_hop_message = "\nPlease enter the diversion next-hop for this customer: "
                next_hop = data_validation(next_hop_message)

            elif isDisco == True:
                entry_num_message = "\nFor the Nokia devices, what is the customer's entry number for the ddos2-dynamic-check policy: "
                entry_num = data_validation(entry_num_message)

                next_hop_message = "\nPlease enter the diversion next-hop for this customer: "
                next_hop = data_validation(next_hop_message)

                marvel_message = "\nIs this a Marvel order? (y/n): "
                marvel = data_validation(marvel_message)
                marvel = re.match(yesPattern, marvel)

                dm_message = "\nIs this a DM order? (y/n): "
                dm_order = data_validation(dm_message)
                dm_order = re.match(yesPattern, dm_order)

                uppercase_message = "\nFor the prefix list name, is AORC capatilized? (y/n)"
                uppercase = data_validation(uppercase_message)
                uppercase = re.match(yesPattern, uppercase)



            else:
                entry_num = '0'
                next_hop = '192.168.192.168'
                marvel_message = "\nIs this a Marvel order? (y/n): "
                dm_message = "\nIs this a DM order? (y/n): "
                uppercase_message = "\nFor the prefix list name, is AORC capatilized? (y/n)"

                marvel = data_validation(marvel_message)
                marvel = re.match(yesPattern, marvel)

                dm_order = data_validation(dm_message)
                dm_order = re.match(yesPattern, dm_order)

                uppercase = data_validation(uppercase_message)
                uppercase = re.match(yesPattern, uppercase)

            print('\nThe information that you have entered:')
            print('Prefixes: ' + str(value))
            print('Customer Name: ' + customer_name)
            print('Bus Org ID: ' + bus_org_id)
            if entry_num != '0':
                print('Next Available Nokia Policy Entry Number: ' + entry_num)
                print('Next Hop Diversion IP: ' + next_hop)
            if marvel:
                print('You have indicated that this is a Marvel order.')
            if dm_order:
                print('You have indicated that this is a DM order.')
            if uppercase:
                print('You have indicated that AORC should be capatilized at the beginning of the prefix list name.')


        else:
            print("Farewell")
            break

        isCorrect_message = "\nAre the above values correct? (y/n): "
        isCorrect = data_validation(isCorrect_message)
        isCorrectMatch = re.match(yesPattern, isCorrect)

        if not isCorrectMatch:
            continue

        prefix_list = list_name_generator(customer_name, bus_org_id, marvel, dm_order, uppercase)

        if user_choice == "1":
            # Change "devices" to "test_devices" if you want to use the spare PE devices for testing
            for each in devices:
                if each["manufacturer"] == "Nokia":
                    add_to_prefix_list_nokia(each["dns"], route_attributes, prefix_list, entry_num, next_hop, isNew)
                elif each["manufacturer"] == "Juniper":
                    add_to_prefix_list_juniper(each["dns"], route_attributes, prefix_list, next_hop, isNew)
            for each in devices:
                if each["manufacturer"] == "Nokia":
                    push_file(each["dns"], save)
                    print('\nSaving config on device ' + each['dns'])
        # Change "devices" to "test_devices" if you want to use the spare PE devices for testing
        if user_choice == "2":
            for each in devices:
                if each["manufacturer"] == "Nokia":
                    rem_from_prefix_list_nokia(each["dns"], route_attributes, prefix_list, entry_num, next_hop, isDisco)
                if each["manufacturer"] == "Juniper":
                    rem_from_prefix_list_juniper(each["dns"], route_attributes, prefix_list, next_hop, isDisco)
            for each in devices:
                if each["manufacturer"] == "Nokia":
                    push_file(each["dns"], save)
                    print('\nSaving config on device ' + each['dns'])

    os.unlink(pid_file)
    if pid == str(os.getpid()):
        os.kill(int(pid), signal.SIGKILL)


# The script will timeout after the duration, in seconds, is exceeded.
# This should prevent someone from starting the script and keeping it locked indefinitely.
def timeout():
    print('Timed Out')


signal.signal(signal.SIGALRM, timeout)

signal.alarm(duration)

if debug == True:
    user_menu()
else:
    try:
        user_menu()
    except:
        print('Your session has timed out. Goodbye.')

# user_menu()