# FH RSS Newsfeed - Telegram Bot

## What are the goals of this project?

This Python script provides university newsfeeds as a Telegram bot.

## Relevant URLs

* https://www.fh-dortmund.de/de/fb/4/aktuelles.php - RSS feed of the university
* https://t.me/fh_dortmund_aktuelles - The channel which the Bot publishes to

## How do I set this project up?

### Prerequesites

* Python 3.4

### Setup/Installation

1. Create a bot in Telegram, use Botfather, save the token.
2. Check the RSS feed for the latest added Message and adjust the save.txt to the date from the feed.
3. Move `main.py`, `requirements.txt`, and `save.txt` to your server.
4. Install requirements with `pip3 install -r requirements.txt`
5. Add your bot as admin to your telegram channel, and change the channelname in `main.py` to the name of your channel.
6. Setup a cronjob: `*/5 * * * * python3 /home/path_to_main/main.py <token>`, you should get the first messages if you change the date in `save.txt` to the previous message from the feed.


## How do I use this project?

### Usage

This script takes the Telegram API token as an argument:

```shell
python main.py <YOUR_SECRET>
```

`TODO: add more usage`

## Contributing

1. [Fork it!](http://github.com/hitim/fh_rss_news/fork)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

### Author/Contact information

Julian Jarminowski (@hitim)

### Licences

MIT.
