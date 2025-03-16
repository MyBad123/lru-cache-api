# lru-cache-api

## Описание

Это приложение реализует REST API для структуры данных Least Recently Used (LRU) cache с поддержкой Time-To-Live (TTL). Оно позволяет хранить ограниченное количество элементов, автоматически удаляя наименее используемые при достижении лимита или при истечении срока действия (TTL). API предоставляет возможности для добавления, получения и удаления элементов, а также управления временем жизни каждого элемента. Такой кэш полезен для оптимизации работы с ограниченными ресурсами, где важно быстро извлекать актуальную информацию.

## Развертывание

```bash
echo "EXTERNAL_PORT=8080" >> .env # установить порт, по которому пользователь будет обращаться к api
echo "CACHE_CAPACITY=5" >> .env # установить ограничение на количество элементов

sudo docker compose up -d
```

## Тестирование приложения

```bash
pytest tests --maxfail=1 --disable-warnings -v -s
```

## Общие рекомендации
- Использовать ограничения по памяти, а не по количеству элементов. Благодаря этому коцептуальному изменению можно использовать Redis, соответственно, мы получим преимущества из следующего пункта.
- Подключить Redis. Изначально, это и планировалось, но, так как ограничение должно задаваться количеством элементов, а не используемой памятью, было решено отказаться от этой идеи. В Redis есть встроенные механизмы поддержки LRU и TTL, а также автоматическое удаление элементов, срок хранения которых истек. Это поможет облегчить код и организовать более безопасный механизм хранения данных. 