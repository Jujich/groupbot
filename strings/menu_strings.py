from string import Template

menu_strings: dict = {
    "get_groups": "Выберите группу",
    "settings": Template("Выбрана группа: <b>$title</b>"),
    "text": Template("<b>Текст сообщения</b> (при отправке price и amount будут заменены соответственно на цену и кол-во занятий):\n\n$text"),
    "default_text": "Цена за месяц: <b>$price</b>\nКол-во занятий: <b>$amount</b>",
    "schedule": Template("<b>Следующее сообщение:</b>\n\n"
                         "Дата отправки: <b>$date</b> число\n"
                         "Время отправки: <b>$time</b>"),
    "default_date": "не установлено",
    "default_time": "не установлено",
    "incorrect_date": "Некорректная дата. Введите день в формате:\n\n<b>ДД</b>\n\nДень должен быть между 1 и 28 числом включительно",
    "incorrect_time": "Некорректное время. Введите время в формате:\n\n<b>ЧЧ:ММ</b>",
    "edit_text": "Введите текст сообщения.\nТам, где хотите указать кол-во занятий и стоимость пишите соответственно $amount и $price",
    "confirm_edit_text": Template("Новое сообщение:\n\n$text\n\n<b>Применить?</b>"),
    "confirm_edit_schedule": Template("Новое значение:\n\n<b>$text</b>\n\nПрименить?"),
    "edit_text_success": "Текст успешно изменен",
    "edit_text_failure": "Ошибка при изменении текста.\nПожалуйста, убедитесь, что текст не содержит некорректных символов и повторите попытку.",
    "text_no_template": "Текст должен содержать $price и $amount в местах, где Вы хотите вставить центу и кол-во занятий.",
    "edit_schedule_date": "Введите дату отправки сообщения в формате:\n\n<b>ДД</b>\n\nДень должен быть между 1 и 28 числом включительно",
    "edit_schedule_time": "Введите время отправки сообщения в формате:\n\n<b>ЧЧ:ММ</b>",
    "edit_schedule_date_success": "Дата успешно изменена",
    "edit_schedule_time_success": "Время успешно изменены",
    "edit_schedule_failure": "Ошибка!\nПожалуйста, убедитесь в правильности введенных значений и повторите попытку",
    "default_price": "Н/Д",
    "default_amount": "Н/Д",
    "edit_price": "Введите новую цену",
    "edit_amount": "Введите новое количество занятий",
    "incorrect_price": "Некорректно введена цена\nЦена должна быть положительным числом. Не указывайте единицы валюты",
    "left_group": Template("Покинута группа: <b>$title</b>"),
    "confirm_edit_price": Template("Новая цена: <b>$price</b>\n\nПрименить?"),
    "confirm_edit_amount": Template("Новое количество занятий: <b>$amount</b>\n\nПрименить?"),
}
