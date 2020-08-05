#!/usr/bin/env python3

from flask import Flask
from flask import request, jsonify

from datetime import datetime
import pickle, copy

from mashup import *
from ont2nl import *
import matplotlib.pyplot as plt
import networkx as nx

app = Flask(__name__)


mashups = []
graph_mashups = []
cursor = None

@app.route('/', methods=['POST'])
def main():
    global mashups
    global graph_mashups
    global cursor

    data = request.get_json()
    ret = {}

    # check user intent
    intent = data['queryResult']['intent']['displayName']
    
    if intent == 'new_mashup':
        now = int(datetime.now().timestamp())
        print('[INFO] New mashup session initiated at ' + str(now) + ' - ' + str(cursor))

        mashups.append([])
        cursor = mashups[-1]
    
    if intent == 'finish_add_command':
        cursor.append(data['queryResult']['parameters'])

        now = int(datetime.now().timestamp())
        f = open('dump/' + str(now) + '-cur' + '.bin', 'wb+')
        pickle.dump(cursor, f)
        f.close()

        # Build a mashup from dump file
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(cursor))

            ret = {
                "outputContexts": [
                    {"name": "{}/contexts/add_command-followup".format(data['session']),
                     "lifespanCount": 2}
                ],
            }

            fulfillmentText = 'Okay, your mashup is ' + speak_mashup(m) + 'Do you want to generate your mashup?'
            ret['fulfillmentText'] = fulfillmentText

        except Exception as e:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            cursor.pop()
            ret = {
                "fulfillmentText": "Oops, your input is not yet supported by the agent. Could you try with other commands?",
            }

            return jsonify(ret)

    if intent == 'add_command - yes':
        now = int(datetime.now().timestamp())
        f = open('dump/' + 'single-yes-' + str(now) + '.bin', 'wb+')
        pickle.dump(cursor, f)

        print('[INFO] New mashup created at ' + str(now) + ' - ' + str(cursor))

        f.close()
        cursor = None

        # Build a mashup from dump file
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(mashups[-1]))

            nx.draw_networkx(m.graph)
            plt.savefig('dump/' + str(now) + '.png')
            plt.close('all')
                    
            # If not redundant
            graph_mashups.append(m)

        except Exception as e:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            ret = {
                "fulfillmentText": "Sorry, something strange has occurred while processing your input.",
                "expectUserResponse": False
            }

            return jsonify(ret)
        
        # Resetting contexts
        outputContexts = data['queryResult']['outputContexts']
        for context in outputContexts:
            context['lifespanCount'] = 0
        
        ret['outputContexts'] = outputContexts

    if intent == 'add_command - no':
        now = int(datetime.now().timestamp())
        f = open('dump/' + 'single-no-' + str(now) + '.bin', 'wb+')
        pickle.dump(cursor, f)

        print('[INFO] Mashup creation aborted at ' + str(now) + ' - ' + str(cursor))

        f.close()
        cursor = None
        
        # Resetting contexts
        outputContexts = data['queryResult']['outputContexts']
        for context in outputContexts:
            context['lifespanCount'] = 0
        
        ret['outputContexts'] = outputContexts
    
    return jsonify(ret)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=444, ssl_context=('server.crt', 'server.key'))
