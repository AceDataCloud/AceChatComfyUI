# Ace Data Cloud 的 ComfyUI 聊天节点

本包对应 [ModelProviderDify](https://github.com/AceDataCloud/ModelProviderDify) 的**自填 model ID**模式。模型清单变化很快，输入精确 ID 比冻结一份下拉列表更可靠。聊天请求可能扣除 Credits，以[当前模型价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acechatcomfyui_readme_zh_cn_pricing)为准。

[English guide](../README.md)

## 获取 API Key

1. 登录 [Ace Data Cloud → 应用](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acechatcomfyui_readme_zh_cn_api_key)。新账户没有通用应用时，先选择**初始化通用应用**。
2. 打开**通用应用**，确认已开通本节点使用的服务。单服务应用的 Key 只限该服务。可复制已有 API Key；需要独立 Key 时，选择**管理 Key → 创建**，命名为 `ComfyUI`。
3. 只复制 Token 字符串，不加 `Bearer ` 或引号。平台管理 Token 不能代替节点调用 API 的 Key。若启用**允许的 API**限制，需同时包含工作流用到的提交和任务查询路径；收费动作前核对当前价格与 Credits 余额。

两个节点：**Ace Chat List Models** 只读查询 `/v1/models`，可按名称过滤；**Ace Chat Completion** 通过 `/v1/chat/completions` 发送一次非流式聊天，输出回答文本、工具调用 JSON、用量 JSON、响应 ID 和实际模型。节点只返回函数调用，不会执行函数。

## 安装与 Key

Registry 版本激活后，在 ComfyUI-Manager 搜索 **Ace Chat**，确认发布者 `acedatacloud` 与包名 **Ace Chat by Ace Data Cloud**，安装并重启。Registry ID 为 `ace-chat`，源码仓库为 `AceDataCloud/AceChatComfyUI`。源码可下载或 Registry 上传成功都不代表市场可安装。

源码安装：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/AceDataCloud/AceChatComfyUI.git
cd AceChatComfyUI
python -m pip install -r requirements.txt
```

在**实际 ComfyUI 进程环境**中设置 `ACEDATACLOUD_API_KEY`（也支持 `ACEDATACLOUD_API_TOKEN`），然后重启。不要把 Key 写进工作流、仓库或截图。

## 使用

导入 [01-list-models.json](../examples/01-list-models.json) 只读列出当前 Key 可见的 model ID。列表可能包含只支持其他 API 的模型；聊天节点应选择当前可用于 Chat Completions 的精确 ID，并核对权限与价格。

导入 [02-chat-completion.json](../examples/02-chat-completion.json) 前先确认价格，再只运行一次。`prompt` 和可选 `system_prompt` 适合简单对话；`messages_json` 填非空消息数组时优先使用；`tools_json` 可传 OpenAI 风格函数定义。`temperature=-1` 表示使用模型默认值。收费请求超时后先查 [Ace 控制台](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acechatcomfyui_readme_zh_cn_api_key)记录，不自动重试。详见[隐私说明](PRIVACY.md)。
