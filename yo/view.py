from django.http import HttpResponse
from django.template import Context, loader
import urllib.request
import datetime
import xlrd
import pymysql
# import MySQLdb
import paramiko
from sshtunnel import SSHTunnelForwarder
import os
import time
import cgi, cgitb

from yo.settings import BASE_DIR


class downloadvideo(object):
    def __init__(self):
        self.loc = ("/Users/chuck/Dropbox (Personal)/quvideo/hotvideo/hot.xls")
        self.urlfile = "/Users/chuck/Dropbox (Personal)/quvideo/vidstatus/Daily top videos from vids/video/tamil/id_in.txt"
        self.urllist = []
        self.hot = {}
        self.hotDtrPuid = []

    # def mediaupload(request):
    #     if 'POST' == request.method:
    #         form = PicForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             files = request.FILES.getlist('pic')
    #             for f in files:
    #                 destination = open('d:/temp/' + f.name, 'wb+')
    #                 for chunk in f.chunks():
    #                     destination.write(chunk)
    #                 destination.close()
    #         # ...
    #         # othercodes
    #         # ...

    # extract the best dtr video puid list
    def manuExc(self,requestDtr = 0,play_uv_3sR=0,lang=''):

        # print(111)
        print(lang)

        wb = xlrd.open_workbook(self.loc)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0,0)
    #    for i in range(sheet.ncols):
    #        print(sheet.cell_value(0,i))

        # for i in range(sheet.nrows):
        #     print(i)
        #     print(sheet.cell_value(i+1,15))
        #print the download_uv value
        lan_list = sheet.col_values(16)
        # print(lan_list)
        puid_list = sheet.col_values(0)
        # print(puid_list)
        download_uv_dic = sheet.col_values(14)
        # print(download_uv_dic[1])
        play_uv_dic = sheet.col_values(4)
        # print(download_uv_dic)
        #cal the dtr
        str = '';
        for i in range(1, sheet.nrows):
            # print(download_uv_dic[i])
            # print(play_uv_dic[i])
            dtr = download_uv_dic[i]/play_uv_dic[i]
            # print(lan_list[i])
            # print(dtr)
            if dtr > requestDtr and lan_list[i] == lang and play_uv_dic[i] > play_uv_3sR:
                # print(dtr)
                # ['{:.0f}'.format(x) for x in nums]
                self.hotDtrPuid.append('{:.0f}'.format(puid_list[i]))
                temp = ('{:.0f}'.format(puid_list[i]))
                str = str + temp + ',';

                # file.write('{:.0f}'.format(puid_list[i]))
                # print('write success')
        #sample_list = [line + '\n' for line in self.hotDtrPuid]
        # file = open('/Users/chuck/Dropbox (Personal)/quvideo/hotvideo/tamil_puid.txt', 'w')
        # file.writelines(sample_list)
        return str + '999999999'


        # db = pymysql.connect("47.88.220.16","vivashow_read","VishOW@519#REAd","vivashowcenter")
        # cursor = db.cursor()
        # cursor.execute("SELECT VERSION()")
        # data = cursor.fetchone()
        # print("Database version : %s " % data)
        # db.close()
    def connection(self,e):
        private_key_path = '/Users/chuck/.ssh/id_rsa'
        rsaKey = paramiko.RSAKey.from_private_key_file(private_key_path)

        ssh = paramiko.SSHClient()
        # print(1111)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print(111)
        ssh.connect('47.88.220.16', 22, 'jianbinyang', rsaKey)
        ssh._families_and_addresses('rr-t4n4awd847oh9074i.mysql.singapore.rds.aliyuncs.com', 3306)
        # print(555)
        # return ssh

        with SSHTunnelForwarder(
                ('47.88.220.16', 22),
                ssh_username="jianbinyang",
                ssh_pkey="/Users/chuck/.ssh/id_rsa",
                ssh_private_key_password="secret",
                remote_bind_address=('rr-t4n4awd847oh9074i.mysql.singapore.rds.aliyuncs.com', 3306),
                local_bind_address=('127.0.0.1', 3307)) as tunnel:
            # time.sleep(100000)

        # print('FINISH!')
        # print('conenct to server!')
        #
        # stdin, stdout, stderr = ssh.exec_command('pwd')
        # std  = stdout.read()
        # print(std)
        # connect mysql
            conn = pymysql.connect(host = '127.0.0.1',
                               user = 'vivashow_read',
                               passwd = 'VishOW@519#REAd',
                               db = 'vivashowcenter',
                               port = 3307)
            # print("333333")
            cursor = conn.cursor()
            print(e)
            #e====.1,2,3,4(str)
            print("SELECT file_url FROM video_publish WHERE id in ("+e+");")
            cursor.execute("SELECT file_url,id FROM video_publish WHERE id in ("+e+");")
            data = cursor.fetchall()
            # print(data)
            # print(type(data))
            fileUrllist = list(data)
            # print(fileUrllist)
            for i in fileUrllist:
                # print(i[0])
                self.hot[i[0]]=i[1]

            # print(self.hot)
            # print(fileUrllist)
            for i in fileUrllist:
                self.urllist.append(i[0])
                # temp2 = ('{:.0f}'.format(i[0]))
            # url_list = [line + '\n' for line in self.hotDtrPuid]
            # print(self.urllist)

            # file = open('/Users/chuck/Dropbox (Personal)/quvideo/vidstatus/Daily top videos from vids/video/tamil/id_in2.txt', 'w')
            # file.writelines(i[0])
            # return fileUrllist
            # print(fileUrllist)
            conn.close()

            # print('FINISH!')

    def download(self,e):

        # urlfile = open("/Users/chuck/Downloads/httpvideo-v.pdf", "r")
        #
        # print(urlfile.read())
        # with open(self.urlfile) as f:
        #     url = f.readlines()
        #     print(url)
        # puidlist = self.urllist.split(",")
        for i in self.urllist:
            # self.urllist = i
            # print(i)
            now = datetime.datetime.now()
            date = now.strftime('%m-%d-%y')
            # print(self.hot[i])
            # filename = 'tamil_' + date + '_' + i.split("/mp4")[1].split(".mp4")[0].replace('/','') + '.mp4'
            filename = 'tamil_' + date + '_' + str(self.hot[i]) + '.mp4'
            # print(filename)
            # print(self.urllist)
            filepath = '/Users/chuck/Dropbox (Personal)/quvideo/vidstatus/Daily top videos from vids/video/tamil/'+filename
            print(filepath)
            rsp = urllib.request.urlretrieve(i, filepath)

            print("download successful!")
        # url = "http://video-vivashow.xiaoying.tv/vivashow/mp4/1966740095406743976.mp4"
        # with urllib.request.urlopen("http://video-vivashow.xiaoying.tv/vivashow/mp4/1966740095406743976.mp4") as url:
        #     s = url.read()
        # rsp = urllib.request.urlretrieve(url, '/Users/chuck/Downloads/doadwnlo/yo.mp4')

        #
        # test=urllib.FancyURLopener()
        #
        #
        # test.retrieve("http://video-vivashow.xiaoying.tv/vivashow/mp4/1966740095406743976.mp4","/Users/chuck/Dropbox (Personal)/quvideo/vidstatus1966740095406743976.mp4")




def hello(request):
    return HttpResponse("hello world")


def index(request):
    template = loader.get_template("vidsdownload.html")
    return HttpResponse(template.render())

def post(self, request):
    template = loader.get_template("vidsdownload.html")
    return HttpResponse(template.render())
    obj = request.FILES.get('fafafa', '1')
    print(obj.name)
    f = open(os.path.join(BASE_DIR, 'media', 'image', obj.name), 'wb')
    for chunk in obj.chunks():
        f.write(chunk)
    f.close()
    # return render(request, 'clashphone/test.html')
    return HttpResponse('OK')



def add(request):
    f = request.FILES['file']
    with open('a.mp4', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # language = request.GET["lan"]
    # print(language)
    # dir = request.GET["DTR"]
    # play_uv_3s = request.GET['play_uv_3s']
    # ali = downloadvideo()
    # e = ali.manuExc(float(dir),int(play_uv_3s),language)
    # ali.connection(e)
    # ali.download(e)
    # return HttpResponse('Success :' +dir + "play_uv_3s:" + play_uv_3s )
