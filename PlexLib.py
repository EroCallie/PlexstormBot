#!/usr/bin/env python
init_done = False

callbacks = {"on_message": [], "on_messagedeleted": [], "on_viewercountupdate": [], "on_milestoneupdate": [],
             "on_milestonereached": [], "on_tip": [], "on_tipsuggestions": [], "on_streamstart": [],
             "on_streamupdate": [], "on_streamend": [], "on_streamerupdate": [], "on_experiencereceived": [],
             "on_newreward": [], "on_followedstreamstart": [], "on_userupdate": [], "on_creditbalanceupdate": []}
outgoing_messages = []
tip_menu = None
milestones = {}
stream_info = {}


class Auth:
    def __init__(self, name):
        self.__auth_token_bot = ""
        self.__auth_token_streamer = ""

    def set_token(self, t_type, token):
        if t_type == "bot":
            self.__auth_token_bot = token
        elif t_type == "streamer":
            self.__auth_token_streamer = token

    def get_token(self, t_type):
        if __name__:  # == "__main__":
            if t_type == "bot":
                return self.__auth_token_bot
            elif t_type == "streamer":
                return self.__auth_token_streamer


def register_callback(name, function):
    callbacks[name].append(function)


def retrieve_callbacks(name):
    return callbacks[name]


def send_message(channel, message):
    msg_obj = {'channel': channel, 'message': message}
    outgoing_messages.append(msg_obj)


def retrieve_message():
    if len(outgoing_messages) > 0:
        out = outgoing_messages.pop(0)
        return out


def retrieve_all_messages():
    global outgoing_messages
    out = outgoing_messages
    outgoing_messages = []
    return out


def set_tips(menu):
    global tip_menu
    tip_menu = menu


def retrieve_tips():
    global tip_menu
    menu = tip_menu
    tip_menu = None
    return menu


def format_tips(tips):
    out = []
    for key in tips:
        out.append({"credits": tips[key], "title": key})
    return out


def format_milestones(milestone_list):
    out = []
    for key in milestone_list:
        out.append({"name": key, "credits": milestone_list[key]})
    return out


def set_stream_info(title, public, nsfw, chatting, milestone_list, tags):
    global stream_info
    stream_info = {'name': title, 'use_milestones': False, 'terms': True, 'i_am_i': True, 'is_public': public,
                   'is_nsfw': nsfw, 'is_chat': chatting}
    if milestone_list:
        stream_info['milestones'] = milestone_list
        stream_info['use_milestones'] = True
    stream_info['tags'] = tags


def retrieve_stream_info():
    global stream_info
    temp_info = stream_info
    stream_info = None
    return temp_info
