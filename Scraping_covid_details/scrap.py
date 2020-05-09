import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib import style

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#   open the url and make the connections
html = urllib.request.urlopen("https://www.mohfw.gov.in/", context=ctx).read()

# parsing the Data by Beautiful BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# table_headers contain all headers of table
table_headers = ['S.No','Name of State',"conformed cases",'Discharged',"Deaths","Active cases"]

# soup all the required data
tr=soup('tr')

content=[]
sum_of_total_active_cases=0

# converts convert the data and remove '\n'
converts=lambda line:[word.text.replace('\n','') for word in line]
for row_data in tr[1:34]:
    tr1=converts(row_data.find_all('td'))
    tr1.append(int(tr1[2])-int(tr1[3])-int(tr1[4]))
    sum_of_total_active_cases += int(tr1[2])-int(tr1[3])-int(tr1[4])
    content.append(tr1)


#----------------------------------------------
#print the table content all Data
table_contain_all_data=tabulate(content,headers=table_headers)
print(table_contain_all_data)
#-------------------------------------------------

# total_conformed_cases_in_india so far
total_conformed_cases_in_india=converts(tr[34].find_all('td'))  #all totals

print(total_conformed_cases_in_india[0],':')
print("Total Conformed Cases:",total_conformed_cases_in_india[1])
print("Total Discharged Cases:",total_conformed_cases_in_india[2])
print("Total Deaths:",total_conformed_cases_in_india[3])
print("Total Active cases:",sum_of_total_active_cases)
#-----------------------------------------

# get all column Data
States,Active_cases,death,Discharged=[],[],[],[]
for specific_data in content:
    States.append(specific_data[1])
    Active_cases.append(specific_data[5])
    death.append(specific_data[4])
    Discharged.append(specific_data[3])
#--------------------------------------------

# bar graph shows all active cases statewise
plt.barh(States,Active_cases,label='Active cases in India',color='g')
plt.legend()
plt.tick_params(axis='x',rotation=0)
plt.tick_params(axis='y',rotation=0)
plt.xlabel("States in India")
plt.ylabel("Active cases in India")
plt.title('Active cases in each state in India')
plt.show()
#--------------------------------------------------
# it shows Discharged cases in India
style.use('ggplot')
plt.plot(States,Discharged,'g',label='Discharged',linewidth='4')
plt.plot(States,death,'r',label="Deaths",linewidth='4')
plt.legend()
plt.xlabel("States")
plt.ylabel("Discharged and Deaths")
plt.tick_params(axis='x',rotation=70)
plt.grid(True,color='k')
plt.title('Discharged cases in India')
plt.show()

#-----------------------------------------------------------
#pie chart shows Percentage of deaths in each state
colors=['r','g','y']*11
plt.pie(death,
        labels=States,
        colors=colors,
        startangle=90,
        shadow=True,
        explode=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0),
        autopct="%1.1f%%")
plt.title('Percentage of Deaths in each States in India')
plt.show()
#-----------------------------------------------------------
