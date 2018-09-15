""" This is the class for blocks
"""

class Block:
    def __init__(self):
        self.photo = "" # url
        self.prompt = "" # is this a quesiton?
        self.text = "" # the text in a block
        self.timestamp = "" # the timestamp of the block
        self.emoji = "" # TODO: What are the text version of each emoji we want?
        self.caption = "" # generated from the image to text and then the ad lib nlp model
        self.type = "" # block types: photo, fitbit, location, etc.
        self.keywords = []

    def set_photo(self, photo):
        self.photo = photo

    def get_photo(self):
        return self.photo

    def set_keywords(self, keywords):
        self.keywords = keywords # Need to make this actual keyword extraction

    def get_keywords(self):
        return self.keywords

    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_prompt(self):
        return self.prompt


    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_timestamp(self):
        return self.timestamp

    def set_emoji(self, emoji):
        self.emoji = emoji

    def get_emoji(self):
        return self.emoji

    def set_caption(self, caption):
        self.caption = caption

    def get_caption(self):
        return self.caption

    def set_type(self, type):
        # type is photo, fitbit, location
        self.type = type

    def get_type(self):
        return self.type