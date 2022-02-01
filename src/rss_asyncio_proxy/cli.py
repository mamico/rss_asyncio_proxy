"""Console script for rss_asyncio_proxy."""
import sys
from uri import URI
import click
import asyncio
from aiohttp import web
from aiocache import caches
from .proxy import RSSProxy
from .worker import worker, consumer


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=8000)
# TODO: @click.option('--whitelist', default='.*')
@click.option('--redis', default=None, help="redis uri. e.g. redis://127.0.0.1:6379/?db=0")
def main(host: str, port: int, redis: str) -> int:
    """Console script for rss_asyncio_proxy."""
    app = web.Application()
    # TODO: redis
    if redis:
        redis_uri = URI(redis)
        caches.set_config({
            'default': {
                'cache': "aiocache.RedisCache",
                'endpoint': redis_uri.host,
                'port': redis_uri.port,
                'db': redis_uri.query.get('db', 0),
                'serializer': {
                    'class': "aiocache.serializers.JsonSerializer"
                },
            },
        })
    else:
        caches.set_config({
            'default': {
                'cache': "aiocache.SimpleMemoryCache",
                'serializer': {
                    'class': "aiocache.serializers.JsonSerializer"
                },
            },
        })
    loop = asyncio.new_event_loop()
    queue = asyncio.Queue(loop=loop)
    RSSProxy(app, queue)
    loop.create_task(consumer(queue), name="consumer")
    loop.create_task(worker(), name="worker")
    web.run_app(app, loop=loop, host=host, port=port)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
