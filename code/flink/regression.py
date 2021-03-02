import numpy as np

class LogisticRegression:
    
    #默认没有正则化，正则项参数默认为1，学习率默认为0.001，迭代次数为10001次
    def __init__(self,penalty = None,Lambda = 1,a = 0.001,epochs = 10001):
        self.W = None
        self.penalty = penalty
        self.Lambda = Lambda
        self.a = a
        self.epochs =epochs
        self.sigmoid = lambda x:1/(1 + np.exp(-x))   
        
    def loss(self,x,y):
        m=x.shape[0]
        y_pred = self.sigmoid(x * self.W)
        return (-1/m) * np.sum((np.multiply(y, np.log(y_pred)) + np.multiply((1-y),np.log(1-y_pred))))
    
    def fit(self,x,y):
        lossList = []
        #计算总数据量
        m = x.shape[0]
        #给x添加偏置项
        X = np.concatenate((np.ones((m,1)),x),axis = 1)
        #计算总特征数
        n = X.shape[1]
        #初始化W的值,要变成矩阵形式
        self.W = np.mat(np.ones((n,1)))
        #X转为矩阵形式
        xMat = np.mat(X)
        #y转为矩阵形式，这步非常重要,且要是m x 1的维度格式
        yMat = np.mat(y.reshape(-1,1))
        #循环epochs次
        for i in range(self.epochs):
            #预测值
            h = self.sigmoid(xMat * self.W)
            gradient = xMat.T * (h - yMat)/m
            
            
            #加入l1和l2正则项，和之前的线性回归正则化一样
            if self.penalty == 'l2':
                gradient = gradient + self.Lambda * self.W
            elif self.penalty == 'l1':
                gradient = gradient + self.Lambda * np.sign(self.W)
          
            self.W = self.W-self.a * gradient
            if i % 50 == 0:
                lossList.append(self.loss(xMat,yMat))
		#返回系数，和损失列表
        return self.W,lossList

 

from sklearn.datasets import make_classification
from matplotlib import pyplot as plt
#生成2特征分类数据集
x,y =make_classification(n_features=2,n_redundant=0,n_informative=1,n_clusters_per_class=1,random_state=2043)

# #第一个特征作为x轴，第二个特征作为y轴
# plt.scatter(x[:,0],x[:,1],c=y)
# plt.show()


#默认参数
#lr = LogisticRegression(penalty='l2',Lambda=1)
lr = LogisticRegression(Lambda=2)
w,lossList = lr.fit(x,y)

#前面讲过，z=0是线性分类临界线
# w[0]+ x*w[1] + y* w[2]=0,求解y (x,y其实就是x1,x2)
x_test = [[-1],[0.7]]
y_test = (-w[0]-x_test*w[1])/w[2] 

plt.scatter(x[:,0],x[:,1],c=y)
plt.plot(x_test,y_test)
plt.show()


from sklearn.linear_model import LogisticRegression as LR
clf = LR(penalty='none') #查看系数可知，默认带L2正则化，且正则项参数C=1，这里的C是正则项倒数，越小惩罚越大，这里也不用正则化
clf.fit(x,y)
print('sklearn拟合的参数是：\n','系数：',clf.coef_,'\n','截距：',clf.intercept_)

y_pred_1 = clf.predict(x)
print('\n')
print(classification_report(y,y_pred_1))