import httpx
import asyncio
import socket


async def check_http_endpoint(url):
    destination = url.address + ":" + str(url.port)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.head(destination)
            if response.status_code == 200:
                return True, response.status_code
            else:
                return False, response.status_code
        except httpx.RequestError:
            return False, -1


async def check_ftp_endpoint(url):
    try:
        # Create a socket connection to the FTP server
        reader, writer = await asyncio.open_connection(url.address, url.port)
        # The server is running if the connection is successful
        response = await reader.readline()  # Read the first response line
        response_text = response.decode().strip()
        code = int(response_text.split(" ")[0])
        writer.close()
        await writer.wait_closed()
        return True, code
    except (ConnectionRefusedError, socket.gaierror):
        return False, -1
    except Exception:
        return False, -1
