# Shade, my personal Discord bot, written in Python, using Discord.py

## Instalation

Clone this repository, and install the dependencies by using `python3 -m pip install -r requirements.txt` or (if you are in Windows) `py -m pip install -r requirements.txt`. Once everything is installed, you can start the bot by running the `main.py` file.

## Configuration File

There's a hidden file that stores sensitive information, called `config.py`. If you want to run the bot, you must create it inside of the bot's folder.

This is how it looks like:

```py
token = '' # Your bot's Discord token
guild_id = '' # The development server ID
app_id = '' # The ID of your bot
dev_id = '' # Your own ID
cat_api_key = '' # The API Key for https://thecatapi.com
```

You will be able to use the configuration variables inside of other files by using `self.bot.config` property.