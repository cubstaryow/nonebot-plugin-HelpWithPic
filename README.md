<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-HelpWithPic

_✨ nonebot插件-动态帮助图片制作 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/cubstaryow/nonebot-plugin-HelpWithPic.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-HelpWithPic">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-HelpWithPic.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>





## ⚠ 注意
因为我是小白,我只能以我自己的方式写我觉得可能挺好用的插件()
所以部分代码逻辑可能不是很好
此插件部分代码参考 nonebot-plugin-picstatus (制图与部分资源获取)


## 📖 介绍

这里是插件的详细介绍部分

## 💿 安装

暂时未完成上传PYPI，目前只能下载源码使用。

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-HelpWithPic

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-HelpWithPic
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-HelpWithPic
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-HelpWithPic
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-HelpWithPic
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_HelpWithPic"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| ps_font | 否 | None | 配置说明 |
| ps_custom_bg | 否 | [] | 图片背景,需要以file:///开头,比如['file:///./data/draw/default_bg1.png'] |
| version | 否 | "Unknow" | 可以填你的bot版本 |
| HWP_commandstart | 否 | "#" | 自定义命令头 |
| HWP_nickname | 否 | "本bot的帮助文档" | 标题 |
| HWP_text | 否 | "你想要的,我们都没有(不是\n这是描述" | 描述 |
| plugin_version | 否 | "HelpWithPic-Beta1.0"  | 插件版本 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| #help | user | 否 | 群聊/私聊 | 请根据HWP_commandstart使用 |
