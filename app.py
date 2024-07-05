from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

TOKEN = '6944652004:AAHwny2n9DDJ6TSVsKeXrpCXMJqbtKKsLx8'
CHAT_ID = '781095523'

counter = 0

@app.route('/')
def index():
    # Отображение главной страницы с текущим значением счетчика
    return render_template('index.html', counter=counter)

@app.route('/tap', methods=['POST'])
def tap():
    global counter
    # Увеличение счетчика
    counter += 1
    message = f'Tap Counter: {counter}'
    send_message(message)
    # Возвращение нового значения счетчика в формате JSON
    return jsonify({'counter': counter})

@app.route('/reset', methods=['POST'])
def reset():
    global counter
    # Сброс счетчика
    counter = 0
    message = 'The counter has been reset.'
    send_message(message)
    # Возвращение нового значения счетчика в формате JSON
    return jsonify({'counter': counter})

@app.route('/stats', methods=['GET'])
def stats():
    global counter
    # Возвращение текущего значения счетчика в формате JSON
    return jsonify({'counter': counter})

def send_message(message):
    # Отправка сообщения в чат Telegram
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

if __name__ == '__main__':
    # Запуск Flask-приложения
    app.run(debug=True)
