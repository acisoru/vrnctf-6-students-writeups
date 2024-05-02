from flask import Flask, request, render_template

app = Flask(__name__)

app.config.from_object(__name__)


def generate_key(login: str):
    v1 = len(login)
    t2 = v1 * 32
    v2 = 37
    v3 = 1
    key = 0

    while(v1 > 0):
        key = v2 ^ (v2 * (t2 - v2) - v3 + 705 + v2 * (t2 - v2))
        v3 = 4 + (v1 % 2)
        v2 = 31 + (v2 % 3)
        v1 -= 1
    
    return (key * key)


def check_login(login: str):
    ln = len(login)
    if ln < 5 or ln > 14:
        return False
    
    verifyedSymbols = 0

    for e in login:
        if e == '_':
            verifyedSymbols += 1

    if verifyedSymbols < 3:
        return False
    
    return True


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if password.isdigit() == False:
            return "Вы кто такие? Я вас не звал, идите в ПЕНЬ!"

        password = int(password)

        generated = generate_key(username)

        if check_login(username) == False:
            return "Вы кто такие? Я вас не звал, идите в ПЕНЬ!"

        if generated == password:
            return "vrnctf{sl0v3n1k_k3ys}"
        else:
            return "Вы кто такие? Я вас не звал, идите в ПЕНЬ!"
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0")