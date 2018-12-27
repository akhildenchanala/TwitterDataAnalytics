import pandas as pd

file = pd.read_csv('./data/trends/trends.csv')
data = []
for id,row in file.iterrows():
    location = row[0]
    file_path = str("./data/hashtags/") + str(location) + str(".csv")
    ####################################################################
    hashtag = pd.read_csv(file_path, low_memory = False)
    hashtag['created_at'] = pd.to_datetime(hashtag['created_at_list'])
    hashtag.set_index('created_at', drop=False, inplace=True)
    hashtag = hashtag['created_at'].resample('1d').count()
    #######################################################################
    data.append(hashtag)
    
df = pd.concat(data, axis=1, ignore_index=True).fillna(0)
df.to_csv('./data/trends_flow/graph.csv')