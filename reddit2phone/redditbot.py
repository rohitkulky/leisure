import time
import csv
import praw
import sys
from collections import defaultdict
from pushbullet import PushBullet

apiKey = "YOUR API KEY HERE"
p = PushBullet(apiKey)
devices = p.getDevices()

contacts = p.getContacts()

subreddit_names = sys.argv[1]
r = praw.Reddit('Reddit app to deliver jokes and other stuff. For now, news..')

already_delivered = defaultdict(list)
time_counter = 0
while True:
    delivery_text = defaultdict(list)
    time_counter += 1
    subreddit = r.get_subreddit(subreddit_names)
    for submission in subreddit.get_hot(limit=30):
        text = submission.selftext.encode('utf-8').strip().replace('\n',' ')
        title = submission.title.encode('utf-8').strip().replace('\n',' ')
        url = submission.url.encode('utf-8').strip().replace('\n',' ')
        post_time = submission.created
        if submission.id not in already_delivered.keys():
            delivery_text[submission.id].append([subreddit_names,title,text,url,post_time])
            already_delivered[submission.id].append(title)
            already_delivered[submission.id].append(text)
            already_delivered[submission.id].append(url)
            already_delivered[submission.id].append(post_time)
    for each_post in delivery_text.keys():
        if 'jokes' in subreddit_names.lower():
            print delivery_text[each_post][0][1],delivery_text[each_post][0][2]
            p.pushNote(devices[0]["iden"],'JOKES',delivery_text[each_post][0][1] + '|' + delivery_text[each_post][0][2])
        else:
            print delivery_text[each_post][0][1],delivery_text[each_post][0][3]
            p.pushNote(devices[0]["iden"],delivery_text[each_post][0][0] + ' : ' + delivery_text[each_post][0][1], 'Read More - ' + delivery_text[each_post][0][3])
        time.sleep(60)
    if time_counter % 10 == 0:
        with open('/home/ubuntu/reddit-delivery/news/'+str(time.time())+'.txt','wb') as tf:
            writer = csv.writer(tf, delimiter = '\t')
            for item in already_delivered.keys():
                writer.writerow(already_delivered[item])
        already_delivered = defaultdict(list)
    time.sleep(1800)