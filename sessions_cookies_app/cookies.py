''' Code from: https://overiq.com/flask-101/cookies-in-flask/ '''
from flask import Flask, render_template, request, make_response, url_for, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = 'my_super_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response("Setting a cookie")
        res.set_cookie('foo', 'bar', max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
    return res


@app.route('/delete-cookie/')
def delete_cookie():
    res = make_response("Cookie Removed")
    res.set_cookie('foo', 'bar', max_age=0)
    return res


@app.route('/article/', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60 * 60 * 24 * 15)
        res.headers['location'] = url_for('article')
        return res, 302
    return render_template('article.html')


if __name__ == '__main__':
    app.run(debug=True)
