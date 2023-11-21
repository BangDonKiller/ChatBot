import warnings
from elasticsearch import Elasticsearch
from openpyxl import load_workbook
import json

es = Elasticsearch('http://localhost:9200')
# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# es = Elasticsearch([{'host': 'localhost'}])

warnings.filterwarnings("ignore")


def StdQ_to_Elastic(Path):
    '''
    讀取excel檔案, 讀取Std_Q_All工作表
    '''
    wb = load_workbook(Path)
    sheet = wb['Std_Q_All']

    # 把標準問題跟答案分開
    Q = sheet['A']
    A = sheet['B']

    # 題目數量
    num = int(Q[0].value)

    question = []
    for i in range(1, num+1):
        # 題目存儲為list
        question.append(Q[i].value)
        # 題目解答存儲為dict
        data = {'title': Q[i].value, 'Ans': A[i].value}

        # 建立資料的index curpus2，doc_type為politics，id為i，body為data
        result = es.create(
            index='curpus2', doc_type='politics', id=i, body=data)

        result = es.get(index="curpus2", doc_type="politics", id=i)

        # 把資料轉成json格式，並且編碼成utf8
        j = json.dumps(result, separators=(',\n', ': '),
                       ensure_ascii=False).encode('utf8')
        # print(j.decode())


def Put_All_StdQ_to_Els():
    '''
    將所有標準答案放入elasticsearch裡面
    '''
    # 把curpus2 index資料庫刪掉
    es.indices.delete(index='curpus2', ignore=[400, 404])
    Std_place = './Customer-Service-Chatbot-from-FAQ/QA/Total_User_Q.xlsx'
    StdQ_to_Elastic(Std_place)


# Put_All_StdQ_to_Els()
