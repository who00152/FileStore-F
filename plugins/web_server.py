from aiohttp import web

async def health_check(request):
    return web.Response(text="OK", status=200)

async def web_server():
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)  # Optional: for root endpoint
    return app
