import concurrent.futures
import uuid

__futures = {}


def create(nodelist, context):
    key = str(uuid.uuid4())

    executor = concurrent.futures.ThreadPoolExecutor()
    __futures[key] = executor.submit(nodelist.render, context)

    return key


def get(key):
    if key not in __futures:
        return None

    return __futures.pop(key).result()
