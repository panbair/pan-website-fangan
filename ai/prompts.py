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
def build_data_summary(website_data: dict, capture_time: str, capture_date: str) -> str:
    """将抓取数据格式化为 AI 友好的数据摘要"""
    return f"""
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
