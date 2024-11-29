import uuid

from asgiref.sync import sync_to_async


def task(key, nodelist, context):
    return key, nodelist.render(context)


def create(nodelist, context):
    key = str(uuid.uuid4())

    return key, sync_to_async(task)(key, nodelist, context)
