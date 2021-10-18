import psycopg2
class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host='localhost', dbname='Koroad',user='postgres',password='1234',port=5433)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()

    def read_biggest(self, target, schema = 'public', table = 'test_table'):
        target = "'" + target + "'"
        sql = "SELECT * from {}.{} WHERE name in ({}, '전체')".format(schema,table,target)
        try:
            self.cursor.execute(sql)
            sub = self.cursor.fetchall()
            t = ['기어', '주차브레이크', '가속불가', '정지시 미제동', '타력주행', '엔진미정지', '신호계속', '급조작', '30미터 전 미신호', '핸들 조작 미숙']
            result = []
            for i in range(3, len(sub[0])):
                score = (sub[1][i] / sub[0][2]* 100) - sub[0][i] / sub[0][2] * 100
                if score < 0 : result.append((-score, t[i-3], False))
                else: result.append((score, t[i - 3], True))
            result.sort()
            for idx in range(3):
                x, y, z = result[idx]
                if z : print(result[idx][1] + ' 항목 점수평균이 {}% 더 높습니다.'.format(round(x, 2)))
                else: print(result[idx][1] + ' 항목 점수평균이 {}% 더 낮습니다.'.format(round(x, 2)))
            return

        except Exception as e :
            return " read DB err",e
    
    def updateDB(self, df, schema = 'public', table = 'test_table'):
        sql = 'UPDATE {}.{} SET total = total + {}, Ta1=Ta1+{}, Ta2=Ta2+{}, Ta3=Ta3+{}, Ta4=Ta4+{}, Ta5=Ta5+{}, Ta6=Ta6+{}, Ta7=Ta7+{}, Ta8=Ta8+{}, Ta9=Ta9+{}, Ta10=Ta10+{} WHERE name = {}'.format(schema,table, df[1], df[2], df[3],df[4],df[5],df[6],df[7],df[8],df[9],df[10],df[11],"'" + df[0] + "'")                         
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err", 'error = 1', e)
        
        sql = 'UPDATE {}.{} SET total = total + {}, Ta1=Ta1+{}, Ta2=Ta2+{}, Ta3=Ta3+{}, Ta4=Ta4+{}, Ta5=Ta5+{}, Ta6=Ta6+{}, Ta7=Ta7+{}, Ta8=Ta8+{}, Ta9=Ta9+{}, Ta10=Ta10+{} WHERE name = {}'.format(schema,table, df[1], df[2], df[3],df[4],df[5],df[6],df[7],df[8],df[9],df[10],df[11],"'" + '전체' + "'")                         
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err", 'error = 2', e)
