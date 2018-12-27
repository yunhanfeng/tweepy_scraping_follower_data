
#### twitter scraping follower's data ####
import tweepy
import pandas as pd
from secrets import *

C_KEY = 
C_SECRET = 
A_TOKEN = 
A_TOKEN_SECRET = 

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)

api = tweepy.API(auth)

##################################################################################### 
### scrape followers of UMASH
users = tweepy.Cursor(api.followers, screen_name="umash_umn", count = 200).items()

screennamelst = list()
namelst0 = list()

for u in users:   
    namelst0.append(u.name)

for u in users:
    screennamelst.append(u.screen_name)

umash_follower = pd.DataFrame({'screen_name':screennamelst, 'user_name':namelst0})
umash_follower.to_csv('follower.csv', sep=',')

################################# single user follower #############################
 ### experiemnt : giantfoodie
foodie_follower = tweepy.Cursor(api.followers, screen_name="SFGiantFoodie", count = 200).items()
foodie_list = list()

for u in foodie_follower:
    foodie_list.append(u.screen_name)

### get all follower's follower 
all_follower = list()

for i in screennamelst[1:5]:
    for u in tweepy.Cursor(api.followers, screen_name=i,count=200).items():
        all_follower.append(u.screen_name)
        
follower_follower_15 = pd.DataFrame({'screen_name':all_follower})
follower_follower_15.to_csv("follower's followers.csv", sep = ',')

follower_count = follower_follower_15.groupby('screen_name').size().sort_values(ascending = False)
# no duplicate

#####################################################################################
### experiment: get envirostat's friend_id
env_friend = tweepy.Cursor(api.friends_ids, screen_name='EnviroStat_AJ',count=200).items()
env_friendlst = list()

for u in env_friend:
    env_friendlst.append(u)

### get all follower's friend_id     
all_friend2 = list()
for i in screennamelst[6:10]:
    for u in tweepy.Cursor(api.friends_ids, screen_name=i,count=200).items():
        all_friend2.append(u)

follower_friend610 = pd.DataFrame({'friend_id': all_friend2})
follower_friend610.to_csv("follower's friend.csv", sep = ',')

friend_count = follower_friend610.groupby('friend_id').size().sort_values(ascending = False)
friend_count2 = friend_count[friend_count>=2]

friend_count2.to_csv('top friend.csv', sep=',')

#####################################################################################
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

api = twitter_setup()

## First trial with first user for timeline fields
tweets = api.user_timeline(screen_name="wiscoag", count=2)
print ("Number of tweets extracted: {}.\n".format(len(tweets)))

for item in tweets:
    print(item._json)
    
for tweet in tweets[1:2]:
    print (tweet.user.location, '/' ,tweet.user.name)

#####################################################################################
df_follower = pd.read_csv('follower.csv')

namelst = df_follower['screen_name'].tolist()

loclist = []
namelist = []

for name in namelst[1:300]:
    try:
        user_tweets = api.user_timeline(screen_name= name, count=2)
    except Exception as e:
        user_tweets = list([0])
    if type(user_tweets) == list:
        loclist.append('Private Account')
        namelist.append('Private Account')
    else:
        for tweet in user_tweets[1:2]:
            loclist.append(tweet.user.location)
            namelist.append(tweet.user.name)

df_300 = pd.DataFrame({'1. name':namelist, '2. location':loclist})
df_300.to_csv('follower_location.csv', sep=',')
