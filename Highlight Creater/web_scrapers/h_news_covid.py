import requests
from bs4 import BeautifulSoup
import re as remov
import random

def include_stop_word(title,stop_words):
  for word in stop_words:
    if (word.lower() in title):
      return True
  return False
    


def get_news(titles_used,stop_words,debugging=False):
  try:
      tokens = {'result_not_found':"[SPECIALTOKEN][NO MATCHING TITLE]",
                'search_not_found':"[SPECIALTOKEN][NO RESULTS FOUND][SEARCH ERROR]",
                'article_not_found':"[SPECIALTOKEN][ARTICLE NOT FOUND][ARTICLE READ ERROR]",
                'unexpected_error':"[SPECIALTOKEN][UNEXPECTED ERROR][INFO IN DOC]",
                'article_found':"[SPECIALTOKEN][ARTICLE FOUND]"}

      address_1 = "https://www.medicalnewstoday.com/categories/covid-19"
      page_1 = requests.get(address_1)
      soup_1 = BeautifulSoup(page_1.content,'html.parser')
      results_1 = soup_1.find('ol',{'class':'css-1iruc8t'})
      results_1 = results_1.find_all('a')
      select = []
      for ii,result in enumerate(results_1):
          if (result.text != '') and (result.text != 'READ MORE'):
              select.append(ii)

      results_1 = [results_1[index] for index in select]
      results_1 = [results_1[index] for index in range(len(results_1)) if (index+1)%2]

      #Getting all the links
      links=[]
      for result in results_1:
        temp = "https://www.medicalnewstoday.com"+result['href']
        links.append(temp)
      #Getting all the titles
      titles=[]
      for result in results_1:
          temp = result.text
          # temp = remov.sub(r'[0-9]+','',temp)
          titles.append(temp)

      filtered_titles= []
      filtered_links = []

      for i,title in enumerate(titles):
            if not (title.lower() in titles_used):
                if not (include_stop_word(title,stop_words)):
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
      temp = list(range(len(filtered_titles)))
      perm = random.sample(temp, len(filtered_titles))
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


      '''Fetching the Article'''
      ii=index
      address_2 = links[ii]
      page_2 = requests.get(address_2)
      soup_2 = BeautifulSoup(page_2.content,'html.parser')

      #Logic for searching different ID's and Classes in the article
      results_2 = soup_2.find('div',{'class':'css-z468a2'})

      #If there is  no content in the article
      # if results_2 == None:  
      #     return tokens['article_not_found'],None,titles[index]

      #Selecting the filtered Anchor Tags
      results_2 = results_2.find_all(['p','h1','h2','h3','h4','h5'])[2:]

      doc=''
      for result in results_2:
          doc += result.text + "\n"

      #Return the article
      return tokens['article_found'],doc,titles[index]
          
  except (Exception,NameError,KeyError) as e:
    return tokens['unexpected_error'],e,None
