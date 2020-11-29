# coding=utf-8

from argparse import ArgumentParser
import struct
import sys

from dnslib import DNSRecord, DNSLabel
from dnslib.server import DNSHandler, DNSServer
from dnslib.proxy import send_tcp, send_udp
import psutil


class DPDHandler(DNSHandler):
    upstream_dns = None
    dns_pattern = None

    def get_reply(self, data):
        try:
            host, port = self.upstream_dns.split(':', 1)
        except ValueError:
            host = self.upstream_dns
            port = 53
        else:
            port = int(port)

        # Parse client request
        request = DNSRecord.parse(data)
        self.detect_process(request)

        # Proxy request to upstream server
        if self.protocol == 'tcp':
            data = struct.pack("!H", len(data)) + data
            response = send_tcp(data, host, port)
            response = response[2:]
        else:
            response = send_udp(data, host, port)

        return response

    def detect_process(self, request):
        query_names = []
        is_match = False

        for q in request.questions:
            query_names.append(str(q.qname)[:-1])
            # Filter process output by glob pattern
            if self.dns_pattern and q.qname.matchGlob(self.dns_pattern):
                is_match = True

        if self.dns_pattern and not is_match:
            return

        # Find process by port and print his command line
        client_addr, client_port = self.client_address
        for proc in psutil.process_iter():
            for conns in proc.connections(kind='udp4'):
                if conns.laddr.port == client_port:
                    cmd = ' '.join(proc.cmdline())
                    print('%s> %s (%s)' %
                          (','.join(query_names), cmd, proc.username()))


def main():
    parser = ArgumentParser(description='Process detector by DNS usage.')
    parser.add_argument('-a', '--address',
                        default='127.0.0.1',
                        help='local proxy address, default 127.0.0.1')
    parser.add_argument('-p', '--port',
                        type=int,
                        default=53,
                        help='local proxy port, default 53')
    parser.add_argument('-u', '--upstream',
                        default='8.8.8.8:53',
                        help='upstream DNS server, default 8.8.8.8:53')
    parser.add_argument('-t', '--pattern',
                        metavar='GLOB',
                        default=None,
                        help='glob pattern of query to detect process name on '
                             'match. By default, prints the process for each '
                             'request.')
    args = parser.parse_args()

    DPDHandler.upstream_dns = args.upstream
    if args.pattern:
        DPDHandler.dns_pattern = DNSLabel(args.pattern)

    server = DNSServer(None,  # здесь не нужен Resolver
                       address=args.address,
                       port=args.port,
                       tcp=False,
                       handler=DPDHandler)

    print('Start DNS server on %s:%d...' % (args.address, args.port))
    server.start()


if __name__ == '__main__':
    # TODO: add README.rst
    # TODO: pattern is list of globs
    # TODO: logging to file
    # TODO: TCP server
    sys.exit(main)
