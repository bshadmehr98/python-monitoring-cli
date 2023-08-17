import click
from uuid import uuid4
import plotext as plt

from models.history import HistoryModel


@click.group(name="history")
def history_group():
    """
    Manage history.
    """
    pass


@history_group.command(name="list")
@click.option("--endpoint", "-e", help="Filter history by endpoint")
@click.option("--ok", "-o", type=bool, help="Filter history by success status")
def list(endpoint, ok):
    """
    Show a report of history
    """
    q = HistoryModel.all()
    if endpoint:
        q = q.filter(endpoint=endpoint)
    if ok is not None:
        q = q.filter(ok=int(ok))
    click.echo(" [!] Listing history")
    data = []
    for e in q.all():
        data.append({"id": e.id, "ok": e.ok, "ts": e.ts})
        click.echo(f" [-] {e.id}, {e.endpoint}, {bool(e.ok)}, {e.date}")


@history_group.command(name="report")
@click.argument("endpoint")
@click.argument("mode")
def report(endpoint, mode):
    """
    Providing report for an endpoint
    """
    q = HistoryModel.all()
    q = q.filter(endpoint=endpoint)
    data = {}
    for e in q.all():
        if e.date not in data:
            data[e.date] = {"success": 0, "failed": 0}
        if e.ok:
            data[e.date]["success"] += 1
        else:
            data[e.date]["failed"] += 1
    if mode == "list":
        for k, v in data.items():
            if v["failed"] > 0:
                click.echo(
                    click.style("  [*] ", fg="red")
                    + f"{k}: Failed: {click.style(v['failed'], fg='red')}, success: {click.style(v['success'], fg='green')}"
                )
            else:
                click.echo(
                    click.style("  [*] ", fg="green")
                    + f"{k}: Failed: {v['failed']}, success: {click.style(v['success'], fg='green')}"
                )
    elif mode == "chart":
        dates = []
        success = []
        failed = []
        for k, v in data.items():
            dates.append(k)
            success.append(v["success"])
            failed.append(v["failed"])
        plt.simple_multiple_bar(
            dates,
            [success, failed],
            width=100,
            labels=["success", "failed"],
            title=f"[!] Here is the report for: {endpoint}",
        )
        plt.show()
    else:
        raise Exception("Invalid mode option, options are: list, chart")
