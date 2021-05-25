import random

#data store for possible responses to common talking points
def greeting():
    greet = ["Hello", "Hi", "How are you", "What's up", "Here to help", "How can I help"]
    num = random.randint(0,4)
    print(greet[num])

def joke():
    jokes = ["Why did the chicken cross the road... to get to the other side","Whats 2 + 2 ... Fish","What’s the best thing about Switzerland?...I don’t know, but the flag is a big plus","Did you hear about the mathematician who’s afraid of negative numbers?... He’ll stop at nothing to avoid them.",
             "Why do we tell actors to “break a leg?”... Because every play has a cast."]
    num = random.randint(0, 4)
    print(jokes[num])