import click
from uuid import uuid4

from models.channel import ChannelModel


@click.group(name="channels")
def channels_group():
    """
    Manage channels.
    """
    pass


@channels_group.command(name="register")
@click.argument("channel_type", type=int)
@click.argument("webhook_url")
def register_channel(channel_type, webhook_url):
    """
    Registering a channel in our database
    """
    c = ChannelModel.create(id=str(uuid4()), type=channel_type, webhook_url=webhook_url)
    click.echo(f"Registered channel: {c}")


@channels_group.command()
@click.argument("channel_id")
def delete(channel_id):
    """
    Delete a channel.
    """
    c = ChannelModel.all().get(id=channel_id)
    click.echo(f"Deleting channel: {c}")
    c.delete()


@channels_group.command(name="list")
def list_channels():
    """
    List all channels.
    """
    click.echo(" [!] Listing channels")
    q = ChannelModel.all()
    for c in q.all():
        click.echo(f" [-] {c.id}, {c.type_value}, {c.webhook_url}")
