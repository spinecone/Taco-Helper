#!/usr/bin/env python
# encoding: utf-8

import requests
import tweepy
import secrets
import random

counts = [
    'Double',
    'Triple',
    'Quadruple',
]
adjectives = [
    'Beefy',
    'Cheesy',
    'Spicy',
    'Fiery',
    'Crunchy',
    'Crispy',
    'Loaded',
    'Grilled',
    'Smothered',
    'Stuft',
    'Cantina',
]
fillers = [
    'Potato',
    'Nacho Cheese',
    'Bean',
    'Black Bean',
    'Rice',
    'Ground Beef',
    'Shredded Chicken',
    'Chicken',
    'Steak',
    'Fajitas',
    u'Fritos®',
    u'Doritos® Locos',
    u'Fiery Doritos® Locos',
    u'Cool Ranch® Doritos® Locos',
    u'Nacho Cheese Doritos® Locos',
]
meal_modifiers = [
    'Fiesta',
    'Fresco',
    'Fresco Grilled',
    'Lava',
]
meals = [
    'Taco',
    'Soft Taco',
    u'Double Decker® Taco',
    'Taco Salad',
    'Burrito',
    'Gordita',
    'Chalupa',
    'Triplelupa', # https://www.tacobell.com/food/specialties/triplelupa
    'Crunchwrap',
    'Quesadilla',
    'Griller',
    'Mexican Pizza',
    'Quesarito',
    'Crunchwrap Slider',
    'Tostada',
    u'Meximelt®',
    'XXL Grilled Stuft Burrito',
    'Smothered Burrito',
    'Combo Burrito',
    '5-Layer Burrito',
    '7-Layer Burrito',
    'Nachos',
    u'Nachos Bellgrande®',
    u'Doritos® Locos Taco',
    u'Doritos® Locos Gordita',
    u'Doritos® Locos Chalupa',
    u'Doritos® Locos Nachos',
    'Waffle Taco',
    'Enchirito',
    'Roll-Up',
    'Power Bowl',
]
modifiers = [
    'Crunch',
    u'Supreme®',
    'Party Pack',
]

meats = [
    'Nacho Cheese',
    'Quesarito',
    'Quesadilla',
    'Griller',
    'Mexican Pizza',
    'Beef'
    'Beefy'
    'Ground Beef',
    'Shredded Chicken',
    'Chicken',
    'Steak',
    'Fajitas',
]

def get_next_phrase(phrases, skips=None, randomness=0.5, vegan=False):
    trues = int(randomness * 100)
    falses = int(100 - trues)
    chance = [True] * trues + [False] * falses
    if not random.choice(chance):
        return []
    if not skips:
        skips = []
    for _ in range(len(phrases)):
        word = random.choice(phrases)
        skip = False
        for s in skips:
            if s in word:
                skip = True
            if vegan:
                if s in meats:
                    skip = True
        if not skip:
            break
    return [word]


def generate_taco_bell(vegan=False):
    food = get_next_phrase(counts, randomness=.1, vegan=vegan)
    food += get_next_phrase(adjectives, skips=food, randomness=.85, vegan=vegan)
    food += get_next_phrase(fillers, skips=food, randomness=.75, vegan=vegan)
    food += get_next_phrase(meal_modifiers, skips=food, randomness=.1, vegan=vegan)
    food += get_next_phrase(meals, skips=food, randomness=1.0, vegan=vegan)
    food += get_next_phrase(modifiers, skips=food, randomness=.25, vegan=vegan)

    return ' '.join(food)


def tacobellitem():
    drinks = ["Mtn Dew Baja Blast"]
    items = []
    for _ in range(random.randint(1, 3)):
        items.append(generate_taco_bell())
    if len(items) <= 2 and random.randint(1, 11) == 1:
        items.append(random.choice(drinks))
    if len(items) > 1:
        saying = ", a ".join(items[:-1]) + ", and a " + items[-1]
    else:
        saying = items[0]
    return u"You should get a {}.".format(saying)

def tweet(message):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True

  search_phrases = ["\"I'm so high\"", "\"so high rn\"", "\"high af\"", "\"so blazed\""]
  if random.randint(1, 5) == 1:
    phrase = random.choice(search_phrases)
    taco_recipient = api.search(q=phrase, rpp=1, count=1)[0]
    retweet_url = " https://twitter.com/" + taco_recipient.user.screen_name + "/status/" + str(taco_recipient.id)
    message += retweet_url

  print("Posting message {}".format(message))
  api.update_status(status=message)

tweet(tacobellitem())
