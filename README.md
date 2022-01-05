# 基于opencv的银行卡卡号识别    
## 1.背景及介绍
  随着互联网金融的兴起，人们需要在各种终端中录入银行卡号，并绑定银行卡从而进行资金交易，在卡号的录入过程中，需要对拍摄或者预先保存的银行卡图像进行卡号识别，从而将识别结果实现录入。银行卡号识别方法首先将银行卡图像进行灰度化、二值化等预处理，再定位银行卡号，最后对银行卡号进行数字识别。
## 2.项目的目标与意义
  通过基于opencv设计的程序识别银行卡上的卡号，并且该程序具有较高的识别速率和准确率，让人们不用手动输入银行卡号就能进行自动识别。本文根据银行卡号的特点，设计了一个基于模版匹配的银行卡号识别程序，经过实验发现，这个程序可以比较快速而准确地识别银行卡号，并且基本上可以保证银行卡号识别功能要求。通过对图像处理与模式识别中已有算法的分析研究，设计并实现了基于模板识别的银行卡号识别系统。不仅可以识银行卡号，其相关技术也可应用到车牌号码、护照号、身份证号或其他印刷体字符的识别。
## 3.项目的功能
  上传一张银行卡照片（前提是其上面的数字能与之前的模板相同），系统能自动识别该银行卡的卡号与类别。
## 4.项目的组成
  数字图像处理报告、数字图像处理PPT、数字图像处理过程图、实验代码
## 5.安装环境
  在python3.8环境下安装opencv，安装命令为"pip install opencv-python"。（在Anaconda Prompt终端输入）
  在python3.8环境下安装numpy，安装命令为"pip install numpy"。（在Anaconda Prompt终端输入）
  在python3.8环境下安装matplotlib，安装命令为"pip install matplotlib"。（在Anaconda Prompt终端输入）
  在python3.8环境下安装imutils，安装命令为"pip install imutils"。（在Anaconda Prompt终端输入）
## 6.参与人员
   代码部分————何磊、罗永乐
   答辩部分————刘梁兵
   PPT制作————林超煌
