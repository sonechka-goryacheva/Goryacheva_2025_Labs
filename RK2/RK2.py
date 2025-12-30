from operator import itemgetter
import unittest

class Computer:
    def __init__(self, id, name, price, display_class_id):
        self.id = id
        self.name = name
        self.price = price
        self.display_class_id = display_class_id

class DisplayClass:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class ComputerDisplayClass:
    def __init__(self, display_class_id, computer_id):
        self.display_class_id = display_class_id
        self.computer_id = computer_id

def create_one_to_many(display_classes, computers):
    """Логика для связи один-ко-многим"""
    return [(c.name, c.price, dc.name) 
            for dc in display_classes 
            for c in computers 
            if c.display_class_id == dc.id]

def create_many_to_many_temp(display_classes, computers_display_classes):
    """Логика для временной связи многие-ко-многим"""
    return [(dc.name, cdc.display_class_id, cdc.computer_id) 
            for dc in display_classes 
            for cdc in computers_display_classes 
            if dc.id == cdc.display_class_id]

def create_many_to_many(many_to_many_temp, computers):
    """Логика для связи многие-ко-многим"""
    return [(c.name, c.price, dc_name) 
            for dc_name, dc_id, computer_id in many_to_many_temp
            for c in computers if c.id == computer_id]

def sort_computers_by_class(one_to_many):
    """Логика задания А1"""
    return sorted(one_to_many, key=itemgetter(2))

def calculate_total_prices(one_to_many, display_classes):
    """Логика задания А2"""
    display_classes_total_price = []
    for dc in display_classes:
        dc_computers = list(filter(lambda i: i[2] == dc.name, one_to_many))
        if len(dc_computers) > 0:
            total_price = sum([price for _, price, _ in dc_computers])
            display_classes_total_price.append((dc.name, total_price))
    return sorted(display_classes_total_price, key=itemgetter(1), reverse=True)

def filter_departments_with_computers(many_to_many, display_classes):
    """Логика задания А3"""
    departments_with_computers = {}
    for dc in display_classes:
        if 'отдел' in dc.name:
            dc_computers = list(filter(lambda i: i[2] == dc.name, many_to_many))
            computer_names = [name for name, _, _ in dc_computers]
            departments_with_computers[dc.name] = computer_names
    return departments_with_computers

def main():
    # Исходные данные
    display_classes = [
        DisplayClass(1, 'отдел игровых компьютеров'),
        DisplayClass(2, 'архивный отдел офисной техники'),
        DisplayClass(3, 'бухгалтерия'),
        DisplayClass(11, 'отдел графических станций'),
        DisplayClass(22, 'архивный отдел серверов'),
        DisplayClass(33, 'отдел тестирования'),
    ]

    computers = [
        Computer(1, 'ASUS ROG', 25000, 1),
        Computer(2, 'HP Office', 35000, 2),
        Computer(3, 'Apple MacBook', 45000, 3),
        Computer(4, 'Dell Precision', 35000, 3),
        Computer(5, 'Lenovo ThinkPad', 25000, 3),
    ]

    computers_display_classes = [
        ComputerDisplayClass(1, 1),
        ComputerDisplayClass(2, 2),
        ComputerDisplayClass(3, 3),
        ComputerDisplayClass(3, 4),
        ComputerDisplayClass(3, 5),
        ComputerDisplayClass(11, 1),
        ComputerDisplayClass(22, 2),
        ComputerDisplayClass(33, 3),
        ComputerDisplayClass(33, 4),
        ComputerDisplayClass(33, 5),
    ]

    # Создание связей с помощью вынесенных функций
    one_to_many = create_one_to_many(display_classes, computers)
    many_to_many_temp = create_many_to_many_temp(display_classes, computers_display_classes)
    many_to_many = create_many_to_many(many_to_many_temp, computers)

    print('Задание А1')
    print('Список всех связанных компьютеров и дисплейных классов, отсортированный по дисплейным классам:')
    result_a1 = sort_computers_by_class(one_to_many)
    for item in result_a1:
        print(f"  {item[2]}: {item[0]} - {item[1]} руб.")

    print('\nЗадание А2')
    print('Список дисплейных классов с суммарной стоимостью компьютеров в каждом классе, отсортированный по суммарной стоимости:')
    result_a2 = calculate_total_prices(one_to_many, display_classes)
    for item in result_a2:
        print(f"  {item[0]}: {item[1]} руб.")

    print('\nЗадание А3')
    print('Список всех дисплейных классов, у которых в названии присутствует слово "отдел", и список компьютеров в них:')
    result_a3 = filter_departments_with_computers(many_to_many, display_classes)
    for department, computers_list in result_a3.items():
        print(f"  {department}: {', '.join(computers_list)}")


class TestRK1Functions(unittest.TestCase):
    """Тесты для функций РК1"""
    
    def setUp(self):
        """Тестовые данные"""
        self.display_classes = [
            DisplayClass(1, 'отдел игровых компьютеров'),
            DisplayClass(2, 'архивный отдел офисной техники'),
            DisplayClass(3, 'бухгалтерия'),
        ]
        
        self.computers = [
            Computer(1, 'ASUS ROG', 25000, 1),
            Computer(2, 'HP Office', 35000, 2),
            Computer(3, 'Apple MacBook', 45000, 3),
        ]
        
        self.computers_display_classes = [
            ComputerDisplayClass(1, 1),
            ComputerDisplayClass(2, 2),
            ComputerDisplayClass(3, 3),
            ComputerDisplayClass(1, 2),
        ]
    
    def test_sort_computers_by_class(self):
        """Тест 1: Проверка сортировки компьютеров по классам (Задание А1)"""
        one_to_many = create_one_to_many(self.display_classes, self.computers)
        result = sort_computers_by_class(one_to_many)
        
        # Проверяем сортировку по имени класса
        expected_order = ['архивный отдел офисной техники', 'бухгалтерия', 'отдел игровых компьютеров']
        actual_order = [item[2] for item in result]
        
        self.assertEqual(actual_order, expected_order)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], 'HP Office')  # Первый компьютер в отсортированном списке
    
    def test_calculate_total_prices(self):
        """Тест 2: Проверка расчета суммарной стоимости (Задание А2)"""
        one_to_many = create_one_to_many(self.display_classes, self.computers)
        result = calculate_total_prices(one_to_many, self.display_classes)
        
        # Проверяем правильность расчетов
        expected_results = {
            'бухгалтерия': 45000,
            'архивный отдел офисной техники': 35000,
            'отдел игровых компьютеров': 25000
        }
        
        self.assertEqual(len(result), 3)
        
        for class_name, total_price in result:
            self.assertEqual(total_price, expected_results[class_name])
        
        # Проверяем сортировку по убыванию цены
        self.assertTrue(result[0][1] >= result[1][1] >= result[2][1])
    
    def test_filter_departments_with_computers(self):
        """Тест 3: Проверка фильтрации отделов (Задание А3)"""
        many_to_many_temp = create_many_to_many_temp(self.display_classes, self.computers_display_classes)
        many_to_many = create_many_to_many(many_to_many_temp, self.computers)
        result = filter_departments_with_computers(many_to_many, self.display_classes)
        
        # Проверяем, что выбраны только отделы
        self.assertIn('отдел игровых компьютеров', result)
        self.assertIn('архивный отдел офисной техники', result)
        self.assertNotIn('бухгалтерия', result)
        
        # Проверяем состав компьютеров в отделах
        self.assertEqual(len(result['отдел игровых компьютеров']), 2)
        self.assertIn('ASUS ROG', result['отдел игровых компьютеров'])
        self.assertIn('HP Office', result['отдел игровых компьютеров'])
        
        self.assertEqual(len(result['архивный отдел офисной техники']), 1)
        self.assertIn('HP Office', result['архивный отдел офисной техники'])


if __name__ == '__main__':
    print("=== ВАШ РК1 С ТЕСТАМИ ===")
    print("\n--- Запуск основной программы ---")
    main()
    
    print("\n--- Запуск модульных тестов ---")
    unittest.main(argv=[''], exit=False, verbosity=2)