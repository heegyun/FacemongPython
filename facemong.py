from wordcloud  import WordCloud
from konlpy.tag import Twitter
# 명사의 출현 빈도를 세는 라이브러리를 불러옵니다.
from collections import Counter
# 그래프 생성에 필요한 라이브러리를 불러옵니다.
import matplotlib.pyplot as plt
# Flask 웹 서버 구축에 필요한 라이브러리를 불러옵니다.
from flask import Flask, request, jsonify

app=Flask(__name__, static_folder='outputs')

def get_tags(text,max_count, min_length):
    t = Twitter()
    nouns = t.nouns(text)
    processed = [n for n in nouns if len(n) >= min_length]
    # 모든 명사의 출현 빈도를 계산합니다.
    count = Counter(processed)
    result = {}
    # 출현 빈도가 높은 max_count 개의 명사만을 추출합니다.
    for n, c in count.most_common(max_count):
        result[n] = c
    # 추출된 단어가 하나도 없는 경우 '내용이 없습니다.'를 화면에 보여줍니다.
    if len(result) == 0:
        result["내용이 없습니다."] = 1
    return result

def make_cloud_image(tags, file_name):
    # 만들고자 하는 워드 클라우드의 기본 설정을 진행합니다.
    word_cloud = WordCloud(
        width=800,
        height=800,
        background_color="white",
    )
    # 추출된 단어 빈도수 목록을 이용해 워드 클라우드 객체를 초기화 합니다.
    word_cloud = word_cloud.generate_from_frequencies(tags)
    # 워드 클라우드를 이미지로 그립니다.
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(word_cloud)
    plt.axis("off")
    # 만들어진 이미지 객체를 파일 형태로 저장합니다.
    fig.savefig("outputs/{0}.png".format(file_name))



def process_from_text(text, max_count, min_length,dogs,file_name):
    # 최대 max_count 개의 단어 및 등장 횟수를 추출합니다.
    tags = get_tags(text, max_count, min_length)
    # 단어 가중치를 적용합니다.
    for n, c in dogs.items():
        if n in tags:
            tags[n] = tags[n] * int(dogs[n])
    # 명사의 출현 빈도 정보를 통해 워드 클라우드 이미지를 생성합니다.
    make_cloud_image(tags, "output")


@app.route("/process", methods=['GET', 'POST'])
def process():
    content = request.json
    dogs = {}
    if content['dogs'] is not None:
        for data in content['dogs'].values():
            dogs[data['dog']] = data['emotion']
            dogs[data['dog']] = data['ear']
            dogs[data['dog']] = data['tail']
            dogs[data['dog']] = data['size']
            dogs[data['dog']] = data['breed']
            dogs[data['dog']] = data['age']

    process_from_text(content['text'], content['maxCount'], content['minLength'], dogs,content['textID'])
    result = {'result': True}
    return jsonify(result)



@app.route('/outputs',methods=['GET','POST'])
def output():
    text_id = request.args.get('textID')
    return app.send_static_file(text_id+'.png')
    



if __name__=='__main__':
    app.run('0.0.0.0',port=5000)



