import feedparser
import datetime
import time
import telepot
import os.path
import sys


def get_telegram_token():

    try:

        token = sys.argv[1]

    except IndexError:

        raise ValueError('No token given')

    return token


def get_filepath(filename):

    working_directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(working_directory, filename)

    return filepath


def get_last_update():

    filepath = get_filepath('save.txt')

    file_isnt_created = os.path.isfile(filepath) is False

    if file_isnt_created:

        with open(filepath, 'w') as file:

            file.write('2000-01-01 00:00:00')

    with open(filepath, 'r') as file:

        unparsed_last_update = file.read()
        clean_last_update = remove_newlines(unparsed_last_update)

    last_update = datetime.datetime.strptime(clean_last_update, '%Y-%m-%d %H:%M:%S')

    return last_update


def remove_newlines(string):

    if string.endswith('\n'):

        string.strip('\n')

    return string


def get_rss_feed_from_url(url):

    rss_feed = feedparser.parse(url)

    return rss_feed


def get_entries(rss_feed):

    entires = rss_feed['entries']

    return entires


def check_update(first_entry_date, last_update_date):

    update_exists = first_entry_date > last_update_date

    return update_exists


def update_date(date):

    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    filepath = get_filepath('save.txt')

    with open(filepath, 'w') as file:

        file.write(formatted_date)


def get_new_articles(old_date, entries):

    items_wich_need_to_be_sent = []

    for entry in entries:

        unformatted_entry_time = entry['published_parsed']
        entry_time = datetime.datetime(*unformatted_entry_time[:6])
        reached_old_entry = old_date >= entry_time

        if reached_old_entry:

            return items_wich_need_to_be_sent

        else:

            items_wich_need_to_be_sent.append(entry)

    return items_wich_need_to_be_sent


def write_update(message):

    date_time = datetime.datetime.today()
    current_date = date_time.date()
    current_time = date_time.time()

    filename = 'log-{}.txt'.format(current_date)
    filepath = get_filepath(filename)

    log_isnt_created = os.path.isfile(filepath) is False

    if log_isnt_created:

        with open(filepath, 'w') as file:

            file.write('logs from {}'.format(current_date))
            file.write('\n')

    with open(filepath, 'a') as file:

        file.write('{}: {}'.format(current_time, message))
        file.write('\n')


def send_messages(bot, unsend_messages, address):

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
        bot.sendMessage(address, message)
        time.sleep(1)


def main():

    address = '@fh_dortmund_aktuelles'
    rss_feed_url = 'http://www.inf.fh-dortmund.de/rss.php'
    token = get_telegram_token()

    bot = telepot.Bot(token)

    complete_feed = get_rss_feed_from_url(rss_feed_url)
    entries = get_entries(complete_feed)

    unformatted_first_entry_date = entries[0]['published_parsed']
    first_entry_date = datetime.datetime(*unformatted_first_entry_date[:6])
    last_update = get_last_update()

    update_available = check_update(first_entry_date, last_update)

    if update_available:

        unsend_messages = get_new_articles(last_update, entries)
        send_messages(bot, unsend_messages, address)
        update_date(first_entry_date)


if '__main__' == __name__:

    try:

        main()

    except Exception as error:

        write_update('Failed: {}'.format())
