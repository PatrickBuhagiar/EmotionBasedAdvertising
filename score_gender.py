def calculate(result):

    from random import randint

    gender_list = list(map(get_gender, result))
    male_no = gender_list.count("male")
    female_no = gender_list.count("female")

    if male_no > female_no:
        index = 0
    elif male_no == female_no:
        index = randint(0,1)
    elif male_no < female_no:
        index = 1


    if index == 0:
        return "male"
    elif index == 1:
        return "female"
    else:
        return "boqq"

def get_gender(x):
    return x['faceAttributes']['gender']