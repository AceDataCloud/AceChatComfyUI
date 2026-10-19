# Ace Data Cloud 的 ComfyUI 聊天节点

本包对应 [ModelProviderDify](https://github.com/AceDataCloud/ModelProviderDify) 的**自填 model ID**模式。模型清单变化很快，输入精确 ID 比冻结一份下拉列表更可靠。聊天请求可能扣除 Credits，以[当前模型价格](https://platform.acedata.cloud/models?utm_source=comfyui&utm_medium=referral&utm_campaign=evergreen&utm_content=acechatcomfyui_readme_zh_cn_pricing)为准。

[English guide](../README.md)


## 当前版本与安装来源

本源码版本为 **0.1.1**，版本 ZIP 见 [GitHub Releases](https://github.com/AceDataCloud/AceChatComfyUI/releases)。下文 Registry 安装段保留 **2026-10-19 已核 Active 的 0.1.0**；该旧 ZIP 尚不包含本版更新的图文、示例或修复。需要本版时，使用对应 GitHub Release ZIP，或等 Registry 中准确的 **0.1.1** 变为 Active 后再手选该版本；不要用默认 nightly 代替已核 stable。

从 GitHub ZIP 安装：停止 ComfyUI，先备份已有同名节点目录，把 ZIP 内文件解压到 `ComfyUI/custom_nodes/ace-chat/`（不要多嵌套一层目录），在该目录运行 `python -m pip install -r requirements.txt`，然后重启并刷新。API Token 仍只配在实际启动进程环境中。GitHub ZIP 安装与 Registry/Manager 正式稳定版安装是不同路径。

## 官方安装

打开官方 [Ace Chat by Ace Data Cloud Registry页面](https://registry.comfy.org/nodes/ace-chat)，或在 **Manager → Custom Nodes Manager** 搜索 **Ace Chat**；核对下述Ace发布者/源码，找不到时再搜 **Ace Data Cloud**。选择 **Ace Chat by Ace Data Cloud**，核对发布者 **acedatacloud** 和源码仓库 [`AceDataCloud/AceChatComfyUI`](https://github.com/AceDataCloud/AceChatComfyUI)，再点击 **Install**。在 **Select Version** 版本对话框明确选择已批准的 Registry 稳定版 **0.1.0**；普通对话框可能默认高亮 **nightly**，本教程不要直接接受该选项。保留依赖自动安装。出现 **Restart Required** 后重启 ComfyUI，并刷新浏览器。Registry ID 为 `ace-chat`。

这条 Registry 稳定版安装路径已于 **2026-10-16 在原版 Linux CPU ComfyUI 0.41.0** 验证；该次安装验收没有提交生成或聊天请求。更新的宿主版本及每个收费动作仍需分别验证，模型可用性与价格以当前服务规则为准。

![真实Manager品牌搜索列表](images/manager-discovery.png)

![真实Manager重启后启用回读](images/manager-installed.png)

以上为 **2026-10-16 Linux ComfyUI0.41.0** 原图，不是新服务词实拍或收费请求；见[来源与限制](screenshot-sources.json)。

## 获取 API Key

### 复制或创建自己的 API Token

注册/登录Ace后打开**应用 → 通用应用**；无通用应用时先初始化。复制有本服务权限的已有Token，或用**管理Key → 创建**单独命名为`ComfyUI`。先核权限、有效期/允许API、Credits余额与当前价格。

![Ace应用页：复制Token或管理Key](images/get-api-key-en.png)

![Ace创建Key对话框](images/create-api-key-en.png)

以上是 **2026-10-08** SunoDify中的真实脱敏原图，第二图的示例名`Dify tutorial`在此改为`ComfyUI`，本次未创建Key。Token只配置在**实际启动ComfyUI的进程环境**`ACEDATACLOUD_API_KEY`中并重启；节点没有图示的Key输入框，不要填到prompt/JSON/工作流/截图。另一个终端的export不能配置已运行的Desktop进程。

1. 登录 [Ace Data Cloud → 应用](https://platform.acedata.cloud/console/applications?utm_source=comfyui&utm_medium=referral&utm_campaign=evergreen&utm_content=acechatcomfyui_readme_zh_cn_api_key)。新账户没有通用应用时，先选择**初始化通用应用**。
2. 打开**通用应用**，确认已开通本节点使用的服务。单服务应用的 Key 只限该服务。可复制已有 API Key；需要独立 Key 时，选择**管理 Key → 创建**，命名为 `ComfyUI`。
3. 只复制 Token 字符串，不加 `Bearer ` 或引号。平台管理 Token 不能代替节点调用 API 的 Key。若启用**允许的 API**限制，需同时包含工作流用到的提交和任务查询路径；收费动作前核对当前价格与 Credits 余额。

两个节点：**Ace Chat List Models** 只读查询 `/v1/models`，可按名称过滤；**Ace Chat Completion** 通过 `/v1/chat/completions` 发送一次非流式聊天，输出回答文本、工具调用 JSON、用量 JSON、响应 ID 和实际模型。节点只返回函数调用，不会执行函数。

## 安装与 Key

源码安装：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/AceDataCloud/AceChatComfyUI.git
cd AceChatComfyUI
python -m pip install -r requirements.txt
```

终端启动时在同一私有终端配置Token再启动：

```bash
export ACEDATACLOUD_API_KEY='在此粘贴自己的Token'
python main.py --cpu
```

在**实际 ComfyUI 进程环境**中设置 `ACEDATACLOUD_API_KEY`（也支持 `ACEDATACLOUD_API_TOKEN`），然后重启。不要把 Key 写进工作流、仓库或截图。

## 使用

导入 [01-list-models.json](../examples/01-list-models.json) 只读列出当前 Key 可见的 model ID。列表可能包含只支持其他 API 的模型；聊天节点应选择当前可用于 Chat Completions 的精确 ID，并核对权限与价格。

导入 [02-chat-completion.json](../examples/02-chat-completion.json) 前先确认价格，再只运行一次。`prompt` 和可选 `system_prompt` 适合简单对话；`messages_json` 填非空消息数组时优先使用；`tools_json` 可传 OpenAI 风格函数定义。`temperature=-1` 表示使用模型默认值。收费请求超时后先查 [Ace 控制台](https://platform.acedata.cloud/console/applications?utm_source=comfyui&utm_medium=referral&utm_campaign=evergreen&utm_content=acechatcomfyui_readme_zh_cn_api_key)记录，不自动重试。详见[隐私说明](PRIVACY.md)。

模型列表接口只读，但本版可能缓存相同图输入；确需刷新时修改`filter_text`。不要为了刷新列表改聊天输入，那可能新建收费请求；收费聊天图先关闭自动队列。

## 排错

| 现象 | 处理 |
| --- | --- |
| 缺Key/401 | 配实际启动进程的API Token并重启；管理Token不能替代API Key |
| 403 | 读具体权限/有效期/允许路径或内容限制原因，不盲目重发 |
| 429 | 等限流恢复，保留已接受任务ID，不重复付费提交 |
| JSON/模型/字段无效 | 按工具字段修正，示例`{}`/URL只是占位 |
| 超时/5xx | 再付费提交前查控制台请求/Trace记录 |
| 结果或媒体异常 | 按本服务同步/异步说明检查；pending不冒充成品 |
