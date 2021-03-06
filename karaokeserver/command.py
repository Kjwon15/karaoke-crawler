import argparse
from .app import app
from .crawler import crawl, crawl_special_indices


def crawl_command(args):
    crawl(args.url, target=args.target, new=args.new)
    if args.special:
        crawl_special_indices(args.url)


def server_command(args):
    app.config['DB_URI'] = args.url
    app.debug = args.debug
    app.run(host=args.host, port=args.port)


parser = argparse.ArgumentParser(prog='karaokeserver')
subparsers = parser.add_subparsers(dest='command')

crawl_parser = subparsers.add_parser('crawl', help='Crawl karaoke database')
crawl_parser.set_defaults(function=crawl_command)
crawl_parser.add_argument('-t', '--target', default=None,
                          help='Target date. example: 2014-11')
crawl_parser.add_argument('-n', '--new', default=False, action='store_true',
                          help='crawl only new data.')
crawl_parser.add_argument('-s', '--special', default=False,
                          action='store_true', help='Crawl special indices.')
crawl_parser.add_argument('url', help='Database url for store karaoke datas')

server_parser = subparsers.add_parser('server', help='query server')
server_parser.set_defaults(function=server_command)
server_parser.add_argument('url', help='Database url for store karaoke datas')
server_parser.add_argument(
    '-H', '--host', default='0.0.0.0', help='Host to bind.')
server_parser.add_argument(
    '-p', '--port', type=int, default='8080', help='Port to bind.')
server_parser.add_argument(
    '-d', '--debug', action='store_true', default=False, help='debug mode')


def main():
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        exit(1)

    args.function(args)


if __name__ == '__main__':
    main()
