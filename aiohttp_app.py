import asyncio
import settings
from utils.app_factory import init, shutdown

if __name__ == '__main__':
    log = settings.log

    loop = asyncio.get_event_loop()
    serv_generator, handler, app = loop.run_until_complete(init(loop))
    serv = loop.run_until_complete(serv_generator)
    log.debug('start server %s' % str(serv.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        log.debug(' Stop server begin')
    finally:
        loop.run_until_complete(shutdown(serv, app, handler))
        loop.close()
    log.debug('Stop server end')
