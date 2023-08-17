import click

from commands.endpoints import endpoints_group
from commands.alerts import alerts_group
from commands.channel import channels_group
from commands.monitor import monitor_group
from commands.history import history_group


@click.group()
def cli():
    pass


cli.add_command(endpoints_group)
cli.add_command(alerts_group)
cli.add_command(channels_group)
cli.add_command(monitor_group)
cli.add_command(history_group)

