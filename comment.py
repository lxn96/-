import jieba
import wordcloud

def stop_words(texts, stopname):
    words_list = []
    word_generator = jieba.cut(texts, cut_all=False)  # 返回的是一个迭代器
    with open(stopname) as f:
        str_text = f.read()
        unicode_text = str_text  # 把str格式转成unicode格式
        f.close()  # stopwords文本中词的格式是'一词一行'
    for word in word_generator:
        if word.strip() not in unicode_text:
            words_list.append(word)
    return ' '.join(words_list)  # 注意是空格

openname = input('输入打开文件名（.txt结尾：)')
stopname = input('输入忽略词文件名（.txt结尾：)')
savename = input('输入保存图片名（.png结尾：)')
maxword = eval(input('输入词云显示词语个数：'))
f = open(openname, 'r')
comments = ''
for i in f:
    i = i.split()
    comment = i[2] + ' '
    comments += comment
f.close()
word = stop_words(comments, stopname)
w = wordcloud.WordCloud(font_path="msyh.ttc",  width=1000, height=700,\
    background_color="white", max_words=maxword)
w.generate(word)
w.to_file(savename)