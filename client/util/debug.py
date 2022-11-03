DEBUG_MESSAGES = True


def debug(*args, **kwargs):
    if DEBUG_MESSAGES:
        print("[DEBUG]", *args, **kwargs)
