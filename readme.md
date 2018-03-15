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
2. Move `main.py` and `requirements.txt` to your server.
3. Install requirements with `pip3 install -r requirements.txt`
4. Add your bot as admin to your telegram channel, and change the channelname in `main.py` to the name of your channel or solely use a Telegram UserId and get private Messages.
5. Setup a cronjob: `*/5 * * * * python3 /home/path_to_main/main.py <token>` and add your taken instead of `<token>`. You should receive all Feed items, within the bot's first scan.


## How do I use this project?

### Usage

This script takes the Telegram API token as an argument:

```shell
python main.py <YOUR_SECRET>
```

After the first scan, there should be a `save.txt` in the directory. It saves the last update.

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
