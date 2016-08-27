# -*- coding:utf-8 -*-
import sys

import flask
from apiclient.discovery import build
from flask import Flask, request, render_template
from oauth2client.tools import argparser
from config import *

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


def make_json(list):
    print "==result_Json=="

    json_list = []
    for n in list:
        music_name = n[: n.rfind("(") - 1]
        music_code = n[n.rfind("(") + 1:-1]
        json_list.append({'name': music_name, 'id': music_code})
    print json_list
    return flask.jsonify(json_list)


# Search in Youtube and return with JSON parameter
# Key: AIzaSyAcmrNRK5GBEmlUWTFidyqj08m3572jUG8
argparser.add_argument("--q", help="Search term", default="Google")
argparser.add_argument("--max-results", help="Max results", default=25)

def scrapingInYoutube(text):
    # sudo pip install --upgrade google-api-python-client


    # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
    # tab of
    #   https://cloud.google.com/console
    # Please ensure that you have enabled the YouTube Data API for your project.

    def youtube_search(options, keyword):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=YOUTUBE_API_DEVELOPER_KEY)

        # Call the search.list method to retrieve results matching the specified
        # query term.
        options.q = keyword
        search_response = youtube.search().list(
            q=options.q,
            part="id,snippet",
            maxResults=options.max_results
        ).execute()

        videos = []
        channels = []
        playlists = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append('\"%s\" (%s)' % ((search_result["snippet"]["title"]).decode('utf-8'),
                                               search_result["id"]["videoId"]))

        # videos = unicode(videos)
        # videos = videos.split('\n')

        # print "Videos:\n", "\n".join(videos), "\n"

        # Edit tracklist in JSON
        # {name: [name], id: [id]}
        tracklist = videos

        return tracklist

    # argparser.add_argument("--q", help="Search term", default="Google")
    # argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()
    print args
    return youtube_search(args, text)


@app.route('/')
def index():
    return render_template('index.html')


# { type: youtube }, { name: [search] } POST
# else, send "Barking up the wrong tree"
@app.route('/music', methods=['GET'])
def search():
    print "Searching music..."
    # print request.form.get('name')
    # if request.form.get('type') is "youtube":
    result = []
    name = request.args.get('name')
    if name > 0:
        print name
        result = make_json(scrapingInYoutube(name))
    return result


if __name__ == '__main__':
    app.debug = True
    app.run()
