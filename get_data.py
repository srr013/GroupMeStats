
#{'attachments': [], 'avatar_url': 'https://i.groupme.com/750x750.jpeg.62819788722a4584a4db8ba812e622c5', 'created_at': 1546720335,
# 'favorited_by': [], 'group_id': '41856287', 'id': '154672033522145700', 'name': 'Scott Rossignol', 'sender_id': '9406803',
# 'sender_type': 'user', 'source_guid': '4683A95A-841F-497B-A1B2-945828A43F31', 'system': False, 'text': 'Mer’s company holiday party. Just there Friday and Saturday', 'user_id': '9406803'}

from flask import session
from groupy.client import Client

def fetch_data():
    if 'client_key' not in session:
        #do some sort of error
        pass
    else:
        client = Client.from_token(session['client_key'])
    return client

def generate_statistics(groupID):
    # my_groups = client.groups.list();
    # for group in my_groups:
    #     print(group.name)
    client = fetch_data()
    my_groups = []
    for group in client.groups.list_all():
        my_groups.append(group)

    messages = my_groups[groupID-1].messages.list_all()
    users = []
    num_messages = 0
    for message in messages:
        if message.data['sender_id'] != 'calendar' and message.data['sender_id'] != 'system':
            num_messages +=1
            print(num_messages)
            sender = None
            for user in users:
                if user['id'] == message.data['sender_id']:
                    sender = user
                    sender['num_posts'] +=1
            if not sender:
                   sender = {'name': message.data['name'], 'id': message.data['sender_id'], 'num_favorites': 0, 'num_favorited': 0, 'num_favorited_messages': 0,
                             'num_posts':0}
                   users.append(sender)
            if message.data['favorited_by']:
                sender['num_favorited_messages'] += 1
            for favorite in message.data['favorited_by']:
                sender['num_favorites'] += 1
                for user in users:
                    if user['id'] == favorite:
                        user['num_favorited'] += 1

    leaderboard = {'group_name': my_groups[groupID-1].name, 'most_hearts_given': [None, 0], 'most_hearts_received':[None,0], 'favorites_per_favorited_post': [None,0]}
    for user in users:
        if user['num_favorites'] > leaderboard['most_hearts_given'][1]:
            leaderboard['most_hearts_received'] = [user['name'], user['num_favorites']]
        if user['num_favorited'] > leaderboard['most_hearts_given'][1] :
            leaderboard['most_hearts_given'] = [user['name'], user['num_favorited']]
        if user['num_posts'] > 0:
            user['hearts_per_post'] = user['num_favorites'] / user['num_posts']
        else:
            user['hearts_per_post'] = 0
        if user['num_favorited_messages'] > 0:
            user['favorites_per_favorited_post'] = user['num_favorites'] / user['num_favorited_messages']
            if user['favorites_per_favorited_post'] > leaderboard['favorites_per_favorited_post'][1]:
                leaderboard['favorites_per_favorited_post'] = [user['name'], user['favorites_per_favorited_post']]

    print(users)
    print(leaderboard)
    return [users, leaderboard]

