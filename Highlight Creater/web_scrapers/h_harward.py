import requests
from bs4 import BeautifulSoup
import re as remov
import random

def include_stop_word(title,stop_words):
  for word in stop_words:
    if (word.lower() in title):
      return True
  return False

def health_harward(org_specific,titles_used,debugging=False):
      ''' docs:-
          It takes in a word that has to be searched and then return the
          related article.

          It also ensures the article returned is unique by comparing already 
          used titles.

          It also apply a few techniques to filter irrelevant articles.
      '''
      ''' 
          Parameters:
          org_specific: Word to search
          titles_used: List of already used titles

          return format: token,doc,title
          token:specific token
          doc:article or blog
          title:title of the doc'''

      try:
          find_in = [{'type':"div",'class':"e-content entry-content"},{'type':"section",'class':"entry-content"}]

          tokens = {'result_not_found':"[SPECIALTOKEN][NO MATCHING TITLE]",
          'search_not_found':"[SPECIALTOKEN][NO RESULTS FOUND][SEARCH ERROR]",
          'article_not_found':"[SPECIALTOKEN][ARTICLE NOT FOUND][ARTICLE READ ERROR]",
          'unexpected_error':"[SPECIALTOKEN][UNEXPECTED ERROR][INFO IN DOC]",
          'article_found':"[SPECIALTOKEN][ARTICLE FOUND]"}

          #Getting all the search Results
          specific = org_specific.split(" ")
          specific = "+".join(specific)
          address_1 = "https://www.health.harvard.edu/search?q={}".format(specific)
          page_1 = requests.get(address_1)
          soup_1 = BeautifulSoup(page_1.content,'html.parser')
          results_1 = soup_1.find("div", {"class": "search-results-container"})

          #If no search results are found
          if results_1 == None:
            return tokens['search_not_found'],None,None

          #Get all the search results
          results_1 = results_1.find_all('a')

          #Getting all the links
          links=[]
          for result in results_1:
            temp = result['href']
            links.append(temp)

          #Getting all the titles
          titles=[]
          for result in results_1:
              temp = result.text
              temp = remov.sub(r'[0-9]+','',temp)
              titles.append(temp)
          '''Logic for selecting unique Article will go Here'''   
          #Filtering all the titles
          filtered_titles= []
          filtered_links = []
          for i,title in enumerate(titles):
            if org_specific.lower() in title.lower() :
              if not ('questions' in title.lower()) and not (title.lower() in titles_used):
                filtered_titles.append(title)
                filtered_links.append(links[i])

          if (debugging==True):
            print("Filtered Titles")
            print(filtered_titles)
            print("\n\n")
          #If no matching title is found
          if len(filtered_titles) == 0:
              return tokens['result_not_found'],None,None

          #Randomly Shuffling
          index = None
          if (len(filtered_titles)<=3):
              temp = list(range(len(filtered_titles)))
              perm = random.sample(temp, len(filtered_titles))
              titles = [filtered_titles[index] for index in perm]
              links  = [filtered_links[index] for index in perm]
              if (debugging==True):
                print("Randomly Shuffling")
                print(titles)
                print(links)

          else:
              temp = list(range(len(filtered_titles)))
              perm_1 = random.sample(temp[:3], 3)
              perm_2 = random.sample(temp[3:], len(filtered_titles)-3)
              perm = perm_1+perm_2
              titles = [filtered_titles[index] for index in perm]
              links  = [filtered_links[index] for index in perm]
              if (debugging==True):
                print("Randomly Shuffling")
                print(titles)
                print(links)

          index = 0
          #Loading the article with the selected title
          if debugging==True:
            print("Selected Article: ")
            print(titles[index])
          ii=index
          address_2 = links[ii]
          page_2 = requests.get(address_2)
          soup_2 = BeautifulSoup(page_2.content,'html.parser')

          #Logic for searching different ID's and Classes in the article
          ii = 0
          results_2 = soup_2.find(find_in[ii]['type'], {"class":find_in[ii]['class']})
          ii += 1
          while (results_2 == None and ii<len(find_in)):
            results_2 = soup_2.find(find_in[ii]['type'], {"class":find_in[ii]['class']})
            ii += 1

          #If there is  no content in the article
          if results_2 == None:  
              return tokens['article_not_found'],None,titles[index]
    
          #else
          doc = results_2.text
          #Remove the disclaimer
          if ("Disclaimer:" in doc) or ("disclaimer:" in doc):
              doc = doc[:doc.index("Disclaimer:")]
          #Return the article
          return tokens['article_found'],doc,titles[index]

      except (Exception,NameError,KeyError) as e:
        return tokens['unexpected_error'],e,None