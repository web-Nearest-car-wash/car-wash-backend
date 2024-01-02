import datetime as dt

from drf_spectacular.utils import extend_schema

AROUND_THE_CLOCK = 'Круглосуточно'
CLOSED = 'Закрыто'
NO_INFORMATION = 'Нет информации'
WORKS_UNTIL = 'Работает до '

DAYS_OF_WEEK = [
    (0, 'Понедельник'),
    (1, 'Вторник'),
    (2, 'Среда'),
    (3, 'Четверг'),
    (4, 'Пятница'),
    (5, 'Суббота'),
    (6, 'Воскресенье'),
]

SCHEDULE_HELP_TEXT = 'Введите время в формате ЧЧ:ММ, например 10:00'

SCORES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

PAYMENT_CHOICES = (
    ('cash', 'Наличные'),
    ('card', 'Картой'),
    ('online', 'Онлайн'),
    ('SBP', 'СБП'),
)

TIME_UTC_CORRECTION = dt.timedelta(hours=3)

USERS_API_SCHEMA_EXTENSIONS = {
    'list': extend_schema(
        tags=['Users'], summary="Получить список пользователей"),
    'update': extend_schema(
        tags=['Users'], summary="Изменения данных о пользователе"),
    'partial_update': extend_schema(
        tags=['Users'],
        summary="Частичное изменение данных о пользователе",
        description="Изменения данных о пользователе. Поля, "
                    "которые не заполнены будут оставлены без изменений."
    ),
    'create': extend_schema(
        tags=['Users'], summary="Создать нового пользователя"),
    'destroy': extend_schema(
        tags=['Users'], summary="Удалить пользователя"),
    'retrieve': extend_schema(
        tags=['Users'], summary="Получить данные о пользователе")
}

CARWASH_API_SCHEMA_EXTENSIONS = {
    'list': extend_schema(
        tags=['CarWash'],
        summary="Получить список автомоек"),
    'retrieve': extend_schema(
        tags=['CarWash'],
        summary="Получить данные для карточки мойки")
}

KEYWORDS_SERVICES_API_SCHEMA_EXTENSIONS = {
    'list': extend_schema(
        tags=['Services'],
        summary="Получить ключевые слова для фильтрации по услугам"
    )
}

CARWASH_TYPE_API_SCHEMA_EXTENSIONS = {
    'list': extend_schema(
        tags=['Types'],
        summary="Получить типы автомоек"
    )
}
