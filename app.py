import os

from base import Arena
from flask import Flask, render_template, request, url_for, jsonify
from werkzeug.utils import redirect

from equipment import Equipment
from classes import unit_classes
from unit import PlayerUnit, EnemyUnit

from db import db

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


heroes = {
    "player": ...,
    "enemy": ...,
}

# инициализируем класс арены
arena = Arena()


@app.route("/")
def menu_page():
    # Рендерим главное меню (шаблон index.html)
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    # выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # рендерим экран боя (шаблон fight.html)
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    # кнопка нанесения удара
    # обновляем экран боя (нанесение удара) (шаблон fight.html)
    # если игра идет - вызываем метод player.hit() экземпляра класса арены
    # если игра не идет - пропускаем срабатывание метода (просто рендерим шаблон с текущими данными)
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    # кнопка использования скилла
    # логика практически идентична предыдущему эндпоинту
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    # кнопка пропуска хода
    # логика практически идентична предыдущему эндпоинту
    # однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    # кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # кнопка выбор героя. 2 метода GET и POST
    # на GET отрисовываем форму.
    # на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    if request.method == 'GET':
        header = 'Выберите героя'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']
        # Добавить проверку, что класс с таким именем существует
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        # Обработать отсутствующую броню и оружие
        player.equip_armor(Equipment().get_armor(armor_name))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # кнопка выбор соперников. 2 метода GET и POST
    # также на GET отрисовываем форму.
    # на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'GET':
        header = 'Выберите противника'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']
        # Добавим проверку, что класс с таким именем существует
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        # Обработать отсутствующую броню и оружие
        enemy.equip_armor(Equipment().get_armor(armor_name))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


@app.route('/test_db')
def test_db():
    db.session.execute(
        '''
        SELECT 1
        '''
    ).scalar()

    return jsonify(
        {
            'result': 'result'
        }
    )


if __name__ == "__main__":
    app.run()
