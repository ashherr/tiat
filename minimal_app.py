from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>TIAT Minimal Test</h1><p>This is a minimal test page that works.</p>"

@app.route('/env')
def show_env():
    import os
    env_vars = sorted(os.environ.keys())
    return "<h1>Environment Variables</h1><pre>" + "\n".join(env_vars) + "</pre>"

if __name__ == '__main__':
    app.run() 