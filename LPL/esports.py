# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 13:50:02 2019

@author: Lee
"""

import requests
from pymongo import MongoClient


class LOL(object):
    
    def __init__(self):
        
        self.origin='https://data.pentaq.com/business_api/2018may/'
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.client=MongoClient()
        self.db=self.client.esports
        self.tourna_id=[]
        self.tourna_name=[]

    def get_tourna_id(self):
        
        url='https://data.pentaq.com/business_api/2018mar/tournament_list'
        r=requests.get(url,headers=self.headers)
        
        tornas=r.json()['tournaments']
        for torna in tornas: 
            self.tourna_id.append(torna['id'])
            self.tourna_name.append(torna['full_name'])
        print("已获得所有比赛信息列表！")
    
    def get_player_data(self):
        
        url=self.origin+'tournament_player_duty_data'
        for i in range(len(self.tourna_id)):
            params={
                   'tour':self.tourna_id[i],
                   }
            r=requests.get(url,headers=self.headers,params=params)
            players_data=r.json()['data']['players_data']
            for player in players_data:
                appear=player['appear']
                assist=player['assist']
                battle_rate_per_game=player['battle_rate_per_game']
                buy_true_eye_per_minute=player['buy_true_eye_per_minute']
                damage_efficiency=player['damage_efficiency']
                damage_per_minute=player['damage_per_minute']
                damage_percent=player['damage_percent']
                dead=player['dead']
                destroy_eye_per_minute=player['destroy_eye_per_minute']
                duty_id=player['duty_id']
                exp_diff_10m_per_game=player['exp_diff_10m_per_game']
                kda=player['kda']
                kill=player['kill']
                lose=player['lose']
                player_id=player['player_id']
                player_name=player['player_name']
                psr=player['psr']
                put_eye_per_minute=player['put_eye_per_minute']
                solo_dead=player['solo_dead']
                solo_kill=player['solo_kill']
                tank_efficiency=player['tank_efficiency']
                tank_per_minute=player['tank_per_minute']
                tank_percent=player['tank_percent']

                team_name=player['team_name']
                ten_minutes_creeps_per_game=player['ten_minutes_creeps_per_game']
                ten_minutes_gold_offset_per_game=player['ten_minutes_gold_offset_per_game']
                win=player['win']
                win_rate=player['win_rate']
                tournament=self.tourna_name[i]
                item={
                    'appear':appear,
                    'assist':assist,
                    'battle_rate_per_game':battle_rate_per_game,
                    'buy_true_eye_per_minute':buy_true_eye_per_minute,
                    'damage_efficiency':damage_efficiency,
                    'damage_per_minute':damage_per_minute,
                    'damage_percent':damage_percent,
                    'dead':dead,
                    'destroy_eye_per_minute':destroy_eye_per_minute,
                    'duty_id':duty_id,
                    'exp_diff_10m_per_game':exp_diff_10m_per_game,
                    'kda':kda,
                    'kill':kill,
                    'lose':lose,
                    'player_id':player_id,
                    'player_name':player_name,
                    'psr':psr,
                    'put_eye_per_minute':put_eye_per_minute,
                    'solo_dead':solo_dead,
                    'solo_kill':solo_kill,
                    'tank_efficiency':tank_efficiency,
                    'tank_per_minute':tank_per_minute,
                    'tank_percent':tank_percent,
                    'team_name':team_name,
                    'ten_minutes_creeps_per_game':ten_minutes_creeps_per_game,
                    'ten_minutes_gold_offset_per_game':ten_minutes_gold_offset_per_game,
                    'win':win,
                    'win_rate':win_rate,
                    'tournament':tournament                     
                        }
                
                self.db['player'].insert_one(item)
            print("已存入{}所有职业选手数据！".format(tournament))
            
            
    def get_team_data(self):
        
        url=self.origin+'tournament_team_data'
        for i in range(len(self.tourna_id)):
            params={
                   'tour':self.tourna_id[i],
                   }
            r=requests.get(url,headers=self.headers,params=params)
            teams_data=r.json()['data']['teams_data']
            for team in teams_data:
                appear=team['appear']
                baron_nashor_percent=team['baron_nashor_percent']
                bloodiness=team['bloodiness']
                buy_true_eye_per_minute=team['buy_true_eye_per_minute']
                damage_per_minute=team['damage_per_minute']
                dead=team['dead']
                destroy_eye_per_minute=team['destroy_eye_per_minute']
                dragon_percent=team['dragon_percent']
                duration_per_game=team['duration_per_game']
                duration_per_lose=team['duration_per_lose']
                duration_per_win=team['duration_per_win']
                first_baron_nashor_percent=team['first_baron_nashor_percent']
                first_blood_percent=team['first_blood_percent']
                first_dragon_percent=team['first_dragon_percent']
                first_tower_percent=team['first_tower_percent']
                kill=team['kill']
                lose=team['lose']
                minions_percent_per_game=team['minions_percent_per_game']
                put_eye_per_minute=team['put_eye_per_minute']
                rift_hearld_percent=team['rift_hearld_percent']
                tank_per_minute=team['appear']
                team_name=team['team_name']
                ten_minutes_gold_offset_per_game=team['ten_minutes_gold_offset_per_game']
                win=team['win']
                win_rate=team['win_rate']
                tournament=self.tourna_name[i]
                item={
                    'appear':appear,
                    'baron_nashor_percent':baron_nashor_percent,
                    'buy_true_eye_per_minute':buy_true_eye_per_minute,
                    'bloodiness':bloodiness,
                    'damage_per_minute':damage_per_minute,
                    'dragon_percent':dragon_percent,
                    'dead':dead,
                    'destroy_eye_per_minute':destroy_eye_per_minute,
                    'duration_per_game':duration_per_game,
                    'duration_per_lose':duration_per_lose,
                    'duration_per_win':duration_per_win,
                    'kill':kill,
                    'lose':lose,
                    'first_baron_nashor_percent':first_baron_nashor_percent,
                    'first_blood_percent':first_blood_percent,
                    'first_dragon_percent':first_dragon_percent,
                    'put_eye_per_minute':put_eye_per_minute,
                    'first_dragon_percent':first_dragon_percent,
                    'rift_hearld_percent':rift_hearld_percent,
                    'first_tower_percent':first_tower_percent,
                    'tank_per_minute':tank_per_minute,
                    'minions_percent_per_game':minions_percent_per_game,
                    'team_name':team_name,
                    'ten_minutes_gold_offset_per_game':ten_minutes_gold_offset_per_game,
                    'win':win,
                    'win_rate':win_rate,
                    'tournament':tournament                     
                        }
                
                self.db['team'].insert_one(item)
            print("已存入{}所有战队数据！".format(tournament))
                
                
                
                
if __name__=='__main__':
    
    data=LOL()
    data.get_tourna_id()
    data.get_player_data()
    data.get_team_data()