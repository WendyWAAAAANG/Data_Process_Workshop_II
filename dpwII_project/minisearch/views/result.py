from django.shortcuts import render
from .search_call import sql_search
from .forms import SearchForm
from PyDictionary import PyDictionary
import time
from multiprocessing.pool import ThreadPool
from functools import partial
from nltk.corpus import wordnet
from pyhdfs import HdfsClient
from hdfs.client import Client
import os
import subprocess
import re
import difflib
import linecache

# define a class used to fetch files from hdfs.
class Process_Data_Hdfs():
    # initialize an object.
    def __init__(self, filename):
        self.client = Client('http://localhost:9870')
        self.filename = "/project_big/" + filename

    # download file from hdfs.
    def get_from_hdfs(self, local_path):
        self.client.download(self.filename, local_path, overwrite=False)
        return

    # return file under directory on hdfs.
    def list(self):
        return self.client.list(self.filename, status=False)
 
    # read the content of file in hdfs.
    # def read_hdfs_file(self, rownum):
    #     # with client.read('samples.csv', encoding='utf-8', delimiter='\n') as reader:
    #     #  for line in reader:
    #     # pass
    #     lines = []
    #     with self.client.read(self.filename, encoding='utf-8', delimiter='\n') as reader:
    #         counter = 0;
    #         for line in reader:
    #             # pass
    #             # print line.strip()
    #             if counter == rownum:
    #                 lines.append(line.strip())
    #                 break
    #             counter += 1
    #     print(lines)
    #     return str(lines)

# post_data <==> search_term
# namelist <==> filename (results)

# # used to read the file from hdfs.
# client = HdfsClient(hosts = '10.20.0.151:9870')
# res = client.open('/project_big/*.txt')
# text = res.read()
# line = str(text, encoding = 'utf8')
# print(line)

# amount = 0  # count the number of books
# f = open("C:/Users/94883/Desktop/WS/ws2_django_demo/static/big_index_dictionary_tfidf.txt", 'r+')
# read in the index from static files, but here we use MySQL to store index.
# f = open("/root/MyPyspark/Gutenberg/Django/dpwII_project/UIC_workshopII-Search-Enginie-Demo/ws2_django_demo/static/big_index_dictionary_tfidf_2.txt", 'r+')
# dic = eval(f.read()) #global index dictionary
# f.close()
# set_of_word = set(re.findall(r'\w+',open('/root/MyPyspark/Gutenberg/Django/dpwII_project/UIC_workshopII-Search-Enginie-Demo/ws2_django_demo/static/big_index_dictionary_tfidf_2.txt').read().lower())) #a text with lots of word

def sql_result(request):
    # spilt the result, and find the preview in hdfs.
    #time counter and variable initialization.
    start_time = time.time()
    results = []    # store the filename.
    search_term = ''    # store the term that user search.
    context = dict()    # used to render html.
    # read in the index and filename related to input.
    if request.method == "POST":
        search_term=request.POST['keyword']
        # call function in the search_call.py at current path.
        results=sql_search(query=search_term)
        results_list = list(results[1])
        context={'results':results_list,'count':results[0],'search_term':search_term}  
        # acquire filename, TFIDF, rowNum and preview of text.
        context['fileName'] = [list(results_list[i])[0] for i in range(results[0])]
        context['TFIDF'] = [list(results_list[i])[1] for i in range(results[0])]
        # context['rowNum'] = [list(results_list[i])[2] for i in range(results[0])]
        # get the english meaning.
        context['title1'] = "English Explantion"
        context['explanation'] = get_meaning(search_term)
        # get chinese translation.
        context['title2'] = "Synonyms"
        context['synonyms']= get_synonyms(search_term)

        # # do not know what it is??
        # a = [i for i in range(amount)]
        # partial_func = partial(fill_context, context=context, namelist=[i[1] for i in results], post_data=search_term)
        # pool = ThreadPool(processes=20)
        # pool.map(partial_func, a)
        # pool.close()
        # pool.join()

        # get final result of the html page
        context['final'] = ""
        count = 1
        fileName = list(context['fileName'])
        TFIDF = context['TFIDF']
        # rowNum = list(context['rowNum'])
        #infoList = zip(fileName, rowNum)
        for i in range(results[0]):
            # change!!! from hdfs.
            # get final results, with a special form.
            # we can preview 3 lines besides the article.
            context['final'] += "<table><th><tr>"
            content,bookName = get_finalRes(fileName[i])
            weblink = "<a href=http://localhost:8000/static/tfidf-index/"+fileName[i]+">"
            context['final'] += weblink
            context['final'] += "<h5>"
            context['final'] += str(count)
            context['final'] += ". "
            context['final'] += bookName
            context['final'] += "</h5></a></tr>"
            context['final'] += content
            context['final'] += "</h6></th></table>"
            context['final'] += '<br>'
            count+=1
            # testStr = get_finalRes(fileName[i], rowNum[i])
            # print(testStr)
            # if(testStr != "Wrong"):
            #     # change!!! from hdfs.
            #     # get final results, with a special form.
            #     # we can preview 3 lines besides the article.
            #     weblink = "<a href=http://127.0.0.1:8000/tfidf-index/"+fileName[i]+">"
            #     context['final'] += weblink
            #     context['final'] += "<h5>"
            #     context['final'] += str(count)
            #     context['final'] += ". "
            #     context['final'] += fileName[i]
            #     context['final'] += "</h5></a>"
            #     # context['final'] += testStr
            #     context['final'] += "<h6></h6>"
            #     context['final'] += '<br>'
            #     count+=1 
            # else:
            #     continue

        # request.GET.get('keyword')
        # results = request.GET['keyword']
        # results = sql_search(query = search_term, topN = 20)
        # print(results)
        # # context['results'] = results[1]
        # context['results'] = [i[1] for i in results]
        # filename = [i[1] for i in results]
        # context['count'] = len(results)
        # context['rownum'] = [i[3] for i in results]
        # rownum = [i[3] for i in results]
        # # context={'results':results[1],'count':results[0],'search_term':search_term}
        # # return related result.
        # # get the english meaning.
        # context['title1'] = "English Explantion"
        # context['explanation'] = get_meaning(search_term)
        # # get chinese translation.
        # context['title2'] = "Synonyms"
        # context['synonyms']= get_synonyms(search_term)
        # amount is declared at the beginning, global variable.

        # a = [i for i in range(amount)]
        # partial_func = partial(fill_context, context=context, namelist=[i[1] for i in results], post_data=search_term)
        # pool = ThreadPool(processes=20)
        # pool.map(partial_func, a)
        # pool.close()
        # pool.join()

        # #final result of the html page
        # context['final'] = ""
        # count = 1
        # amount = len[search_term]
        # infolist = zip(filename, rownum)
        # for i in infolist:
        #     if(get_finalRes(infolist[i][0], rownum[i][1]) != "Wrong"):
        #         # change!!! from hdfs.
        #         # get final results, with a special form.
        #         # we can preview 3 lines besides the article.
        #         weblink = "<a href=10.20.0.151:9870/project_big/"+infolist[i][0]+">"
        #         context['final'] += weblink
        #         context['final'] += "<h5>"
        #         context['final'] += str(count)
        #         context['final'] += "."
        #         context['final'] += infolist[i][0]
        #         context['final'] += "</h5></a><h6>"
        #         context['final'] += get_finalRes(filename[i][0], rownum[i][1])
        #         context['final'] +="</h6>"
        #         context['final'] += '<br>'
        #         count+=1 
        #     else:
        #         continue
        # use amount to store the num of true term in the result.
        # maybe the num of result < 20.
        context['amount'] = count - 1
        # end of time calculation, add time into context dictionary.
        end_time = time.time()
        context['time'] = str(round(end_time-start_time,2))
    return render(request, 'minisearch/result.html', context)

def get_finalRes(filename):
    bookName=''
    ### maybe need to change.
    # # used to read the file from hdfs.
    # client = HdfsClient(hosts = '10.20.0.151:9870')
    # filepath = "/project_big" + filename
    #output = subprocess.check_output("hdfs dfs -cat " + filename, shell = True)
    # res = client.open('/project_big/' + filename)
    # text = res.read()
    # lines = str(text, encoding = 'utf8')
    #path = "10.20.0.151:9870/project_big/" + filename
    # initialize a string to store the preview of text.
        # create an object to fetch file we need.
    fileFetcher = Process_Data_Hdfs(filename)
    content = ""
    local_path = "/root/MyPyspark/Gutenberg/Django/dpwII_project/static/tfidf-index/"
    if(os.path.exists(local_path + filename) == False):
        fileFetcher.get_from_hdfs(local_path)

    # after download the file, we open it to fetch info.
    with open(local_path + filename) as f:
            for lines in f.readlines():
                # get the title of book.
                if 'Title: ' in lines:
                    bookName=lines[7:]
                    # print(lines)
                    # content += '<tr><h6>'
                    # content += lines + '\n'
                    # content += '</h6></tr>'
                # get the author of book. 
                # content += '<br>'
                if 'Author: 'in lines:
                    print(lines)
                    content += '<tr><h6>'
                    content += lines 
                    content += '</h6></tr>'
                    break
                # if 'Release Date: ' in lines:
                #     book_image='<img src="https://www.gutenberg.org/cache/epub/{page_id}/pg{page_id}.cover.medium.jpg" >'.format(page_id=filename[:-4])
                #     content += '<th>'
                #     content += book_image
                #     content += '</th>'
                #     break
    return content,bookName
    #filePath = ""
    # try:
        # content = fileFetcher.read_hdfs_file(rownum)
        #fileFetcher.get_from_hdfs("/root/MyPyspark/Gutenberg/Django/dpwII_project/static/tfidf-index")
        #filePath = fileFetcher.list()
        # with client.read(filepath) as fs:
        #     content = fs.read()
        # f = open(path, 'r',encoding='gb18030',errors='ignore')
        # line_0 = linecache.getline(lines, rownum-1)
        # line_1 = linecache.getline(lines, rownum)[:20]
        # line_2 = linecache.getline(lines, rownum+1)
        # line0 = linecache.getline(path, rownum-1)
        # line1 = linecache.getline(path, rownum)
        # line2 = linecache.getline(path, rownum+1)
        # content = str(rownum-1) + line_0 + '\n' + str(rownum) + line_1 + '\n' + str(rownum+1) + line_2
        # content = str(rownum) + line_1
    # except:
    #     return "Wrong"
        #finalres = [(rownum-1, line0), (rownum, line1), (rownum+1, line2)]
    # return rownum
    
#get the english meanings of the keywords.
def get_meaning(post_data):
    # which means the input is a phrase,
    # simply show a warning.
    if(len(post_data.split())>1):
        return "Sorry, A phrase is not supported to get the English explanation for now!"
    # otherwise, create a pydictionary object.
    dictionary = PyDictionary()
    dict = dictionary.meaning(post_data)
    try:
        # try to get the lenth of the dictionary.
        length = len(dict[list(dict.keys())[0]])
    except:
        # which means there is no explanation in the pydictionary.
        return "The keyword you input has no explanation in the dictionary!"
    # if try successful, then get the meaning of keywords.
    value = list(dict.values())[0]
    string = ""
    count = 1
    for i in range(length):
        if count > 5:
            break
        # output all meanings of keywords.
        string += str(i+1)
        string += ". "
        string += value[i]
        # a new line.
        string += "<br>"
        count += 1
    return string

#get the synonyms of the keywords.
def get_synonyms(post_data):
    synonyms = []
    try:
        for syn in wordnet.synsets(post_data):
            for l in syn.lemmas():
                synonyms.append(l.name())
    except:
        return "The keyword you input has no synonyms in the dictionary!"
    if(len(synonyms)==0):
        return "The keyword you input has no synonyms in the dictionary!"
    str1 = ""
    count = 1
    synonyms = list(set(synonyms))
    for i in synonyms:
        if count > 5:
            break
        str1 += (str(count)+". "+i+"<br>")
        count += 1
    return str1

# def result(request):
#     #time counter
#     start_time = time.time()
#     context = dict()
#     if request.method == "POST":
#         # read in the input keywords.
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             # read in data which filter by form we defined.
#             # we define only input string.
#             post_data = form.cleaned_data['search']
#             #post_data,second_post_data,third_post_data = spell_correction(post_data)
#             post_data = post_data.strip()
#             # add post data into context dictionary.
#             context['postdata'] = post_data
#     # otherwise, the request is GET.
#     else:
#         context['content'] = ""
#         form = SearchForm()
#         context['form'] = form
#         return render(request, 'result.html', context)
    
#     # return related result.
#     context['form'] = form
#     context['title1'] = "English Explantion"
#     #get the english meaning.
#     context['explanation'] = get_meaning(post_data)
#     context['title2'] = "Synonyms"
#     #get chinese translation.
#     context['synonyms']= get_synonyms(post_data)
#     namelist = return_result(post_data)
#     #build a list of amount.
#     # amount is declared at the beginning, global variable.
#     a = [i for i in range(amount)]
#     partial_func = partial(fill_context, context=context, namelist=namelist, post_data=post_data)
#     pool = ThreadPool(processes=20)
#     pool.map(partial_func, a)
#     pool.close()
#     pool.join()

#     #final result of the html page
#     context['final'] = ""
#     count = 1
#     for i in range(amount):
#         if(context['line'+str(i+1)] != "Wrong" and context['line'+str(i+1)] != ""):
#             # change!!! from hdfs.
            
#             total = "<a href=10.20.0.151:9870/project_big/"+context['result'+str(i+1)]+">"
#             context['final'] += total
#             context['final'] += "<h5>"
#             context['final'] += str(count)
#             context['final'] += "."
#             context['final'] += context['result'+str(i+1)]
#             context['final'] += "</h5></a><h6>"
#             context['final'] += context['line'+str(i+1)]
#             context['final'] += "</h6>"
#             context['final'] += '<br>'
#             count += 1
#         else:
#             continue
#     # if (second_post_data == None and third_post_data == None):#the input is correct
#     #     if(count >1):#we have result
#     #         context['content'] = "ALL of the results we found of " + "<strong><i><u>" + post_data + ":" + "</strong></i></u>"
#     #     else:#we do not have result
#     #         context['content'] = "Sorry, there is no such file that matches your keyword!"
#     # else:#the input is wrong
#     #     context['content'] = "<p>"
#     #     context['content'] += "The word input has no matched files." + "Here are all of results we found of " + "<strong><i><u>" + post_data + "." + "</strong></i></u>"
#     #     context['suggestion'] = "Candidate Words: " + "<strong><i><u>" + second_post_data + "</strong></i></u>" + " and " + " <strong><i><u>" + third_post_data + ".</strong></i></u>"
#     #     context['suggestion'] +="</p>"
#     end_time = time.time()
#     context['time'] = str(round(end_time-start_time,2))
#     context['amount'] = count-1
#     return render(request, 'minisearch/result.html', context)

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

# #get the list of all file names
# def return_result(post_data):
#     global amount
#     amount = len(dic[post_data])
#     return dic[post_data]

# #!!!!!change!!
# #fatch files from hdfs
# #get the line contents
# def read_and_load(file_name,post_data,row):
#     path = "10.20.0.151:9870/project_big/"+file_name
#     try:
#         # f = open(path, 'r',encoding='gb18030',errors='ignore')
#         line = linecache.getline(path, int(row))
#     except:
#         return "Wrong"
#     # lines = f.r
#     # eadlines()
#     row = int(row) - 1    #true row number.
#     str1 = ""
#     list1 = re.sub('[^a-zA-Z\d\s]+', '', line).split()
#     try:
#         index = list1.index(post_data)
#     except:
#         return "Wrong"
#     str1 += str(row)
#     if (row < 1000):
#         str1 += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
#     elif(row < 10000):
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

# #fill the context content.
# def fill_context(i,context, namelist, post_data):
#     name1 = 'result' + str(i + 1)
#     namelist_new = namelist[i].split()
#     context[name1] = namelist_new[0]  # get the file name
#     row = namelist_new[1]
#     name2 = 'line' + str(i + 1)
#     context[name2] = read_and_load(context[name1], post_data,row)  # get the line where the post word lies in