from datetime import datetime, timedelta
import calendar

users = [{"name": "Bill", "birthday": datetime(year=2012, month=11, day=8)},
         {"name": "Jill", "birthday": datetime(year=2009, month=11, day=12)},
         {"name": "Kim", "birthday": datetime(year=2009, month=11, day=9)},
         {"name": "Jan", "birthday": datetime(year=2009, month=11, day=13)},
         {"name": "Jan__", "birthday": datetime(year=2009, month=11, day=22)}]

weekdays = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}


def get_birthdays_per_week(users):
    users_ = users
    сurrent_day = datetime.today()
    сurrent_day = сurrent_day.date()
    week = timedelta(weeks=1)
    week += сurrent_day
    for i in users_:
        a = i["birthday"].strftime('%Y %B %d')
        a = a.split(' ')
        a[0] = str(datetime.today().year)
        a[0] = ' '.join(a)
        i["birthday"] = datetime.strptime(a[0], '%Y %B %d')

        day_ = calendar.day_name[i["birthday"].weekday()]
        if сurrent_day < i["birthday"].date() < week:
            if calendar.day_name[i["birthday"].weekday()] in weekdays.keys():
                weekdays[day_].append(i["name"])
            else:
                weekdays['Monday'].append(i["name"])
    for k, v in weekdays.items():
        if len(v) != 0:
            v = ', '.join(v)
            print(f'{k}: {v}')


if __name__ == "__main__":
    get_birthdays_per_week(users)
