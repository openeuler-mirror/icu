# icu

#### 介绍
如今的软件市场是一个全球性的市场，应用程序需要支持和维护多种不同语言。The International Components for Unicode（ICU）库提供了针对不同平台的强大且功能齐全的Unicode服务，以帮助实现这一设计目标。ICU库对以下方面提供支持：

- 支持Unicode标准的最新版本。
- 支持超过220个代码页的字符集转换。
- 支持超过300个语言环境的数据。
- 支持敏感语言整理（排序）和基于Unicode Collation算法（ISO 14651）的搜索。
- 支持正则表达式匹配和Unicode集。
- 支持规范化、大写/小写、脚本音译的转换（50 对以上）。
- 支持用于存储和访问本地化信息的资源包。
- 支持日期/数字/消息格式和特定于文化的输入/输出格式的解析。
- 支持日历特定的日期和时间操作。
- 支持用于查找字符、单词和句子边界的文本边界分析。

ICU有一个姊妹项目ICU4J，将Java的国际化能力扩展到了类似于ICU的水平。当需要区分时，ICU C/C++项目也称为ICU4C。

#### 软件架构
软件架构说明

#### 安装教程
Linxu环境编译命令：

```
$ tar -zxvf icu4c-67_1-src.tgz
$ cd icu/source
$ chmod +x runConfigureICU configure install-sh
$ ./runConfigureICU Linux
$ make
$ make check
$ make install
```

#### 使用说明
1. 下载并编译ICU
2. 按照API文档的示例使用所需接口

#### 参与贡献
1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request