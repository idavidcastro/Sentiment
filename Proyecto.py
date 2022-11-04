import dash
from textblob import TextBlob
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import time

api_key = 'wUXAAynkSntYwfxRzBqCqGIUi'
api_secret = 'JWwjsXm1f5FKl4uccUTFrnOzb6vl5YhL2SaQfzy9KHYa0KcOUm'
access_token = '1579570339968913432-aiNFrGp92WRylDlnmj5SEzKXlO2BwD'
access_token_secret = '4rwNM0E64sVfWuL5H8jkLNspdYw69jPkSIPYdPMcrXX1B'
bearer_token='AAAAAAAAAAAAAAAAAAAAALEgiAEAAAAAlEqDwkRGiNNlato%2BjqPfP1slewg%3DK9p5sk9jgGP5iFUFCJBUa25ih1Pa7pbmZrsOozXeHWjltlcH1p'

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print('---------------------')
print('polaridad de tweets sobre un tema (con gráfico)')
print('---------------------')

search_term = input('Termino a evaluar: ')
tweet_amount = int(input('Cantidad de tweets: '))

def porcentaje(part, whole):
    return 100*float(part)/float(whole)

tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang='es').items(tweet_amount)

polaridad=0
positive=0
neutral=0
negative=0

for tweet in tweets:
    final_text = tweet.text.replace('RT','')
    if final_text.startswith(' @'):
        position=final_text.index(':')
        final_text=final_text[position+2:]
    if final_text.startswith('@'):
        position=final_text.index(' ')
        final_text=final_text[position+2:]
    analysis= TextBlob(final_text)
    tweet_polarity=analysis.polarity
    if tweet_polarity > 0:
        positive += 1
    elif tweet_polarity < 0:
        negative += 1
    else:
        neutral += 1
    polaridad += tweet_polarity

positive = porcentaje(positive, tweet_amount)
neutral = porcentaje(neutral, tweet_amount)
negative = porcentaje(negative, tweet_amount)

positive= format(positive, '.2f')
neutral= format(neutral, '.2f')
negative= format(negative, '.2f')

labels =['Positivos ['+str(positive)+'%]', 'Neutros [' +str(neutral) + '%]', 'Negativos [' + str(negative) +' %]']
sizes =[positive, neutral, negative]
colors =['green','gold', 'red']
patches, texts =plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()

print('---------------------')
print('información de cuenta de twitter')
print('---------------------')

user=input('Usuario de twitter: ')
limit =int(input('Limite de tweets: '))

tweets_user=tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)

myuser=api.get_user(screen_name=user)

print(myuser.screen_name)
print(myuser.followers_count)
#print(myuser.retweet_count)

columns =['Usuario', 'Tweet', 'Fecha']
datos=[]

for mytweets in tweets_user:
    datos.append([mytweets.user.screen_name, mytweets.full_text, mytweets.created_at])

df=pd.DataFrame(datos, columns=columns)
print(df)
df.to_csv('Información de cuenta de Twitter')

print('---------------------')
print('busqueda de opiniones sobre un tema en específico')
print('---------------------')

palabra_clave=input('Termino a evaluar: ')
limit =int(input('Limite de Tweets: '))

tweets_tema=tweepy.Cursor(api.search_tweets, q=palabra_clave, count=100, tweet_mode='extended').items(limit)


columns =['Id de usuario ', 'Usuario', 'Nombre', 'Tweet', 'Fecha', 'Seguidores', 'Lugar']
datos=[]

for mytweets in tweets_tema:
    
    datos.append([mytweets.user.id, mytweets.user.screen_name, mytweets.user.name, mytweets.full_text, mytweets.created_at, mytweets.user.followers_count, mytweets.user.location])
    

df=pd.DataFrame(datos, columns=columns)
print(df)
df.to_csv('Busqueda de opiniones sobre un tema en específico')

print('---------------------')
print('busqueda de tweets en tiempo real')
print('---------------------')

keywords_ = input('Palabra claves: ')

class MyStream(tweepy.StreamingClient):

    def on_connect(self):

        print("Connected")

    def on_tweet(self, _tweet):

        if _tweet.referenced_tweets == None:
            print(_tweet.text)

            time.sleep(0.5)
        
stream = MyStream(bearer_token=bearer_token)

for _term in keywords_:
    stream.add_rules(tweepy.StreamRule(_term))

stream.filter(tweet_fields=["referenced_tweets"])

#---------------------
#publicar tweets
#---------------------

# api.update_status("")