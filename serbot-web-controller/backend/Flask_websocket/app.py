from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from pop import Pilot
import time



def own_id_adress():
    #import socket
    #return socket.gethostbyname(socket.gethostname())
    #return '192.168.2.56'
    return '127.0.0.1'

def create_rand_string():
    import string
    import random

    _LENGTH = 4
    string_pool = string.ascii_lowercase
    result = ""
        
    for i in range(_LENGTH):
        result += random.choice(string_pool)
    return result

def client_ip():
    #return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return request.remote_addr

def create_app(app, socketio, bot):
    @app.route('/abc')
    def abc():
        return "ABC"

    @app.route('/', methods=['GET', 'POST'])
    def login():
        global password, session

        error = None
        if request.method == 'POST':
            if request.form['password'] != password:
                error = 'Invalid Credentials. Please try again.'
            else:
                password = create_rand_string()
                session = client_ip()

                print("Password : ", password)
                print("Session : ", session)

                return redirect(url_for('joystic_control'))

        return render_template('login.html', error=error)

    @app.route('/control')
    def joystic_control():
        global session

        if client_ip() != session:
            return redirect(url_for('login'))
        else:
            return render_template('index.html')


    @app.route('/reset')
    def reset_session():
        global session, password
    
        if client_ip() == own_id_adress():
            session = own_id_adress()
            password = create_rand_string()
            print("Reset!")
            print("Password : ", password)
            bot.stop()
            return "Reset!"
        else:
            return "You are not Admin!"

    @app.route('/hostname')
    def get_hostname():
        import platform
        global session

        print(platform.node())
        return platform.node()

    @app.route('/password')
    def get_password():
        global password
        if client_ip() == own_id_adress():
            print(password)
            return password
        else:
            return ""


    def messageReceived(methods=['GET', 'POST']):
        print('message was received!!!')

    @socketio.on('joystic')
    def handle_my_custom_event(json, methods=['GET', 'POST']):
        if session != client_ip():
             return
        print('received my event: ' + str(json))

        degree = 360 - (json['degree'] + 270) % 360

        if json['distance'] == 0:
            bot.stop()
        else:
            bot.move(degree, json['distance'] * 1.5)


if __name__ == "__main__":
    bot = Pilot.SerBot()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'BCODE_Flask'
    socketio = SocketIO(app)
    password = "default"
    session = own_id_adress()

    print(own_id_adress(), 'test')
    create_app(app, socketio, bot) 


    socketio.run(app, debug=False, host="0.0.0.0", port=5000)
