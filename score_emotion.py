def calculate(result):
    if len(result) == 0:
        return "blank"

    scores = list([sum(list(map(get_happiness, result))) / len(result),
    sum(list(map(get_neutral, result))) / len(result),
    sum(list(map(get_sadness, result))) / len(result),
    sum(list(map(get_anger, result))) / len(result),
    sum(list(map(get_surprise, result))) / len(result)])

    index = scores.index(max(scores))

    if index == 0:
        return "happy"
    elif index == 1:
        return "neutral"
    elif index == 2:
        return "sadness"
    elif index == 3:
        return "anger"
    elif index == 4:
        return "surprise"
    else:
        return "boqq"

def get_happiness(x):
    return x['faceAttributes']['emotion']["happiness"]


def get_neutral(x):
    return x['faceAttributes']['emotion']["neutral"]


def get_sadness(x):
    return x['faceAttributes']['emotion']["sadness"]


def get_anger(x):
    return x['faceAttributes']['emotion']["anger"]


def get_surprise(x):
    return x['faceAttributes']['emotion']["surprise"]
