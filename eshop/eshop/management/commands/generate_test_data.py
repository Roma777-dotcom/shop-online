from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Category, Product
from orders.models import Order, OrderItem
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Генерирует тестовые данные для разработки'
    
    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')
        
        self.stdout.write('Создание тестовых данных...')
        
        # Создание категорий
        categories_data = [
            {'name': 'Электроника', 'description': 'Техника и гаджеты'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
            {'name': 'Книги', 'description': 'Художественная и учебная литература'},
            {'name': 'Спорт', 'description': 'Спортивные товары и инвентарь'},
            {'name': 'Красота', 'description': 'Косметика и уход'},
            {'name': 'Дом', 'description': 'Товары для дома'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            self.stdout.write(f'Категория: {category.name}')
        
        # Создание товаров
        products = []
        for i in range(50):
            category = random.choice(categories)
            product = Product.objects.create(
                name=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                price=random.randint(100, 50000),
                stock=random.randint(0, 100),
                category=category,
                available=random.choice([True, True, True, False]),  # 75% доступны
            )
            products.append(product)
            if i % 10 == 0:
                self.stdout.write(f'Создано товаров: {i+1}')
        
        # Создание пользователей
        for i in range(10):
            user = User.objects.create_user(
                email=fake.email(),
                username=fake.user_name(),
                password='testpass123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                address=fake.address(),
                city=fake.city(),
                postal_code=fake.postcode(),
            )
            self.stdout.write(f'Пользователь: {user.email}')
        
        # Создание заказов
        users = User.objects.all()
        statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        
        for i in range(30):
            user = random.choice(users) if users.exists() else None
            order_date = datetime.now() - timedelta(days=random.randint(0, 90))
            
            order = Order.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                address=fake.address(),
                postal_code=fake.postcode(),
                city=fake.city(),
                phone=fake.phone_number(),
                status=random.choice(statuses),
                paid=random.choice([True, False]),
                payment_method=random.choice(['card', 'cash', 'online']),
                created=order_date,
            )
            
            # Добавляем товары в заказ
            order_items_count = random.randint(1, 5)
            for _ in range(order_items_count):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=quantity,
                )
            
            self.stdout.write(f'Заказ #{order.id}')
        
        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные успешно созданы!'))