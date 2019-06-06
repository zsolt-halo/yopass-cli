"""CLI Interface for Yopass server."""

import json
import random
import string
import os
import click
from sjcl import SJCL
import requests


@click.group()
def cli():
    """CLI Interface for Yopass server."""


@cli.command()
@click.option(
    "--outmode", "-m",
    type=click.Choice(["verbose", "one-click-link", "short-link", "id"]),
    default="one-click-link",
    help="Which type of link to return"
)
@click.option(
    "--outformat", "-f", type=click.Choice(["plain", "json"]), default="json",
    help="Return output in plain text or json format.")
@click.option("--expires", "-e", type=click.Choice(["1h", "1d", "1w"]), default="1h")
@click.argument("secret", type=click.STRING, default=click.get_text_stream('stdin'))
def send(secret, expires, outmode, outformat):
    """Submit secret to server. Optionally pipe secret via stdin.

    """
    backend = os.environ.get("YOPASS_BACKEND_URL")
    if backend is None:
        click.echo(
            """YOPASS_BACKEND_URL is not defined, run export
            YOPASS_BACKEND_URL=<your backend> first"""
        )
        exit(1)
    frontend = os.environ.get("YOPASS_FRONTEND_URL")
    if frontend is None and outmode != "id":
        click.echo(
            """YOPASS_FRONTEND_URL is not defined, run export
            YOPASS_FRONTEND_URL=<your frontend> first"""
        )
        exit(1)
    try:
        secret = secret.read()
    except AttributeError:
        pass

    passphrase = generate_passphrase(15)
    cypherdict = SJCL().encrypt(secret.encode(), passphrase)
    converted_cypherdict = {}

    for key, value in cypherdict.items():
        try:
            converted_cypherdict[key] = value.decode("utf-8")
        except AttributeError:
            converted_cypherdict[key] = value

    expiry_dict = {"1h": 3600, "1d": 86400, "1w": 604800}
    payload = {
        "expiration": expiry_dict[expires],
        "secret": json.dumps(converted_cypherdict),
    }
    response = {}
    try:
        response = requests.post(
            "{:s}/secret".format(backend), data=json.dumps(payload)
        )
    except requests.exceptions.HTTPError as errh:
        click.echo("HTTP Error: {:s}".format(errh))
        exit(1)
    except requests.exceptions.ConnectionError as errc:
        click.echo("Error Connecting: {:s}".format(errc))
        exit(1)
    except requests.exceptions.Timeout as errt:
        click.echo("Timeout: {:s}".format(errt))
        exit(1)
    except requests.exceptions.RequestException as err:
        click.echo("Request Exception: {:s}".format(err))
        exit(1)

    secret_id = json.loads(response.text)["message"]

    one_click_link = "{:s}/#/s/{:s}/{:s}".format(
        frontend, secret_id, passphrase)
    short_link = "{:s}/#/s/{:s}".format(frontend, secret_id)

    if outmode == "verbose":
        if outformat == "json":
            click.echo(
                json.dumps(
                    {
                        "one-click-link": one_click_link,
                        "short-link": short_link,
                        "decryption-key": passphrase,
                    }
                )
            )
        else:
            click.echo(one_click_link)
            click.echo(short_link)
            click.echo(passphrase)
    elif outmode == "short-link":
        if outformat == "json":
            click.echo(json.dumps(
                {"short-link": short_link, "decryption-key": passphrase}))
        else:
            click.echo(short_link)
            click.echo(passphrase)
    elif outmode == "id":
        if outformat == "json":
            click.echo(json.dumps(
                {"id": secret_id, "decryption-key": passphrase}))
        else:
            click.echo(secret_id)
            click.echo(passphrase)
    elif outmode == "one-click-link":
        if outformat == "json":
            click.echo(json.dumps({"one-click-link": one_click_link}))
        else:
            click.echo(one_click_link)


@cli.command()
@click.option(
    "--outformat", "-f",
    type=click.Choice(["plain", "json"]),
    default="json",
)
@click.argument("sid", type=click.STRING)
@click.argument("passphrase", type=click.STRING)
def get(sid, passphrase, outformat):
    """Get secret from server

    """
    backend = os.environ.get("YOPASS_BACKEND_URL")
    if backend is None:
        click.echo(
            "YOPASS_BACKEND_URL is not defined, "
            "run export YOPASS_BACKEND_URL=<your backend> first"
        )
        exit(1)
    try:
        response = requests.get("{:s}/secret/{:s}".format(backend, sid))
    except requests.exceptions.HTTPError as errh:
        click.echo("HTTP Error: {:s}".format(errh))
        exit(1)
    except requests.exceptions.ConnectionError as errc:
        click.echo("Error Connecting: {:s}".format(errc))
        exit(1)
    except requests.exceptions.Timeout as errt:
        click.echo("Timeout: {:s}".format(errt))
        exit(1)
    except requests.exceptions.RequestException as err:
        click.echo("Request Exception: {:s}".format(err))
        exit(1)

    response_dict = json.loads(response.text)
    response_message = response_dict["message"]
    if response_message == "Secret not found":
        click.echo("The requested secret was not found.")
        click.echo(
            "Please check if you have entered the sid (secret id) properly.")
        click.echo("The secret might have expired or got opened previously.")
        exit(1)

    print(response.text)
    cypherdict = json.loads(response_message)
    decrypted_secret = SJCL().decrypt(cypherdict, passphrase)

    if outformat == "json":
        click.echo(json.dumps({"secret": decrypted_secret}))
    else:
        click.echo(decrypted_secret)


def generate_passphrase(length):
    """Generate passphrase locally.

    """
    result = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )
    return result


if __name__ == "__main__":
    cli()
