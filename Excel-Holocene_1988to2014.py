
# coding: utf-8

# In[2]:

import anthropocene.readers as rd
from anthropocene.classes import Paper,KeyPaper
dir_papers = rd.wos.from_dir("/Users/Ramki/Desktop/Anthropocene/Anthropocene Files/Holocene_1988to2014")
#dir_papers


# In[3]:

dir_papers[40]


# In[4]:

# December 1

# Initialize to avoid overwriting
keywords_list = []
side_list=[]
main_list = [] 
main_dict ={}


keywords_list_new = []
side_list_new=[]
main_list_new = [] 
main_dict ={}
count=1
# This loop runs for each paper
for r in dir_papers:
    if r['keywords']:
        print "count::" , count
        #print "################################Keywords::" , r['keywords'] , r['date']
        
        
        ### Make the lists empty to avoid overwriting
        keywords_list = []
        side_list=[]
        main_list_new = [] 
        
        # New dict
        keywords_list_new = []
        side_list_new=[]
        main_list = [] 
        
        ### This loop runs for each each keyword of a paper
        for each_kw in r['keywords']:
            each_kw = each_kw.strip().lower() # convert to lowercase, even if it is not.
            try:
                main_dict[r['date']][0].keys() # to direct it to main_dict
                if r['date'] in main_dict.keys():
                    lst = [item.keys() for item in main_dict[r['date']]]
                    for i in lst:
                            for j in i:
                                if j not in side_list:
                                    side_list.append(j)
                    if any(each_kw in st for st in lst):
                        #print "##ALREADY"
                        kw_index = side_list.index(each_kw)
                        main_dict[r['date']][kw_index][each_kw] += 1
                        #print "cool*************" ,main_dict[r['date']] 
                    
                    else:
                       #print "##else"
                        new_dict={}
                        new_dict[each_kw] = 1
                        main_dict[r['date']].append(new_dict)
                        #print "main dict here$$$$$$$ " , main_dict
                        #print "herererrerer" , main_dict[r['date']]      
                           
            except:
                #print "except",main_dict
                keywords_dict={}
                side_list=[]
                keywords_dict[each_kw] = 1
                keywords_list.append(keywords_dict)
                main_dict[r['date']]= keywords_list  
                #print "keywords_dict" , keywords_dict , "keywords_list", keywords_list
                #print "maindict in except" , main_dict
        count=count+1


# In[ ]:




# In[5]:

#Prepare the dict for CSV

papers = []
main_list =[]
main_dict


for k,val in main_dict.iteritems():
        print k
        paper = KeyPaper()
        for j in val:
            #print j
            for l,m in j.iteritems():
                paper['date'] = k
                paper['keywords'] = l
                paper['count'] = m
                main_list.append(paper)
                paper={}
                
  
#print "main_list", main_list
   


# In[6]:

# Create the CSV File.

import csv
keys = ['date','keywords','count']
f = open('Excel-Holocene_1988to2014.csv', 'wb')
dict_writer = csv.DictWriter(f, keys)
dict_writer.writer.writerow(keys)
dict_writer.writerows(main_list)

