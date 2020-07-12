import requests
from bs4 import BeautifulSoup
import re as remov
import random

def include_stop_word(title,stop_words):
  for word in stop_words:
    if (word.lower() in title):
      return True
  return False
    

def mbg_health(specific_topic,titles_used,stop_words,search=False,debugging=False):



      try:
          tokens = {'result_not_found':"[SPECIALTOKEN][NO MATCHING TITLE]",
          'search_not_found':"[SPECIALTOKEN][NO RESULTS FOUND][SEARCH ERROR]",
          'article_not_found':"[SPECIALTOKEN][ARTICLE NOT FOUND][ARTICLE READ ERROR]",
          'unexpected_error':"[SPECIALTOKEN][UNEXPECTED ERROR][INFO IN DOC]",
          'article_found':"[SPECIALTOKEN][ARTICLE FOUND]"}

          find_in = [{'type':'section','class':'search-results'},
                      {'type':'div','class':'main-content__article-body'}]
          
          #Preprocessing
          #Reading all the curated topics
          topic = specific_topic
          if not search:
                  address_1 = "https://www.mindbodygreen.com/"+topic
                  page_1 = requests.get(address_1)
                  soup_1 = BeautifulSoup(page_1.content,'html.parser')
                  results_1 = soup_1.find('div',{'class':"category__featured-cards"})
                  results_1=results_1.find_all('a')
                  select=[]
                  for i in range(len(results_1)):
                    temp = results_1[i]['href']
                    if ("articles" in temp):
                      select.append(i)
                  results_1 = [results_1[index] for index in select]
                  results_1 = [results_1[index] for index in range(len(results_1)) if (index+1)%2==0]



                  results_1_2 = soup_1.find('div',{'class':"latest-cards"})
                  results_1_2 = results_1_2.find_all('a')
                  select=[]
                  for i in range(len(results_1_2)):
                    temp = results_1_2[i]['href']
                    if ("articles" in temp):
                      select.append(i)
                  results_1_2 = [results_1_2[index] for index in select]
                  results_1_2 = results_1_2[:17] + results_1_2[21:]
                  results_1_2 = [results_1_2[index] for index in range(len(results_1_2)) if results_1_2[index].text!='' ]

                  results_1 += results_1_2
          else:
                  #Searching the required Topic
                  specific = specific_topic.split(" ")
                  specific = "+".join(specific)
                  address_1 = "https://www.mindbodygreen.com/search?q={}".format(specific)
                  page_1 = requests.get(address_1)
                  soup_1 = BeautifulSoup(page_1.content,'html.parser')
                  results_1 = soup_1.find(find_in[0]['type'],{'class':find_in[0]['class']})
                  #Preprocessing to extract links
                  results_1 = results_1.find_all('a')
                  select=[]
                  for i in range(len(results_1)):
                    temp = results_1[i]['href']
                    if ("articles" in temp):
                      select.append(i)

                  #Selecting the filtered Anchor Tags
                  results_1 = [results_1[index] for index in select] 

          
          #Getting all the links
          links=[]
          for result in results_1:
            temp = "https://www.mindbodygreen.com"+result['href']
            links.append(temp)
          #Getting all the titles
          titles=[]
          for result in results_1:
              temp = result.text
              temp = remov.sub(r'[0-9]+','',temp)
              titles.append(temp)

          #Filtering all the titles and selecting the required title
          filtered_titles= []
          filtered_links = []
          if search:
              for i,title in enumerate(titles):
                if topic in title.lower() and not (title.lower() in titles_used):
                    if not (include_stop_word(title,stop_words)):
                        filtered_titles.append(title)
                        filtered_links.append(links[i])
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
          results_2 = soup_2.find(find_in[1]['type'],{'class':find_in[1]['class']})
          #If there is  no content in the article
          if results_2 == None:  
              return tokens['article_not_found'],None,titles[index]

          #Selecting the filtered Anchor Tags
          results_2 = results_2.find_all(['p','h1','h2','h3','h4','h5'])[2:]

          doc=''
          for result in results_2:
            doc += result.text + "\n"

          #Return the article
          return tokens['article_found'],doc,titles[index]
          
      except (Exception,NameError,KeyError) as e:
        return tokens['unexpected_error'],e,None