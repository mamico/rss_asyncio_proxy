"""Main module."""
import time

from aiocache import caches
import aiohttp

from . import GRACE
from . import logger
from . import TTL


class RSSProxy(object):

    def __init__(self, app, queue):
        app.add_routes([
            aiohttp.web.get('/rss-proxy', self.rss_proxy, allow_head=False),
        ])
        self.queue = queue

    @property
    def session(self):
        timeout = aiohttp.ClientTimeout(connect=0.5, total=2*60)
        return aiohttp.ClientSession(timeout=timeout)

    @property
    def cache(self):
        return caches.get('default')

    async def rss_proxy(self, request):
        """Proxy for RSS feeds.
        """
        params = request.rel_url.query
        url = params["url"]
        cache_key = "rss:{url}".format(url=url)

        # TODO: header nella request ?
        cached = await self.cache.get(cache_key)
        if cached:
            if time.time() < cached['expire']:
                logger.warning('DEBUG HIT %s %s %s', url, cached['expire'], len(cached['text']))
                return aiohttp.web.Response(
                    text=cached['text'],
                    headers=cached['headers'],
                )
            else:
                logger.warning('DEBUG EXPIRED %s %s %s', url, cached['expire'], len(cached['text']))

        await self.queue.put(url)

        async with self.session as session:
            try:
                async with session.get(url) as response:
                    result = await response.read()
                    result = result.decode()
                    logger.warning('DEBUG MISS %s %s %s', url, cache_key, len(result))
                    await self.cache.set(
                        cache_key,
                        {'headers': dict(response.headers), 'text': result, 'expire': time.time() + TTL},
                        ttl=TTL + GRACE
                    )
                    return aiohttp.web.Response(text=result, headers=response.headers)
            except:
                logger.exception("ERROR %s", url)
                if cached:
                    logger.warning('DEBUG GRACE %s %s %s', url, cache_key, len(cached['text']))
                    return aiohttp.web.Response(
                        text=cached['text'],
                        headers=cached['headers'],
                    )
                return aiohttp.web.Response(text="", status=500)
