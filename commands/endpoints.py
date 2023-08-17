import click
from uuid import uuid4

from models.url import URLModel


@click.group(name="endpoints")
def endpoints_group():
    """
    Manage endpoints.
    """
    pass


@endpoints_group.command(name="register")
@click.argument("protocol")
@click.argument("port", type=int)
@click.argument("address")
@click.argument("interval", type=int)
def register_endpoint(protocol, port, address, interval):
    """
    Registering an endpoint in our database
    """
    u = URLModel.create(
        id=str(uuid4()),
        address=address,
        port=port,
        protocol=protocol,
        interval=interval,
    )
    click.echo(f"Registered endpoint: {u}")


@endpoints_group.command(name="list")
@click.option("--protocol", "-r", help="Filter endpoints by protocol.")
@click.option("--port", "-p", type=int, help="Filter endpoints by port.")
@click.option("--address", "-a", help="Filter endpoints by address.")
def list_endpoints(protocol, port, address):
    """
    List all endpoints or filter by protocol and/or port and/or address.
    """
    q = URLModel.all()
    if protocol:
        q = q.filter(protocol=protocol)
    if port:
        q = q.filter(port=port)
    if address:
        q = q.filter(address=address)
    click.echo(" [!] Listing endpoints")
    for u in q.all():
        click.echo(f" [-] {u.id}, {u.address}, {u.port}, {u.protocol}, {u.interval}")


@endpoints_group.command()
@click.argument("endpoint_id", type=int)
@click.argument("status_code", type=int)
@click.argument("occurrence_time")
@click.argument("notif_channel_id")
def set_alert(endpoint_id, status_code, occurrence_time, notif_channel_id):
    """
    Set an alert for an endpoint.
    """
    # Your code to handle the 'set' command for alerts goes here
    click.echo(
        f"Setting alert for endpoint ID: {endpoint_id}, Status Code: {status_code}, Occurrence Time: {occurrence_time}, Notif Channel ID: {notif_channel_id}"
    )


@endpoints_group.command()
@click.argument("endpoint_id")
def delete(endpoint_id):
    """
    Delete an endpoint.
    """
    u = URLModel.all().get(id=endpoint_id)
    click.echo(f"Deleting endpoint: {u}")
    u.delete()

