from pathlib import Path
from .config import config
#from nonebot import get_driver
import os
import json
from nonebot.log import logger
#driver = get_driver()
# 插件数据代理
if config.cubplugin_datadir=="":
    from nonebot import require
    require("nonebot_plugin_localstore")
    import nonebot_plugin_localstore as store
    data_dir = store.get_data_dir("cubplugins")

    logger.warning("未配置自定义数据文件夹,将使用localstore路径->"+str(data_dir))
else:
    path_name=config.cubplugin_datadir
    data_dir = Path(Path(path_name)).absolute()
    logger.debug("已配置自定义数据文件夹!->"+str(data_dir))

    if data_dir.is_dir():
        logger.opt(colors=True).debug(f"[plugin_data]\033[0m根目录正常-\<{path_name}\>")
    else:
        #os.mkdir(path_name)
        os.mkdir(data_dir)
        logger.opt(colors=True).debug(f"[plugin_data]\033[0m初始化根目录\<{path_name}\>")

def initdata(
    conf_name,
    bashdata:dict={"status":1}
):
    conf_path = Path(data_dir / conf_name).absolute()
    config_init(conf_path,conf_name,"plugin_data",bashdata)
    return True

def rdata(
    conf_name
):
    conf_path = Path(data_dir / conf_name).absolute()
    with open(conf_path, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

def wdata(
    conf_name:str,
    data:dict
):
    conf_path = Path(data_dir / conf_name).absolute()
    with open(conf_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4,ensure_ascii=False))
    return True

def config_init(
    _path_ ,
    conf_name:str ,
    module_name:str="None" ,
    data:dict={"status":1}
):
    if _path_.is_file():
        logger.opt(colors=True).debug(f"\033[1;36;43m[util]\033[0m>>><W>{module_name}</>>>>{conf_name}-OK!")
    else:
        logger.opt(colors=True).debug(f"\033[1;36;43m[util]\033[0m>>><W>{module_name}</>>>>Create-{conf_name}!")
        with open(_path_, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4))
            f.close()

#本插件由 cubstaryow 编写