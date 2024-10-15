def singleton(class_):
    instances: dict = {}

    def getinstance(*args, **kwargs):
        nonlocal instances
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance
