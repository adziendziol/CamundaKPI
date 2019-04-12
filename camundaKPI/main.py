import pymysql
import pylru
import schedule
import time
import uuid

from datetime import datetime
from functools import lru_cache
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request



@lru_cache(maxsize=4)	
@app.route('/Tasks')
def tasks():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select ART.NAME_ as Name,ART.TENANT_ID_ as Kundennummer,count(*) as count from ACT_RU_TASK as ART group by ART.NAME_")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@lru_cache(maxsize=4)
@app.route('/HistoryTasks')
def historyTasks():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select AHT.NAME_ as Name,AHT.TENANT_ID_ as Kundennummer,count(*) as count from ACT_HI_TASKINST as AHT group by AHT.NAME_")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        resp.headers["Content-Type"] = "application/json; charset=utf-8" 
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@lru_cache(maxsize=4)
@app.route('/KpiEvents')
def kpiEvents():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select AHI.ACT_NAME_ as StatusName, count(*) as count from ACT_HI_ACTINST as AHI where AHI.`ACT_TYPE_` in ('intermediateNoneThrowEvent','startEvent') and AHI.ACT_NAME_ is not null group by AHI.ACT_NAME_")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        resp.headers["Content-Type"] = "application/json; charset=utf-8" 
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@lru_cache(maxsize=4)
@app.route('/ProcessTimelines')
def processTimeLines():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from JAR_GET_IIDS_BY_FINISHED_PROCESSES order by BusinessKey, StartTime LIMIT 400")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        resp.headers["Content-Type"] = "application/json; charset=utf-8" 
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@lru_cache(maxsize=4)
@app.route('/Processtimeline/<BusinessKey>')
def processTimeLineByBusinessKey(BusinessKey):
    try:
        print(BusinessKey)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(f'select * from JAR_GET_IIDS_BY_FINISHED_PROCESSES where BusinessKey= {BusinessKey} order by BusinessKey, StartTime')
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@lru_cache(maxsize=4)
@app.route('/task/<taskname>/count')
def taskCount(taskname):
    try:
        print(taskname)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print("select '{taskname}' as Name,count(*) as count from `ACT_RU_TASK` as ART where ART.NAME_ ='{taskname}''")
        cursor.execute("select '{taskname}' as Name,count(*) as count from `ACT_RU_TASK` as ART where ART.NAME_ ='{taskname}'")
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/CreateKpiReport')
def casdreateKpiReport():
    try: 
        UpdateKpiReport()
        message = {
        'status': 200,
        'message': 'Everything OK' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 200
    except Exception as e:
        print(e)

@lru_cache(maxsize=4)
@app.route('/GetKpiOverview')
def getKpiOverview():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""Select K.`title`,K.`KPI_VALUE`,
CASE WHEN KR.`KpiBroken`='1' THEN true
ELSE false END as KpiBroken
,count(*) as Anzahl from `JAR_KPI_REPORT` as KR inner join `KPI` as K on K.`KPI_id`=KR.`KpiID`
group by K.`title`,KR.`KpiBroken`""")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp



def UpdateKpiReport():
    print('Update des KPI-Reports gestartet')
    try:
        uid = uuid.uuid4()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        statement = f"""INSERT INTO `JAR_KPI_REPORT` (`BusinessKey`,`StartactivityID`,`EndactivityID`,`StartName`,`EndName`,`StartTime`,`EndTime`,`KpiID`,`DifferenzInStunden`,`DifferenzInTagen`,`KpiBroken`,`updateRun`) 
Select 
X.BusinessKey as BusinessKey,
X.`ACT_ID_` as StartactivityID,
Y.`ACT_ID_` as EndactivityID,
X.`ACT_NAME_`as StartName,
Y.`ACT_NAME_` as EndName,
X.`START_TIME_` as StartTime,
Y.`END_TIME_` as EndTime,
X.`KPI_id` as KpiID,
hour(TIMEDIFF(Y.`END_TIME_`,X.`START_TIME_`)) as DifferenzInStunden,
DateDIFF(Y.`END_TIME_`,X.`START_TIME_`) as DifferenzInTagen,
CASE WHEN (DateDIFF(Y.`END_TIME_`,X.`START_TIME_`) <= X.`KPI_VALUE`) THEN '0'
ELSE '1' END as KpiBroken,
'{uid}' as updateRun
from 
	(Select * from `JAR_EVENT_SELECTION_ACTIVITY_HISTORY` as A
				inner join JAR_BK_WITH_INSTANCEIDS as O
							ON A.`PROC_INST_ID_` = O.`InstanceID`
				inner join `KPI` as K 
							ON K.`START_ACT_ID_` = A.`ACT_ID_`) AS X
	inner join  
	(Select * from `JAR_EVENT_SELECTION_ACTIVITY_HISTORY` as B
				inner join JAR_BK_WITH_INSTANCEIDS as I
							ON B.`PROC_INST_ID_` = I.`InstanceID`
				inner join `KPI` as K2 
 							ON K2.`END_ACT_ID_` = B.`ACT_ID_`) AS Y
on Y.`BusinessKey`= X.`BusinessKey` and Y.`KPI_id` = X.`KPI_id`"""
        print(statement)
        cursor.execute(statement)
        return True
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


""" def job():
    print("I'm working...")
    UpdateKpiReport()
    schedule.every(1).minutes.do(job)


while 1:
    schedule.run_pending()
    time.sleep(1) """


if __name__ == "__main__":
    app.run()
