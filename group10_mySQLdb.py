# Please run in Python 3

###===Imports===
import sshtunnel
import MySQLdb
import datetime
import MySQLdb
import tweepy

###=== Removes non-ascii characters for storage in mysql db===
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

###===20 finalist cities===
cities = ["Atlanta", "Austin", "Boston", "Chicago", "Columbus", "Dallas", "Denver", "Indianapolis", "Los Angeles",
"Miami", " Montgomery", "Nashville", "Newark", "New York", "Virginia", "Philadelphia", "Pittsburgh", "Raleigh",
"Toronto", "dc", "D.C.", "Arlington"]

###===API credentials for twitter===
myApi = 'R2vve0QghBEo5YCmcZ7B7lOyB'
sApi = 'lUATUlkyaG1CIVVgtTRlqfrgIUxxBHNKHKShWfK2jRe08jd5xs'
at = '994461904415305729-jO7ZjwBTfsiZpqFaQRYxEZPbczklqsC'
sAt = 'OJyjrHqfR0C7s5YJivW9l3lHq7ZLJj6w8c9A1iKlQSbPb'
auth = tweepy.OAuthHandler(myApi, sApi)
auth.set_access_token(at, sAt)
api = tweepy.API(auth)

###==Access to mysql db===
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='jdmoore7', ssh_password='Py.Coder77$$',
    remote_bind_address=('jdmoore7.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    connection = MySQLdb.connect(
        user='jdmoore7', password='password13',
        host='127.0.0.1', port=tunnel.local_bind_port,
        database='jdmoore7$default',
    )
    c = connection.cursor()

###===Iterates through cities and stores a tweet if the id is not already present.===
    
    for city in cities:
    new = api.search(q='AmazonHQ2 '+city,rpp=100,show_user=True)
    for tweet in new:
        previous = c.execute("SELECT * FROM tweets WHERE twid= %s", [tweet.id_str])
        if previous == 0:
            text = strip_non_ascii(tweet.text)
            date = tweet.created_at.strftime('%m/%d/%Y')
            c.execute("INSERT INTO tweets (twid, content, date, usid, followers, retweet) VALUES (%s, %s, %s, %s, %s, %s)", [tweet.id_str, text, date, tweet.user.id_str, tweet.user.followers_count, tweet.retweet_count])
        else:
            continue

###===Commit changes and close connection===
    conn.commit()
    connection.close()
