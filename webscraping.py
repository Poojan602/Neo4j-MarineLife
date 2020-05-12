from bs4 import BeautifulSoup
import requests
import pandas as pd

link = 'https://oceana.ca/en/marine-life/canadian-marine-life-encyclopedia'
response = requests.get(link)

soup = BeautifulSoup(response.text,"html.parser")

division = soup.findAll('section',attrs={'class':'block-callout-action-contain inner-contain flex-contain-wrap'})

Name = []
Ecosystem = []
Feeding = []
Conservation = []

for loop in division:
    for loop2 in loop.findAll('a',href=True):
        inner_link = "https://oceana.ca/"+loop2['href']
        temp_response = requests.get(inner_link)
        soup2 = BeautifulSoup(temp_response.text,"html.parser")

        namesection = soup2.findAll('div',attrs={'class':'subpage-header-inner'})

        for lp in namesection:
            Name.append(lp.find('h1').text)

        inner_division = soup2.findAll('div',attrs={'class':'animal-details-side animal-details-side-canada'})

        for loop3 in inner_division:     
            allh2 = loop3.findAll('h2')
            allp = loop3.findAll('p')

            success = 0
            for test in allh2:
                if(test.text == "Conservation Status"):
                    success+=1

            for index4,loop4 in enumerate(allh2):
                if(success == 1):
                    if(loop4.text == "Ecosystem/Habitat"):
                        Ecosystem.append(allp[index4].text.strip())
                    elif(loop4.text == "Feeding Habits"):
                        Feeding.append(allp[index4].text.strip())
                    elif(loop4.text == "Conservation Status"):
                        Conservation.append(allp[index4].text.strip())
                elif(success == 0):
                    if(loop4.text == "Ecosystem/Habitat"):
                        Ecosystem.append(allp[index4].text.strip())
                    elif(loop4.text == "Feeding Habits"):
                        Feeding.append(allp[index4].text.strip())
                        Conservation.append("Not available")
                    
df = pd.DataFrame({'Name':Name,'Habitat/Ecosystem':Ecosystem,'Feeding_Habits':Feeding,'Conservation_Status':Conservation})
df.to_csv('Marine_Life.csv', index=False, encoding='utf-8')





