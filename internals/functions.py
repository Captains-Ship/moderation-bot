__all__ = (
    "ignore_exc"
)

async def ignore_exc(func):
    """Important! you need to pass the coroutine as if you were calling it, but without the `await`!"""
    try:
        await func
    except:
        pass

