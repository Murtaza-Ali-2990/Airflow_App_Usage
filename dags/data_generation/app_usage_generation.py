import json
import random as rand
import os

# List of users
users = ['vinit@tribes.ai', 'guilermo@tribes.ai', 'christian@tribes.ai', 'elly@tribes.ai', 'murtaza@tribes.ai']

# List of devices and their operating system
devices = [
    {
        'os': 'iOS',
        'brand': 'Apple'
    },
    {
        'os': 'Android',
        'brand': 'Samsung'
    },
    {
        'os': 'Android',
        'brand': 'MI'
    }
]

# List of apps which may be on the user's phone
usages = [
    {
        'app_name': 'Slack',
        'app_category': 'communication'
    },
    {
        'app_name': 'Gmail',
        'app_category': 'communication'
    },
    {
        'app_name': 'Jira',
        'app_category': 'task_management'
    },
    {
        'app_name': 'Chrome',
        'app_category': 'web_browser'
    },
    {
        'app_name': 'Spotify',
        'app_category': 'entertainment_music'
    }
]

# Function which generates the app usages present in data['usages']
def generate_app_usage_stats() -> list:
    number_of_apps = rand.randint(1, len(usages))
    app_usage_stats = rand.sample(usages, number_of_apps)
    sum_app_usage = 480
    for app_usage in app_usage_stats:
        app_usage['minutes_used'] = rand.randint(0, min(sum_app_usage, 180))
        sum_app_usage -= app_usage['minutes_used']
    return app_usage_stats

# Funtion which generates the .json file for each user
def generate_user_data(current_date: str, filepath: str):
    
    app_usage_user_data = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user
        user_data['usages_date'] = current_date
        user_data['device'] = devices[rand.randint(0, 2)]
        user_data['usages'] = generate_app_usage_stats()
        app_usage_user_data.append(user_data)
    
    # Saving data to the "userdata" directory
    os.makedirs(filepath + '/userdata', exist_ok = True)
    with open(filepath + '/userdata/USERDATA-' + current_date + '.json', 'w') as fp:
        json.dump(app_usage_user_data, fp)

