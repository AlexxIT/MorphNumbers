# Morph Numbers

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Компонент **Home Assistant**, добавляющий **Jinja2** фильтр для работы с числительными. Хорошо подходит в дополнение к моему второму компоненту [YandexStation](https://github.com/AlexxIT/YandexStation).

**Внимание:** Если вы пользовались компонентом ранее - название функции изменилось!

![template](template.png)

## Установка и настройка

Устанавливается через HACS.

Настраивается в `configuration.yaml`:

```yaml
morph_numbers:
````

Используется как дополнительный фильтр в шаблонах.

## Примеры

### Согласование слов с числительными

Полезно при отправке в Телеграм

```jinja2
{{ 24|format(morph='градус', as_text=false) }} => 24 градуса
```

### Преобразование чисел в текст

Полезно для TTS. Яндекс и Google допускают ошибки при произнесении числительных.

```jinja2
{{ 2|format(morph='просроченная задача') }} => две просроченные задачи
```

### Прочее

```jinja2
{{ 2000435|format(morph='') }} => два миллиона четыреста тридцать пять
```

### Шаблон из скриншота

```yaml
Старт занял {{ states('sensor.start_time')|round|format(morph='секунду') }}

{{ 1|format(morph='градус') }}
{{ 1|format(morph='задача') }}
{{ 1|format(morph='дерево') }}

{{ 2000435|format(morph='синее облако') }}

{{ 2|format(morph='запланированная задача', as_text=false) }}
{{ 5|format(morph='просроченная задача', as_text=false) }}

{{ 123|format(morph='') }}

{{ 0|format(morph='градус') }}
{{ -2|format(morph='градус') }}
```

```yaml
script:
  morph_numbers_test:
    sequence:
    - service: persistent_notification.create
      data_template:
        message: Старт занял {{ states('sensor.start_time')|round|format(morph='секунду') }}
```