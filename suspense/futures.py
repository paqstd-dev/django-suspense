import uuid


def create(nodelist, context):
    key = str(uuid.uuid4())

    def task():
        return key, nodelist.render(context)

    return key, task
