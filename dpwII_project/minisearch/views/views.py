from django.shortcuts import render
from minisearch.models import BookTFIDF
from .search_call import sql_search
from .result import sql_result
from .forms import SearchForm
# from .forms import SearchForm
# import re
# import difflib
# from PyDictionary import PyDictionary
# import time
# from multiprocessing.pool import ThreadPool
# from functools import partial
# import linecache
# from nltk.corpus import wordnet

# amount = 0  # count the number of books
# # f = open("C:/Users/94883/Desktop/WS/ws2_django_demo/static/big_index_dictionary_tfidf.txt", 'r+')
# f = open("/root/MyPyspark/Gutenberg/Django/dpwII_project/UIC_workshopII-Search-Enginie-Demo/ws2_django_demo/static/big_index_dictionary_tfidf_2.txt", 'r+')
# dic = eval(f.read()) #global index dictionary
# f.close()
# set_of_word = set(re.findall(r'\w+',open('/root/MyPyspark/Gutenberg/Django/dpwII_project/UIC_workshopII-Search-Enginie-Demo/ws2_django_demo/static/big_index_dictionary_tfidf_2.txt').read().lower())) #a text with lots of word

# def search_index(request):
#     results=[]
#     search_term=""
#     context={'results':{},'count':0,'search_term':'empty'}
#     if request.GET.get('keyword'):
#         search_term=request.GET['keyword']
#         results=search(query=search_term,topN=20)
#         print(results)
#         context={'results':results[1],'count':results[0],'search_term':search_term}
#     return render(request,'minisearch/index.html',context)
# # Create your views here.

def index(request):
    # here used to get keyword and do operation.
    # initialize variables of getting information.
    # results=[]
    # search_term=""
    # define the form of render.
    context={'results':{},'count':0,'search_term':'empty'}
    # get keyword of searching.
    if request.method == "POST":
        # request.GET.get('keyword')
        # search_term=request.GET['keyword']
        # print(search_term)
        # # call function in the search_call.py at current path.
        # results=sql_search(query=search_term, topN=20)
        # print(results)
        # context={'results':results[1],'count':results[0],'search_term':search_term}
        
        # just submit the result to the result url.
        return sql_result(request)
    else:
        #If it is get, just stay
        # form = SearchForm()
        # context['form'] = form
        return render(request, 'minisearch/header.html', context)

# def result(request):
#     start_time = time.time()#time counter
#     context = dict()
#     if request.method == "POST":
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             post_data = form.cleaned_data['search']
#             post_data,second_post_data,third_post_data = spell_correction(post_data)
#             post_data = post_data.strip()
#             context['postdata'] = post_data
#     else :#GET
#         context['content'] = ""
#         form = SearchForm()
#         context['form'] = form
#         return render(request, 'result.html', context)
        
#     context['form'] = form
#     context['title1'] = "English Explantion"
#     context['explanation'] = get_meaning(post_data)#get the english meaning
#     context['title2'] = "Synonyms"
#     context['synonyms']= get_synonyms(post_data)#get chinese translation
#     namelist = return_result(post_data)
#     a = [i for i in range(amount)]#build a list of amount
#     partial_func = partial(fill_context, context=context, namelist=namelist, post_data=post_data)
#     pool = ThreadPool(processes=20)
#     pool.map(partial_func, a)
#     pool.close()
#     pool.join()
#     context['final'] = ""#final result of the html page
#     count = 1
#     for i in range(amount):
#         if(context['line'+str(i+1)]!="Wrong" and context['line'+str(i+1)]!=""):
#             total = "<a href=http://127.0.0.1:8000/static/"+context['result'+str(i+1)]+">"
#             context['final'] += total
#             context['final'] += "<h5>"
#             context['final'] += str(count)
#             context['final'] += "."
#             context['final'] += context['result'+str(i+1)]
#             context['final'] += "</h5></a><h6>"
#             context['final'] += context['line'+str(i+1)]
#             context['final'] +="</h6>"
#             context['final'] += '<br>'
#             count += 1
#         else:
#             continue
#     if (second_post_data == None and third_post_data == None):#the input is correct
#         if(count >1):#we have result
#             context['content'] = "ALL of the results we found of " + "<strong><i><u>" + post_data + ":" + "</strong></i></u>"
#         else:#we do not have result
#             context['content'] = "Sorry,there is no such file that matches your word"
#     else:#the input is wrong
#         context['content'] = "<p>"
#         context['content'] += "The word input has no matched files." + "Here are all of results we found of " + "<strong><i><u>" + post_data + "." + "</strong></i></u>"
#         context['suggestion'] = " Candidate Words: " + "<strong><i><u>" + second_post_data + "</strong></i></u>" + " and " + " <strong><i><u>" + third_post_data + ".</strong></i></u>"
#         context['suggestion'] +="</p>"
#     end_time = time.time()
#     context['time'] = str(round(end_time-start_time,2))
#     context['amount'] = count-1
#     return render(request, 'result.html', context)

# def spell_correction(post_data):#a function to correct the wrong spelling
#     post_data = post_data.lower()
#     correction = ""
#     second_correction = ""
#     third_correction = ""
#     if(post_data in set_of_word):
#         correction += post_data
#         correction += " "
#         return correction,None,None
#     else:
#         highest = 0
#         for i in set_of_word:
#             if(highest>0.9):#to high ratio
#                 break
#             ratio = difflib.SequenceMatcher(None,post_data, i).quick_ratio()
#             if(ratio>highest):
#                 highest = ratio
#                 third_correction = second_correction
#                 second_correction = correction
#                 correction = i
#     return correction,second_correction,third_correction

# def get_meaning(post_data):#get the english meanings
#     if(len(post_data.split())>1):
#         return "Sorry, A phrase is not supported to get the English explanation for now"
#     dictionary = PyDictionary()
#     dict = dictionary.meaning(post_data)
#     try:
#         length = len(dict[list(dict.keys())[0]])
#     except:
#         return "The word you input has no explanation in the dictionary"
#     value = list(dict.values())[0]
#     string = ""
#     for i in range(length):
#         string += str(i+1)
#         string += ". "
#         string += value[i]
#         string += "<br>"
#     return string

# def get_synonyms(post_data):#get the chinese translation
#     synonyms = []
#     try:
#         for syn in wordnet.synsets(post_data):
#             for l in syn.lemmas():
#                 synonyms.append(l.name())
#     except:
#         return "The word you input has no synonyms in the dictionary"
#     if(len(synonyms)==0):
#         return "The word you input has no synonyms in the dictionary"
#     str1 = ""
#     count = 1
#     synonyms = list(set(synonyms))
#     for i in synonyms:
#         str1 += (str(count)+"."+i+"<br>")
#         count += 1
#     return str1

# def return_result(post_data):#get the list of all file names
#     global amount
#     amount = len(dic[post_data])
#     return dic[post_data]

# #!!!!!change!!
# #fatch files from hdfs
# def read_and_load(file_name,post_data,row):#get the line contents
#     path = "C:/Users/94883/Desktop/WS/ws2_django_demo/static/"+file_name
#     try:
#         # f = open(path, 'r',encoding='gb18030',errors='ignore')
#         line = linecache.getline(path, int(row))
#     except:
#         return "Wrong"
#     # lines = f.readlines()
#     row = int(row)-1#true row number
#     str1 = ""
#     list1 = re.sub('[^a-zA-Z\d\s]+', '', line).split()
#     try:
#         index = list1.index(post_data)
#     except:
#         return "Wrong"
#     str1 += str(row)
#     if (row < 1000):
#         str1 += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
#     elif(row<10000):
#         str1 += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
#     else:
#         str1 += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
#     list1.insert(index,"<span class='badge badge-pill badge-danger'>")
#     list1.insert(index+2,"</span>")
#     for l in list1:
#         str1 += l
#         str1 +=" "
#     str1 += "<br>"
#     return str1

# def fill_context(i,context,namelist,post_data):#fill the context content
#     name1 = 'result' + str(i + 1)
#     namelist_new = namelist[i].split()
#     context[name1] = namelist_new[0]  # get the file name
#     row = namelist_new[1]
#     name2 = 'line' + str(i + 1)
#     context[name2] = read_and_load(context[name1], post_data,row)  # get the line where the post word lies in