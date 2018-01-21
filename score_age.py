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
        category = "CHILDREN"
    if x >= 10 and x < 18:
        category = "ADOLESCENT"
    if x >= 18 and x < 30:
        category = "YOUNG ADULT"
    if x >= 30 and x < 40:
        category = "ADULT"
    if x >= 40 and x < 70:
        category = "OLD"

    return category
