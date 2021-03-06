from flask import Flask, request, render_template, redirect, url_for
import os, threading, json, websockets
import assistant, all_scores

app = Flask(__name__)
@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/scoreRoute", methods=["POST"])
def score_route():
    data = str(request.get_json(force=True)).replace("'", "\"")
    dangers = all_scores.get_all_scores(data, "pickle_test.p", 0.007)
    return json.dumps(dangers)

@app.route("/assistant", methods=["POST"])
def startcall():
    threading.Thread(target=assistant.run, args=()).start()
    # data = request.get_json(force=True)
    # threading.Thread(target=assistant.run_demo, args=data)
    return ""

# @app.route("/calling", methods=["GET"])
# def calling():
#     return render_template("calling.html")

@app.route("/demo/assistant", methods=["POST"])
def startdemocall():
    phone_num = "+1{}".format(list(request.form.to_dict().keys())[0])
    global CALL
    CALL = assistant.Call(phone_num)
    return ""

@app.route("/demo/update", methods=["POST"])
def handle_update():
    score = float(list(request.form.to_dict().keys())[0])
    print("Road segment index: {}".format(score))
    if score < 0.5:
        CALL.update_good()
    elif score < 0.65:
        pass
    else:
        CALL.update_bad()
    return ""


# @app.route("/demo", methods=["GET"])
# def demo_map():
#     return render_template("demo.html") 

# @app.route("/subscribe-ws", methods=["GET"])
# def subscribe_ws():
#     return

if __name__ == "__main__":
    app.run(debug=True)