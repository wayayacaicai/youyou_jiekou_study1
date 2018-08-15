# -*- coding: UTF-8 -*-
import os,time
import unittest
import HTMLTestRunner
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
#当前所在文件真实路径
cur_path = os.path.dirname(os.path.abspath(__file__))

def add_case(caseName='case', rule='test*.py'):
    '''第一步：加载所有的用例'''
    case_path = os.path.join(cur_path, caseName)

    if not os.path.exists(case_path):
        os.mkdir(case_path)
    print('test case path：%s' % case_path)

    suite = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(start_dir=case_path,
                                                   pattern=rule,
                                                   top_level_dir=None)
    for test_suite in discover:
        for test_case in test_suite:
            suite.addTest(test_case)
    return suite

def run_case(all_case, reportName='report'):
    '''第二步：执行所有的用例，并把结果写入HTML测试报告'''
    now = time.strftime("%Y_%m_%d %H_%M_%S")
    report_path = os.path.join(cur_path, reportName)

    if not os.path.exists(report_path):
        os.mkdir(report_path)
    print('test report path: %s' % report_path)

    report_abspath = os.path.join(report_path, now+'result.html')
    try:
        fp = open(report_abspath, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                               title=u'自动化测试报告，测试结果如下:',
                                               description=u'用例执行情况:')
        runner.run(all_case)
        fp.close()
    except Exception as e:
        print(e)

    return report_path

#如果第二步不加时间戳，只是生成 result.html，那这一步其实没卵用，
# 可以 忽略 （个人觉得报告用一个名称 result.html 就行,
# 新的自动覆盖旧的，加时间戳虽 然可以装逼，但是最后集成 jenkins 会不好弄）
def get_report_file(report_path):
    '''第三步：获取最新的测试报告'''
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)),
               reverse=False)
    print(lists)
    print(u'最新的测试报告：'+lists[-1])

    report_file = os.path.join(report_path, lists[-1])
    return report_file

def send_email(smtp_server, port, sender, pwd, recver, report_file):
    '''第四步：发送最新的测试报告内容'''
    with open(report_file, 'rb') as f:
        data_body = f.read()
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recver
    msg['Subject'] = Header(s=u'自动化测试报告', charset='utf8')

    body = MIMEText(data_body, _subtype='html', _charset='utf8')
    msg.attach(body)

    att1 = MIMEText(data_body, 'base64', 'utf8')
    att1['Content-Type'] = 'application/octet-stream'
    att1['Content-Disposition'] = "attachment;filename = newest_report.html"
    msg.attach(att1)

    try:
        try:
            smtp = smtplib.SMTP_SSL(smtp_server, port)
        except:
            smtp = smtplib.SMTP()
            smtp.connect(smtp_server, port)
        finally:
            smtp.login(sender, pwd)
            smtp.sendmail(sender, recver, msg.as_string())
            smtp.quit()
            print(u'邮件发送成功')
        # smtp = smtplib.SMTP_SSL(smtp_server, port)
        # smtp.login(sender, pwd)
        # smtp.sendmail(sender, recver, msg.as_string())
        # smtp.quit()
        # print(u'邮件发送成功')
    except Exception as e:
        print(u'邮件发送失败')
        print(e)

if __name__ == '__main__':
    all_case = add_case()  #加载用例

    report_path = run_case(all_case)  #执行用例

    report_file = get_report_file(report_path)  #获取最新用例

    from config import readConfig
    smtp_server = readConfig.smtp_server
    port = readConfig.port
    sender = readConfig.sender
    pwd = readConfig.pwd
    recver = readConfig.receiver

    send_email(smtp_server, port, sender, pwd, recver, report_file)













