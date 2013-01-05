#!/usr/bin/env python
# - * - coding: utf-8 -*-
__author__ = 'huangzhiyong'
from operator import itemgetter
import sys
import MySQLdb
import smtplib
from email.Header import Header
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

##date storage host info
S_HOST = 'xxxx'
S_USER = 'xxxx'
S_PASSWD = 'xxx'
S_DBNAME = 'xxxx'


##define mail server info
mail_host = "smtp.xxxx.com.cn"
mail_user = "huangzhiyong@xxx.com.cn"
mail_pass = "xxxx"
mail_postfix = "xxxx.com.cn"
mail_from = "huangzhiyong@xxxx.com.cn"
mail_tolist = ["zhaotc@xxx.com.cn","huangzhiyong@xxxx.com.cn"]

def send_mail(to_list,sub,content):
    """
    to_list:发给谁
    sub:主题
    content:发送内容
    """
    #msg = MIMEMultipart()
    msg = MIMEText(content,'plain','utf-8')
    msg['Subject'] = Header(sub,'utf-8')
    msg['From'] = mail_user
    msg['To'] = ";".join(to_list)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host,port = 25)
        smtp.login(mail_user,mail_pass)
        smtp.sendmail(mail_user,to_list,msg.as_string())
        smtp.close()
        return True
    except Exception,e:
        print str(e)
        return False


def DictValueSort(d,reverse = False):
    return sorted(d.iteritems(),key = itemgetter(1),reverse = reverse)

if __name__ == "__main__":
    try:
        con = MySQLdb.connect(S_HOST,S_USER,S_PASSWD,S_DBNAME,charset = 'utf8')
        cur = con.cursor()
        cur.execute("SELECT tag_id FROM ms_tag_category WHERE retailer_id=4 AND tag_id IS NOT NULL AND tag_id !=''")
        temp_res = cur.fetchall()
        temp_result = []
        for rows in temp_res:
            temp = [row.split(',') for row in rows]
            temp_result = temp_result + temp[0]

        #print len(temp_result)
        result = {}.fromkeys(temp_result).keys()
        #print len(result)
        res = None
        for element in result:
            #print element
            if not res:
                res = element
            else:
                res = res + ',' + element
                #print res
        if res:
            tag_fans = {}
            msg = "赵总，您好!\n        下面是今天粉丝排在前三十的品牌:\n"
            sql = "SELECT tag_id,tag_name,COUNT(*) FROM ms_subscribe_tag WHERE  tag_id IN (%s) group by tag_id order by null" % res
            cur.execute(sql)
            temp_tag = cur.fetchall()
            if temp_tag:
                for tag_row in temp_tag:
                    tag_fans[tag_row[1]] = tag_row[2]
                tag_res = DictValueSort(tag_fans,True)
                for index,tag_name in enumerate(tag_res):
                    if index == 30:
                        break
                    msg += "                %s                %s\n" % (tag_name[0],tag_name[1])
                    #print index,tag_name[0],tag_name[1]

                subject = "甘家口品牌排行榜信息"
                status = send_mail(mail_tolist,subject.encode("utf8"),msg.encode('utf8'))
                if status:
                    print "Email was sent successfully!"
                else:
                    print "Email was sent unsuccessfully!"
            else:
                print "RSS tag is not exists..."

        else:
            print "tag_id is not exists..."
            sys.exit(1)

    except MySQLdb.Error,e:
        print "Query Data Section -- Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    except Exception,er:
        print "Error %s: %s" % (er.args[0],er.args[1])
        sys.exit(1)

    cur.close()
