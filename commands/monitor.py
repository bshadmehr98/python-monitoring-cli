import click
from uuid import uuid4
import asyncio

from models.alert import AlertModel
from models.channel import ChannelModel
from models.url import URLModel
from models.history import HistoryModel
from services.monitorer import run_monitoring


@click.group(name="monitor")
def monitor_group():
    """
    Monitoring commands.
    """
    pass


@monitor_group.command(name="start")
def start():
    """
    Starts monitoring
    """
    urls = URLModel.all().all()

    # Run the monitoring process asynchronously
    asyncio.run(run_monitoring(urls))

