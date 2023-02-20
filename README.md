# Тестовое задание Kerka Development

### Бот для приема платежей


## Особенности

* Отправка данных о пользователях в формате таблицы [код](https://github.com/LevChistyakov/Kerka_pay_bot/blob/91c733ab04b16efd24be61535efc6152906140df/app/handlers/owner/get_users.py#L15) 
* Блокировка пользователей с помощью middleware [код](https://github.com/LevChistyakov/Kerka_pay_bot/blob/91c733ab04b16efd24be61535efc6152906140df/app/middlewares/banned_users_middleware.py#L10) 
* Пополнение баланса внутри Telegram [код](https://github.com/LevChistyakov/Kerka_pay_bot/blob/91c733ab04b16efd24be61535efc6152906140df/app/handlers/user/replenish_balance.py#L56)

## Запуск

* Создать бота и получить токен в [BotFather](https://t.me/BotFather) 
* Получить тестовый токен для оплаты
> ([BotFather](https://t.me/BotFather) -> bot -> Payments -> ЮKassa -> Connect ЮKassa Test -> /start)
* Переименовать `example.toml` в `config.toml` и изменить настройки бота, базы данных и id админа
* Установить зависимости из файла `requirements.txt` 
> pip install -r requirements.txt
* Запустить бота командой `python -m app`

## Контакты
[Telegram](https://t.me/banana_maaan)
