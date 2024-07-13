from flask import Flask,render_template
from web.sqlite import webSqlite

app = Flask(__name__)
app.config["SECRET_KEY"] = "SourQuarendenLiquid"


@app.route("/")
def hello_world():
    return render_template("index.html",actTitle="欢迎",actHeadline="酸苹果汁")

app.register_blueprint(webSqlite,url_prefix="/sqlite")


if __name__ == "__main__":
    app.run()