Модуль mapgenerator.py містить функції, що дозволяють згенерувати інтерактивну web-карту світу на основі інформації у базах даних locations.csv, world.json.

1. Країни на карті розфарбовуються залежно від площі країни (площа менше нижньої межі - зелений, між нижньою та верхньою межею - жовтий,
вище верхньої межі - червоний)

На карті генеруються точки, що вказують місця зйомок фільмів за даними параметрами:
2. Зелені точки - місця та назви фільмів, що були зняті у рік, що задав користувач
3. Сині точки - місця, де знімали фільм, назву якого задав користувач



Згенерований html файл має структуру:
*head - тег, всередині якого знаходяться інші теги, що допомагають браузеру коректно сприймати та відображати дану сторінку
  *meta - теги, що надають інформацію браузерам та пошуковим системам щодо того, як працювати зі сторінкою
  *script- теги, що містять скрипти (код на певній мові програмування), що має виконуватися при запуску сторінки
  link - тег, що встановлює зв'язок із зовнішніми файлами(стилями, шрифтами)
  style - тег для визначення стилів веб-сторінки

body - тег, що містить інформацію, яку слід виводити на веб сторінці
  div - тег, що використовується для відокремлення первного фрагменту документу, щоб потім примінити до нього стилі


script - тег, що містить код, що генерує карту
