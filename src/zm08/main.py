#main.py
import datetime

import typer
from zm08 import mathtools
from . import demo
from zm08 import tracker
from . import logic
app = typer.Typer()


@app.callback()
def callback():
    """
    A Collection of Useful Commands
    """

# --- 運動記録アプリのメインコマンド ---
@app.command()
def run():
    """
    運動記録を記入・保存・集計する。
    """
    logic.check_and_update_penalty()
    tracker.record_today()


@app.command()
def now():
    """
    Show local date and time
    """
    today = datetime.datetime.today()
    typer.echo(today.strftime('%A, %B %d, %Y'))


@app.command()
def gcd(x: int, y: int):
    """
    Greatest Common Divisor
    """
    typer.echo(mathtools.gcd(x, y))

@app.command()
def lcm(x: int, y: int):
    """
    Least Common Multiple
    """
    typer.echo(mathtools.lcm(x, y))

@app.command()
def is_prime(x:int):
    """
    Prime Number Test 
    """
    typer.echo(mathtools.is_prime(x))

@app.command()
def multiply(x:int, y:int):
    """
    Multiplication Table 
    """
    typer.echo(mathtools.multiply(x, y))


@app.command()
def hello(name:str="ken"):
    typer.echo(demo.hello(name))







# 他のコマンドがあればここに追加...

if __name__ == "__main__":
    app()


