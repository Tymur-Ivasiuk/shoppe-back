# Shoppe
Shoppe – інтернет магазин весільних плать
[Дизайн](https://www.figma.com/file/tbVLkrE8eEpAQGOu0HVMvp/Shoppe-(Community)?node-id=0%3A1&t=a3P2BaKIytjoAT0m-0) був взятий з Figma Community 

## Зміст
- [Технології](#технології)
- [Встановлення](#Встановлення)
- [Вимоги](#Вимоги)
- [Опис проекту](#опис-проекту)
- [Команда проекта](#команда-проекта)

## Технології
- [Django](https://www.djangoproject.com/)
- [jQuery](https://jquery.com/)
- ...

## Встановлення
Для встановлення бібліотек виконайте команду
```pip install -r requirements.txt```

### Вимоги
Для встановлення та запуску проекта потрібне віртуальне оточення а також Python (бажано 3.10.4 версії)

##Опис проекту
Спочатку мною був створений Frontend сайту. Потім в процесі написання Backend'у, зустрічаючи різні нюанси, виправляв і переписував велику частину коду. 
На сайті є такі сторінки: 
1.	[Головна сторінка](#головна-сторінка)
2.	[Сторінка товарів](#сторінка-товарів)
3.	[Сторінка самого товару](#сторінка-самого-товару)
4.	[Сторінка корзини](#сторінка-корзини)
5.	[Сторінка перевірки замовлення та вказання адреси доставки](#сторінка-перевірки-замовлення-та-вказання-адреси-доставки)
6.	[Сторінка реєстрації і логіна](#сторінка-реєстрації-і-логіна)
7.	[Сторінка свого кабінету](#сторінка-свого-кабінету)
8.	[Сторінка замовлення](#сторінка-замовлення)
9.	[Сторінка контакту](#сторінка-контакту)
10.	[Футер](#Футер)
11.	Прості сторінки з текстом про проект і правила

### Головна сторінка
![Home](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/home.png)

На цій сторінці є великий слайдер новинок, або ж любого товару, який можна вказати в базі даних при створенні запису. Також відображення 6 останніх товарів, які було додано до бд, та вказано статус публікації. 

### Сторінка товарів
![Shop](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/shop.png)
На цій сторінці є всі товари, які виставлені в статус публікації. На сайті присутні фільтрація та пошук. Також адміністратор має можливість виставляти на товар % скидки, який буде показано та враховано в майбутню корзину/чек. Пагінація також присутня. Максимальна кількість товарів на 1 сторінці - 9. 


### Сторінка самого товару
![Product](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/product.png)
Фотографії відображаються, як слайдер. Враховуючи кількість фото боковий слайдер, може бути статичний або мати безкінечний прокрут. 

У товара є опис, ціна (можлива знижка), середній бал по зірочкам (на даному скріні їх немає, але вони враховуються з тих коментарів, які можуть написати користувачі), атрибути, кількість, категорію. Користувач може додавати товар в свої уподобані (AJAX-запит), якщо він залогінений. 

Обравши кількість потрібного продукту – можна додати, його до корзини (також AJAX-запит). Реалізував це через сесії, куди записую ід, кількість і теперішню ціну товара (щоб при зміні адміністратором ціни, вона не була більше чим тоді, коли клієнт натиснув кнопку «Додати до корзини»). 

![Product-info](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/product-info.png)

### Сторінка корзини
![Cart](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/cart.png)
Корзина виглядає таким чином. Тут ще є можливість змінити кількість товарів, видалити їх або ж очистити корзини повністю. Реалізовано також через AJAX-запити, які змінюють також і остаточну ціну чека.

### Сторінка перевірки замовлення та вказання адреси доставки
![Checkout](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/checkout.png)
На цій сторінці реалізував систему купонів (скидочних). При введені коду купона, скидка починає діяти та впливає на остаточну ціну чека (записується також в сесії).

Тут також вводиться адреса доставки та можлива записка до заказу. Обирається спосіб оплати і кнопка створення замовлення. 

До натиску на кнопку створення замовлення все діє на сесіях, тому навіть незареєстрований користувач, може купити товар. 

При натиску на кнопку створюється саме замовлення в базі данних. Додаються товари до цього замовлення, а також інформація про адресу доставки. 

Якщо користувач був зареєстрований, то в бд записується про це інформація, щоб потім користувач міг проглянути всі свої замовлення та їх статус. Якщо ж користувач був не зареєстрований, то замовлення всеодно створюється, але тепер ід замовлення записується в cookie користувача, щоб всеодно мав змогу переглянути потім своє замовлення. 

При додаванні любого запису в список товарів замовлення – їхня кількість віднімається від кількості товару впринципі, тому магазину достатньо просто ввести загальну кількість продукту і не контролювати завжди його кількість при створенні замовлення. (в адмін панелі також є різні можливості по зміні списку товара, якщо при підтвердженні по телефону замовлення клієнт захоче внести зміни. Зміна кількості в замовленні впливає на загальну кількість товару при додаванні чи відніманні). Більшість цих всіх процесів реалізовано через [Django Signals](https://docs.djangoproject.com/en/4.1/topics/signals/). 


### Сторінка реєстрації і логіна
![Login](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/signin.png)

При створенні нового акаунта, потрібно спочатку підтвердити свою електронну скриньку. На email нового користувача відправляється лист з посиланням підтвердження своєї пошти. Звісно ж все ж для користувача ясно, тому що я також вивожу повідомлення про етапи реєстрації. Реалізував це через [Django Messages](https://docs.djangoproject.com/en/4.1/ref/contrib/messages/). 

Тільки після підтвердження пошти користувач може увійти у свій кабінет. 

>На сторінці логіну є також кнопка відновлення паролю. Використав користувацькі шаблони

### Сторінка свого кабінету
![Account](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/account.png)

На сторінці свого кабінету є декілька вкладок основними з яких є «Замовлення», «Уподобані товари», «Деталі акаунта», де є можливість змінити дані свого профілю.

### Сторінка замовлення
![Order](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/order.png)

Тут виводитьcя вся інформація про замовлення та чек.

### Сторінка контакту
![Contact](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/contact.png)

Тут любий користувач має можливість написати своє повідомлення, яке буде відправлено на пошту адміністратору.

### Футер
![Footer](https://github.com/Tymur-Ivasiuk/shoppe-back/blob/master/demo-image/footer.png)

Тут є можливість ввести свою електронну скриньку, щоб підписатись на новинки товарів. Кожен раз коли створюється новий товар з статусом опублікувано, то на ці скриньки будуть відправлені смс з посиланням на товар

Використовував також [Django Signals](https://docs.djangoproject.com/en/4.1/topics/signals/)

## Команда проекта
Весь сайт писав самотужки. Не мій - тільки дизайн
