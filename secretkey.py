
from flask import (
    Blueprint, render_template, request, session,
)
from . import get_data

secretkey = Blueprint('secretkey', __name__, url_prefix='/')


@secretkey.route('/', methods=["GET","POST"])
def show():
    """Submits the secret key into get_data"""
    if 'client key' not in session and request.method == "POST":

        session['client_key'] = request.form['key']
        client = get_data.fetch_data()
        num = 1
        my_groups = []
        for group in client.groups.list_all():
            #print(group)
            my_groups.append((group, group.name, num))
            num +=1
        #results = get_data.generate_statistics(client)
        #print(my_groups)
        return render_template('statistics/index.html', results=my_groups)
    else:
        return render_template('statistics/secretkey.html')

@secretkey.route('/groupnum=<int:groupID>', methods=["GET"])
def display_stats(groupID):
    results = get_data.generate_statistics(groupID)
    return render_template('statistics/groupstats.html', results=results)