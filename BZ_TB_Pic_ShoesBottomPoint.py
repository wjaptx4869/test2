# -*- coding: utf-8 -*-

from _X import *

#--------------------------
# Function
# 1.自动分析图片鞋底
# 2.
# 3.
#--------------------------
# Usage
# 1.直接启动服务
# 2.
# 3.
#--------------------------
# Update
# 2018-06-28	Xwolf	优化性能
# 2018-06-28	Xwolf	修改Python2.7到3.6,升级后的错误
# 2018-05-16	Xwolf	分割图片,分成多分传输
# 2018-05-10	Xwolf	开发
#--------------------------
def X():
	#--------------------------
	a = [0]*10
	a[1-1] = 'BZ_ShoesBottomPoint'		# table名称
	a[2-1] = X_Main					# 函数
	X_Init(a, 1)
	#--------------------------
	
def X_Main(p_a, p_mode):
	#--------------------------
	id = p_a[1-1]
	#--------------------------

	#--------------------------
	a = [0]*10
	a[1-1] = id	# 需要处理的数据
	r = X_1(a, 1)
	#--------------------------
	
	
def X_1(p_a, p_mode):
	#--------------------------
	id = p_a[1-1]
	#--------------------------
	
	#--------------------------
	C('46.获取文件路径')
	#--------------------------
	a = []
	a.append('select app_path2 from BZ_ShoesBottomPoint where id={};'.format(id))
	a_rows = X_SQL(a, 1)
	#--------------------------
	app_path2 = a_rows[0][0]
	app_path2 = re.sub(r'\\', '/', app_path2)
	C('53.app_path2:{}'.format(app_path2))
	if os.path.exists(app_path2)==False:raise ValueError('57.Error:文件不存在:{0}'.format(app_path2))
	#--------------------------

	C('56.读取图片数据')
	#--------------------------
	a = [0]*10
	a[1-1] = app_path2		# 路径
	app_path2 = X_cv2_imread_path(a, 1)
	#--------------------------
	
	img = cv2.imread(app_path2, 0)

	# 使用算法
	# 在Sobel函数的第二个参数这里使用了cv2.CV_16S。因为OpenCV文档中对Sobel算子的介绍中有这么一句：“in the case of 8-bit input images it will result in truncated derivatives”。即Sobel函数求完导数后会有负值，还有会大于255的值。而原图像是uint8，即8位无符号数，所以Sobel建立的图像位数不够，会有截断。因此要使用16位有符号的数据类型，即cv2.CV_16S。
	gray = cv2.Laplacian(img, cv2.CV_8U, ksize=3)
	
	# 灰度图转换为二值图
	ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
	
	# 获取轮廓
	# contours	轮廓本身	列表,一个个的闭合的轮廓数据 可以用len(contours)分析出轮廓的数量
	# hierarchy	每条轮廓对应的属性
	_, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	C('70.显示轮廓数量:{}'.format(len(contours)))
	
	C('72.分析出某个轮廓的极值')
	a1 = []
	for a2 in contours:
		index = a2[:,:,1].argmax()
		# C('165.获取当前轮廓,该坐标点数据')
		s = a2[:,0][index]
		a1.append(list(s))
	
	C('80.将数组转换为np格式')
	a3 = np.array(a1)
	
	index = a3[:,1].argmax()
	C('85.从所有轮廓中,分析出最底部下标:{}'.format(index))
	
	a_r = a3[:,:][index]
	C('88.最底部坐标:{}'.format(list(a_r)))
	
	text = str(a_r)
	
	# 画小圆点
	# bottommost_new = tuple(a_r)
	# C(bottommost_new)
	# cv2.circle(img2, (100,100), 2, (0,0,255), 3)
	# cv2.circle(img2, bottommost_new, 2, (0,0,255), 3)
	# cv2.imwrite('images/1/2.jpg', img2)
	
	#--------------------------
	C('109.更新table')
	#--------------------------
	a = []
	a.append('update BZ_ShoesBottomPoint set app_station=1,app_return="{1}" where id={0};'.format(id,text))
	rows = X_SQL(a, 1)
	#--------------------------

X()
cv2.waitKey(0)
sys.exit(0)
