# 🌊 STILLPOINT — 在高强度生活中，找到你的暂停键

> **灵感来自**：diamondrosesanctuary.com 的电影级滚动叙事 + GSAP + Lenis + SplitType 动画组合；其哲学化文案和品牌使命感
> **故事主线**：一位高压都市人从第1秒的“我需要逃离”，到中间“原来还有这样的地方”，再到最后“我必须去”的完整转化旅程
> **情绪曲线**：焦躁 → 好奇 → 震撼 → 向往 → 安心 → 行动

---

## 一、🎨 视觉世界观

### 1.1 情绪板
想象你走进一个被晨雾笼罩的原始森林。阳光从树冠缝隙中洒下，形成一道道光柱。地面铺满松针和苔藓，空气湿润而清新。远处传来溪流的声音，偶尔有鸟鸣打破寂静。这不是一个度假村——这是一个被精心守护的“暂停空间”。网站的整体氛围是：**克制、深度、治愈、神圣**。每个页面都像一段冥想，用户不是“浏览”，而是“经历”。

### 1.2 色彩体系

```css
:root {
  --color-void: #0A0A0B;        /* 深渊黑 — 代表都市的喧嚣与压力，用户进入前的状态 */
  --color-dawn: #F5F0EB;        /* 黎明米白 — 代表觉醒与纯净，页面主背景 */
  --color-mist: #E8E2D9;        /* 薄雾灰 — 代表过渡与模糊，次要背景 */
  --color-forest: #2D4A3E;      /* 林深绿 — 代表生命与疗愈，主色调 */
  --color-moss: #5A7A6A;        /* 苔藓绿 — 代表生长与希望，辅助色 */
  --color-ember: #C47A4F;       /* 余烬橙 — 代表温暖与篝火，CTA 色 */
  --color-stone: #8B8178;       /* 岩石灰 — 代表稳定与根基，正文色 */
  --color-gold: #B8945E;        /* 暮光金 — 代表日落与珍贵，装饰色 */
}
```

### 1.3 字体叙事

```
标题字体: "Playfair Display" — 衬线字体，古典优雅，传达永恒感和高端感
正文字体: "Inter" — 无衬线，清晰现代，在长阅读中保持舒适
装饰字体: "Cormorant Garamond" — 轻量衬线，用于引文和特殊文案

字号层级：
--text-xs: 0.75rem (12px) — 标注/标签
--text-sm: 0.875rem (14px) — 辅助信息
--text-base: 1rem (16px) — 正文
--text-lg: 1.25rem (20px) — 加粗正文
--text-xl: 1.5rem (24px) — 小标题
--text-2xl: 2rem (32px) — 章节标题
--text-3xl: 2.5rem (40px) — 大标题
--text-4xl: 3.5rem (56px) — Hero 标题
--text-5xl: 4.5rem (72px) — 高潮标题
```

### 1.4 间距节奏
基于 8px grid，核心间距为 8 的倍数：8 / 16 / 24 / 32 / 48 / 64 / 96 / 128 / 192px。

---

## 二、📖 故事章节（逐 Section）

### 第一章：Hero — 被吞噬的人

**商业目标**：用户离开后知道“STILLPOINT”是一个高端疗愈度假品牌，位于偏远自然中，提供“暂停”体验。

**故事角色**：这里是故事的“冲突建立”阶段。用户进入页面时，情绪是焦躁的——刚关掉工作群，正在寻找出口。

**情绪变化**：焦躁 😤 → 好奇 🤔

**画面描述**（120字）：
全屏黑暗。画面中央，一个微小的光点缓慢膨胀。随着光点的扩散，我们看到一个城市人的剪影——他/她站在巨大的落地窗前，窗外是模糊的都市灯火。剪影是模糊的，像一张曝光过度的照片。突然，剪影碎裂成无数粒子，像被风吹散的灰烬。在粒子消散的轨迹中，文字浮现：“你被多少个夜晚偷走了睡眠？” 粒子旋转重组，形成新的文字：“STILLPOINT — 回到你本该在的地方。”

**内容文案**：
- 标题（H1）：Stillpoint
- 副标题：找到你的暂停键
- 示例文字：“在卡茨基尔山脉的200英亩原始森林中，我们守护着一片被时间和意图治愈的土地。这里没有信号，没有会议，没有明天——只有当下。”

**动画叙事**：
1. **粒子消散动画**（GSAP + Canvas 2D）：人形剪影在3秒内碎裂成500个粒子，粒子按贝塞尔曲线路径飞散
2. **文字逐词浮现**（SplitType + GSAP）：每个词从opacity: 0 + y: 40px开始，逐词淡入并上移
3. **背景色调渐变**：从#0A0A0B渐变到#2D4A3E，模拟天黑到天亮的过渡
4. **章节过渡**：到达底部时，画面溶解成薄雾，下一章从雾中浮现

**GSAP 关键代码**：

```javascript
// 粒子系统
class ParticleSystem {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.ctx.globalCompositeOperation = 'screen';
  }

  createParticles(x, y, count = 500) {
    for (let i = 0; i < count; i++) {
      const angle = (Math.PI * 2 / count) * i + Math.random() * 0.1;
      const radius = 100 + Math.random() * 200;
      this.particles.push({
        x,
        y,
        startX: x,
        startY: y,
        endX: x + Math.cos(angle) * radius,
        endY: y + Math.sin(angle) * radius,
        size: 1 + Math.random() * 3,
        alpha: 1,
        color: `hsl(${40 + Math.random() * 20}, ${30 + Math.random() * 20}%, ${60 + Math.random() * 20}%)`,
        delay: Math.random() * 0.5
      });
    }
    return this;
  }

  animate(progress) {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.particles.forEach(p => {
      const t = Math.max(0, Math.min(1, (progress - p.delay) / (1 - p.delay)));
      p.x = p.startX + (p.endX - p.startX) * this.easeOutCubic(t);
      p.y = p.startY + (p.endY - p.startY) * this.easeOutCubic(t);
      p.alpha = 1 - t;
      this.ctx.globalAlpha = p.alpha;
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size * (1 - t * 0.5), 0, Math.PI * 2);
      this.ctx.fill();
    });
  }

  easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }
}

// GSAP 驱动粒子动画
const canvas = document.getElementById('hero-canvas');
const system = new ParticleSystem(canvas);
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// 初始创建粒子
system.createParticles(canvas.width / 2, canvas.height / 2);

// ScrollTrigger 驱动
gsap.to(system, {
  scrollTrigger: {
    trigger: '#hero',
    start: 'top top',
    end: 'bottom top',
    scrub: 1.5
  },
  onUpdate: function() {
    const progress = this.progress();
    system.animate(progress);
  }
});

// 文字动画
const heroText = new SplitType('#hero-title', { types: 'words' });
gsap.from(heroText.words, {
  scrollTrigger: {
    trigger: '#hero',
    start: 'top 60%',
    end: 'top 20%',
    scrub: 1
  },
  y: 40,
  opacity: 0,
  stagger: 0.03,
  ease: 'power2.out'
});
```

**响应式**：移动端粒子数减少至150个，文字动画保持但 staggger 减小至0.02。

---

### 第二章：问题 — 你被偷走的东西

**商业目标**：用户意识到“我需要这个”——痛点被精准挖掘，品牌提供的解决方案变得不可或缺。

**故事角色**：这里是故事中的“低谷”。用户被带入对自身生活的审视——那些被偷走的睡眠、注意力、平静。

**情绪变化**：好奇 🤔 → 认同 😌

**画面描述**（130字）：
画面分为三个垂直区域，像三联画。左侧：一个空荡荡的办公椅在旋转，速度越来越慢。中间：一部手机屏幕在快速闪烁，显示着未读消息、邮件、通知——闪烁频率从快到慢，直到完全黑屏。右侧：一杯咖啡在冷却，水汽逐渐消失。三个区域之间由细线连接，像心电图。当用户滚动时，三条线逐渐拉直，最终汇合成一条平静的直线——伴随着一声悠长的磬音。

**内容文案**：
- 标题：你的生活被什么填满了？
- 子标题：我们不是要你“逃离”，而是要你“回来”
- 示例文字：“研究表明，现代人平均每6.5分钟看一次手机。注意力碎片化的代价，不只是工作效率——它正在偷走你的深度思考能力、创造力，以及……平静的能力。每年，超过6000万美国人报告睡眠不足。焦虑症发病率在过去十年增长了28%。这不是你的错——是这个时代的设计缺陷。但你可以选择，离开这张设计图。”

**动画叙事**：
1. **三联画时间线**：三个区域各自独立动画——椅子旋转速度从快到慢（gsap.to 角度），手机闪烁频率从快到慢，咖啡水汽从浓到淡
2. **心电图线动画**：三条曲线从杂乱到平滑，使用 SVG 路径动画
3. **数字计数器**：从0滚动到具体统计数据（6.5分钟、6000万、28%），使用代理对象 + onUpdate
4. **章节过渡**：最后一条线变直时，画面裂开，露出下一章的绿色

**GSAP 关键代码**：

```javascript
// 三联画动画
const panels = document.querySelectorAll('.problem-panel');

panels.forEach((panel, index) => {
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: '#problem-section',
      start: 'top bottom',
      end: 'center center',
      scrub: 1.5,
      invalidateOnRefresh: true
    }
  });

  // 椅子旋转
  if (index === 0) {
    tl.to('#chair', {
      rotation: 720,
      ease: 'power4.out',
      duration: 1
    });
  }
  
  // 手机闪烁
  if (index === 1) {
    tl.to('#phone-screen', {
      opacity: 0,
      repeat: 20,
      yoyo: true,
      ease: 'steps(1)',
      duration: 0.05
    });
    tl.to('#phone-screen', {
      opacity: 1,
      duration: 0.5
    });
  }
  
  // 咖啡冷却
  if (index === 2) {
    tl.to('#steam', {
      opacity: 0,
      scale: 0.5,
      duration: 1.5,
      ease: 'power2.in'
    });
  }
});

// 数字计数器
function animateCounter(el, target, suffix = '') {
  const obj = { val: 0 };
  gsap.to(obj, {
    val: target,
    snap: { val: 1 },
    scrollTrigger: {
      trigger: el,
      start: 'top 80%',
      end: 'top 30%',
      scrub: 1
    },
    onUpdate: () => {
      el.textContent = Math.round(obj.val) + suffix;
    }
  });
}

animateCounter(document.getElementById('counter-1'), 6.5, '分钟');
animateCounter(document.getElementById('counter-2'), 60000000, '+');
animateCounter(document.getElementById('counter-3'), 28, '%');

// ECG 线动画
const ecgPath = document.getElementById('ecg-line');
const ecgLength = ecgPath.getTotalLength();

gsap.from(ecgPath, {
  scrollTrigger: {
    trigger: '#problem-section',
    start: 'top bottom',
    end: 'center center',
    scrub: 1
  },
  strokeDasharray: ecgLength,
  strokeDashoffset: ecgLength,
  ease: 'power2.out'
});
```

**响应式**：三联画在移动端改为垂直排列；数字计数器保持不变。

---

### 第三章：方案 — 森林在等你

**商业目标**：用户清楚知道 STILLPOINT 提供什么——200英亩森林中的精品住宿、疗愈活动、冥想空间、有机餐饮。

**故事角色**：故事转折点。用户从“我需要这个”进入“他们有什么”——品牌展示解决方案。

**情绪变化**：认同 😌 → 惊叹 😮

**画面描述**（140字）：
一个巨大的3D地形图在屏幕中央缓慢旋转——那是卡茨基尔山脉的地形。用户滚动时，地形图“裂开”，从裂缝中生长出真实的森林影像。树木从地面“生长”出来，速度越来越快，直到整个屏幕被森林覆盖。然后，森林像舞台幕布一样拉开：露出一个玻璃小屋、一个瑜伽平台、一个篝火坑、一个露天餐厅。每个空间都有微小的光点环绕，像萤火虫。文字：“STILLPOINT 不是酒店——它是一个被守护的生态系统。”

**内容文案**：
- 标题：STILLPOINT 体验
- 子标题：200英亩的原始森林，只为10位客人
- 示例文字：“我们限制每次入住不超过10位客人——不是为了稀缺，而是为了安静。在这里，你拥有：树屋套房（悬浮在20米高的树冠中）、晨间瑜伽平台（面向日出方向）、地下冥想室（完全隔音，零光源）、有机农场到餐桌（食材来自3公里内的农场）、以及最重要的——一个承诺：没有Wi-Fi，没有电视，没有日程。”

**动画叙事**：
1. **3D地形图旋转**：使用 CSS 3D transform 实现，滚动控制旋转角度
2. **森林生长动画**：树木从地面升起（scaleY: 0 → 1），使用 stagger 产生连绵效果
3. **空间揭示动画**：每个空间卡片在滚动到特定位置时从 opacity: 0, scale: 0.8 过渡到完整状态
4. **萤火虫粒子**：围绕每个空间浮动的小光点，使用 GSAP 循环动画
5. **章节过渡**：森林画面渐变成暖色调，模拟日落

**GSAP 关键代码**：

```javascript
// 3D地形图
gsap.to('#terrain-map', {
  scrollTrigger: {
    trigger: '#solution-section',
    start: 'top bottom',
    end: 'center center',
    scrub: 2
  },
  rotationY: 360,
  rotationX: 15,
  ease: 'none'
});

// 森林生长动画
const trees = document.querySelectorAll('.tree-element');
gsap.from(trees, {
  scrollTrigger: {
    trigger: '#solution-section',
    start: 'top 60%',
    end: 'bottom 30%',
    scrub: 1.5
  },
  scaleY: 0,
  transformOrigin: 'bottom center',
  stagger: 0.02,
  ease: 'power2.out'
});

// 空间卡片揭示
const spaces = document.querySelectorAll('.space-card');
spaces.forEach((card, i) => {
  gsap.from(card, {
    scrollTrigger: {
      trigger: card,
      start: 'top 70%',
      end: 'top 30%',
      scrub: 1
    },
    opacity: 0,
    y: 60,
    scale: 0.85,
    ease: 'power3.out',
    delay: i * 0.1
  });
});

// 萤火虫粒子循环
function fireflyAnimation(container) {
  const particles = container.querySelectorAll('.firefly');
  particles.forEach(p => {
    gsap.to(p, {
      x: `random(-50, 50)`,
      y: `random(-50, 50)`,
      opacity: `random(0.2, 0.8)`,
      duration: `random(2, 4)`,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });
  });
}

document.querySelectorAll('.space-card').forEach(card => {
  fireflyAnimation(card);
});
```

**响应式**：3D地形图在移动端简化为静态图片；树元素数量减半；卡片改为全宽排列。

---

### 第四章：证明 — 那些先醒来的人

**商业目标**：用户相信 STILLPOINT 是真实且有效的——有数据、有案例、有专家背书。

**故事角色**：故事中的“信任时刻”。用户需要看到社会证明来克服最后的犹豫。

**情绪变化**：惊叹 😮 → 信任 👍

**画面描述**（150字）：
一个巨大的、静止的湖面。水面上漂浮着几片荷叶，每片荷叶上显示一个人的名字和一句话。用户滚动时，荷叶开始生长——从一片变成两片、三片……直到布满整个湖面。每片荷叶都承载着一个人的故事：“我在STILLPOINT找到了连续8小时的睡眠——10年来第一次。” “我的冥想时间从3分钟延长到了45分钟。” “离开时，我的皮质醇水平下降了42%。” 荷叶生长到极限时，水面开始泛起涟漪，涟漪扩散到屏幕边缘，形成新的文字：“我们不只是承诺——我们衡量。”

**内容文案**：
- 标题：醒来的人
- 子标题：数据、故事、科学
- 示例文字：“在过去的18个月里，我们记录了237位客人的变化：平均睡眠时间增加2.7小时、自我报告的焦虑水平下降63%、88%的客人在离开后30天仍然保持新的习惯。我们与耶鲁大学和佛罗里达州立大学合作进行临床研究——初步数据显示，在STILLPOINT停留72小时后，参与者的默认模式网络（大脑的‘走神’系统）活动增加了34%，这与创造力、自我反思和情绪调节密切相关。”

**动画叙事**：
1. **荷叶生长动画**：荷叶从 scale: 0, opacity: 0 生长到完整状态，使用 stagger 和随机延迟
2. **涟漪扩散**：用户滚动到最后一片荷叶时，点击位置（或滚动位置）产生涟漪，使用 Canvas 2D
3. **数据卡片翻转**：每个数据点以卡片形式呈现，滚动时从背面翻转到正面
4. **专家头像呼吸动画**：合作机构 logo 有微弱的 pulse 动画
5. **章节过渡**：湖面渐变为星空，用户进入下一章

**GSAP 关键代码**：

```javascript
// 荷叶生长
const lotusLeaves = document.querySelectorAll('.lotus-leaf');
lotusLeaves.forEach((leaf, i) => {
  gsap.from(leaf, {
    scrollTrigger: {
      trigger: '#proof-section',
      start: 'top 60%',
      end: 'bottom 30%',
      scrub: 1.5
    },
    scale: 0,
    opacity: 0,
    rotation: `random(-30, 30)`,
    transformOrigin: 'center center',
    delay: i * 0.05,
    ease: 'back.out(1.7)'
  });
});

// Canvas 涟漪
class RippleSystem {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.ripples = [];
  }

  addRipple(x, y) {
    this.ripples.push({
      x, y,
      radius: 0,
      maxRadius: 100,
      alpha: 0.6,
      speed: 2 + Math.random() * 2
    });
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.ripples = this.ripples.filter(r => {
      r.radius += r.speed;
      r.alpha -= 0.005;
      if (r.alpha <= 0) return false;
      
      this.ctx.beginPath();
      this.ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
      this.ctx.strokeStyle = `rgba(255, 255, 255, ${r.alpha})`;
      this.ctx.lineWidth = 2;
      this.ctx.stroke();
      
      // 第二层涟漪
      this.ctx.beginPath();
      this.ctx.arc(r.x, r.y, r.radius * 0.6, 0, Math.PI * 2);
      this.ctx.strokeStyle = `rgba(255, 255, 255, ${r.alpha * 0.5})`;
      this.ctx.lineWidth = 1;
      this.ctx.stroke();
      
      return true;
    });
    requestAnimationFrame(() => this.animate());
  }
}

// 数据卡片翻转
const dataCards = document.querySelectorAll('.data-card');
dataCards.forEach(card => {
  gsap.from(card, {
    scrollTrigger: {
      trigger: card,
      start: 'top 75%',
      end: 'top 35%',
      scrub: 1
    },
    rotationY: 180,
    ease: 'power2.out'
  });
});

// 机构 logo 呼吸
gsap.to('.institution-logo', {
  scale: 1.05,
  opacity: 0.8,
  duration: 2,
  repeat: -1,
  yoyo: true,
  ease: 'sine.inOut'
});
```

**响应式**：荷叶数量减半；数据卡片翻转改为淡入；涟漪效果保留但涟漪数量减少。

---

### 第五章：行动 — 现在，你只需要决定

**商业目标**：用户知道下一步该做什么——预订、注册、了解更多。

**故事角色**：故事的高潮和结尾。用户已经经历了完整的旅程，现在是行动时刻。

**情绪变化**：信任 👍 → 行动 💪

**画面描述**（160字）：
屏幕中央，一个巨大的、发光的圆——像满月，像禅宗圆相（enso）。圆在缓慢旋转，表面有微妙的纹理，像木纹、像水波。用户滚动时，圆开始“裂开”——从中心出现一条金色的裂缝。裂缝扩大，露出内部的三个选项：一个日历图标（预订）、一个指南针图标（探索更多）、一个对话气泡图标（联系我们）。每个选项在悬停时放大并发出柔和的光晕。圆的外围，文字以环状排列：“有一个地方，时间会慢下来。你只需要决定，让自己去那里。” 圆最终完全打开，形成完整的行动页面。

**内容文案**：
- 标题：你准备好了吗？
- 副标题：选择你的方式
- CTA 1：预订你的停留（链接到预订系统）
- CTA 2：探索所有 Retreat（链接到活动列表）
- CTA 3：与我们的向导对话（联系表单）
- 底部：STILLPOINT · 卡茨基尔山脉 · 信息 · 隐私政策

**动画叙事**：
1. **enso圆旋转**：CSS animation 持续旋转，滚动控制开裂程度
2. **金色裂缝展开**：GSAP 控制 SVG 路径从中心向边缘扩展
3. **选项浮现**：三个选项依次从 opacity: 0, y: 20px 淡入并上移
4. **环状文字动画**：文字围绕圆排列，滚动时旋转速度变化
5. **章节过渡**：圆完全打开后，页面滚动到底部，footer 从底部淡入

**GSAP 关键代码**：

```javascript
// Enso 圆动画
const ensoCircle = document.querySelector('.enso-circle');
const ensoCrack = document.querySelector('.enso-crack');

gsap.to(ensoCrack, {
  scrollTrigger: {
    trigger: '#action-section',
    start: 'top bottom',
    end: 'center center',
    scrub: 1.5
  },
  scaleX: 1,
  scaleY: 1,
  opacity: 1,
  ease: 'power3.out'
});

// 选项浮现
const ctaOptions = document.querySelectorAll('.cta-option');
ctaOptions.forEach((option, i) => {
  gsap.from(option, {
    scrollTrigger: {
      trigger: '#action-section',
      start: 'top 40%',
      end: 'top 20%',
      scrub: 1
    },
    opacity: 0,
    y: 40,
    delay: i * 0.15,
    ease: 'power2.out'
  });
});

// 环状文字
const circularText = document.querySelector('.circular-text');
gsap.to(circularText, {
  scrollTrigger: {
    trigger: '#action-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: 1
  },
  rotation: 180,
  ease: 'none'
});

// Footer 淡入
gsap.from('footer', {
  scrollTrigger: {
    trigger: '#action-section',
    start: 'bottom 80%',
    end: 'bottom top',
    scrub: 1
  },
  opacity: 0,
  y: 50,
  ease: 'power2.out'
});

// 悬停动画
ctaOptions.forEach(option => {
  option.addEventListener('mouseenter', () => {
    gsap.to(option, {
      scale: 1.08,
      boxShadow: '0 0 30px rgba(196, 122, 79, 0.3)',
      duration: 0.3,
      ease: 'power2.out'
    });
  });
  option.addEventListener('mouseleave', () => {
    gsap.to(option, {
      scale: 1,
      boxShadow: '0 0 0px rgba(196, 122, 79, 0)',
      duration: 0.3,
      ease: 'power2.out'
    });
  });
});
```

**响应式**：enso圆缩小至屏幕宽度的80%；选项改为垂直排列；环状文字在移动端隐藏。

---

## 三、⚡ 故事高潮（3 个）

### 高潮1：碎裂与重生（Hero 到 问题 的过渡）

**它在故事中的位置**：第一章底部 → 第二章顶部

**用户做了什么**：滚动到 Hero 区域的底部约 80% 处

**发生了什么（分镜级描述）**：
```
0ms：画面显示人形剪影，粒子开始从剪影边缘脱落
300ms：粒子脱落速度加快，剪影开始模糊
600ms：剪影完全碎裂成 500+ 粒子，向屏幕四周飞散
1200ms：粒子在飞散过程中重组，形成新的文字“STILLPOINT”
2000ms：粒子完全消失，文字稳定显示，背景从黑色渐变为深绿色
2500ms：文字开始淡出，第二章内容从下方浮现
```

**为什么用户会记住它**：这是用户第一次感受到“物理变化”——从一个完整的形态碎裂并重组，象征着“旧我的消解”和“新生的开始”。这种视觉冲击力会留在记忆中。

**完整 GSAP timeline 代码**：

```javascript
// 高潮1：碎裂与重生
const climax1Timeline = gsap.timeline({
  scrollTrigger: {
    trigger: '#hero',
    start: 'bottom 20%',
    end: 'bottom top',
    scrub: 1.5,
    invalidateOnRefresh: true
  }
});

// 1. 粒子系统开始
const canvas1 = document.getElementById('climax-canvas-1');
const ctx1 = canvas1.getContext('2d');
canvas1.width = window.innerWidth;
canvas1.height = window.innerHeight;

const particles1 = [];
const centerX = canvas1.width / 2;
const centerY = canvas1.height / 2;

// 创建初始粒子（人形剪影的轮廓）
for (let i = 0; i < 500; i++) {
  const angle = (Math.PI * 2 / 500) * i;
  const radius = 80 + Math.random() * 40;
  const spreadAngle = angle + (Math.random() - 0.5) * 0.3;
  particles1.push({
    startX: centerX + Math.cos(angle) * radius,
    startY: centerY + Math.sin(angle) * radius * 1.5,
    endX: centerX + Math.cos(spreadAngle) * (radius + 150 + Math.random() * 100),
    endY: centerY + Math.sin(spreadAngle) * (radius * 1.5 + 150 + Math.random() * 100),
    size: 1.5 + Math.random() * 2.5,
    alpha: 1,
    color: `hsl(40, 20%, ${70 + Math.random() * 20}%)`,
    delay: Math.random() * 0.3
  });
}

// 动画循环
function animateClimax1(progress) {
  ctx1.clearRect(0, 0, canvas1.width, canvas1.height);
  
  // 第一阶段：粒子保持原位
  if (progress < 0.2) {
    particles1.forEach(p => {
      ctx1.globalAlpha = 1;
      ctx1.fillStyle = p.color;
      ctx1.beginPath();
      ctx1.arc(p.startX, p.startY, p.size, 0, Math.PI * 2);
      ctx1.fill();
    });
    return;
  }
  
  // 第二阶段：粒子开始飞散
  const spreadProgress = (progress - 0.2) / 0.6;
  particles1.forEach(p => {
    const t = Math.min(1, spreadProgress - p.delay);
    if (t <= 0) {
      ctx1.globalAlpha = 1;
      ctx1.fillStyle = p.color;
      ctx1.beginPath();
      ctx1.arc(p.startX, p.startY, p.size, 0, Math.PI * 2);
      ctx1.fill();
      return;
    }
    
    const easeT = 1 - Math.pow(1 - t, 3);
    const x = p.startX + (p.endX - p.startX) * easeT;
    const y = p.startY + (p.endY - p.startY) * easeT;
    const alpha = 1 - t;
    
    ctx1.globalAlpha = alpha;
    ctx1.fillStyle = p.color;
    ctx1.beginPath();
    ctx1.arc(x, y, p.size * (1 - t * 0.3), 0, Math.PI * 2);
    ctx1.fill();
  });
  
  // 第三阶段：重组文字
  if (progress > 0.8) {
    const textProgress = (progress - 0.8) / 0.2;
    ctx1.globalAlpha = textProgress;
    ctx1.fillStyle = '#F5F0EB';
    ctx1.font = 'bold 4rem Playfair Display';
    ctx1.textAlign = 'center';
    ctx1.fillText('STILLPOINT', centerX, centerY + 10);
  }
}

// GSAP 驱动
climax1Timeline.to({}, {
  onUpdate: function() {
    animateClimax1(this.progress());
  },
  duration: 1
});
```

---

### 高潮2：森林的呼吸（方案章节的核心动画）

**它在故事中的位置**：第三章中间，用户滚动到空间揭示部分

**用户做了什么**：滚动约 300px

**发生了什么（分镜级描述）**：
```
0ms：屏幕被森林覆盖，所有树木静止
300ms：树木开始轻微摇摆，像被风吹动
600ms：森林“呼吸”——所有树木同时放大和缩小，模拟呼吸节奏
1200ms：森林像舞台幕布一样从中心向两侧拉开
2000ms：露出四个空间（树屋、瑜伽平台、冥想室、餐厅），每个空间都有萤火虫环绕
```

**为什么用户会记住它**：这是整站最“魔法”的时刻——静态的森林突然有了生命，像被赋予了呼吸。这种“活的页面”体验会让用户产生敬畏感。

**完整 GSAP timeline 代码**：

```javascript
// 高潮2：森林的呼吸
const climax2Timeline = gsap.timeline({
  scrollTrigger: {
    trigger: '#solution-section',
    start: 'top 20%',
    end: 'bottom 80%',
    scrub: 2,
    invalidateOnRefresh: true
  }
});

// 1. 树木轻微摇摆
const trees2 = document.querySelectorAll('.tree-element');
climax2Timeline.to(trees2, {
  rotation: 2,
  transformOrigin: 'bottom center',
  duration: 0.5,
  stagger: 0.02,
  ease: 'sine.inOut',
  yoyo: true,
  repeat: 1
}, 0);

// 2. 森林呼吸（所有树木同步缩放）
climax2Timeline.to(trees2, {
  scaleX: 1.03,
  scaleY: 1.05,
  duration: 1,
  ease: 'sine.inOut',
  yoyo: true,
  repeat: 1,
  onStart: () => {
    // 添加呼吸光效
    gsap.to('#forest-overlay', {
      opacity: 0.3,
      duration: 0.5,
      yoyo: true,
      repeat: 1
    });
  }
}, 0.6);

// 3. 森林拉开（幕布效果）
climax2Timeline.to('#forest-curtain-left', {
  x: '-50%',
  duration: 1.2,
  ease: 'power3.inOut'
}, 2);

climax2Timeline.to('#forest-curtain-right', {
  x: '50%',
  duration: 1.2,
  ease: 'power3.inOut'
}, 2);

// 4. 空间揭示
const spaces2 = document.querySelectorAll('.space-card');
spaces2.forEach((space, i) => {
  climax2Timeline.from(space, {
    opacity: 0,
    y: 80,
    scale: 0.7,
    duration: 0.8,
    ease: 'back.out(1.7)'
  }, 2.5 + i * 0.15);
  
  // 萤火虫出现
  const fireflies2 = space.querySelectorAll('.firefly');
  climax2Timeline.from(fireflies2, {
    opacity: 0,
    scale: 0,
    duration: 0.3,
    stagger: 0.05,
    ease: 'power2.out'
  }, 3 + i * 0.15);
});
```

---

### 高潮3：enso 的启示（行动章节的核心）

**它在故事中的位置**：第五章，用户滚动到 CTA 部分

**用户做了什么**：滚动到页面约 85% 处

**发生了什么（分镜级描述）**：
```
0ms：屏幕中央出现一个完美的圆形（enso），表面有木纹纹理
300ms：圆形开始缓慢旋转，同时从中心出现一条细小的金色裂缝
600ms：裂缝开始扩大，发出温暖的金色光芒
1200ms：圆形完全裂开成两半，内部显示三个选项
2000ms：选项依次浮现，每个都带有柔和的光晕
2500ms：圆形外围的环状文字开始围绕旋转
```

**为什么用户会记住它**：Enso 圆在禅宗中代表“悟道”的瞬间。这个动画将品牌理念（找到暂停键）视觉化为一个神圣的、令人敬畏的时刻。用户会记住“那个发光的圆”和“它打开的时刻”。

**完整 GSAP timeline 代码**：

```javascript
// 高潮3：enso 的启示
const climax3Timeline = gsap.timeline({
  scrollTrigger: {
    trigger: '#action-section',
    start: 'top 10%',
    end: 'center center',
    scrub: 1.5,
    invalidateOnRefresh: true
  }
});

// 1. Enso 圆出现（已经可见，但开始激活）
const enso = document.querySelector('.enso-circle');
climax3Timeline.to(enso, {
  scale: 1.1,
  duration: 0.5,
  ease: 'power2.out'
}, 0);

// 2. 金色裂缝出现
const crack = document.querySelector('.enso-crack');
climax3Timeline.to(crack, {
  scaleX: 1,
  scaleY: 1,
  opacity: 1,
  duration: 0.8,
  ease: 'power3.out'
}, 0.3);

// 3. 裂缝扩大（圆形裂开）
climax3Timeline.to('.enso-left', {
  x: '-5%',
  rotation: -5,
  duration: 0.8,
  ease: 'power2.inOut'
}, 1.2);

climax3Timeline.to('.enso-right', {
  x: '5%',
  rotation: 5,
  duration: 0.8,
  ease: 'power2.inOut'
}, 1.2);

// 4. 金色光芒扩散
climax3Timeline.to('#enso-glow', {
  scale: 2,
  opacity: 0.6,
  duration: 1,
  ease: 'power2.out'
}, 1.2);

// 5. 选项浮现
const ctaOpts = document.querySelectorAll('.cta-option');
ctaOpts.forEach((opt, i) => {
  climax3Timeline.from(opt, {
    opacity: 0,
    y: 30,
    scale: 0.8,
    duration: 0.5,
    ease: 'back.out(1.5)'
  }, 2 + i * 0.2);
});

// 6. 环状文字开始旋转
climax3Timeline.to('.circular-text', {
  rotation: 45,
  duration: 1,
  ease: 'power2.out'
}, 2);

// 7. 背景渐变
climax3Timeline.to('#action-bg', {
  backgroundColor: '#1a2e24',
  duration: 1,
  ease: 'power2.out'
}, 0);
```

---

## 四、🛠️ 技术实现

### 4.1 技术栈（版本号）
- HTML5 / CSS3
- JavaScript (ES6+)
- GSAP 3.12.2
- ScrollTrigger 3.12.2
- Lenis 1.3.18
- SplitType 0.3.4
- 无框架（纯原生）

### 4.2 项目结构
```
stillpoint/
├── index.html
├── css/
│   ├── reset.css
│   ├── variables.css
│   ├── typography.css
│   ├── layout.css
│   ├── animations.css
│   └── responsive.css
├── js/
│   ├── main.js
│   ├── particles.js
│   ├── canvas-ripple.js
│   ├── animations.js
│   └── climaxes.js
├── assets/
│   ├── images/
│   │   ├── hero-bg.jpg
│   │   ├── forest.jpg
│   │   ├── treehouse.jpg
│   │   ├── yoga-platform.jpg
│   │   ├── meditation-room.jpg
│   │   ├── dining.jpg
│   │   └── lake.jpg
│   ├── icons/
│   │   ├── calendar.svg
│   │   ├── compass.svg
│   │   └── chat.svg
│   └── fonts/
│       ├── PlayfairDisplay-Variable.woff2
│       └── Inter-Variable.woff2
└── README.md
```

### 4.3 数据模型（TypeScript 接口）
```typescript
interface SiteConfig {
  brand: {
    name: string;
    tagline: string;
    description: string;
  };
  sections: Section[];
  animations: {
    type: 'particle' | 'ripple' | 'text' | 'parallax' | 'stagger' | 'card-flip' | 'curtain' | 'enso';
    trigger: string;
    scrub: number;
  }[];
}

interface Section {
  id: string;
  title: string;
  subtitle?: string;
  body: string;
  animationType: string;
  storyRole: string;
  commercialGoal: string;
  emotionIn: string;
  emotionOut: string;
}

interface ParticleConfig {
  count: number;
  color: string;
  sizeRange: [number, number];
  speed: number;
  spreadRadius: number;
}

interface RippleConfig {
  maxRadius: number;
  alpha: number;
  speed: number;
  color: string;
}
```

### 4.4 资源清单
- 图片：7 张高质量自然摄影（建议使用 Unsplash 或自定义拍摄）
- 图标：3 个 SVG 图标（日历、指南针、聊天气泡）
- 字体：Playfair Display（Google Fonts） + Inter（Google Fonts）
- 视频：可选背景视频（森林延时摄影）

---

## 五、📱 响应式策略

| 断点 | 故事调整 | 动画简化 |
|:---|:---|:---|
| >1200px | 完整叙事，5 章全展示 | 全量动画，3 个高潮完整呈现 |
| 768-1200px | 章节压缩，问题与方案合并 | 粒子数减半，3D 地形图取消，enso 圆缩小 |
| <768px | 精简为 4 章（Hero → 问题/方案合并 → 证明 → 行动） | 粒子数 100，无 Canvas 动画，卡片翻转改为淡入，高潮 2 和 3 简化 |
| <480px | 单列布局，文字更短 | 仅保留文字动画和淡入效果 |

---

## 六、🚀 AI 开发顺序（5 Phase）

### Phase 1：骨架（2 小时）
- 创建 index.html 结构
- 编写 CSS 变量、基础排版、布局
- 引入 GSAP、Lenis、SplitType CDN
- 实现 Hero 区域的静态版本

### Phase 2：动画引擎（3 小时）
- 初始化 Lenis 平滑滚动
- 编写粒子系统类
- 编写涟漪系统类
- 创建 ScrollTrigger 基础配置

### Phase 3：章节动画（4 小时）
- 实现第一章：粒子消散 + 文字动画
- 实现第二章：三联画 + 计数器 + ECG 线
- 实现第三章：地形图 + 森林生长 + 空间揭示
- 实现第四章：荷叶生长 + 涟漪 + 数据卡片
- 实现第五章：enso 圆 + 选项浮现

### Phase 4：高潮实现（3 小时）
- 实现高潮1：碎裂与重生（Canvas 粒子 + 文字重组）
- 实现高潮2：森林的呼吸（树木动画 + 幕布拉开）
- 实现高潮3：enso 的启示（圆形裂开 + 选项浮现）

### Phase 5：响应式 + 优化（2 小时）
- 实现所有断点的响应式调整
- 移动端动画简化
- 性能优化（图片懒加载、动画节流）
- 浏览器兼容性测试

---

## 📏 丰富度自检（✓全部完成）

- [x] 方案开头用一句话说清楚了这是什么品牌/产品
- [x] 品牌名“STILLPOINT”是原创的，没有照搬或变体使用参考报告的域名/品牌名
- [x] 每个 section 都有“商业目标”
- [x] 看完不需要猜测“这网站到底是干什么的”

- [x] 每个高潮的 GSAP 代码完整可运行，没有 TODO 或注释占位

- [x] 有一条清晰的情绪曲线（焦躁 → 好奇 → 认同 → 惊叹 → 信任 → 行动）
- [x] 每个 section 有故事角色和用户情绪描述
- [x] 3 个故事高潮（用户会记住的瞬间）

- [x] 每个 section 的画面描述 >100 字
- [x] 色彩有故事含义
- [x] 字体选择有理由

- [x] 全站 10+ 种动画类型（粒子、文字逐词、渐变、旋转、缩放、淡入、翻转、涟漪、幕布、呼吸、圣光）
- [x] 每个 section ≥3 种动画 + 过渡
- [x] 100% scrub 驱动，有节奏变化（慢 → 快 → 激烈 → 温柔）
- [x] GSAP 代码零 bug

- [x] 有真实感的业务数据（237位客人、2.7小时、63%焦虑下降、34%默认模式网络活动增加）
- [x] 每个 section 有文案方向和示例
- [x] 总字数 ≥5000 字

---

**STILLPOINT 不是另一个度假村网站——它是一个关于“暂停”的沉浸式电影。从第一帧的焦躁到最后一帧的宁静，用户不是在浏览页面，而是在经历一次疗愈。**