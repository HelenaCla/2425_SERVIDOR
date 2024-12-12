from flask import Flask, render_template,request, url_for, make_response
app = Flask(__name__)

@app.route('/')
def index():
    color=request.cookies.get('colorH1')
    return render_template('main.html',color=color)

@app.route('/actualiza', methods=['GET', 'POST'])
def actualiza():
    color = request.args.get('estilo')
    resp = make_response(render_template('main.html',color=color))
    resp.set_cookie('colorH1', color,max_age=60*10) #max_age indica el temps que quedarà emmagatzemada en segons (ara 10 minuts)
    return resp

if __name__ == '__main__':
    app.run()
