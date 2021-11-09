# API

## Суть проекта:

Необходимость в разработке сервиса опросов пользователей и API к нему.

## Стек:

1. База данных: **PostgreSQL**.

2. Фреймворк: **Django-rest-framework**.

3. WSGI: **Gunicorn**.

4. Веб-сервер: **Nginx**.

5. Развертывание: **Docker-Compose**. 

## Пример работы API:

### Регистрация пользователя и создание JWT (+анонимный пользователь):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/3.%20user_create.gif)

### Получение актуальных опросов:

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/4.%20actually_polls.gif)

### Получение актуальных опросов, вопросов и ответов (для пользователей):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/5.%20actually_polls_questions_answers.gif)

### Поулчение всех опросов и вопросов (для администраторов):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/6.%20all_polls_questions.gif)

### Поулчение всех опросов, вопросов и ответов (для администраторов):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/7.%20polls_questions_answers_admin.gif)

### Поулчение всех опросов, вопросов и только правильных ответов (для администраторов):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/8.%20polls_questions_answers_right.gif)

### Создание ответа на вопрос (акутальность предачи идентификатора пользователя):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/9.gif)

### Создание ответа на вопрос (акутальность предачи идентификаторов опроса и вопроса):

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/10.gif)

### Получение пройденных опросов с ответами на вопросы по указанному идентификатору:

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/11.%20user_answers.gif)

### Изменение ответа на вопрос:

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/12.%20user_answers_new.gif)


## Административное управление сервисом:

Сервис предоставляет удобную административную панель, в которой совершать различные манипуляции с опросами. 

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/1.%20admin.gif)

## Документация API:

Сервис содержит автоматически генерируемую документацию. 

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API_3/2.%20swagger.gif)


## Запуск проекта:

Изменить название *example.env* на *.env*, при необходимости внеся в него коррективы.

1. Убедиться, что необходимые порты для работы проекта не заняты (8080 - nginx, 5433 - postgres, 8001 - django/gunicorn): 

`sudo netstat -tulpn | grep :<xxxx>`

где `xxxx` - номер порта.

2. Если на данных портах запущены стандартные сервисы, их необходимо выключить: 

```sudo kill `sudo lsof -t i:<xxxx>` ```

3. Создать docker-compose: 

`docker-compose build`

4. Запустить docker-compose: 

`docker-compose up -d`

5. Перейти по ссылке:

`http://localhost:8080/`

6. Остановить и удалить docker-compose:

`docker-compose down -v`


## Эндпоинты и методы:

**Эндпоинты**:
```
/swagger/
/api/v1/actually_polls/{<pk>}
/api/v1/actually_polls_questions_answers/{<pk>}
/api/v1/all_polls_questions/{<pk>}
/api/v1/polls_questions_answers_admin/{<pk>}
/api/v1/polls_questions_answers_right/{<pk>}
/api/v1/user_answer/<id_user>/<id_poll>/<id_question>/
/api/v1/user_answers/<id_user>/
```

**Методы**:

*GET*

Ссылка | Значение
--- | ---
`/swagger/` | Получение API проекта
`/api/v1/actually_polls/{<pk>}` | Получение актульных опросов
`/api/v1/actually_polls_questions_answers/{<pk>}` | Получение актульных опросов, вопросов и ответов
`/api/v1/all_polls_questions/{<pk>}` | Получение всех опросв и вопросов
`/api/v1/polls_questions_answers_admin/{<pk>}` | Получение актульных опросов, вопросов и ответов
`/api/v1/polls_questions_answers_right/{<pk>}` | Поулчение всех опросов, вопросов и только правильных ответов
`/api/v1/user_answers/<id_user>/` | Получение пройденных опросов с ответами на вопросы


*POST*

Ссылка | Значение
--- | --- 
`/api/v1/user_answer/<id_user>/<id_poll>/<id_question>/` | Создание ответа на вопрос `*`

`*` - Пример тела запроса:
```
{
    "text": "Ответ на вопрос"
}
```

## Полезное:

### Зайти в панель администратора (пользователь подгружается из фикстур):

```
Name: admin
Password: admin
```
