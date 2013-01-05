#!/usr/bin/python
# - * - coding: utf-8 -*-
__author__ = 'huangzhiyong'

import MySQLdb
import sys
import datetime
#import time

##data query host info
Q_HOST = 'xxx'
Q_USER = 'xx'
Q_PASSWD = 'xx'
Q_DBNAME = 'xx'

##date storage host info
S_HOST = 'localhost'
S_USER = 'xxx'
S_PASSWD = 'xxx'
S_DBNAME = 'xxx'
S_SOCKET = 'xx'

##date handle
owner_user = "\"13522524071\",\"13810824656\",\"15652248060\",\"18911274890\",\"18611854398\",\"18601305627\",\"13911712776\",\"13439715071\",\"18610240221\",\"13718215569\",\"15611018401\",\"13051279817\",\"15110079690\",\"18600410922\",\"18611169301\",\"13269203981\",\"13520347057\",\"18810293957\",\"13488817926\",\"18201034732\",\"15811345284\",\"18210996458\",\"15001167646\",\"18810759155\",\"15810117680\",\"13521686930\",\"18601949618\",\"18601357963\",\"15210262378\",\"15801018980\",\"18610068021\",\"18310723306\",\"15201509490\",\"18611668180\",\"13521693560\",\"18618138428\",\"13581725228\",\"13618665732\",\"18210588710\",\"18911821017\",\"13121376606\",\"15010165535\",\"13616522422\",\"13146618995\",\"13621190001\",\"15321899850\",\"18600693109\",\"18600497358\""

def Detals(interval = 1):
    date1 = datetime.date(2012,06,06)
    date2 = datetime.date(2012,06,07)
    delta = date2 - date1
    delta0 = delta - delta
    if interval == 2:
        return delta
    elif interval == 3:
        return delta * 2
    elif interval == 4:
        return delta * 3
    elif interval == 5:
        return delta * 4
    elif interval == 6:
        return delta * 5
    elif interval == 7:
        return delta * 6
    elif interval == 1:
        return delta0
    else:
        print "Beyond the normal range parameters: 1-7"
        sys.exit(1)

current_date = datetime.date.today()
stats_date = current_date - Detals(2)
month_num = stats_date.month
day_num = stats_date.day
week_day = stats_date.isoweekday()
start_date = stats_date - Detals(week_day)
stats_date = stats_date.isoformat()
start_date = start_date.isoformat()
current_date = current_date.isoformat()

#print week_day,start_date,stats_date
#sys.exit(1)

###################################################query data section

try:
    con_q = MySQLdb.connect(Q_HOST,Q_USER,Q_PASSWD,Q_DBNAME,charset = 'utf8')
    cur = con_q.cursor()

    #######summary
    ##register user total numbers
    cur.execute("select count(uid) as user_total from ms_user")
    user_total = int(cur.fetchone()[0])

    ##android platform register total numbers
    cur.execute("select count(uid) as android from ms_user where agent like '%java%'")
    android_total = int(cur.fetchone()[0])

    ##iphone platform register total numbers
    cur.execute("select count(uid) as android from ms_user where agent like '%IPhone%'")
    iphone_total = int(cur.fetchone()[0])

    ##register user male total numbers
    cur.execute("select count(uid) as male from ms_user where sex = '男'")
    male_total = int(cur.fetchone()[0])

    ##register user female total numbers
    cur.execute("select count(uid) as female from ms_user where sex = '女'")
    female_total = int(cur.fetchone()[0])

    #print "total:%d |android:%d |iphone:%d |male:%d |female:%d "%(user_total,android_total,iphone_total,male_total,female_total)

    ######days active user numbers
    ##days active user numbers
    cur.execute(
        "select count(uid) as day_active from ms_user where last_time>=unix_timestamp(%s) and last_time< unix_timestamp(%s)"
        ,(stats_date,current_date))
    day_active = int(cur.fetchone()[0])

    #2:----------------------------------------------------
    sql = "select count(uid) as day_active from ms_user where mobile not in (%s) and last_time>=unix_timestamp(%r) and last_time< unix_timestamp(%r)" % (
        owner_user,stats_date,current_date)
    cur.execute(sql)
    day_active_2 = int(cur.fetchone()[0])

    sql = "select count(uid) from ms_user where mobile not in (%s) and last_time>=unix_timestamp(%r) and last_time< unix_timestamp(%r) and agent not like '%%IPhone%%'" % (
        owner_user,stats_date,current_date)

    cur.execute(sql)
    day_android_active_2 = int(cur.fetchone()[0])

    sql = "select count(uid) from ms_user where mobile not in (%s) and last_time>=unix_timestamp(%r) and last_time< unix_timestamp(%r) and agent like '%%IPhone%%'" % (
        owner_user,stats_date,current_date)
    cur.execute(sql)
    day_iphone_active_2 = int(cur.fetchone()[0])

    print "mobile:",owner_user
    print "day2:%s|%s|%s" % (day_active_2,day_android_active_2,day_iphone_active_2)
    #-------------------------------------------------------

    ##days resiter user numbers
    cur.execute(
        "select count(uid) as day_register from ms_user where reg_time>=unix_timestamp(%s) and reg_time< unix_timestamp(%s)"
        ,(stats_date,current_date))
    day_register = int(cur.fetchone()[0])

    ##day android platform resiter numbers
    cur.execute(
        "select count(uid) as day_android from ms_user where reg_time>=unix_timestamp(%s) and reg_time< unix_timestamp(%s) and agent like '%%java%%'"
        ,(stats_date,current_date))
    day_android = int(cur.fetchone()[0])

    ##day iphone platform resiter numbers
    cur.execute(
        "select count(uid) as day_iphone from ms_user where reg_time>=unix_timestamp(%s) and reg_time< unix_timestamp(%s) and agent like '%%IPhone%%'"
        ,(stats_date,current_date))
    day_iphone = int(cur.fetchone()[0])

    ##day android avtive numbers
    cur.execute(
        "select count(uid) from ms_user where last_time>=unix_timestamp(%s) and last_time< unix_timestamp(%s) and agent not like '%%IPhone%%'"
        ,(stats_date,current_date))
    day_android_active = int(cur.fetchone()[0])

    ##day iphone active numbers
    cur.execute(
        "select count(uid) from ms_user where last_time>=unix_timestamp(%s) and last_time< unix_timestamp(%s) and agent like '%%IPhone%%'"
        ,(stats_date,current_date))
    day_iphone_active = int(cur.fetchone()[0])

    #print "days -- active users:%d |register users:%d |android users:%d |iphone users:%d |android active:%d |iphone active:%d"%(day_active,day_register,day_android,day_iphone,day_android_active,day_iphone_active)

    ##retailer info and active info
    retailer_res = {}
    for i in range(3):
        cur.execute(
            "select retailer_id,count(*),type,date_add(curdate(),interval -1 day) as create_time from ms_retailer_admin where type=%s group by retailer_id"
            ,(i))
        retailer_res[i] = cur.fetchall()

    cur.execute(
        " select uname,store_id,retailer_id,type, from_unixtime(last_time),date_add(curdate(),interval -1 day) as create_time  from ms_retailer_admin where last_time>=unix_timestamp(%s) and last_time<unix_timestamp(%s)"
        ,(stats_date,current_date))
    retailer_active_res = cur.fetchall()

    cur.execute(
        " select uname,store_id,retailer_id,type, from_unixtime(reg_time),date_add(curdate(),interval -1 day) as create_time  from ms_retailer_admin where reg_time>=unix_timestamp(%s) and reg_time<unix_timestamp(%s)"
        ,(stats_date,current_date))
    retailer_register_res = cur.fetchall()

    #print retailer_active_res
    #print retailer_register_res

except MySQLdb.Error,e:
    print "Query Data Section -- Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

cur.close()
con_q.close()

###################################################storage data section

try:
    con_s = MySQLdb.connect(S_HOST,S_USER,S_PASSWD,S_DBNAME,unix_socket = S_SOCKET,charset = 'utf8')
    cur_s = con_s.cursor()

    #day2 -------------------------------------------
    cur_s.execute(
        "insert into user_days_2 (day_active_num,day_android_active,day_iphone_active,day_time) values (%d,%d,%d,%r)" % (
            day_active_2,day_android_active_2,day_iphone_active_2,stats_date))
    #------------------------------------------------

    ##retailer infos
    #summary
    values = retailer_res.values()
    for num in range(len(values)):
        sql = "insert into retailer_clerk_info (retailer_id,person_number,type,create_time) values (%s,%s,%s,%s)"
        cur_s.executemany(sql,values[num])
        #active info
    sql = "insert into retailer_clerk_info (user_name,store_id,retailer_id,type,last_time,create_time) values (%s,%s,%s,%s,%s,%s)"
    cur_s.executemany(sql,retailer_active_res)
    #register info
    sql = "insert into retailer_clerk_info (user_name,store_id,retailer_id,type,reg_time,create_time) values (%s,%s,%s,%s,%s,%s)"
    cur_s.executemany(sql,retailer_register_res)

    ##summary table
    cur_s.execute(
        "insert into user_summary (register_num,male_num,female_num,android_register_num,iphone_register_num,create_time) values (%d,%d,%d,%d,%d,%r)" % (
            user_total,male_total,female_total,android_total,iphone_total,stats_date))

    ##days table
    cur_s.execute(
        "insert into user_days (day_active_num,day_register_num,day_android_register_num,day_iphone_register_num,day_android_active,day_iphone_active,day_time) value (%d,%d,%d,%d,%d,%d,%r)" % (
            day_active,day_register,day_android,day_iphone,day_android_active,day_iphone_active,stats_date))

    ##weeks table
    if week_day == 1:
        cur_s.execute(
            "insert into user_weeks (week_active_num,week_register_num,week_android_register_num,week_iphone_register_num,week_android_active,week_iphone_active,start_date) value (%d,%d,%d,%d,%d,%d,%r)" % (
                day_active,day_register,day_android,day_iphone,day_android_active,day_iphone_active,start_date))
    elif week_day in range(2,8):
        cur_s.execute(
            "update user_weeks set week_active_num=week_active_num+%d,week_register_num=week_register_num+%d,week_android_register_num=week_android_register_num+%d,week_iphone_register_num=week_iphone_register_num+%d,week_android_active=week_android_active+%d,week_iphone_active=week_iphone_active+%d where start_date = %r" % (
                day_active,day_register,day_android,day_iphone,day_android_active,day_iphone_active,start_date))
    else:
        print "Parameter week_day error - Beyond the normal range parameters: 1-7"
        sys.exit(1)
        ##months table
    #print type(day_num)
    if day_num == 1:
        cur_s.execute(
            "insert into user_months (month_active_num,month_register_num,month_android_register_num,month_iphone_register_num,month_android_active,month_iphone_active,months) value (%d,%d,%d,%d,%d,%d,%d)" % (
                day_active,day_register,day_android,day_iphone,day_android_active,day_iphone_active,month_num))
    elif day_num in range(2,32):
        cur_s.execute(
            "update user_months set month_active_num=month_active_num+%d,month_register_num=month_register_num+%d,month_android_register_num=month_android_register_num+%d,month_iphone_register_num=month_iphone_register_num+%d,month_android_active=month_android_active+%d,month_iphone_active=month_iphone_active+%d where months=%d" % (
                day_active,day_register,day_android,day_iphone,day_android_active,day_iphone_active,month_num))
    else:
        print "Parameter day_num error - Beyond the normal range parameters: 1-31"
        sys.exit(1)

    #commit data
    con_s.commit()
except MySQLdb.Error,s:
    print "Storage Data Section -- Error %d: %s" % (s.args[0],s.args[1])
    sys.exit(1)

cur_s.close()
con_s.close()
