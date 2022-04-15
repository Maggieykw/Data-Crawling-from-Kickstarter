
# coding: utf-8

# In[ ]:


#ReadMe - Instruction
###Before running code
#1.make sure your python installed requests,beautifulsoup4 (type the following code inside terminal)
#pip install -U requests
#pip install -U beautifulsoup4

#2.make sure you have "query_result.csv" (which contains column "uname" and "url") inside directory.

###Instruction
#This coding is used to crawl web data of all selected Kickstarter products from Kickstarter :
#-->Loop all URL of the product
#--> Crawl info of designer/product 
#--> Save all result in csv called "DesignerData.csv"

#Remark: there is the function called randomSleep which is used to try avoiding to be blocked by the website


# In[10]:


###List of importing
#For function "make_soup", "crawl_info"
import requests
from bs4 import BeautifulSoup

#For function "rawdata", Data_write_csv", Data_append_csv"
import csv

#For function "rawdata"
from collections import defaultdict

#For function "randomSleep"
import time, random


# In[11]:


def rawdata():
    columns = defaultdict(list) # each value in each column is appended to a list

    with open('query_result.csv',encoding="latin-1") as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k

    return(columns['uname'],columns['url'])

#OR using Pandas, below is just for reference, may have some typo
#import pandas as pd
#data = pd.read_csv("sdfds.csv")
#uname = data['uname'] #pandas.series
#uname = pd.to_list(uname)


# In[12]:


def make_soup(url):

    page = requests.get(url)

    return BeautifulSoup(page.text, 'html.parser')


# In[13]:


def randomSleep():
        sleeptime =  random.randint(2, 5)
        time.sleep(sleeptime)


# In[14]:


def crawl_info(ProductName,KickstarterURL): 
    try:
        ###Collect designer page of the product
        soup=make_soup(KickstarterURL+'/creator_bio')
        
        ###Try avoiding to be blocked, with a random short wait
        randomSleep()

        ###For testing
        #print(soup) 
        #print(soup.status_code) 
        #print(soup.prettify()) #show all coding in the web page
        
        links=[] #for store related websites
        Data=[] #for store result
        CompanyName = ""
        CompanyDescription = ""
        ListOfWebsites = ""       
        MainDesignerName = ""
        LastLogin = ""
        LastLogin2 = ""
        DesignerFB = ""
        NoOfFBFriends = ""
        NoOfProductCreated = ""
        NoOfProductBacked = ""
        NoOfUpdate = ""
        StartFundingDate = ""
        StartFundingDate2 = ""
        EndFundingDate = ""
        EndFundingDate2 = ""
        
        ##Below: before getting web data, we assume they are nothing, if the specific text is found, we will update them
        #1. Crawl company name
        CN = soup.find('div',class_="table-cell full-width px3 border-box")
        if CN:
            CompanyName = CN.find('a',class_="green-dark").get_text()
            CompanyName = CompanyName.replace('\n','') #remove "\n" in the text
        
        #2. Crawl company description
        CD = soup.find('div',class_="col col-7 col-post-1 pt3 pb3 pb10-sm")
        if CD:
            CompanyDescription = CD.find('div',class_="readability").get_text()
            CompanyDescription = CompanyDescription.replace('\n','') #remove "\n" in the text
        
        #3. Crawl list of related websites (e.g. company homepage, facebook, twitter)
        LW = soup.find('div',class_="pt3 pt7-sm mobile-hide")
        if LW:
            ListOfWebsites = LW.findAll('a')

            for link in ListOfWebsites:
                links.append(link.get('href'))  #OR: links.append(link['href'].strip())
        
        ###Prepare for the following crawlling
        RangeOfDesignerDetail = soup.find('div',class_="creator-bio-details col col-4 pt3 pb3 pb10-sm")
        
        if RangeOfDesignerDetail:
            #4. Crawl designer name
            MDN = RangeOfDesignerDetail.find('span',class_="identity_name")
            if MDN:
                MainDesignerName = MDN.get_text()
                MainDesignerName = MainDesignerName.replace('\n','') #remove "\n" in the text

            #5. Crawl last login
            LL = RangeOfDesignerDetail.find('time')
            if LL:
                LastLogin = LL.get('datetime') #Original datetime

                LastLogin2 = LL.get_text() #Adjusted time

            #6. Crawl private FB account of designer
            FB = RangeOfDesignerDetail.find('span',class_="number f6 nowrap")
            if FB:
                DesignerFB = FB.find('a').get('href')

            #7. Crawl facebook like of designer private account
                NoOfFBFriends = FB.get_text().split()[0] #remove "friends" after the number

            #8. Crawl number of product created by designer on Kickstarter
            NPC = RangeOfDesignerDetail.find('div',class_="created-projects py2 f5 mb3")
            if NPC:
                NoOfProductCreated = NPC.get_text().split()[0] #remove "created" after the number
                NoOfProductCreated = NoOfProductCreated.replace('First','1') #change "first" into "1" if designer only create one product in Kickstarter

                #9. Crawl number of product backed by designer on Kickstarter
                NoOfProductBacked = NPC.get_text().split()[-2] #remove "created" after the number      

        ###change soup to crawl the following data
        soup=make_soup(KickstarterURL)

        #10. Crawl number of time to update product's related info in Kickstarter
        NOU = soup.find('a',class_="js-load-project-content js-load-project-updates mx3 project-nav__link--updates tabbed-nav__link type-14")
        if NOU:
            NoOfUpdate = NOU.get_text().split()[1]

        #11. Crawl funding period
        period = soup.find('div',class_="NS_campaigns__funding_period").find('p',class_="f5").findAll()
        if period:
            StartFundingDate = period[0].get('datetime')
            StartFundingDate2 = period[0].get_text()     

            EndFundingDate = period[1].get('datetime')
            EndFundingDate2 = period[1].get_text()
        
        Data.append(ProductName) #input value
        Data.append(CompanyName)
        Data.append(CompanyDescription)
        Data.append(links)
        Data.append(MainDesignerName)
        Data.append(StartFundingDate)   #Data = Data + [StartFundingDate, StartFundingDate2]
        Data.append(StartFundingDate2)
        Data.append(EndFundingDate)
        Data.append(EndFundingDate2)
        Data.append(LastLogin)
        Data.append(LastLogin2)
        Data.append(NoOfUpdate)
        Data.append(DesignerFB)
        Data.append(NoOfFBFriends)
        Data.append(NoOfProductCreated)
        Data.append(NoOfProductBacked)
        
        Data_append_csv(Data)

    except Exception as e:
        print(e)

#crawl_info('naked-0','https://www.kickstarter.com/projects/1218200025/naked-0')


# In[15]:


def Data_write_csv():
    with open("DesignerData.csv","w") as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(["Product Name","Company Name","Company Description",                         "List of related websites","Designer","Start Funding Period","Start Funding Period2",                         "End Funding Period","End Funding Period2","Last Login Time",                         "Adjusted Last Login Time","No. of update for the product",                         "Facebook Account of designer","No. of Facebook Friends",                         "No. of product created in Kickstarter","Number of product backed in Kickstarter"])


# In[16]:


def Data_append_csv(data):
    with open("DesignerData.csv","a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)


# In[17]:


def main():
    
    #Collect list of product name and their Kickstarter URL from "query_result.csv"
    ListOfProductName = rawdata()[0]
    ListOfKickstarterURL = rawdata()[1]
    
    #Create a new csv file called "DesignerData.csv" storing result of data crawling
    Data_write_csv() 
    
    x=0
    
    for KickstarterURL in ListOfKickstarterURL:
        #1. Crawl comment from website & 2. put them into "DesignerData.csv" file
        ProductName = ListOfProductName[x]
        
        crawl_info(ProductName,KickstarterURL)

        x +=1 #change to next product
main()

