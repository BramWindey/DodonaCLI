import click
import http.client

from source import get_data
from source import handle_flags


@click.command(help="Display info")
def display():
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    handle_flags.handle_display(config, connection, headers)
