import asyncio
import inspect
import uuid

from asgiref.sync import sync_to_async


def create(nodelist, context):
    key = str(uuid.uuid4())

    def task():
        return key, nodelist.render(context)

    return key, task


def create_async(nodelist, context, async_context_keys):
    key = str(uuid.uuid4())

    async def task():
        coroutines = []
        if async_context_keys:
            for k in async_context_keys:
                v = context.get(k, None)
                if v and inspect.isawaitable(v):
                    coroutines.append((k, v))
        else:
            flatten_context = context.flatten()
            for k, v in flatten_context.items():
                if inspect.isawaitable(v):
                    coroutines.append((k, v))

        async def wait_for(to_await):
            k, v = to_await
            return k, await v

        results = await asyncio.gather(*[wait_for(co) for co in coroutines])
        new_context = {}
        for k, v in results:
            new_context[k] = v

        context.push(new_context)
        return key, await sync_to_async(nodelist.render)(context)

    return key, task()
