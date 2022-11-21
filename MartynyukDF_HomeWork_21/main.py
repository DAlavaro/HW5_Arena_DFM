from courier import Courier
from request import Request
from shop import Shop
from store import Store
from exeption import BaseError

store = Store(
    items={
        'печеньки': 4,
        'собачки': 4,
        'коробки': 11,
        'хлопушки': 7,
        'петарды': 9,
        'звездочки': 8
    }
)

shop = Shop(
    items={
        'печеньки': 2,
        'собачки': 1,
        'коробки': 2,
        'шарики': 10
    }
)
storages = {
    'склад': store,
    'магазин': shop
}


def main():
    while True:
        # вывести содержимое складов
        for storage_name in storages:
            print(f'\nВ {storage_name} хранится:')
            for key, value in storages[storage_name].get_items().items():
                print(f'{value} {key}')

        # Запросить у пользователя строку
        user_input = input(
            '\nВведите строку в формате "Доставить 3 печеньки из склад в магазин".\n'
            'Введите "stop" или "стоп", чтобы закончить\n'
        )

        if user_input in ('stop', 'стоп'):
            print('До встречи в будущем')
            break

        # Обработать строку, проверить на ошибки, определить товар, количество, точки отправления и назначения.
        try:
            request = Request(request_str=user_input, storages=storages)

            # Доставить товар
            courier = Courier(request=request, storages=storages)
            courier.move()
        except BaseError as error:
            print(error.massage)


if __name__ == '__main__':
    main()
