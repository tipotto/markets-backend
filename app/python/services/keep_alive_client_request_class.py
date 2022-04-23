from aiohttp.client_reqrep import ClientRequest
import socket


class KeepAliveClientRequest(ClientRequest):
    # async def send(self, conn: "Connection") -> "ClientResponse":
    async def send(self, conn):
        sock = conn.protocol.transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 2)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

        return (await super().send(conn))
