#!/usr/bin/env python

import asyncio
import ssl
import websockets
import json
import time
import requests
import configparser
import os
import traceback
import importlib.util
import PlexLib

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

log = False

print("Loading External Scripts!")
basedir = os.getcwd()
os.chdir('scripts')
modules = next(os.walk('.'))[1]
for m in modules:
    script_name = os.path.join(m, 'main.py')
    if os.path.isfile(script_name):
        spec = importlib.util.spec_from_file_location(m, script_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
os.chdir(basedir)
print("...complete!")

ssl_context = ssl.create_default_context()
_auth = None


async def send_messages():
    while _auth.get_token("bot") == "":
        await asyncio.sleep(5)
    while True:
        await asyncio.sleep(1)
        msg_obj = PlexLib.retrieve_message()
        if msg_obj:
            r = requests.post(f"https://api.plexstorm.com/api/channels/{msg_obj['channel']}/messages",
                              headers={'Authorization': f'Bearer {_auth.get_token("bot")}'},
                              data={'message': msg_obj['message']})
        menu = PlexLib.retrieve_tips()
        if menu is not None:
            if not menu:
                r = requests.post(
                    f"https://api.plexstorm.com/api/channels/{config['Streamer']['username']}/tip-suggestions/multiple",
                    headers={'Authorization': f'Bearer {_auth.get_token("streamer")}'})
            else:
                r = requests.post(
                    f"https://api.plexstorm.com/api/channels/{config['Streamer']['username']}/tip-suggestions/multiple",
                    headers={'Authorization': f'Bearer {_auth.get_token("streamer")}'}, json=menu)
        stream_info = PlexLib.retrieve_stream_info()
        if stream_info is not None:
            r = requests.post("https://api.plexstorm.com/api/stream/setup",
                              headers={'Authorization': f'Bearer {_auth.get_token("streamer")}'}, json=stream_info)


async def do_ping(websocket):
    while True:
        await asyncio.sleep(25)
        try:
            await websocket.send('2')
        except websockets.exceptions.ConnectionClosedError:
            return


async def show_receive(websocket):
    if log:
        f = open(f'logs/PlexDump-{time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime())}.log', 'w+')
    while True:
        try:
            response = await websocket.recv()
        except websockets.exceptions.ConnectionClosedError:
            if log:
                f.close()
            return
        if log:
            f.write(f'{response}\r\n')
            f.flush()
        if response[:2] == '42':
            jres = json.loads(response[2:])
            channel = jres[1].split('.')[1]
            if jres[0] == 'App\\Events\\MessageCreated':
                message = jres[2]['data']['message']
                for cb in PlexLib.retrieve_callbacks("on_message"):
                    try:
                        cb(channel, message)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\MessageDeleted':
                message_id = jres[2]['data']['message_id']
                for cb in PlexLib.retrieve_callbacks("on_messagedeleted"):
                    try:
                        cb(channel, message_id)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\ViewersCountUpdated':
                viewers = jres[2]['data']['active_viewers']
                for cb in PlexLib.retrieve_callbacks("on_viewercountupdate"):
                    try:
                        cb(channel, viewers)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\MilestonesUpdated':
                if jres[2]['data']['milestones']:
                    milestones = jres[2]['data']['milestones']['all']
                    progress = jres[2]['data']['milestones']['progress']
                else:
                    milestones = None
                    progress = None
                for cb in PlexLib.retrieve_callbacks("on_milestoneupdate"):
                    try:
                        cb(channel, milestones, progress)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\MilestoneReached':
                if jres[2]['data']['milestones']:
                    milestones = jres[2]['data']['milestones']['all']
                    progress = jres[2]['data']['milestones']['progress']
                else:
                    milestones = None
                    progress = None
                for cb in PlexLib.retrieve_callbacks("on_milestonereached"):
                    try:
                        cb(channel, milestones, progress)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\Tipped':
                if jres[2]['data']['milestones']:
                    milestones = jres[2]['data']['milestones']['all']
                    progress = jres[2]['data']['milestones']['progress']
                else:
                    milestones = None
                    progress = None
                top = jres[2]['data']['top_tippers']
                for cb in PlexLib.retrieve_callbacks("on_tip"):
                    try:
                        cb(channel, milestones, progress, top)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\TipSuggestionsUpdated':
                tips = jres[2]['data']['tip_suggestions']
                for cb in PlexLib.retrieve_callbacks("on_tipsuggestions"):
                    try:
                        cb(channel, tips)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\ChannelUserUpdated':
                user = jres[2]['data']['user']
                for cb in PlexLib.retrieve_callbacks("on_userupdate"):
                    try:
                        cb(channel, user)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\StreamStarted':
                if jres[2]['data']['stream']['milestones']:
                    milestones = jres[2]['data']['stream']['milestones']['all']
                    progress = jres[2]['data']['stream']['milestones']['progress']
                else:
                    milestones = None
                    progress = None
                top = jres[2]['data']['stream']['top_tippers']
                title = jres[2]['data']['stream']['name']
                tags = jres[2]['data']['stream']['tags']
                start_time = jres[2]['data']['stream']['started_at']
                public = (jres[2]['data']['stream']['is_public'] == 1)
                for cb in PlexLib.retrieve_callbacks("on_streamstart"):
                    try:
                        cb(channel, milestones, progress, top, title, tags, start_time, public)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\StreamUpdated':
                if jres[2]['data']['stream']['milestones']:
                    milestones = jres[2]['data']['stream']['milestones']['all']
                    progress = jres[2]['data']['stream']['milestones']['progress']
                else:
                    milestones = None
                    progress = None
                top = jres[2]['data']['stream']['top_tippers']
                title = jres[2]['data']['stream']['name']
                tags = jres[2]['data']['stream']['tags']
                start_time = jres[2]['data']['stream']['started_at']
                public = jres[2]['data']['stream']['is_public']
                nsfw = jres[2]['data']['is_nsfw']
                for cb in PlexLib.retrieve_callbacks("on_streamupdate"):
                    try:
                        cb(channel, milestones, progress, top, title, tags, start_time, public, nsfw)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\StreamStopped':
                status = jres[2]['data']['status']
                for cb in PlexLib.retrieve_callbacks("on_streamend"):
                    try:
                        cb(channel, status)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'App\\Events\\StreamerUpdated':
                user = jres[2]['data']['user']
                for cb in PlexLib.retrieve_callbacks("on_streamerupdate"):
                    try:
                        cb(channel, user)
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            elif jres[0] == 'Illuminate\\Notifications\\Events\\BroadcastNotificationCreated':
                if jres[2]['type'] == 'App\\Notifications\\ExperienceReceived':
                    amount = jres[2]['value']
                    level_stats = jres[2]['level_progress']
                    for cb in PlexLib.retrieve_callbacks("on_experiencereceived"):
                        try:
                            cb(amount, level_stats)
                        except:
                            print('033[93m' + traceback.format_exc() + '033[0m')
                elif jres[2]['type'] == 'App\\Notifications\\Toasts\\NewRewardReceived':
                    message = jres[2]['message']
                    reason = jres[2]['data']['name']
                    amount = jres[2]['data']['value']
                    for cb in PlexLib.retrieve_callbacks("on_newreward"):
                        try:
                            cb(message, reason, amount)
                        except:
                            print('033[93m' + traceback.format_exc() + '033[0m')
                elif jres[2]['type'] == 'App\\Notifications\\Toasts\\FollowedChannelStreamStarted':
                    message = jres[2]['message']
                    streamer = jres[2]['data']['streamer']
                    for cb in PlexLib.retrieve_callbacks("on_followedstreamstart"):
                        try:
                            cb(message, streamer)
                        except:
                            print('033[93m' + traceback.format_exc() + '033[0m')
                elif jres[2]['type'] == 'App\\Notifications\\CreditsBalanceUpdated':
                    _credits = jres[2]['credits']
                    for cb in PlexLib.retrieve_callbacks("on_creditbalanceupdate"):
                        try:
                            cb(_credits)
                        except:
                            print('033[93m' + traceback.format_exc() + '033[0m')
                else:
                    try:
                        print(
                            f'-----------------\nBroadcast Notification\n-----------------\n{jres}\n-----------------')
                    except:
                        print('033[93m' + traceback.format_exc() + '033[0m')
            else:
                try:
                    print(f'--------------------\n{jres}\n--------------------')
                except:
                    print('033[93m' + traceback.format_exc() + '033[0m')
    if log:
        f.close()


async def plex_chat(uri):
    global _auth
    _auth = PlexLib.Auth("Auth")
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        if not PlexLib.init_done:
            secret = 'tJ1Ng4AoDwnecJ1zknyX0cDd3BaxWAKR10s7YKnw'
            r = requests.post('https://api.plexstorm.com/oauth/token',
                              data={"username": config['Bot']['email'], "password": config['Bot']['password'],
                                    "grant_type": "password", "client_id": "1", "client_secret": secret})
            _auth.set_token("bot", r.json()['access_token'])
            if config['Bot']['email'] == config['Streamer']['email']:
                _auth.set_token("streamer", _auth.get_token("bot"))
            else:
                r = requests.post('https://api.plexstorm.com/oauth/token',
                                  data={"username": config['Streamer']['email'],
                                        "password": config['Streamer']['password'], "grant_type": "password",
                                        "client_id": "1", "client_secret": secret})
                _auth.set_token("streamer", r.json()['access_token'])
        PlexLib.init_done = True
        await websocket.send(
            r'42["subscribe",{"channel":"private-user.%s","auth":{"headers":{"Authorization":"Bearer %s"}}}]' % (
                config['Streamer']['username'], _auth.get_token("streamer")))
        channels = list(config['Channels'].keys())
        for channel in channels:
            await websocket.send(
                r'42["subscribe",{"channel":"channel.%s","auth":{"headers":{"Authorization":"Bearer %s"}}}]' % (
                    channel, _auth.get_token("bot")))
        await asyncio.gather(
            do_ping(websocket),
            show_receive(websocket),
            send_messages()
        )


async def run_repeatedly():
    while True:
        print('Connecting...')
        await plex_chat(r'wss://websocket.plexstorm.com/socket.io/?EIO=3&transport=websocket')


asyncio.get_event_loop().run_until_complete(run_repeatedly())
