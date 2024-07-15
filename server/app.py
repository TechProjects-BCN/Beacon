from flask import Flask, render_template, request, Response

button_status = [0, 0, 0, 0]

app = Flask(__name__)
app.config["SECRET_KEY"] = "fejhwfjewlk"


@app.route("/")
def main_route():
    return render_template("index.html")


@app.route("/get_press")
def get_press():
    return {"button_status": button_status}

@app.route("/press", methods=["POST"])
def button_press():
    button_id = request.json["id"]
    button_status[button_id] = request.json["status"]
    return {"status": button_status[button_id]}

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
