from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("test.html")


if __name__ == "__main__":
    # # ngrok.set_auth_token("2uHI6Rn7WxHxXq7Sy25DaNp1KzQ_22S8KCsMwQNfnQJuAHJ7h")
    # ngrok_tunnel = ngrok.connect(5000)
    # print(f"Public URL: {ngrok_tunnel.public_url}")

    app.run(port=5000)
    # app.run(debug=True)
