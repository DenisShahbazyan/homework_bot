import logging
import os
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
handler.setFormatter(formatter)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат. Принимает на вход два параметра:
    экземпляр класса Bot и строку с текстом сообщения.
    """
    bot.send_message(TELEGRAM_CHAT_ID, message)


def get_api_answer(current_timestamp):
    """Делает запрос к эндпоинту API-сервиса. В случае успешного запроса
    возвращает ответ API, преобразовав его из формата JSON к типам данных
    Python, иначе возвращает None.
    """
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}

    homework_statuses = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if homework_statuses.status_code != HTTPStatus.OK:
        raise Exception

    try:
        homework_statuses = homework_statuses.json()
    except Exception as error:
        logger.error(f'Ошибка при запросе к основному эндпоинту: {error}')
    else:
        return homework_statuses


def check_response(response):
    """Проверяет ответ API на корректность. Функция получает ответ API,
    приведенный к типам данных Python. Если ответ API соответствует ожиданиям,
    то функция возвращает список домашних работ (он может быть и пустым),
    доступный в ответе API по ключу 'homeworks'.
    """
    if not isinstance(response, dict):
        raise TypeError('Ответ от сервера не является словарем.')

    key = 'homeworks'
    if not key in response:
        raise KeyError(f'В словаре нет ключа {key}')

    if not isinstance(response[key], list):
        raise TypeError(f'В ключе {key}, данные приходят не в словаре.')

    try:
        response = response.get(key)
    except Exception as error:
        logger.error(f'Ошибка: {error}')
    else:
        return response


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус этой
    работы. В случае успеха, функция возвращает подготовленную для отправки
    в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_STATUSES.
    """
    if not 'homework_name' in homework:
        raise KeyError('В словаре нет ключа "homework_name"')
    homework_name = homework.get('homework_name')

    if not 'status' in homework:
        raise KeyError('В словаре нет ключа "status"')
    homework_status = homework.get('status')

    if not homework_status in HOMEWORK_STATUSES:
        raise KeyError(f'В словаре нет ключа {homework_status}')
    verdict = HOMEWORK_STATUSES[homework_status]

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения, которые необходимы
    для работы программы. Если отсутствует хотя бы одна переменная окружения
    функция должна вернуть False, иначе — True.
    """
    if (PRACTICUM_TOKEN or TELEGRAM_TOKEN or TELEGRAM_CHAT_ID) is None:
        return False
    return True


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Проверь переменные окружения')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time()) - 60 * 60 * 24 * 30

    while True:
        try:
            response = get_api_answer(current_timestamp)
            answer = check_response(response)
            status = parse_status(answer[0])
            send_message(bot, status)
            print('Отправил!')

            current_timestamp = int(time.time()) - 60 * 60 * 24 * 30
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
