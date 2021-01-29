#!/usr/bin/env python3

from flask import Flask
from flask import request, jsonify

from datetime import datetime
import pickle, copy, random

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

# Count of added commands from last current mashup check
feedback_given = 0
last_length = 0

# Undo check
undo_used = False

@app.route('/', methods=['POST'])
def main():
    global mashups
    global graph_mashups
    global cursor
    global paused
    global feedback_given
    global last_length
    global undo_used

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
        
        now = int(datetime.now().timestamp())
        print('[INFO] New mashup session initiated at ' + str(now))

        mashups.append([])
        cursor = mashups[-1]
        confirm_init()
        feedback_given = 0
        last_length = 0
        undo_used = False
    
    if intent == 'add_command':
        now = int(datetime.now().timestamp())
        print('[INFO] Command added at ' + str(now))

        cursor.append(data['queryResult']['parameters'])
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(mashups[-1]))
            feedback_given += m.graph.number_of_nodes() - last_length
            last_length = m.graph.number_of_nodes()

            ret['fulfillmentText'] = speak_add_command(m, False if feedback_given > 4 else True)

            if feedback_given > 4:
                now = int(datetime.now().timestamp())
                print('[INFO] Feedback suggested at ' + str(now))

                ret["outputContexts"] = [
                    {"name": "{}/contexts/add_command-followup".format(data['session']),
                     "lifespanCount": 2}
                ]
                
                ret["fulfillmentText"] += "Great. Before moving on to the next step, would you like to check the current progress of your mashup?"

                feedback_given = 0

        except Exception as e:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            cursor.pop()
            ret = {
                "fulfillmentText": "Oops, I failed to process your input. Could you rephrase it?",
            }

            return jsonify(ret)

    if intent == 'undo_command':
        now = int(datetime.now().timestamp())
        print('[INFO] Command undone at ' + str(now))

        feedback_given += 1
        last_length -= 1

        try:
            cursor.pop()
        except IndexError as e:
            print('[Error] Failed to pop a command - ' + str(e))
            ret['fulfillmentText'] = 'Sorry, you cannot undo when you did not add any commands.'

            return jsonify(ret)

        if not undo_used:
            undo_used = True
            ret['fulfillmentText'] = 'Sure, the last command has been undone. Please tell me commands you want to add.'
        else:
            ret_str = [
                'Removing the last action.',
                'Undoing the last action.'
            ]
            ret['fulfillmentText'] = random.choice(ret_str)

    if intent == 'pause_add_command':
        now = int(datetime.now().timestamp())
        print('[INFO] Paused at ' + str(now) + ' - ' + str(cursor))
        outputContexts = data['queryResult']['outputContexts']
        for context in outputContexts:
            context['lifespanCount'] = 0
        
        ret['outputContexts'] = outputContexts
        paused = True
    
    if intent == 'resume_add_command':
        now = int(datetime.now().timestamp())
        print('[INFO] Resumed at ' + str(now) + ' - ' + str(cursor))
        paused = False

    if intent == 'finish_add_command':
        # Check if the mashup is empty
        if len(cursor) == 0:
            ret = {
                "fulfillmentText": "Umm... Nothing has been added.",
                "payload": {
                    'google': {'expectUserResponse': False}
                }
            }

            return jsonify(ret)
        
        if feedback_given > 2:
            now = int(datetime.now().timestamp())
            print('[INFO] Feedback suggested at ' + str(now))
            
            outputContexts = data['queryResult']['outputContexts']
            for context in outputContexts:
                if 'finish_add_command-followup' not in context['name']:
                    context['lifespanCount'] = 0
            
            ret['outputContexts'] = outputContexts
            ret["fulfillmentText"] = "Okay, it's almost ready. Before I deploy your mashup, do you want to check it out?"

            return jsonify(ret)
        else:
            ret['payload'] = {
                'google': {'expectUserResponse': False}
            }

        now = int(datetime.now().timestamp())
        f = open('dump/multi-' + str(now) + '.bin', 'wb+')
        pickle.dump(cursor, f)

        print('[INFO] New mashup created at ' + str(now) + ' - ' + str(cursor))

        f.close()
        cursor = None

        # Build a mashup from dump file
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(mashups[-1]))

            nx.draw_networkx(m.graph)
            plt.savefig('dump/multi-' + str(now) + '.png')
            plt.close('all')
                    
            # If not redundant
            graph_mashups.append(m)

        except Exception as e:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            ret = {
                "fulfillmentText": "Sorry, something strange has occurred while processing your input.",
                "payload": {
                    'google': {'expectUserResponse': False}
                }
            }

            return jsonify(ret)
        
        # Resetting contexts
        outputContexts = data['queryResult']['outputContexts']
        for context in outputContexts:
            context['lifespanCount'] = 0
        
        ret['outputContexts'] = outputContexts

    if intent == 'finish_add_command - no' or intent == 'finish_add_command - yes - yes':
        now = int(datetime.now().timestamp())
        f = open('dump/multi-' + str(now) + '.bin', 'wb+')
        pickle.dump(cursor, f)

        print('[INFO] New mashup created at ' + str(now) + ' - ' + str(cursor))

        f.close()
        cursor = None

        # Build a mashup from dump file
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(mashups[-1]))

            nx.draw_networkx(m.graph)
            plt.savefig('dump/multi-' + str(now) + '.png')
            plt.close('all')
                    
            graph_mashups.append(m)

        except Exception as e:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            ret = {
                "fulfillmentText": "Sorry, something strange has occurred while processing your input.",
                "payload": {
                    'google': {'expectUserResponse': False}
                }
            }

            return jsonify(ret)
        
        # Resetting contexts
        outputContexts = data['queryResult']['outputContexts']
        for context in outputContexts:
            context['lifespanCount'] = 0
        
        ret['outputContexts'] = outputContexts

    if intent == 'finish_add_command - yes':
        now = int(datetime.now().timestamp())
        print('[INFO] Final feedback is provided at ' + str(now))
        f = open('dump/multi-' + str(now) + '-cur' + '.bin', 'wb+')
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

            fulfillmentText = speak_mashup(m) + 'Do you want to deploy your mashup?</speak>'
            ret['fulfillmentText'] = fulfillmentText
            feedback_given = 0 
        except:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            ret = {
                "fulfillmentText": "Sorry. I got an error while checking the mashup command.",
                "payload": {
                    'google': {'expectUserResponse': False}
                }
            }

            return jsonify(ret)
    
    if intent == 'current_mashup' or intent == 'add_command - yes':
        now = int(datetime.now().timestamp())
        print('[INFO] Current feedback is provided at ' + str(now))

        now = int(datetime.now().timestamp())
        f = open('dump/multi-' + str(now) + '-cur' + '.bin', 'wb+')
        pickle.dump(cursor, f)
        f.close()

        # Build a mashup from dump file
        try:
            m = Mashup()
            m.init_list(copy.deepcopy(cursor))

            fulfillmentText = speak_mashup(m) + " Tell me if you have more to add, or just say I'm done.</speak>"

            ret['fulfillmentText'] = fulfillmentText
            feedback_given = 0

        except Exception as e:
            print('[Error] Failed to instantiate the mashup - ' + str(e))
            ret = {
                "fulfillmentText": "Sorry. I got an error while checking the mashup command.",
                "payload": {
                    'google': {'expectUserResponse': False}
                }
            }

            return jsonify(ret)

    
    return jsonify(ret)



if __name__ == "__main__":
    # Let's prefer HTTP for development, and reverse-proxy it to HTTPS for production.
    # app.run(host='0.0.0.0', port=443, ssl_context=('server.crt', 'server.key'))
    app.run(host='0.0.0.0', port=9000)
