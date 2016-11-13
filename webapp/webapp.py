from flask import Flask
import click
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world"

@click.command()
@click.option("--debug", is_flag=True, default=False)
def run(debug):
    app.run(host="0.0.0.0", debug=debug)


if __name__ == '__main__':
    run()
