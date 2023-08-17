from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def run_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "pass", "./.data", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()


if __name__ == "__main__":
    run_ftp_server()
