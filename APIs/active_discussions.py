import requests

from plotly.graph_objs import Bar
from plotly import offline
from operator import itemgetter

# Make an API call and store the response.
#url = 'https://hacker-news.firebaseio.com/v0/item/19155826.json'
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
links, comments, titles = [], [], []
for submission_id in submission_ids[:30]:
    # Make a separate API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Build a dictionary for each article.
    try:    
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
        }
    except KeyError:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': 0
        }
    finally:
        submission_dicts.append(submission_dict)
    
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                                reverse=True)
for submission_dict in submission_dicts:
    links.append(submission_dict['hn_link'])
    comments.append(submission_dict['comments'])
    titles.append(submission_dict['title'])

# Make visualization.
data = [{
    'type': 'bar',
    'x': links,
    'y': comments,
    'hovertext': titles,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
}]

my_layout = {
    'title': 'Most-Commented Articles on HackerNews',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Article',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': 'Comments',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='active_discussions.html')