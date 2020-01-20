def remove_empty(dictionary):
    return {
        k: v
        for k, v in dictionary.items()
        if v is not None
    }
