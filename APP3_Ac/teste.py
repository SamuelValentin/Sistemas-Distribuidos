
import threading
import time
import random
from datetime import date
from datetime import datetime
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sse import sse
import redis
from flask.views import MethodView
from threading import Thread

r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

Alerta = {
    "": 'nao'
}

agenda = [
    {
        'nome': 'teste nome',
        'data': 'teste data',
        'horario': ' teste horario',
        'convidado': ['convidado1', 'convidado2']
    },
]
agenda2 = {
    'teste': [
        ['data'],
        ['hora'],
        [['convidados']]
    ]
}
# cadastro 2, ele nao envia convite para os conviados
# @app.route('/verifica', methods=['POST'])


@app.route('/cadastroag', methods=['POST'])
def cadastro():
    nome = request.json['nome']
    nomecomp = request.json['nomecomp']
    data = request.json['data']
    horario = request.json['horario']
    convidado = request.json['convidado']
    print('novo')
    agenda3 = {
        'nome': nomecomp,
        'data': data,
        'horario': horario,
        'convidado': [convidado]
    }
    Alerta[convidado] = 'sim'
    print(agenda[0]['nome'])
    print(agenda)
    print(agenda3)
    agenda3['convidado'].append(nome)
    agenda.append(agenda3)
    msg = 'compromisso criado pelo '+nome + ' com o nome de ' + nomecomp + \
        ' na data '+data+' no horario '+horario+' com o convidados '+convidado
    print(msg)

    return enviar_mensagem(msg, 'cadastronovousuario'+nome)


@app.route('/busca', methods=['POST'])
def busca():
    msg = ''
    nome = request.json['nome']
    data = request.json['data']
    for comp in agenda:
        print('testando ++++++++++++++++++++++++')
        print(comp)
        print(comp['data'])
        if comp.get('data') == data:
            msg += 'compromisso ' + comp['nome'] + ' na data '+str(comp['data']) + \
                ' no horario '+comp['horario'] + \
                ' com o convidados '+str(comp['convidado'])+'\n'
    return enviar_mensagem(msg, 'cadastronovousuario'+nome)


@app.route('/cadcog', methods=['POST'])
def colega():
    msg = ''
    nome = request.json['nome']
    nomecomp = request.json['nomecomp']
    Alerta[nome] = 'sim'
    for comp in agenda:
        if comp.get('nome') == nomecomp:
            comp['convidado'].append(nome)
            msg += 'compromisso ' + comp['nome'] + ' na data '+str(comp['data']) + \
                ' no horario '+comp['horario'] + \
                ' com o convidados '+str(comp['convidado'])+'\n'
    return enviar_mensagem(msg, 'cadastronovousuario'+nome)


@app.route('/cancel', methods=['POST'])
def cancel():
    msg = ''
    nome = request.json['nome']
    nomecomp = request.json['nomecomp']
    for comp in agenda:
        if comp.get('nome') == nomecomp:
            comp['convidado'].remove(nome)
            msg += 'compromisso ' + comp['nome'] + ' na data '+str(comp['data']) + \
                ' no horario '+comp['horario'] + \
                ' com o convidados '+str(comp['convidado'])+'\n'
    return enviar_mensagem(msg, 'cadastronovousuario'+nome)


@app.route('/cancelalert', methods=['POST'])
def cancelalert():
    nome = request.json['nome']
    nomecomp = request.json['nomecomp']
    Alerta[nome] = 'nao'
    msg = 'nao ira mais receber alerta do compromisso ' + nomecomp
    return enviar_mensagem(msg, 'cadastronovousuario'+nome)


def enviar_mensagem(mensagem, tipo):
    print("entrou")
    with app.app_context():
        sse.publish({"message": mensagem}, type=tipo)
        return 'Messagem sent!'


@app.route('/cadastro', methods=['POST'])
def inicia():
    nome = request.json['nome']
    agenda3 = {
        'nome': 'tesfasggads nome',
        'data': 'tesasdgdsaa',
        'horario': ' tesgsdarario',
        'convidado': ['convigads1']
    }
    Alerta[nome] = 'sim'
    print(agenda3)
    agenda.append(agenda3)
    print('++++++++++++++++++++++++++++')

    print(agenda)
    return enviar_mensagem('bem vindo '+nome, 'cadastronovousuario'+nome)


def EnviaAlerta():
    while True:
        time.sleep(5)
        print('iniciou a thread pro alert')
        today = datetime.now()
        print('data '+str(today))
        today = today.strftime("%Y-%m-%d")
        print('data '+str(today))
        for comp in agenda:
            time.sleep(3)
            print('data que foi passado: '+comp.get('data'))
            if comp.get('data') == today:
                print('entrou?')
                horario = comp.get('horario')
                hora_agr = datetime.now()  # hora
                hora_not = hora_agr - \
                    timedelta(
                        minutes=10)
                hora_not = hora_not.strftime("%H:%M")
                print('HORA NOTIFICA ' + hora_not)
                print('TEIQ SER MENOR Q AGR ' + horario)
                print('E TAMO VERIFICANDO SE PODE RECEBER O ALERTA ' +
                      str(comp.get('convidado')))
                for conv in comp.get('convidado'):

                    if(hora_not <= horario and Alerta[conv] == "sim"):
                        Alerta[conv] = "nao"
                        msg = 'ta chegano a hora do compromisso ' + comp['nome'] + ' na data '+str(comp['data']) + \
                            ' no horario '+comp['horario'] + \
                            ' com o convidados '+str(comp['convidado'])+'\n'
                        enviar_mensagem(msg,
                                        'cadastronovousuario'+conv)


t1 = Thread(target=EnviaAlerta, args=())
t1.daemon = True
t1.start()

app.run(debug=True)
