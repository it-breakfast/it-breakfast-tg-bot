# it-breakfast-tg-bot

## Production
при коммите в prod собирается образ и выкатывается в основной чат

## Staging
при коммите в main собирается образ и выкатывается на тест в отдельный чатик
https://t.me/+Wcakgvd4iuA1Yjc6

## Local run

Для локального запуска можно в корень поместить небольшой bash скрипт с вашими собственными BOT_TOKEN и CHAT_ID

```
#!/bin/bash

export BOT_TOKEN='123123'
export CHAT_ID='123123'

python3 -m TelegramBot
```
