# Morph Numbers

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Компонент **Home Assistant**, добавляющий **Jinja2** фильтр для работы с числительными.

**Внимание:** API в стадии beta и в обновлениях могут быть изменены!

![template](template.png)

### Согласование слов с числительными

Полезно при отправке в Телеграм

```jinja2
{{ 24|numword('градус', false) }} => 24 градуса
```

### Преобразование чисел в текст

Полезно для TTS. Яндекс и Google допускают ошибки при произнесении числительных.

**Внимание:** [Яндекс Станция](https://github.com/AlexxIT/YandexStation) в режиме обычного TTS неправильно произносит числительные даже текстом (*например, "две просроченные задачи"*). Необходимо использовать режим [Продвинутого TTS](https://github.com/AlexxIT/YandexStation#%D0%BF%D1%80%D0%BE%D0%B4%D0%B2%D0%B8%D0%BD%D1%83%D1%82%D1%8B%D0%B9-tts).

```jinja2
{{ 2|numword('просроченная задача') }} => две просроченные задачи
```

### Прочее

```jinja2
{{ 2000435|numword }} => два миллиона четыреста тридцать пять
```

## Установка и настройка

Устанавливается через HACS.

Настраивается в `configuration.yaml`:

```yaml
morph_numbers:
````

Используется как дополнительный фильтр в шаблонах.

## Пример

```yaml
Старт занял {{ states('sensor.start_time')|round|numword('секунду') }}

{{ 1|numword('градус') }}
{{ 1|numword('задача') }}
{{ 1|numword('дерево') }}

{{ 2000435|numword('синее облако') }}

{{ 2|numword('запланированная задача', false) }}
{{ 5|numword('просроченная задача', false) }}

{{ 123|numword }}
```

```yaml
script:
  morph_numbers_test:
    sequence:
    - service: system_log.write
      data_template:
        message: Старт занял {{ states('sensor.start_time')|round|numword('секунду') }}
        level: warning
```