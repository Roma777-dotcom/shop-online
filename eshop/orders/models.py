from django.db import models
from django.core.validators import MinValueValidator
from shop.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    PAYMENT_CHOICES = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличные при получении'),
        ('online', 'Онлайн платеж'),
    ]
    
    user = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Пользователь'
    )
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Статус'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='card',
        verbose_name='Способ оплаты'
    )
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return f'Заказ {self.id}'
    
    @property
    def total_cost(self):
        return sum(item.cost for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, 
        related_name='order_items', 
        on_delete=models.SET_NULL,
        null=True
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f"{self.id}"
    
    @property
    def cost(self):
        return self.price * self.quantity


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершен'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возврат'),
    ]
    
    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    payment_method = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    transaction_id = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
    
    def __str__(self):
        return f"Платеж для заказа {self.order.id}"
