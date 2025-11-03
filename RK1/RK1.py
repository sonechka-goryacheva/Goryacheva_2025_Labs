from operator import itemgetter

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

def main():
    one_to_many = [(c.name, c.price, dc.name) 
        for dc in display_classes 
        for c in computers 
        if c.display_class_id == dc.id]
    
    many_to_many_temp = [(dc.name, cdc.display_class_id, cdc.computer_id) 
        for dc in display_classes 
        for cdc in computers_display_classes 
        if dc.id == cdc.display_class_id]
    
    many_to_many = [(c.name, c.price, dc_name) 
        for dc_name, dc_id, computer_id in many_to_many_temp
        for c in computers if c.id == computer_id]

    print('Задание А1')
    print('Список всех связанных компьютеров и дисплейных классов, отсортированный по дисплейным классам:')
    
    result_a1 = sorted(one_to_many, key=itemgetter(2))
    for item in result_a1:
        print(f"  {item[2]}: {item[0]} - {item[1]} руб.")

    print('\nЗадание А2')
    print('Список дисплейных классов с суммарной стоимостью компьютеров в каждом классе, отсортированный по суммарной стоимости:')
    
    display_classes_total_price = []
    for dc in display_classes:
        dc_computers = list(filter(lambda i: i[2] == dc.name, one_to_many))
        if len(dc_computers) > 0:
            total_price = sum([price for _, price, _ in dc_computers])
            display_classes_total_price.append((dc.name, total_price))
    
    result_a2 = sorted(display_classes_total_price, key=itemgetter(1), reverse=True)
    for item in result_a2:
        print(f"  {item[0]}: {item[1]} руб.")

    print('\nЗадание А3')
    print('Список всех дисплейных классов, у которых в названии присутствует слово "отдел", и список компьютеров в них:')
    
    departments_with_computers = {}
    for dc in display_classes:
        if 'отдел' in dc.name:
            dc_computers = list(filter(lambda i: i[2] == dc.name, many_to_many))
            computer_names = [name for name, _, _ in dc_computers]
            departments_with_computers[dc.name] = computer_names
    
    for department, computers_list in departments_with_computers.items():
        print(f"  {department}: {', '.join(computers_list)}")

if __name__ == '__main__':
    main()