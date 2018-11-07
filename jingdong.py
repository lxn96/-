import requests
import json

def GetUrlText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def CommentSum(comj):
    imag = comj['imageListCount']
    coms = comj['productCommentSummary']
    label = ['产品ID', '总评数', '好评数', '好评率', '中评数', '中评率', '差评数', '差评率', '追评数', '晒图数', '视频晒单', 'DefaultGoodCount']
    comslist = [label]
    t = [coms['productId'], coms['commentCount'], coms['goodCount'], coms['goodRate'], coms['generalCount'], coms['generalRate'], coms['poorCount'], coms['poorRate'], coms['afterCount'], imag, coms['videoCount'], coms['defaultGoodCount']]
    comslist.append(t)
    return comslist

def KeywordsGet(key):
    label = ['评论热门词', '次数']
    keyword = [label]
    for keydict in key:
        name = keydict['name']
        count = keydict['count']
        keyword.append([name, count])
    return keyword

def AfterComGet(comment):
    after = []
    if comment['afterDays'] != 0:
        after.append(comment['afterDays'])
        after.append(comment['afterUserComment']['hAfterUserComment']['content'])
    else:
        after = [0, 0]
    return after
def CommentGet(comment):
    content =  comment['content']
    a = content.replace('\n', ' ')
    return a.replace(u'\ufffd', '')
def TimeGet(comments):
    referencetime = comments['referenceTime']
    creationtime = comments['creationTime']
    days = comments['days']
    time = [referencetime, creationtime, days]
    return time
def ScoreGet(comment):
    return comment['score']
def UsefulGet(comment):
    return comment['usefulVoteCount']
def ReplyGet(comment):
    return comment['replyCount']

def Get(urldemo, maxpage):
    label = ['序号', '星', '评论内容', '购买时间', '评论时间', '天数差', '追评天数', '追评内容', '有用数', '回复数']
    comments = [label]
    i = 0
    for page in range(maxpage):
        pages = str(page)
        url = urldemo + pages
        html = GetUrlText(url)
        comj = json.loads(html.lstrip('fetchJSON_comment98vv67701(').rstrip(');'))
        com = comj['comments']
        for comment in com:
            after = AfterComGet(comment)
            content = CommentGet(comment)
            time = TimeGet(comment)
            score = ScoreGet(comment)
            useful = UsefulGet(comment)
            reply = ReplyGet(comment)
            i += 1
            comments.append([i, score, content, time[0], time[1], time[2], after[0], after[1], useful, reply])
    return comments

def AnswerGet(answerurldemo, ansmaxpage):
    label = ['序号', '创建时间', '回答数量', '最新回答时间']
    answers = [label]
    i = 0
    for page in range(ansmaxpage+1):
        if page > 0:
            pages = str(page)
            url = answerurldemo + pages
            html = GetUrlText(url)
            ansj = json.loads(html.lstrip('jQuery8012345(').rstrip(');'))
            ans = ansj['questionList']
            for answer in ans:
                i +=1
                answers.append([i, answer['created'], answer['answerCount'], answer['lastAnswerTime']] )
    return answers


def Saved(fname, coms, key, com, answer):
    f = open(fname, 'w', encoding='GB18030')
    for x in coms:
        for y in x:
            f.write(str(y) + '\t')
        f.write('\n')
    f.write('\n')
    for x in key:
        for y in x:
            f.write(str(y) + '\t')
        f.write('\n')
    f.write('\n')
    for x in com:
        for y in x:
            f.write(str(y) + '\t')
        f.write('\n')
    f.write('\n')
    for x in answer:
        for y in x:
            f.write(str(y) + '\t')
        f.write('\n')
    f.close()


def main():
    product = input('输入产品ID：')
    maxpage = input('输入评论最大页数：')
    ansmaxpage = input('输入问答最大页数：')
    fname = input("输入存储文件名（.xls结尾）：")
    maxpage = eval(maxpage)
    ansmaxpage = eval(ansmaxpage)
    urldemo = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv67701&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&productId=' + product + '&page='
    url = urldemo + '0'
    html = GetUrlText(url)
    comj = json.loads(html.lstrip('fetchJSON_comment98vv67701(').rstrip(');'))
    coms = CommentSum(comj)
    key = KeywordsGet(comj['hotCommentTagStatistics'])
    answerurldemo = 'https://question.jd.com/question/getQuestionAnswerList.action?callback=jQuery8012345&productId=' + product + '&page='
    com = Get(urldemo, maxpage)
    answer = AnswerGet(answerurldemo, ansmaxpage)
    Saved(fname, coms, key, com, answer)
main()