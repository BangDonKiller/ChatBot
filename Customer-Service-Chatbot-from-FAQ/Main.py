import StandardQ as SQ
import BertW2V as bertw2v
import Combine as cb
import argparse
import warnings

# 忽略警告訊息
warnings.filterwarnings("ignore")


# 自訂命令列、-h說明 please enter user query
parser = argparse.ArgumentParser()
parser.description = 'please enter user query'

# 定義3組可選參數，作為字串儲存在args裡
parser.add_argument(
    "-w", "--w2v", help="predict user query in W2V+ElasticSearch", type=str)
parser.add_argument(
    "-b", "--bert", help="predict user query in Bert", type=str)
parser.add_argument(
    "-c", "--combine", help="predict user query in  the combination of W2V+ElasticSearch and Bert", type=str)

# 解析參數，分別是.w2v .bert .combine
args = parser.parse_args()
print(args)
# ------------------------

print("Running...")


# 先將所有標準問題放入ElasticSearch，再將使用者的問題轉成W2V向量，並與ElasticSearch裡的標準問題做比對
if args.w2v:
    # 將所有標準問題放入ElasticSearch
    SQ.Put_All_StdQ_to_Els()
    # 將使用者的問題轉成W2V向量，並與ElasticSearch裡的標準問題做比對
    w2v_dic = bertw2v.RunW2V(args.w2v)
    cb.single_output(w2v_dic)

# TODO 還在看要怎麼做
if args.bert:
    bert_dic = bertw2v.RunBert(args.bert)
    cb.single_output(bert_dic)

# TODO 還在看要怎麼做
if args.combine:
    SQ.Put_All_StdQ_to_Els()
    bert_dic, w2v_dic = bertw2v.Run(args.combine)
    cb.single_run(w2v_dic, bert_dic)
