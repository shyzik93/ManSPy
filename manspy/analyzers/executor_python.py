def analyze(message):

    exec(message.text, globals())
    result = execute()
    return result