#!/usr/bin/env python3

from flask import Flask
from flask import request, jsonify

from datetime import datetime
import pickle, copy

from mashup import *
from ont2nl import *
from ont2confirm import *
import matplotlib.pyplot as plt
import networkx as nx

app = Flask(__name__)


mashups = []
graph_mashups = []
cursor = None
paused = False

# Final feedback
feedback_given = False

@app.route('/', methods=['POST'])
def main():
    global mashups
    global graph_mashups
    global cursor
    global paused
    global feedback_given

    data = request.get_json()
    ret = {}

    # check user intent
    intent = data['queryResult']['intent']['displayName']
    
    if intent == 'new_mashup':
        if paused:
            ret = {
                "fulfillmentText": "It seems you haven't finished making a mashup, please resume it."
            }
            outputContexts = data['queryResult']['outputContexts']
            
            # Reset contexts
            for context in outputContexts:
                context['lifespanCount'] = 0
        
            ret['outputContexts'] = outputContexts
        
        mashups.append([])
        cursor = mashups[-1]
        confirm_init()
    
    if intent == 'add_command':
        cursor.append(data['queryResult']['parameters'])
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(mashups[-1]))
            feedback_given = False

            ret['fulfillmentText'] = speak_add_command(m)
            
        except Exception as e:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            cursor.pop()
            ret = {
                "fulfillmentText": "Oops, your input is not yet supported by the agent. Could you try with other commands?",
            }

            return jsonify(ret)


    if intent == 'undo_command':
        feedback_given = False
        cursor.pop()

    if intent == 'pause_add_command':
        print('[INFO] Paused - ' + str(cursor))
        outputContexts = data['queryResult']['outputContexts']
        for context in outputContexts:
            context['lifespanCount'] = 0
        
        ret['outputContexts'] = outputContexts
        paused = True
    
    if intent == 'resume_add_command':
        print('[INFO] Resumed - ' + str(cursor))
        paused = False

    if intent == 'finish_add_command':
        # Check if the mashup is empty
        if len(cursor) == 0:
            ret = {
                "fulfillmentText": "Umm... Nothing has been added.",
                "expectUserResponse": False
            }

            return jsonify(ret)
        
        if not feedback_given:
            ret = {
                "outputContexts": [
                    {"name": "{}/contexts/finish_add_command-followup".format(data['session']),
                     "lifespanCount": 2}
                ],
                "fulfillmentText": "Before I generate your mashup, do you want to check your current mashup?"
            }

            return jsonify(ret)

        now = int(datetime.now().timestamp())
        f = open('dump/' + str(now) + '.bin', 'wb+')
        pickle.dump(cursor, f)

        print('[INFO] New mashup created - ' + str(cursor))

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

    if intent == 'finish_add_command - no' or intent == 'finish_add_command - yes - yes':
        now = int(datetime.now().timestamp())
        f = open('dump/' + str(now) + '.bin', 'wb+')
        pickle.dump(cursor, f)

        print('[INFO] New mashup created - ' + str(cursor))

        f.close()
        cursor = None

        # Build a mashup from dump file
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(mashups[-1]))

            nx.draw_networkx(m.graph)
            plt.savefig('dump/' + str(now) + '.png')
            plt.close('all')
                    
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

    if intent == 'finish_add_command - yes':
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
                    {"name": "{}/contexts/finish_add_command-yes-followup".format(data['session']),
                     "lifespanCount": 2}
                ],
            }

            fulfillmentText = speak_mashup(m) + 'Do you want me to generate your mashup?'
            ret['fulfillmentText'] = fulfillmentText
            feedback_given = True 
        except:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            ret = {
                "fulfillmentText": "Sorry. I got an error while checking the mashup command.",
                "expectUserResponse": False
            }

            return jsonify(ret)
    
    if intent == 'current_mashup':
        now = int(datetime.now().timestamp())
        f = open('dump/' + str(now) + '-cur' + '.bin', 'wb+')
        pickle.dump(cursor, f)
        f.close()

        # Build a mashup from dump file
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(cursor))

            fulfillmentText = speak_mashup(m) + 'Is there anything you want to add?'

            ret['fulfillmentText'] = fulfillmentText
            feedback_given = True 
        except Exception as e:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            ret = {
                "fulfillmentText": "Sorry. I got an error while checking the mashup command.",
                "expectUserResponse": False
            }

            return jsonify(ret)

    
    return jsonify(ret)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, ssl_context=('server.crt', 'server.key'))
