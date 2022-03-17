#!/home/rblackwe/menv_sbux/bin/python
import curses
import sys
import requests
import json
import time
import grt

encoding = 'utf-8'
headers = grt.headers
store_url = grt.store_url
mac_url = grt.mac_url
suspend_url = grt.suspend_url

mac_banner = ['------------------------------', 'Enter MAC address below', '------------------------------']
store_choices = ['Enable/Disable Wi-Fi schedule', 'Home Menu']


def convert(n):
    return time.strftime("%I:%M %p", time.gmtime(n))


def set_width(n, w):
    while len(n) < w:
        n += " "
    return n


def get_store_data(store):
    payload = {}
    store = str(store)
    url = store_url + store
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text.encode('utf8'))
    data = json.loads(response.content.decode())
    # print (json.dumps(data,indent=2))
    return data


def suspend_store(stdscr, store, hours):
    store = str(store)
    hours = int(hours)
    # url = suspend_url + str(store)

    actionpayload = {"stores": [store], "suspend_hours": hours}
    actionjson = json.dumps(actionpayload)
    actionresponse = requests.request("POST", suspend_url, headers=headers, data=actionjson)
    actiondata = json.loads(actionresponse.content.decode())

    return actiondata


def hours_prompt(stdscr, store):
    menu_hours = ["------- Afterhours Wi-Fi Disable/Enable -------", ""]
    menu_hours.append("Store number: " + store)
    menu_hours.append("How many hours would you like to disable this for?")
    menu_hours.append("Enter 1 - 72, or 0 to cancel")
    menu_hours.append('')
    stdscr.clear()
    offset = 0
    print_menu_store(stdscr, menu_hours, offset)

    while 1:
        h, w = stdscr.getmaxyx()
        prompt_get = "Hour(s): "
        prompt_invalid = "Invalid number of hours: "
        x = w // 2
        y = h // 2 - len(menu_hours) // 2 + len(menu_hours) - offset + 1
        curses.curs_set(1)
        hours = my_raw_input(stdscr, y, x - len(prompt_get) // 2, prompt_get)
        curses.curs_set(0)
        if int(hours) <= 72 and int(hours) >= 1:
            return int(hours)
        elif int(hours) == 0:
            stdscr.clear()
            main(stdscr)
        else:
            stdscr.clear()
            stdscr.addstr(y + 1, x - len(prompt_invalid) // 2 - 3, prompt_invalid + str(hours))
        print_menu_store(stdscr, menu_hours, 0)


def toggle_prompt(stdscr, store, schedule_status):
    stdscr.refresh()
    menu_toggle = ["------- Afterhours Wi-Fi Disable/Enable -------", ""]
    if schedule_status == False:
        menu_toggle.append("Are you sure you want to DISABLE the W-Fi schedule?")
        menu_toggle.append("")
        menu_toggle.append('----------------------------------------------')
        menu_toggle.append("YES")
        menu_toggle.append("NO!")
    else:
        menu_toggle.append("Are you sure you want to ENABLE the W-Fi schedule?")
        menu_toggle.append("")
        menu_toggle.append('----------------------------------------------')
        menu_toggle.append("YES")
        menu_toggle.append("NO!")
    return menu_toggle


def toggle_wifi_branch(stdscr, store, schedule_status):
    if schedule_status == True:
        hours = 0
    else:
        hours = hours_prompt(stdscr, store)

    menu_toggle = toggle_prompt(stdscr, store, schedule_status)

    success_prompt = ['Store number: ' + store, 'Store schedule successfully changed!']
    no_success_prompt = ['Store number: ' + store, 'Store schedule was NOT changed!']

    current_row_idx = len(menu_toggle) - 1
    stdscr.clear()
    print_formatted_store(stdscr, menu_toggle, current_row_idx, 0)

    while 1:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > len(menu_toggle) - 3:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu_toggle) - 1:
            current_row_idx += 1
        elif key == curses.KEY_EXIT or key == 27:
            break
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row_idx == len(menu_toggle) - 2:  # select store menu
                actiondata = suspend_store(stdscr, store, hours)
                stdscr.clear()
                if actiondata['success'] == True and actiondata['stores_updated'] == 1:
                    print_menu_store(stdscr, success_prompt, 0)
                else:
                    print_menu_store(stdscr, no_success_prompt, 0)
                time.sleep(2)
                main(stdscr)
            if current_row_idx == len(menu_toggle) - 1:  # select store menu
                main(stdscr)
            stdscr.refresh()

        print_formatted_store(stdscr, menu_toggle, current_row_idx, 0)


def print_formatted_store(stdscr, menu, current_row_idx, offset):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx - offset
        if idx == current_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def fmt_store_data(data):
    formatted_store_data = ['----------------- Store Info -----------------', '']
    formatted_store_data.append("Store Number: " + str(data["id"]))
    formatted_store_data.append("Name: " + str(data["name"]) + "  Store Status: " + str(data["status_code"]))
    formatted_store_data.append("Timezone Offset GMT: " + str(int(data["offset"] / 3600)) + "  Grace period: " + str(
        int(data["grace_time"] / 3600)) + " hour(s)")
    if data["disable_schedule"] == False:
        formatted_store_data.append("Wi-Fi Schedule is currently ENABLED")
    else:
        formatted_store_data.append("Wi-Fi Schedule is currently DISABLED")
    formatted_store_data.append('')
    # Format and print wifi hours313
    n = data["wifi_schedule"]
    daysofweek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for idx, i in enumerate(n):
        if n[i] == False:
            formatted_store_data.append(set_width(daysofweek[int(i) - 1], 10) + " : Store Closed")
        else:
            for q in reversed(n[i]):
                formatted_store_data.append(
                    set_width(daysofweek[int(i) - 1], 10) + " : " + convert(q["o"]) + " - " + convert(q["c"]))
    formatted_store_data.append('')
    formatted_store_data.append('----------------------------------------------')
    if data["disable_schedule"] == False:
        formatted_store_data.append("Disable Wi-Fi schedule")
    else:
        formatted_store_data.append("Enable Wi-Fi schedule")
    formatted_store_data.append('Home Menu')
    return formatted_store_data


def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo()
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr()
    return input


def print_menu_store(stdscr, menu, offset):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx - offset
        stdscr.addstr(y, x, row)

    stdscr.refresh()



def store_branch(stdscr, message):
    stdscr.clear()
    stdscr.addstr(0, 0, "You selected " + message)

    get_store_banner = ['----------------------------------------------',
                        'Enter store number below', 'Remove the leading "S". Example "5233"',
                        '----------------------------------------------']
    print_menu_store(stdscr, get_store_banner, 6)
    i_want_to_loop = True
    while i_want_to_loop:
        h, w = stdscr.getmaxyx()
        prompt_get = "Store number: "
        prompt_valid = "Store number is valid: "
        prompt_invalid = "Store number is NOT valid: "
        x1 = w // 2 - len(prompt_get) // 2
        x2 = w // 2 - len(prompt_valid) // 2
        x3 = w // 2 - len(prompt_invalid) // 2
        y = h // 2 - 2
        curses.curs_set(1)
        store = my_raw_input(stdscr, y, x1, prompt_get)
        curses.curs_set(0)
        store = store.decode(encoding)
        if 3 <= len(store) < 7 and store[0].lower() == 's':
            stdscr.addstr(y + 1, x2, prompt_valid + store + " " + store[1:])
            store_id = store[1:]
            store_data = get_store_data(store_id)
            if 'error' in store_data:
                stdscr.clear()
                stdscr.addstr(y - 1, x3, prompt_invalid + store)
            else:
                i_want_to_loop = False
        elif 3 <= len(store) < 6:
            stdscr.addstr(y + 1, x2, prompt_valid + store)
            store_id = store
            store_data = get_store_data(store_id)
            if 'error' in store_data:
                stdscr.clear()
                stdscr.addstr(y - 1, x3, prompt_invalid + store)
            else:
                i_want_to_loop = False
        elif len(store) == 0:
            main(stdscr)
        else:
            stdscr.clear()
            stdscr.addstr(y - 1, x3, prompt_invalid + store)

        print_menu_store(stdscr, get_store_banner, 5)


    if 'id' in store_data:
        formatted_store_data = fmt_store_data(store_data)

        current_row_idx = len(formatted_store_data) - 2
        stdscr.clear()
        print_formatted_store(stdscr, formatted_store_data, current_row_idx, 0)

        while 1:
            key = stdscr.getch()
            stdscr.clear()
            if key == curses.KEY_UP and current_row_idx > len(formatted_store_data) - 3:
                current_row_idx -= 1
            elif key == curses.KEY_DOWN and current_row_idx < len(formatted_store_data) - 1:
                current_row_idx += 1
            elif key == curses.KEY_EXIT or key == 27:
                break
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_row_idx == len(formatted_store_data) - 2:  # select store menu
                    toggle_wifi_branch(stdscr, store_id, store_data["disable_schedule"])
                if current_row_idx == len(formatted_store_data) - 1:  # select store menu
                    main(stdscr)

            print_formatted_store(stdscr, formatted_store_data, current_row_idx, 0)
    elif 'error' in store_data:
        stdscr.clear()
        stdscr.addstr(0, 0, "The store you selected '" + store_id + "' is not in the database")
        stdscr.addstr(1, 0, "Press enter to try again")
    else:
        stdscr.clear()
        main(stdscr)


def print_menu_main(stdscr, menu, current_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == current_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    menu_main = ['==============================', 'GRT API Script', '==============================', '',
                 'Store Lookup', 'MAC Lookup', 'Exit']
    current_row_idx = len(menu_main) - 3
    print_menu_main(stdscr, menu_main, current_row_idx)

    while True:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > len(menu_main) - 3:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu_main) - 1:
            current_row_idx += 1
        elif key == curses.KEY_EXIT or key == 27:
            sys.exit(0)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row_idx == len(menu_main) - 3:  # select store menu
                store_branch(stdscr, "User selected '" + menu_main[current_row_idx] + "'")

            if current_row_idx == len(menu_main) - 2:  # select mac lookup
                stdscr.addstr(0, 0, "User selected '" + menu_main[current_row_idx] + "'")
            if current_row_idx == len(menu_main) - 1:  # Exit
                sys.exit(0)
            # stdscr.addstr(0,0,"You pressed {}".format(menu[current_row_idx]))
            stdscr.refresh()
            stdscr.getch()

        print_menu_main(stdscr, menu_main, current_row_idx)


curses.wrapper(main)
