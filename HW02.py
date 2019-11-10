import requests  # 爬取网页
from bs4 import BeautifulSoup # 解析网页
import re

ID=input('请输入十八位身份证号码: ')
if len(ID)==18:
  print('')
  print("你的身份证号码是: "+ID)
else:
  print("错误的身份证号码") #检验是否为18位

ID_area=ID[0:6]
ID_birth=ID[6:14]
ID_sex=ID[14:17]
ID_check=ID[17]
province = {}
city = {}
county = {}

url = 'http://www.mca.gov.cn/article/sj/xzqh/1980/201903/201903011447.html' #网页链接
response = requests.get(url)
information = response.text

pro_c = re.findall(r'<td class=xl723852>(\d{6})</td>', information)
pro_z = re.findall(r'<td class=xl723852>.*?([\u4E00-\u9FA5]+).*?</td>', information)
con_c = re.findall(r'<td class=xl733852>(\d{6})</td>', information)
con_z = re.findall(r'<td class=xl733852>.*?([\u4E00-\u9FA5]+).*?</td>', information, re.S)

#省市级 ：
for i in range(len(pro_c)):
    str1 = ''.join(pro_c[i])
    flag = int(str1[-4:6])
    if flag == 0:
        province[pro_c[i]] = pro_z[i]
    else:
        city[pro_c[i]] = pro_z[i]
#县级：     
for j in range(len(con_c)):
    county[con_c[j]] = con_z[j]

#以下部分为错误判断，来检验是否符合国家校验码标准
W=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
ID_CHECK=['1','0','X','9','8','7','6','5','4','3','2']
ID_num=0
for i in range(len(W)):
 ID_num=ID_num+int(ID[i])*W[i]
print('') 
ID_Check=ID_num%11
if ID_check==ID_CHECK[ID_Check]:
  print('符合校验规则的身份证号码!\n')
else:
  print('不符合校验规则的身份证号码!\n')  

#解析出生地区
if ID_check==ID_CHECK[ID_Check]:
    j = 1
else:
    j = 0

if j == 1:
    pan = ''.join(ID_area)
    pro = str(pan[0:2])+'0000'
    cit = str(pan[0:4])+'00'
    n1 = ID_area in county.keys()
    n2 = cit in city.keys()
    n3 = pro in province.keys()
    print('出生地区：',end=' ')
    if n1 == True and n2 == True and n3 == True:
        print(f'{province[pro]}{city[cit]}{county[str(ID_area)]}')
    elif n1 == False and n2 == True and n3 == True:
        print(f'{province[pro]}{city[cit]}')
    elif n3 == True and n1 == False and n2 == False:
        print(f'{province[pro]}')
    else:
        print('不符合国家行政区划代码！')

#解析出生日期
year=ID_birth[0:4]
moon=ID_birth[4:6]
day=ID_birth[6:8]
print('')
print("出生日期: "+year+'年'+moon+'月'+day+'日')

#解析性别 
print('')
if int(ID_sex)%2==0:
  print('性别：女\n')
else:
  print('性别：男\n')