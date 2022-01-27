from django.db import models


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID Пользователя в Telegram")
    name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    username = models.CharField(max_length=100, verbose_name="Username пользователя", null=True)
    email = models.EmailField(max_length=100, verbose_name="Email", null=True)
    balance = models.IntegerField(verbose_name="Баланс", null=True)

    def __str__(self):
        return f"User id: {self.id} ({self.user_id} - {self.name})"


class Referral(TimeBasedModel):
    class Meta:
        verbose_name = "Реферал"
        verbose_name_plural = "Рефералы"

    id = models.ForeignKey(User, unique=True, primary_key=True, on_delete=models.CASCADE)
    referrer_id = models.BigIntegerField()

    def __str__(self):
        return f"Реферал {self.id} - от пользователя {self.referrer_id}"


class Item(TimeBasedModel):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название товара", max_length=50)
    photo = models.CharField(verbose_name="Фото file_id", max_length=200)
    price = models.CharField(verbose_name="Цена", max_length=50)
    description = models.TextField(verbose_name="Описание", null=True)

    def __str__(self):
        return f"Id товара: {self.id} - Название товара: {self.name}"


class Purchase(TimeBasedModel):
    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, verbose_name="Покупатель", on_delete=models.SET(0))
    item_id = models.ForeignKey(Item, verbose_name="Идентификатор товара", on_delete=models.CASCADE)
    amount = models.CharField(verbose_name="Стоимость", max_length=50)
    quantity = models.CharField(verbose_name="Количество", max_length=10)
    purchase_time = models.DateTimeField(verbose_name="Время покупки", auto_now_add=True)
    shipping_address = models.CharField(verbose_name="Адрес доставки", max_length=100, null=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=100)
    email = models.CharField(verbose_name="Email", max_length=100, null=True)
    receiver = models.CharField(verbose_name="Имя получателя", max_length=100, null=True)
    successful = models.BooleanField(verbose_name="Оплачено", default=False)

    def __str__(self):
        return f"Номер заказа: {self.id} - ID заказа: {self.item_id} ({self.quantity})"
