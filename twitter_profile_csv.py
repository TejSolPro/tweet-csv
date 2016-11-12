import tweepy
import csv
import webbrowser
import time


def get_all_tweets(tweepy_user):
    alltweets = []

    screen_name = input(
        'Enter the screenname of the profile : @')

    new_tweets = tweepy_user.user_timeline(screen_name=screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        print ("getting tweets before " + str(oldest))

        new_tweets = tweepy_user.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest)

        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1

        print ("..." + str(len(alltweets)) + ' tweets downloaded so far')

        outtweets = [[tweet.id_str, tweet.created_at,
                      tweet.text.encode("utf-8")] for tweet in alltweets]

        with open('%s_tweets.csv' % screen_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text"])
            writer.writerows(outtweets)


def get_auth():
    print('To paste -> Ctrl+Shift+V \n')
    consumer_token = input('Enter your consumer token :')
    consumer_secret = input('Enter your consumer secret :')

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url()
        print ('\nOpen this link : ' + redirect_url)
        time.sleep(1)
        webbrowser.open(redirect_url)

    except tweepy.TweepError:
        print ('Error! Failed to get auth_url.')

    time.sleep(2)
    pin = input("Enter Authorization Pin :").strip()
    auth.get_access_token(verifier=pin)

    tweepy_user = tweepy.API(auth)

    get_all_tweets(tweepy_user)


if __name__ == '__main__':
    get_auth()
