# Weather Voice Prompt
🌈 Get The Weather INFO Then Ouput Voice Prompt And Send It To Your WeChat

## OS
* `Raspberry Pi 4B 4GB`

## Env
* `Python 3.7`
* `urllib`
* `apscheduler`
* `baidu-aip`
* `Baidu AIP SDK( aip-python-sdk-2.2.15 )`

## How To Run On RasPi 4B
you need to install the dependencies firstly
> $ pip3 install apscheduler

> $ cd aip-python-sdk-2.2.15

> $ pip3 install baidu-aip

> $ python3.7 setup.py install

then run it
> $ python3.7 weather.py

## Bug fixed
* [ImportError no module named 'xxx'. . .](https://stackoverflow.com/questions/62154632/importerror-no-module-named-playsound)
* [ValueError: Namespace Gtk not available. . .](https://www.e-learn.cn/topic/3787817)

## Thanks
* [ServerChan](http://sc.ftqq.com/3.version)
* [Baidu AI of voice technology](https://ai.baidu.com/ai-doc/SPEECH/)
* [Weather voice prompt by python](https://www.cnblogs.com/daniumiqi/p/12171186.html)
* [How to Text To Speech by baidu AI](https://blog.csdn.net/weixin_44897649/article/details/103173247)
