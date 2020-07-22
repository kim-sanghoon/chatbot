import networkx as nx
import pickle

from identifier2ont import *


class Node:
    
    def __init__(self):
        # Empty node initialization
        self.raw = None
        self.category = ''
    

    def __repr__(self):
        return self.category

    
    def __str__(self):
        return self.category
    
    
    def fillTrigger(self, cmd):
        # Fill the node with trigger information
        self.raw = cmd

        # Special 'turn' handling
        if cmd['action'] == 'turn':
            if 'on' in cmd['params']:
                cmd['action'] = 'enable'
            else:
                cmd['action'] = 'disable'

        
        if cmd['pos_object'] != '':
            self.category = id2trigger(cmd['pos_object'], cmd['pos_action'])
            return
        
        if cmd['pos_object'] == '' and cmd['pos_action'] == '':
            if cmd['time'] != '':
                self.category = 'EveryTimeTrigger'
            else:
                raise RuntimeError('[Error] Could not infer the trigger.')
    

    def fillAction(self, cmd):
        # Fill the node with action information
        self.raw = cmd

        # Special 'turn' handling
        if cmd['action'] == 'turn':
            if 'on' in cmd['params']:
                cmd['action'] = 'enable'
            else:
                cmd['action'] = 'disable'
        
        self.category = id2action(cmd['object'], cmd['action'])
        return


class Mashup:
    
    def __init__(self, fname=None):
        # Generate a new, empty mashup
        self.graph = nx.DiGraph()
        self.first = None
        self.last = None

        if fname is not None:
            # Generate mashup from pickle if fname is given
            f = open(fname, 'rb')
            raw = pickle.load(f)

            for cmd in raw:
                print(cmd)
                self.addCommand(cmd)

            f.close()
    
    def init_list(self, raw):
        self.graph = nx.DiGraph()
        self.first = None
        self.last = None

        for cmd in raw:
            print(cmd)
            self.addCommand(cmd)

    
    def merge(self, m):
        def traverse(n):
            for subnode in m.graph.neighbors(n):
                self.graph.add_node(subnode)
                self.graph.add_edge(n, subnode)
                traverse(subnode)
        
        for second in m.graph.neighbors(m.first):
            self.graph.add_node(second)
            self.graph.add_edge(self.first, second)
            traverse(second)

    
    def addCommand(self, cmd):
        pos = cmd['position'] # Remember that pos can contain multiple items!

        if 'first' in pos:
            self._add_first(cmd)
        elif 'then' in pos:
            self._add_last(cmd)
        elif 'last' in pos:
            self._add_last(cmd)
        elif 'after' in pos:
            if 'that' in cmd['pos_object']:
                self._add_last(cmd)
            else:
                raise NotImplementedError
        elif 'before' in pos:
            if 'that' in cmd['pos_object']:
                self._add_first(cmd)
            else:
                raise NotImplementedError
        else:
            if cmd['time'] != '':
                cmd['position'].append('at')
            
            self._add_last(cmd)


    def _add_first(self, cmd):
        if 'if' in cmd['position']:
            if 'success' in cmd['pos_object'] or 'fail' in cmd['pos_object']:
                raise RuntimeError('[Error] Consequential commands cannot be added in first.')
            else:
                trigger, action, action_2 = Node(), Node(), None
                trigger.fillTrigger(cmd)

                if len(cmd['object']) > 1:
                    action_2 = Node()
                    one, another = cmd['object'][1], cmd['object'][0]

                    cmd['object'] = one
                    action.fillAction(cmd)
                    cmd['object'] = another
                    action_2.fillAction(cmd)
                else:
                    cmd['object'] = cmd['object'][0]
                    action.fillAction(cmd)

                self.graph.add_node(trigger)
                self.graph.add_node(action)

                if action_2 is not None:
                    self.graph.add_node(action_2)
                    self.graph.add_edge(trigger, action_2)
                    self.graph.add_edge(action_2, action)
                else:
                    self.graph.add_edge(trigger, action)


                if self.first is not None:
                    self.graph.add_edge(action, self.first)
                self.first = trigger

                if self.last is None:
                    self.last = action
        else:
            action, action_2 = Node(), None
            
            if len(cmd['object']) > 1:
                action_2 = Node()
                one, another = cmd['object'][1], cmd['object'][0]

                cmd['object'] = one
                action.fillAction(cmd)
                cmd['object'] = another
                action_2.fillAction(cmd)
            else:
                cmd['object'] = cmd['object'][0]
                action.fillAction(cmd)

            self.graph.add_node(action)

            if action_2 is not None:
                self.graph.add_node(action_2)
                self.graph.add_edge(action_2, action)

            if self.first is not None:
                self.graph.add_edge(action, self.first)
            self.first = action

            if self.last is None:
                self.last = action


    def _add_last(self, cmd):
        if 'if' in cmd['position'] or 'at' in cmd['position']:
            if 'success' in cmd['pos_object'] or 'fail' in cmd['pos_object']:
                if self.last is None:
                    raise RuntimeError('[Error] Consequential commands cannot be added in first.')

                action, action_2 = Node(), None
            
                if len(cmd['object']) > 1:
                    action_2 = Node()
                    one, another = cmd['object'][1], cmd['object'][0]
                    
                    cmd['object'] = one
                    action.fillAction(cmd)
                    cmd['object'] = another
                    action_2.fillAction(cmd)
                else:
                    cmd['object'] = cmd['object'][0]
                    action.fillAction(cmd)

                self.graph.add_node(action)

                if action_2 is not None:
                    self.graph.add_node(action_2)
                    self.graph.add_edge(action_2, action)

                if 'fail' in cmd['pos_object'] and 'Action' in self.last.category:
                    trig = list(self.graph.predecessors(self.last))[0]
                    self.graph.add_edge(trig, action)
                else:
                    self.graph.add_edge(self.last, action)

                if 'success' in cmd['pos_object']:
                    self.last = action

            else:
                trigger, action, action_2 = Node(), Node(), None
                trigger.fillTrigger(cmd)

                if len(cmd['object']) > 1:
                    action_2 = Node()
                    one, another = cmd['object'][1], cmd['object'][0]

                    cmd['object'] = one
                    action.fillAction(cmd)
                    cmd['object'] = another
                    action_2.fillAction(cmd)
                else:
                    cmd['object'] = cmd['object'][0]
                    action.fillAction(cmd)

                self.graph.add_node(trigger)
                self.graph.add_node(action)

                if action_2 is not None:
                    self.graph.add_node(action_2)
                    self.graph.add_edge(trigger, action_2)
                    self.graph.add_edge(action_2, action)
                else:
                    self.graph.add_edge(trigger, action)

                if self.first is None:
                    self.first = trigger

                if self.last is not None:
                    self.graph.add_edge(self.last, action)
                self.last = action
        else:
            action, action_2 = Node(), None
            
            if len(cmd['object']) > 1:
                action_2 = Node()
                one, another = cmd['object'][1], cmd['object'][0]
                
                cmd['object'] = one
                action.fillAction(cmd)
                cmd['object'] = another
                action_2.fillAction(cmd)
            else:
                cmd['object'] = cmd['object'][0]
                action.fillAction(cmd)

            self.graph.add_node(action)

            if action_2 is not None:
                self.graph.add_node(action_2)
                self.graph.add_edge(action_2, action)

            if self.first is None:
                self.first = action

            if self.last is not None:
                self.graph.add_edge(self.last, action)
            self.last = action

    
