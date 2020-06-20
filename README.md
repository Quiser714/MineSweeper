# MineSweeper
在win10玩扫雷

<img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1592669172087&di=850fbbaced39678785b5acdf3ea2e8f4&imgtype=0&src=http%3A%2F%2Fpic.baike.soso.com%2Fp%2F20131221%2F20131221060140-2027942049.jpg" width=300 alt="扫雷">

## 闲话时间
* 游戏是用python的pygame写的，相比于虚幻引擎或unity，这玩意儿学习成本低。~~懒人的首选~~
* python文件后缀名用.pyw保存，运行时不会有控制台的小黑窗口跳出来。
* 游戏图片资源放在res文件夹里，游戏内写有一个函数加载所有资源，返回一个字典
> ```
> def loadImage():  # 载入游戏所需素材，返回库imageDict，字典类型
>     # 为配合pyinstaller，写了一个我也搞不懂什么意思的if else
>     if getattr(sys, 'frozen', False):
>         cur_path = sys._MEIPASS
>     else:
>         cur_path = os.path.dirname(__file__)
> 
>     # 创建一个空字典，准备存入图片的rect类型数据
>     imageDict = {}
> 
>     # 数字方块1-8
>     for i in range(1, 9):
>         imageDict['block{}'.format(i)] = pygame.image.load(
>             os.path.join(cur_path, r'res/{}.gif'.format(i))).convert()
> 
>     # 炸弹方块，白色
>     imageDict['bomb'] = pygame.image.load(
>         os.path.join(cur_path, r'res/bomb.gif')).convert()
> 
>     # 这里省略许多行类似的加载语句
>    
>    return imageDict   
> ```
