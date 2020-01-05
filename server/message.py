#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Mythezone
# DATE: 2020/01/05 Sun
# TIME: 14:43:34

# DESCRIPTION:
import os,sys,json,socket,time


def gen_msg(tp,content):
    copy_content={}
    for key,value in content.items():
        copy_content[key]=value
    msg={
        "type":tp,
        "content":copy_content
    }
    return json.dumps(msg).encode()

def reg_msg(addr):
    ip,port=addr
    content={
        "ip":ip,
        "port":port
    }
    return gen_msg("register",content)

def que_msg(solution,fitness,iteration,timecost):
    content={
        "solution":solution,
        "fitness":fitness,
        "iteration":iteration,
        "timecost":timecost
    }
    return gen_msg("result",content)

def qued_msg(dict_result):
    return gen_msg("result",dict_result)

def par_msg(msg):
    d=json.loads(msg.decode())
    return d