from flask import Flask, render_template
from config import LOGIN, PASSWORD
from logic import main

app = Flask(__name__)


# Создаем обработчик адресной строки
@app.route('/vk_stat/<int:group_id>')
def vk_stat(group_id):
    stats = main(LOGIN, PASSWORD, group_id)
    activity = stats['Activities']
    ages = stats['Ages']
    cities = stats['Cities']
    return render_template('vk_stat.html', group=group_id, activity=activity, ages=ages, cities=cities)


if __name__ == '__main__':
    app.run(port=8080, host="127.0.0.1")
