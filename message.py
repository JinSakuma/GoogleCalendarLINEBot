import datetime


def get_time_range(text):
    t_start = None
    t_end = None
    d = None
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    tod = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0)
    if ("スケジュール" in text) or ("予定" in text):
        if "明日" in text:
            d = "明日"
            tom = tod + datetime.timedelta(days=1)
            t_start = tom.isoformat()+'Z'
            t_end = datetime.datetime(tom.year, tom.month, tom.day, 23, 59, 59, 999999).isoformat()+'Z'
        elif "昨日" in text:
            d = "昨日"
            yes = tod - datetime.timedelta(days=1)
            t_start = yes.isoformat()+'Z'
            t_end = datetime.datetime(yes.year, yes.month, yes.day, 23, 59, 59, 999999).isoformat()+'Z'
        elif "今週" in text:
            d = "今週"
            dw = now.weekday()
            t_start = tod.isoformat()+'Z'
            nxt = tod + datetime.timedelta(days=6-dw)
            t_end = datetime.datetime(nxt.year, nxt.month, nxt.day, 23, 59, 59, 999999).isoformat()+'Z'
        elif "来週" in text:
            d = "来週"
            dw = now.weekday()
            nxt = tod + datetime.timedelta(days=7)
            t_start = nxt.isoformat()+'Z'
            t_end = datetime.datetime(nxt.year, nxt.month, nxt.day+7, 23, 59, 59, 999999).isoformat()+'Z'
        elif "先週" in text:
            d = "先週"
            dw = now.weekday()
            nxt = tod - datetime.timedelta(days=7)
            t_start = nxt.isoformat()+'Z'
            t_end = datetime.datetime(nxt.year, nxt.month, nxt.day+7, 23, 59, 59, 999999).isoformat()+'Z'
        else:
            d = "今日"
            t_start = tod.isoformat()+'Z'
            t_end = datetime.datetime(now.year, now.month, now.day, 23, 59, 59, 999999).isoformat()+'Z'

    return t_start, t_end, d


def get_reply(events, d):
    if not events:
        reply = '予定はありません'
    else:
        reply = d+"の予定は\n"
        events_num = len(events)
        for i, event in enumerate(events):
            s_time_list = event['start'].get('dateTime', event['start'].get('date')).replace("-"," ").replace("T"," ").replace("+"," ").split(" ")
            e_time_list = event['end'].get('dateTime', event['start'].get('date')).replace("-"," ").replace("T"," ").replace("+"," ").split(" ")
            if len(s_time_list) == 5:
                s_year, s_month, s_day, s_hour, _ = s_time_list
                e_year, e_month, e_day, e_hour, _ = e_time_list
                if (s_month == e_month) and (s_day == e_day):
                    s_date = str(int(s_month))+'/'+s_day+' '+":".join(s_hour.split(":")[:-1])
                    e_date = ":".join(e_hour.split(":")[:-1])
                else:
                    s_date = str(int(s_month))+'/'+s_day+' '+":".join(s_hour.split(":")[:-1])
                    e_date = str(int(e_month))+'/'+e_day+' '+":".join(e_hour.split(":")[:-1])

                reply += s_date+"~"+e_date+" "+event['summary']

            else:
                s_year, s_month, s_day = s_time_list
                e_year, e_month, e_day = e_time_list
                if (s_month == e_month) and (s_day == e_day):
                    s_date = str(int(s_month))+'/'+s_day
                    reply += s_date+" "+event['summary']
                else:
                    s_date = str(int(s_month))+'/'+s_day
                    e_date = str(int(e_month))+'/'+e_day
                    reply += s_date+"~"+e_date+" "+event['summary']

            if i != events_num - 1:
                reply += "\n"

    return reply


def get_message(data):
    message = "今日の予定は\n"
    data_len = len(data)
    for i, event in enumerate(data):
        s_time_list = event['start'].replace("-", " ").replace("T", " ").replace("+", " ").split(" ")
        e_time_list = event['end'].replace("-", " ").replace("T", " ").replace("+", " ").split(" ")
        if len(s_time_list) == 4:
            s_year, s_month, s_day, s_hour = s_time_list
            e_year, e_month, e_day, e_hour = e_time_list
            if (s_month == e_month) and (s_day == e_day):
                s_date = str(int(s_month))+'/'+s_day+' '+":".join(s_hour.split(":")[:-1])
                e_date = ":".join(e_hour.split(":")[:-1])

            else:
                s_date = str(int(s_month))+'/'+s_day+' '+":".join(s_hour.split(":")[:-1])
                e_date = str(int(e_month))+'/'+e_day+' '+":".join(e_hour.split(":")[:-1])

            message += s_date+"~"+e_date+" "+event['summary']

        else:
            s_year, s_month, s_day = s_time_list
            e_year, e_month, e_day = e_time_list
            if (s_month == e_month) and (s_day == e_day):
                s_date = str(int(s_month))+'/'+s_day
                message += s_date+" "+event['summary']
            else:
                s_date = str(int(s_month))+'/'+s_day
                e_date = str(int(e_month))+'/'+e_day
                message += s_date+"~"+e_date+" "+event['summary']

        if i != data_len - 1:
            message += "\n"

    return message
