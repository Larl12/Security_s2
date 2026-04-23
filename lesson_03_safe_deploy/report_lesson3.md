# Отчет по ДЗ 3 «Hello, Production!»

## Ссылка на GitHub

```text
[https://github.com/Larl12/Security_s2]
```

## Скриншот терминала Linux / WSL

![alt text](image-2.png)

- команду запуска `python3 main.py`
- вывод программы `System started. Secret hash: MyS**`
- вывод `ls -la`, где есть файл `.env`

подписи:

```text
![alt text](image-3.png)
![alt text](image-4.png)

## Команды, которые должны быть видны на скриншоте

```bash
cd ~/project/Security_s2/safe_deploy
source venv/bin/activate
python3 main.py
ls -la
```

## Ожидаемый результат запуска

```text
System started. Secret hash: MyS**
```

## Что проверяется

- в репозитории есть `.gitignore`
- в репозитории есть `.env.example`
- в репозитории есть `requirements.txt`
- файла `.env` нет в GitHub
- файл `.env` есть локально в Linux / WSL
- приложение запускается и читает `APP_SECRET`
