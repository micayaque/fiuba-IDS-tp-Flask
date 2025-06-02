from flask import Flask, render_template, request, make_response, jsonify, url_for

app = Flask(__name__)

@app.route("/")
def base ():
    return render_template('grupos_por_materia.html')

if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)