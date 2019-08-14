# Resume_Recommender
基于知识图谱与人工神经网络的简历推荐系统

前端基于echarts.js, 后端基于Python Django;

特征处理阶段，技能相关特征使用知识图谱构建特征，图谱构建使用neo4j;

流程是先做二分类筛选，再给分类为正的样本进行排序；

二分类模型基于DNN，基于Keras开发;

排序函数基于随机森林的特征重要性;

系统演示如下：


<h1>首页</h1>
<div align="center"> <img src="./data/pic/1.png"/> </div>

---

<h1>原始简历查看页面</h1>
<div align="center"> <img src="./data/pic/2.png"/> </div>

---

<h1>原始简历统计分析图表展示页面</h1>
<div align="center"> <img src="./data/pic/3.png"/> </div>

---

<h1>项目简介</h1>
<div align="center"> <img src="./data/pic/4.png"/> </div>

---

<h1>招聘信息分析页面</h1>
<div align="center"> <img src="./data/pic/5.png"/> </div>

---

<h1>简历推荐结果页面</h1>
<div align="center"> <img src="./data/pic/6.png"/> </div>