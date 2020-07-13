from web_scrapers import h_news as hn
from web_scrapers import h_harward as d
from web_scrapers import e_nutrition as e
from web_scrapers import mbg_health as m
from web_scrapers import h_news_covid as covid

import random

def get_value(dicti,_key):
  for key,value in dicti.items():
    if _key in key:
      return value
  return None 


def select_website(query,titles_used,stop_words,nutrition_topics,debugging=False):

  tokens = [{'result_not_found':"[SPECIALTOKEN][NO MATCHING TITLE]",
          'search_not_found':"[SPECIALTOKEN][NO RESULTS FOUND][SEARCH ERROR]",
          'article_not_found':"[SPECIALTOKEN][ARTICLE NOT FOUND][ARTICLE READ ERROR]",
          'unexpected_error':"[SPECIALTOKEN][UNEXPECTED ERROR][INFO IN DOC]",
          'article_found':"[SPECIALTOKEN][ARTICLE FOUND]"}]

  select_site = {('mental-health','womens-health','food','fitness','skin-care','parenting'):'mbg',
                       ('nutritions', 'diet' , 'supplements'):'e_nutrition',
                       ('health-news'):'h_news',
                       ('covid-19'):'h_news_covid'}

  mbg_topics = {"mental-health":["meditation",'spirituality','personal-growth','social-good'],
                'womens-health':['womens-health'],
                'food':['recipes','food-trends'],
                'fitness':['healthy-weight','motivation','routines','outdoors','recovery'],
                'skin-care': ['beauty'],
                'parenting':['parenting'],
                'child-health':['parenting']}
  
  if (query['INTEREST'] != None):
      site = get_value(select_site,query['INTEREST'])
      if (debugging==True):
        print("Site Selcted: "+str(site))

      if (site==None):
        return "[SPECIALTOKEN][INVALID_INTEREST]",query['INTEREST']+": Not Found",None

      if (site == 'mbg'):
        topics = mbg_topics[query['INTEREST']]
        id = random.randint(0,len(topics)-1)
        if (debugging==True):
            print("Topic Selcted: "+str(topics[id]))

        token,doc,title = m.mbg_health(topics[id],titles_used,stop_words,False,True)
        return token,doc,title

      elif (site == 'e_nutrition'):
        topic = nutrition_topics[random.randint(0,len(nutrition_topics)-1)]
        if (debugging==True):
            print("Topic Selcted: "+str(topic))
        token,doc,title = e.e_nutrition(topic,titles_used,stop_words,True,True)
        return token,doc,title

      elif (site == 'h_news'):
        choice = ['h_news','h_news','h_news','e_nutrition'] #To give more weightage to h_news
        id = random.randint(0,3)
        site = choice[id]
        if (debugging==True):
          print("Site Selected: "+site)
        if (site == 'h_news'):
          token,doc,title = hn.get_news(titles_used,stop_words,True)
        else:
          token,doc,title = e.e_nutrition('',titles_used,stop_words,False,True)
        return token,doc,title
      elif (site== 'h_news_covid'):
        token,doc,title = covid.get_news(titles_used,stop_words,True)
        return token,doc,title
        
  elif (query["DISEASE_GENERAL_SEARCH"] != None):
    # Search Article in mbg
    # If article not found then
    # Search Article in harward_health
    topic = query["DISEASE_GENERAL_SEARCH"]
    choice = ['a','a','b'] #To give more weightage to h_news
    id = random.randint(0,2)
    site = choice[id]
    if (debugging==True):
          print("Site Selected: a--> mbg, b--> harward "+ site)
    if (site=='a'):
        token,doc,title = m.mbg_health(topic,titles_used,stop_words,True,True)
        if token != "[SPECIALTOKEN][ARTICLE FOUND]":
          token,doc,title = d.health_harward(topic,titles_used,debugging=True)
    else:
      token,doc,title = d.health_harward(topic,titles_used,debugging=True)
      if token != "[SPECIALTOKEN][ARTICLE FOUND]":
          token,doc,title = m.mbg_health(topic,titles_used,stop_words,True,True)

    return token,doc,title  
