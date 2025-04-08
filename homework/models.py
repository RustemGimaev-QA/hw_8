class Product:
    """
    Класс продукта.
    """

    def __init__(self, name: str, price: float, description: str, quantity: int):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity: int) -> bool:
        """Проверяет, достаточно ли товара на складе."""
        return self.quantity >= quantity

    def buy(self, quantity: int):
        """Уменьшает количество товара на складе."""
        if not self.check_quantity(quantity):
            raise ValueError("Недостаточно товара на складе.")
        self.quantity -= quantity


class Cart:
    """
    Класс корзины.
    """

    def __init__(self):
        self.products = {}

    def add_product(self, product: Product, buy_count: int = 1):
        """Добавляет продукт в корзину."""
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count: int = None):
        """Удаляет продукт из корзины."""
        if product not in self.products:
            raise ValueError("Продукт не найден в корзине.")

        if remove_count is None or remove_count >= self.products[product]:
            del self.products[product]
        else:
            self.products[product] -= remove_count

    def clear(self):
        """Очищает корзину."""
        self.products.clear()

    def get_total_price(self) -> float:
        """Возвращает общую стоимость товаров в корзине."""
        return sum(product.price * quantity for product, quantity in self.products.items())

    def buy(self):
        """Покупает все товары в корзине."""
        for product, quantity in list(self.products.items()):
            if not product.check_quantity(quantity):
                raise ValueError("Не удалось завершить покупку: Недостаточно товара на складе.")
            product.buy(quantity)
        self.clear()