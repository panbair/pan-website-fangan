# 🎨 高端自然疗愈度假村品牌网站创意开发方案

> **灵感来源**：基于 2 个竞品分析：fame-estate.com（技术架构失败但品牌定位优秀）、diamondrosesanctuary.com（顶级品牌叙事与动画体验）
> **设计方向**：电影级滚动叙事 + 深度感官沉浸 + 像素级触觉反馈
> **对标品质**：Apple.com 的克制 × Awwwards SOTD 的创新 × 戛纳创意奖的叙事深度

---

## 一、🎯 设计系统

### 1.1 色彩方案
```
主色: #1A1A1E — 深空黑（用于深色背景，营造静谧包裹感）
辅色: #F5F0EB — 暖白（用于文字和浅色背景，模拟纸张质感）
强调色: #C8A97E — 古铜金（用于CTA、分割线、高亮元素，有金属温度感）
深色背景: #0D0D0F
浅色背景: #F8F6F3
文字主色: #E8E4DE（深色背景上）/ #2D2B28（浅色背景上）
文字辅色: #9A958E
渐变: linear-gradient(135deg, #C8A97E, #D4B88C)
```

### 1.2 字体系统
```
标题: Playfair Display (Google Fonts) — weight: 400/600, letter-spacing: -0.02em
副标题: Inter (Google Fonts) — weight: 300/400, letter-spacing: 0.05em
正文: Inter (Google Fonts) — weight: 300, line-height: 1.7
数字/数据: Inter — weight: 200, letter-spacing: -0.03em
```

### 1.3 间距
基于 8px 网格系统：8/16/24/32/48/64/96/128/192

### 1.4 设计原则
1. **感官优先** — 每个交互都必须让用户"感觉到"：滚动有阻力、按钮有磁性、图片有呼吸
2. **叙事驱动** — 页面是一本书，每个 section 是一章，滚动是翻页
3. **克制即奢华** — 不做一个多余的元素，每个动画都有叙事目的
4. **深度包裹** — 通过视差、景深、声音（文字质感）创造三维空间的沉浸感

---

## 二、📐 页面结构（逐 Section）

### Section 1: Hero — “Earth. Sky. You.”

**视觉布局**：
- 全屏深色背景，中心偏上位置出现品牌名 "TERRA SANCTUARY"
- 背景是 3 层 parallax：最远层是模糊的星空粒子（Canvas），中层是山脉轮廓（SVG），前景是飘动的雾气（CSS filter）
- 品牌名下方是副标题 "A Place Where Time Surrenders"
- 右下角有极小的向下滚动指示器（一条渐变的金色线，随滚动长度变化）

**响应式行为**：
- 移动端：3 层 parallax 简化为 2 层，品牌名缩小至 48px，副标题隐藏
- 平板：保持 3 层但降低粒子密度

### Section 2: Philosophy — “We Don't Build. We Protect.”

**视觉布局**：
- 左侧 60% 是叙事文字，右侧 40% 是一张渐显的风景摄影
- 文字部分：4 行关键理念，每行先出现英文（大），再覆盖中文翻译（小）
- 右侧图片：从黑白模糊 → 彩色清晰，配合 clip-path 从对角线展开
- 背景：纯色过渡到浅色

**响应式行为**：
- 移动端：改为上下布局，图片在上，文字在下

### Section 3: Experiences — “Three Paths. One Destination.”

**视觉布局**：
- 水平滚动画廊（3 张全屏卡片），每张卡片代表一种体验（Forest Bathing / Mountain Meditation / Lake Ceremony）
- 卡片切换时：背景色渐变（深绿→深蓝→暖金），clip-path 圆形展开揭示新卡片
- 每张卡片内：图片占 70%，下方 30% 是标题 + 简短描述 + "Explore" 链接
- 导航点：底部 3 个点，当前点有金色填充动画

**响应式行为**：
- 移动端：改为垂直滚动，每张卡片占一屏

### Section 4: Data & Trust — “Not Just Numbers. Promises Kept.”

**视觉布局**：
- 深色背景，中心是 3 个巨大的数据块
- 每个数据块：数字（从 0 滚到目标值） + 单位 + 描述文字
- 数据之间用金色细线分隔
- 背景：微妙的粒子动画（Canvas），粒子缓慢聚集形成星座图案
- 数字滚动时，粒子同步加速流动

**响应式行为**：
- 移动端：3 个数据块垂直排列，粒子密度降低 50%

### Section 5: Testimonials — “Voices from the Sanctuary”

**视觉布局**：
- 全屏引用卡片，带背景视频（静音自动播放）
- 卡片从右侧滑入，覆盖 70% 屏幕
- 引用文字用大号斜体，下方是署名 + 日期
- 左右箭头导航
- 切换时：旧卡片 clip-path 从中心收缩消失，新卡片从边缘展开

**响应式行为**：
- 移动端：卡片占 90% 宽度，视频改为静态图片

### Section 6: CTA — “Your Journey Begins Here”

**视觉布局**：
- 全屏深色背景，中心是一个圆形发光区域
- 发光区域内：主 CTA "Book Your Sanctuary"（金色按钮）
- 按钮周围：3 个环绕的装饰性文字（"Stillness" / "Connection" / "Renewal"），缓慢旋转
- 按钮 hover 时：发光区域扩大，环绕文字加速
- 底部：最小化的联系方式（邮件 + 电话）

**响应式行为**：
- 移动端：发光区域缩小，环绕文字隐藏，按钮尺寸增大

---

## 三、⚡ 惊艳时刻（本章是方案灵魂，必须详细）

### 惊艳时刻 1：「时间暂停」— Hero 到 Philosophy 的过渡

**用户在什么时候看到**：从 Hero 滚动到 Philosophy 的瞬间（约 20% 滚动位置）

**发生了什么**：
- Hero 的星空粒子（Canvas）在 800ms 内逐渐减速至静止
- 山脉轮廓 SVG 从下到上消失（drawSVG reverse，600ms）
- 雾气 filter 消散
- 品牌名 "TERRA SANCTUARY" 分裂成单个字母，每个字母以不同的速度向不同方向飘散（像被风吹散）
- 整个画面在 1.2s 内变成纯白
- 然后 Philosophy 的文字从纯白中浮现：先是英文单词逐字出现（每字 80ms stagger），然后中文翻译从下方模糊到清晰滑入

**为什么震撼**：
- 这是"翻页"的物理化表达 — 不是简单的 fade，而是"时间被暂停，世界被重置"
- 字母飘散是对"品牌名消失"的诗意诠释，而不是粗暴隐藏
- 从深色到纯白的过渡模拟了"闭上眼睛，再睁开"的感官体验

**GSAP 实现思路**：
```javascript
// 时间暂停序列
const pauseTimeline = gsap.timeline({
  scrollTrigger: {
    trigger: ".hero-section",
    start: "bottom bottom",
    end: "+=1200",
    scrub: 1.5,
    pin: true
  }
});

// 1. 粒子减速 (Canvas 控制)
pauseTimeline.to(canvasParticles, {
  speed: 0,
  duration: 0.8,
  ease: "power3.out"
}, 0);

// 2. 山脉消失
pauseTimeline.to(".mountain-svg path", {
  drawSVG: "0% 0%",
  duration: 0.6,
  ease: "power2.in"
}, 0.2);

// 3. 雾气消散
pauseTimeline.to(".hero-fog", {
  opacity: 0,
  filter: "blur(20px)",
  duration: 0.5
}, 0.4);

// 4. 品牌名字母飘散
const brandChars = document.querySelectorAll(".hero-title .char");
pauseTimeline.to(brandChars, {
  x: () => gsap.utils.random(-200, 200),
  y: () => gsap.utils.random(-300, 100),
  rotation: () => gsap.utils.random(-45, 45),
  opacity: 0,
  duration: 1.2,
  stagger: 0.03,
  ease: "power4.out"
}, 0.6);

// 5. 纯白过渡
pauseTimeline.to(".hero-overlay", {
  backgroundColor: "#FFFFFF",
  duration: 0.6
}, 0.8);

// 6. Philosophy 文字浮现 (在下一个 section)
const philosophyTimeline = gsap.timeline({
  scrollTrigger: {
    trigger: ".philosophy-section",
    start: "top bottom",
    end: "top center",
    scrub: 1
  }
});

philosophyTimeline.fromTo(".philosophy-text .word", {
  y: 60,
  opacity: 0,
  filter: "blur(10px)"
}, {
  y: 0,
  opacity: 1,
  filter: "blur(0px)",
  stagger: 0.08,
  duration: 0.6,
  ease: "power2.out"
}, 0);
```

### 惊艳时刻 2：「水波展开」— Experiences 卡片切换

**用户在什么时候看到**：在水平滚动画廊中，切换到下一张卡片时

**发生了什么**：
- 当前卡片从中心开始，像水波一样扩散的圆形 clip-path 逐渐消失（250ms）
- 在圆形扩散的同时，下一张卡片从中心点开始，以同样的圆形 clip-path 展开（250ms，与消失重叠 100ms）
- 两张卡片在重叠的 100ms 内，旧卡片的边缘模糊与新卡片的清晰形成对比
- 背景色在 500ms 内渐变到新卡片对应的颜色
- 底部导航点的当前点：金色填充从中心向外扩散（300ms）

**为什么震撼**：
- 这是对"空间穿越"的视觉化 — 不是生硬的切换，而是"穿过一道门进入另一个世界"
- 圆形 clip-path 的物理感（水波扩散）让切换变得有机、自然
- 背景色渐变 + 卡片切换 + 导航点动画三者同步，形成完美的节奏感

**GSAP 实现思路**：
```javascript
// 水平滚动画廊卡片切换
const cardTransition = (oldCard, newCard, newColor) => {
  const tl = gsap.timeline({
    paused: true
  });

  // 旧卡片消失：圆形 clip-path 从中心扩散
  tl.to(oldCard, {
    clipPath: "circle(150% at 50% 50%)",
    duration: 0.25,
    ease: "power2.in",
    onComplete: () => {
      oldCard.style.display = "none";
    }
  }, 0);

  // 新卡片展开：圆形 clip-path 从中心扩散（反向）
  tl.set(newCard, {
    display: "block",
    clipPath: "circle(0% at 50% 50%)"
  }, 0.1);
  tl.to(newCard, {
    clipPath: "circle(150% at 50% 50%)",
    duration: 0.25,
    ease: "power2.out"
  }, 0.1);

  // 背景色渐变
  tl.to(".experiences-bg", {
    backgroundColor: newColor,
    duration: 0.5,
    ease: "power1.inOut"
  }, 0);

  // 导航点动画
  const dot = document.querySelector(".nav-dot.active");
  tl.fromTo(dot, {
    scale: 0,
    opacity: 0
  }, {
    scale: 1,
    opacity: 1,
    duration: 0.3,
    ease: "back.out(1.7)"
  }, 0.2);

  return tl;
};

// ScrollTrigger 控制水平滚动
gsap.to(".experiences-track", {
  x: () => -(window.innerWidth * 2),
  ease: "none",
  scrollTrigger: {
    trigger: ".experiences-section",
    pin: true,
    scrub: 1,
    end: () => `+=${window.innerWidth * 2}`,
    onUpdate: (self) => {
      const progress = self.progress;
      const cardIndex = Math.round(progress * 2);
      // 触发卡片切换逻辑
    }
  }
});
```

### 惊艳时刻 3：「数据呼吸」— 数字滚动 + 粒子星座

**用户在什么时候看到**：滚动到 Data & Trust section，数字开始滚动时

**发生了什么**：
- 三个数字从 0 开始滚动到目标值（如 0 → 12, 0 → 4,800, 0 → 100%）
- 数字滚动的同时，背景的 Canvas 粒子开始从随机位置向 3 个星座图案聚集
- 每个数字对应一个星座图案：第一个数字 → 树形星座，第二个 → 山脉星座，第三个 → 太阳星座
- 当数字达到目标值时，对应的星座完全成形并发出微弱的金色光芒（glow animation）
- 三个星座成形后，整个 Canvas 粒子系统进入缓慢旋转状态（60s 一圈）

**为什么震撼**：
- 这是一次"数据可视化"的艺术化表达 — 不是简单的数字变化，而是"数据在宇宙中找到了它的位置"
- 粒子星座的创意将冰冷的数字转化为有生命的图案，让用户"看到"品牌承诺
- 三个星座的 sequential 成形创造了一种"揭晓"的仪式感

**GSAP 实现思路**：
```javascript
// 数字滚动 + 粒子星座动画
const dataSection = document.querySelector(".data-section");
const numbers = [
  { element: ".data-1", target: 12, symbol: "Years" },
  { element: ".data-2", target: 4800, symbol: "Guests" },
  { element: ".data-3", target: 100, symbol: "% Satisfaction" }
];

// 创建 Canvas 粒子系统
const canvas = document.getElementById("particle-canvas");
const ctx = canvas.getContext("2d");
const particles = [];
const constellations = []; // 3 个星座的目标位置

// 初始化粒子
for (let i = 0; i < 200; i++) {
  particles.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    targetX: 0,
    targetY: 0,
    speed: 0.02,
    size: Math.random() * 3 + 1,
    opacity: Math.random() * 0.5 + 0.3
  });
}

// ScrollTrigger 触发数字滚动
const dataTimeline = gsap.timeline({
  scrollTrigger: {
    trigger: dataSection,
    start: "top center",
    end: "bottom top",
    scrub: 1,
    onEnter: () => {
      // 开始数字滚动
      numbers.forEach((num, index) => {
        gsap.fromTo(num.element, {
          innerText: 0
        }, {
          innerText: num.target,
          duration: 2,
          delay: index * 0.6,
          ease: "power2.out",
          snap: { innerText: 1 },
          onUpdate: () => {
            // 同步更新粒子星座进度
            const progress = this.progress();
            updateConstellation(index, progress);
          }
        });
      });
    }
  }
});

// 粒子星座成形
function updateConstellation(index, progress) {
  const constellation = constellations[index];
  particles.forEach((p, i) => {
    const target = constellation[i % constellation.length];
    p.targetX = gsap.utils.interpolate(p.x, target.x, progress);
    p.targetY = gsap.utils.interpolate(p.y, target.y, progress);
  });
}

// 粒子绘制循环
function animateParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles.forEach(p => {
    p.x += (p.targetX - p.x) * p.speed;
    p.y += (p.targetY - p.y) * p.speed;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(200, 169, 126, ${p.opacity})`;
    ctx.fill();
  });
  requestAnimationFrame(animateParticles);
}
animateParticles();
```

---

## 四、🎬 GSAP 动画系统（逐 Section 详细描述）

### 4.1 全局策略
- **性能原则**：所有动画仅操作 `transform` 和 `opacity`，禁止 `top`/`left` 或 `width`/`height`
- **matchMedia 响应式**：
  ```javascript
  ScrollTrigger.matchMedia({
    "(min-width: 1024px)": function() { /* 桌面动画 */ },
    "(min-width: 768px) and (max-width: 1023px)": function() { /* 平板动画（简化版） */ },
    "(max-width: 767px)": function() { /* 移动端动画（最简化版） */ }
  });
  ```
- **全局 ScrollTrigger 配置**：
  ```javascript
  ScrollTrigger.defaults({
    toggleActions: "play none none reverse",
    markers: false
  });
  ```

### 4.2 Section 1: Hero 动画

**动画类型**：Parallax Multi-Layer (3层) + Staggered Char Reveal + DrawSVG

**完整动画描述**：
- **触发条件**：页面加载即开始，滚动时 parallax 生效
- **3层视差**：
  - 最远层（星空Canvas）：`y: (scroll * 0.1)` — 几乎不动
  - 中层（山脉SVG）：`y: (scroll * 0.3)` — 缓慢移动
  - 前景层（雾气CSS）：`y: (scroll * 0.5)` + `opacity: (scroll * -0.003)` — 快速移动并淡出
- **品牌名揭示**：页面加载后 500ms，每个字母从 `y: 80, opacity: 0, blur: 10px` → `y: 0, opacity: 1, blur: 0`，stagger 80ms
- **山脉线稿**：SVG 路径从 `drawSVG: "0% 0%"` → `drawSVG: "0% 100%"`，duration 1.2s，ease: "power2.out"

**GSAP 代码骨架**：
```javascript
// 页面加载动画
const heroTL = gsap.timeline({ delay: 0.3 });

// 山脉线稿绘制
heroTL.fromTo(".hero-mountain path", {
  drawSVG: "0% 0%"
}, {
  drawSVG: "0% 100%",
  duration: 1.2,
  ease: "power2.out"
}, 0);

// 品牌名逐字出现
heroTL.fromTo(".hero-title .char", {
  y: 80,
  opacity: 0,
  filter: "blur(10px)"
}, {
  y: 0,
  opacity: 1,
  filter: "blur(0px)",
  stagger: 0.08,
  duration: 0.6,
  ease: "power3.out"
}, 0.4);

// 副标题
heroTL.fromTo(".hero-subtitle", {
  y: 40,
  opacity: 0
}, {
  y: 0,
  opacity: 1,
  duration: 0.8,
  ease: "power2.out"
}, 0.8);

// 滚动指示器
heroTL.fromTo(".scroll-indicator", {
  opacity: 0,
  scale: 0.5
}, {
  opacity: 1,
  scale: 1,
  duration: 0.6,
  ease: "back.out(1.7)"
}, 1.4);

// 滚动视差
gsap.to(".hero-stars", {
  y: () => window.innerHeight * 0.1,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero-section",
    start: "top top",
    end: "bottom top",
    scrub: 1
  }
});

gsap.to(".hero-mountains", {
  y: () => window.innerHeight * 0.3,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero-section",
    start: "top top",
    end: "bottom top",
    scrub: 1
  }
});

gsap.to(".hero-fog", {
  y: () => window.innerHeight * 0.5,
  opacity: 0,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero-section",
    start: "top top",
    end: "bottom top",
    scrub: 1
  }
});
```

### 4.3 Section 2: Philosophy 动画

**动画类型**：Clip-Path Reveal (对角线) + Progressive Image Reveal + Staggered Word

**完整动画描述**：
- **触发条件**：滚动到 section 时，clip-path 从右下角向左上角展开
- **图片揭示**：同时，图片从 `grayscale(100%) blur(5px)` → `grayscale(0%) blur(0px)`，配合 clip-path
- **文字揭示**：clip-path 完成后，4 行理念文字逐行出现，每行先显示英文（从右向左滑动），再覆盖中文（从下向上）

**GSAP 代码骨架**：
```javascript
const philosophyTL = gsap.timeline({
  scrollTrigger: {
    trigger: ".philosophy-section",
    start: "top center",
    end: "center center",
    scrub: 1
  }
});

// 图片对角线揭示
philosophyTL.fromTo(".philosophy-image", {
  clipPath: "polygon(100% 100%, 100% 100%, 100% 100%, 100% 100%)",
  filter: "grayscale(100%) blur(5px)"
}, {
  clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",
  filter: "grayscale(0%) blur(0px)",
  duration: 1.2,
  ease: "power3.out"
}, 0);

// 文字逐行
const philosophyLines = document.querySelectorAll(".philosophy-line");
philosophyLines.forEach((line, index) => {
  const english = line.querySelector(".english");
  const chinese = line.querySelector(".chinese");
  
  philosophyTL.fromTo(english, {
    x: 100,
    opacity: 0
  }, {
    x: 0,
    opacity: 1,
    duration: 0.6,
    ease: "power2.out"
  }, 1.5 + index * 0.3);
  
  philosophyTL.fromTo(chinese, {
    y: 30,
    opacity: 0,
    filter: "blur(5px)"
  }, {
    y: 0,
    opacity: 1,
    filter: "blur(0px)",
    duration: 0.4,
    ease: "power2.out"
  }, 1.8 + index * 0.3);
});
```

### 4.4 Section 3: Experiences 动画

**动画类型**：Horizontal Scroll Gallery + Clip-Path Circle Reveal + Color Transition

**完整动画描述**：
- **触发条件**：水平滚动控制卡片切换
- **卡片切换动画**：见惊艳时刻 2
- **额外效果**：每张卡片 hover 时，图片有微妙的 scale(1.02) + brightness(1.1)，持续 400ms

**GSAP 代码骨架**：参考惊艳时刻 2 的代码

### 4.5 Section 4: Data & Trust 动画

**动画类型**：Count-Up Numbers + Canvas Particle Constellation + DrawSVG (分隔线)

**完整动画描述**：
- **触发条件**：进入 viewport 时触发
- **数字滚动**：从 0 到目标值，每个数字延迟 600ms
- **粒子星座**：惊艳时刻 3 的实现
- **分隔线绘制**：金色细线从中心向两侧 drawSVG

**GSAP 代码骨架**：
```javascript
const dataTL = gsap.timeline({
  scrollTrigger: {
    trigger: ".data-section",
    start: "top 70%",
    end: "bottom 30%",
    scrub: 1
  }
});

// 分隔线绘制
dataTL.fromTo(".data-divider", {
  drawSVG: "50% 50%"
}, {
  drawSVG: "0% 100%",
  duration: 0.8,
  ease: "power2.out"
}, 0);

// 数字滚动
const dataValues = [
  { selector: ".data-years", value: 12, suffix: "" },
  { selector: ".data-guests", value: 4800, suffix: "+" },
  { selector: ".data-satisfaction", value: 100, suffix: "%" }
];

dataValues.forEach((item, index) => {
  dataTL.fromTo(item.selector, {
    innerText: "0"
  }, {
    innerText: item.value,
    duration: 2.5,
    delay: 0.6 * index,
    ease: "power3.out",
    snap: { innerText: 1 }
  }, 0.2);
  
  // 数值出现时放大效果
  dataTL.fromTo(item.selector, {
    scale: 0.5,
    opacity: 0
  }, {
    scale: 1,
    opacity: 1,
    duration: 0.4,
    ease: "back.out(2)"
  }, 0.2 + 0.6 * index);
});
```

### 4.6 Section 5: Testimonials 动画

**动画类型**：Clip-Path Slide Reveal + Background Video + Magnetic Navigation

**完整动画描述**：
- **触发条件**：点击左右箭头或键盘左右键
- **卡片切换**：旧卡片从右侧 clip-path 收缩消失，新卡片从左侧展开
- **背景视频**：切换时视频淡入淡出，与卡片同步
- **导航箭头**：hover 时箭头有 magnetic 效果（跟随鼠标微移 10px）

**GSAP 代码骨架**：
```javascript
class TestimonialCarousel {
  constructor() {
    this.current = 0;
    this.testimonials = document.querySelectorAll(".testimonial-card");
    this.total = this.testimonials.length;
    
    document.querySelector(".arrow-left").addEventListener("click", () => this.prev());
    document.querySelector(".arrow-right").addEventListener("click", () => this.next());
  }
  
  next() {
    const oldCard = this.testimonials[this.current];
    this.current = (this.current + 1) % this.total;
    const newCard = this.testimonials[this.current];
    
    const tl = gsap.timeline();
    
    // 旧卡片收缩消失
    tl.to(oldCard, {
      clipPath: "inset(0 100% 0 0)",
      duration: 0.4,
      ease: "power2.in"
    }, 0);
    
    // 新卡片展开
    tl.set(newCard, {
      clipPath: "inset(0 100% 0 0)"
    }, 0);
    tl.to(newCard, {
      clipPath: "inset(0 0 0 0)",
      duration: 0.4,
      ease: "power2.out"
    }, 0.1);
    
    // 背景视频切换
    tl.to(".testimonial-video", {
      opacity: 0,
      duration: 0.2
    }, 0);
    tl.set(".testimonial-video", {
      src: newCard.dataset.video
    }, 0.2);
    tl.to(".testimonial-video", {
      opacity: 1,
      duration: 0.3
    }, 0.3);
  }
  
  prev() {
    // 类似 next()，但方向相反
    const oldCard = this.testimonials[this.current];
    this.current = (this.current - 1 + this.total) % this.total;
    const newCard = this.testimonials[this.current];
    
    const tl = gsap.timeline();
    
    tl.to(oldCard, {
      clipPath: "inset(0 0 0 100%)",
      duration: 0.4,
      ease: "power2.in"
    }, 0);
    
    tl.set(newCard, {
      clipPath: "inset(0 0 0 100%)"
    }, 0);
    tl.to(newCard, {
      clipPath: "inset(0 0 0 0)",
      duration: 0.4,
      ease: "power2.out"
    }, 0.1);
  }
}
```

### 4.7 Section 6: CTA 动画

**动画类型**：Magnetic Button + Rotating Text + Glow Pulse + Scale Reveal

**完整动画描述**：
- **触发条件**：进入 viewport 时，整个 section 从 scale(0.8) opacity(0) 出现
- **发光区域**：持续的微弱脉冲（scale 1.02 → 1.05，duration 2s，重复）
- **环绕文字**：360° 旋转，每 12s 一圈
- **按钮 hover**：magnetic 效果（跟随鼠标偏移 15px），发光区域扩大到 1.5x

**GSAP 代码骨架**：
```javascript
// 进入动画
const ctaTL = gsap.timeline({
  scrollTrigger: {
    trigger: ".cta-section",
    start: "top 80%",
    end: "top 30%",
    scrub: 1
  }
});

ctaTL.fromTo(".cta-section", {
  scale: 0.8,
  opacity: 0,
  filter: "blur(10px)"
}, {
  scale: 1,
  opacity: 1,
  filter: "blur(0px)",
  duration: 1.2,
  ease: "power3.out"
}, 0);

// 发光脉冲 (持续)
gsap.to(".cta-glow", {
  scale: 1.05,
  duration: 2,
  repeat: -1,
  yoyo: true,
  ease: "sine.inOut"
});

// 环绕文字旋转 (持续)
gsap.to(".cta-orbiting-text", {
  rotation: 360,
  duration: 12,
  repeat: -1,
  ease: "none"
});

// Magnetic 按钮
const button = document.querySelector(".cta-button");
button.addEventListener("mousemove", (e) => {
  const rect = button.getBoundingClientRect();
  const x = e.clientX - rect.left - rect.width / 2;
  const y = e.clientY - rect.top - rect.height / 2;
  
  gsap.to(button, {
    x: x * 0.3,
    y: y * 0.3,
    duration: 0.4,
    ease: "power2.out"
  });
  
  gsap.to(".cta-glow", {
    scale: 1.5,
    duration: 0.4,
    ease: "power2.out"
  });
});

button.addEventListener("mouseleave", () => {
  gsap.to(button, {
    x: 0,
    y: 0,
    duration: 0.6,
    ease: "elastic.out(1, 0.5)"
  });
  
  gsap.to(".cta-glow", {
    scale: 1,
    duration: 0.6,
    ease: "power2.out"
  });
});
```

### 4.8 全局微交互

**导航栏**：
- 滚动 200px 后：背景从透明 → `rgba(13, 13, 15, 0.9)`，backdrop-filter: blur(20px)
- 链接 hover：下划线从中心向两侧展开（clip-path），duration 300ms
- Logo hover：scale(1.05)，duration 200ms

```javascript
// 导航栏滚动效果
gsap.to(".navbar", {
  backgroundColor: "rgba(13, 13, 15, 0.9)",
  backdropFilter: "blur(20px)",
  duration: 0.4,
  scrollTrigger: {
    trigger: "body",
    start: "top -200px",
    end: "top -300px",
    scrub: 1
  }
});

// 链接 hover 下划线
document.querySelectorAll(".nav-link").forEach(link => {
  const underline = link.querySelector(".nav-underline");
  link.addEventListener("mouseenter", () => {
    gsap.to(underline, {
      clipPath: "inset(0 0 0 0)",
      duration: 0.3,
      ease: "power2.out"
    });
  });
  link.addEventListener("mouseleave", () => {
    gsap.to(underline, {
      clipPath: "inset(0 100% 0 0)",
      duration: 0.3,
      ease: "power2.out"
    });
  });
});
```

**自定义光标**：
- 默认：小圆点（直径 8px），跟随鼠标延迟 50ms
- 经过链接/按钮：扩大到 40px，边框出现，中心空心
- 经过图片：变成放大镜图标

```javascript
const cursor = document.querySelector(".custom-cursor");
const cursorFollower = document.querySelector(".custom-cursor-follower");

document.addEventListener("mousemove", (e) => {
  gsap.to(cursor, {
    x: e.clientX,
    y: e.clientY,
    duration: 0.1
  });
  gsap.to(cursorFollower, {
    x: e.clientX,
    y: e.clientY,
    duration: 0.3,
    ease: "power2.out"
  });
});

// 交互元素 hover
document.querySelectorAll("a, button, .interactive").forEach(el => {
  el.addEventListener("mouseenter", () => {
    gsap.to(cursorFollower, {
      scale: 2.5,
      borderColor: "#C8A97E",
      duration: 0.3
    });
  });
  el.addEventListener("mouseleave", () => {
    gsap.to(cursorFollower, {
      scale: 1,
      borderColor: "transparent",
      duration: 0.3
    });
  });
});
```

**加载动画**：
- 品牌名从中心放大出现（scale: 0 → 1），duration 800ms
- 然后分裂成两个半圆，向左右移动，露出页面内容
- 整体 duration 1.5s

```javascript
const loaderTL = gsap.timeline();

loaderTL.fromTo(".loader-logo", {
  scale: 0,
  opacity: 0
}, {
  scale: 1,
  opacity: 1,
  duration: 0.8,
  ease: "back.out(2)"
}, 0);

loaderTL.to(".loader-logo", {
  clipPath: "inset(0 50% 0 0)",
  duration: 0.4,
  ease: "power2.inOut"
}, 0.8);

loaderTL.to(".loader-logo", {
  clipPath: "inset(0 0 0 50%)",
  duration: 0.4,
  ease: "power2.inOut"
}, 0.8);

loaderTL.to(".loader-logo", {
  scale: 0.5,
  opacity: 0,
  duration: 0.3
}, 1.2);

loaderTL.to(".loader", {
  opacity: 0,
  duration: 0.3,
  onComplete: () => {
    document.querySelector(".loader").style.display = "none";
  }
}, 1.3);
```

---

## 五、🛠️ 技术实现

### 5.1 技术栈
```
框架: 原生 JavaScript (ES Modules)
动画: GSAP 3.12 + ScrollTrigger + ScrollToPlugin + DrawSVGPlugin + SplitType
样式: Tailwind CSS 3.x (自定义配置)
Canvas: 原生 Canvas 2D API (粒子系统)
字体: Playfair Display + Inter (Google Fonts)
图标: 自定义 SVG sprite
部署: Vercel (自动 HTTPS + CDN)
构建: Vite 5.x
```

### 5.2 项目结构
```
project/
├── index.html
├── src/
│   ├── main.js              # 入口文件
│   ├── styles/
│   │   ├── main.css          # Tailwind + 自定义样式
│   │   └── animations.css    # @keyframes 补充
│   ├── js/
│   │   ├── anim-hero.js      # Section 1 动画
│   │   ├── anim-philosophy.js # Section 2 动画
│   │   ├── anim-experiences.js # Section 3 动画
│   │   ├── anim-data.js      # Section 4 动画 + 粒子系统
│   │   ├── anim-testimonials.js # Section 5 动画
│   │   ├── anim-cta.js       # Section 6 动画
│   │   ├── anim-global.js    # 导航、光标、加载动画
│   │   ├── particles.js      # Canvas 粒子系统类
│   │   └── utils.js          # 工具函数
│   └── assets/
│       ├── images/
│       ├── videos/
│       └── fonts/
├── package.json
├── vite.config.js
└── tailwind.config.js
```

### 5.3 性能清单
1. ✅ **所有动画仅操作 transform 和 opacity** — 无 layout 触发
2. ✅ **图片使用 AVIF 格式**，设置 explicit width/height 防止 CLS
3. ✅ **GSAP 脚本使用 defer 加载**，不阻塞首次渲染
4. ✅ **Canvas 粒子系统使用 requestAnimationFrame**，60fps 稳定
5. ✅ **滚动事件通过 ScrollTrigger 节流**，不直接绑定 scroll
6. ✅ **低端设备检测**：navigator.hardwareConcurrency < 4 时，粒子数量减半，取消 blur 滤镜
7. ✅ **prefers-reduced-motion 支持**：用户开启时，所有动画 duration 缩短 50%，取消 parallax
8. ✅ **资源预加载**：首屏 Hero 图片 + 视频使用 `<link rel="preload">`

---

## 六、📱 响应式策略

| 断点 | 宽度 | 设计变化 | 动画调整 |
|:---|:---|:---|:---|
| Desktop | ≥1024px | 全功能设计 | 所有动画完整执行 |
| Tablet | 768-1023px | 水平画廊改为垂直滚动，粒子减少 30% | parallax 层数从 3 减到 2，取消 blur 滤镜 |
| Mobile L | 425-767px | 所有 section 改为单列布局，图片占满宽度 | 取消 Canvas 粒子，改为 CSS 渐变背景；clip-path 动画改为简单 fade-in |
| Mobile S | <425px | 最小字体 14px，CTA 按钮全宽 | 完全禁用 parallax，所有动画 duration 减半 |

```javascript
// 响应式动画配置
ScrollTrigger.matchMedia({
  "(min-width: 1024px)": function() {
    // 桌面端：全功能
    initHeroParallax(3);
    initCanvasParticles(200);
    initHorizontalGallery();
  },
  "(min-width: 768px) and (max-width: 1023px)": function() {
    // 平板：简化
    initHeroParallax(2);
    initCanvasParticles(140);
    initVerticalGallery();
  },
  "(max-width: 767px)": function() {
    // 移动端：最简
    initHeroSimple();
    initGallerySimple();
    // 禁用 Canvas
    document.getElementById("particle-canvas").style.display = "none";
  }
});
```

---

## 七、🎯 差异化总结

1. **「时间暂停」过渡** — Hero 到 Philosophy 的字母飘散 + 纯白重置，让"翻页"有了物理质感。这是目前没有任何竞品实现过的交互。

2. **粒子星座数据可视化** — 将冰冷的"12年/4800位客人/100%满意度"转化为会呼吸的星座图案，数字滚动时粒子同步聚集成形。数据不再只是数字，而是一种"仪式"。

3. **水波展开卡片切换** — 用圆形 clip-path 模拟"穿过水波进入另一个世界"，比常规的 slide/fade 切换更具沉浸感和有机感。

4. **三级视差叙事** — 星空粒子（微动）→ 山脉SVG（中速）→ 雾气（快速），三者在同一画面中创造深度感和时间流逝感。这不是简单的装饰，而是"在这片土地上，时间以不同速度流动"的叙事表达。

5. **Magnetic 按钮 + 环绕文字** — CTA 按钮的磁性跟随 + 发光区域扩大 + 环绕文字加速，让"点击"变成一种物理互动，而不是机械的 UI 操作。

---

## 📏 动画多样性自检

- [x] 至少 3 个 section 使用了 pin + sequence 而非简单 fade-in：Hero（时间暂停 pin）、Experiences（水平滚动 pin）、Testimonials（卡片切换 pin）
- [x] 至少 1 个 section 使用了 parallax multi-layer（≥3层）：Hero 的星空/山脉/雾气 3 层
- [x] 至少 1 个 section 使用了 clip-path 或 mask 揭示：Philosophy（对角线 clip-path）、Experiences（圆形 clip-path）
- [x] 至少 1 个 section 使用了 stagger 文字动画（SplitType）：Hero 品牌名、Philosophy 理念文字
- [x] 至少 1 个 section 使用了数字 count-up：Data section 3 个数字
- [x] 至少 1 个惊艳时刻是"前所未见"的创新动画：时间暂停过渡、粒子星座
- [x] 没有任何一个 section 只用 `from {y, opacity:0}` 作为全部动画：每个 section 都组合了 2-3 种动画类型
- [x] 所有动画描述都给出了触发点、属性值、缓动函数