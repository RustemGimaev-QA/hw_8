"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # Проверяем, что метод check_quantity возвращает True, если запрашиваемое количество меньше или равно доступному
        assert product.check_quantity(500) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False  # Запрашиваемое количество больше доступного

    def test_product_buy(self, product):
        # Проверяем, что метод buy уменьшает количество продукта на складе
        product.buy(100)  # Покупаем 100 единиц
        assert product.quantity == 900  # Проверяем, что осталось 900 единиц

    def test_product_buy_more_than_available(self, product):
        # Проверяем, что метод buy выбрасывает ValueError, если пытаемся купить больше, чем есть в наличии
        with pytest.raises(ValueError, match="Недостаточно товара на складе."):
            product.buy(1001)  # Пытаемся купить 1001 единицу


class TestCart:
    """
    Тесты на методы класса Cart
    """

    @pytest.fixture
    def cart(self):
        return Cart()

    def test_add_product(self, cart, product):
        cart.add_product(product, 2)  # Добавляем 2 единицы продукта
        assert cart.products[product] == 2  # Проверяем, что продукт добавлен с правильным количеством

        cart.add_product(product, 3)  # Добавляем еще 3 единицы продукта
        assert cart.products[product] == 5  # Проверяем, что общее количество теперь 5

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)  # Добавляем 5 единиц продукта
        cart.remove_product(product, 2)  # Удаляем 2 единицы
        assert cart.products[product] == 3  # Проверяем, что осталось 3 единицы

        cart.remove_product(product)  # Удаляем все оставшиеся единицы
        assert product not in cart.products  # Проверяем, что продукт удален из корзины

    def test_remove_product_not_found(self, cart, product):
        with pytest.raises(ValueError, match="Продукт не найден в корзине."):
            cart.remove_product(product)  # Пытаемся удалить продукт, которого нет в корзине

    def test_clear(self, cart, product):
        cart.add_product(product, 5)  # Добавляем 5 единиц продукта
        cart.clear()  # Очищаем корзину
        assert cart.products == {}  # Проверяем, что корзина пустая

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 2)  # Добавляем 2 единицы продукта
        assert cart.get_total_price() == 200  # Проверяем общую стоимость (2 * 100)

        cart.add_product(product, 3)  # Добавляем еще 3 единицы продукта
        assert cart.get_total_price() == 500  # Проверяем общую стоимость (5 * 100)

    def test_buy(self, cart, product):
        cart.add_product(product, 2)  # Добавляем 2 единицы продукта
        product.buy(2)  # Уменьшаем количество на складе
        cart.buy()  # Покупаем все из корзины
        assert product.quantity == 996  # Проверяем, что на складе осталось 996 единиц
        assert cart.products == {}  # Проверяем, что корзина пустая

    def test_buy_not_enough_stock(self, cart, product):
        cart.add_product(product, 2)  # Добавляем 2 единицы продукта
        product.buy(1)  # Уменьшаем количество на складе
        with pytest.raises(ValueError, match="Не удалось завершить покупку: Недостаточно товара на складе."):
            cart.buy()  # Пытаемся купить 2 единицы, когда на складе только 1