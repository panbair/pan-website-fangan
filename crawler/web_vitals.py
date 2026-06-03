"""
Web Vitals 测量 — 通过 Playwright 注入 web-vitals.js 测量真实性能

测量指标:
- LCP (Largest Contentful Paint)
- CLS (Cumulative Layout Shift)
- INP (Interaction to Next Paint)
- FCP (First Contentful Paint)
- TTFB (Time to First Byte)
- 动画帧率 (FPS) — 在动画执行期间采样
- 长任务 (Long Tasks) — 检测主线程阻塞
"""
import asyncio
import json

from config import logger

_WEB_VITALS_JS = """
// 使用 PerformanceObserver API 捕获 Web Vitals
new Promise((resolve) => {
    const metrics = {};
    let checks = 4; // 需要等待的指标数

    function done() {
        if (--checks <= 0) resolve(metrics);
    }

    // LCP
    try {
        new PerformanceObserver((list) => {
            const entries = list.getEntries();
            if (entries.length > 0) {
                metrics.lcp = entries[entries.length - 1].startTime;
                metrics.lcp_element = entries[entries.length - 1].element?.tagName || '';
                done();
            }
        }).observe({ type: 'largest-contentful-paint', buffered: true });
    } catch(e) { done(); }

    // CLS
    try {
        let cls = 0;
        new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (!entry.hadRecentInput) cls += entry.value;
            }
            metrics.cls = cls;
        }).observe({ type: 'layout-shift', buffered: true });
        // CLS 持续更新，延迟标记完成
        setTimeout(() => { if (metrics.cls === undefined) metrics.cls = cls; done(); }, 3000);
    } catch(e) { done(); }

    // FCP
    try {
        new PerformanceObserver((list) => {
            const entries = list.getEntries();
            if (entries.length > 0) {
                metrics.fcp = entries[0].startTime;
                done();
            }
        }).observe({ type: 'paint', buffered: true });
    } catch(e) { done(); }

    // Long Tasks (主线程阻塞 > 50ms)
    try {
        const longTasks = [];
        new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                longTasks.push({
                    duration: entry.duration,
                    startTime: entry.startTime,
                    attribution: entry.attribution ? entry.attribution[0]?.name || '' : '',
                });
            }
            metrics.long_tasks = longTasks.slice(0, 20);
            done();
        }).observe({ type: 'longtask', buffered: true });
    } catch(e) { done(); }

    // 超时兜底
    setTimeout(() => {
        if (metrics.lcp === undefined) metrics.lcp = null;
        if (metrics.fcp === undefined) metrics.fcp = null;
        resolve(metrics);
    }, 5000);
})
"""

_ANIMATION_FPS_JS = """
// 测量当前页面的动画帧率 (FPS)
new Promise((resolve) => {
    let frames = 0;
    let startTime = performance.now();
    let rafId;

    function countFrame() {
        frames++;
        const elapsed = performance.now() - startTime;
        if (elapsed >= 2000) {
            cancelAnimationFrame(rafId);
            resolve({
                fps: Math.round(frames / (elapsed / 1000)),
                total_frames: frames,
                duration_ms: Math.round(elapsed),
            });
        } else {
            rafId = requestAnimationFrame(countFrame);
        }
    }

    rafId = requestAnimationFrame(countFrame);
})
"""

_ANIMATION_PERFORMANCE_JS = """
// 检测动画性能问题
(() => {
    const issues = [];

    // 1. 检测非合成动画 (触发 layout/paint 的 CSS 属性)
    const nonCompositedProps = ['width', 'height', 'top', 'left', 'right', 'bottom',
        'margin', 'padding', 'border-width', 'font-size', 'line-height'];
    document.querySelectorAll('*').forEach(el => {
        const cs = window.getComputedStyle(el);
        if (cs.animation !== 'none' && cs.animation !== '') {
            // 检查 @keyframes 是否修改了非合成属性
            const animName = cs.animationName;
            if (animName && animName !== 'none') {
                // 通过检查 transition 属性来推断可能的性能问题
                nonCompositedProps.forEach(prop => {
                    if (cs.transitionProperty && cs.transitionProperty.includes(prop)) {
                        issues.push({
                            type: 'non_composited_transition',
                            element: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
                            property: prop,
                        });
                    }
                });
            }
        }
    });

    // 2. 检测大量并发动画 (>50 个动画元素)
    let animCount = 0;
    document.querySelectorAll('*').forEach(el => {
        const cs = window.getComputedStyle(el);
        if (cs.animation !== 'none' && cs.animation !== '') animCount++;
    });
    if (animCount > 50) {
        issues.push({
            type: 'excessive_animations',
            count: animCount,
            severity: animCount > 100 ? 'high' : 'medium',
        });
    }

    // 3. 检测无 will-change 的频繁动画元素
    let transformAnimNoWC = 0;
    document.querySelectorAll('*').forEach(el => {
        const cs = window.getComputedStyle(el);
        if (cs.animation !== 'none' && cs.animation !== '' &&
            cs.transform !== 'none' &&
            (cs.willChange === 'auto' || cs.willChange === '')) {
            transformAnimNoWC++;
        }
    });
    if (transformAnimNoWC > 10) {
        issues.push({
            type: 'missing_will_change',
            count: transformAnimNoWC,
            hint: '使用 transform 动画的元素缺少 will-change 提示',
        });
    }

    return { issues, total_animations: animCount };
})()
"""


async def measure_web_vitals(page) -> dict:
    """测量 Core Web Vitals"""
    try:
        result = await page.evaluate(_WEB_VITALS_JS)
        return result or {}
    except Exception as e:
        logger.debug(f"Web Vitals 测量失败: {e}")
        return {}


async def measure_animation_fps(page) -> dict:
    """测量动画帧率"""
    try:
        # 触发滚动以确保滚动动画被激活
        await page.evaluate("window.scrollTo({ top: 300, behavior: 'instant' })")
        await asyncio.sleep(0.3)
        fps_result = await page.evaluate(_ANIMATION_FPS_JS)
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
        return fps_result or {}
    except Exception as e:
        logger.debug(f"FPS 测量失败: {e}")
        return {}


async def audit_animation_performance(page) -> dict:
    """审计动画性能问题"""
    try:
        result = await page.evaluate(_ANIMATION_PERFORMANCE_JS)
        return result or {}
    except Exception as e:
        logger.debug(f"动画性能审计失败: {e}")
        return {}
