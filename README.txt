CONVY

Веб-приложение
Стек: Python, Django, HTML, CSS, Bootstrap, PostgreSQL

Convy нужен для помощи в изучении английского языка в игровой форме.
- В сервисе предполагается регистрация пользователей.
- Каждый пользователь формирует свой словарь постепенно добавляя в него слова из общей базы.
- Интерфейс предлагает пользователю перевести случайно выбранное из словаря слово.
- Каждое слово в словаре каждого пользователя имеет свою вероятность выпадения.
- Вероятность выпадения увеличивается с каждым неправильным ответом и уменьшается с правильным.

Фишки:
- реализована аутентификация пользователя по электронной почте вместо имени пользователя
- отображение статистики, а также деление слов на категории с указанием прогресса изучения
- цветовая схема всего приложения выведена в три переменные с цветами в файле
  controls/static/css/convy.css
  всю цветовую схему полностью можно изменить через них.
- пользователю показывается структура слова в виде "______ __ _____"(кол-во букв и пробелы если есть)

Структура БД:
- таблица Sector (id, sectors) - категории слов - связь один-ко-многим с таблицей Words
- таблица Word (id, lang1, lang2, sector) - общая база слов на двух языках с указанием категории
- таблица Progress (id, user_id, word_id, chance) - база записей вероятностей выпадения конкретного слова у
  конкретного пользователя

def index -             Рендер для главной страницы. Считает и передает в контексте количество слов в словаре и
                        общий прогресс изучения для отображения если пользователь авторизован.
def button_plus_word -  Логика добавления слов в словарь пользователя из общей базы.
                        Запись в таблицу Progress.
                        Возвращает текстовое сообщение с результатом  для передачи в вызывающую функцию
def button_plus_one -   Реакция на кнопку "Добавить 1 слово" в итерфейсе.
                        Вызывает button_plus_word, принимает сообщение в контексте, обновляет страницу Game,
                        передает в нее сообщение
def button_plus_ten -   Реакция на кнопку "Добавить 10 слов" в итерфейсе.
                        То же, что и button_plus_one, только для 10 слов.
def inverse_percentage - Шанс выпадения слова обратно пропорционален прогрессу изучения в процентах.
                        Формула вынесена в отдельную функцию.
def game -              Рендер для страницы с игрой (Game).
                        Собирает контекст для передачи на страницу:
                        'sector_statistics': словарь с текущей статистикой изучения по секторам (отображается справа)
                        'words_in_dictionary': всего слов в словаре пользователя на изучении
                        'message_from_answer': сообщение для пользователя внизу (правильный/неправильный ответ)
                        'message_from_button': сообщение для пользователя вверху (например, после добавления новых слов)
                        'offered_id': выпавшее для отгадывания слово (его id)
                        'offered_answer': ожидаемый ответ пользователя
                        'offered_word': предлагаемое на перевод слово
                        'offered_sector': категория выпавшего для угадывания слова
                        'offered_structure': структура слова (подсказка в виде черточек по количеству букв)
                        'learning_progress': текущий процент изучения конкретного слова
def dictionary_with_sector_statictics - Принимает списки данных из game()
                        Возвращает словарь со статистикой изучения слов по секторам.
def make_word_structure - Принимает строку (выпавшее для отгадывания слово из game())
                        Возвращает структуру-подсказку в виду "-" вместо букв
def answer -            Реакция на кнопку ОК со страницы с игрой.
                        Принимает ответ, введенный пользователем.
                        Корректирует значение шанса выпадения в таблице Progress в зависимости от ответа.
                        Обновляет страницу с игрой, передавая туда сообщение (правильный/неправильный ответ)
def chance_change -     Корректирует значение шанса выпадения слова в зависимости от принятых аргументов.
                        Контролирует чтобы шанс был не менее 1 и не более 99 для корректной работы выборки.
class EmailBackend(ModelBackend):
    def authenticate -  корректировка встроенной функции для того чтобы в качестве логина принималась почта пользователя
def my_login -          Реакция на кнопку под формой аутентификации.
                        Передает данные из POST запроса на кастомную фукцию authenticate (для принятия почты вместо имени).
def my_logout -         Кнопка выхода из аккаунта
def registration -      Реакция на кнопку под формой регистрации.
                        Делает проверки, регистрирует пользователя в базе и сразу же аутентифицирует его.
class MyPasswordResetView(PasswordResetView):
    def form_valid -    Испоьзование кастомной формы для сброса пароля.
