from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import tweepy
from dotenv import load_dotenv
from textblob import TextBlob
from deep_translator import GoogleTranslator

@csrf_exempt
def peru_vibe(request):
    if request.method == 'GET':
        # Get trends (It's neccesary a PRO account X API v2)
        
        load_dotenv()
        consumer_key = CONSUMER_KEY
        consumer_secret = CONSUMER_SECRET
        access_token = ACCESS_TOKEN
        access_token_secret = ACCESS_TOKEN_SECRET
        trend_names = []

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        woeid_peru = 23424919

        trends = api.get_place_trends(woeid_peru)

        for trend in trends[0]['trends']:
            trend_names.append(trend['name'])
            print(f"Trend: {trend['name']} | Tweet volume: {trend['tweet_volume']}")
        
        # Expected output:
        """
        trend_names = ['Suplente', 'Caute', 'VivoXElRock', 'Panamericana Norte', 'Puente Piedra']
        """
        tweet_text = []
        # Get tweets (It's neccesary a PRO account X API v2)
        
        for trend in trend_names:
            tweets = api.search_tweets(q=trend, count=5, lang='es')
            for tweet in tweets:
                tweet_text.append(tweet)
        
        # Expected output:
        """
        tweet_text = ["De mal en peor, hasta dónde hemos llegado por culpa de la delincuencia, paro de transportes, extorsiones, asesinatos y ahora qué hará el gobierno y el congreso?",
                      "Son 7am y ese noticiero en lugar de informar sobre toda la crítica situación en puente Piedra por el paro está transmitiendo publicidad de la universidad, todo mal",
                      "Terrible lo que se vive en estos momentos en la Panamericana Norte por Ancón, Puente Piedra. Transportistas hacen para dejando varados a cientos de pasajeros.",
                       "Chofer de Anconero fue asesinado por no pagar cupos, inseguridad y caos en la ciudad",
                       "Ante la falta de buses por el paro de transportistas, usuarios intentan ir en las puertas de las unidades llenas de pasajeros en el distrito de Puente Piedra. Lo cual resulta peligroso."]
        """
        translator = GoogleTranslator(source='es', target='en')
        sentiment_counts = {
            "Very Positive": 0,
            "Positive": 0,
            "Neutral": 0,
            "Negative": 0,
            "Very Negative": 0
        }
        for tweet in tweet_text:
            translated = translator.translate(tweet)
            analysis = TextBlob(translated)
            sentiment = get_sentiment(analysis)
            sentiment_counts[sentiment] += 1
            print(f"Tweet: {tweet} | Sentiment: {sentiment}")

        total_tweets = len(tweet_text)
        sentiment_percentages = {key: (count / total_tweets) * 100 for key, count in sentiment_counts.items()}
        return JsonResponse({'sentiment_percentages': sentiment_percentages, 'message': 'Done.'})

def get_sentiment(analysis):
    polarity = analysis.sentiment.polarity
    
    if polarity >= 0.5:
        return "Very Positive"
    elif 0.1 <= polarity < 0.5:
        return "Positive"
    elif -0.1 < polarity < 0.1:
        return "Neutral"
    elif -0.5 <= polarity <= -0.1:
        return "Negative"
    else:
        return "Very Negative"    