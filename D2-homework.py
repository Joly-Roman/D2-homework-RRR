import os
from bottle import Bottle, request, route, run, response
import sentry_sdk
from sentry_sdk.integrations.bottle import BottleIntegration
from bottle import route, run

# Привязка логирования sentry
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[BottleIntegration()]
)

app = Bottle()

# Основаная страница
@app.route("/")
def index():
    html = """
<!doctype html>
<html lang="en">
  <head>
    <title>D2 Homework </title>
  </head>
  <body>
    <div class="container">
        <h1>Доступно два маршрута </h1>
        <h2 ><a href='http://localhost:8080/success'>Удачное установление соединения </a></h2>
        <h2 ><a href='http://localhost:8080/fail'>Ошибка сервера</a></h2>
    </div>
  </body>
</html>
"""
    return html

# Маршрут, выводящий ошибку
@app.route("/fail")
def fail():
    raise RuntimeError("It's a trap!")
    return

# Маршрут, работающий без ошибки
@app.route("/success")
def success():
    return f"Статус HTTP - {response.status}"



if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host="localhost", port=8080, debug=True)