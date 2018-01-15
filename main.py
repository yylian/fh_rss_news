import feedparser
import datetime
import time
import telepot
import os.path


def get_last_update():

    with open('/home/rss_feed_fh/save.txt', 'r') as file:

        unparsed_last_update = file.read()

    last_update = datetime.datetime.strptime(unparsed_last_update, '%Y-%m-%d %H:%M:%S')

    return last_update


def get_rss_feed_from_url(url):

    rss_feed = feedparser.parse(url)

    return rss_feed


def get_entries(rss_feed):

    entires = rss_feed['entries']

    return entires


def check_update(first_entry_date, last_update_date):

    first_entry_is_not_changed = first_entry_date == last_update_date

    if first_entry_is_not_changed:

        return False

    else:

        update_date(first_entry_date)

        return True


def update_date(date):

    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')

    with open('/home/rss_feed_fh/save.txt', 'w') as file:

        file.write(formatted_date)


def get_new_articles(old_date, entries):

    items_wich_need_to_be_sent = []

    for entry in entries:

        entry_time = entry['published_parsed']
        formatted_entry_time = datetime.datetime(*entry_time[:6])
        reached_old_entry = old_date == formatted_entry_time

        if reached_old_entry:

            return items_wich_need_to_be_sent

        else:

            items_wich_need_to_be_sent.append(entry)


def write_update(message):

    date_time = datetime.datetime.today()
    current_date = date_time.date()
    current_time = date_time.time()
    log_isnt_created = not os.path.isfile('/home/rss_feed_fh/log-{}.txt'.format(current_date))

    if log_isnt_created:

        with open('/home/rss_feed_fh/log-{}.txt'.format(current_date), 'w') as file:

            file.write('/home/rss_feed_fh/logs from {} \n'.format(current_date))

    with open('/home/rss_feed_fh/log-{}.txt'.format(current_date), 'a') as file:

        file.write('{}: {}\n'.format(current_time, message))


def send_messages(bot, unsend_messages, adress):

    correct_oder_list = reversed(unsend_messages)

    for message in correct_oder_list:

        title = message['title']
        timex = message['published_parsed']
        timex = datetime.datetime(*timex[:6])
        timex = timex + datetime.timedelta(hours=1)
        timex = timex.strftime("%d. %B %Y - %H:%M:%S")
        title = title + ':\n\n'
        summary = message['summary'].replace('<br />', '')
        message = title + summary + '\n\n' + timex
        bot.sendMessage(adress, message)
        time.sleep(1)


def main():

    adress = '@fh_dortmund_aktuelles'
    rss_feed_url = 'http://www.inf.fh-dortmund.de/rss.php'
    token = 'TOKEN'

    bot = telepot.Bot(token)

    complete_feed = get_rss_feed_from_url(rss_feed_url)
    entries = get_entries(complete_feed)

    first_entry_date = entries[0]['published_parsed']
    formatted_first_entry_date = datetime.datetime(*first_entry_date[:6])
    last_update = get_last_update()

    update_available = check_update(formatted_first_entry_date, last_update)

    if update_available:

        unsend_messages = get_new_articles(last_update, entries)
        send_messages(bot, unsend_messages, adress)


if '__main__' == __name__:

    try:

        main()

    except Exception:

        write_update('Failed')

# 2017-10-24 9:24:24 letzter eintrag
