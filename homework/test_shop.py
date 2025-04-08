"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100.0, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(500) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(100)
        assert product.quantity == 900

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match="Недостаточно товара на складе."):
            product.buy(1001)


class TestCart:

    def test_add_product(self, cart, product):
        cart.add_product(product, 2)
        assert cart.products[product] == 2

        cart.add_product(product, 3)
        assert cart.products[product] == 5

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)

        # Удаляем часть продукта из корзины.
        cart.remove_product(product, 2)
        assert cart.products[product] == 3

        # Удаляем весь продукт из корзины.
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_exact_quantity(self, cart, product):
        # Добавляем продукт в корзину.
        cart.add_product(product, 5)

        # Удаляем столько же товара сколько есть в корзине.
        cart.remove_product(product, 5)
        assert product not in cart.products

    def test_remove_product_not_found(self, cart, product):
        with pytest.raises(ValueError, match="Продукт не найден в корзине."):
            cart.remove_product(product)

    def test_clear(self, cart, product):
        cart.add_product(product, 5)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 2)
        assert cart.get_total_price() == 200.0

        cart.add_product(product, 3)
        assert cart.get_total_price() == 500.0

    def test_buy(self, cart, product):
        # Добавляем продукт в корзину.
        original_stock = product.quantity
        assert original_stock >= 2

        # Добавляем продукт в корзину.
        cart.add_product(product, 2)

        # Покупаем товары из корзины.
        cart.buy()

        # Проверяем что количество на складе уменьшилось.
        assert product.quantity == original_stock - 2

        # Корзина должна быть очищена после покупки.
        assert len(cart.products) == 0

    def test_buy_not_enough_stock(self, cart):
        # Создаем новый продукт с количеством 1
        low_stock_product = Product("low_stock_book", 100.0, "This is a low stock book", 1)

        # Добавляем продукт в корзину и уменьшаем количество на складе до одного экземпляра.
        low_stock_product.buy(1)

        # Теперь добавим еще один товар в корзину (всего будет два).
        cart.add_product(low_stock_product)

        with pytest.raises(ValueError,
                           match="Не удалось завершить покупку: Недостаточно товара на складе."):
            cart.buy()