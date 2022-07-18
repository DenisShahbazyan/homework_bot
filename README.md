# Telegram бот

## Описание:
Телеграм бот для оповещения о проверки домашнего задания на Яндекс Практикуме.

## Развертывание:
- Склонируйте проект на Ваш компьютер 
```sh 
git clone https://github.com/DenisShahbazyan/homework_bot.git
``` 
- Перейдите в папку с проектом 
```sh 
cd homework_bot
``` 
- Создайте и активируйте виртуальное окружение 
```sh 
python -m venv venv 
source venv/Scripts/activate 
``` 
- Обновите менеджер пакетов (pip) 
```sh 
pip install --upgrade pip 
``` 
- Установите необходимые зависимости 
```sh 
pip install -r requirements.txt
``` 
- Создайте файл `.env` в корне, с необходимым содержимым
```sh
PRACTICUM_TOKEN=YOUR_PRACTICUM_TOKEN
TELEGRAM_TOKEN=YOUR_TELEGRAM_TOKEN
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
```
- Запустить файл `homework.py`

## Системные требования:
-   [Python](https://www.python.org/) 3.10.4

## Планы по доработке:
>Этот проект не требует доработки, так как может использоваться только студентами Яндекс Практикума. К тому же это не плохой пример по написанию Telegram ботов.

## Используемые технологии:
-   [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) 13.7
-   [requests](https://pypi.org/project/requests/) 2.26.0

## Авторы:
[Denis Shahbazyan](https://github.com/DenisShahbazyan)

## Лицензия:
- MIT
