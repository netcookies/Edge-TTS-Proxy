## Edge-TTS-Proxy 插件

### 1. 插件介绍

`Edge-TTS-Proxy` 插件将 Microsoft Edge TTS（文本到语音）服务集成到 Home Assistant 中。通过代理服务，该插件利用 [read-aloud API](https://github.com/yy4382/read-aloud) 实现语音合成功能，为 Home Assistant 提供基于 Microsoft Edge 的文本到语音支持。

### 2. 插件功能

- 使用 Microsoft Edge 提供的 TTS 引擎进行语音合成。
- 支持通过 Home Assistant 发送语音通知。
- 提供缓存功能，提升语音播放效率。
- 支持两种使用方式：通过语音助手选择或通过 `tts.speak` 调用指定实体。
- 后端通过 [read-aloud API](https://github.com/yy4382/read-aloud) 调用 Microsoft Edge TTS 服务。

### 3. 安装与配置

#### 安装步骤

1. 通过 HACS（Home Assistant Community Store）进行安装：
   - 在 Home Assistant 中打开 HACS。
   - 搜索 `Edge TTS Proxy` 插件并点击安装。
   - 安装完成后，重新启动 Home Assistant。

#### 配置

安装完成后，可以通过 Home Assistant 的 UI 配置流程（`config_flow`）来设置插件：

1. 在 Home Assistant UI 中，转到 **设置** > **集成**。
2. 点击右下角的 **+ 添加集成**。
3. 搜索 `Edge TTS Proxy` 并选择它。
4. 按照向导完成配置

完成配置后，插件会自动进行设置并准备就绪。

### 4. 使用方法

插件提供两种使用方式：

#### 方式一：通过语音助手配置

1. 在 Home Assistant 的 **设置** > **语音助手** 中选择您配置的语音助手。
2. 在语音助手的配置中，选择使用 `Edge TTS Proxy` 作为语音引擎。
3. 配置完成后，语音助手会使用 Microsoft Edge TTS 进行语音合成并播放。

#### 方式二：通过 `tts.speak` 服务调用

您还可以通过 `tts.speak` 服务来指定具体的 TTS 实体（如 `tts.edge_tts_proxy_entity`），例如：

```yaml
service: tts.speak
data:
  entity_id: tts.edge_tts_proxy_entity  # 选择您的 TTS 实体
  message: "Hello, this is a test of Edge TTS Proxy!"
```

通过这种方式，您可以在任何自动化或脚本中使用 Edge TTS。

### 5. 后端技术说明

`Edge-TTS-Proxy` 插件的语音合成是通过调用 [read-aloud API](https://github.com/yy4382/read-aloud) 实现的，该 API 提供了对 Microsoft Edge TTS 服务的代理接口。`read-aloud` 是一个基于 Node.js 的项目，通过 Microsoft Edge 和 Azure 的语音服务进行文本到语音合成。

- **read-aloud API**：该 API 提供了通过 HTTP 请求将文本转换为语音文件的功能，支持多种语言和语音模型。
- 插件通过此 API 调用来处理文本转语音请求，返回的语音文件可以缓存并在 Home Assistant 中播放。

### 6. 支持的语言与语音

插件支持通过 Microsoft Edge TTS API 提供的多种语言和语音模型。您可以在配置过程中选择所需的语言和语音。例如：

- **中文（简体）**：`zh-CN`

更多语言和语音模型的选择，请参考 [Microsoft Edge TTS API 文档](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/voices).

### 7. 更新与维护

- 插件支持通过 HACS 自动更新，确保您获得最新的功能和修复。
- 定期检查 HACS 中的插件更新，保持插件为最新版本。

### 8. 问题排查

- **无法播放语音**：检查插件配置中的语言和语音设置，确保您选择了有效的语音模型。
- **缓存问题**：如果启用了缓存并且遇到问题，尝试清空缓存目录并重新启动 Home Assistant。
- **API 配置错误**：确保您的网络环境可以访问 Microsoft Edge TTS API 和 [read-aloud API](https://github.com/yy4382/read-aloud)。

### 9. 贡献与开发

如果您希望为插件贡献代码，请按照以下步骤：

1. Fork 本仓库。
2. 创建新分支：`git checkout -b feature/your-feature`。
3. 提交更改：`git commit -m 'Add new feature'`。
4. 推送至 GitHub：`git push origin feature/your-feature`。
5. 提交 Pull Request。

### 10. 许可证

本插件采用 [MIT 许可证](https://opensource.org/licenses/MIT)，可以自由修改和分发。

---

## 代码分析

- **核心功能**：插件通过代理服务与 [read-aloud API](https://github.com/yy4382/read-aloud) 交互，调用 Microsoft Edge TTS 服务进行语音合成。插件支持缓存机制以提高多次调用时的效率。
