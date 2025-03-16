# UML-MCP-Server

UML-MCP-Server是一个基于MCP (Model Context Protocol) 的UML图生成工具，可以帮助用户通过自然语言描述或直接编写PlantUML代码来生成各种类型的UML图。

## 功能特点

- 支持多种UML图类型：类图、序列图、活动图、用例图、状态图、组件图、部署图、对象图
- 可以通过自然语言描述生成UML图
- 可以直接使用PlantUML代码生成UML图
- 返回PlantUML代码和可访问的URL链接，方便分享和查看
- 同时将生成的UML图保存到本地，提供本地文件路径
- 支持自定义保存路径，可以指定UML图片的输出目录
- 作为MCP服务器，可以与支持MCP的客户端（如Claude）集成
- 完善的日志记录系统，记录服务器运行状态和操作日志

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/UML-MCP-Server.git
cd UML-MCP-Server
```

2. 创建并激活虚拟环境：

```bash
python -m venv uml-mcp-venv
source uml-mcp-venv/bin/activate  # Linux/Mac
# 或
uml-mcp-venv\Scripts\activate  # Windows
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 作为Python库使用

```python
from fix_plantuml import generate_uml

# 创建UML代码
uml_code = """
@startuml
title 简单类图

class User {
  -String name
  -String email
  +login()
  +logout()
}

class Order {
  -int id
  -Date date
  +process()
}

User "1" -- "many" Order: places
@enduml
"""

# 生成UML图的URL、代码和本地路径
result = generate_uml(uml_code)

# 输出结果
print("PlantUML代码:")
print(result["code"])
print("\nPlantUML URL:")
print(result["url"])
print("\n本地文件路径:")
print(result["local_path"])
```

### 作为MCP服务器使用

1. 启动MCP服务器：

```bash
python uml_mcp_server.py
```

2. 在支持MCP的客户端（如Claude）中配置并连接到服务器。

3. 使用以下工具函数：

- `generate_uml(diagram_type, description, output_dir="output")`: 根据类型和描述生成UML图，可指定输出目录
- `generate_class_diagram(description, output_dir="output")`: 生成类图，可指定输出目录
- `generate_sequence_diagram(description, output_dir="output")`: 生成序列图，可指定输出目录
- `generate_activity_diagram(description, output_dir="output")`: 生成活动图，可指定输出目录
- `generate_usecase_diagram(description, output_dir="output")`: 生成用例图，可指定输出目录
- `generate_state_diagram(description, output_dir="output")`: 生成状态图，可指定输出目录
- `generate_component_diagram(description, output_dir="output")`: 生成组件图，可指定输出目录
- `generate_deployment_diagram(description, output_dir="output")`: 生成部署图，可指定输出目录
- `generate_object_diagram(description, output_dir="output")`: 生成对象图，可指定输出目录
- `generate_uml_from_code(code, output_dir="output")`: 从PlantUML代码生成UML图，可指定输出目录

### 自定义保存路径

所有UML生成工具函数都支持通过`output_dir`参数指定输出目录：

```python
# 示例：生成类图并保存到自定义目录
result_json = generate_class_diagram("用户和订单系统", output_dir="/path/to/custom/directory")
result = json.loads(result_json)
print(f"UML图保存到: {result['local_path']}")

# 示例：从代码生成UML图并保存到自定义目录
uml_code = """
@startuml
class User {}
class Order {}
User -- Order
@enduml
"""
result_json = generate_uml_from_code(uml_code, output_dir="/path/to/custom/directory")
result = json.loads(result_json)
print(f"UML图保存到: {result['local_path']}")
```

在MCP客户端中，你可以在调用工具函数时指定`output_dir`参数：

```
请使用UML工具生成一个类图，描述用户和订单系统，并保存到/path/to/custom/directory目录
```

### 日志系统

UML-MCP-Server内置了完善的日志记录系统，可以帮助你监控服务器运行状态和排查问题。

#### 日志配置

- 日志文件保存在项目根目录下的`logs`文件夹中
- 日志文件命名格式为`uml_mcp_server_YYYY-MM-DD.log`，每天生成一个新的日志文件
- 同时在控制台和日志文件中记录日志
- 日志级别默认为INFO，记录服务器的主要操作和状态变化

#### 日志内容

日志记录了以下内容：

- 服务器启动和关闭
- 工具函数的调用和参数
- UML图生成过程
- HTTP请求和响应
- 错误和异常信息

#### 查看日志

你可以通过以下方式查看日志：

1. 在控制台中查看实时日志输出
2. 打开日志文件查看历史日志记录：

```bash
# 查看最新的日志文件
cat logs/uml_mcp_server_$(date +%Y-%m-%d).log

# 或者使用tail命令实时查看日志更新
tail -f logs/uml_mcp_server_$(date +%Y-%m-%d).log
```

#### 自定义日志配置

如果需要自定义日志配置，可以修改`uml_mcp_server.py`文件中的`setup_logging`函数。例如，你可以：

- 修改日志级别（DEBUG、INFO、WARNING、ERROR、CRITICAL）
- 更改日志文件的保存路径
- 自定义日志格式
- 添加日志轮转功能

### 在Cursor中配置MCP

Cursor支持MCP（Model Context Protocol）服务器，可以让你直接在Cursor中使用UML-MCP-Server生成UML图。配置步骤如下：

1. 确保已安装最新版本的Cursor IDE（支持MCP功能的版本）。

2. 打开Cursor的配置文件：
   - 在macOS上：`~/Library/Application Support/Cursor/config.json`
   - 在Windows上：`%APPDATA%\Cursor\config.json`
   - 在Linux上：`~/.config/Cursor/config.json`

3. 在配置文件中添加或修改`mcpServers`部分：

```json
{
  "mcpServers": {
    "UML-MCP-Server": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/edy/vs-code/UML-MCP-Server",
        "run",
        "uml_mcp_server.py"
      ],
      "env": {
        "OUTPUT_DIR": "/Users/edy/vs-code/data-conversion/uml-output"
      }
    }
  }
}
```

配置说明：
- `UML-MCP-Server`：MCP服务器的名称，可以根据需要修改
- `command`：使用 `uv` 作为运行命令
- `args`：
  - `--directory`：指定项目目录的绝对路径
  - `run`：运行命令
  - `uml_mcp_server.py`：主程序文件
- `env`：环境变量配置
  - `OUTPUT_DIR`：指定UML图片的输出目录，这里设置为 `/Users/edy/vs-code/data-conversion/uml-output`

请根据你的实际情况修改以下路径：
- 将 `/Users/edy/vs-code/UML-MCP-Server` 替换为你的UML-MCP-Server项目的实际路径
- 将 `/Users/edy/vs-code/data-conversion/uml-output` 替换为你想要保存UML图片的目录路径

4. 保存配置文件并重启Cursor。

5. 在Cursor中使用UML-MCP-Server：
   - 打开一个新的聊天窗口
   - 在聊天界面底部的工具栏中，你会看到"UML-MCP-Server"工具图标
   - 点击该图标，会出现UML工具的选项菜单
   - 选择你需要的UML图类型（如"生成类图"、"生成序列图"等）

### 在Cursor中使用UML工具

在Cursor中，你可以通过以下方式使用UML工具：

#### 方式一：通过工具栏使用

1. 在聊天界面底部的工具栏中点击"UML"图标
2. 从弹出的菜单中选择需要的UML图类型，例如"生成类图"
3. 在弹出的输入框中输入你的描述，例如"用户和订单系统"
4. 点击"提交"按钮

#### 方式二：通过聊天直接使用

你可以在聊天中直接请求Claude生成UML图，例如：

```
请使用UML工具生成一个类图，描述用户和订单系统
```

或者：

```
请使用UML工具从以下代码生成UML图：

@startuml
title 简单类图

class User {
  -String name
  -String email
  +login()
  +logout()
}

class Order {
  -int id
  -Date date
  +process()
}

User "1" -- "many" Order: places
@enduml
```

### UML工具返回的结果

无论通过哪种方式使用UML工具，Cursor都会调用UML-MCP-Server并返回以下内容：

1. **PlantUML代码** - 你可以复制这段代码在其他PlantUML工具中使用
2. **PlantUML URL** - 你可以在浏览器中打开这个URL查看生成的UML图
3. **本地文件路径** - 生成的UML图片保存在本地的这个路径下

例如：

```
已生成类图：

PlantUML代码：
@startuml
title 用户和订单系统
class User {
  -String name
  -String email
  +login()
  +logout()
}
class Order {
  -int id
  -Date date
  +process()
}
User "1" -- "many" Order: places
@enduml

PlantUML URL：
http://www.plantuml.com/plantuml/png/~1UDgCqB5Bn0G1k1zYWM_EfPYQYY0Qd9oQc9oQaPcKYYcKc9gMYaiKc9gK...

本地文件路径：
/Users/username/projects/UML-MCP-Server/output/class_diagram_12345.png
```

你可以通过以下方式查看生成的UML图：
- 点击返回的URL链接在浏览器中查看
- 在文件浏览器中打开本地文件路径查看保存的图片
- 在Cursor中，你可以使用Markdown语法在聊天窗口中直接显示图片：

```markdown
![类图](file:///Users/username/projects/UML-MCP-Server/output/class_diagram_12345.png)
```

### 高级配置选项

如果你需要更多控制，可以参考以下高级配置示例：

```json
{
  "mcpServers": {
    "uml": {
      "command": "python",
      "args": [
        "uml_mcp_server.py"
      ],
      "cwd": "/绝对路径/到/UML-MCP-Server",
      "env": {
        "PYTHONPATH": "/绝对路径/到/UML-MCP-Server",
        "OUTPUT_DIR": "/自定义输出目录",
        "LOG_LEVEL": "DEBUG"  // 设置日志级别
      }
    }
  }
}
```

## 故障排除

如果你在使用UML-MCP-Server时遇到问题，可以尝试以下步骤：

1. **检查日志文件**：查看`logs`目录下的日志文件，了解错误详情
2. **验证依赖安装**：确保所有依赖已正确安装
3. **检查网络连接**：确保可以访问PlantUML服务器（www.plantuml.com）
4. **检查输出目录权限**：确保程序有权限写入`output`目录

常见问题及解决方案：

- **无法生成UML图**：检查日志中的错误信息，可能是网络问题或PlantUML服务器暂时不可用
- **图片未保存到本地**：检查`output`目录是否存在且有写入权限
- **MCP服务器无法启动**：检查日志文件，确保没有端口冲突或其他程序错误

## 贡献

欢迎贡献代码、报告问题或提出改进建议！请通过GitHub Issues或Pull Requests参与项目开发。

## 许可证

本项目采用MIT许可证。详见LICENSE文件。 