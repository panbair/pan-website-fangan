"""动画分析模块 — 页面模块提取、CSS 动画参数解析"""


_MODULE_EXTRACTION_JS = """() => {
    const result = [];
    const selectors = [
        'section', '[class*="section"]', '[class*="module"]',
        '[class*="block"]', '[class*="panel"]', '[class*="hero"]',
        '[class*="feature"]', '[class*="banner"]', '[class*="card"]',
        'header[class]', 'footer[class]',
        'main > div', '#root > div > div', '#app > div > div',
        'body > div[id]', 'body > div[class*="wrapper"] > div',
    ];

    const foundElements = new Set();

    for (const sel of selectors) {
        try {
            const els = document.querySelectorAll(sel);
            els.forEach(el => {
                const rect = el.getBoundingClientRect();
                const isVisible = rect.width > 100 && rect.height > 50 &&
                                  rect.bottom > -200 && rect.top < window.innerHeight + 500;
                if (isVisible) foundElements.add(el);
            });
        } catch(e) {}
        if (foundElements.size >= 3) break;
    }

    if (foundElements.size === 0) {
        document.querySelectorAll('body > div > div > div').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width > 200 && rect.height > 100) foundElements.add(el);
        });
    }

    Array.from(foundElements).forEach((el, index) => {
        const rect = el.getBoundingClientRect();
        if (rect.width < 100 || rect.height < 50) return;

        const style = window.getComputedStyle(el);

        // HTML 结构摘要
        const tagNames = {};
        el.querySelectorAll('*').forEach(child => {
            const tag = child.tagName.toLowerCase();
            tagNames[tag] = (tagNames[tag] || 0) + 1;
        });

        // CSS 类名
        const classList = [];
        el.querySelectorAll('[class]').forEach(child => {
            child.classList.forEach(cls => {
                if (classList.length < 30 && !classList.includes(cls)) classList.push(cls);
            });
        });

        const inlineStyles = el.getAttribute('style') || '';
        const text = el.innerText ? el.innerText.trim().substring(0, 500) : '';

        // 子元素摘要
        const childSummary = [];
        const directChildren = el.children;
        for (let i = 0; i < Math.min(directChildren.length, 15); i++) {
            const child = directChildren[i];
            const childTag = child.tagName.toLowerCase();
            const childClass = child.className ? (typeof child.className === 'string' ? child.className.substring(0, 60) : '') : '';
            const childText = child.innerText ? child.innerText.trim().substring(0, 80) : '';
            childSummary.push({
                tag: childTag, class: childClass, text: childText,
                childCount: child.children.length
            });
        }

        // 动画详细参数 — 解析 CSS animation 简写
        const animDetail = (() => {
            if (style.animation === 'none' || !style.animation) return null;
            const parts = style.animation.split(',').map(a => a.trim());
            return parts.slice(0, 4).map(a => {
                const tokens = a.split(/\\s+/);
                return {
                    full: a.substring(0, 120),
                    name: tokens[0] || '',
                    duration: tokens[1] || '',
                    easing: tokens[2] || '',
                    delay: tokens[3] || '',
                    iteration: tokens[4] || '',
                };
            });
        })();

        // 动画详细参数 — 解析 CSS transition 简写
        const tranDetail = (() => {
            if (style.transition === 'none' || !style.transition || style.transition === 'all 0s ease 0s') return null;
            const parts = style.transition.split(',').map(t => t.trim());
            return parts.slice(0, 4).map(t => ({
                full: t.substring(0, 120),
                prop: t.split(/\\s+/)[0] || '',
                duration: t.split(/\\s+/)[1] || '',
                easing: t.split(/\\s+/)[2] || '',
                delay: t.split(/\\s+/)[3] || '',
            }));
        })();

        // 统计有动画的子元素数量
        const animatedChildCount = (() => {
            let count = 0;
            el.querySelectorAll('*').forEach(child => {
                const cs = window.getComputedStyle(child);
                if ((cs.animation !== 'none' && cs.animation !== '') ||
                    (cs.transition !== 'none' && cs.transition !== '' && cs.transition !== 'all 0s ease 0s') ||
                    cs.transform !== 'none') {
                    count++;
                }
            });
            return count;
        })();

        result.push({
            index: index + 1,
            tag: el.tagName.toLowerCase(),
            id: el.id || '',
            className: (typeof el.className === 'string' ? el.className : '').substring(0, 150),
            width: Math.round(rect.width),
            height: Math.round(rect.height),
            top: Math.round(rect.top + window.scrollY),
            display: style.display,
            position: style.position,
            flexDirection: style.flexDirection,
            gridTemplateColumns: style.gridTemplateColumns || '',
            backgroundColor: style.backgroundColor,
            backgroundImage: style.backgroundImage ? style.backgroundImage.substring(0, 120) : '',
            padding: style.padding,
            margin: style.margin,
            border: style.border,
            borderRadius: style.borderRadius,
            boxShadow: style.boxShadow,
            textContent: text,
            textLength: (el.innerText || '').length,
            childCount: el.children.length,
            tagStats: tagNames,
            cssClasses: classList.slice(0, 30),
            inlineStyle: inlineStyles.substring(0, 200),
            childElements: childSummary,
            // 动画布尔标志
            hasAnimation: style.animation !== 'none' && style.animation !== '',
            hasTransform: style.transform !== 'none',
            hasTransition: style.transition !== 'none' && style.transition !== 'all 0s ease 0s',
            hasGradient: style.backgroundImage.includes('gradient'),
            // 内容统计
            hasVideo: el.querySelectorAll('video').length > 0,
            hasForm: el.querySelectorAll('form, input, textarea').length > 0,
            hasCanvas: el.querySelectorAll('canvas').length > 0,
            hasSVG: el.querySelectorAll('svg').length > 0,
            imgCount: el.querySelectorAll('img').length,
            buttonCount: el.querySelectorAll('button').length,
            linkCount: el.querySelectorAll('a').length,
            // 动画详细参数
            animationDetail: animDetail,
            transitionDetail: tranDetail,
            transformDetail: style.transform !== 'none' ? style.transform.substring(0, 200) : '',
            willChange: style.willChange !== 'auto' ? style.willChange : '',
            hasScrollAnimClass: /scroll|reveal|aos|wow|parallax|tilt|magnetic/i.test(
                (typeof el.className === 'string' ? el.className : '') + ' ' +
                Array.from(el.querySelectorAll('[class]')).map(c => c.className).join(' ').substring(0, 500)
            ),
            animatedChildCount: animatedChildCount,
        });
    });

    return result;
}"""


async def extract_page_modules_playwright(page) -> list:
    """使用 Playwright 提取页面每个模块/区块的详细信息"""
    modules = await page.evaluate(_MODULE_EXTRACTION_JS)
    return modules


def format_modules_for_prompt(modules: list) -> str:
    """将模块数据格式化为 AI 友好的 Markdown"""
    if not modules:
        return "（无模块数据 — 页面可能为极简页面或 SPA 空壳，内容由 JS 动态渲染）"

    lines = []
    for mod in modules:
        idx = mod.get('index', '?')
        tag = mod.get('tag', 'div')
        cls = mod.get('className', '')[:120]
        mod_id = mod.get('id', '')
        id_str = f' id="{mod_id}"' if mod_id else ''

        lines.append(f"""
### 模块 {idx}: `<{tag}{id_str} class="{cls}">`

| 属性 | 值 |
|------|-----|
| **尺寸** | {mod.get('width', '?')}×{mod.get('height', '?')}px |
| **垂直位置** | 距顶部 {mod.get('top', '?')}px |
| **display** | `{mod.get('display', '?')}` |
| **position** | `{mod.get('position', '?')}` |
| **flexDirection** | `{mod.get('flexDirection', '?')}` |
| **gridTemplateColumns** | `{mod.get('gridTemplateColumns') or '无'}` |
| **backgroundColor** | `{mod.get('backgroundColor', '?')}` |
| **backgroundImage** | `{mod.get('backgroundImage') or '无'}` |
| **padding** | `{mod.get('padding', '?')}` |
| **borderRadius** | `{mod.get('borderRadius', '?')}` |
| **boxShadow** | `{mod.get('boxShadow') or '无'}` |
| **hasGradient** | {'是' if mod.get('hasGradient') else '否'} |
| **hasAnimation** | {'是' if mod.get('hasAnimation') else '否'} |
| **hasTransform** | {'是' if mod.get('hasTransform') else '否'} |
| **hasTransition** | {'是' if mod.get('hasTransition') else '否'} |
| **willChange** | `{mod.get('willChange') or '无'}` |
| **hasScrollAnimClass** | {'是' if mod.get('hasScrollAnimClass') else '否'} |
| **动画子元素数** | {mod.get('animatedChildCount', 0)} 个 |
| **子元素数** | {mod.get('childCount', 0)} |
| **文本长度** | {mod.get('textLength', 0)} 字符 |
| **图片** | {mod.get('imgCount', 0)} 个 |
| **按钮** | {mod.get('buttonCount', 0)} 个 |
| **链接** | {mod.get('linkCount', 0)} 个 |
| **Canvas** | {mod.get('hasCanvas', False)} |
| **SVG** | {mod.get('hasSVG', False)} |
| **Video** | {mod.get('hasVideo', False)} |
| **表单** | {mod.get('hasForm', False)} |

**🎬 动画详细参数**:
""")
        # animationDetail
        anim_detail = mod.get('animationDetail')
        if anim_detail and len(anim_detail) > 0:
            for a in anim_detail[:4]:
                lines.append(f"- 动画 `{a.get('name', '?')}`: 时长={a.get('duration', '?')}, 缓动={a.get('easing', '?')}, 延迟={a.get('delay', '?')}, 重复={a.get('iteration', '?')}")
        else:
            lines.append("- （无 CSS Animation）")

        # transitionDetail
        tran_detail = mod.get('transitionDetail')
        if tran_detail and len(tran_detail) > 0:
            for t in tran_detail[:4]:
                lines.append(f"- 过渡 `{t.get('prop', '?')}`: 时长={t.get('duration', '?')}, 缓动={t.get('easing', '?')}, 延迟={t.get('delay', '?')}")
        else:
            lines.append("- （无 CSS Transition）")

        tf = mod.get('transformDetail', '')
        if tf:
            lines.append(f"- Transform: `{tf}`")

        lines.append(f"""
**CSS 类名**: {', '.join(['`' + c + '`' for c in mod.get('cssClasses', [])[:20]]) if mod.get('cssClasses') else '（无）'}

**元素标签统计**: {__import__('json').dumps(mod.get('tagStats', {}), ensure_ascii=False)}

**内联样式**: `{mod.get('inlineStyle', '无')}`

**文本内容**: {mod.get('textContent', '（无文本）')[:600]}

**直接子元素结构**:
""")
        for child in mod.get('childElements', [])[:15]:
            lines.append(f"- `<{child['tag']}>` class=\"{child['class'][:80]}\" → {child['text'][:100]} (内含 {child['childCount']} 个子元素)")

        lines.append("")

    return "\n".join(lines)
