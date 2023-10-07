# Multilanguage Telegram Bot

This skeleton project implements base functions for multilanguage bot 
with administrator panel and AsyncIOScheduler functionality.
---
> Directory structure and file locations


- root
  - database
    - __init__.py
    - blogger_bot.db         - automatically created SQLight database
    - sql.py                 - base **SQL commands** for specific database manipulations
    - user_info.py           - **class UserInfo**  stores minimal user information in a database and provides a simple interface to retrieve this information. For example, the `get_language()` function is used to select the language of the bot messages...
  - private
    - .gitignore
    - __init__.py
    - tokens.py              - Any secret tokens **should** be stored in this file. For example, the variable 
                               `CLIENT_BOT_TOKEN = "unoque.telegram.bot.token"` should contain the token of your telegram bot
  - shared
    - __init__.py
    - admin_panel.py         - contains the _/admin_ command handler and command handlers for stopping and restarting the scheduler, as well as a function for creating an inline keyboard
    - callback_factory       - contains all callback class definitions
    - config.py              - Main application configuration file. The **Config** class contains class variables that define the functionality of the bot
    - content_manage.py      - Contains extensible functionality for creating content intended for distribution to users and broadcasting it to predefined channels
    - content_provider.py    - Contains the **ContentProvider class** that implements the task scheduler, as well as functions for stopping and restarting, which are called from the file _**admin_panel.py**_
    - language_selector.py   - Implements functionality for selecting and changing the user interface language. The selected language ID is saved in the database for later use by all client-facing bot functions
    - message.py             - Contains three message **lists**, one for each supported language (Russian, English and Hebrew), as well as the **MultiLang class**, which implements the functionality of displaying messages in accordance with the selected language. When expanding the functionality of the bot, add the messages you need to this file in the corresponding lists
    - scheduler_manage.py    - Contains functionality for setting the trigger time of the content distribution scheduler
  - src
    - __init__.py
    - bot_commands.py        - Contains a list of commands recognized by the bot, which is transmitted to the telegram bot at the start
    - commands.py            - Contains an expandable list of bot command handlers
- main.py                    - Contains functionality to start, initialize and stop the bot
- README.md
- requirements.txt

    