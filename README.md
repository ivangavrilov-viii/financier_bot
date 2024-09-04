# @Manual_Financier_Bot
#### Created by Ivan Gavrilov   

------  
#### ***Task Description:***  
***This Telegram bot is designed to maintain financial accounting for a given period. It can be used to calculate a daily budget, which also varies depending on expenses and income. The bot allows you to record all transactions during a given period and also receive them for user analysis.***
_________  
### _Requirements_ 
Python version 3.8 or higher and the following modules are required for the bot to work correctly:  
```  
certifi==2023.7.22
charset-normalizer==3.3.0
colorama==0.4.6
idna==3.4
loguru==0.7.2
pyTelegramBotAPI==4.14.0
python-decouple==3.6
requests==2.31.0
telebot==0.0.5
urllib3==2.0.7
win32-setctime==1.1.0
```  
---  
### _Bot's file composition_  
The bot uses polling technology, so no additional server configuration is required.  
The following files are used in the bot:  
* main.py - main file for bot's work  
* messages.py - file containing functions for outputting various bot messages
* keyboards.py - file with functions for creating keyboards for working with the bot
* db_funcs.py -  file containing functions for CRUD concept of working with SQLite3 database
* .env - file containing the token for connecting the bot to Telegram servers and link for payment. This file should be created manually and the token obtained with @BotFather should be added to it.
* requirements.txt - list of required modules and dependencies
* utils.py - file containing different utils for work
* budgets.json - formatted example model of budget
---  
### _Preparing for start bot_  
For the bot to function, you first need to register the bot in Telegram using @BotFather.  
The received tokens should be located in the ".env" file: 
* key_bot = 'token received from @BotFather in Telegram'
* admin_1 = 'chat id in TG for first admin'
* db_name = 'db name file'
---  
### _Start bot_  
1. Virtual environment creation:  
``` 
python -m venv venv  
```  
  
2. Virtual environment activation on Windows:  
```  
source venv/bin/activate
```  
  
3. Installing requirements:  
```  
pip install -r requirements.txt    
```  
  
4. Starting bot:  
```  
python main.py  
```  
---  
### _After the start, the bot will start working in Telegram under the name [Manual_Financier_Bot](https://t.me/Manual_Financier_Bot)_

---  
### _Bot's command list:_ 
- /help - Help with bot commands
- /balance - View the status of your account
- /period_history - List of expenses in the current period
- /add_expense - Add expense in today
- /add_profit - Add profit in today
- /update_budget - Calculate and update the daily budget
- /set_budget - Set the budget for the selected period and start the bot's work
- /clean_history - Delete user history

_For administrators:_
- in development...

---
### If you have any questions about the bot you can write to me [@gavril_23](https://t.me/gavril_23)

---
