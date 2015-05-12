# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Odoo Connector
# QQ:35350428
# 邮件:sale@100china.cn
# 手机：13584935775
# 作者：'cheng_000'
# 公司网址： www.odoo.pw  www.100china.cn
# Copyright 昆山一百计算机有限公司 2012-2016 Amos
# 日期：2014-06-18
#未解决问题：1、odoo有很多个分支。无法copy其他分支
            # 2、更新时间周期长，无法表达每次更新内容。

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import  urllib2
from bs4 import BeautifulSoup
import os
import datetime
import subprocess
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def github2osc():
    subprocess.call('rm -rf /root/gitallen/odoo/*', shell=True)
    subprocess.call('cp -r /root/gitodoo/odoo/* /root/gitallen/odoo/', shell=True)


file_tmp = open("/root/gitodoo/odoo/update.log",'a')
file_tmp.write('\r\n')
file_tmp.write('本次运行时间：%s' % str(datetime.datetime.now()))
file_tmp.write('\r\n')
file_tmp.close()
#获取更新页面
url = "https://github.com/odoo/odoo"
response = urllib2.urlopen(url)
result = response.read()
html = BeautifulSoup(result)

os.chdir("/root/gitodoo/odoo/")
var = 0
fix = []  #存放更新说明
#获取每次修改记录，并与历史记录比较，最终将记录存入fix.log文件中
try:
    file_tmp = open('fix.log', 'rb')
except IOError:
    pass
b = html.find('div',attrs={'class':'commit commit-tease js-details-container'}).find('p',attrs={'class':'commit-title'}).find('a',attrs={'class':'message'})
try:
    tmp = file_tmp.read()
except IOError:
    tmp = ''
except NameError:
    tmp = ''
tmp1 = str(b['title'])
if tmp != tmp1:
    var =var + 1
    fix.append(tmp1)


try:
    file_tmp.close()
except NameError:
    pass

#删除原来fix。log文件，并加新修改添加至其中
if var > 0:
    try:
        os.remove('fix.log')
    except OSError:
        pass
    file_tmp = open('fix.log', 'ab')
    for a in fix:
        file_tmp.write(a)
    file_tmp.close()
    #subprocess.call('git pull git@github.com:odoo/odoo.git 8.0:master', shell=True)
    subprocess.call('git pull git@github.com:odoo/odoo.git 8.0:master', shell=True)
    github2osc()
    os.chdir("/root/gitallen/odoo")
    subprocess.call('cp /root/README.md /root/gitallen/odoo/', shell=True)
    subprocess.call('git add .', shell=True)
    subprocess.call('git commit -a -m "%s"' % fix[0] , shell=True)
    # subprocess.call('git pull origin master' , shell=True)
    subprocess.call('git push origin master', shell=True) #可能会出现ssh_exchange_identification: connection closed by remote host
                                                                # 解决: 删除/root/。ssh/known_hosts
                                                            #可能出现 error:failed to push som refs to .......
                                                            # 解决：git pull origin master然后再push
                                                        # 可能会出现fatal: Couldn't find remote ref master或者fatal: 'origin' does not appear to be a git repository以及fatal: Could not read from remote repository.
                                                       #解决办法  git remote add origin git@git.oschina.net:Odoo/Odoo.git
    file_tmp = open("/root/gitodoo/odoo/update.log",'a')
    file_tmp.write('\r\n')
    file_tmp.write(u'系统更新完毕') 
    file_tmp.write(u'更新内容：%s' % fix[0])
    file_tmp.write(str(datetime.datetime.now()))
    file_tmp.write('\r\n')
    file_tmp.close()
#clone code
else:
    file_tmp = open("/root/gitodoo/odoo/update.log",'a')
    file_tmp.write('\r\n')
    file_tmp.write(u"系统无更新")
    file_tmp.write(str(datetime.datetime.now()))
    file_tmp.write('\r\n')
    file_tmp.close()


#file_tmp.close()
#
# # <time is="relative-time" datetime="2015-04-14T22:26:18Z" title="Apr 15, 2015, 6:26 AM GMT+8">7 hours ago</time>
# #将每次修改时间追加写入time.log文件中
# file_tmp = open('time.log', 'wb+')
# for b in html.find_all("time",):
#     file_tmp.write(str(b).join('\r\n'))
# file_tmp.close()
#
#
# #从fix。log中读取一行出来进行比较
# file_tmp = open('fix.log', 'rb+')
# print file_tmp.readline()
# file_tmp.close()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
