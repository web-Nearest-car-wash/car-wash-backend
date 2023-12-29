from decimal import Decimal

from drf_spectacular.utils import extend_schema


CENTER_MOSCOW_LATITUDE = Decimal(55.558741)
CENTER_MOSCOW_LONGITUDE = Decimal(37.378847)

PAYMENT_CHOICES = (
    ('cash', 'Наличные'),
    ('card', 'Картой'),
    ('online', 'Онлайн'),
    ('SBP', 'СБП'),
)

DAYS_OF_WEEK = [
    (0, 'Понедельник'),
    (1, 'Вторник'),
    (2, 'Среда'),
    (3, 'Четверг'),
    (4, 'Пятница'),
    (5, 'Суббота'),
    (6, 'Воскресенье'),
]

SCORES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

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
