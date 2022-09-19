import requests, csv, bs4
from pathlib import Path
from urllib.request import Request,urlopen
from requests import get
from requests_html import HTMLSession
import time
import os


session = HTMLSession()
file = open('extraccionfotocasa.csv')

csvreader = csv.reader(file)
header = []
header = next(csvreader)

rows = []

script = ''' 

 if (document.readyState === "complete" || document.readyState === "interactive"){
 p = document.querySelector('.re-DetailMosaicPhotoWrapper-photo5');
p.click();
 }


'''


for row in csvreader:
	rows.append(row)
	r = session.get(row[1])
	r.html.render(sleep=5, timeout=25, script=script)
	soup = bs4.BeautifulSoup(r.html.html, "html.parser")
	pp= soup.findAll("img")

	os.makedirs('scrapped/'+row[0])
	os.makedirs('scrapped/'+row[0]+'/photos')
	cont = 1
	for img in pp:
		print(img['src'])
		print(cont)
		if '.svg' in img['src']:
			continue
		if cont == 1:
			resource = urlopen(img['src'])
			output = open("scrapped/"+ row[0] +"/featured_photo.jpg","wb")
			output.write(resource.read())
			output.close()
		else:
			try:
				resource = urlopen(img['src'])
			except URLError as e:
				print(e)
			output = open("scrapped/"+ row[0] +"/photos/"+ str(cont) +".jpg","wb")
			output.write(resource.read())
			output.close()
		cont+=1

	time.sleep(15)