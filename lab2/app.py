from flask import Flask
import math

app = Flask(__name__)

def integrate(lower, upper, N):
    h = (upper - lower) / N
    s = sum(abs(math.sin(lower + i * h)) * h for i in range(N))
    return s

@app.route('/integral/<float:lower>/<float:upper>')
def get_integral(lower, upper):
    n_values = [10, 100, 1000, 10000, 100000, 1000000]
    results = [f"N={n}: {integrate(lower, upper, n)}" for n in n_values]
    return "<br>".join(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)