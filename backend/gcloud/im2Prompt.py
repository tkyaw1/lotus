from captionbot import CaptionBot
import nltk
import random
import importlib
import sys
import urllib
import ast

import gCloudStorage
import im2metadata
import gVision
import questions

class QuestionGeneration(object):
    def __init__(self):
        pass

    def askGeneralQ(self):
        return random.choice(["What is something that bugged you today?",
        "What is something you should work on?",
        "What was your favorite thing about today?",
        "Who did you talk to today and about what?",
        "What were you grateful for today?",
        "Did you notice anything different today?",
        "What did you accomplish today?"])

    def askLocationQ(self, location):
        return random.choice(["What did you do in %s?" %location,
        "Why did you go to %s?" %location,
        "What did eat do in %s?" %location,
        "Who did you meet in %s?" %location,
        "First time in %s?" %location,
        "Have you ever been to %s?" %location])

    def askActivityQ(self, activity):
        return random.choice(["How did %s go?" %activity,
        "Can you tell me more about %s?" %activity,
        "Was %s fun?" %activity])

    def askFoodQ(self, food):
        return random.choice(["How was your meal?",
        "Have a good meal?"])

    def askPeopleQ(self):
        return random.choice(["With friends?",
        "Who were you with?"])

# order of things to be printed
# timestamp - 11:30pm as string
# caption
# image_url
# image_prompt

# {'type': 'timestamp', 'data': timestamp},
# {'type': 'caption', 'data': caption},
# {'type': 'image', 'data': image},
# {'type': 'emoji', 'data': emoji},
# {'type': 'imagePrompt', 'data': imagePrompt},
def main():
    # load data from front end
    # photo_url = sys.argv[1]
    photo_url = "https://storage.googleapis.com/project-tao/kastanByLake.jpg"
    # keyword_dict_str = sys.argv[2]
    # keyword_dict = ast.literal_eval(keyword_dict_str)
    keyword_dict = {"surfing":{"date":["Aug-15-2018","Sep-16-2018"],"pos":"VBG","location":["Malibu","Hawaii"],"type":"activity","comp":[["Aug-15-2018","Malibu"],["Sep-16-2018","Hawaii"]]},"running":{"date":["Aug-02-2018"],"pos":"VBG","location":["Swarthmore"],"type":"activity","comp":[["Aug-02-2018","Swarthmore"]]},"Malibu":{"date":["Aug-15-2018"],"pos":"NN","location":["Malibu"],"type":"location","comp":[["Aug-15-2018","Malibu"]]},"Swarthmore":{"date":["Aug-02-2018"],"pos":"NN","location":["Swarthmore"],"type":"location","comp":[["Aug-02-2018","Swarthmore"]]},"Hawaii":{"date":["Sep-16-2018"],"pos":"NN","location":["Hawaii"],"type":"location","comp":[["Sep-16-2018","Hawaii"]]}}
    # print "YAYYY", type(keyword_dict)

    photo_name = str(random.randint(0, 99999999)) + ".jpg"
    loc_photo_path = "./fromFrontEnd/" + photo_name
    urllib.urlretrieve(photo_url, loc_photo_path )

    gcloud_base_url = 'https://storage.googleapis.com/project-tao/'
    photo_gcloud_url = gcloud_base_url + photo_name

    # upload to gCloudStorage
    bucket_name = 'project-tao'
    gCloudStorage.upload_blob(bucket_name, loc_photo_path, photo_name)

    # localPhotoPath = '../resources/kastanByLake.jpg'
    date_str, date_nl, time_nl, time_12hr_str, address_nl = im2metadata.im2date_time_addr(loc_photo_path)

    capt = captionImage(photo_gcloud_url)

    print("{'type': 'timestamp', 'data':" + time_12hr_str + "}, ")
    print("{'type': 'image', 'data':" + photo_gcloud_url + "}, ")

    labels_list = gVision.gcloudLabels(loc_photo_path)
    group_bool = gVision.gcloudFaces(loc_photo_path)
    capt = captionImage(photo_gcloud_url)

    tagged = tokenizeAndTag(capt)
    populateDict(tagged, keyword_dict, address_nl, date_nl, group_bool)


    for word in tagged:
        keyword = word[0]
        pos = word[1]
        if pos == 'VBG':
            capt = keyword + " " + address_nl + " " + time_nl

    print("{'type': 'caption', 'data':" + capt + "}, ")

def captionImage(url):
    image_url = url
    cBot = CaptionBot()
    caption = cBot.url_caption(image_url)
    caption = caption.split(" ")[2:]
    caption = " ".join(caption)
    return caption

# types of blocks:
# timestamp, caption, image, imagePrompt (fitbit, location)

def tokenizeAndTag(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    print("tagged", tagged)
    return tagged

def populateDict(tagged, keywords, location, date, blockType):
    activity = None
    for word in tagged:
        keyword = word[0]
        pos = word[1]
        if pos == 'VBG' or pos == 'VB':
            activity = True
        locationAndDate=None
        if location != None and date != None:
            locationAndDate = [date, location]
        if keyword not in keywords:
            keywords[keyword] = {"location": [location],
                                "pos": pos,
                                "date": [date],
                                "type": blockType,
                                "comp": locationAndDate
                                }
        else:
            keywords[keyword]["location"].append(location)
            keywords[keyword]["date"].append(date)

    group = None
    food = None
    if type == "Group":
        group = True
    elif type == "Activity":
        activity = True
    elif type == "Food":
        food = True
    imagePrompt = askQs(location, activity, food, group)
    print("{'type': 'imagePrompt', 'data': %s}" %imagePrompt)
    sys.stdout.flush()

def askQs(location=None, activity=None, food=None, group=None):
    qG = questions.QuestionGeneration()
    if location:
        return qG.askLocationQ(location)
    elif group:
        return qG.askPeopleQ()
    elif activity:
        return qG.askActivityQ(activity)
    elif food:
        return qG.askFoodQ(food)
    else:
        return qG.askGeneralQ()

main()
