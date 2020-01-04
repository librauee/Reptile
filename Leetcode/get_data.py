# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 10:45:32 2020

@author: Administrator
"""

import requests
from pymongo import MongoClient

def get_title():
    
    headers={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
         }   
    title_url='https://leetcode.com/api/problems/all/'
    r=requests.get(url=title_url,headers=headers)
    stat_status_pairs=r.json()['stat_status_pairs']
    question_ids=[]
    question_title_slugs=[]
    for stat in stat_status_pairs:
        question_id=stat['stat']['question_id']
        question_title_slug=stat['stat']['question__title_slug']
        question_ids.append(question_id)
        question_title_slugs.append(question_title_slug)
    question_dic=dict(zip(question_ids,question_title_slugs))
    return question_dic


def get_attitude(db):
    
    question_dic=get_title()
    headers={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
         'origin': 'https://leetcode-cn.com'
         }
    url='https://leetcode-cn.com/graphql/'
    for question_id,question_title_slug in question_dic.items():
        
        data={"query":'query{{question(titleSlug:"{}") {{content,likes,difficulty,dislikes,stats,boundTopicId}}}}'.format(question_title_slug)}
        r=requests.post(url,headers=headers,data=data)
        question_data=r.json()['data']['question']
        # content=question_data['content']

        try:
            likes=question_data['likes']
            difficulty=question_data['difficulty']
            stats=eval(question_data['stats'])
            dislikes=question_data['dislikes']
            totalAcceptedRaw=stats['totalAcceptedRaw']
            totalSubmissionRaw=stats['totalSubmissionRaw']
            acRate=stats['acRate']
            boundTopicId=question_data['boundTopicId']
            question={
                  'id':question_id,
                  'title':question_title_slug,
                  'likes':likes,
                  'difficulty':difficulty,
                  'dislikes':dislikes,
                  'totalAcceptedRaw':totalAcceptedRaw,
                  'totalSubmissionRaw':totalSubmissionRaw,
                  'acRate':acRate,
                  'boundTopicId':boundTopicId
                 
                }
            print(question)
            db['1'].insert_one(question)
        except Exception as e:
            print(e)
            pass
    
    


if __name__=='__main__':
    db=MongoClient().leetcode
    get_attitude(db)