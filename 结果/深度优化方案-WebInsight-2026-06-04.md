# 🚀 WebInsight 深度优化方案

**报告日期：2026年06月04日**
**分析师：GitHub Copilot（世界顶级网站分析师兼资深全栈工程师，精通 AI/MCP/Agent 开发）**

---

## 一句话总览

WebInsight 是一个结构清晰、功能完整的 AI 网站分析工具，但当前版本存在**抓取深度不足、AI 上下文质量低、无 Agent 自主推理能力、无 MCP 集成、缺乏历史管理**等核心缺陷，通过引入 **GitHub Skills + MCP 协议 + Multi-Agent 架构**，可将产品能级从"单次分析工具"升级为"持续智能竞品情报平台"。

---

## 🔍 一、现有方案问题深度剖析

### 1.1 输出质量问题（从分析结果文件直接观察）

从 `analysis-diamondrosesanctuary.com-2026-06-04.md` 可以看到几个关键问题：

| 问题 | 具体表现 | 影响 |
|:---|:---|:---|
| **推断 > 实测** | "从脚本命名推断首屏有 GSAP 动画"，运行时数据为空 | AI 大量编造、猜测，输出可信度低 |
| **模块数据缺失** | `page_modules: []`，SPA 未被 Playwright 正确渲染 | 最核心的模块级分析章节完全依赖推断 |
| **网络请求数据缺失** | `network_summary` 为空 | 无法分析 API 调用、第三方依赖 |
| **运行时动画数据缺失** | `runtime_animation: {}` | GSAP 版本、ScrollTrigger 实例数均为空 |
| **混淆性结论** | 同一网站被判定为"Webflow + Next.js 混合架构"，逻辑矛盾 | 误导使用者 |
| **报告开头格式异常** | 文件第一行是"世界顶级的网站分析师兼资深全栈工程师"（system prompt 泄漏） | 下载的报告内容不规范 |

### 1.2 抓取层缺陷

```
当前流程：requests 静态抓取 → is_spa_page() 判断 → Playwright 渲染（如果是 SPA）
```

**问题1：SPA 判断逻辑过于简单**
```python
# 现有逻辑：仅凭 root/app 挂载点 + 低文本量
has_spa_root = bool(RE_SPA_ROOT.search(html))
has_low_text = text_len < 500 and script_count > 0
```
Webflow 等平台生成的页面 `text_len` > 500 但仍需 JS 渲染动画数据，会被误判为"非 SPA"，
导致跳过 Playwright，无法获取 runtime_animation 和 page_modules。

**问题2：Playwright 等待策略粗糙**
```python
await page.goto(url, wait_until="networkidle", timeout=30000)
await asyncio.sleep(0.8)  # 仅等待 0.8 秒
```
0.8 秒远不够 GSAP 动画初始化完成，导致 runtime_animation 数据为空。

**问题3：始终单线程串行处理**
抓取 → AI 分析 串行执行，没有并发，浪费时间。

**问题4：无截图传给 AI**
代码虽然截图了但在发给 AI 之前就删掉了：
```python
website_data.pop("screenshot_base64", None)  # 直接丢弃！
```
DeepSeek 支持视觉模型（deepseek-vl2），截图本应作为关键输入。

### 1.3 AI 层缺陷

**问题1：Prompt 过于宏大，导致 AI 注意力分散**
当前 Prompt 一次性要求分析 8+ 个维度，超过 2000 字的 system prompt，导致：
- AI 无法专注于单个维度
- 对空数据倾向于"编造合理推断"而非"如实说明缺失"
- token 浪费严重

**问题2：无 Agent 推理链，缺乏验证步骤**
当前是单次 LLM 调用，没有：
- 自我反思（self-reflection）步骤
- 数据验证步骤（声明的技术 vs 实际检测到的技术一致性检查）
- 多轮推理（先分析技术栈 → 再分析设计 → 最后综合评分）

**问题3：API Key 明文存储在 localStorage**
```javascript
localStorage.setItem('deepseek_api_key', apiKey);
```
存在 XSS 风险，API Key 可被恶意脚本窃取。

**问题4：system prompt 泄漏到输出**
输出文件第一行是 system prompt 内容，说明 AI 的角色设定被当作正文输出了。

### 1.4 工程层缺陷

| 问题 | 现状 | 风险 |
|:---|:---|:---|
| **无任务队列** | 每次请求直接执行，无并发控制 | 多用户同时使用会崩溃 |
| **无结果持久化** | 分析结果只在前端内存中 | 刷新即丢失 |
| **无历史记录** | 无法查看历史分析 | 无法趋势对比 |
| **无 robots.txt 遵守** | 强制抓取所有网站 | 法律风险 |
| **无速率限制** | API 调用无节流 | DeepSeek 账单风险 |
| **API Key 暴露在注释中** | `index.html` 第 669 行有 `<!--sk-f359f0...-->` | 严重安全漏洞 |

---

## 🏗️ 二、整体优化架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                     WebInsight v2.0                         │
├─────────────────────────────────────────────────────────────┤
│  前端层  │  Vue 3 SPA  │  历史记录  │  对比分析  │  导出    │
├──────────┼────────────────────────────────────────────────── │
│  API层   │  FastAPI  │  任务队列(Celery)  │  WebSocket      │
├──────────┼────────────────────────────────────────────────── │
│  Agent层 │  Orchestrator Agent                               │
│          │  ├── CrawlerAgent (Playwright深度抓取)            │
│          │  ├── TechAnalystAgent (技术栈专项分析)            │
│          │  ├── UXAnalystAgent (设计/动画专项分析)           │
│          │  ├── SEOAgent (SEO专项分析)                       │
│          │  ├── SecurityAgent (安全专项分析)                 │
│          │  └── ReflectionAgent (自我反思/验证)              │
├──────────┼────────────────────────────────────────────────── │
│  MCP层   │  GitHub MCP  │  Lighthouse MCP  │  Puppeteer MCP │
├──────────┼────────────────────────────────────────────────── │
│  数据层  │  SQLite/PostgreSQL  │  Redis Cache  │  文件存储   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 三、Multi-Agent 架构优化（核心升级）

### 3.1 Orchestrator Agent（指挥中枢）

**设计思路**：将当前的单次 LLM 调用，改为多 Agent 协作流水线。

```python
# app_v2.py - Agent 架构核心

class AnalysisOrchestrator:
    """
    主控 Agent：协调各专项 Agent，整合结果，执行反思验证
    """
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.model = model
    
    async def run(self, website_data: dict, stream_callback=None) -> str:
        """
        执行 Agent 流水线：
        1. CrawlerAgent 深度抓取（已完成，传入 website_data）
        2. 并发执行：TechAgent + UXAgent + SEOAgent + SecurityAgent
        3. ReflectionAgent 验证各 Agent 结论的一致性
        4. 合成最终报告
        """
        results = {}
        
        # 步骤1：并发执行专项分析
        tasks = {
            "tech": self._run_tech_agent(website_data),
            "ux": self._run_ux_agent(website_data),
            "seo": self._run_seo_agent(website_data),
            "security": self._run_security_agent(website_data),
            "content": self._run_content_agent(website_data),
        }
        
        if stream_callback:
            await stream_callback("status", "🤖 各专项 Agent 并发分析中...")
        
        # 并发执行所有专项 Agent
        agent_results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        for key, result in zip(tasks.keys(), agent_results):
            results[key] = result if not isinstance(result, Exception) else f"分析失败: {result}"
        
        # 步骤2：ReflectionAgent 验证
        if stream_callback:
            await stream_callback("status", "🔍 ReflectionAgent 验证结论一致性...")
        reflection = await self._run_reflection_agent(website_data, results)
        
        # 步骤3：流式生成最终综合报告
        if stream_callback:
            await stream_callback("status", "✍️ 正在生成综合报告...")
        report = await self._synthesize_report(website_data, results, reflection, stream_callback)
        
        return report
    
    async def _run_tech_agent(self, data: dict) -> str:
        """技术栈专项 Agent - 专注且精准"""
        prompt = f"""你是技术架构专家。仅分析以下数据中的技术实现，不要分析其他方面。

检测到的技术栈：{json.dumps(data.get('tech_stack', {}), ensure_ascii=False)}
JS 脚本：{data.get('scripts', [])[:15]}
CSS 样式：{data.get('styles', [])[:10]}
响应头：{data.get('response_headers_summary', '')}
运行时动画数据：{json.dumps(data.get('runtime_animation', {}), ensure_ascii=False)}

要求：
1. 精确识别前端框架、构建工具、CSS方案、动画库
2. 明确区分"检测到"vs"推断"，数据缺失时明确说明"无数据"
3. 对技术选型的合理性给出专业评价
4. 输出 JSON 格式，结构：{{"frameworks":[],"build_tools":[],"animation":{},"assessment":"","confidence":0.0-1.0}}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  # 低温度，确保精确性
            max_tokens=2000,
        )
        return response.choices[0].message.content
    
    async def _run_reflection_agent(self, data: dict, results: dict) -> str:
        """
        ReflectionAgent：检查各 Agent 结论的矛盾点
        例如：TechAgent 说"Next.js"但 SEOAgent 说"无 SSR"，需要协调
        """
        prompt = f"""你是一个批判性审查员。检查以下各专项 Agent 的分析结论是否存在矛盾或不一致：

技术分析：{results.get('tech', '')}
UX分析：{results.get('ux', '')}
SEO分析：{results.get('seo', '')}

请找出：
1. 各 Agent 之间的矛盾结论
2. 与原始数据不符的推断
3. 置信度较低需要标注"推断"的结论
输出 JSON：{{"conflicts":[],"low_confidence_claims":[],"corrections":[]}}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1000,
        )
        return response.choices[0].message.content
```

### 3.2 CrawlerAgent 深度升级

**核心问题修复：始终使用 Playwright，并等待足够时间**

```python
# crawler_v2.py

class CrawlerAgent:
    """
    深度抓取 Agent：
    1. 始终使用 Playwright（不依赖简单的 SPA 检测）
    2. 等待 GSAP/动画库初始化完成
    3. 分阶段截图（首屏 + 滚动后）
    4. 主动执行页面交互（滚动触发 ScrollTrigger）
    """
    
    ANIMATION_INIT_WAIT = 2.5  # 等待动画库初始化（秒）
    SCROLL_STEPS = 5           # 分步滚动次数（触发 ScrollTrigger）
    
    async def crawl(self, url: str) -> dict:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1440, "height": 900},
                user_agent=USER_AGENT,
            )
            page = await context.new_page()
            
            # 注入 MutationObserver 监听动画初始化
            await page.add_init_script("""
                window.__animationReady = false;
                window.__gsapReady = false;
                const origDefineProperty = Object.defineProperty;
                Object.defineProperty(window, 'gsap', {
                    set(v) { window.__gsapReady = true; this._gsap = v; },
                    get() { return this._gsap; }
                });
            """)
            
            await page.goto(url, wait_until="networkidle", timeout=45000)
            
            # 等待动画库初始化（不是固定等待，而是轮询）
            await self._wait_for_animation_init(page)
            
            # 分步滚动触发 ScrollTrigger 动画
            screenshots = await self._scroll_and_screenshot(page)
            
            # 提取完整数据
            data = await self._extract_all(page)
            data["screenshots"] = screenshots  # 保留用于视觉分析
            
            return data
    
    async def _wait_for_animation_init(self, page, timeout=5000):
        """等待 GSAP 等动画库初始化完成"""
        try:
            await page.wait_for_function(
                "() => typeof gsap !== 'undefined' || document.readyState === 'complete'",
                timeout=timeout
            )
            # 额外等待动画库注册插件
            await asyncio.sleep(self.ANIMATION_INIT_WAIT)
        except Exception:
            await asyncio.sleep(1.5)
    
    async def _scroll_and_screenshot(self, page) -> list:
        """分步滚动页面，触发 ScrollTrigger，分段截图"""
        screenshots = []
        total_height = await page.evaluate("document.body.scrollHeight")
        
        # 首屏截图
        data = await page.screenshot(type="jpeg", quality=70, clip={"x":0,"y":0,"width":1440,"height":900})
        screenshots.append({"position": "top", "data": base64.b64encode(data).decode()})
        
        # 分步滚动
        for i in range(1, self.SCROLL_STEPS + 1):
            scroll_y = int(total_height * i / self.SCROLL_STEPS)
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            await asyncio.sleep(0.5)  # 等待 ScrollTrigger 动画触发
        
        # 滚动到底部后截图
        data = await page.screenshot(type="jpeg", quality=70, full_page=True)
        screenshots.append({"position": "full", "data": base64.b64encode(data).decode()})
        
        return screenshots
```

---

## 🔌 四、MCP（Model Context Protocol）集成

### 4.1 为什么需要 MCP？

当前工具是**封闭式单机工具**，通过 MCP 可以：
1. 让 Claude Desktop / Cursor / VS Code Copilot 直接调用本工具作为 MCP Server
2. 连接外部数据源（GitHub 仓库、Lighthouse API、PageSpeed API）
3. 实现工具链的标准化互操作

### 4.2 MCP Server 实现

```python
# mcp_server.py - 将 WebInsight 暴露为 MCP Server

"""
安装: pip install mcp
启动: python mcp_server.py
配置到 Claude Desktop: ~/.claude/claude_desktop_config.json
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

app_mcp = Server("webinsight")

@app_mcp.list_tools()
async def list_tools():
    return [
        Tool(
            name="analyze_website",
            description="深度分析网站技术栈、设计、SEO、动画和性能",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "要分析的网站 URL"},
                    "focus": {
                        "type": "string", 
                        "enum": ["tech", "seo", "animation", "performance", "full"],
                        "description": "分析重点，默认 full"
                    },
                    "depth": {
                        "type": "string",
                        "enum": ["quick", "standard", "deep"],
                        "description": "分析深度：quick(仅静态), standard(Playwright), deep(含交互模拟)"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="compare_websites",
            description="对比分析两个竞品网站",
            inputSchema={
                "type": "object",
                "properties": {
                    "url_a": {"type": "string"},
                    "url_b": {"type": "string"},
                    "dimensions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "对比维度：tech/design/seo/performance"
                    }
                },
                "required": ["url_a", "url_b"]
            }
        ),
        Tool(
            name="get_analysis_history",
            description="获取历史分析记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "过滤特定域名"},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        ),
        Tool(
            name="tech_stack_lookup",
            description="快速检测网站技术栈（无需 AI 分析）",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        )
    ]

@app_mcp.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "analyze_website":
        url = arguments["url"]
        focus = arguments.get("focus", "full")
        depth = arguments.get("depth", "standard")
        
        # 调用内部分析引擎
        from app import fetch_website_playwright, fetch_website_requests
        if depth in ("standard", "deep"):
            data = await fetch_website_playwright(url)
        else:
            data = await fetch_website_requests(url)
        
        # 返回结构化结果（不调用 AI，让调用方的 LLM 自行分析）
        return [TextContent(
            type="text",
            text=f"网站技术数据：\n{json.dumps(data, ensure_ascii=False, indent=2)[:8000]}"
        )]
    
    elif name == "compare_websites":
        url_a, url_b = arguments["url_a"], arguments["url_b"]
        data_a, data_b = await asyncio.gather(
            fetch_website_requests(url_a),
            fetch_website_requests(url_b)
        )
        comparison = {
            "site_a": {"url": url_a, "tech": data_a.get("tech_stack"), "stats": data_a.get("page_stats")},
            "site_b": {"url": url_b, "tech": data_b.get("tech_stack"), "stats": data_b.get("page_stats")},
        }
        return [TextContent(type="text", text=json.dumps(comparison, ensure_ascii=False, indent=2))]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app_mcp.run(read_stream, write_stream, app_mcp.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

**Claude Desktop 配置（`~/.claude/claude_desktop_config.json`）：**
```json
{
  "mcpServers": {
    "webinsight": {
      "command": "python",
      "args": ["D:/work20240226/rcs-20250311/website-fangan-20260604/pan-website-fangan/mcp_server.py"],
      "env": {}
    }
  }
}
```

配置后，在 Claude Desktop 中可以直接说：
> "帮我分析 diamondrosesanctuary.com 的技术栈，并和 sixsenses.com 做对比"

Claude 会自动调用 WebInsight MCP Server 抓取数据，然后自行分析。

---

## 🐙 五、GitHub Skills 集成

### 5.1 GitHub Actions 自动化分析流水线

```yaml
# .github/workflows/competitor-monitor.yml
name: 竞品网站定期监控

on:
  schedule:
    - cron: '0 8 * * 1'  # 每周一早8点
  workflow_dispatch:
    inputs:
      url:
        description: '要分析的网站 URL'
        required: true

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: 安装 Python 依赖
        run: |
          pip install -r pan-website-fangan/requirements.txt
          playwright install chromium
      
      - name: 运行深度分析
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: |
          python pan-website-fangan/cli_analyze.py \
            --url "${{ github.event.inputs.url || 'https://diamondrosesanctuary.com' }}" \
            --output "结果/$(date +%Y-%m-%d)-analysis.md"
      
      - name: 提交分析结果
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "🔍 自动分析报告 $(date +%Y-%m-%d)"
          file_pattern: '结果/*.md'
      
      - name: 创建 Issue（如发现重大变化）
        if: steps.analyze.outputs.has_changes == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '🚨 竞品网站重大变化检测',
              body: '检测到 ${{ github.event.inputs.url }} 技术栈或内容发生重大变化，请查看最新分析报告。',
              labels: ['competitor-alert']
            })
```

### 5.2 GitHub Copilot 扩展（VS Code）

```typescript
// copilot-extension/src/extension.ts
// 将 WebInsight 集成为 VS Code Copilot Chat 参与者

import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    const handler: vscode.ChatRequestHandler = async (request, chatContext, stream, token) => {
        if (request.command === 'analyze') {
            const url = request.prompt.trim();
            stream.progress('正在分析网站...');
            
            // 调用本地 WebInsight API
            const response = await fetch('http://localhost:8765/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    url, 
                    api_key: process.env.DEEPSEEK_API_KEY,
                    model: 'deepseek-chat' 
                })
            });
            
            const data = await response.json();
            stream.markdown(data.report);
        }
    };

    const participant = vscode.chat.createChatParticipant('webinsight.analyzer', handler);
    participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'icon.png');
}
```

用法：在 VS Code Copilot Chat 中输入：
```
@webinsight /analyze https://diamondrosesanctuary.com
```

### 5.3 GitHub Models API 集成（降低成本）

GitHub Models 提供免费的 AI 模型访问：

```python
# 支持切换到 GitHub Models（免费额度）
def get_ai_client(provider: str = "deepseek", api_key: str = ""):
    if provider == "github":
        return OpenAI(
            api_key=os.environ.get("GITHUB_TOKEN"),  # GitHub Personal Access Token
            base_url="https://models.inference.ai.azure.com"
        ), "gpt-4o"  # GitHub Models 免费提供 GPT-4o
    elif provider == "deepseek":
        return OpenAI(api_key=api_key, base_url="https://api.deepseek.com"), "deepseek-chat"
```

---

## 🔧 六、具体代码优化项

### 6.1 修复 API Key 泄漏（最高优先级）

```html
<!-- index.html 第 669 行 - 立即删除 -->
<!-- ❌ 删除这行！ -->
<!--sk-f359f0e8601a487aa9e00e585ae33e52-->
```

API Key 改为服务端环境变量管理：
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# 服务端可配置默认 API Key（可选，用户也可自己输入）
DEFAULT_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
```

### 6.2 修复 system prompt 泄漏到输出

```python
# 当前问题：AI 把 role 描述当正文输出
# 原因：system prompt 开头是"你是世界顶级的网站分析师..."
# AI 将其作为输出的第一句话重复了

# 修复：在 stream endpoint 中，过滤掉第一个 chunk 如果它重复了 system prompt
async def event_generator():
    ...
    first_chunk = True
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            content = delta.content
            # 过滤可能的角色自我介绍
            if first_chunk and any(kw in content for kw in ["世界顶级", "资深全栈", "作为"]):
                first_chunk = False
                continue
            first_chunk = False
            payload = json.dumps({"content": content}, ensure_ascii=False)
            yield f"data: {payload}\n\n"
```

更好的解法：改写 system prompt，明确禁止自我介绍：

```python
system_content = f"""你是网站分析 AI。当前日期 {capture_date}。
规则：
- 直接输出报告内容，不要以自我介绍开头
- 报告第一行必须是 Markdown 标题（# 开头）
- 数据缺失时写"数据缺失，无法分析"，不要推断
- 使用 Markdown 格式"""
```

### 6.3 Playwright 优化（修复模块数据缺失）

```python
# 修改 is_spa_page 判断：所有网站都尝试 Playwright
async def fetch_website_smart(url: str) -> dict:
    """智能抓取：先静态，同时启动 Playwright，取更好的结果"""
    
    # 并发执行静态和 Playwright 抓取
    static_task = asyncio.create_task(fetch_website_requests(url))
    playwright_task = asyncio.create_task(fetch_website_playwright_v2(url))
    
    static_data = await static_task
    
    # 判断是否需要等待 Playwright 结果
    needs_dynamic = (
        is_spa_page(static_data) or
        static_data.get("text_length", 0) < 2000 or  # 内容太少
        len(static_data.get("scripts", [])) > 5       # 脚本密集型
    )
    
    if needs_dynamic:
        try:
            pw_data = await asyncio.wait_for(playwright_task, timeout=40)
            if pw_data.get("_source") == "playwright":
                return pw_data
        except asyncio.TimeoutError:
            logger.warning("Playwright 超时，使用静态数据")
    else:
        playwright_task.cancel()
    
    return static_data
```

### 6.4 增加历史记录持久化

```python
# database.py
import sqlite3
from datetime import datetime
import json

def init_db():
    conn = sqlite3.connect("webinsight.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            domain TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tech_stack TEXT,
            page_stats TEXT,
            report_md TEXT,
            report_summary TEXT
        )
    """)
    conn.commit()
    return conn

def save_analysis(url: str, website_data: dict, report: str):
    conn = init_db()
    # 生成简短摘要（前500字）
    summary = report[:500].replace('\n', ' ')
    conn.execute(
        "INSERT INTO analyses (url, domain, tech_stack, page_stats, report_md, report_summary) VALUES (?,?,?,?,?,?)",
        (url, website_data.get("domain"), 
         json.dumps(website_data.get("tech_stack"), ensure_ascii=False),
         json.dumps(website_data.get("page_stats"), ensure_ascii=False),
         report, summary)
    )
    conn.commit()
    conn.close()

# 新增 API 端点
@app.get("/api/history")
async def get_history(limit: int = 20, domain: str = None):
    conn = init_db()
    if domain:
        rows = conn.execute(
            "SELECT id, url, domain, created_at, report_summary, tech_stack FROM analyses WHERE domain LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{domain}%", limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, url, domain, created_at, report_summary, tech_stack FROM analyses ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()
    return [{"id": r[0], "url": r[1], "domain": r[2], "created_at": r[3], "summary": r[4], "tech_stack": json.loads(r[5] or "{}")} for r in rows]

@app.get("/api/history/{id}")
async def get_history_item(id: int):
    conn = init_db()
    row = conn.execute("SELECT * FROM analyses WHERE id=?", (id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "记录不存在")
    return {"id": row[0], "url": row[1], "domain": row[2], "created_at": row[3], "report": row[6]}
```

### 6.5 前端增加历史记录 UI

在 `index.html` 的报告区域下方添加历史记录面板：

```html
<!-- 历史记录 -->
<div id="historyPanel" style="margin-top:24px">
  <div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <h3 style="color:var(--text-secondary);font-size:0.9rem">📚 分析历史</h3>
      <button onclick="loadHistory()" class="btn btn-secondary" style="font-size:0.75rem;padding:4px 10px">刷新</button>
    </div>
    <div id="historyList" style="font-size:0.8rem;color:var(--text-muted)">点击"刷新"加载历史记录</div>
  </div>
</div>
```

```javascript
async function loadHistory() {
  const res = await fetch('/api/history?limit=10');
  const items = await res.json();
  const list = document.getElementById('historyList');
  if (!items.length) { list.textContent = '暂无历史记录'; return; }
  list.innerHTML = items.map(item => `
    <div style="padding:8px 0;border-bottom:1px solid var(--border);cursor:pointer" onclick="loadHistoryItem(${item.id})">
      <div style="color:var(--text-primary);font-weight:500">${item.domain || item.url}</div>
      <div style="color:var(--text-muted);font-size:0.72rem">${item.created_at} · ${Object.keys(item.tech_stack).join(', ')}</div>
      <div style="color:var(--text-secondary);margin-top:2px">${item.summary.slice(0, 100)}...</div>
    </div>
  `).join('');
}

async function loadHistoryItem(id) {
  const res = await fetch(`/api/history/${id}`);
  const item = await res.json();
  currentReport = item.report;
  renderReport(item.report);
  $('reportWrapper').classList.add('visible');
}
```

---

## 📋 七、优化路线图

### 第一阶段：立即修复（1天内）

| 优先级 | 任务 | 文件 | 预估时间 |
|:---|:---|:---|:---|
| 🔴 紧急 | 删除 HTML 注释中的 API Key | `index.html:669` | 5分钟 |
| 🔴 紧急 | 修复 system prompt 泄漏到输出 | `app.py` | 30分钟 |
| 🔴 高 | Playwright 等待时间从 0.8s 改为 2.5s | `app.py:813` | 5分钟 |
| 🟡 高 | 修复 SPA 判断：脚本密集型也走 Playwright | `app.py` | 1小时 |

### 第二阶段：核心升级（1周内）

| 任务 | 说明 |
|:---|:---|
| Multi-Agent 架构 | 拆分 Prompt 为 5 个专项 Agent 并发执行 |
| 历史记录持久化 | SQLite + 历史 API + 前端历史面板 |
| MCP Server | 将工具暴露为标准 MCP 协议 |
| CLI 工具 | 支持命令行批量分析 |

### 第三阶段：平台化（1个月内）

| 任务 | 说明 |
|:---|:---|
| GitHub Actions 监控 | 定期自动分析竞品网站 |
| 竞品对比分析 | 支持两个网站并排对比 |
| VS Code 插件 | Copilot Chat 集成 |
| GitHub Models 集成 | 提供免费 AI 模型选项 |

---

## 📊 优化前后对比

| 维度 | 当前版本 | 优化后 v2.0 |
|:---|:---|:---|
| **AI 分析质量** | 单次调用，大量推断 | Multi-Agent 并发，专项精准分析 |
| **数据采集深度** | 0.8s 等待，模块数据经常为空 | 2.5s+ 等待 + 滚动触发，数据完整 |
| **可集成性** | 独立工具，无接口 | MCP Server，可被任意 AI 工具调用 |
| **历史记录** | 无 | SQLite 持久化，支持趋势对比 |
| **自动化** | 手动触发 | GitHub Actions 定期监控 |
| **安全性** | API Key 明文注释泄漏 | 环境变量管理，无泄漏 |
| **报告质量** | system prompt 泄漏，结论矛盾 | ReflectionAgent 验证，结论一致 |
| **部署方式** | 本地单机 | 可部署到云端，支持多用户 |

---

*报告生成：2026年06月04日 | WebInsight 深度分析与优化方案*

