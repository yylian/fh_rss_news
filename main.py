import feedparser
import datetime
import time
import telepot
from pprint import pprint
import os.path


def get_last_update():

    with open('save.txt', 'r') as file:
        date_string = file.read()

    parsed_update = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

    return parsed_update


def get_rss_feed_from_url(url):

    complete_feed = feedparser.parse(url)

    return complete_feed


def get_entries(feed_dict):

    entries_from_feed = feed_dict['entries']

    return entries_from_feed


def check_update(first_entry_date, last_update):

    formatted_first_entry_date = datetime.datetime(*first_entry_date[:6])
    first_entry_is_not_changed = formatted_first_entry_date == last_update

    if first_entry_is_not_changed:

        print('No updates!')

        return True

    else:

        update_date(formatted_first_entry_date)
        return False


def update_date(date):

    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')

    with open('save.txt', 'w') as file:

        file.write(formatted_date)


def get_new_articles(old_date, entries):

    items_wich_need_to_be_sent = []

    for entry in entries:

        entry_time = entry['published_parsed']
        formatted_entry_time = datetime.datetime(*entry_time[:6])

        print(formatted_entry_time)
        print(old_date)

        reached_old_entry = old_date == formatted_entry_time

        if reached_old_entry:

            print('hi')

            return items_wich_need_to_be_sent

        else:

            items_wich_need_to_be_sent.append(entry)


def write_update(message):

    date_time = datetime.datetime.today()
    date = date_time.date()
    time = date_time.time()
    log_isnt_created = not os.path.isfile(f'log-{date}.txt')

    if log_isnt_created:

        with open(f'log-{date}.txt', 'w') as file:

            file.write(f'logs from {date} \n')

    with open(f'log-{date}.txt', 'a') as file:

        file.write(f'{time}: {message}\n')






def main():

    rss_feed_url = 'http://www.inf.fh-dortmund.de/rss.php'
    token = 'TOKEN'
    bot = telepot.Bot(token)

    complete_feed = get_rss_feed_from_url(rss_feed_url)
    entries = get_entries(complete_feed)

    first_entry_date = entries[0]['published_parsed']
    last_update = get_last_update()

    if check_update(first_entry_date, last_update):

        return

    unsend_messages = get_new_articles(last_update, entries)

    for message in unsend_messages:

        pprint(message)
        title = message['title']
        timex = message['published_parsed']
        timex = datetime.datetime(*timex[:6])
        timex = timex.strftime("%d. %B %Y - %H:%M:%S")
        title = title + ':\n\n'
        summary = message['summary'].replace('<br />', '')
        lolz = title + summary + '\n\n' + timex
        bot.sendMessage(TOKEN, lolz)
        time.sleep(1)


if '__main__' == __name__:

    try:

        main()
        write_update('Everything ok')

    except Exception:

        write_update('Failed')

# 2017-10-24 9:24:24 letzter eintrag
