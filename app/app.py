from flask import Flask, render_template, request
import redis

##app = Flask(__name__)
app= Flask(__name__, template_folder='../templates')
r = redis.Redis(host='redis', port=6379)

@app.route('/')
def index():
    votes_dog = int(r.get('dog') or 0)
    votes_cat = int(r.get('cat') or 0)
    return render_template("index.html", dog=votes_dog, cat=votes_cat)

@app.route('/vote', methods=['POST'])
def vote():
    vote = request.form.get('vote')
    if vote == 'dog':
        r.incr('dog')
    elif vote == 'cat':
        r.incr('cat')
    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
