# 需要修改的参数如下
from dataclasses import replace

COOKIE = \
    "_abfpc=45e0182901d28e785e4d95772015cc67ebae97f3_2.0; cna=c4ca863cc5cf6488466fc35c55869199; mode_type=normal; UM_distinctid=195517eccc47a8-0481b9b37a1e0a-296e4933-3d10d-195517eccc5cce; CNZZDATA1281406241=297351484-1740829019-https%253A%252F%252Fwww.xuetangx.com%252F%7C1742019406; provider=xuetang; django_language=zh; point={%22point_active%22:true%2C%22platform_task_active%22:true%2C%22learn_task_active%22:true}; login_type=E; csrftoken=x1kp5qCYDIs1NqVSDdGD4p4oCB4CRhGL; sessionid=3ok86fvnyz2m4iak4qmtvyykj50b7xqp; k=88644769; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2288644769%22%2C%22first_id%22%3A%22195515174c447b-0df325b71912c08-26011a51-921600-195515174c5669%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22195515174c447b-0df325b71912c08-26011a51-921600-195515174c5669%22%7D; JG_016f5b1907c3bc045f8f48de1_PV=1743158870910|1743158926020"
HOMEWORK_URL = \
    "https://www.xuetangx.com/h5/homework/bitP0854KC007977/23901367/58564584?avatar=https%3A%2F%2Fstoragecdn.xuetangx.com%2Fpublic_assets%2Fxuetangx%2Fimages%2Fb6ce32912ffa1c5959b0da6ceb9ce27e.avatar%402x.png&name=&user_number=null&term=latest&university_id=0&user_role=null&sessionid=null&csrftoken=undefined&xtbz=xt&django-language=zh"

import json
import requests
import re

def escape_for_markdown(str):
    str = str.replace('&nbsp;', ' ')
    str = re.sub(r'<[^>]+>', '', str)

    special_characters = r'\*_{}`[]()#+-.!|'
    for char in special_characters:
        str = str.replace(char, fr'\{char}')
    return str.replace('&', r'&amp;').replace('<', r'&lt;')

UID = ''
CID = ''
EID = ''

# 从 HOMEWORK_URL 中提取关键参数
pattern = r'/homework/([^/]+)/([^/]+)/([^/?]+)'
match = re.search(pattern, HOMEWORK_URL)
if match:
    UID = match.group(1)
    CID = match.group(2)
    EID = match.group(3)
    print(f"UID: {UID}, CID: {CID}, EID: {EID}")
else:
    print("No match found")

headers = {
    'authority': 'www.xuetangx.com',
    'accept': 'application/json, text/plain, */*',
    'django-language': 'zh',
    'x-client': 'web',
    'accept-language': 'zh',
    'xtbz': 'xt',
    'user-agent': 'jdapp;android;8.4.2;8.0.0;;network/wifi;model/Mi Note 2;osVer/26;appBuild/71043;psn/|7;psq/1;uid/;adk/;ads/;pap/JA2015_311210|8.4.2|ANDROID 8.0.0;osv/8.0.0;pv/2.23;jdv/;ref/com.jingdong.app.mall.WebActivity;partner/huawei;apprpd/Home_Main;Mozilla/5.0 (Linux; Android 8.0.0; Mi Note 2 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36',
    'x-csrftoken': 'undefined',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.xuetangx.com/learn/{UID}/{UID}/{CID}/chapter',
    'cookie': COOKIE,
}
params = (
    # ('cid', '4231538'),
    # ('sign', 'HNU03031001055'),
    ('cid', CID),
    ('sign', UID),
)
response = requests.get('https://www.xuetangx.com/api/v1/lms/learn/course/chapter', headers=headers, params=params)
mJson = json.loads(response.text)
course_name = mJson['data'].get('course_name')
with open(f'{course_name}.md', 'w', encoding='utf-8') as f:
    f.write(f'# {course_name}\n\n')
    course_chapter = mJson['data'].get('course_chapter')
    for chapter in course_chapter:
        f.write('---\n\n')
        f.write(f'## {chapter["name"]}\n\n') # 章节名

        mCourse_chapter = json.dumps(eval(str(chapter)))
        section_leaf_list = chapter.get('section_leaf_list')
        for m in range(len(section_leaf_list)):
            eachChapter = section_leaf_list[m]
            leaf_list = eachChapter['leaf_list']
            for j in leaf_list:
                leaf_listReal = j
                courseId = leaf_listReal['id']
                print(j['name'])
                f.write(f"### {j['name']}\n" + '\n') # 小章节名
                headers = {
                    'authority': 'www.xuetangx.com',
                    'x-mina-sessid': 'null',
                    'django-language': 'zh',
                    'accept-language': 'zh',
                    'user-agent': 'jdapp;android;8.4.2;8.0.0;;network/wifi;model/Mi Note 2;osVer/26;appBuild/71043;psn/|7;psq/1;uid/;adk/;ads/;pap/JA2015_311210|8.4.2|ANDROID 8.0.0;osv/8.0.0;pv/2.23;jdv/;ref/com.jingdong.app.mall.WebActivity;partner/huawei;apprpd/Home_Main;Mozilla/5.0 (Linux; Android 8.0.0; Mi Note 2 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36',
                    'platform-id': '0',
                    'accept': 'application/json, text/plain, */*',
                    'x-client': 'apph5',
                    'xtbz': 'xt',
                    'university-id': '0',
                    'x-csrftoken': 'undefined',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    # 'referer': f'https://www.xuetangx.com/h5/homework/{UID}/{CID}/{EID}?avatar=https%3A%2F%2Fstoragecdn.xuetangx.com%2Fpublic_assets%2Fxuetangx%2Fimages%2Fb6ce32912ffa1c5959b0da6ceb9ce27e.avatar%402x.png&name=&user_number=null&term=latest&university_id=0&user_role=null&sessionid=null&csrftoken=poWpK8NCBXy4jTOx2S8d8ZcZRnqtK5EN&xtbz=xt&django-language=zh',
                    'referer': HOMEWORK_URL,
                    'cookie': COOKIE,
                }
                params = (
                    # ('sign', 'HNU03031001055'),
                    ('sign', UID),
                    ('term', 'latest'),
                    ('uv_id', '0'),
                )
                response = requests.get(
                    f'https://www.xuetangx.com/mooc-api/v1/lms/learn/leaf_info/{CID}/{str(courseId)}/',
                    headers=headers, params=params)
                mJson = json.loads(response.text)
                mLeaf_type_id = mJson['data']['content_info']['leaf_type_id']
                # f.write('leaf_type_id: ' + str(mLeaf_type_id) + '\n')
                try:
                    if mLeaf_type_id is not None:
                        # 正常的操作
                        headers = {
                            'authority': 'www.xuetangx.com',
                            'accept': 'application/json, text/plain, */*',
                            'django-language': 'zh',
                            'x-client': 'web',
                            'accept-language': 'zh',
                            'xtbz': 'xt',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
                            'content-type': 'application/json',
                            'sec-fetch-site': 'same-origin',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-dest': 'empty',
                            # 'referer': 'https://www.xuetangx.com/learn/HNU03031001055/HNU03031001055/4231538/exercise/6325463',
                            'referer': f'https://www.xuetangx.com/learn/{UID}/{UID}/{CID}/exercise/{EID}',
                            'cookie': COOKIE,
                        }
                        response = requests.get(
                            'https://www.xuetangx.com/api/v1/lms/exercise/get_exercise_list/' + str(mLeaf_type_id) + '/',
                            headers=headers)
                        mJson = json.loads(response.text)
                        mDescription = mJson['data']['description']
                        mName = mJson['data']['name']
                        problems = mJson['data'].get('problems')
                        for problem in problems:
                            problemIndex = problem['index']
                            problemIndexText = f'##### 第{problemIndex}题\n\n'

                            problemType = problem['content']['Type'] # 'MultipleChoice', 'Judgement', 'SingleChoice', 'ShortAnswer', 'FillBlank', ...
                            # problemTypeText = i['content']['TypeText'] + '\n\n'
                            problemTypeText = ''

                            problemScore = int(problem['content']['score'])
                            problemScoreText = f'({problemScore}分)' + ' '
                            problemBody = problem['content']['Body']
                            problemBody = escape_for_markdown(problemBody) # 转义
                            if problemType == 'Judgement': # 判断题
                                problemBodyText = problemBody + '\n\n'
                            elif problemType == 'SingleChoice': # 单选题
                                problemOptions = problem['content']['Options']
                                problemOptionsText = ''
                                for option in problemOptions:
                                    problemOptionsText += f"`{option['key']}` {escape_for_markdown(option['value'])}\n"
                                problemBodyText = problemBody + '\n' + problemOptionsText + '\n'
                            elif problemType == 'MultipleChoice': # 多选题
                                problemOptions = problem['content']['Options']
                                problemOptionsText = ''
                                for option in problemOptions:
                                    problemOptionsText += f"`{option['key']}` {escape_for_markdown(option['value'])}\n"
                                problemBodyText = problemBody + '\n' + problemOptionsText + '\n'
                            elif problemType == 'ShortAnswer': # 主观题
                                problemBodyText = problemBody + '\n\n'
                            else:
                                problemBodyText = problemBody + '\n\n'
                            problemText = problemIndexText + problemTypeText + problemScoreText + problemBodyText

                            try:
                                if problemType == 'FillBlank':
                                    answers = problem['user']['answers']
                                    answerText = '\n'
                                    for i in range(len(answers)):
                                        key = str(i + 1)
                                        answerText += fr'\[填空{key}\] '
                                        answerText += ' '.join(f'`{choice}`' for choice in answers[key])
                                        answerText += '\n'
                                else:
                                    answer = problem['user']['answer']
                                    if problemType == 'Judgement': # 判断题
                                        answerText = r"$\checkmark$" if answer[0] == "true" else r"$\times$"
                                    elif problemType == 'MultipleChoice' or problemType == 'SingleChoice': # 单选题/多选题
                                        answerText = ' '.join(f'`{choice}`' for choice in answer)
                            except:
                                answerText = ''
                            finally:
                                answerText = '**正确答案：** ' + answerText + '\n'
                                f.write(problemText + answerText + '\n')
                except:
                    # 发生异常，执行这块代码
                    f.write('---' + '\n')
                    f.write('出现异常！' + '\n')
                    f.write('---' + '\n')
                    continue
                else:
                    # 如果没有异常执行这块代码
                    # f.write('---\n\n')
                    None