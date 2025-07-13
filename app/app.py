from flask import Flask, render_template, request
import redis
import os

# Read from environment variables set by ConfigMap
redis_host = os.getenv('REDIS_HOST', 'localhost')
app_title = os.getenv('APP_TITLE', 'Voting App')

print("🔧 REDIS_HOST:", redis_host)
print("📝 APP_TITLE:", app_title)

app = Flask(__name__, template_folder='../templates')
r = redis.Redis(host=redis_host, port=6379)

@app.route('/')
def index():
    votes_dog = int(r.get('dog') or 0)
    votes_cat = int(r.get('cat') or 0)
    votes_buffalo = int(r.get('buffalo') or 0)
    return render_template("index.html", dog=votes_dog, cat=votes_cat, buffalo=votes_buffalo, title=app_title, redis_host=redis_host)

@app.route('/vote', methods=['POST'])
def vote():
    vote = request.form.get('vote')
    if vote in ['dog', 'cat', 'buffalo']:
        r.incr(vote)
    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
