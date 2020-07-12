import requests
from bs4 import BeautifulSoup
import re as remov
import random

def include_stop_word(title,stop_words):
  for word in stop_words:
    if (word.lower() in title):
      return True
  return False
    

def e_nutrition(specific_topic,titles_used,stop_words,not_news=True,debugging=False):
      ''' 
          Parameters:
          org_specific: Word to search
          titles_used: List of already used titles

          return format: token,doc,title
          token:specific token
          doc:article or blog
          title:title of the doc'''


      try:
          tokens = {'result_not_found':"[SPECIALTOKEN][NO MATCHING TITLE]",
          'search_not_found':"[SPECIALTOKEN][NO RESULTS FOUND][SEARCH ERROR]",
          'article_not_found':"[SPECIALTOKEN][ARTICLE NOT FOUND][ARTICLE READ ERROR]",
          'unexpected_error':"[SPECIALTOKEN][UNEXPECTED ERROR][INFO IN DOC]",
          'article_found':"[SPECIALTOKEN][ARTICLE FOUND]"}

          stop_words += ['april fools','celebrating']

          find_in = [{'type':"div",'class':"spi-2-all-supplements spi-2-section",'desc':'For getting all the article links'},
                     {'type':'div','class':"spi-2-popular spi-2-section",'desc':'For getting links from top articles'},
                     {'type':'div','class':"spi-2-class-of-supplements spi-2-section",'desc':'For getting links from recent articles'},
                     {'type':"div",'class':"article-module-content",'desc':'For reading the article'}
                     ]
          
          #Preprocessing
          #Reading all the curated topics
          if not_news:
                  topic = specific_topic
                  if (debugging==True):
                    print("Topic:-")
                    print(topic)
                  #Getting all the search Results
                  address_1 = "https://examine.com/nutrition/"
                  page_1 = requests.get(address_1)
                  soup_1 = BeautifulSoup(page_1.content,'html.parser')
                  results_1 = soup_1.find(find_in[0]['type'], {"class": find_in[0]['class']})
                  results_1 = results_1.find_all('a')
          else:
                  address_1 = "https://examine.com/nutrition/"
                  page_1 = requests.get(address_1)
                  soup_1 = BeautifulSoup(page_1.content,'html.parser')

                  #Getting all the links from recent articles and top articles
                  results_1 = soup_1.find(find_in[1]['type'], {"class": find_in[1]['class']})
                  results_1 = results_1.find_all('a')
                

                  results_1_2 = soup_1.find(find_in[2]['type'], {"class": find_in[2]['class']})
                  results_1_2 = results_1_2.find_all('a')

                  results_1 = results_1+results_1_2
          
          #Getting all the links
          links=[]
          for result in results_1:
            temp = "https://examine.com"+result['href']
            links.append(temp)
          #Getting all the titles
          titles=[]
          for result in results_1:
              temp = result.text
              temp = remov.sub(r'[0-9]+','',temp)
              titles.append(temp)

          #Randomly Shuffling all the titles and links
          temp = list(range(len(titles)))
          perm = random.sample(temp, len(titles))
          titles = [titles[index] for index in perm]
          links  = [links[index] for index in perm]
          if(debugging==True):
            print("Filtered")
            print(titles[:5])
            print(links[:5])

          #Filtering all the titles and selecting the required title
          filtered_titles= []
          filtered_links = []
          if not_news:
              for i,title in enumerate(titles):
                if topic in title.lower() and not (title.lower() in titles_used):
                    if not (include_stop_word(title,stop_words)):
                        filtered_titles.append(title)
                        filtered_links.append(links[i])
                        break;
          else:
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

          #Reassigning Titles and links
          titles = filtered_titles
          links = filtered_links
          #Randomly Shuffling
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
          results_2 = soup_2.find(find_in[3]['type'], {"class":find_in[3]['class']})

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