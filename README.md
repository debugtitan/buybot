# Solana-Telegram-Ping-Bot
PingBot is a friendly Telegram bot that monitors Solana tokens, sending quick alerts to your group. Stay in the loop with PingBot by your side!

[Working Demo](https://buybotwsb)

![Ping Bot](image.png)
## Developer quick start 👩‍💻
`python -m pingbot` will launch the bot locally


### Configuration 🔧

First, install the dependencies:
`pip install -r requirements.txt`
`python -m pingbot`


For the bot to run, it needs these variables, laid out in the `.env.example` file

## Running App

1. Fork `https://github.com/debugtitan/buybot.git ` repository into your own namespace such as `your_username/buybot`.

2. Clone your project locally:

```bash
git clone https://github.com/debugtitan/buybot.git 
cd buybot
```

3. Create and activate your venv  [Read More about venv](https://docs.python.org/3/library/venv.html)

4. Installed required packages used in this app

```bash
pip install -r requirements.txt
```

5. Setup env variables required
    - `TOKEN` telegram bot token [GET TELEGRAM BOT TOKEN HERE](https://t.me/BotFather)
    - `USE_DJANGO_IN_MEMORY_DATABASE` boolean (if to use sqlite mode: default is False)
    - `SUPER_ADMIN` your telegram id [GET UNIQUE TELEGRAM ID](https://t.me/useridinfobot)
    - `RPC_CLIENT` get a non rate limit rpc node url [GET RPC NODE ENDPOINT](https://dashboard.quicknode.com/?prompt=signup)

6. Run Application
```bash
python -m pingbot
```


## Todo Tasks
- [x] Setup Application Codebase
- [x] Integration of django ORM
- [x] Implementation of Python Telegram Bot Wrapper
- [x] Building PingBot Solana Client
- [x] Fetch Token Info
- [x] Fetch Token Liquidty Pool Address
- [x] Fetch Token Liquidity Pool Events
- [x] Create Admin Panel
    - [x] min buy alert
    - [x] min sell alert
    - [x] steps emoji setup
    - [x] pause alerts
    - [x] delete token from database
- [x] Implement Decorator
    - [x] only bot super admin can make changes



## feel free to open `pull request ` for new `contribution`
    

