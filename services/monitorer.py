import asyncio
import time
from uuid import uuid4
import datetime as dt

from models.url import URLModel
from models.history import HistoryModel
from utils.monitor import check_http_endpoint, check_ftp_endpoint

lock = asyncio.Lock()


# Function to perform monitoring for a single URL
async def monitor_url(url):
    while True:
        result = str(url)

        # Store the result in the global variable
        if url.protocol == "http" or url.protocol == "https":
            res = await check_http_endpoint(url)
        elif url.protocol == "ftp":
            res = await check_ftp_endpoint(url)
        # Print the result
        print(res, flush=True)

        # Acquire the lock before writing to the global_results list
        async with lock:
            HistoryModel.create(
                id=str(uuid4()),
                endpoint=url.id,
                status=res[1],
                ok=int(res[0]),
                ts=int(time.time()),
                date=str(dt.date.today()),
            )

        # Wait for the monitoring interval before running the task again
        await asyncio.sleep(url.interval)


# Function to run the monitoring process for all URLs in the list
async def run_monitoring(urls):
    tasks = [monitor_url(url) for url in urls]
    await asyncio.gather(*tasks)
