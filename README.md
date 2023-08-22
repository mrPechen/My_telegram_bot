# Онлайн магазин в виде Телеграм бота.

Онлайн магазин реализован с помощью Django, Aiogram и PostgreSQL.

- Реализована админка с помощью Django, где можно добавлять/ изменять/ удалять товары.
- Реализован вывод и поиск товаров с помощью инлайн мода. В двух словах инлайн мод - это возможность вывода товаров в списке в сплывающем окне, когда в поле для ввода вводится название бота. Поиск работает так: в поле для ввода текста вводится начало/ часть наименования товара и во всплываюшем окне отображаются подходящие товары.
- Реализована система оплаты товара через банковскую карту. В данном случае сбербанк. 
- Реализована реферальная система. В боте есть кнопка для формирования уникальной ссылки. Когда зарегистрированный пользователь приглашает друга по этой ссылке, он получает внутреннюю валюту, которую может обменять на скидку при покупке товара.
- Реализован пример ограничения доступа к боту. Если человек хочет воспользоваться ботом без реферральной ссылки, то бот предложит человеку подписаться на определенную группу. Когда человек подпишется бот проверит, что человек подписался и ему будет доступен функционал бота.
- Пользователь может узнать свой баланс бонусной валюты и приглашенных пользователей.
