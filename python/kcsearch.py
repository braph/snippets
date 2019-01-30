#!/usr/bin/python3

import json
import requests
from itertools import count, takewhile

board_url = 'https://kohlchan.net/%s/%i.json'
thread_url = 'https://kohlchan.net/%s/res/%i.html'

def search_board_for(board, search):
    search = search.lower()

    board_urls = map(lambda p: board_url % (board, p), count(1))
    responses = takewhile(lambda r: r.status_code == 200, map(requests.get, board_urls))
    board_pages = map(lambda r: json.loads(r.text), responses)

    for board_page in board_pages:
        for thread in board_page['threads']:
            for post in thread['posts']:
                if search in post.get('com', '').lower():
                    print('Found <%s> in %s:' % (search, thread_url % (board, post['no'])))
                    print('>', post['com'], '\n')
