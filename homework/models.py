class Product:
    """
    Класс продукта
    """
    name: str  # Название продукта
    price: float  # Цена продукта
    description: str  # Описание продукта
    quantity: int  # Количество продукта на складе

    def __init__(self, name, price, description, quantity):
        # Инициализация атрибутов продукта
        self.name = name  # Устанавливаем название продукта
        self.price = price  # Устанавливаем цену продукта
        self.description = description  # Устанавливаем описание продукта
        self.quantity = quantity  # Устанавливаем количество продукта на складе

    def check_quantity(self, quantity) -> bool:
        """
        Верните True если количество продукта больше или равно запрашиваемому
        и False в обратном случае
        """
        return self.quantity >= quantity  # Проверяем, достаточно ли товара на складе

    def buy(self, quantity):
        """
        Реализуйте метод покупки
        Проверьте количество продукта используя метод check_quantity
        Если продуктов не хватает, то выбросите исключение ValueError
        """
        if not self.check_quantity(quantity):  # Проверяем, достаточно ли товара
            raise ValueError("Недостаточно товара на складе.")  # Если нет, выбрасываем исключение
        self.quantity -= quantity  # Уменьшаем количество на складе на запрашиваемое количество


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]  # Определяем тип словаря, где ключ - продукт, значение - количество

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}  # Инициализируем пустой словарь для хранения продуктов

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products:  # Проверяем, есть ли продукт в корзине
            self.products[product] += buy_count  # Увеличиваем количество, если продукт уже есть
        else:
            self.products[product] = buy_count  # Добавляем новый продукт в корзину

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product not in self.products:  # Проверяем, есть ли продукт в корзине
            raise ValueError("Продукт не найден в корзине.")  # Если нет, выбрасываем исключение

        if remove_count is None or remove_count >= self.products[product]:  # Если не указано количество или оно больше, чем в корзине
            del self.products[product]  # Удаляем продукт из корзины
        else:
            self.products[product] -= remove_count  # Уменьшаем количество продукта в корзине

    def clear(self):
        """Очистить корзину."""
        self.products.clear()  # Очищаем все продукты из корзины

    def get_total_price(self) -> float:
        """Возвращает общую стоимость всех продуктов в корзине."""
        total_price = sum(product.price * quantity for product, quantity in self.products.items())  # Считаем общую стоимость
        return total_price  # Возвращаем общую стоимость

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        try:
            for product, quantity in self.products.items():  # Проходим по всем продуктам в корзине
                product.buy(quantity)  # Проверяем и уменьшаем количество на складе
            self.clear()  # Очищаем корзину после успешной покупки
        except ValueError as e:  # Если возникла ошибка при покупке
            raise ValueError("Не удалось завершить покупку: " + str(e))  # Выбрасываем новое исключение с сообщением