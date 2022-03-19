from abc import ABC
import time
from typing import Union

SUNDAY = 0
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6


class OpenningClosingTimes:
    def __init__(self, openning, closing):
        self.openning = openning
        self.closing = closing


class WeeklySchedule:
    def __init__(self, sunday=None, monday=None, tuesday=None, wednesday=None, thursday=None, friday=None,
                 saturday=None):
        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.all = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]

    def get_all(self):
        return self.all

    def set_day_closed(self, day):
        if 0 <= day < 7:
            self.all[day] = None
        raise RuntimeError("in valid day number {}".format(day))

    def set_by_day(self, day, openning, closing):
        if 0 <= day < 7:
            self.all[day] = OpenningClosingTimes(openning, closing)
        raise RuntimeError("in valid day number {}".format(day))

    def get_by_day(self, day):
        if 0 <= day < 7:
            return self.all[day]
        raise RuntimeError("in valid day number {}".format(day))


class StoreRecord:
    def __init__(self, id, name, status_code, offset, grace_time, schedule_is_disabled, wifi_schedule,
                 wifi_schedule_suspension):
        self.id = id
        self.name = name
        self.status_code = status_code
        self.offset = offset
        self.grace_time = grace_time
        self.schedule_is_disabled = schedule_is_disabled
        self.wifi_schedule = wifi_schedule
        self.wifi_schedule_suspension = wifi_schedule_suspension
        pass


t_6_8 = OpenningClosingTimes(time.strptime("6:00", "%H:%M"), time.strptime("20:00", "%H:%M"))
t_7_6 = OpenningClosingTimes(time.strptime("7:00", "%H:%M"), time.strptime("18:00", "%H:%M"))
seven_day_schedule = WeeklySchedule(t_6_8, t_6_8, t_6_8, t_6_8, t_6_8, t_6_8, t_6_8, )
five_day_schedule = WeeklySchedule(sunday=None, saturday=None, monday=t_7_6, tuesday=t_7_6, wednesday=t_7_6,
                                   thursday=t_7_6, friday=t_7_6)


store_database = [
    StoreRecord("S87601", "store_01", "some_status", 0, 0, False, seven_day_schedule, 0),
    StoreRecord("S87602", "store_02", "some_status", 0, 0, False, seven_day_schedule, 0),
    StoreRecord("S87603", "store_03", "some_status", 0, 0, False, five_day_schedule, 0),
]


class StoreDatabase:
    @classmethod
    def get_store(cls, ident: str) -> Union[None, StoreRecord]:
        global store_database
        for store in store_database:
            if ident == store.id:
                return store
        return None
