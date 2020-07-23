# WINDOWS  
1.安装`python3.8*`  
2.执行`configure.py`  
定位输入  
南校区：  
`{"type":"complete","info":"SUCCESS","status":1,"VDa":"jsonp_980898_","position":{"Q":34.122061903212,"R":108.83052978515701,"lng":108.83053,"lat":34.122062},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"029","adcode":"610113","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"雷甘路","streetNumber":"264号","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道西安电子科技大学长安校区","roads":[],"crosses":[],"pois":[]}`  
北校区：  
`{"type":"complete","info":"SUCCESS","status":1,"VDa":"jsonp_980898_","position":{"Q":34.23254,"R":108.91514000000001,"lng":108.91514,"lat":34.23254},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"029","adcode":"610113","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"白沙路","streetNumber":"付8号","country":"中国","province":"陕西省","city":"西安市","district":"雁塔区","township":"电子城街道"},"formattedAddress":"陕西省西安市雁塔区电子城街道西安电子科技大学北校区","roads":[],"crosses":[],"pois":[]}`  
3.打开`submit.py`测试  
4.右键win键-计算机管理-任务计划程序  
在右边有创建基本任务  
5.创建基本任务：随意填  
6.触发器：每天  
选个低峰的时间  
7.操作：启动程序  
8.程序或脚本：写`python`安装目录中的`python.exe`  
添加参数：填写脚本的位置中的`submit.py`  
起始于：填写脚本的路径  

# LINUX  
虚拟机炸了，写大概思路吧  
1.安装`python3.8*`  
2.执行`configure.py`  
定位输入  
南校区：  
`{"type":"complete","info":"SUCCESS","status":1,"VDa":"jsonp_980898_","position":{"Q":34.122061903212,"R":108.83052978515701,"lng":108.83053,"lat":34.122062},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"029","adcode":"610113","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"雷甘路","streetNumber":"264号","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道西安电子科技大学长安校区","roads":[],"crosses":[],"pois":[]}`  
北校区：  
`{"type":"complete","info":"SUCCESS","status":1,"VDa":"jsonp_980898_","position":{"Q":34.23254,"R":108.91514000000001,"lng":108.91514,"lat":34.23254},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"029","adcode":"610113","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"白沙路","streetNumber":"付8号","country":"中国","province":"陕西省","city":"西安市","district":"雁塔区","township":"电子城街道"},"formattedAddress":"陕西省西安市雁塔区电子城街道西安电子科技大学北校区","roads":[],"crosses":[],"pois":[]}`  
3.设置`crontab`  

# TODO
* 优化获取定位的代码  
* 晨午检
* 反馈代码
* 学习使用`github`
# 写在最后
我其实只是个不会写代码的萌新，看了[大佬的代码](https://github.com/Apache553/xidian-ncov-report)，再学习了一点点`python`，才把教程写出来了。
