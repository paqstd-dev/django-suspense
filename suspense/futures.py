import asyncio
import inspect
import uuid


def create(nodelist, context):
    key = str(uuid.uuid4())

    def task():
        return key, nodelist.render(context)

    return key, task


def create_async(nodelist, context, async_context_keys, shared_futures=None):
    key = str(uuid.uuid4())
    if shared_futures is None:
        shared_futures = {}

    def resolve_awaitables():
        if async_context_keys:
            items = [(k, context.get(k, None)) for k in async_context_keys]
        else:
            items = list(context.flatten().items())

        awaitables = []
        for k, v in items:
            if inspect.isawaitable(v):
                future = shared_futures.get(id(v))
                if future is None:
                    future = asyncio.ensure_future(v)
                    shared_futures[id(v)] = future
                awaitables.append((k, future))
        return awaitables

    async def task():
        async def wait_for(to_await):
            k, v = to_await
            return k, await v

        results = await asyncio.gather(
            *[wait_for(pair) for pair in resolve_awaitables()]
        )
        context.push(dict(results))
        return key, await asyncio.to_thread(nodelist.render, context)

    return key, task
