# ZWTHYS · 软件与项目中心

网站：**https://zwthys-cyber.github.io/**

展示 zwthys-cyber 的公开 GitHub 项目、公开发布的下载文件与使用文档，包含 CC Pocket、Xiaote、TethrX、WQFiles、Telegram 工具、OpenWrt 等不同方向。

## 功能

- 项目分类、关键词搜索和展开全部项目。
- 从 GitHub 仓库与 Releases 生成公开目录；无发布文件的项目提供源码和文档入口。
- 保留维护项目与上游分支的区别，不将所有仓库标记为原创。
- 中文界面、手机布局、键盘操作及减少动态效果支持。
- CC Pocket 的独立介绍页保留在 `/ccpocket/install/?lang=zh`。

## 发布

`Deploy project center` 工作流在 GitHub runner 运行 `scripts/build.py`，生成 `_site/`，检查 JavaScript 语法并发布到 GitHub Pages。网站不依赖当前部署 Bridge 的服务器。

推送到 `main`、手动运行工作流或每日定时任务会刷新项目与公开发布信息。安装包发布后可手动重新运行工作流更新下载入口，无需修改首页代码。

源码为 HTML / CSS / JavaScript，目录生成器只使用 Python 标准库。GitHub token 只在 Actions 环境中用于读取公开元数据，不会写入网页。
