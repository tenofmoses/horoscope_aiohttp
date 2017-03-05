from aiohttp import web
import aiohttp_jinja2
import jinja2
import asyncio
import aioredis
import time

zodiacs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']


@aiohttp_jinja2.template('index.html')
async def index(request):
    redis = await aioredis.create_redis(('localhost', 6379))

    redis.close()
    await redis.wait_closed()
    return {
        'date': time.strftime('%d' + '.' + '%m' + '.' + '%Y'),
        'title': 'Гороскоп',
    }

@aiohttp_jinja2.template('zodiac.html')
async def zodiac(request):
    name = request.match_info.get('name')
    if name not in zodiacs:
        raise web.HTTPNotFound(text='Такого знака зодака не существует!')

    redis = await aioredis.create_redis(('localhost', 6379))
    zodiac = await redis.get('horo:%s' % name)

    redis.close()
    await redis.wait_closed()
    return {
        'date': time.strftime('%d' + '.' + '%m' + '.' + '%Y'),
        'name': name,
        'zodiac': zodiac.decode(),

        'title': name,
    }


app = web.Application()

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app.router.add_static('/static/', path='static')
app.router.add_get('/', index)
app.router.add_get('/{name}', zodiac)

web.run_app(app)
