import click
from uuid import uuid4
import time

from models.alert import AlertModel
from models.channel import ChannelModel
from models.history import HistoryModel
from utils.slack import send_slack_message


@click.group(name="alerts")
def alerts_group():
    """
    Manage alerts.
    """
    pass


@alerts_group.command(name="register")
@click.argument("endpoint_id")
@click.argument("channel_id")
@click.argument("occurrence", type=int)
@click.argument("status_code", type=int)
def register_alert(endpoint_id, channel_id, occurrence, status_code):
    """
    Registering an alert in our database
    """
    a = AlertModel.create(
        id=str(uuid4()),
        channel=channel_id,
        endpoint=endpoint_id,
        occurrence=occurrence,
        status_code=status_code,
    )
    click.echo(f"Registered alert: {a}")


@alerts_group.command(name="list")
@click.option("--endpoint", "-e", help="Filter alerts by endpoint.")
@click.option("--channel", "-c", help="Filter alerts by channel.")
@click.option("--status", "-s", type=int, help="Filter alerts by status.")
def list_alerts(endpoint, channel, status):
    """
    List all alerts or filter by endpoint and/or channel and/or status.
    """
    q = AlertModel.all()
    if endpoint:
        q = q.filter(endpoint=endpoint)
    if channel:
        q = q.filter(channel=channel)
    if status:
        q = q.filter(status_code=status)
    click.echo(" [!] Listing alerts")
    for a in q.all(load_related=True):
        click.echo(
            f" [-] {a.id}, {a.endpoint_obj}, {a.channel_obj}, {a.status_code}, {a.occurrence}"
        )


@alerts_group.command()
@click.argument("alert_id")
def delete(alert_id):
    """
    Delete an alert.
    """
    a = AlertModel.all().get(id=alert_id)
    click.echo(f"Deleting alert: {a}")
    a.delete()


@alerts_group.command(name="start-service")
def start_service():
    """
    Starts alerting service
    """
    alerts = AlertModel.all().all(load_related=True)
    while True:
        for a in alerts:
            click.echo("Checking the alert: " + str(a))
            q = HistoryModel.all()
            q = q.filter(endpoint=a.endpoint)
            should_send = True
            for h in q.all()[0 - a.occurrence :]:
                if h.status != a.status_code:
                    should_send = False
                    break

            click.echo(should_send)
            if should_send:
                pass
                click.echo(a.channel_obj)
                send_slack_message(
                    a.channel_obj.webhook_url,
                    f"{a.endpoint_obj} has faced {a.status_code} ({a.occurrence}) times",
                )

        time.sleep(30)
