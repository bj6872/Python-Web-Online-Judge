import socket
import webbrowser

def username(x):  # 根据 id 返回用户名的 HTML 标签
    return '<b style="color:#e74c3c">zxd</b>'

ip = "192.168.101.24"
port = 8866
data = ans = head = ""

def find_label(text):  # 寻找标签
    ans = []
    flag = 0
    for i in range(len(text) - 6):
        if text[i : (i + 6)] == '@label':
            flag = 1
            continue
        if flag == 1:
            if text[i] == ' ':
                continue
            if text[i] == '[':
                flag = 2
                ans.append('')
        elif flag == 2:
            if text[i] == ']':
                flag = 0
                continue
            ans[len(ans) - 1] += text[i]
    return ans

def label_define(user, page, label):  # 标签定义（要写代码）
    if label == 'problems':  # 问题列表
        file = open('data/pindex.txt', 'r', encoding='utf-8')
        data = file.read()
        file.close()
        data = data.split('\n')
        data = [i.split(' ')  for i in data]

        ans = '<table border="0"><tr>'
        for i in ['编号&nbsp;', '难度', '名称']:
            ans += '<td style="font-size:2px">' + i + '</td>'
        ans += '</tr>'
        
        for i in range(len(data)):
            ans += '<tr>'
            for j in range(len(data[i])):
                if j == 0:
                    ans += '<td>' + data[i][j] + '</td>'
                elif j == 1:
                    if data[i][j] == 'A':
                        elem = '<b style="color:#e74c3c">入门</b>'
                    elif data[i][j] == 'B':
                        elem = '<b style="color:#f39c11">普及</b>'
                    elif data[i][j] == 'C':
                        elem = '<b style="color:#ffc116">中等</b>'
                    elif data[i][j] == 'D':
                        elem = '<b style="color:#52c41a">提高</b>'
                    elif data[i][j] == 'E':
                        elem = '<b style="color:#3498db">省选</b>'
                    elif data[i][j] == 'F':
                        elem = '<b style="color:#9d3dcf">顶尖</b>'
                    else:
                        elem = '<p style="color:#bbbbbb">未知</b>'
                    ans += '<td>' + elem + '&nbsp;</td>'
                else:
                    ans += '<td><a href="/problems/' + data[i][0] + '">' + data[i][j] + '</a></td>'
            ans += '</tr>'
        ans += '</table><br />'
        return ans

    if label == 'one-problem':  # 单个问题
        file = open('data/problems/' + str(page[10:]) + '.txt', 'r', encoding='utf-8')
        data = file.read().split('\n')
        file.close()
        ans = ''
        for i in range(1, len(data)):
            ans += data[i]
        data = data[0].split(' ')
        return '<h1>' + data[0] + '</h1>' + ans

    if label[:3] == 'op-':  # 单个问题中的一些标签
        file = open('data/problems/' + str(page[10:]) + '.txt', 'r', encoding='utf-8')
        data = file.read().split('\n')[0].split(' ')
        file.close()
        # data - 第一行存储的数据，分别为：题目、难度、
        #        贡献者或来源（* 或 A|B|C）、标签（同上）
        if label == 'op-dfcty':  # 难度
            if data[1] == 'A':
                return '<b style="color:#e74c3c">入门</b>'
            elif data[1] == 'B':
                return '<b style="color:#f39c11">普及</b>'
            elif data[1] == 'C':
                return '<b style="color:#ffc116">中等</b>'
            elif data[1] == 'D':
                return '<b style="color:#52c41a">提高</b>'
            elif data[1] == 'E':
                return '<b style="color:#3498db">省选</b>'
            elif data[1] == 'F':
                return '<b style="color:#9d3dcf">顶尖</b>'
            else:
                return '<b style="color:#bbbbbb">未知</b>'
        if label == 'op-from':  # 来源及贡献者
            if data[2] == '*':
                return ''
            else:
                ans = ''
                data = data[2].split('|')
                for i in data:
                    try:
                        int(i)
                    except:
                        ans += '<tr><td>题目来源</td><td style="float:right">' + i + '</td></tr>'
                        continue
                    ans += '<tr><td>题目提供者</td><td style="float:right">' + username(int(i)) + '</td></tr>'
                return ans
        if label == 'op-score':  # 历史分数
            return '无'
        if label == 'op-label':  # 标签
            if data[3] == '*':
                return '无'
            else:
                ans = ''
                data = data[3].split('|')
                for i in data:
                    if ans == '':
                        ans += i
                    else:
                        ans += '，' + i
                return ans
    return '<!-- Error -->'

def fill_label(text, labels, auto, user=None, page=None):  # 填充标签
    if auto == True:
        filled_labels = [label_define(user, page, i)  for i in labels]
    else:
        filled_labels = labels
    ans = ''
    cnt = 0
    flag = False
    for i in range(len(text)):
        if i + 6 < len(text) and text[i : (i + 6)] == '@label':
            flag = True
        if flag == True and text[i] == ']':
            flag = False
            ans += filled_labels[cnt]
            cnt += 1
            continue
        if flag == False:
            ans += text[i]
    return ans

def retpage(user, page, real_page):  # 自动处理页面
    file = open(real_page, encoding='utf-8')
    answer = file.read()
    file.close()
    labels = find_label(answer)
    answer = fill_label(answer, labels, True, user=user, page=page)
    return [200, 'text/html', answer]

def answer(user, page):  # 返回函数（在这里编写代码）
    print(user, page)
    if page == '/' or page == '':  # 主页
        return retpage(user, page, 'pages/index.html')
    
    if page == '/style.css':  # 默认 CSS
        file = open('pages/style.css', encoding='utf-8')
        answer = file.read()
        file.close()
        return [200, 'text/css', answer]
    
    if page == '/problems':  # 题目列表
        return retpage(user, page, 'pages/problem.html')

    if page[:10] == '/problems/':  # 单个题目
        try:
            pid = int(page[10:])
            flag = False
            file = open('data/pindex.txt', 'r', encoding='utf-8')
            data = file.read()
            file.close()
            data = data.split('\n')
            for i in data:
                if int(i.split(' ')[0]) == pid:
                    flag = True
            if flag == False:
                return [404]
        except:
            return [404]
        return retpage(user, page, 'pages/onep.html')

    return[404]  # 不存在的内容


so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.bind((ip, port))

so.listen(4)
webbrowser.open('http://192.168.101.24:8866/')

while True:
    conn, addr = so.accept()
    data = bytes.decode(conn.recv(1024))
    data = data.split()
    ans = answer(addr[0], data[1])
    if ans[0] == 200:
        head = 'HTTP/1.1 200 OK\nContent-type: ' + ans[1] +'; charset="utf-8"\n\n'  # 拼接 Response 头
        conn.sendall(str.encode(head + ans[2]))
    elif ans[0] == 301:
        head = 'HTTP/1.1 301 Permanently Moved\nLocation: ' + ans[1] + '\n\n<html><head></head><body></body></html>'
        conn.sendall(str.encode(head))
    elif ans[0] == 404:
        head = 'HTTP/1.1 404 Object Not Found\nContent-type: text/html; charset="utf-8"\n\n'
        file = open('pages/error.html', 'r', encoding='utf-8')
        content = file.read()
        file.close()
        conn.sendall(str.encode(head + content))
    conn.shutdown(2)
    conn.close()
    del conn
