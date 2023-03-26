import sys
import os
from dotenv import load_dotenv
import requests
import re

load_dotenv()
api_key = os.getenv('API_KEY')
max_results = '100'


def get_comments(video_id):
    text = 'plainText'
    part = 'snippet'
    order = 'relevance'
    next_token = ''
    max_page_num = 100

    comments = []
    page, counter = 1, 1

    while (True):
        url = f"https://www.googleapis.com/youtube/v3/commentThreads?&key={api_key}&part={part}&videoId={video_id}&maxResults={max_results}&order={order}&pageToken={next_token}"
        response = requests.get(url)
        data = response.json()

        for item in data['items']:
            top_level_comment = item['snippet']['topLevelComment']['snippet']
            comment_text = top_level_comment['textDisplay']
            comments.append(comment_text)
            counter += 1

        counter = 1

        if page > max_page_num:
            break
        elif 'nextPageToken' in data:
            next_token = data['nextPageToken']
            page += 1
        else:
            break

    return comments


def cleaner(data):
    mod_data = re.sub(r"(\t|\n|[^a-zA-Z0-9])+", " ", data)
    return (mod_data)


def main():
    video_url = sys.argv[-1]
    video_id = video_url.split("https://youtu.be/")[-1]
    comments = get_comments(video_id)

    with open("comments.txt", "w") as f:
        c = 0
        for comment in comments:
            f.write(f"{comment}")
            c += 1

    with open("comments.txt", "r") as f:
        string = f.read()
        result = cleaner(string)

    with open("comments.txt", "w") as f:
        f.write(result)


if __name__ == '__main__':
    main()
