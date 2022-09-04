# ----- Эмуляция smoke testing -----
# 1) python manage.py shell
# 2) from django.test import Client

# Создаём объект класса Client(), эмулятор веб-браузера
# 3) guest_client = Client()

# Браузер, сделай GET-запрос к главной странице
# response = guest_client.get('/')

# Какой код вернула страница при запросе?
# 4) response.status_code
# -----------------------------------


# ----- Что содержится в response -----
# status_code — содержит код ответа запрошенного адреса
# client — объект клиента, который использовался для обращения
# content — данные ответа в виде строки байтов;
# request — объект request, первый параметр view-функции, обработавшей запрос;
# templates — перечень шаблонов, вызванных для отрисовки запрошенной страницы;
# resolver_match — специальный объект, соответствующий path() из списка
# urlpatterns.
# Context — словарь переменных, переданный для отрисовки шаблона при вызове
# функции render();
# -----------------------------------


# ----- Варианты запуска -----
# Запустит все тесты проекта
# python3 manage.py test

# Запустит только тесты в приложении posts
# python3 manage.py test posts

# Запустит только тесты из файла test_urls.py в приложении posts
# python3 manage.py test posts.tests.test_urls

# Запустит только тесты из класса StaticURLTests для test_urls.py
# в приложении posts
# python3 manage.py test posts.tests.test_urls.StaticURLTests

# Запустит только тест test_homepage()
# из класса StaticURLTests для test_urls.py в приложении posts
# python3 manage.py test posts.tests.test_urls.StaticURLTests.test_homepage
# -----------------------------------


# ----- Вариации запуска -----
# Команду python3 manage.py test можно запустить с параметром --verbosity
# (есть сокращённая запись этого параметра: -v )

# 1) По умолчанию стоит 1
# 2) Чтобы увидеть развёрнутый список пройденных и проваленных тестов - 2
# python3 manage.py test -v 2

# -----------------------------------


# ----- Coverage -----
# pip install coverage
# coverage run --source='posts,users' manage.py test -v 2

# Параметр -source='posts,users' (без пробела после запятой)
# ограничит проверку coverage модулями posts и users.

# Параметр --source='.' запустит проверку coverage всех модулей в текущей
# директории (символ «точка» означает текущую директорию) и в её
# субдиректориях.

# Если параметр --source не указывать — будет проверено покрытие тестами всех
# модулей проекта, включая /venv. В результате в отчёт будет выведена масса
# ненужной информации. Лучше явно указывать в параметре --source те модули или
# директории, которые нужно проверить.

# Для получения большей детализации установите для параметра verbosity
# значение 2.

# coverage report - Просмотреть информацию

# Для представления результатов есть и более удобный формат: отчёт
# можно сохранить в виде HTML.
# Команда coverage html сформирует папку /htmlcov:
