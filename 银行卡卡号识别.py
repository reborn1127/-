import cv2 as cv
from imutils import contours
import matplotlib as plt
import numpy as np
FIRST_NUMBER = {
	"3": "American Express",
	"4": "Visa",
	"5": "MasterCard",
	"6": "Discover Card"
}
#对模板图像做预处理
img=cv.imread("yhkmb.png")
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret,ref=cv.threshold(gray,10,255,cv.THRESH_BINARY_INV)#此步骤，应该加前面的ret,否则会报错
refCnts,hierarchy=cv.findContours(ref.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
#后面还要继续使用ref，因此需使用ref.copy()，否则会对原图做出改变；第二个参数为指定检测外轮廓；第三个参数为轮廓逼近的一种方法
cv.drawContours(img,refCnts,-1,(0,0,255),3)#-1表示绘制所有轮廓，当指定为其他值时，只在图像中选择一个绘制单个轮廓
refCnts=contours.sort_contours(refCnts,method="left-to-right")[0]#返回排序完的轮廓
digits={}#建立一个字典类型，i是轮廓索引，c是轮廓----字典类型：每个索引号对应一个索引值
for(i,c)in enumerate(refCnts):#i是轮廓索引，c是对应轮廓，则完成了对检测出来的轮廓进行了排序
    (x,y,w,h)=cv.boundingRect(c)#得到没一个外接矩形的左上坐标点以及长度、宽度
    roi=ref[y:y+h,x:x+w]#每个数字的外接矩形的尺寸
    roi=cv.resize(roi,(57,88))#重置外接矩形的尺寸至合适大小
    digits[i]=roi#每个数字对应一个模板
#对待检测图像做预处理
recKernel=cv.getStructuringElement(cv.MORPH_RECT,(10,3))#为保证检测信息准确，需去除银行卡页面杂乱信
sqKernel=cv.getStructuringElement(cv.MORPH_RECT,(2,2))#因此需要对图像做形态学操作，故在此设立卷积核
image=cv.imread("yhk.png")
image=cv.resize(image,(250,200))
gray=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
tophat=cv.morphologyEx(gray,cv.MORPH_TOPHAT,recKernel)#根据字体的大小来选定合适的核；顶帽操作来突出明亮的区域
gradx=cv.Sobel(tophat,ddepth=cv.CV_32F,dx=1,dy=0,ksize=3)#对X还是对Y需要或者同时需要根据实际需要来设定，图像梯度
gradx=np.absolute(gradx)#取绝对值
(minVal,maxVal)=(np.min(gradx),np.max(gradx))#归一化
gradx=(255*((gradx-minVal)/(maxVal-minVal)))
gradx=gradx.astype("uint8")
gradx=cv.morphologyEx(gradx,cv.MORPH_CLOSE,recKernel)#执行闭操作，使图像上的内容成块出现
ret,thresh=cv.threshold(gradx,0,255,cv.THRESH_BINARY|cv.THRESH_OTSU)#低阈值之所以设为0，是因为后面的方法选用了OTSU自动设定阈值，适合双峰的图像操作
thresh=cv.morphologyEx(thresh,cv.MORPH_CLOSE,sqKernel)#本次闭操作是为了填补二值化图像中块中的不完整小块
Cnts,hierarchy=cv.findContours(thresh.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
cnts=Cnts
curImage=image.copy()
cv.drawContours(curImage,cnts,-1,(0,0,255),3)#此处轮廓不是原图像的轮廓，而是经历了一些列运算之后的图像的轮廓
locs=[]
for (i,c)in enumerate(cnts):
    (x,y,w,h)=cv.boundingRect(c)#做出每个轮廓的外接矩形
    ar=w/float(h)#根据外接矩形的长宽比来筛选有用的矩形，并将其添加到元组中
    if ar>2.5 and ar<4.0:
        if(w>40 and w<55)and(h>10 and h<20):
            locs.append((x,y,w,h))
locs=sorted(locs,key=lambda x:x[0])#经筛选之后的轮廓
output=[]
for (i,(gx,gy,gw,gh))in enumerate(locs):#遍历每一块中的每一个数字
    groupOutput=[]
    group=gray[gy-5:gy+gh+5,gx-5:gx+gw+5]#取轮廓及其周围的区域
    cv.imshow("group",group)
    group=cv.threshold(group,0,255,cv.THRESH_BINARY|cv.THRESH_OTSU)[1]#后面的[]要加，否则会报错元组类型不能copy,下面再对每个块进行轮廓检测、绘制
    digitCnts,hierarchy=cv.findContours(group.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)#每一个group再进行轮廓检测、绘制
    digitCnts=contours.sort_contours(digitCnts,method="left-to-right")[0]
    for c in digitCnts:#计算每一组数中的每一个数值
        (x,y,w,h)=cv.boundingRect(c)
        roi=group[y:y+h,x:x+w]
        roi=cv.resize(roi,(57,88))#尺寸需与模板的尺寸对应,得到每一个数字所在的区域
        scores=[]#新建一个空列表，用来存储检测到的数字
        for (digit,digitROI)in digits.items():#在模板预处理中建立了数值的字典类型,一个为索引、一个为值
            result=cv.matchTemplate(roi,digitROI,cv.TM_CCOEFF)#匹配，返回与之匹配度最高的数值
            (_,score,_,_)=cv.minMaxLoc(result)#做10次匹配，取最大值（注意：取最大值还是最小值跟选取的模板匹配方法有关）
            scores.append(score)
        groupOutput.append(str(np.argmax(scores)))
    cv.rectangle(image,(gx-5,gy-5),(gx+gw+5,gy+gh+5),(0,0,255),1)#第一组的矩形框
    cv.putText(image,"".join(groupOutput),(gx,gy-15),cv.FONT_HERSHEY_SIMPLEX,0.65,(0,0,255),2)
    output.extend(groupOutput)
print("Credit Card Type: {}".format(FIRST_NUMBER[output[0]]))
print("Credit Card #: {}".format("".join(output)))
cv.imshow("Image",image)
cv.waitKey(0)
cv.destroyAllWindows()
