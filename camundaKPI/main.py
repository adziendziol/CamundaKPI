import pymysql
import pylru
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

""" @app.route('/update', methods=['POST'])
def update_user():
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']		
		# validate the received values
		if _name and _email and _password and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
 """
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()