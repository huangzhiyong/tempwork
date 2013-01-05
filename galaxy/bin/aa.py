# - * - coding: utf-8 -*-
msg = "赵总，您好!\n\t下面是今天粉丝排在前三十的品牌\n\t\taa 1"
print msg

import smtplib
from email.Header import Header
from email.mime.text import MIMEText
