# 配置选项

CalculusCalculator 的配置分为两类：**界面设置**（语言 / 主题，存于配置文件）与**工程存档**（当前工作现场，存于项目文件）。

## 界面设置（设置选项卡）

通过菜单栏"功能 → 设置"打开设置页面，可配置：

- **界面语言**：中文 / English。切换后立即生效，并持久化。
- **界面主题**：浅色 / 深色。切换后立即生效，并持久化。

这两项设置在应用关闭后依然保留，下次启动自动恢复。

### 配置文件位置

界面设置以 JSON 形式保存，路径由 Qt 标准配置目录决定：

```
<AppConfigLocation>/CalculusCalculator/CalculusCalculator/settings.json
```

典型位置：

- Windows：`C:/Users/<用户名>/AppData/Local/CalculusCalculator/CalculusCalculator/settings.json`
- Linux：`~/.config/CalculusCalculator/CalculusCalculator/settings.json`
- macOS：`~/Library/Application Support/CalculusCalculator/CalculusCalculator/settings.json`

文件结构示例：

```json
{
  "language": "zh_CN",
  "theme": "dark"
}
```

!!! tip
    早期版本（未设置应用名时）可能将设置写入 `AppData/Local/settings.json` 或
    `AppData/Local/python/settings.json`。新版本在首次启动时会自动兼容并迁移这些旧路径，
    因此你此前保存的浅色 / 深色偏好不会丢失。

## 工程存档 / 读档

通过菜单栏"文件 → 保存 / 另存为 / 打开"将当前工作现场保存为项目文件（JSON），内容包括：

- 所有标签页的输入内容
- 自定义函数列表（`fs` 字典）
- 标签页序号
- 几何对象（点 / 直线 / 圆 / 三角形 / 多边形等）
- 保存时的语言与主题

打开项目文件时会自动恢复上述现场，并应用其中保存的主题与语言设置。

!!! note
    项目文件中的主题 / 语言仅在"打开该项目"时生效；全局界面设置仍以 `settings.json` 为准。
