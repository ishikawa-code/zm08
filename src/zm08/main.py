import datetime

import typer
from zm08 import mathtools

app = typer.Typer()


@app.callback()
def callback():
    """
    A Collection of Useful Commands
    """


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
def is_prime(x):
    """
    Prime Number Test 
    """
    typer.echo(mathtools.is_prime(x))

@app.command()
def multiply(x, y):
    """
    Multiplication Table 
    """
    typer.echo(mathtools.multiply(x, y))