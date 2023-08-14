from django.test import TestCase
from organization.models import Organization
import snscrape.modules.twitter as sntwitter
import tweepy
import threading
import datetime
from twitter.models import *



def parse_date(tweet):
    tweet['created_at'] = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S %z %Y') if type(tweet['created_at']) is not datetime.datetime else tweet['created_at']
    tweet['user']['created_at'] = datetime.datetime.strptime(tweet['user']['created_at'],'%a %b %d %H:%M:%S %z %Y') if type(tweet['user']['created_at']) is not datetime.datetime else tweet['user']['created_at']
    return tweet

def createUser(tweet):
    #tweet['created_at'] = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')

    user = User(
        id = tweet['id_str'],
        name = tweet['name'],
        screen_name = tweet['screen_name'],
        location = tweet['location'],
        description = tweet['description'],
        protected = tweet['protected'],
        followers_count = tweet['followers_count'],
        fast_followers_count = tweet.get('fast_followers_count',None),
        normal_followers_count = tweet.get('normal_followers_count',None),
        friends_count = tweet['friends_count'],
        listed_count = tweet['listed_count'],
        created_at = tweet['created_at'],
        favourites_count = tweet['favourites_count'],
        geo_enabled = tweet['geo_enabled'],
        verified = tweet['verified'],
        statuses_count = tweet['statuses_count'],
        media_count = tweet.get('media_count',None),
        lang = tweet['lang'],
        contributors_enabled = tweet['contributors_enabled'],
        is_translator = tweet['is_translator'],
        is_translation_enabled = tweet['is_translation_enabled'],
        profile_background_color = tweet['profile_background_color'],
        profile_background_image_url = tweet['profile_background_image_url'],
        profile_background_image_url_https = tweet['profile_background_image_url_https'],
        profile_background_tile = tweet['profile_background_tile'],
        profile_image_url = tweet['profile_image_url'],
        profile_image_url_https = tweet['profile_image_url_https'],
        profile_banner_url = tweet.get('profile_banner_url',None),
        profile_link_color = tweet['profile_link_color'],
        profile_sidebar_border_color = tweet['profile_sidebar_border_color'],
        profile_sidebar_fill_color = tweet['profile_sidebar_fill_color'],
        profile_text_color = tweet['profile_text_color'],
        profile_use_background_image = tweet['profile_use_background_image'],
        has_custom_timelines = tweet.get('has_custom_timelines',None),
        advertiser_account_type = tweet.get('advertiser_account_type',None),
        analytics_type = tweet.get('analytics_type',None),
        translator_type = tweet.get('translator_type',None),
    )
    #users_bulk[user.id] = user
    user.save()

    for url_json in tweet['entities'].get('url',{'urls':[]})['urls']:
        url = Url(
            #id = url_json['url'],
            url = url_json['url'],
            expanded_url = url_json.get('expanded_url',None),
            display_url = url_json.get('display_url', None),
        )
        #url_bulk[url.url] = url
        #url_bulk_through[(url.url,user.id)] = User.urls.through(user_id=user.id,url_id=url.url)
        url.save()
        user.urls.add(url)

        
    for description_url_json in tweet['entities']['description']['urls']:
        url = Url(
            url = description_url_json['url'],
            expanded_url = description_url_json['expanded_url'],
            display_url = description_url_json['display_url'],
        )
        #url_bulk[url.url] = url
        #urlDescription_bulk_through[(url.url,user.id)] = User.descriptionUrl.through(user_id=user.id,url_id=url.url)
        url.save()
        user.descriptionUrl.add(url)



def tweetParse(tweet):
    tweet = parse_date(tweet)

    # if('retweeted_status' in tweet):
    #     retweeted_status = tweetParse(tweet.get('retweeted_status',False))
    #     retweeted_status.save()
    # else:

    retweeted_status = None

    # if('quoted_status' in tweet):
    #     quoted_status = tweetParse(tweet.get('quoted_status',False))
    #     quoted_status.save()
    # else:
    quoted_status = None

    user = User(
        id = tweet['user']['id_str'],
        name = tweet['user']['name'],
        screen_name = tweet['user']['screen_name'],
        location = tweet['user']['location'],
        description = tweet['user']['description'],
        protected = tweet['user']['protected'],
        followers_count = tweet['user']['followers_count'],
        fast_followers_count = tweet['user'].get('fast_followers_count',None),
        normal_followers_count = tweet['user'].get('normal_followers_count',None),
        friends_count = tweet['user']['friends_count'],
        listed_count = tweet['user']['listed_count'],
        created_at = tweet['user']['created_at'],
        favourites_count = tweet['user']['favourites_count'],
        geo_enabled = tweet['user']['geo_enabled'],
        verified = tweet['user']['verified'],
        statuses_count = tweet['user']['statuses_count'],
        media_count = tweet['user'].get('media_count',None),
        lang = tweet['user']['lang'],
        contributors_enabled = tweet['user']['contributors_enabled'],
        is_translator = tweet['user']['is_translator'],
        is_translation_enabled = tweet['user']['is_translation_enabled'],
        profile_background_color = tweet['user']['profile_background_color'],
        profile_background_image_url = tweet['user']['profile_background_image_url'],
        profile_background_image_url_https = tweet['user']['profile_background_image_url_https'],
        profile_background_tile = tweet['user']['profile_background_tile'],
        profile_image_url = tweet['user']['profile_image_url'],
        profile_image_url_https = tweet['user']['profile_image_url_https'],
        profile_banner_url = tweet['user'].get('profile_banner_url',None),
        profile_link_color = tweet['user']['profile_link_color'],
        profile_sidebar_border_color = tweet['user']['profile_sidebar_border_color'],
        profile_sidebar_fill_color = tweet['user']['profile_sidebar_fill_color'],
        profile_text_color = tweet['user']['profile_text_color'],
        profile_use_background_image = tweet['user']['profile_use_background_image'],
        has_custom_timelines = tweet['user'].get('has_custom_timelines',None),
        advertiser_account_type = tweet['user'].get('advertiser_account_type',None),
        analytics_type = tweet['user'].get('analytics_type',None),
        translator_type = tweet['user'].get('translator_type',None),
    )
    #users_bulk[user.id] = user
    user.save()

    for url_json in tweet['user']['entities'].get('url',{'urls':[]})['urls']:
        url = Url(
            #id = url_json['url'],
            url = url_json['url'],
            expanded_url = url_json.get('expanded_url',None),
            display_url = url_json.get('display_url', None),
        )
        #url_bulk[url.url] = url
        #url_bulk_through[(url.url,user.id)] = User.urls.through(user_id=user.id,url_id=url.url)
        url.save()
        user.urls.add(url)

        
    for description_url_json in tweet['user']['entities']['description']['urls']:
        url = Url(
            url = description_url_json['url'],
            expanded_url = description_url_json['expanded_url'],
            display_url = description_url_json['display_url'],
        )
        #url_bulk[url.url] = url
        #urlDescription_bulk_through[(url.url,user.id)] = User.descriptionUrl.through(user_id=user.id,url_id=url.url)
        url.save()
        user.descriptionUrl.add(url)

    status = Status(
        created_at = tweet['created_at'],
        id = tweet['id_str'],
        content = tweet['full_text'],
        display_text_range_start = tweet['display_text_range'][0],
        display_text_range_end = tweet['display_text_range'][1],
        user_id = user.id,
        source = tweet['source'],
        in_reply_to_status_id = tweet['in_reply_to_status_id'],
        in_reply_to_user_id = tweet['in_reply_to_user_id'],
        in_reply_to_screen_name = tweet['in_reply_to_screen_name'],
        #place = models.ForeignKey(Place,on_delete=models.PROTECT)
        is_quote_status = tweet['is_quote_status'],
        retweet_count = tweet['retweet_count'],
        favorite_count = tweet['favorite_count'],
        conversation_id = tweet.get('conversation_id',None),
        possibly_sensitive = tweet.get('possibly_sensitive',False),
        possibly_sensitive_editable = tweet.get('possibly_sensitive_editable',False),
        lang = tweet['lang'],
        retweet_status = None if retweeted_status == None else retweeted_status,
        quoted_status = None if quoted_status == None else quoted_status,
    )
    #status_bulk[status.id] = status
    status.save()

    if 'extended_entities' in tweet:
        for entity_json in tweet['extended_entities']['media']:
            if(entity_json['type'] == "photo"):
                url = Url(
                    url = entity_json['url'],
                    display_url = entity_json['display_url'],
                    expanded_url = entity_json['expanded_url'],
                )
                #url_bulk[url.url] = url
                url.save()

                photo = Photo(
                    id = entity_json['id_str'],
                    media_url = entity_json['media_url'],
                    media_url_https = entity_json['media_url_https'],
                    media_key = entity_json.get('media_key',None),
                    url_id = url.url,
                )
                photo.save()
                status.photos.add(photo)
                #photos_bulk[photo.id] = photo
                #photoStatus_bulk[(photo.id,status.id)] = Status.photos.through(photo_id=photo.id,status_id=status.id)

            elif(entity_json['type'] == "video"):
                url = Url(
                    url = entity_json['url'],
                    display_url = entity_json['display_url'],
                    expanded_url = entity_json['expanded_url'],
                )
                url.save()
                #url_bulk[url.url] = url
                for variants_json in entity_json['video_info']['variants']:
                    if( variants_json["content_type"] == "application/x-mpegURL" ):
                        video_url = variants_json["url"]
                    
                video = Video(
                    id = entity_json['id_str'],
                    media_url = entity_json['media_url'],
                    media_url_https = entity_json['media_url_https'],
                    media_key = entity_json.get('media_key',None),
                    url_id = url.url,
                    aspect_ratio_x = entity_json['video_info']['aspect_ratio'][0],
                    aspect_ratio_y = entity_json['video_info']['aspect_ratio'][1],
                    duration_millis = entity_json['video_info']['duration_millis'],
                    video_url = video_url,
                )
                video.save()
                status.videos.add(video)
                #videos_bulk[video.id] = video
                #videosStatus_bulk[(video.id,status.id)] = Status.videos.through(video_id=video.id,status_id=status.id)
            elif(entity_json['type'] == "animated_gif"):
                url = Url(
                    url = entity_json['url'],
                    display_url = entity_json['display_url'],
                    expanded_url = entity_json['expanded_url'],
                )
                #url_bulk[url.url] = url
                url.save()
                gif = Gif(
                    id = entity_json['id_str'],
                    media_url = entity_json['media_url'],
                    media_url_https = entity_json['media_url_https'],
                    media_key = entity_json.get('media_key',None),
                    url_id = url.url,
                    aspect_ratio_x = entity_json['video_info']['aspect_ratio'][0],
                    aspect_ratio_y = entity_json['video_info']['aspect_ratio'][1],
                    gif_url = entity_json['video_info']['variants'][0]["url"],
                )
                gif.save()
                status.gifs.add(gif)
                #gifs_bulk[gif.id] = gif
                #gifsStatus_bulk[(gif.id,status.id)] = Status.gifs.through(gif_id=gif.id,status_id=status.id)


    for hashtag_json in tweet['entities']['hashtags']:
        hashtag = Hashtag(
            text = hashtag_json['text']
        )
        hashtag.save()
        status.hashtags.add(hashtag)
        #hashtag_bulk[hashtag.text] = hashtag
        #hashtag_bulk_through[(hashtag.text,status.id)] = Status.hashtags.through(status_id=status.id,hashtag_id=hashtag.text)

    for user_mention_json in tweet['entities']['user_mentions']:
        user_mention = UserMention(
            screen_name = user_mention_json['screen_name'],
            name = user_mention_json['name'],
            id = user_mention_json['id_str'],
        )
        user_mention.save()
        status.user_mentions.add(user_mention)
        #userMention_bulk[user_mention.id] = user_mention 
        #userMention_bulk_through[(user_mention.id,status.id)] = Status.user_mentions.through(status_id=status.id,usermention_id=user_mention.id)

    for url_json in tweet['entities']['urls']:
        url = Url(
            url = url_json['url'],
            expanded_url = url_json['expanded_url'],
            display_url = url_json['display_url'],
        )
        url.save()
        status.urls.add(url)
        #url_bulk[url.url] = url
        #urlStatus_bulk_through[(url.url,status.id)] = Status.urls.through(status_id=status.id,url_id=url.url)

    return status

class TwitterAPI:
    def __init__(self):
        self.keys = [
                    # ['3nVuSoBZnx6U4vzUxf5w','Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'],
                    # ['IQKbtAYlXLripLGPWd0HUA','GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU'],
                    # ['CjulERsDeqhhjSme66ECg','IQWdVyqFxghAtURHGeGiWAsmCAGmdW3WmbEx6Hck'],
                    # ['3rJOl1ODzm9yZy63FACdg','5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8'],
                    # ['3nVuSoBZnx6U4vzUxf5w','Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'],
                    # ['d0CTc4Zg9pufCnMkteDc7w','z4FMZhP87U5QEwycggDe5JN6TDDh7xEyhnAcEpdWk'],
                    # ['CVbiuNGV6MeQCsku7SUZnejVb','AXzQ9ZSxu1JPWbQNXHj4Zn1uI32fMDviLDYyKM6RihwPjGz6i9'],
                     ['7Uifmz2gkHF8RcOcMtItTJRoF', 'YmcL95Yy15zvwAfGVaCrbGaUkcWo6wv0OT9RXCOxWfoHwuY1RT'],
                    # ['fTOd3soD4e9vhvArXdoVFVdCS', 'WlBzWiuZ33RxyFhJXPuMMRWi1tJu71hzIGLUYHv6k59DsXOYjp'],
                    #['PMXB9uR9Qfh4gweyTtjOZqZvV', 'dwaLM6DL8kPQnUppJp8upK9ftTdfu30vcCP03vOb5dgRYW2mH5'],
                    ]
        

        self.data = []
        self.apis = []
        for x in self.keys:
            try:
                auth = tweepy.AppAuthHandler(x[0], x[1]) 
                authenticated = tweepy.API(auth, wait_on_rate_limit=True)
                self.apis.append(authenticated)
                print('working')
            except:
                print(f'Failure on {x[0]}, does not work any more')
            # client = tweepy.Client(
            #     consumer_key="q57QlTTwLKnCoacZZobutKuoB",
            #     consumer_secret="TX2t6yrMaM6VmXdKHQhtiwBF9K4uZYUgBCIwHvb0Ao5kR0fN3o",
            #     access_token="1708154522-5g1ftU40y8FsWiIjRUoq6miG6prgKxrKDFG1wf4",
            #     access_token_secret="7P4eHgzSVllx5tA8Tzt4ppIrAAXUFg2khWXnKtejdIc8P"
            # )
            # self.apis.append(client)
    @property
    def keysLen(self,):
        return len(self.apis)

    def splitList(self,alist, wanted_parts=1):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts) ]


class TwitterTimeLine(TwitterAPI):
    def __init__(self):
        super().__init__()
        self.data = {}

    def _getTweets(self,userids,api,lastid):
        for i,id in enumerate(userids):
            
            print(id)
            
            for x in tweepy.Cursor(api.user_timeline, screen_name =id,since_id=lastid,tweet_mode="extended",count=200).items():
            #for x in tweepy.Paginator(api.get_users_tweets, id =id,since_id=lastid,max_results=100,user_auth=True).flatten(limit=3200):
                tweetParse(x._json)


    def getTweets(self, userids,lastid):
        splitedList = self.splitList(userids,self.keysLen) 
        print(self.keysLen)
         
        threads = [threading.Thread(target=self._getTweets, args=(splitedList[i],self.apis[i],lastid)) for i in range(self.keysLen)]
        #threads = [threading.Thread(target=self._getTweets, args=(splitedList[i],self.apis[i],inicialid)) for i in range(1)]
        print(threads)
        [thread.start() for thread in threads]        
        [thread.join() for thread in threads]

# Create your tests here.

def getAllTwitters():
    urls = Organization.objects.filter(twitter_url__isnull=False).values_list('twitter_url',flat=True)
    handles = list( map(lambda x : x.split('/')[-1], urls) )
    print(handles)
    return handles


handles = getAllTwitters()
timelines = TwitterTimeLine()
lastTweetId = Status.objects.latest('created_at').id
timelines.getTweets(handles,lastTweetId)

lastTweetId = 0




# import spacy
# from spacy import displacy
# from collections import Counter
# import pt_core_news_md

# nlp = pt_core_news_md.load()
# status = Status.objects.filter(entities__isnull=True)

# for i,item in enumerate(status):
#     print(f'{i} of {len(status)}')
#     document = nlp(item.content)
#     for named_entity in document.ents:
#         entity = Entity(
#             name = str(named_entity),
#             type = named_entity.label_,
#         )
#         entity.save()
#         item.entities.add(entity)
