def calculate(result):
    age_list = list(map(get_age, result))
    bin_list = list(map(bin_age, age_list))

    print(age_list)
    print(bin_list)

    return max(set(bin_list), key=bin_list.count)


def get_age(x):
    return x['faceAttributes']["age"]


def bin_age(x):
    if x >= 0 and x < 10:
        category = "0-10"
    if x >= 10 and x < 18:
        category = "9-18"
    if x >= 18 and x < 30:
        category = "19-30"
    if x >= 30 and x < 70:
        category = "31-70"
    if x >= 70:
        category = "above 70"

    return category
