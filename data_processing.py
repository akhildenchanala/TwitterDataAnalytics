import pandas as pd
import googlemaps
from textblob import TextBlob

def filter_tweets(tweets, file_path):
    id_list = tweets['id_list']
    tweet_Data = pd.DataFrame(id_list,columns=['id'])
    tweet_Data['id'] = tweets['id_list']
    tweet_Data['user'] = tweets['screen_name_list']
    tweet_Data['text'] = tweets['text_list']
    tweet_Data['retweet_count'] = tweets['retweet_count_list']
    tweet_Data['location'] = tweets['location_list']

    tweet_text_list = []
    tweet_location_list = []
    tweet_latitude = []
    tweet_longitude =[]
    tweet_country = []
    tweet_translation= []
    tweet_language = [] 
    Sentiments_list = []

    count = 0

    for id,row  in tweets.iterrows():
        
        raw_tweet_text = row['text_list']
        message = TextBlob(str(raw_tweet_text))
        location = row['location_list']
        if((count<200) & (len(location) >=4)):
 
            (latitude,longitude,country) = geocode_location(location)
            count = count+1
            tweet_latitude.append(latitude)
            tweet_longitude.append(longitude)
            tweet_country.append(country)
    
            #Detecting and Changing the language to english for sentiment analysis
            lang = message.detect_language()
            tweet_language.append(str(lang))
            try:
                if str(lang) != "en":
                    message = message.translate(to="en") #Problem Here
            except:
                pass

            #### Special Character removal #####
            message = str(message)
            new_message = ""
            for letter in range(0,len(message)):
                current_read =message[letter]
                if ord(current_read) > 126:
                    #this is a special character & hence will be skipped
                    continue
                else:
                    new_message =new_message+current_read

            message = new_message ### Change here on :: Added the Translated Text to Database
            tweet_translation.append(message[:120])
            message = TextBlob(message)
            
            ######################################
            #Changing the Language is important
            #Since it will help in sentiment analysis using TextBlob
            #When language is english remove special characters :: heavily affects analysis
            sentiment = message.sentiment.polarity
            Sentiments_list.append(sentiment)
                            
        else:
            tweet_latitude.append("")
            tweet_longitude.append("")
            tweet_country.append("")
            Sentiments_list.append("")
       
        tweet_text_list.append(raw_tweet_text)
        tweet_location_list.append(location)

        
           
    tweet_Data["location"] = tweet_location_list
    tweet_Data["sentiments"] = Sentiments_list
    tweet_Data["text"] = tweet_text_list
    tweet_Data["latitude"] = tweet_latitude
    tweet_Data["longitude"]= tweet_longitude
    tweet_Data["country"] = tweet_country
    
    tweet_Data.to_csv(file_path)
    print("saved file to: "+ file_path)


def geocode_location(loc):

    gm = googlemaps.Client(key='AIzaSyBq0Lddhu5DQ3v_Kukw421h4TX01gSmlrA')
    location_result = gm.geocode(loc)

    if len(location_result) > 0:
        
        latitude = location_result[0]['geometry']['location']['lat']
        longitude= location_result[0]['geometry']['location']['lng']
        country =location_result[0]['formatted_address'].split(",")
        country = country[len(country)-1]	
        return (latitude,longitude,country)

    else:

        return ("","","")
  
    return


file = pd.read_csv('./data/trends/trends.csv')

for id,row in file.iterrows():
    location = row[0]
    file_path = str("./data/hashtags/") + str(location) + str(".csv")
    data = pd.read_csv(file_path)
    tweet_Data = filter_tweets(data, file_path = file_path)
