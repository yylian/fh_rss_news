import feedparser
from telegram.ext import Updater
from telegram import ParseMode
from markdownify import markdownify as md
import sys
import time
from datetime import datetime


DESCRIPTION_APPENDIX = ' This channel regularly posts the news from https://www.fh-dortmund.de/de/fb/4/aktuelles.php Source: https://github.com/yylian/fhd_news'


class Entry:

    def __init__(self, title, text, date):

        self.title = title
        self.text = text
        self.date = date

    def __str__(self):

        message = ''

        clean_title = self.title.replace('*', '')
        clean_title = clean_title.replace('_', '')
        clean_title = clean_title + ':'
        bold_title = f'*{clean_title}*'
        full_title = bold_title + '<br /><br />'
        text = self.text
        text = text + '<br />'
        text = text.replace('*', '')
        clean_text = text.replace('_', '')
        date = self.date.strftime('%d. %B %Y - %H:%M:%S')

        message = message + full_title
        message = message + clean_text
        message = message + date
        message = md(message)
        message = message.replace('\n ', '\n')

        return message


def main(bot, chat_id):

    rss_feed = get_rss_content()
    all_entries = get_entries(rss_feed)
    last_message_date = get_last_message_date(bot, chat_id)

    entries = filter_entries(all_entries, last_message_date)
    send_messages(entries, bot, chat_id)


def get_telegram_token():

    try:

        token = sys.argv[1]

    except IndexError:

        raise ValueError('No token given')

    return token


def get_rss_content():

    url = 'http://www.inf.fh-dortmund.de/rss.php'
    rss_feed = feedparser.parse(url)

    return rss_feed


def get_entries(rss_content):

    entries = rss_content['entries']
    formatted_entries = []

    for entry in entries:

        title = entry['title']
        text = entry['summary']
        timestamp = entry['published_parsed']
        date = datetime.fromtimestamp(time.mktime(timestamp))
        new_entry = Entry(title, text, date)

        formatted_entries.append(new_entry)

    return formatted_entries


def get_last_message_date(bot, chat_id):

    message = bot.getChat(chat_id=chat_id).description
    last_date = ''

    if message.endswith(DESCRIPTION_APPENDIX):

        position_to_cut_appendix = -1 * len(DESCRIPTION_APPENDIX)
        last_date = message[:position_to_cut_appendix]

    return last_date


def set_last_message_date(bot, message, chat_id):

    date = message.date.strftime('%Y-%m-%dT%H:%M:%SZ')

    message = date + DESCRIPTION_APPENDIX

    bot.set_chat_description(chat_id, message)


def filter_entries(raw_entries, last_message_date):

    entries = []

    for entry in raw_entries:

        date = entry.date.strftime('%Y-%m-%dT%H:%M:%SZ')

        if date == last_message_date:

            return entries

        entries.append(entry)

    return entries


def send_messages(entries, bot, chat_id):

    if not entries:

        return

    last_message = entries[0]

    set_last_message_date(bot, last_message, chat_id)

    for entry in reversed(entries):

        message = str(entry)

        bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)

        time.sleep(1)


if __name__ == '__main__':

    chat_id = -1001190575483
    token = get_telegram_token()
    bot = Updater(token=token, use_context=True).bot

    main(bot, chat_id)
