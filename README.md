# llama.cpp Model Manager（llama-manager）

可视化模型管理台：管理本地 [llama.cpp](https://github.com/ggml-org/llama.cpp) 多模型的**启停、切换、参数配置与实时监控**，告别每次手动翻找 `run-*.bat` 脚本。

支持**浏览器模式**（纯 Python 标准库，零依赖）与**桌面 GUI 模式**（pywebview 原生窗口，可打包为独立 EXE）。

## ✨ 功能特性

| 能力 | 说明 |
|---|---|
| 🧠 **模型自动发现** | 扫描模型目录（默认 `G:\models`），新增 `.gguf` 文件自动生成启动配置，2 秒内出现在列表 |
| 🔧 **失效路径自动修复** | 模型文件被移动/整理后，自动在新位置修正启动脚本的 `--model` 路径 |
| ▶️ **一键启停/切换** | 统一端口 11434（OpenAI 兼容 API），启动 / 停止 / 重启 / 切换模型，全部图形化 |
| ⚙️ **参数可视化配置** | ctx-size、KV 缓存量化（K/V）、Flash Attention、MTP 投机解码、GPU 层数、并行槽位、温度 / top-p / repeat-penalty / seed 等采样参数，按模型分别记忆 |
| 📊 **实时监控** | CPU / 内存 / 显存占用（含 GPU 利用率）、实时输出速度（tok/s）、Token 消耗统计 |
| 📜 **实时日志窗** | 自动跟随运行中的模型，滚动查看 llama-server 输出 |
| 🖥️ **桌面 GUI** | pywebview 原生窗口（WebView2），可打包成单文件 EXE，双击即用 |

## 📸 界面预览

> 界面截图占位，详见项目实际运行效果。

## 🚀 快速开始

### 环境要求

- Windows 10 / 11（启动脚本为 `.bat`）
- Python 3.10+
- 本地可用的 llama.cpp（含 `llama-server.exe`）与 GGUF 模型文件
- GUI 模式可选安装 [pywebview](https://pywebview.flowrl.com/)

### 目录结构

```
llama-manager/
├── server.py            # HTTP 后端（纯标准库，负责模型启停/状态/监控/日志）
├── launcher.py          # GUI 入口（pywebview 原生窗口，WebView2 缺失时回退浏览器）
├── index.html           # 前端界面（单页）
├── llama-manager.bat    # 一键启动（浏览器模式）
└── scripts/             # llama.cpp 的 run-*.bat 启动脚本（每个模型一份）
```

### 配置

默认路径适配 `G:\llama.cpp` 与 `G:\models`，可通过环境变量覆盖（方便部署到其他机器）：

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `LLAMA_CPP_DIR` | `G:\llama.cpp` | llama.cpp 根目录（含 `llama-server.exe` 与 `scripts/`） |
| `LLAMA_MODELS_DIR` | `G:\models` | 模型存放根目录（自动扫描其中的 `*.gguf`，含 `gguf/` 子目录） |

**配置文件方式（推荐，免设环境变量）**：在 exe/脚本同目录放 `llama-manager.json`（参考 `llama-manager.json.example`）：

```json
{
  "llama_dir": "D:\\llama.cpp",
  "models_dir": "D:\\models",
  "port_api": 17890
}
```

配置优先级：环境变量 > 配置文件 > 默认值。跨电脑部署时，把 EXE 拷到目标机器，改这份 json 即可，无需重新打包。

### 运行

```bash
# 浏览器模式（无需任何第三方依赖）
python server.py
# 打开 http://127.0.0.1:17890

# 桌面 GUI 模式（需要 pywebview）
pip install pywebview
python launcher.py

# 或直接双击 llama-manager.bat（自动启动后端并打开浏览器）
```

### 打包为独立 EXE

```bash
pip install pyinstaller pywebview
pyinstaller --onefile --noconsole --name llama-manager --add-data "index.html;." launcher.py
# 产物：dist/llama-manager.exe，双击即用（WebView2 缺失时自动回退浏览器）
```

## 🔌 HTTP API

| 接口 | 方法 | 说明 |
|---|---|---|
| `/` | GET | 前端页面 |
| `/api/models` | GET | 模型列表（自动发现/修复路径） |
| `/api/status` | GET | 运行状态：stopped / loading / running + 速度 + Token |
| `/api/sys` | GET | CPU / 内存 / 显存占用 |
| `/api/log?script=run-xxx.bat` | GET | 模型运行日志（尾部） |
| `/api/scan` | GET | 手动扫描模型目录 |
| `/api/start` | POST | 启动 `{script, options}` |
| `/api/stop` | POST | 停止当前模型 |
| `/api/restart` | POST | 重启 `{script, options}` |
| `/api/switch` | POST | 切换 `{script, options}` |

`options` 支持：`ctx`、`cache_k`、`cache_v`、`flash_attn`、`mtp`、`mtp_n`、`gpu_layers`、`parallel`、`threads`、`temp`、`top_p`、`repeat_penalty`、`seed`、`reasoning`。

## 🧩 使用技巧

- **添加新模型**：把 `.gguf` 文件丢进模型目录即可，管理台自动识别、一键启动
- **MTP 投机解码**：仅 Qwen3 系列（GGUF 内嵌 MTP 头）支持，可提速 15-20%
- **reasoning 开关**：管理台开关 = 服务端 `--reasoning`，请与客户端（如 WorkBuddy 思考模式）保持一致，同开同关

## 📄 许可证

本项目仅供个人学习与本地工具使用。
