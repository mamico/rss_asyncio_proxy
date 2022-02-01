import asyncio
from threading import local
import time

from aiocache import caches
import aiohttp

from . import GRACE
from . import logger
from . import TTL

data = local()
data.urls = set()


async def consumer(queue: asyncio.Queue):
    while True:
        url = await queue.get()
        data.urls.add(url)
        queue.task_done()


async def worker(runevery: int=5*60):
    """Ogni `runevery` secondi, scarica le url in `data.urls` e le mette in cache.

    Args:
        runevery ([int], optional): [description]. Defaults to 5*60.
    """
    while True:
        await asyncio.sleep(runevery)
        # TODO: parallelizzare le fetch ?
        # TODO: gestire gli errori ?
        for url in data.urls:
            cache = caches.get('default')
            cache_key = "rss:{url}".format(url=url)
            # i timeout dello worker sono più alti di quelli delle richieste web
            timeout = aiohttp.ClientTimeout(connect=0.5, total=5*60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.get(url) as response:
                        logger.warning("FETCHED %s", url)
                        result = await response.read()
                        result = result.decode()
                        await cache.set(
                            cache_key,
                            {'headers': dict(response.headers), 'text': result, 'expire': time.time() + TTL},
                            ttl=TTL + GRACE
                        )
                # TODO: se una url da errore troppo volte va inseita in una blacklist
                # e ignorata per un po' di tempo
                except aiohttp.client_exceptions.ServerTimeoutError:
                    logger.warning("TIMEOUT %s", url)
                except aiohttp.client_exceptions.ClientError:
                    logger.exception("ERROR %s", url)
                except Exception as e:
                    logger.exception("ERROR %s", url)
