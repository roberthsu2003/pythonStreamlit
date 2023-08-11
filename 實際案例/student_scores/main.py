#codespace 要安裝中文字型
#命令列:sudo apt-get update -y
#命令列:sudo apt-get install -y fonts-wqy-zenhei
#install 要加-y
#說明網址:https://askubuntu.com/questions/490829/how-can-i-install-chinese-fonts-on-kubuntu-14-04
#字型位置:/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font=FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',size=8)
font1=FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',size=12)
#window font=FontProperties(fname=r'c:\windows\fonts\simsun.ttc',size=8)

student1 = {'國文':78, '英文':80, '數學':92, '歷史':75, '探索':85}
student2 = {'國文':90, '英文':75, '數學':98, '歷史':65, '探索':75}

subjects =list(student1.keys())
value1 =list(student1.values())
value2 = list(student2.values())

fig = plt.figure(figsize=(8,5), dpi=250, facecolor="#cccccc")
ax = fig.add_subplot(1,1,1)
ax.set_title("學生1和學生2分數比較表",fontproperties=font)
ax.set_xlabel("科目",fontproperties=font)
ax.set_ylabel("分數",fontproperties=font)
ax.plot(subjects,value1,'m-.o')
ax.plot(subjects,value2,'c--o')
ax.set_xticklabels(subjects,fontproperties=font)


x_locations = ax.get_xticks()
#y_locations = ax.get_yticks()

for i in range(len(x_locations)):
    ax.annotate(str(value1[i]),(x_locations[i]+0.03,value1[i]))
    ax.annotate(str(value2[i]),(x_locations[i]+0.03,value2[i])) 
      
value1_total = 0
value2_total = 0
for score in value1:
    value1_total += score

for score in value2:
    value2_total += score

ax.annotate(f'學生1總分{value1_total}\n學生2總分{value2_total}',(2.5,85),fontproperties=font)
ax.legend([f"學生1:{value1_total}",f"學生2:{value2_total}"],prop=font) 
plt.show()