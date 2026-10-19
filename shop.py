"""
Итоговый проект: Симулятор магазина с корзиной покупок.
Реализованы: ООП, алгоритмы сортировки (Bubble, Insertion, Quick, Merge),
визуализация промежуточных этапов и скидки.
"""

import time


# ========== 1. МОДУЛЬ ТОВАРОВ (Product) ==========
class Product:
    """Класс для хранения информации о товаре."""

    def __init__(self, name, category, price, weight, description=""):
        self.name = name
        self.category = category
        self.price = price
        self.weight = weight
        self.description = description

    def __str__(self):
        return f"{self.name:<15} | {self.category:<10} | {self.price:>6.2f} руб. | {self.weight:>5.2f} кг"


# ========== 2. МОДУЛЬ КОРЗИНЫ (Cart) ==========
class Cart:
    """Класс для управления корзиной покупок."""

    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def remove_product(self, product_name):
        for item in self.items:
            if item.name.lower() == product_name.lower():
                self.items.remove(item)
                return True
        return False

    def calculate_total(self, discount_percent=0):
        """Считает итоговую стоимость с учетом скидки."""
        total = sum(item.price for item in self.items)
        if discount_percent > 0:
            total -= total * (discount_percent / 100)
        return total

    def display(self):
        if not self.items:
            print("Корзина пуста.")
            return

        print("\n" + "=" * 65)
        print(f"{'Название':<15} | {'Категория':<10} | {'Цена':>9} | {'Вес':>7}")
        print("-" * 65)
        for item in self.items:
            print(item)
        print("=" * 65)
        print(f"Итого товаров: {len(self.items)} | Общий вес: {sum(i.weight for i in self.items):.2f} кг")


# ========== 3. МОДУЛЬ СОРТИРОВКИ (Sorting Algorithms) ==========
def bubble_sort(arr, key, reverse=False):
    """Пузырьковая сортировка."""
    a = arr.copy()
    n = len(a)
    steps = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # Сравниваем значения (getattr) и учитываем направление (reverse)
            val1 = getattr(a[j], key)
            val2 = getattr(a[j + 1], key)
            # Логика: если (val1 > val2) И мы сортируем по возрастанию (!reverse)
            # ИЛИ (val1 < val2) И мы сортируем по убыванию (reverse)
            if (val1 > val2 and not reverse) or (val1 < val2 and reverse):
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                steps += 1
        if not swapped:
            break
    print(f"   [Bubble Sort] Сделано перестановок: {steps}")
    return a


def insertion_sort(arr, key, reverse=False):
    """Сортировка вставками."""
    a = arr.copy()
    for i in range(1, len(a)):
        key_item = a[i]
        j = i - 1
        # Пока не дошли до начала и пока условие сортировки выполняется
        while j >= 0:
            val_j = getattr(a[j], key)
            val_item = getattr(key_item, key)
            if (val_j > val_item and not reverse) or (val_j < val_item and reverse):
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = key_item
    return a


def quick_sort(arr, key, reverse=False):
    """Быстрая сортировка."""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    pivot_val = getattr(pivot, key)

    left = []
    middle = []
    right = []

    for item in arr:
        item_val = getattr(item, key)
        if item_val == pivot_val:
            middle.append(item)
        elif (item_val < pivot_val and not reverse) or (item_val > pivot_val and reverse):
            left.append(item)
        else:
            right.append(item)

    return quick_sort(left, key, reverse) + middle + quick_sort(right, key, reverse)


def merge_sort(arr, key, reverse=False):
    """Сортировка слиянием."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        val_left = getattr(left[i], key)
        val_right = getattr(right[j], key)

        if (val_left < val_right and not reverse) or (val_left > val_right and reverse):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ========== 4. ПОЛЬЗОВАТЕЛЬСКИЙ ИНТЕРФЕЙС ==========
# Каталог товаров (имитация базы данных)
catalog = [
    Product("Ноутбук", "Электроника", 75000, 2.5, "Мощный игровой ноутбук"),
    Product("Мышь", "Электроника", 1500, 0.1, "Беспроводная мышь"),
    Product("Хлеб", "Продукты", 50, 0.4, "Свежий белый хлеб"),
    Product("Молоко", "Продукты", 80, 1.0, "Молоко 3.2%"),
    Product("Книга 'Python'", "Книги", 2000, 0.8, "Учебник по программированию"),
    Product("Футболка", "Одежда", 1200, 0.2, "Хлопковая футболка"),
    Product("Кофе", "Продукты", 450, 0.25, "Молотый кофе"),
]


def show_catalog():
    print("\n--- КАТАЛОГ ТОВАРОВ ---")
    print(f"{'ID':<3} | {'Название':<15} | {'Категория':<12} | {'Цена':>8} | {'Вес':>6}")
    print("-" * 60)
    for i, p in enumerate(catalog, 1):
        print(f"{i:<3} | {p.name:<15} | {p.category:<12} | {p.price:>8.2f} | {p.weight:>6.2f}")


def get_sort_algorithm():
    print("\nВыберите алгоритм сортировки:")
    print("  1. Пузырьковая (Bubble Sort)")
    print("  2. Вставками (Insertion Sort)")
    print("  3. Быстрая (Quick Sort)")
    print("  4. Слиянием (Merge Sort)")
    choice = input("Ваш выбор (1-4): ").strip()
    if choice == "1":
        return bubble_sort
    elif choice == "2":
        return insertion_sort
    elif choice == "3":
        return quick_sort
    elif choice == "4":
        return merge_sort
    else:
        print("Неверный выбор. Используем Bubble Sort по умолчанию.")
        return bubble_sort


def get_sort_key():
    print("\nСортировать по:")
    print("  1. Цене")
    print("  2. Весу")
    print("  3. Категории")
    choice = input("Ваш выбор (1-3): ").strip()
    if choice == "1":
        return "price"
    elif choice == "2":
        return "weight"
    elif choice == "3":
        return "category"
    else:
        print("Неверный выбор. Сортируем по цене.")
        return "price"


def get_sort_order():
    print("\nПорядок:")
    print("  1. По возрастанию")
    print("  2. По убыванию")
    choice = input("Ваш выбор (1-2): ").strip()
    return choice == "2"  # True, если убывание


def main():
    cart = Cart()

    while True:
        print("\n" + "=" * 30)
        print("      СИМУЛЯТОР МАГАЗИНА")
        print("=" * 30)
        print("1. Показать каталог товаров")
        print("2. Добавить товар в корзину")
        print("3. Удалить товар из корзины")
        print("4. Показать корзину")
        print("5. Отсортировать корзину")
        print("6. Посчитать итоговую стоимость (со скидкой)")
        print("0. Выход")
        print("=" * 30)

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("До свидания!")
            break

        elif choice == "1":
            show_catalog()

        elif choice == "2":
            show_catalog()
            try:
                item_id = int(input("Введите ID товара для добавления: ")) - 1
                if 0 <= item_id < len(catalog):
                    cart.add_product(catalog[item_id])
                    print(f"Товар '{catalog[item_id].name}' добавлен в корзину.")
                else:
                    print("Ошибка: товара с таким ID нет.")
            except ValueError:
                print("Ошибка: нужно ввести число.")

        elif choice == "3":
            if not cart.items:
                print("Корзина пуста.")
                continue
            cart.display()
            name = input("Введите название товара для удаления: ")
            if cart.remove_product(name):
                print(f"Товар '{name}' удален.")
            else:
                print(f"Товар '{name}' не найден в корзине.")

        elif choice == "4":
            cart.display()

        elif choice == "5":
            if not cart.items:
                print("Корзина пуста, нечего сортировать.")
                continue

            sort_func = get_sort_algorithm()
            sort_key = get_sort_key()
            reverse = get_sort_order()

            print("\nСортировка...")
            time.sleep(0.5)  # Небольшая пауза для эффекта
            cart.items = sort_func(cart.items, sort_key, reverse)
            print("Корзина успешно отсортирована!")
            cart.display()

        elif choice == "6":
            if not cart.items:
                print("Корзина пуста.")
                continue
            try:
                discount = float(input("Введите размер скидки в % (0, если нет): "))
                total = cart.calculate_total(discount)
                print(f"\nИтоговая стоимость: {total:.2f} руб.")
                if discount > 0:
                    print(f"(С учетом скидки {discount}%)")
            except ValueError:
                print("Ошибка: введите число.")


if __name__ == "__main__":
    main()