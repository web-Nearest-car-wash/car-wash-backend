from drf_spectacular.utils import extend_schema

PAYMENT_CHOICES = (
    ('cash', 'Наличные'),
    ('card', 'Картой'),
    ('online', 'Онлайн'),
    ('SBP', 'СБП'),
)

DAYS_OF_WEEK = [
    (1, 'Понедельник'),
    (2, 'Вторник'),
    (3, 'Среда'),
    (4, 'Четверг'),
    (5, 'Пятница'),
    (6, 'Суббота'),
    (7, 'Воскресенье'),
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
