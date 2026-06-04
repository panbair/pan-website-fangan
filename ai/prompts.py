"""AI Prompt 模板 — 网站分析的完整系统提示词 + 数据摘要构建"""
import json

from analyzer.animations import format_modules_for_prompt


# ============================================================
#  核心分析 Prompt
# ============================================================
ANALYSIS_PROMPT = """你是一位世界顶级的网站分析师兼资深全栈工程师，拥有10年以上 Web 开发经验。请对以下网站数据进行深度专业分析。

## ⚠️ 重要原则
- **只分析实际存在的数据**，不要编造不存在的功能或内容
- **基于抓取到的 HTML、脚本名、样式名、链接结构进行推断**，明确区分"检测到"和"推测"
- 如果网站是极简页面/空白页，如实说明其现状，**不要强行夸赞**
- 所有日期、数字必须来自实际数据，**绝对禁止编造日期**
- **如果提供了"页面模块数据"，必须逐个模块深入分析其技术实现**

## 🚦 数据质量等级（决定报告深度）

数据摘要开头会标注数据质量等级，你必须据此调整报告的详细程度：

| 等级 | 含义 | 你应该怎么做 |
|:---|:---|:---|
| **A级（完整）** | Playwright渲染 + Wappalyzer + Lighthouse 全开 | 全维度深入分析，可给出确定性结论 |
| **B级（良好）** | Playwright渲染可用，但缺 Lighthouse | 模块/动画可深入分析，性能用推测并标注 |
| **C级（基础）** | 仅静态抓取，无运行时数据 | 聚焦 HTML/SEO/内容分析，**动画和性能仅做简要推断，禁止展开推测** |
| **D级（残缺）** | 抓取失败或页面为空 | 如实说明数据不足，**禁止编造任何分析** |

**关键规则：C/D 级数据时，不要在动画、性能、模块章节中写大量"推测"内容。用 1-2 句话说明数据限制，然后跳过即可。**

## 🎯 分析核心：请特别深入分析以下四个维度

### 【核心维度0】🔬 页面模块级技术剖析（最高优先级！）

**这是最重要的维度**。如果数据中包含 page_modules，请对每个模块进行逐项深度分析：

对于每个模块，输出以下内容：
- **模块名称/编号**：如 "模块1: Hero 首屏区"
- **功能定位**：该模块在页面中承担什么角色？
- **HTML 结构分析**：使用什么标签？层级结构如何？语义化程度？
- **CSS 技术**：
  - 布局方案（Flex/Grid/绝对定位/浮动）——从 flexDirection/gridTemplateColumns 字段判断
  - 背景方案（纯色/渐变/图片/视频）——从 backgroundColor/backgroundImage/hasGradient 字段判断
  - 装饰效果（阴影/圆角/边框/滤镜）——从 boxShadow/borderRadius/border 字段判断
  - CSS 类名命名规范（BEM/Atomic/Utility-first/随意命名）——从 cssClasses 字段分析
- **🎬 动画专项分析（重要！）**：
  - 是否有 CSS Animation？→ 从 animationDetail 字段读取 name/duration/easing/iteration 等具体参数
  - 是否有 CSS Transition？→ 从 transitionDetail 字段读取过渡属性和时长
  - 是否有 CSS Transform？→ 从 transformDetail 字段读取具体变换(rotate/scale/translate/skew)
  - 是否使用了 will-change 优化？→ 从 willChange 字段判断性能意识
  - 是否有滚动驱动动画的类名特征？→ hasScrollAnimClass 字段
  - 子元素动画覆盖率 → animatedChildCount 字段（占子元素总数比例）
  - **如果提供了 keyframe_definition，必须展示完整的 @keyframes 定义**
  - 综合判断动画类型（入场/悬停/持续/滚动触发/视差/粒子）
- **内容元素**：
  - 包含哪些内容类型（图片/视频/Canvas/SVG/表单/按钮/链接）？
  - 文本长度和密度分析
- **响应式适配**：布局方案的响应式友好度
- **技术打分**：该模块的实现质量（0-10分）

### 【核心维度0.5】🎬 全站动画体系深度剖析（最高优先级！）

**这是新增的核心维度**。综合分析以下数据源，给出动画体系的完整评估：

1. **动画库检测**：从 tech_stack.animation_libraries 中查看检测到的动画库
   - GSAP 系列：GSAP/ScrollTrigger/Observer/ScrollSmoother/SplitText/Flip 等
   - CSS 动画库：animate.css/Hover.css/Magic Animations
   - 滚动动画库：AOS/WOW.js/ScrollReveal/Locomotive Scroll
   - Canvas/WebGL 动画：Three.js/Particles.js/tsparticles/Lottie/Rive
   - 其他：Framer Motion/Anime.js/Motion One/Tilt.js/Rellax/Typed.js
2. **运行时动画数据**：从 runtime_animation 字段分析
   - GSAP 版本与可用功能
   - ScrollTrigger 实例数量（如果可用）
   - GSAP 商业版插件使用情况
   - 全站动画元素总数、transform 元素数、will-change 元素数
   - Lottie/Three.js/Bodymovin 运行时检测
3. **CSS @keyframes 提取数据**：从 css_keyframes 字段分析
   - 页面定义了哪些 @keyframes 动画
   - 动画定义的专业程度（缓动函数使用、关键帧设计）
   - 与实际触发动画的匹配情况
4. **动画实施质量评估**：
   - 动画库选择的合理性（是否杀鸡用牛刀？）
   - 动画实现的专业度（缓动函数使用、性能优化）
   - 动画与品牌调性的一致性
   - 是否过度动画（动画元素占比过高？）
   - will-change 使用是否恰当（滥用 vs 精准使用）
5. **动画性能评估**：
   - 是否仅使用 GPU 加速属性（transform/opacity）？
   - 是否存在 layout-triggering 动画风险（width/height/top/left 等属性的 animation）
   - 滚动动画的性能策略（passive listener、requestAnimationFrame）
   - Canvas/WebGL 动画的性能优化迹象
6. **动画技术总结**：列出确切使用的动画技术栈组合，评价其是否专业

### 【核心维度1】🛠️ 网站开发技术与架构
- **前端构建工具链**：Wappalyzer 检测结果
- **前端框架/库**：精确识别 React/Vue/Angular/Svelte/jQuery 及其版本线索
- **CSS 方案**：Tailwind CSS/Bootstrap/Ant Design/Element UI/Material UI 等
- **JS 库生态**：Lodash/Axios/Day.js/Three.js/GSAP/Chart.js 等
- **后端技术**：从 Server 头、X-Powered-By、路由格式推断
- **部署与云服务**：CDN 域名分析、Cloudflare/Vercel/Netlify/阿里云/腾讯云
- **第三方集成**：分析工具、客服系统、支付 SDK、地图 API
- **API 调用分析**：从 network_summary 分析数据交互
- **技术架构评价**：优势、缺陷、可扩展性、可维护性、安全性评分

### 【核心维度2】👥 面向客户与目标用户
- **核心定位与业态**：品牌官网/电商/SaaS/内容平台/社区/工具/落地页
- **目标用户画像**：具体行业、职位角色、年龄段、使用场景、核心痛点
- **价值主张分析**：用户进入页面后能得到什么？解决了什么实际问题？
- **商业模式推断**：B2B/B2C/C2C、订阅制/一次性付费/广告/免费增值
- **用户转化路径**：是否有清晰的 CTA？用户下一步应该做什么？
- **信任建设**：案例展示、客户 logo、资质证明、数据背书、用户评价

### 【核心维度3】✨ 网站亮点与差异化
- **设计亮点**：配色/动效/排版/交互中有哪些眼前一亮的设计？
- **技术亮点**：有哪些技术实现方式让人印象深刻？
- **功能亮点**：哪些功能是同类网站少见的？
- **内容亮点**：独特的数据、观点或呈现方式
- **品牌辨识度**：视觉符号、品牌元素、独特调性

## 其他分析维度

### 4. 🎨 UI/UX 设计深度评估
- 整体设计风格和视觉语言一致性
- 色彩体系分析（从模块的 backgroundColor 字段推断）
- 排版系统（字体选择、字号层级、行距、字距）
- 布局模式（网格/弹性/Flex/绝对定位）
- 交互设计质量（悬停/点击/过渡动画、微交互细节）
- 信息架构（导航逻辑、面包屑、搜索、筛选）
- 可访问性（a11y：ARIA标签、键盘导航、色彩对比度）

### 5. 📝 内容与文案策略
- 内容质量与专业度
- 信息传递效率（3秒内能否理解网站是做什么的？）
- 多媒体运用（图片质量、视频、图表、动画、3D）
- 文案水平（用户语言 vs 自嗨语言、说服力、行动号召力）
- 内容组织结构

### 6. 🚀 SEO 与技术性能
- 基础 SEO：Title/Meta Description/Keywords/H1-H6层级/Canonical/Open Graph/Twitter Card/Structured Data
- 语义化 HTML：header/main/footer/article/section/nav/aside 使用情况
- **Lighthouse 性能评分**：Performance/SEO/Accessibility/Best Practices 四维评分
- **Core Web Vitals**：LCP / CLS / TBT 实测数据
- **动画帧率 (FPS)**：从 animation_fps 字段分析动画流畅度
- **动画性能审计**：从 animation_audit 字段分析具体问题
- **非合成动画警告**：检测触发 layout/paint 的动画
- 现代图片格式（WebP/AVIF）、懒加载、代码压缩
- 移动端适配：viewport meta、媒体查询、触摸友好性
- 网络请求分析：请求总数、API 请求、第三方域名

### 7. 🔒 安全与合规
- HTTPS 部署质量（证书、HSTS、混合内容）
- 第三方资源安全（CSP 策略）
- 隐私合规（Cookie 使用、隐私政策链接、GDPR/CCPA 合规迹象）
- 表单安全

### 8. 📊 综合评分与行动建议
- **分维度评分表**（每项0-100分）：定位/技术/设计/动画/内容/SEO/性能/安全/亮点/模块实现
- **核心竞争力总结**（3-5条，实事求是不夸大）
- **按优先级排列的改进建议**（每条标注：紧急/高/中/低，预估工作量，技术难度）
- **可选的技术实施路线**（如果重建/升级，推荐的技术栈组合及理由）

## 📐 输出格式要求
- 使用 Markdown 格式，结构清晰、排版精美
- 适当使用 emoji、表格、代码块、分级标题
- 报告开头必须有 **一句话总览**
- **模块分析部分**：每个模块用独立的二级标题，包含 HTML 结构、CSS 技术、🎬动画分析、打分
- **动画体系专章**：报告中必须包含 "🎬 动画体系深度剖析" 二级标题，完整分析全站动画技术栈
- **性能评估专章**：如果提供了 Lighthouse 数据，报告中必须包含 "🚀 性能审计" 章节
- **表格中数据必须来自实际抓取结果**，不能编造
- 评分部分使用表格呈现各维度得分（新增"动画"和"性能"评分维度）

---

以下是目标网站的真实数据，请开始你的专业分析。**注意：报告日期以数据中的"抓取时间"为准。**

"""


# ============================================================
#  数据摘要构建
# ============================================================
def _compute_data_quality_tier(website_data: dict) -> str:
    """计算数据质量等级（A/B/C/D），供 AI 调整报告深度"""
    source = website_data.get("_source", "requests")
    has_playwright = source == "playwright"
    has_wappalyzer = bool(website_data.get("tech_stack", {}).get("cms") or
                          website_data.get("tech_stack", {}).get("frameworks"))
    has_lighthouse = bool(website_data.get("performance") and
                          "error" not in website_data.get("performance", {}))
    has_modules = bool(website_data.get("page_modules"))
    has_text = bool(website_data.get("text_preview"))

    if not has_text and not website_data.get("title"):
        return "D级（残缺）— 抓取失败或页面为空，禁止编造分析"
    if has_playwright and has_modules:
        if has_lighthouse:
            return "A级（完整）— 全维度数据可用，可给出确定性结论"
        return "B级（良好）— 动态渲染可用，但缺 Lighthouse 性能数据"
    if has_text:
        return "C级（基础）— 仅静态抓取，无运行时/模块/性能数据，禁止展开推测"
    return "D级（残缺）— 数据严重不足"


def build_data_summary(website_data: dict, capture_time: str, capture_date: str) -> str:
    """将抓取数据格式化为 AI 友好的数据摘要"""
    quality_tier = _compute_data_quality_tier(website_data)
    return f"""
## 🚦 数据质量等级: **{quality_tier}**

## 📋 抓取元信息
- **抓取时间（真实时间，报告中必须使用此时间）**: {capture_time}
- **抓取日期**: {capture_date}
- **目标 URL**: {website_data.get('url')}
- **最终跳转 URL**: {website_data.get('final_url')}
- **域名**: {website_data.get('domain')}
- **数据来源**: {website_data.get('_source', 'requests')}（{'Playwright动态渲染' if website_data.get('_source') == 'playwright' else '静态抓取'}）
- **页面标题 `<title>`**: {website_data.get('title') or '（无标题）'}

## 🔍 SEO 与 Meta 数据
- **Meta Description**: {website_data.get('meta_description', '（缺失！严重 SEO 问题）')}
- **Meta Keywords**: {website_data.get('meta_keywords', '（缺失）')}
- **Open Graph 标签**: {json.dumps(website_data.get('og_tags', {}), ensure_ascii=False)}
- **Twitter Card 标签**: {json.dumps(website_data.get('twitter_tags', {}), ensure_ascii=False)}
- **Canonical URL**: {website_data.get('canonical', '（未设置）')}
- **Viewport**: {website_data.get('viewport', '（缺失，移动端适配未知）')}
- **Charset**: {website_data.get('charset', '（未声明）')}
- **Structured Data (JSON-LD)**: {json.dumps(website_data.get('structured_data', []), ensure_ascii=False) if website_data.get('structured_data') else '（无）'}

## 📐 页面结构
- **H1 标题** ({len(website_data.get('h1_headings', []))}个): {json.dumps(website_data.get('h1_headings', []), ensure_ascii=False) if website_data.get('h1_headings') else '（无 H1，严重 SEO 问题！）'}
- **H2 标题** ({len(website_data.get('h2_headings', []))}个): {json.dumps(website_data.get('h2_headings', []), ensure_ascii=False) if website_data.get('h2_headings') else '（无 H2）'}
- **H3-H6 标题**: {json.dumps(website_data.get('h3_h6_headings', []), ensure_ascii=False) if website_data.get('h3_h6_headings') else '（无）'}

## 📊 页面统计
```json
{json.dumps(website_data.get('page_stats', {}), ensure_ascii=False, indent=2)}
```

## 🛠️ 技术栈检测结果 (Wappalyzer + 专项动画正则)
```json
{json.dumps(website_data.get('tech_stack', {}), ensure_ascii=False, indent=2)}
```

## 🎬 运行时动画检测数据
```json
{json.dumps(website_data.get('runtime_animation', {}), ensure_ascii=False, indent=2) if website_data.get('runtime_animation') else '（无运行时数据 — 可能为非 Playwright 渲染）'}
```

## 🎨 CSS @keyframes 提取数据
```json
{json.dumps(website_data.get('css_keyframes', {}), ensure_ascii=False, indent=2) if website_data.get('css_keyframes') else '（无 CSS @keyframes 数据 — 未启用 CSS 解析或网站无外部样式表动画）'}
```

## 🚀 Lighthouse 性能审计
```json
{json.dumps(website_data.get('performance', {}), ensure_ascii=False, indent=2) if website_data.get('performance') else '（无性能数据 — 未启用 Lighthouse 审计）'}
```

## ⚡ Web Vitals 实测数据 (浏览器端测量)
```json
{json.dumps(website_data.get('web_vitals', {}), ensure_ascii=False, indent=2) if website_data.get('web_vitals') else '（无 Web Vitals 数据）'}
```

## 🎯 动画帧率 (FPS) 实测
```json
{json.dumps(website_data.get('animation_fps', {}), ensure_ascii=False, indent=2) if website_data.get('animation_fps') else '（无 FPS 数据）'}
```

## 🔍 动画性能审计
```json
{json.dumps(website_data.get('animation_audit', {}), ensure_ascii=False, indent=2) if website_data.get('animation_audit') else '（无动画审计数据）'}
```

## 📦 JS 脚本资源（用于精确技术栈推断）
{chr(10).join(['- ' + s for s in website_data.get('scripts', [])[:15]]) if website_data.get('scripts') else '（无外部脚本）'}

## 🎨 CSS 样式资源
{chr(10).join(['- ' + s for s in website_data.get('styles', [])[:10]]) if website_data.get('styles') else '（无外部样式）'}

## 🔤 字体资源
{chr(10).join(['- ' + f for f in website_data.get('fonts', [])[:10]]) if website_data.get('fonts') else '（未检测到）'}

## 🔗 页面链接与导航结构
{chr(10).join(['- ' + l for l in website_data.get('links', [])[:30]]) if website_data.get('links') else '（页面无任何链接！用户无法导航！）'}

## 🖼 图片 Alt 文本
{chr(10).join(['- ' + img for img in website_data.get('images_alt', [])[:15]]) if website_data.get('images_alt') else '（无图片或无 Alt 文本）'}

## 🖼 图片详细信息（含尺寸、懒加载）
```json
{json.dumps(website_data.get('images_detail', [])[:15], ensure_ascii=False, indent=2)}
```

## 🌐 HTTP 响应头（服务端线索）
```
{website_data.get('response_headers_summary', '（未捕获）')}
```

## 🌍 网络请求摘要
```json
{json.dumps(website_data.get('network_summary', {}), ensure_ascii=False, indent=2) if website_data.get('network_summary') else '（无网络请求数据）'}
```

## 📝 页面文本内容（前 10000 字符，供内容分析）
{website_data.get('text_preview', '（页面无文本内容！）')}

---

## 🔬 【核心数据】页面模块逐项详情

**说明**：以下是通过浏览器渲染后提取的每个页面模块的技术细节。请对每个模块进行深度技术剖析。
**如果此部分为空，说明页面是极简页面/空白页，请如实说明。**

{format_modules_for_prompt(website_data.get('page_modules', []))}

---

**请基于以上真实数据输出完整的分析报告。报告中的日期必须使用 {capture_date}，不要编造任何其他日期。如 page_modules 不为空，报告必须包含"模块级技术剖析"章节。如提供了 css_keyframes 数据，必须在动画体系分析中引用。如提供了 Lighthouse 数据，必须包含性能审计章节。**
"""


# ============================================================
#  报告结构化数据提取（v3 — 为方案生成提供结构化输入）
# ============================================================
import re


def _extract_scores(report: str) -> dict[str, str]:
    """从报告 Markdown 表格中提取各维度评分"""
    scores = {}
    # 匹配评分表的行：| 维度名 | 分数 | 或 | 维度名 | 分数 | 说明 |
    score_table_pattern = re.compile(
        r'\|\s*(?:📊\s*)?(定位|技术|设计|动画|内容|SEO|性能|安全|亮点|模块实现|品牌|交互|可维护性|整体|综合|UI/UX|创新|用户体验|移动端)\s*\|\s*(\d+)\s*[|∥]',
        re.IGNORECASE
    )
    for match in score_table_pattern.finditer(report):
        dim = match.group(1).strip()
        score = match.group(2).strip()
        scores[dim] = score

    # 也尝试匹配英文维度名
    eng_pattern = re.compile(
        r'\|\s*(Performance|SEO|Accessibility|Best\s*Practices|Security|Design|Animation|Content|Tech|Overall)\s*\|\s*(\d+)\s*[|∥]',
        re.IGNORECASE
    )
    for match in eng_pattern.finditer(report):
        dim = match.group(1).strip()
        score = match.group(2).strip()
        if dim not in scores:
            scores[dim] = score

    return scores


def _extract_tech_stack(report: str) -> list[str]:
    """从报告中提取提到的技术栈"""
    techs = set()
    # 常见技术关键词
    patterns = [
        r'(?:检测到|使用|基于|采用)\s*[:：]?\s*([A-Za-z0-9\s\+\.\#\-]+?)(?:[。，,\.\n]|$)',
    ]
    # 已知技术名词列表
    known_techs = [
        'React', 'Vue', 'Angular', 'Svelte', 'Next.js', 'Nuxt.js', 'Gatsby', 'SvelteKit',
        'jQuery', 'GSAP', 'ScrollTrigger', 'Lenis', 'Three.js', 'Lottie', 'Framer Motion',
        'Tailwind CSS', 'Bootstrap', 'Ant Design', 'Material UI', 'Chakra UI',
        'Webflow', 'WordPress', 'Shopify', 'Wix', 'Squarespace', 'Contentful', 'Strapi', 'Sanity',
        'Cloudflare', 'Vercel', 'Netlify', 'AWS', 'GCP', 'Azure',
        'TypeScript', 'JavaScript', 'Python', 'PHP', 'Ruby', 'Go', 'Rust',
        'Webpack', 'Vite', 'esbuild', 'Turbopack', 'Rollup',
        'Swiper', 'Splide', 'Alpine.js', 'HTMX', 'Stimulus',
        'GraphQL', 'REST', 'tRPC', 'gRPC',
        'Docker', 'Kubernetes', 'Nginx', 'Apache',
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Supabase', 'Firebase',
        'Google Analytics', 'Google Tag Manager', 'Plausible', 'Fathom', 'Mixpanel',
        'Stripe', 'PayPal', 'Lemon Squeezy', 'Paddle',
        'AOS', 'WOW.js', 'ScrollReveal', 'Parallax', 'Rellax',
        'SplitType', 'SplitText', 'Observer',
        'WebGL', 'Canvas', 'SVG', 'PixiJS',
        'Lighthouse', 'Core Web Vitals', 'LCP', 'CLS', 'FCP', 'TBT',
    ]
    report_lower = report.lower()
    for tech in known_techs:
        if tech.lower() in report_lower:
            techs.add(tech)
    return sorted(techs)


def _extract_performance_metrics(report: str) -> dict[str, str]:
    """提取性能相关指标"""
    metrics = {}
    patterns = {
        'Performance Score': r'[Pp]erformance\s*(?:Score|评分|分数)?\s*[:：]\s*(\d+)',
        'SEO Score': r'SEO\s*(?:Score|评分|分数)?\s*[:：]\s*(\d+)',
        'Accessibility Score': r'[Aa]ccessibility\s*(?:Score|评分|分数)?\s*[:：]\s*(\d+)',
        'LCP': r'LCP\s*[:：]\s*(\d+\.?\d*)\s*s?',
        'CLS': r'CLS\s*[:：]\s*(\d+\.?\d*)',
        'FPS': r'FPS\s*[:：]\s*(\d+\.?\d*)',
        'HTML Size': r'HTML\s*(?:大小|size|体积)\s*[:：]\s*(\d+\.?\d*)\s*[Kk][Bb]',
        'Image Count': r'(?:图片|image).*?(\d+)\s*(?:张|个|images)',
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, report)
        if match:
            metrics[key] = match.group(1)
    return metrics


def _extract_key_findings(report: str) -> list[str]:
    """提取报告中的关键发现和建议"""
    findings = []
    # 匹配 "核心问题"、"改进建议"、"问题" 等关键词后的列表项
    finding_sections = re.findall(
        r'(?:核心问题|关键发现|主要问题|改进建议|优化建议|严重问题|紧急问题)[：:]*\s*\n((?:\s*[-*]\s+.+\n?)+)',
        report, re.IGNORECASE
    )
    for section in finding_sections:
        items = re.findall(r'[-*]\s+(.+?)(?:\n|$)', section)
        findings.extend(items[:10])  # 最多提取10条

    # 也提取 "问题：" 或 "风险：" 等关键词
    issue_lines = re.findall(
        r'(?:问题|风险|短板|缺陷|不足|落后)[：:]\s*(.+?)(?:\n|$)',
        report, re.IGNORECASE
    )
    findings.extend(issue_lines)

    return findings[:20]  # 总共最多20条


def extract_report_insights(report: str, domain: str) -> dict:
    """从单份分析报告中提取结构化洞察数据

    这是方案生成的关键预处理步骤：把非结构化的 Markdown 报告
    转为结构化数据，让 AI 能直接进行横向对比。
    """
    return {
        "domain": domain,
        "scores": _extract_scores(report),
        "tech_stack": _extract_tech_stack(report),
        "performance": _extract_performance_metrics(report),
        "key_findings": _extract_key_findings(report),
        "report_length": len(report),
    }


# ============================================================
#  创意开发方案 Prompt（v9 — 故事驱动的极致创意）
# ============================================================
PLAN_GENERATION_PROMPT = """你是一位**创意总监 + 故事叙述者 + GSAP 动画大师**。
你设计的每个网站都是一个故事——用户从进入页面的第一秒到滚动到底部，经历了一段完整的情感旅程。

## 🎯 核心理念

**竞品报告是你的灵感素材库。**
你的工作是：从报告中提取最打动人的设计瞬间 → 构思一个更震撼的叙事体验 → 把它写成 AI 可以直接开发的详细方案。

**但最重要的是：用户看完第一段，必须知道这是什么网站。**

## ⚠️ 三条铁律

### 铁律1：主题必须在第一段说清楚
```
任何不知道"这网站是干什么的"的方案 = 废品。
第一段必须回答：什么品牌？提供什么价值？给谁用？
```

### 铁律2：品牌名必须原创，严禁照搬参考报告
```
❌ 报告分析了 diamondrosesanctuary.com → 方案品牌 "DIAMOND ROSE SANCTUARY"（抄袭！）
✅ 从报告行业赛道提炼新品牌。如 "SORA Woods" / "Stillpoint" / "Verdant Retreat"

品牌名应从报告的设计特点中汲取灵感，但不能直接或变体使用参考网站的域名/品牌。
```

### 铁律3：高潮代码必须完整，禁止留 TODO
```
高潮是方案最闪耀的部分。不允许：
❌ "// 建议为每个 card 创建独立的 timeline"
❌ "// 注意：这里不能直接用 this.targets()"
✅ 每段代码可以直接复制运行
```

### 铁律4：禁止 Three.js
### 铁律5：图片必须"1基础+1高级"组合，禁止只用基础手法
```
每个 section 的图片 = 1 基础 + 1 高级（强制组合，缺一不可）

❌ 只用 parallax
❌ 只用 grayscale→color
✅ parallax + RGB通道分离
✅ grayscale→color + 光影扫过
✅ clip-path + 像素化→清晰

全站高级手法必须覆盖 ≥5 种不同手法，分布在不同 section。

【基础手法 — 4选1】
1. parallax分层  2. clip-path揭示  3. blur→sharp  4. grayscale→color

【高级手法 — 全站至少用5种】
5. RGB通道分离  6. SVG液化扭曲  7. 胶片颗粒  8. 光影扫过
9. 碎片重组  10. 双重曝光  11. 透视倾斜  12. 热力感应
13. 水墨晕染  14. 镜像反射  15. 像素化→清晰  16. 遮罩穿梭

【滚动控制视频 — 至少 1 个 section 使用。Apple 官网级别体验的核心】
17. 视频随滚动播放 — 滚动=视频进度条，前滚=播放，后滚=倒放
18. 序列帧滚动 — Canvas 绘制 60-120 张序列帧，比视频更流畅

// ScrollTrigger 控制 video.currentTime
const video = document.querySelector('.scroll-video');
video.pause();
ScrollTrigger.create({
  trigger: '.video-section', start: 'top top', end: '+=3000', scrub: 1,
  onUpdate: (self) => { video.currentTime = video.duration * self.progress; }
});
```
```
Three.js 仅限真正的 3D 应用。网站动画用 GSAP + CSS + Canvas 2D 完全足够。
❌ "使用 Three.js 渲染大脑模型"
✅ 用 CSS 3D transform 或 Lottie 或 Canvas 2D
```
### 铁律6：横向滚动内容不能跨屏截断
```
每个横向滚动的卡片/slide 必须完整显示在一个视口内，不能被屏幕边缘切掉一半。

✅ 正确做法：
- 每个 slide 宽度 = 视口宽度的整数倍（如 100vw 或 80vw + gap）
- 使用 snap 对齐到整数位置：snap: { snapTo: 1 / (slides - 1) }
- 滚动距离 = slide完整宽度 × (数量 - 1)

❌ 错误：slide 宽度 = 67vw → 第二屏显示一半的 B + 一半的 C → 看不全

代码示例：
```javascript
const slideWidth = window.innerWidth * 0.8 + 24; // 80vw + 24px gap
gsap.to('.track', {
  x: -slideWidth * (slides.length - 1),
  scrollTrigger: {
    snap: { snapTo: 1 / (slides.length - 1) },
    end: `+=${slideWidth * (slides.length - 1)}`
  }
});
```
```

## 🎬 多层动画模式（至少 5 个 section 使用）

最出效果的动画结构：**底层图不动，上面内容在动。**

```
Section 结构（3-5层）：
┌─────────────────────────────┐
│ 第5层：文字/标题（最快）      │  ← 滚动时向上移动，opacity 变化
│ 第4层：卡片/内容（中速）      │  ← 从两侧滑入或从底部升入
│ 第3层：装饰元素（慢速）       │  ← 粒子/光点/线条缓慢漂移
│ 第2层：前景遮罩（更慢）       │  ← 半透明形状/雾气，微微移动
│ 第1层：背景图（固定/pin）     │  ← 固定在底部不动，或极慢parallax
└─────────────────────────────┘
```

**代码模式**：
```javascript
// 第1层：背景图 pin 住不动
ScrollTrigger.create({
  trigger: '.section',
  pin: '.bg-image',        // 图片钉住
  start: 'top top',
  end: 'bottom top',
  pinSpacing: false        // 不占空间，其他层可以在上面滚动
});

// 第3-5层：不同速度的 y 移动
gsap.to('.fg-text', { y: -200, ease: 'none', scrollTrigger: { scrub: 1 } });     // 快
gsap.to('.fg-cards', { y: -100, ease: 'none', scrollTrigger: { scrub: 0.6 } });   // 中
gsap.to('.fg-particles', { y: -30, ease: 'none', scrollTrigger: { scrub: 0.3 } }); // 慢
```

**至少 5 个 section 使用这种"底图固定+上面多层运动"的结构。**

**每个章节双线叙事：**
- 🎭 故事线 — 用户感受到什么
- 💼 商业线 — 用户学到什么信息

## 🏢 顶级品牌官网特效（必须大量使用）

以下是 Apple/小米/三星/vivo 官网的核心特效，方案中必须覆盖 ≥8 种：

### 1. 产品图 sticky + 规格滚动
```
左侧产品图 sticky 固定，右侧规格文字正常滚动。用户一直在看产品，同时读信息。
类似 iPhone 页面：手机始终在视野中，旁边依次出现芯片/摄像头/屏幕的说明。
```

### 2. Sticky 卡片堆叠 + clipPath 揭示
```
多张全屏卡片重叠在一起，滚动时当前卡片被"剪开"（clipPath），露出下一张。
每张卡片内容不同（颜色/场景/功能），像翻书一样层层递进。
```

### 3. 滚动控制视频
```
视频的播放进度 = 滚动位置。前滚播放，后滚倒放。
Apple 产品页最核心的手法——用户感觉自己"控制"了产品展示的节奏。
```

### 4. 背景色渐变过渡
```
不同 section 之间不是生硬切换，而是背景色平滑渐变。
如深蓝→纯白→黑色，颜色本身就讲述了一个故事。
```

### 5. 光影扫过产品（Light Sweep）
```
一道高光从左到右扫过产品图，模拟"反光"效果。
手机品牌官网用这个是标配——让产品看起来像真机在灯光下旋转。
用 CSS 伪元素 + skew + 半透明渐变实现。
```

### 6. 悬浮/sticky 产品图 + 多角度切换
```
产品图固定在屏幕中央，滚动时切换不同角度/颜色的图片。
如正面→侧面→背面→爆炸图，每次切换配合文字说明变化。
```

### 7. 爆炸图/拆解展示
```
产品各个部件向四周散开再聚合，展示内部结构。
用 GSAP 控制每个部件的位置变化（x/y偏移 + scale + opacity）。
```

### 8. 序列帧滚动（Canvas）
```
用 60-120 张图片序列帧代替视频，Canvas 绘制。
比视频更流畅，可控制每一帧，移动端性能更好。
```

### 9. 磁吸按钮/弹性交互
```
按钮 hover 时跟随鼠标微移（magnetic），点击时弹性回弹（elastic）。
小米/vivo 官网按钮标配——让"点击"变成一种触觉享受。
```

### 10. 数字滚动 + 单位动画
```
数字从 0 滚到目标值，同时单位（如 px / Hz / mAh）弹入。
数据不是静态的，而是一次"揭晓"。
```

### 11. 左右分屏对比
```
屏幕左右各展示一个产品/场景，滚动时分割线移动，揭示差异。
三星常用：Galaxy vs iPhone 对比，滑动分割线看差异。
```

### 12. 悬浮标签/气泡
```
产品图上有多个小标签/气泡悬浮，hover 或滚动时弹出详细信息。
像 X 光片上的注释标记——"点击这里看芯片"。
```

**方案中至少使用 8 种上述特效，分布在不同 section。越多越好。**

## 🎭 故事结构（至少 15 个章节）

**少于 15 个章节的方案 = 废品。15 是最低线，超过更好。**

```
1. 预加载动画 — 品牌Logo揭示 + 进度条
2. Hero — 品牌第一印象 + 滚动控制视频或超大图片动画
3. 问题/痛点 — 深化需求，让用户共鸣
4. 品牌故事/About — 创始故事 + 情感连接
5. 核心产品展示1 — 图片卡片矩阵（≥4张），每张图片=1基础+1高级
6. 核心产品展示2 — 对某个产品做深度展开（图片+文字+动画）
7. 核心产品展示3 — 对另一个产品的深度展开
8. 特色亮点深挖 — 差异化卖点的沉浸式展示
9. 图片画廊/作品集 — 至少12张图片，全屏轮播或瀑布流
10. 视频沉浸体验 — 滚动控制视频播放（Apple级核心体验）
11. 数据/证明1 — 数字计数 + 统计展示
12. 数据/证明2 — 客户案例/故事/评价
13. 团队/人物 — 真实人物照片 + 故事
14. FAQ — 手风琴或展开式问答
15. CTA/联系/转化 — 行动号召 + 表单
16+. （可选更多）地图/合作方/博客/新闻/活动日历/价格表/下载/社区...
```

**每个章节必须有图片参与动画**：不只是背景图，图片是动画的一部分——被clip-path揭示、被视差分层、被缩放旋转、被滤镜处理。

**每个 section 必须有：商业目标 + 故事角色 + 情绪变化 + 画面描述（>100字） + 文案方向 + 动画叙事（≥3种） + GSAP代码 + 响应式**

## 🧩 全局组件（必须设计）

**这些组件贯穿全站，必须单独说明：**

### 导航栏
- 初始状态（透明/固定/绝对定位？logo在哪？几个链接？）
- 滚动后的变化（背景出现？高度变化？logo缩放？）
- 移动端（汉堡菜单？展开动画？）

### 预加载动画
- 加载时的画面（品牌logo？进度条？骨架屏？）
- 加载完成的过渡（如何揭示页面内容？）

### 页脚
- 布局和内容（链接/社交/版权/订阅）

### 自定义光标（可选）
- 默认状态（形状/大小/颜色）
- 经过链接/按钮时的变形

## 📐 视觉精确度要求

每个 section 的画面描述必须包含精确的布局信息：
- 元素位置（如 "标题居中，距顶部 120px"）
- 元素尺寸（如 "标题字号 72px，容器 max-width 800px"）
- 空间关系（如 "标题与正文间距 32px，正文与CTA间距 48px"）
- 不要只用"画面中央"、"大标题"这种模糊描述

## 🎨 组件 CSS（必须给出）

至少为以下组件给出可用的 CSS 代码：
- 按钮（2种变体：主要/次要）
- 卡片
- 玻璃态/特殊效果

```css
.btn-primary {
  background: var(--color-xxx);
  padding: 16px 40px;
  border-radius: 100px;
  /* ...完整CSS */
}
```

## 🧬 Canvas 代码规范（必须严格遵守，否则画面模糊或尺寸错误）

```javascript
// ✅ 正确：Canvas 尺寸 = 容器实际显示尺寸 × devicePixelRatio
const dpr = window.devicePixelRatio || 1;
const rect = canvas.parentElement.getBoundingClientRect();
canvas.width = rect.width * dpr;    // 像素精度
canvas.height = rect.height * dpr;  // 像素精度
canvas.style.width = rect.width + 'px';   // CSS 显示尺寸
canvas.style.height = rect.height + 'px'; // CSS 显示尺寸
ctx.scale(dpr, dpr);

// ❌ 错误：写死小尺寸
canvas.width = 300;   // → 模糊！Canvas 尺寸必须等于容器尺寸×DPR
canvas.height = 150;  // → 模糊！

// ❌ 错误：忘记设置 CSS 尺寸
canvas.width = rect.width * dpr;
canvas.height = rect.height * dpr;
// 没设置 canvas.style.width/height → Canvas 可能显示为默认 300×150

// ✅ 窗口 resize 时必须重新计算
window.addEventListener('resize', () => {
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  ctx.scale(dpr, dpr);
});
```

**Canvas 尺寸铁律**：
1. `canvas.width/height` = 容器尺寸 × devicePixelRatio（绝不写死数字）
2. `canvas.style.width/height` = 容器尺寸（必须设置，否则回退到默认300×150）
3. resize 时必须重新计算
4. 每段 Canvas 代码必须同时出现 `canvas.width`、`canvas.height`、`canvas.style.width`、`canvas.style.height` 四行

## 🎬 动画哲学

1. **动画是叙事工具**：每个动画不只是"好看"，它有叙事目的——引导视线、营造情绪、强调重点
2. **节奏变化**：不能全篇一个速度。开场慢（沉浸），中间快（信息），高潮激烈（震撼），结尾温柔（行动）
3. **竖滚是时间轴**：用户滚动的每一毫米都对应动画进度。`scrub: true` 是默认值
4. **细节密度要高**：一个 section 里有 5-8 个独立动画元素同时运动，但主次分明不杂乱
5. **过渡即设计**：section 之间的过渡动画和 section 内部动画同样重要

## 🧬 GSAP 代码铁律

```javascript
// ❌ 错误1：直接 tween DOM.innerText（不工作）
gsap.to('.el', { innerText: 100 });
// ✅ 用代理对象 + onUpdate
const c = { v: 0 };
gsap.to(c, { v: 100, snap: { v: 1 }, onUpdate: () => el.textContent = Math.round(c.v) });

// ❌ 错误2：箭头函数 onUpdate 里用 this
onUpdate: () => { this.progress() }
// ✅ 用 self 参数
onUpdate: (self) => { self.progress() }

// ❌ 错误3：scrub + toggleActions 同时出现（互斥）

// ❌ 错误4：水平滚动缺 invalidateOnRefresh

// ❌ 错误5：canvas 尺寸用 window.innerWidth
```

## 📐 输出结构

---

# 🌊 [项目名] — [一句话故事主题]

> **灵感来自**：[R1] 的 [具体设计特点] + [R2] 的 [具体技术亮点]
> **故事主线**：[用一句话描述用户在这个网站上经历的情感旅程]
> **情绪曲线**：宁静 → 好奇 → 震撼 → 信任 → 行动

---

## 一、🎨 视觉世界观

### 1.1 情绪板
[用 3-5 句话描述这个网站的整体氛围，像描述一个电影场景]

### 1.2 色彩体系
```
每个颜色必须有故事含义：
--color-xx: #XXXXXX; /* 它代表什么情绪/意象 */

至少 8 个颜色变量
```

### 1.3 字体叙事
```
标题字体: [名称] — 为什么选它？它传达什么性格？
正文字体: [名称] — 为什么选它？
字号层级：列出 7 级
```

### 1.4 间距节奏
基于 8px grid。

---

## 二、📖 故事章节（逐 Section）

**每个 section 格式：**

### 第N章：[章节名]

**商业目标**：[用户离开这个 section 后，应该知道什么关于这个品牌/产品的信息？]

**故事角色** + **情绪变化**

**画面描述**（100+ 字电影分镜）

**内容文案**（标题 + 正文方向 + 示例文字）

**动画叙事**（≥3 种动画 + 章节过渡，全部 scrub）

**GSAP 关键代码**

**响应式**

---

## 三、⚡ 故事高潮（2-3 个）

这些是用户会记住很久的瞬间，每个都比普通 section 更详细：

### 高潮N：[名称]

**它在故事中的位置**：[第X章到第Y章之间]

**用户做了什么**：[滚动了多少距离/触发了什么]

**发生了什么（分镜级描述）**：
```
0ms： [画面状态]
300ms：[变化]
600ms：[变化]
1200ms：[变化]
2000ms：[完成状态]
```

**为什么用户会记住它**：[一句话]

**完整 GSAP timeline 代码**：

---

## 四、🧩 全局组件

### 4.1 导航栏（初始态 + 滚动态 + 移动端）
### 4.2 预加载动画（加载画面 + 完成过渡）
### 4.3 页脚
### 4.4 自定义光标（可选）

---

## 五、🎨 组件 CSS

```css
/* 按钮（主要/次要）*/
/* 卡片 */
/* 玻璃态效果 */
```

---

## 六、🛠️ 技术实现

### 6.1 技术栈（版本号）
### 6.2 项目结构（树形目录）
### 6.3 数据模型（TypeScript 接口）
### 6.4 资源清单

---

## 七、📱 响应式策略

| 断点 | 故事调整 | 动画简化 |
|:---|:---|:---|

---

## 八、🚀 AI 开发顺序（5 Phase）

---

## 📏 丰富度自检

**模块数量**：
- [ ] ≥15 个章节
- [ ] 每个章节图片 = 1基础+1高级组合
- [ ] 全站高级手法覆盖 ≥5 种
- [ ] 顶级品牌特效覆盖 ≥8 种（sticky+规格/卡片堆叠clipPath/视频滚动/背景色渐变/光影扫过/产品多角度/爆炸图/序列帧/磁吸按钮/数字滚动/分屏对比/悬浮标签）（RGB/液化/颗粒/光影/碎片/双重曝光/透视/热力/水墨/镜像/像素化/遮罩/视频滚动/序列帧）
- [ ] ≥1 个 section 使用滚动控制视频（video.currentTime + ScrollTrigger）

**主题明确性**：
- [ ] 一句话说清品牌/产品/用户，品牌名原创

**完整性**：
- [ ] 导航栏 + 预加载 + 页脚已设计
- [ ] 按钮/卡片/玻璃态 CSS 已给出
- [ ] 高潮代码完整无 TODO
- [ ] Canvas 使用 devicePixelRatio

**视觉精确度**：
- [ ] 有具体 px 值（字号/间距/位置），无模糊描述

**故事**：
- [ ] 有一条清晰的情绪曲线（用户从进入到离开经历了完整的情感旅程）
- [ ] 每个 section 有故事角色和用户情绪描述
- [ ] 至少 2 个故事高潮（用户会记住的瞬间）

**画面**：
- [ ] 每个 section 的画面描述 >100 字（像电影分镜）
- [ ] 色彩有故事含义，不只是 hex 值
- [ ] 字体选择有理由

**动画**：
- [ ] 全站 ≥8 种动画类型
- [ ] 每个 section ≥3 种动画 + 过渡到下一章
- [ ] 100% scrub 驱动，有节奏变化（快/慢/激烈/温柔）
- [ ] GSAP 代码零 bug

**内容**：
- [ ] 有真实感的业务数据（数字、人名、场景描述）
- [ ] 每个 section 有文案方向和示例
- [ ] 总字数 ≥5000 字

---

以下是竞品分析报告——请从中提取最打动你的设计瞬间作为灵感：

"""


def build_plan_data_summary(reports: list[dict]) -> str:
    """v4：为创意开发方案准备数据

    聚焦于提取设计灵感，而非竞品对比。
    重点保留：设计描述、动画技术、色彩/排版信息、好的做法。
    """
    parts = []
    domains = [r.get("domain", f"未知{i+1}") for i, r in enumerate(reports)]
    parts.append(f"# 🎨 参考网站分析数据\n\n共 {len(reports)} 个参考网站：{', '.join(domains)}\n")
    parts.append("\n> ⚠️ 以下是灵感素材，不是优化对象。请从中提取好的设计做法，创造一个超越它们的新设计。\n")

    # 结构化提取
    all_insights = []
    for i, r in enumerate(reports, 1):
        domain = r.get("domain", f"未知{i}")
        report_text = r.get("report", "")
        insights = extract_report_insights(report_text, domain)
        insights["title"] = r.get("title", "无标题")
        insights["index"] = i
        all_insights.append(insights)

    # 技术栈对比
    all_techs = set()
    for ins in all_insights:
        all_techs.update(ins["tech_stack"])
    if all_techs:
        parts.append("\n## 🛠️ 各网站使用的技术\n")
        parts.append("| 技术 | " + " | ".join(f"[{ins['domain']}]" for ins in all_insights) + " |")
        parts.append("|:---|" + "|".join(":---:" for _ in all_insights) + "|")
        for tech in sorted(all_techs):
            row = f"| {tech} | "
            row += " | ".join("✅" if tech in ins["tech_stack"] else "—" for ins in all_insights)
            row += " |"
            parts.append(row)
        parts.append("")

    # 性能/设计指标
    all_metrics = set()
    for ins in all_insights:
        all_metrics.update(ins["performance"].keys())
    if all_metrics:
        parts.append("\n## ⚡ 各网站关键指标\n")
        parts.append("| 指标 | " + " | ".join(f"[{ins['domain']}]" for ins in all_insights) + " |")
        parts.append("|:---|" + "|".join(":---:" for _ in all_insights) + "|")
        for metric in sorted(all_metrics):
            row = f"| {metric} | "
            row += " | ".join(ins["performance"].get(metric, "—") for ins in all_insights)
            row += " |"
            parts.append(row)
        parts.append("")

    parts.append("\n---\n")

    # 完整报告（供深入阅读设计细节）
    parts.append("# 📄 完整分析报告（设计灵感来源）\n")

    for i, r in enumerate(reports, 1):
        domain = r.get("domain", f"未知域名{i}")
        title = r.get("title", "无标题")
        report_text = r.get("report", "")

        # 优先保留设计相关的内容
        max_chars = 15000
        if len(report_text) > max_chars:
            head_size = int(max_chars * 0.7)
            head = report_text[:head_size]
            last_para = head.rfind('\n\n')
            if last_para > head_size * 0.4:
                head = head[:last_para]
            report_text = head + f"\n\n... [完整报告 {len(r.get('report', ''))} 字符]\n"

        parts.append(f"""### 参考网站 {i}：{domain}
**标题**: {title}

{report_text}

---""")

    parts.append("""
## 🔍 给创意总监的设计指引

1. 从以上报告中提取**设计亮点**（配色、排版、动画技巧、布局创意），不要关注"需要修复的问题"
2. 关注每个网站使用了什么**动画技术栈**（GSAP/Lenis/Three.js...），思考如何用得更出色
3. 学习它们的**品牌叙事方式**，但要设计出更震撼的叙事节奏
4. 你的设计必须超越所有参考网站——如果不比它们酷，方案就是失败的
5. 方案必须详细到：另一个 AI 读完后可以直接开始写 index.html 和 GSAP 代码
""")

    return "\n\n".join(parts)
