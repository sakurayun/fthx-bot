from os.path import join
from pathlib import Path
import random
import re
import aiohttp
import math
from PIL import ImageFile
from typing_extensions import runtime
ImageFile.LOAD_TRUNCATED_IMAGES = True
from random import randint
import requests
import hashlib
import json
import shutil
from PIL import ImageFont,ImageDraw
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session, message
from graia.application.message.chain import MessageChain
import asyncio
import aiohttp
from graia.application.group import Group, Member
from graia.application.message.elements.internal import At, Image, Plain, Xml,Json,App
from graia.application.friend import Friend
from operator import eq
from datetime import datetime
import time as Time
from dateutil import rrule
from PIL import Image as Im
from pixivpy3 import *
import sys
import requests
import os
from os.path import join, getsize
import eventlet
import zipfile
from runtimetext import lolicon_key,saucenao_key,admin,hsomap,fl1,fl2,authKey,bot_qq,host_,aks_map,aks_map2,aks_map3,aki_map,helptext,piv_username,piv_password,maxx_img,infomap,maximgpass
api = AppPixivAPI()
loop = asyncio.get_event_loop() 
bcc = Broadcast(loop=loop) 
app = GraiaMiraiApplication(broadcast=bcc,connect_info=Session(host=host_,authKey=authKey,account=bot_qq,websocket=True)) #机器人启动
eventlet.monkey_patch()
with eventlet.Timeout(4,False):
    code = 0
    try:
        api = AppPixivAPI()
        #api.login(piv_username, piv_password)
    except:
        print('Pixiv登录失败')
    code = 1
if code == 0 : print('Pixiv登录超时')
def sdir(tdir): #新建目录
    if not os.path.exists(tdir):
        print('目标不存在,新建目录:',tdir)
        os.makedirs(tdir)
try:#初始化
    if not os.path.exists('cfg.json'):
        if not os.path.exists('./chace/mainbg.png'):
            print('错误:没有找到主界面背景')
        cfg = {}
        cfg['hsolvlist'] = {}
        cfg['hsolv'] = {}
        cfg['qd'] = {}
        cfg['qdlist'] = {}
        cfg['last_setu'] = {}
        cfg['hsolvlist']['0'] = 0
        cfg['hsolv']['0'] = 0
        cfg['qd']['0'] = 0
        cfg['qdlist']['0'] = 0
        cfg['setu_group'] = [0]
        cfg['r18_group'] = [0]
        cfg['last_setu']['0'] = 0
        cfg['time'] = datetime.now().strftime('%Y-%m-%d 10:10:10')
        cfg['setu_l'] = 0
        cfg['xml'] = 0
        jsonfile=open("cfg.json","w")
        json.dump(cfg,jsonfile,indent=4)
        jsonfile.close()
        print('初始化完成，你需要在群聊内输入akra来获取明日方舟的数据')
except Exception:print('初始化出现错误')
try:#配置cfg.json读取与补全
    cfgdlist = ['hsolvlist','hsolv','qd','qdlist','last_setu','plinfodata']
    cfgilist = ['setu_l','xml']
    jsonfile = open("cfg.json","r")
    cfg = json.load(jsonfile)
    jsonfile.close()
    sdir('./r18')
    if not os.path.exists('./aki_60'):
        sdir('./aki_60')
        f = zipfile.ZipFile("./aki_60.zip",'r')
        for file in f.namelist():
            f.extract(file,"aki_60/")
        os.remove("./aki_60.zip")
    if not os.path.exists('./aki_30'):
        sdir('./aki_30')
        flist = os.listdir('./aki_60')
        for file in flist:
            path = './aki_60/' + file
            path2 = './aki_30/' + file
            img = Im.open(path).convert('RGBA')
            img = img.resize((30, 30),Im.ANTIALIAS)
            img.save(path2, 'png')


    sdir('./setu')
    sdir('./chace')
    sdir('./backups')
    sdir('./listpiv')
    for i in cfgdlist:
        try: 
            load = cfg[i]
        except: 
            print('不存在:',i)
            cfg[i] = {}
    for i in cfgilist:
        try: 
            load = cfg[i]
        except: 
            print('不存在:',i)
            cfg[i] = 0
except:pass
try:#配置cfg.json数据转换
    hsolvlist_data = {}
    hsolvlist_data = cfg['hsolvlist']
    hsolv_data = cfg['hsolv']
    qd_data = cfg['qd']
    qdlist_data = cfg['qdlist']
    setu_group = cfg['setu_group']
    r18_group = cfg['r18_group']
    last_setu = cfg['last_setu']
except:print('严重错误，配置读取失败')
try:#方舟json读取
    jsonfile = open("akm.json","r")
    akm_data = json.load(jsonfile)
    jsonfile.close()
    jsonfile = open("aki.json","r")
    aki_data = json.load(jsonfile)
    jsonfile.close()
    jsonfile = open("aks.json","r")
    aks_data = json.load(jsonfile)
    jsonfile.close()
except:print('错误，方舟数据读取失败')

class DF(object): #下载
    async def adf(url,pach):#异步下载
        url = url.replace('i.pximg.net','i.pixiv.cat')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        async with aiohttp.ClientSession() as session:
            response = await session.get(headers=headers, url=url)
            content_img = await response.read()
            tempf = open(pach,'w')
            tempf.close()
            with open(pach, 'wb') as f:
                f.write(content_img)
            await session.close()
            if pach.endswith('png'):
                inputimg = Im.open(pach)
                mmx = inputimg.size[0]
                mmy = inputimg.size[1]
                if mmx > maxx_img and maxx_img != 0:
                    xyb = mmx / mmy
                    new_mmx = maxx_img
                    new_mmy = math.floor(new_mmx / xyb)
                    inputimg = inputimg.resize((new_mmx, new_mmy),Im.ANTIALIAS)
                    mmx = inputimg.size[0]
                    mmy = inputimg.size[1]
                    print('新图片大小:',mmx,'|',mmy)
                    inputimg.save(pach, 'png')
class CHS(object): #数据初始化
    def chs(id): 
        datas = [hsolv_data,hsolvlist_data,qd_data,qdlist_data]
        for i in datas :
            if id not in i:
                i[id] = 0
async def tlen(text): #文字宽度测量
    lenTxt = len(text) 
    lenTxt_utf8 = len(text.encode('utf-8')) 
    size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)
    return size
async def dakm(): #明日方舟m数据获取
    apiurl = 'https://penguin-stats.io/PenguinStats/api/v2/result/matrix'
    print('与api沟通中...')
    async with aiohttp.ClientSession() as session:
        async with session.get(apiurl) as resp:
            res_akm_json = await resp.json()
    ak_m = res_akm_json['matrix']
    akm = []
    for i in ak_m:
        end = False
        print(i)
        for item in i:
            if 'end' in item:
                print(i['stageId'],i['itemId'],'已录入')
                end = True
        if end == False:akm.append(i)
    print('done')
    jsonfile=open("akm.json","w")
    json.dump(akm,jsonfile,indent=4)
    jsonfile.close()
    print('json save done')
async def daki(): #明日方舟i数据获取
    apiurl = 'https://penguin-stats.io/PenguinStats/api/v2/items'
    print('与api沟通中...')
    async with aiohttp.ClientSession() as session:
        async with session.get(apiurl) as resp:
            res_aki_json = await resp.json()
    aki = []
    for i in res_aki_json:
        aki_jsoning = {}
        aki_jsoning['itemId'] = i['itemId']
        aki_jsoning['alias'] = i['alias']['zh']
        aki_jsoning['rarity'] = i['rarity']
        print(aki_jsoning['itemId'],aki_jsoning['alias'][0],'已录入')
        aki.append(aki_jsoning)
    print('done')
    jsonfile=open("aki.json","w")
    json.dump(aki,jsonfile,indent=4)
    jsonfile.close()
    print('json save done')
async def daks(): #明日方舟s数据获取
    apiurl = 'https://penguin-stats.io/PenguinStats/api/v2/stages'
    print('与api沟通中...')
    async with aiohttp.ClientSession() as session:
        async with session.get(apiurl) as resp:
            res_aks_json = await resp.json()
    aks = []
    for i in res_aks_json:
        aks_jsoning = {}
        aks_jsoning['stageId'] = i['stageId']
        aks_jsoning['name'] = i['code_i18n']['zh']
        aks_jsoning['stageType'] = i['stageType']
        try:
            aks_jsoning['apCost'] = i['apCost']
        except:pass
        try:
            aks_jsoning['minClearTime'] = i['minClearTime']
        except:pass
        try:
            aks_jsoning['dropInfos'] = i['dropInfos']
        except:pass
        print(aks_jsoning['stageId'],aks_jsoning['name'],'已录入')
        aks.append(aks_jsoning)
    print('done')
    jsonfile=open("aks.json","w")
    json.dump(aks,jsonfile,indent=4)
    jsonfile.close()
    print('json save done')
async def setu(r18,iid,g,s=''): #获取色图
    outmsg = {}
    id = str(iid)
    if id not in hsolvlist_data:
        print('初始化',id)
        hsolv_data[id] = 0
        hsolvlist_data[id] = 0
        qd_data[id] = 0
        qdlist_data[id] = 0
    exmsg = "none"
    if qd_data[id] == 0:
        if qdlist_data[id] == 0:
            stadd = random.randint(10,28)
            outmsg['extmsg'] = "这是你第一次获取色图,随机获取色图$张".replace('$',str(stadd))
        else:
            stadd = random.randint(6,15)
            outmsg['extmsg'] = "今天第一次获取色图，随机获取色图$张".replace('$',str(stadd))
        hsolv_data[id] = hsolv_data[id] + stadd
        qdlist_data[id] = qdlist_data[id] + 1
        qd_data[id] = 1

    if hsolv_data[id] >= 1 and cfg['setu_l'] == 0:
        apiurl = 'https://api.lolicon.app/setu/?apikey=$APIKEY&r18=$R18&num=$NUM'.replace('$APIKEY',lolicon_key).replace('$R18',str(r18)).replace('$NUM',str(1))
        if s != '':
            apiurl = apiurl + '&keyword=' + s
        print('与api沟通中...')
        async with aiohttp.ClientSession() as session:
            async with session.get(apiurl) as resp:
                res_json = await resp.json()
        code = res_json['code']
        if code == 429:
            cfg['setu_l'] = 1
            outmsg['extmsg'] = "429错误，达到色图调用上限，切换至本地色图"
            return outmsg
        for i in res_json['data']:
            url_ing = i['url']
            pid_ing = i['pid']
            if r18 == 1:path_ing = './r18/' + str(pid_ing) + '.png'
            else:path_ing = './setu/' + str(pid_ing) + '.png'
            outmsg['pid'] = pid_ing
            hsolvlist_data[id] = hsolvlist_data[id] + 1
            hsolv_data[id] = hsolv_data[id] - 1
            print(url_ing,pid_ing,'开始下载')
            try:
                await DF.adf(url_ing,path_ing)
                outmsg['imgpath'] = path_ing
                code = True
            except:
                print('连接错误，正在重试....')
                try:
                    await DF.adf(url_ing,path_ing)
                    outmsg['imgpath'] = path_ing
                    code = True
                except:
                    hsolv_data[id] = hsolv_data[id] + 1
                    hsolvlist_data[id] = hsolvlist_data[id] - 1
                    outmsg['extmsg'] = "连接错误，已退回色图。"
        gr = str(g)
        outdata = ""
        datamsg = res_json['data'][0]
        for i in datamsg:
            outdata = outdata + i + str(datamsg[i]) 
        outdata = outdata.replace('pid','pid:').replace('p0',' p0 - ').replace('uid','uid:').replace('title','\n标题:').replace('author','   作者:').replace('url','\n').replace('r18False','').replace('r18True','').replace('width','\n').replace('height','x').replace('tags','\n标签:')
        print(datamsg)
        outmsg['pid'] = datamsg['pid']
        outmsg['uid'] = datamsg['uid']
        outmsg['title'] = datamsg['title']
        outmsg['author'] = datamsg['author']
        outmsg['url'] = datamsg['url']
        outmsg['tags'] = datamsg['tags']
        last_setu[gr] = outdata
        outmsg['info'] = outdata
    elif hsolv_data[id] >= 1 and cfg['setu_l'] == 1:
        if r18 == 0: setu_ = './setu'
        else: setu_ = './r18'
        folder = os.listdir(setu_)
        pach_chace = []
        All_files_pach = []
        for i in folder:
            pach_chace=setu_ +'/' + i
            All_files_pach.append(pach_chace)
        setulen = len(All_files_pach)
        if All_files_pach == []:print('没有找到色图')
        else:print('色图载入成功')
        x = randint(0,setulen)
        filepach = str(All_files_pach[x])
        filename = filepach.replace(setu_ + '/','')
        print("选中色图" + filepach)
        hsolv_data[id] = hsolv_data[id] - 1
        last_setu[str(g)] = filename
        hsolvlist_data[id] = hsolvlist_data[id] + 1
        outmsg['imgpath'] = filepach
    else:
        outmsg['extmsg'] = "你没有剩余色图或其他错误"
    return outmsg
async def rep(l,text): #文字占位处理
    strnone = ' '
    len_ing = await tlen(text)
    if len_ing > l:
        return
    add = strnone * ( l - len_ing)
    out = text + add
    return out
async def settime(time): #时间格式化
    atime = ''
    time_h = math.floor((time/1000)/60/60)
    if time_h != 0:atime = atime + str(time_h) + ':'
    time_m = math.floor((time/1000)/60) - time_h *60
    if time_m != 0:atime = atime + str(time_m) + ':'
    time_s = (math.floor(time/1000) -time_m *60 ) - time_h*60*60
    if time_s != 0:atime = atime + str(time_s)
    return atime
def restart_program(): #重启
    python = sys.executable
    os.execl(python, python, * sys.argv)
def savecfg(): #保存cfg.json
    try:
        jsonfile=open("cfg.json","w")
        json.dump(cfg,jsonfile,indent=4)
        jsonfile.close()
    except Exception:
        print('save cfg 出现错误')
def toimg(msg,img='./chace/mainbg.png',f1=fl1,f2=fl2,pz=False): #文字转图片
    '''
    input:
      msg:str 输入文字
      img:str 图片路径
      f1:str 字体1路径
      f2:str 字体2路径
    '''
    msg = msg.replace('\n','').replace('\r','')
    image = Im.open(img).convert('RGBA')
#rs
    global x
    global y
    global mx
    global my
    global mmx
    global mmy
    global size
    global color
    lispuimg = []
    xin = -200
    xout = -100
    yin = -200
    yout = -100
    mmx = 2048
    mmy = 1278
    size = 30
    y = 0 
    x = 0
    my = 10
    mx = 10
    color = "#ffffff"
    efunction = False
    functionlist = []
    f = ''
    if img != './chace/mainbg.png' : 
        mmx = image.size[0]
        mmy = image.size[1]
    '''变量:
    x : 坐标x
    y : 坐标y
    mx :裁剪后图片宽度 (如果要设定必须在末尾)
    my :裁剪后图片长度 (如果要设定必须在末尾)
    mmx :原图大小(如果要设定必须在开头)
    mmy :原图大小(如果要设定必须在开头)
    # "y": y + size 是可行的
    size:目前文字大小
    color:颜色
    '''
#def1
    for i in msg: # 遍历所有文字,探测\指令,输出所有文字占图片最大宽 高
        if efunction == False and eq(i,"\\"): #探测到 \ 则进入功能模式
            efunction=True
            functionlist=[] 
            continue
        elif efunction == True: #功能模式
            if eq(i,"\\"): #在功能模式下再次探测到 \ 则退出功能模式
                efunction = False
                text = ''.join(functionlist)
                if text.startswith("n"): #n:换行
                    if x + size > mx: mx = x + size
                    if y + size > my: my = y + size
                    text = text[1:]
                    if text.isdigit():x = int(text) #n<int> 换行并使x = int
                    if text.startswith('s'):x = x  #ns 换行并保持x
                    else: x = 0
                    y += size
                    if x + size > mx: mx = x + size 
                    if y + size > my: my = y + size
                elif text.startswith("b"):size = int(text[1:]) #b<int>:文字大小
                elif text.startswith('#'):color = text ##<16进制颜色>:文字颜色
                elif text.startswith('y'):y = int(text[1:]) #y<int>:立即切换到y坐标
                elif text.startswith('x'):#x<x/y>(-)<int> 
                    """
                    xx<int>: x += int
                    xx-<int>: x -= int

                    xy<int>: y += int
                    xy-<int>: y -= int
                    """
                    text = text[1:]
                    if text.startswith('x'):
                        text = text[1:]
                        if text.startswith('-'):x -= int(text[1:])
                        else: x += int(text)
                    elif text.startswith('y'):
                        text = text[1:]
                        if text.startswith('-'):y -= int(text[1:])
                        else: x += int(text)
                    if x + size > mx: mx = x + size 
                    if y + size > my: my = y + size
                elif text.startswith('p'): #p<图片路径>: 添加图片
                    if pz == True:
                        putpath = text[1:]
                        print(putpath)
                        putimg =  Im.open(putpath).convert('RGBA')
                        putmx = putimg.size[0]
                        putmy = putimg.size[1]
                        xin = x
                        xout = x + putmx
                        yin = y
                        yout = y + putmy
                        if yout > my: my = yout + size
                        if xout > mx: mx = xout + size
                        print(mx,my)
                        x = x + putmx + 1
                        putdata = {"xin":xin,"xout":xout,"yin":yin,"yout":yout} #因为该图片而产生的文字禁区:(xin,yin),(xout,yout)
                        lispuimg.append(putdata) #所有图片的文字禁区
                elif text.startswith('d'): #p<字典>: 变量修改(可用该功能一次性修改 x y color size 等等)
                    if x + size > mx: mx = x + size
                    if y + size > my: my = y + size
                    testx = 0
                    text = text[1:]
                    print(text)
                    dict_ing = json.loads(text)
                    print('修改:',dict_ing)
                    globals().update(dict_ing)
                    print(testx)
                functionlist=[] 
                continue
            functionlist.append(i) #退出后保存功能模式下所探测的文字到 functionlist
            continue
        if i >= u'\u4e00' and i <= u'\u9fa5' or i >= u'\u3040' and i <= u'\u31FF':#中文
            fx = size
            f = f1
        else:   #如果是英文，使用英文字体，并每次x跃进时只会跃进半个文字大小
            fx = size / 2 
            f = f2
        x += fx
        for r in range(maximgpass): #在 单个文字能跨过(图片中的)图片的最多次数 内循环
            code = False
            if pz == True:
                for i in lispuimg: #文字撞到(图片中的)图片则跃进图片宽度
                    if i['xin'] <= x < i['xout'] and i['yin'] <= y < i['yout']:
                        print('撞到图片啦:',x,y,i['xin'],i['xout'])
                        x = i['xout'] + size
                        code = True
                        break
                    if i['xin'] <= x + size < i['xout'] and i['yin'] <= y < i['yout']:
                        print('撞到图片啦:',x,y,i['xin'],i['xout'])
                        x = i['xout'] + size
                        code = True
                        break
                    if i['xin'] <= x < i['xout'] and i['yin'] <= y + size < i['yout']:
                        print('撞到图片啦:',x,y,i['xin'],i['xout'])
                        x = i['xout'] + size
                        code = True
                        break
                    if i['xin'] <= x + size < i['xout'] and i['yin'] <= y + size < i['yout']:
                        print('撞到图片啦:',x,y,i['xin'],i['xout'])
                        x = i['xout'] + size
                        code = True
                        break
            if x + size / 2 > mmx : #文字撞到边缘则换行
                print(x,y,mmx,mmy)
                if x + size > mx: mx = x + size
                if y + size > my: my = y + size
                x = 0
                y += size
                code = True
            if code == False : break #跳出循环
#rs2
    if x > mx: mx = x + size
    if y > my: my = y + size
    if my == 0:mx = x + size
    if my == 0:my += size 
    print('mx:' + str(mx) + "|my:" + str(my))
    ly =  (mmy - my) / 2
    image = image.crop((0,ly,mx,ly+my))
    mmx = mx
    mmy = my
    size = 30
    y = 0
    x = 0
    color = "#ffffff"
    efunction = False
    functionlist = []
    lispuimg = []
    f = ''
#def2
    for i in msg: # 遍历文字,探测\指令, 在图片内写入 文字/图片
        if efunction == False and eq(i,"\\"): #探测到 \ 则进入功能模式
            efunction=True
            functionlist=[] 
            continue
        elif efunction == True: #功能模式
            if eq(i,"\\"): #在功能模式下再次探测到 \ 则退出功能模式
                efunction = False
                text = ''.join(functionlist)
                if text.startswith("n"): #n:换行
                    text = text[1:]
                    if text.isdigit():x = int(text) #n<int> 换行并使x = int
                    if text.startswith('s'):x = x  #ns 换行并保持x
                    else: x = 0
                    y += size
                elif text.startswith("b"):size = int(text[1:]) #b<int>:文字大小
                elif text.startswith('#'):color = text ##<16进制颜色>:文字颜色
                elif text.startswith('y'):y = int(text[1:]) #y<int>:立即切换到y坐标
                elif text.startswith('x'): 
                    """
                    xx<int>: x += int
                    xx-<int>: x -= int

                    xy<int>: y += int
                    xy-<int>: y -= int
                    """
                    text = text[1:]
                    if text.startswith('x'):
                        text = text[1:]
                        if text.startswith('-'):x -= int(text[1:])
                        else: x += int(text)
                    elif text.startswith('y'):
                        text = text[1:]
                        if text.startswith('-'):y -= int(text[1:])
                        else: x += int(text)
                elif text.startswith('p'): #p<图片路径>: 添加图片
                    print(x,y)
                    putpath = text[1:]
                    putimg =  Im.open(putpath).convert('RGBA')
                    putimg.mode 
                    putmx = putimg.size[0]
                    putmy = putimg.size[1]
                    layer = Im.new('RGBA', image.size, (0,0,0,0))
                    layer.paste(putimg,(math.floor(x),math.floor(y)))
                    image = Im.composite(layer, image, layer)
                    if pz == True:
                        xin = x
                        xout = x + putmx
                        yin = y
                        yout = y + putmy
                        x = x + putmx + 1
                        putdata = {"xin":xin,"xout":xout,"yin":yin,"yout":yout} #因为该图片而产生的文字禁区:(xin,yin),(xout,yout)
                        print(putdata,x,y)
                        lispuimg.append(putdata) #所有图片的文字禁区
                elif text.startswith('d'): #p<字典>: 变量修改(可用该功能一次性修改 x y color size 等等)
                    testx = 0
                    text = text[1:]
                    print(text)
                    dict_ing = json.loads(text)
                    print('修改:',dict_ing)
                    globals().update(dict_ing)
                    print(testx)
                functionlist=[] 
                continue
            functionlist.append(i) #退出后保存功能模式下所探测的文字到 functionlist
            continue
        if i >= u'\u4e00' and i <= u'\u9fa5' or i >= u'\u3040' and i <= u'\u31FF': #中文
            fx = size
            f = f1
        else:  #如果是英文，使用英文字体，并每次x跃进时只会跃进半个文字大小
            fx = size / 2 
            f = f2
        ImageDraw.Draw(image).text((x+2, y-6),i,font=ImageFont.truetype(f,size),fill='#000000',direction=None) #文字阴影
        ImageDraw.Draw(image).text((x, y-8),i,font=ImageFont.truetype(f,size),fill=color,direction=None) #文字
        x += fx
        for r in range(maximgpass): #在 单个文字能跨过(图片中的)图片的最多次数 内循环
            code = False
            if pz == True:
                for i in lispuimg: #文字撞到(图片中的)图片则跃进图片宽度
                    if i['xin'] <= x < i['xout'] and i['yin'] <= y < i['yout']:
                        print('撞到图片啦:',x,y,i['xin'],i['xout'])
                        x = i['xout'] + size
                        code = True
                        break
                    if i['xin'] <= x + size < i['xout'] and i['yin'] <= y < i['yout']:
                        print('撞到图片啦:',x,y,i['xin'],i['xout'])
                        x = i['xout'] + size
                        code = True
                        break
                    if i['xin'] <= x < i['xout'] and i['yin'] <= y + size < i['yout']:
                        print('撞到图片啦:',x,y,i['xin'],i['xout'])
                        x = i['xout'] + size
                        code = True
                        break
                    if i['xin'] <= x + size < i['xout'] and i['yin'] <= y + size < i['yout']:
                        print('撞到图片啦:',x,y,i['xin'],i['xout'])
                        x = i['xout'] + size
                        code = True
                        break
            if x + size / 2 > mmx : #文字撞到边缘则换行
                print('撞到墙啦:',x,y)
                x = 0
                y += size
                code = True
            if code == False : break #跳出循环
    image.save('./chace/1.png')
    print("done")

@bcc.receiver("GroupMessage")
async def group_listener(app: GraiaMiraiApplication, MessageChain:MessageChain, group: Group, member:Member): #群聊监听
    msg = MessageChain.asDisplay()
    if MessageChain.has(Xml):
        txml = str(MessageChain.get(Xml))
        print(txml)
    if MessageChain.has(Json):
        tjson = str(MessageChain.get(Json))
        print(tjson)
    if MessageChain.has(App):
        tapp = str(MessageChain.get(App))
        print(tapp)
    if MessageChain.has(Plain):
        tmsg = str(MessageChain.get(Plain)[0].text)
#图片
    if MessageChain.has(Image):
        timg = MessageChain.get(Image)[0].url
        print(timg)
        if MessageChain.has(At):
            if MessageChain.get(At)[0].target == bot_qq:
#-以图搜图
                print('以图搜图')
                url = "https://saucenao.com/search.php?output_type=2&api_key=$key&testmode=1&dbmask=999&numres=5&url=$url".replace('$url',timg).replace('$key',saucenao_key)
                text = requests.get(url, headers={}) 
                data = json.loads(text.text)
                data = data['results']
                print(data)
                outdata = []
                n = 0
                for i in data:
                    n += 1
                    try:
                        url_ing = ''
                        url_ing = i["data"]['ext_urls'][0]
                        ps_ing = i['header']['similarity'] + '%'
                        url_ing = url_ing.replace('https://www.','')
                        texting = '$n.($%):$url\n'\
                            .replace('$n',str(n))\
                            .replace('$%',ps_ing)\
                            .replace('$url',url_ing)
                        outdata.append(texting)
                    except:
                        pass
                n = 0
                outmsg = ''
                for i in outdata:
                    outmsg = ''.join(outdata)
                await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg)]))
#-表情色图来
        if MessageChain.get(Image)[0].imageId == '{B407F708-A2C6-A506-3420-98DF7CAC4A57}.mirai' and group.id in cfg['setu_group']:
            outmsg = await setu(0,member.id,group.id)
            await app.sendGroupMessage(group,MessageChain.create(outmsg))
#普通色图
    if msg.startswith('色图来') and group.id in cfg['setu_group']:
        msg = msg.replace('色图来','').replace(' ','')
        print(msg)
        sc = ''
        if msg == '':
            num = 1
        else:
            try:
                num = int(msg)
            except:
                num = 1
                sc = msg
        print(num)
        if num == 0:pass
        elif num > 10:pass
        else:
            for i in range(num):
                outmsg = await setu(0,member.id,group.id,sc)
                if cfg['xml'] == 1:
                    print(outmsg)
                    chace1 = await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile(outmsg['imgpath'])]))
                    await asyncio.sleep(1)
                    await app.revokeMessage(chace1)
                    filepach = outmsg['imgpath']
                    fd = open(filepach, "rb")
                    f = fd.read()
                    pmd5 = hashlib.md5(f).hexdigest()
                    inputimg = Im.open(filepach)
                    mmx = inputimg.size[0]
                    mmy = inputimg.size[1]
                    tags = ' '.join(outmsg['tags'])
                    size = getsize(filepach)

                    ext =" $title by $author |pid:$pid uid:$uid |tags:$tags"\
                    .replace('$title',outmsg['title'])\
                    .replace('$author',outmsg['author'])\
                    .replace('$pid',str(outmsg['pid']))\
                    .replace('$uid',str(outmsg['uid']))\
                    .replace('$tags',tags)

                    dxy = str(1000)
                    print(pmd5)
                    textxml = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="5" templateID="1" action="test" brief="[色图]" sourceMsgId="0" url="" flag="2" adverSign="0" multiMsgFlag="0"><item layout="0"><image uuid="$md5.png" md5="$md5" GroupFiledid="0" filesize="38504" local_path="" minWidth="$x" minHeight="$y" maxWidth="$mx" maxHeight="$my" /></item><source name="$ext" icon="" action="web" url="$url" appid="-1" /></msg>'''
                    textxml = textxml.replace('$md5',pmd5)\
                        .replace('$x',str(mmx))\
                        .replace('$y',str(mmy))\
                        .replace('$mx',str(mmx))\
                        .replace('$my',str(mmy))\
                        .replace('$ext',ext)\
                        .replace('$url',outmsg['url'])
                        #.replace('$size',str(size))
                    outxml = [Xml(textxml)]
                    await app.sendGroupMessage(group,MessageChain.create(outxml))
                    try:
                        if outmsg['extmsg'] != '':
                            await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg['extmsg'])]))
                    except:pass
                    return
                try:
                    await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile(outmsg['imgpath'])]))
                except:pass
                try:
                    if outmsg['extmsg'] != '':
                        await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg['extmsg'])]))
                except:pass
                await asyncio.sleep(1)
#R18色图
    elif msg.startswith('不够色') and group.id in cfg['r18_group']:
        msg = msg.replace('不够色','').replace(' ','')
        sc = ''
        if msg == '':
            num = 1
        else:
            try:
                num = int(msg)
            except:
                num = 1
                sc = msg
        if num == 0:pass
        elif num > 10:pass
        else:
            for i in range(num):
                outmsg = await setu(1,member.id,group.id,sc)
                if cfg['xml'] == 1:
                    chace1 = await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile(outmsg['imgpath'])]))
                    await asyncio.sleep(1)
                    await app.revokeMessage(chace1)
                    filepach = outmsg['imgpath']
                    fd = open(filepach, "rb")
                    f = fd.read()
                    pmd5 = hashlib.md5(f).hexdigest()
                    inputimg = Im.open(filepach)
                    mmx = inputimg.size[0]
                    mmy = inputimg.size[1]
                    tags = ' '.join(outmsg['tags'])

                    ext =" $title by $author |pid:$pid uid:$uid |tags:$tags"\
                    .replace('$title',outmsg['title'])\
                    .replace('$author',outmsg['author'])\
                    .replace('$pid',str(outmsg['pid']))\
                    .replace('$uid',str(outmsg['uid']))\
                    .replace('$tags',tags)

                    dxy = str(1000)
                    print(pmd5)
                    textxml = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="5" templateID="1" action="test" brief="[色图]" sourceMsgId="0" url="" flag="2" adverSign="0" multiMsgFlag="0"><item layout="0"><image uuid="$md5.png" md5="$md5" GroupFiledid="0" filesize="38504" local_path="" minWidth="$x" minHeight="$y" maxWidth="$mx" maxHeight="$my" /></item><source name="$ext" icon="" action="web" url="$url" appid="-1" /></msg>'''
                    textxml = textxml.replace('$md5',pmd5)\
                        .replace('$x',str(mmx))\
                        .replace('$y',str(mmy))\
                        .replace('$mx',str(mmx))\
                        .replace('$my',str(mmy))\
                        .replace('$ext',ext)\
                        .replace('$url',outmsg['url'])
                    outxml = [Xml(textxml)]
                    await app.sendGroupMessage(group,MessageChain.create(outxml))
                    try:
                        if outmsg['extmsg'] != '':
                            await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg['extmsg'])]))
                    except:pass
                    return
                try:
                    await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile(outmsg['imgpath'])]))
                except:pass
                try:
                    if outmsg['extmsg'] != '':
                        await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg['extmsg'])]))
                except:pass
                await asyncio.sleep(1)
#Experimental_xml_setu
    elif msg.startswith('Experimental_xml_setu'):
        msg = msg.replace('Experimental_xml_setu','').replace(' ','')
        if msg == 'on':
            cfg['xml'] = 1
            await app.sendGroupMessage(group,MessageChain.create([(Plain('已开启'))]))
        elif msg == 'off':
            cfg['xml'] = 0
            await app.sendGroupMessage(group,MessageChain.create([(Plain('已关闭'))]))
        else :pass
#help
    elif msg.startswith('/帮助'):
        text = helptext
        await app.sendGroupMessage(group,MessageChain.create([Plain(text)]))
#test
    elif msg.startswith('test'):
        path = './chace/ak.png'
        fd = open(path, "rb")
        f = fd.read()
        pmd5 = str.upper(hashlib.md5(f).hexdigest())
        inputimg = Im.open(path)
        mmx = inputimg.size[0]
        mmy = inputimg.size[1]
        size = getsize(path)
        chace1 = await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile(path)]))
        print(chace1)
        url = 'http://gchat.qpic.cn/gchatpic_new/0/0-0-md5/0'.replace('md5',pmd5)
        await app.revokeMessage(chace1)

        #textxml = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="5" templateID="1" action="test" brief="[色图]" sourceMsgId="0" url="" flag="2" adverSign="0" #multiMsgFlag="0"><item><image uuid="$md5.png" md5="$md5" GroupFiledid="0" filesize="$size" local_path="" minWidth="$x" minHeight="$y" maxWidth="$mx" maxHeight="$my" /></item><source #name="$ext" icon="" action="web" url="$url" appid="-1" /></msg>'''
        #textxml = textxml.replace('$md5',pmd5)\
        #    .replace('$x',str(mmx))\
        #    .replace('$y',str(mmy))\
        #    .replace('$mx',str(mmx))\
        #    .replace('$my',str(mmy))\
        #    .replace('$size',str(size))
        textxml = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="23" templateID="1" action="web" brief="51神韵博客" sourceMsgId="0" url="跳转网址" flag="0" adverSign="0" multiMsgFlag="0"><item layout="5"><picture cover="$url" w="0" h="0" /></item><source name="" icon="" action="" appid="-1" /></msg>'''
        textxml = textxml\
            .replace('$url',url)
        print(mmx,mmy,pmd5)

 
        await app.sendGroupMessage(group,MessageChain.create([(Json(textxml))]))
#排行榜
    elif msg.startswith('排行榜') and group.id in setu_group:
        msg = msg.replace('排行榜','').replace(' ','')
        mo = 'day'
        if group.id in r18_group:
            if msg.startswith('day_r18'):mo = 'day_r18'
            if msg.startswith('week_r18'):mo = 'week_r18'
            if msg.startswith('week_r18g'):mo = 'week_r18g'
        else:
            if msg.startswith('week'):mo = 'week'
            if msg.startswith('month'):mo = 'month'
        rank_list = api.illust_ranking(mode=mo)
        rank_list = rank_list['illusts']
        n = 0
        msglist = [[(Plain('pixiv排行榜:'))]]
        cfg['plinfodata'][str(group.id)] = []
        for i in rank_list :
            p_ing = {}
            p_ing['url'] = []
            print(i)
            if n == 5 : break
            n = n + 1
            p_ing['pid'] = i['id']
            p_ing['uid'] = i['user']['id']
            p_ing['title'] = i['title']
            p_ing['user'] = i['user']['name']
            p_ing['tags'] = []
            for tag in i['tags']:
                p_ing['tags'].append(tag['name'])
            try:
                p_ing['url'].append(i['meta_single_page']["original_image_url"])
            except :
                for u in i['meta_pages']:
                    p_ing['url'].append( u["image_urls"]['original'])
            savepath = './listpiv/'+ str(group.id) + '/' + str(n) + '.png'
            savefl = './listpiv/'+ str(group.id) 
            sdir(savefl)
            p_ing['path'] = savepath
            print(p_ing['url'])

            await DF.adf(p_ing['url'][0],savepath)
            fd = open(savepath, "rb")
            f = fd.read()
            pmd5 = hashlib.md5(f).hexdigest()
            p_ing['md5'] = pmd5 
            cfg['plinfodata'][str(group.id)].append(p_ing)
            print(str(p_ing))
            ioutmsg = (Plain('\n' + str(n) + '.' + p_ing['title']))
            iimg = (Image.fromLocalFile(savepath))
            msglist.append([ioutmsg,iimg])
            p_ing = {}
        msglist.append([(Plain('使用tp 1~5来查看色图详情'))])
        for i in msglist:
            await app.sendGroupMessage(group,MessageChain.create(i))
            await asyncio.sleep(3)
    elif msg.startswith('tp'):
        msg = msg.replace(' ','').replace('tp','')
        try:
            mint = int(msg) - 1
        except:return
        p_ing = cfg['plinfodata'][str(group.id)][mint]
        tags = ' '.join(p_ing['tags'])
        inputimg = Im.open(p_ing['path'])
        mmx = inputimg.size[0]
        mmy = inputimg.size[1]
        if cfg['xml'] == 1:
            textxml = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="5" templateID="1" action="test" brief="[色图]" sourceMsgId="0" url="" flag="2" adverSign="0" multiMsgFlag="0"><item layout="0"><image uuid="$md5.png" md5="$md5" GroupFiledid="0" filesize="38504" local_path="" minWidth="$x" minHeight="$y" maxWidth="$mx" maxHeight="$my" /></item><source name="$ext" icon="" action="web" url="$url" appid="-1" /></msg>'''
            ext =" $title by $author |pid:$pid uid:$uid |tags:$tags"\
                    .replace('$title',p_ing['title'])\
                    .replace('$author',p_ing['user'])\
                    .replace('$pid',str(p_ing['pid']))\
                    .replace('$uid',str(p_ing['user']))\
                    .replace('$tags',tags)
            textxml = textxml.replace('$md5',p_ing['md5'])\
                .replace('$x',str(mmx))\
                .replace('$y',str(mmy))\
                .replace('$mx',str(mmx))\
                .replace('$my',str(mmy))\
                .replace('$ext',ext)\
                .replace('$url',p_ing['url'])
            outmsg = [Xml(textxml)]
        else:
            print(len(p_ing['url']))
            outmsg = []
            if len(p_ing['url']) > 1:
                n = 0
                for i in p_ing['url']:
                    n += 1
                    savepath = p_ing['path'].replace('.png','_' + str(n) + '.png')
                    print(savepath)
                    await DF.adf(i,savepath)
                    outmsg.append((Image.fromLocalFile(savepath)))
            else:outmsg = [].append((Image.fromLocalFile(p_ing['path'])))
            urlstr = p_ing['url'][0]
            urlstr = urlstr[:-3]
            outmsg.append((Plain(infomap\
                .replace('title',p_ing['title'])\
                .replace('author',p_ing['user'])\
                .replace('$uid',str(p_ing['uid']))\
                .replace('$pid',str(p_ing['pid']))\
                .replace('tags',tags)\
                .replace('mx',str(mmx))\
                .replace('my',str(mmy))\
                .replace('url',urlstr))))
        print(outmsg)
        for i in outmsg:
            await app.sendGroupMessage(group,MessageChain.create([i]))
            await asyncio.sleep(2)
#restart
    elif msg.startswith('restart') and member.id in admin:
        await app.sendGroupMessage(group,MessageChain.create([Plain('执行重启项目----')]))
        restart_program()
#明日方舟企鹅物流物品查询
    elif msg.startswith('ak'):
        msg = msg.replace('ak','').replace(' ','').replace('－','-')
        if msg.startswith('rm') and member.id in admin:
            await dakm()
            await app.sendGroupMessage(group,MessageChain.create([Plain('企鹅物流 - akm 数据下载完成')]))
        if msg.startswith('ri') and member.id in admin:
            await daki()
            await app.sendGroupMessage(group,MessageChain.create([Plain('企鹅物流 - aki 数据下载完成')]))
        if msg.startswith('rs') and member.id in admin:
            await daks()
            await app.sendGroupMessage(group,MessageChain.create([Plain('企鹅物流 - aks 数据下载完成')]))
        if msg.startswith('ra') and member.id in admin:
            await dakm()
            await daki()
            await daks()
            restart_program()
        if msg.startswith('s'):
            msg = msg.replace('s','')
            outdata = {}
            i = {}
            for i in aks_data:
                if msg == i['name']:outdata = i
            if outdata == {} : outmsg = '无结果'
            else:
                sname = await rep(12,outdata['name'])
                scost = await rep(23,str(outdata['apCost']))
                stime0 = await settime(outdata['minClearTime'])
                stime = await rep(41,str(stime0))
                outmsg = aks_map\
                    .replace('sname(12)///',sname)\
                    .replace('scost(23)//////////////',str(scost))\
                    .replace('stime(41)////////////////////////////////',str(stime))
                msglist = []
                for i in outdata['dropInfos']:
                    rarity = 1
                    name = ''
                    outdata2 = {}
                    for o in aki_data:
                        try:
                            if o['itemId'] == i['itemId']:
                                name = o['alias'][0]
                                rarity = o['rarity']
                                break
                        except:pass
                    if name =='':pass
                    else:
                        if rarity == 0: cl = '#FFFFFF\\'
                        elif rarity == 1: cl = '#DFE961\\'
                        elif rarity == 2: cl = '#1AA5E1\\'
                        elif rarity == 3: cl = '#D282DA\\'
                        elif rarity == 4: cl = '#EDCB26\\'
                        else: cl = '#FFFFFF\\'
                        try:
                            aimg = '\\p./aki_30/id.png\\'.replace('id',i['itemId'])
                            aimg_p = './aki_30/id.png'.replace('id',i['itemId'])
                            img = Im.open(aimg_p)
                        except:
                            aimg = '  '
                        dname = cl + aimg + await rep(14,name)
                        num = str(i['bounds']['lower']) + '~' + str(i['bounds']['upper'])
                        if i['dropType'] == "EXTRA_DROP":num = num + 'ex'
                        dnum = await rep(6,num)
                        plist = []
                        for p in akm_data:
                            if p['stageId'] == outdata['stageId']:
                                plist.append(p)
                        for a in plist:
                            try:
                                if a['itemId'] == i['itemId']:
                                    outdata2 = a
                                    break
                            except:pass
                        if outdata2 == {}:continue
                        else:
                            quantity = outdata2['quantity']
                            times = outdata2['times']
                            if quantity == 0 or times == 0:
                                continue
                            rate = quantity / times
                            prate = rate * 100
                            drate = await rep(7,str(round(prate,2)))
                            lz = round( outdata['apCost'] / rate ,2)
                            dlz = await rep(8,str(lz))
                            time = outdata['minClearTime'] / rate
                            atime = await settime(time)
                            dtime = await rep(9,str(atime))
                        listp = str(math.floor(round(prate,0))).rjust(3,'0')
                        imsg = listp + aks_map2.replace('#FFFFFF\\name(24)////////',dname)
                        imsg = imsg.replace('num(6)',dnum)
                        imsg = imsg.replace('rate(7)',str(drate + '%'))
                        imsg = imsg.replace('lz(8)////',str(dlz))
                        imsg = imsg.replace('time(9)//',str(dtime))
                        print(name,dnum,drate,dlz,dtime)
                        msglist.append(imsg)
                        msglist.sort(reverse=True)
                for i in msglist:
                    i = i[3:]
                    outmsg = outmsg + i
                outmsg = outmsg + aks_map3
                print(outmsg)
                toimg(outmsg,img = "./chace/ak.png" )
                await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile("./chace/1.png")]))
        if msg.startswith('i'):
            cost = 1
            stime0 = 1
            sname = ''
            dnum = 0
            iid = ''
            msg = msg.replace('i','')
            outdata = {}
            for i in aki_data:
                for o in i['alias']:
                    if o == msg:
                        outdata = i
                        iid = i['itemId']
                        break
            iname = await rep(12,outdata['alias'][0])
            irarity = outdata['rarity']
            alias = outdata['alias']
            del alias[0]
            ialias = await rep(45,str(alias))
            ilist = []
            try:
                aimg = '\\p./aki_60/id.png\\    '.replace('id',iid)
                aimg_p = './aki_60/id.png'.replace('id',iid)
                img = Im.open(aimg_p)
            except:
                aimg = '  '
            outmsg = aki_map\
                .replace('图片',aimg)\
                .replace('iname(12)///',iname)\
                .replace('$r',str(irarity) + ' ')\
                .replace('stime(41)////////////////////////////////',str(ialias))
            for i in akm_data:#提取
                if i['itemId'] == outdata['itemId']:
                    ilist.append(i)
            msglist =[]
            for o in ilist:#要处理的akm数据 o
                for p in aks_data:#读取物品此时的aks数据 p
                    if o['stageId'] == p['stageId']:
                        sname = '#FFFFFF\\' + await rep(16,p['name'])
                        try:
                            cost = p['apCost']
                            stime0 = p['minClearTime']
                        except:continue
                        for a in p['dropInfos']:#读取p此时的dropInfos a
                            try:
                                if a['itemId'] == iid:
                                    num = str(a['bounds']['lower']) + '~' + str(a['bounds']['upper'])
                                    dnum = await rep(6,num)
                            except:pass

                quantity = o['quantity']
                times = o['times']
                if quantity == 0 or times == 0:
                    continue
                rate = quantity / times
                prate = rate * 100
                drate = await rep(7,str(round(prate,2)))
                lz = round( cost / rate ,2)
                dlz = await rep(8,str(lz))
                time = stime0 / rate
                atime = await settime(time)
                dtime = await rep(9,str(atime))
                listp = str(math.floor(round(prate,0))).rjust(3,'0')
                imsg = ''
                imsg = listp + aks_map2.replace('#FFFFFF\\name(24)////////',sname)
                imsg = imsg.replace('num(6)',dnum)
                imsg = imsg.replace('rate(7)',str(drate + '%'))
                imsg = imsg.replace('lz(8)////',str(dlz))
                imsg = imsg.replace('time(9)//',str(dtime))
                print('获取完毕:',sname,dnum,drate,dlz,dtime)
                msglist.append(imsg)
                msglist.sort(reverse=True)
            for i in msglist:
                i = i[3:]
                outmsg = outmsg  + i + '\n'
            outmsg = outmsg + '\n' + aks_map3
            print(outmsg)

            img = "./chace/ak.png"
            toimg(outmsg,img)
            await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile("./chace/1.png")]))    
#色图info
    elif msg.startswith('info'):
        outmsg = last_setu[str(group.id)]
        await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg)]))
#debug
    elif msg.startswith('debug'):
        id = str(member.id)
        info = 'hsolv_data=' +  str(hsolv_data[id]) + '\nhsolvlist_data=' + str(hsolvlist_data[id]) + '\nqd_data=' + str(qd_data[id]) + '\nqdlist_data=' + str(qdlist_data[id])
        await app.sendGroupMessage(group,MessageChain.create([Plain(info)]))
#hsolv
    elif msg.startswith("hsolv") and member.id in admin:
        msg = msg.replace("hsolv",'')
#-重置色图
        if msg.startswith('r') and member.id in admin:
            outmsg = "所有当天获取色图次数被重置"
            for i in qdlist_data:
                qd_data[i] = 0
            await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg)]))
            savecfg()
            srcfile='./cfg.json'
            name = Time.strftime('%Y-%m-%d-%H',Time.localtime(Time.time()))
            dstfile='./backups/'+ name + '.json'
            shutil.move(srcfile,dstfile)
#-增加色图
        elif msg.startswith('+') and member.id in admin:
            id = msg.replace("+","").replace(' ','')
            hsolv_data[id] = hsolv_data[id] + 10
            outmsg = str(id) + "的色图增加了10"
            await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg)]))
            savecfg()
#-LSP排行榜
        elif msg.startswith('list'):
            print("list读取")
            groupids = []
            hsolvlist = []
            n = 0
            mlist = await app.memberList(group)
            for i in mlist:
                groupids.append(i.id)
            for item in hsolvlist_data:
                try:
                    if int(item) in groupids != 0:
                        for i in mlist:
                            if i.id == int(item) != 0:
                                itemid = await app.getMember(group,int(item))
                                inmsg = '$item:$int'.replace('$item',itemid.name).replace('$int',str(hsolvlist_data[item]))
                                hsolvlist.append(str(inmsg))
                except:
                    print('err')
                    await app.sendGroupMessage(group,MessageChain.create([Plain('执行此命令时发生了错误')]))

            res = sorted(hsolvlist, key=lambda x: (lambda y: (int(y[1]), y[0]))(x.split(':')))
            res.reverse()
            out = ''
            for i in res:
                if n == 0:
                    for i in res[n]:
                        r = random.randint(0,18)
                        out = out + '\\' + hsomap[r] + '\\' + ''.join(i)
                    
                    res[n] = '\\b20\\ \\b30\\' + out + '\\b25\\\\#FF0000\\'
                elif n == 1:
                    res[n] = res[n] + '\\b20\\\\#FF3300\\'
                elif n == 3:
                    res[n] =  res[n] + '\\#FF6600\\'
                elif n == 6:
                    res[n] = res[n] + '\\#FF9900\\'
                elif n == 9:
                    res[n] = res[n] + '\\#FFCC00\\'
                elif n == 12:
                    res[n] = res[n] + '\\#FFFF00\\'
                elif n == 15:
                    res[n] = res[n] + '\\#FFFF66\\'
                elif n == 18:
                    res[n] = res[n] + '\\#FFFFCC\\'
                elif n == 21:
                    res[n] = res[n] + '\\#FFFFFF\\'

                res[n] = res[n] + ' \\n0\\ '
                n = n + 1
            a = ''.join(res)
            msg = "-lsp排行榜:\\#FF0000\\ \\n0\\" + a + "\\n0\\    \\n0\\\y0\\\\b20\\\\#FFFFFF\\ "
            for i in res:
                msg = msg + '\\n0\\|'
            for i in range(3):
                msg = msg + '\\n0\\|'
            print(msg)
            toimg(msg)
            await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile("./chace/1.png")]))
#-显示hsolv等级
        else:
            print("printhsolv")
            id = int(msg.replace("-","").replace(' ',''))
            mid = 0
            mid = int(hsolvlist_data[str(id)])
            outmsg = str(id) + "的hso等级为" + str(mid)
            await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg)]))
#备份
    elif msg.startswith('backup') and member.id in admin:
        savecfg()
        srcfile='./cfg.json'
        name = Time.strftime('%Y-%m-%d-%H',Time.localtime(Time.time()))
        dstfile='./backups/'+ name + '.json'
        shutil.move(srcfile,dstfile)
        outmsg = name + '已备份'
        await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg)]))
#色图群权限管理
    elif msg.startswith('sg setu') and member.id in admin:
        if group.id in cfg['setu_group']:
            outmsg = '此群已经是色图群'
            if msg.endswith('-'):
                cfg['setu_group'].remove(group.id);outmsg = '此群不再是色图群'
        else: cfg['setu_group'].append(group.id) ; outmsg = '已变成色图群'
        await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg)]))
#r18群权限管理
    elif msg.startswith('sg r18'):
        if group.id in cfg['r18_group'] and member.id in admin:
            outmsg = '此群已经是r18群'
            if msg.endswith('-'):
                cfg['r18_group'].remove(group.id);outmsg = '此群不再是r18群'
        else: cfg['r18_group'].append(group.id) ; outmsg = '已变成r18群'
        await app.sendGroupMessage(group,MessageChain.create([Plain(outmsg)]))
#后处理项目
    savecfg()
    initDate = datetime.strptime(cfg['time'],'%Y-%m-%d %H:%M:%S')
    timedata = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timedata2 = datetime.strptime(timedata,'%Y-%m-%d %H:%M:%S')
    firstDay = datetime(initDate.year,initDate.month,initDate.day)
    endDay = datetime(timedata2.year,timedata2.month,timedata2.day)
    days = rrule.rrule(freq = rrule.DAILY,dtstart=firstDay,until=endDay)
    if days.count() >= 2:
        await app.sendGroupMessage(group,MessageChain.create([Plain('执行自动重启项目----')]))
        daki()
        daks()
        dakm()
        if not os.path.exists('./backups'):
            os.makedirs('./backups')
        srcfile='./cfg.json'
        name = Time.strftime('%Y-%m-%d-%H',Time.localtime(Time.time()))
        dstfile='./backups/'+ name + '.json'
        shutil.move(srcfile,dstfile)
        timenow = datetime.now().strftime('%Y-%m-%d 10:10:10')
        cfg['time'] = timenow
        for i in qd_data:
            qd_data[i] = 0
        cfg['setu_l'] = 0
        savecfg()
        restart_program()

app.launch_blocking()