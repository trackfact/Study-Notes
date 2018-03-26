# from elasticsearch import Elasticsearch
# _es = Elasticsearch([{"host":"172.16.132.97","port":"9200"}])

# # 初始化索引的Mappings设置
# _index_mappings = {
#   "mappings": {
 
#     "blogpost": { 
#       "properties": { 
#         "title":    { "type": "text"  }, 
#         "body":     { "type": "text"  }, 
#         "user_id":  {
#           "type":   "keyword" 
#         },
#         "created":  {
#           "type":   "date"
#         }
#       }
#     }
#   }
# }

# # 如果索引不存在，则创建索引
# if _es.indices.exists(index='blog_index') is not True:
#   _es.indices.create(index='blog_index', body=_index_mappings) 



#coding:utf8
import os
import time
from os import walk 
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class ElasticObj:
    def __init__(self, index_name,index_type):
        '''

        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.index_name =index_name
        self.index_type = index_type
   
        self.es = Elasticsearch([{"host":"172.16.132.97","port":"9200"}]) 

    def create_index(self,index_name="news",index_type="news_type"):
        '''
        创建索引,创建索引名称为news，类型为news_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        #创建映射
        _index_mappings = {
            "mappings": {
                self.index_type: {
                    "properties": {
                        "title": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "content": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "date": {
                            "type": "text",
                            "index": True
                        },
                        "keyword": {
                            "type": "text", 
                        },
                        "link": {
                            "type": "text", 
                        }
                    }
                }

            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings)
            print(res)


 

    def Index_Data(self):
        '''
        数据存储到es
        :return:
        '''
        list = [
            {   "date": "2017-09-13",
                "source": "慧聪网",
                "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
                "keyword": "电视",
                "content": "在保增长的问题上，85%的高管认为，未来五年间，付费电视服务供应商需要加强创新才能实现增长。四分之三认为，创新是优先级最高的战略。越来越多的高管将重点放在了独立OTT服务（64%），多屏TVEverywhere服务（67%），基于APP的电视服务（61%）以及语音、4K等高级功能（53%），此外还有创新内容对策（74%）和新的定价与套餐模式（78%）上。",
                "title": "付费 电视 行业面临的转型和挑战"
             },
            {   "date": "2017-09-13",
                "source": "中国文明网",
                "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
                "keyword": "电视",
                "content": "    在盗版问题上，半数高管认为，内容盗版将为产业发展带来更大压力。在线流媒体、P2P下载以及IPTV盗版被列为最重要的三种盗版形式。研究还调查了付费电视盗版导致的实际收入损失。如果至少四分之一的盗版付费电视服务用户转向合法途径，付费电视营收每年将增加70亿美元。此外，72%付费电视供应商认为反盗版活动结合技术手段、法律措施和消费者教育，会带来积极的效果。",
                 "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心"
             }
              ]
        for item in list:
            res = self.es.index(index=self.index_name, doc_type=self.index_type, body=item)
            print(res)

    def bulk_Index_Data(self):
        '''
        用bulk将批量数据存储到es
        :return:
        '''
        list = [
            {"date": "2017-09-13",
             "source": "慧聪网",
             "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
             "keyword": "电视",
             "content": "  Nagra高级产品营销主管SimonTrudelle表示：“付费电视创新论坛第二版为付费电视产业变革提供了一个全景式的观察，并指出了服务供应商和内容所有方的机会领域。此外，该报告还强调了一些新的动向，尤其是内容盗版的兴起。总体而言，行业认可了电视的本质正在发生改变，需要适应快速变化的新环境。服务供应商和内容所有方正通过发展新服务、建立新合作，为转型和未来业务作准备。”电视",
              "title": "付费 电视 行业面临的转型和挑战"
             },
            {"date": "2017-09-13",
             "source": "中国文明网",
             "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
                "content": "    在盗版问题上，半数高管认为，内容盗版将为产业发展带来更大压力。在线流媒体、P2P下载以及IPTV盗版被列为最重要的三种盗版形式。研究还调查了付费电视盗版导致的实际收入损失。如果至少四分之一的盗版付费电视服务用户转向合法途径，付费电视营收每年将增加70亿美元。此外，72%付费电视供应商认为反盗版活动结合技术手段、法律措施和消费者教育，会带来积极的效果。",
             "keyword": "电视",
             "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心"
             },
            {"date": "2017-09-13",
             "source": "人民电视",
             "link": "http://tv.people.com.cn/BIG5/n1/2017/0913/c67816-29533981.html",
             "keyword": "电视",
             "content": "   付费电视创新论坛由内容保护公司Nagra与研究和战略咨询公司MTM共同建立，旨在检视付费电视市场创新情况，为欧洲、亚太、拉美和北美的服务供应商和内容所有方提供建议。",
             "title": "中国第21批赴刚果（金）维和部隊启程--人民 电视 --人民网"
             },
            {"date": "2017-09-13",
             "source": "站长之家",
                "content": "    在盗版问题上，半数高管认为，内容盗版将为产业发展带来更大压力。在线流媒体、P2P下载以及IPTV盗版被列为最重要的三种盗版形式。研究还调查了付费电视盗版导致的实际收入损失。如果至少四分之一的盗版付费电视服务用户转向合法途径，付费电视营收每年将增加70亿美元。此外，72%付费电视供应商认为反盗版活动结合技术手段、法律措施和消费者教育，会带来积极的效果。",
             "link": "http://www.chinaz.com/news/2017/0913/804263.shtml",
             "keyword": "电视",
             "title": "电视 盒子 哪个牌子好？ 吐血奉献三大选购秘笈"
             }
        ]
        ACTIONS = []
        i = 1
        for line in list:
            action = {
                "_index": self.index_name,
                "_type": self.index_type, 
                "_source": {
                    "date": line['date'],
                    "source": line['source'],
                    "link": line['link'],
                    "keyword": line['keyword'],
                    "content": line['content'],
                    "title": line['title']}
            }
            i += 1
            ACTIONS.append(action)
            # 批量处理
        success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
        print('Performed %d actions' % success)

    def Delete_Index_Data(self,id):
        '''
        删除索引中的一条
        :param id:
        :return:
        '''
        res = self.es.delete(index=self.index_name, doc_type=self.index_type, id=id)
        print(res)

    def Get_Data_Id(self,id):

        res = self.es.get(index=self.index_name, doc_type=self.index_type,id=id)
        print(res['_source'])

        print('------------------------------------------------------------------')
        #
        # # 输出查询到的结果
        for hit in res['hits']['hits']:
            # print hit['_source']
            print(hit['_source']['date'],hit['_source']['source'],hit['_source']['link'],hit['_source']['keyword'],hit['_source']['title'])

    def Get_Data_By_Body(self):
        # doc = {'query': {'match_all': {}}}
        doc = {
            "query": {
                "match": {
                    "keyword": "电视"
                }
            }
        }
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)

        for hit in _searched['hits']['hits']:
            # print hit['_source']
            print( hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'], \
            hit['_source']['title'])




obj =ElasticObj("news","news_type") 

obj.create_index()
obj.Index_Data()
while(True):
    obj.bulk_Index_Data()
# obj.IndexData()
# obj.Delete_Index_Data(1)
# csvfile = 'D:/work/ElasticSearch/exportExcels/2017-08-31_info.csv'
# obj.Index_Data_FromCSV(csvfile)
# obj.GetData(es)