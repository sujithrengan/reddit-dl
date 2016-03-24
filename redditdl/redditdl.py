from bs4 import BeautifulSoup
import requests
import pathlib
import threading
import praw
import argparse
import zipfile
import re

def save_image( filename, content):
	with open(str('../bin/'+filename),'wb') as file:
		file.write(content)
		file.close

def file_check(filename,content):
	try:
		filename=re.sub('[/\\?:><"|*]','_',filename)
		path = pathlib.Path('../bin/'+filename)
		#print(''.join( [ "%02X " % ord( x ) for x in content ] ).strip())
		if path.is_file():
			print('AlreadyDownloaded')
		else:
			print('name= '+filename)
			save_image(filename,content)
	except OSError as err:
		print("OS error: {0}".format(err))


parser = argparse.ArgumentParser(description='Options')
parser.add_argument('-r', help='subreddit name')
parser.add_argument('-n', type=int, default=10,
                   help='Number of posts (default: 10)')
#parser.add_argument('-a',help='Album link')

args = parser.parse_args()
#print(args.accumulate(args.integers))

symbols=['\\','/','<','>',':','?','|','"','*']
if args.r!=None:
	r = praw.Reddit(user_agent='redditdlv0.1 by /u/sujithrengan')
	subreddit = r.get_subreddit(args.r).get_hot(limit=args.n)
	#print(dir(subreddit))
	for post in subreddit:
		print(post.url)
		tag=post.url.split('/')
		filetypes=['.jpg','.png','.jpeg','.gif']
		downloaded=False
		for ftype in filetypes:
			if post.url.endswith(ftype):
				request = requests.get (post.url)
				filename=post.title+'_'+tag[-1]+ftype
				file_check(filename,request.content)
				downloaded=True
				print('filetype-found')
				break
		
		ftype='.jpg'
		#if post.url.endswith(('.jpg','.png','.jpeg','.gif')):
		#	request = requests.get (post.url)

		#else:	
		if not(downloaded):
			print('explicit.jpg')
			request = requests.get (post.url+ftype)
			file_check(post.title+'_'+tag[-1]+ftype,request.content)

		"""
		if post.url[:19]=="http://i.imgur.com/":
			filename=post.title+'_'+post.url[19:]
			request = requests.get (post.url)
			file_check(filename,request.content)
		elif "imgur" in post.url:
			filename=post.title+'_'+post.url[17:]+'.jpg'
			request = requests.get ('http://i.imgur.com/'+post.url[17:]+'.jpg')
			file_check(filename,request.content)
		"""
		if True:
			pass
		else:
			with open('../bin/manual_download.txt','a') as file:
				file.write('\n'+post.url)
				file.close

			request = requests.get(post.url)
			soup=BeautifulSoup(request.content,'html.parser')
			for link in soup.find_all('meta'):
				if link.get('property')=='og:image':
					ptype=link.get('content').rsplit('?',1)
					ptype=ptype[0].rsplit('.',1)
					filename=post.title+'_'+'external'+'.'+ptype[1] #TODO: include image tag and filename symbol consistency 
						
					request = requests.get (link.get('content'))
					file_check(filename,request.content)
elif args.a!=None:
	print(args.a)
else:
	print('FuckOff')
