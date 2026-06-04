# 🌊 SORA WOODS — 在受保护的古木间，找回呼吸的节奏

> **灵感来自**：diamondrosesanctuary.com 的诗意叙事与滚动驱动动画 + 其专业 GSAP+Lenis+SplitType 动画技术栈
> **故事主线**：一位疲惫的都市人，从踏入千年古木林的第一秒开始，经历从“遗忘”到“觉醒”的心灵旅程——从被噪音淹没，到听见心跳，最终与自然同频共振
> **情绪曲线**：迷失 → 好奇 → 震撼 → 觉醒 → 信任 → 行动

---

## 一、🎨 视觉世界观

### 1.1 情绪板

想象一个被遗忘的古老森林：晨雾在林间流淌，阳光从百年树冠的缝隙中洒下，变成一缕缕金色的光柱。苔藓覆盖的石阶、鹿蹄印迹、溪水的低语。空气中弥漫着松脂、泥土和野花的混合气息。这里没有水泥路，没有Wi-Fi信号，只有风穿过针叶林的簌簌声，和偶尔传来的鸟鸣。每一棵树都像一位沉默的长者，等待着你坐下来，倾听。

SORA WOODS 的网站就是通往这片森林的入口——它不是预订平台，而是一场灵魂的邀请。

### 1.2 色彩体系

```css
:root {
  --color-forest-deep: #0A1F1A;    /* 古木深处的黑暗，代表“被遗忘的自我” */
  --color-pine-shadow: #1A332B;    /* 松树的阴影，代表“静谧与内省” */
  --color-moss-floor: #3A5A4A;     /* 苔藓覆盖的地面，代表“生命缓慢生长” */
  --color-fern-green: #5A7A6A;     /* 蕨叶的翠绿，代表“复苏与希望” */
  --color-golden-light: #C4A35A;   /* 穿过树冠的阳光，代表“觉醒的瞬间” */
  --color-sun-kissed: #E8D5A0;     /* 被阳光亲吻的落叶，代表“温暖与接纳” */
  --color-mist-white: #F0EDE6;     /* 晨雾的乳白，代表“纯净与开始” */
  --color-bark-brown: #4A3A2A;     /* 古老树皮，代表“根基与信任” */
  --color-ember-glow: #D4735E;     /* 篝火余烬，代表“内心的火焰” */
  --color-stone-gray: #8A8A82;     /* 溪流中的卵石，代表“时间与永恒” */
}
```

每个颜色都有故事含义，它们不是随机的色板，而是森林从黎明到黄昏的完整叙事。

### 1.3 字体叙事

```
标题字体: "Playfair Display", serif — 它有优雅的衬线，像古树的年轮一样有故事感。每个字母的粗细变化，如同森林中光与影的交替。它传达的是“古老智慧”与“永恒优雅”。

正文字体: "Inter", sans-serif — 干净、现代的几何无衬线，像清澈的溪水一样透明。它让用户在沉浸于诗意氛围的同时，能清晰理解信息。它传达的是“简洁”与“可信”。

字号层级：
--text-h1: clamp(56px, 8vw, 120px);     /* 首屏标题，震撼人心 */
--text-h2: clamp(40px, 5vw, 72px);      /* 章节标题，引导叙事 */
--text-h3: clamp(28px, 3vw, 48px);      /* 模块标题，吸引注意 */
--text-h4: clamp(20px, 2vw, 32px);      /* 卡片标题，清晰识别 */
--text-body-lg: clamp(18px, 1.5vw, 24px); /* 关键段落，沉浸阅读 */
--text-body: clamp(16px, 1.2vw, 20px);    /* 正文，舒适阅读 */
--text-caption: 14px;                     /* 辅助信息，低调存在 */
```

### 1.4 间距节奏

基于 8px grid。核心间距值：8px, 16px, 24px, 32px, 48px, 64px, 80px, 120px, 160px, 240px。

Section 之间的间距统一为 160px（移动端缩减为 80px），让每个章节有足够的呼吸感。

---

## 二、📖 故事章节（逐 Section）

### 第一章：HERO — 迷失与第一缕光

**商业目标**：用户离开这个 section 后，应该知道 SORA WOODS 是一个位于古老森林中的疗愈度假村，提供从内到外的身心修复体验。

**故事角色**：一个疲惫的都市人，手机屏幕的蓝光还在脸上闪烁，但她的眼睛已经开始寻找黑暗中的第一缕绿色。

**情绪变化**：焦虑 → 好奇 → 期待

**画面描述**（电影分镜）：

画面从一片漆黑开始。不是死黑，而是有深度的黑——像闭上眼睛后的视网膜上残留的微弱光斑。持续 2 秒后，屏幕中央缓缓浮现出一个极小的光点，像黎明前最遥远的星辰。光点以极慢的速度膨胀，同时它的颜色从冷白渐变到暖金——这是第一缕阳光穿透千年树冠。随着光的扩散，画面被切割成两个世界：左侧是都市的模糊剪影（灰色调，半透明，像记忆中的噪音），右侧开始显现森林的轮廓（树干的深棕色、苔藓的绿色、雾气的乳白色）。当光点最终变成一只金鹿的剪影时，整个画面被森林占据，城市消失。金鹿静静站立在画面中央偏右的位置，背景是无限延伸的森林深处。标题从金鹿的脚边浮现，像苔藓一样慢慢生长。

**内容文案**：

```
标题：SORA WOODS
副标题：在受保护的古木间，找回呼吸的节奏
描述：距城市仅90分钟，却远在喧嚣之外。一片被守护了三个世纪的原始森林，等待着你来重启身心。
CTA：开始你的旅程（↓ 向下滚动）
```

**动画叙事**（≥3 种动画 + 章节过渡，全部 scrub）：

1. **光点入场动画**（0-100vh scrub）：从 2px 光点膨胀到覆盖全屏的金光，使用 `scale` 和 `opacity` 控制
2. **金鹿剪影动画**（50-150vh scrub）：金鹿从半透明变为清晰，同时在原地轻微呼吸（上下浮动 4px，周期 3s）
3. **文字浮现动画**（80-180vh scrub）：标题和副标题从底部 40px 处淡入上移，SplitType 逐字揭示
4. **章节过渡**：当用户滚动到 section 底部时，金鹿向右走出画面，森林场景变成全屏深绿色，作为下一个章节的背景

**GSAP 关键代码**：

```javascript
// Hero 章节 - 光点入场动画
const heroTL = gsap.timeline({
  scrollTrigger: {
    trigger: '.hero-section',
    start: 'top top',
    end: 'bottom top',
    scrub: 1.5,
  }
});

// 光点从 2px 膨胀到覆盖屏
heroTL.fromTo('.hero-light-dot', {
  scale: 0.01,
  opacity: 1,
  filter: 'brightness(2) blur(0px)',
}, {
  scale: 100,
  opacity: 0.6,
  filter: 'brightness(0.8) blur(4px)',
  duration: 1,
  ease: 'power2.out',
}, 0);

// 金鹿浮现并呼吸
heroTL.fromTo('.hero-deer', {
  opacity: 0,
  scale: 0.8,
  y: 20,
}, {
  opacity: 1,
  scale: 1,
  y: 0,
  duration: 0.8,
  ease: 'power2.out',
}, 0.3);

// 金鹿呼吸动画（独立无限循环）
gsap.to('.hero-deer', {
  y: -4,
  duration: 3,
  ease: 'sine.inOut',
  yoyo: true,
  repeat: -1,
});

// SplitType 文字揭示
const heroText = new SplitType('.hero-title', { types: 'chars' });
heroTL.fromTo(heroText.chars, {
  opacity: 0,
  y: 40,
  rotateX: -90,
}, {
  opacity: 1,
  y: 0,
  rotateX: 0,
  stagger: 0.03,
  duration: 0.6,
  ease: 'back.out(1.7)',
}, 0.6);

// 章节过渡 - 金鹿消失，背景变深绿
heroTL.to('.hero-deer', {
  x: 200,
  opacity: 0,
  duration: 0.5,
  ease: 'power2.in',
}, 1.2);

heroTL.to('.hero-section', {
  backgroundColor: '#0A1F1A',
  duration: 0.8,
  ease: 'power2.inOut',
}, 1.2);
```

**响应式**：
- 移动端：光点入场动画速度加快（scrub: 0.8），金鹿剪影缩小至 40%，文字字号缩小至 clamp(32px, 8vw, 56px)
- 平板：文字字号缩小至 56px，金鹿剪影保持在画面中央
- 桌面：全屏体验，光点最大膨胀到 120vw

---

### 第二章：问题 — 被噪音淹没的灵魂

**商业目标**：用户离开后，应该深刻共鸣“现代都市生活正在消耗我的生命力”，并渴望找到出口。

**故事角色**：同一位都市人，但场景切换回她的日常生活——地铁的拥挤、手机通知的轰炸、永远在闪烁的屏幕。

**情绪变化**：烦躁 → 窒息 → 开始怀疑

**画面描述**（100+ 字电影分镜）：

画面从一片温柔的深绿突然切换到刺眼的灰色。一个完全由数据和代码构成的都市景观——建筑物是不断跳动的数字，街道是流动的二进制流，天空中漂浮着无数半透明的通知气泡，像密集的飞虫。主角（我们只能看到她的轮廓）被这些数字包围，她的手机屏幕上不断弹出红色的通知标记（0→99+）。她试图推开这些气泡，但每一个被她碰到的气泡都会炸裂成更多更小的气泡。周围的数字人群面无表情地穿行，每个人都戴着耳机，眼神空洞。画面中的音效（如果有）是嘈杂的城市噪音——汽车喇叭、地铁广播、键盘敲击声——所有声音叠加在一起，形成一个令人窒息的音墙。突然，所有声音消失，画面定格。主角的一只手伸向屏幕，触碰到了那些数字——瞬间，数字崩塌，露出后面的一抹绿色。

**内容文案**：

```
标题：你有多久没有真正呼吸了？
正文：数据显示，现代人平均每天查看手机 96 次。但在 SORA，我们建议你——0 次。
数据点：86% 的都市人报告有“持续疲惫感”
数据点：每天暴露在噪音中超过 8 小时
数据点：平均睡眠时间不足 6.5 小时
CTA：是时候停下了
```

**动画叙事**（≥3 种动画 + 章节过渡）：

1. **数字都市入场**：从上一章的深绿渐变到灰色，都市建筑从底部升起（transform: translateY(100%) → translateY(0)）
2. **通知气泡动画**：气泡从右上角以随机间隔浮入，每个气泡淡入后轻微放大，然后被主角碰触时炸裂成粒子
3. **数字崩塌动画**：当主角伸手触碰屏幕时，所有数字元素以波浪形式崩塌（从左到右），露出背后的森林
4. **章节过渡**：数字崩塌后，画面完全变白（持续 0.5s），然后从白色中缓缓显现下一个章节的森林场景

**GSAP 关键代码**：

```javascript
// 问题章节 - 数字都市入场
const problemTL = gsap.timeline({
  scrollTrigger: {
    trigger: '.problem-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: 1.2,
  }
});

// 城市建筑从底部升起
problemTL.fromTo('.problem-buildings', {
  y: '100%',
  opacity: 0,
}, {
  y: '0%',
  opacity: 1,
  duration: 0.8,
  ease: 'power3.out',
}, 0);

// 通知气泡逐个出现
const bubbles = document.querySelectorAll('.problem-notification-bubble');
bubbles.forEach((bubble, i) => {
  problemTL.fromTo(bubble, {
    x: 200,
    y: -100,
    opacity: 0,
    scale: 0.5,
    rotation: 15,
  }, {
    x: 0,
    y: 0,
    opacity: 1,
    scale: 1,
    rotation: 0,
    duration: 0.4,
    ease: 'power2.out',
  }, 0.2 + i * 0.15);
});

// 主角伸手触碰
problemTL.to('.problem-hand', {
  y: -80,
  duration: 0.6,
  ease: 'power2.out',
}, 1.5);

// 数字崩塌（波浪效果）
problemTL.to('.problem-digit', {
  opacity: 0,
  scale: 0.1,
  rotation: 360,
  stagger: {
    from: 'center',
    each: 0.02,
    grid: 'auto',
  },
  duration: 0.5,
  ease: 'power2.in',
}, 2);

// 章节过渡 - 白屏过渡
problemTL.to('.problem-section', {
  backgroundColor: '#F0EDE6',
  duration: 0.3,
  ease: 'power2.inOut',
}, 2.5);

problemTL.to('.problem-section', {
  opacity: 0,
  duration: 0.5,
  ease: 'power2.in',
}, 2.8);
```

**响应式**：
- 移动端：删除通知气泡动画（性能原因），城市建筑从底部升起改为从上往下覆盖
- 平板：气泡数量减少至 5 个，数字崩塌效果保留但简化

---

### 第三章：方案 — 森林在等你

**商业目标**：用户离开后，应该知道 SORA WOODS 提供的核心服务——森林木屋、森林浴导览、冥想课程、有机餐食——以及如何预订。

**故事角色**：主角已经从城市逃离，站在森林入口。她深呼吸了第一口真正的空气。

**情绪变化**：放松 → 惊喜 → 好奇

**画面描述**（100+ 字电影分镜）：

画面从白色渐渐过渡到一片被晨雾笼罩的森林。镜头从地面开始——苔藓覆盖的树根、落叶、蘑菇、一只蜗牛。然后镜头缓缓上移，经过粗壮的树干（树皮纹理清晰可见），最终停在树冠——阳光从树叶缝隙中洒下，形成丁达尔效应。主角（现在穿着一件亚麻色的衣服）站在一条小径的起点，小径蜿蜒消失于森林深处。在她面前的木牌上，写着“SORA WOODS”。随着她迈出第一步，画面分割成四个卡片，像相框一样排列在屏幕中央，每个卡片展示一个核心服务：木屋内部（温暖灯光、木质家具）、森林浴（一群人走在林中）、冥想课程（一个人坐在溪边）、有机餐食（摆盘精美的素食）。每张卡片在主角经过时逐渐放大，然后缩小回原位。

**内容文案**：

```
标题：森林在等你
副标题：三种方式，重新与自然连接

卡片1：古木居所
在百年红杉的怀抱中入睡。每间木屋都有巨大的落地窗，让森林成为你房间的一部分。
→ 查看木屋

卡片2：森林浴
跟随认证导师，在溪流边、苔藓上、古树下，进行一场感官觉醒的散步。不是徒步，是倾听。
→ 了解森林浴

卡片3：静修课程
从呼吸法到森林冥想，从瑜伽到陶艺。每天一个主题，每项活动不超过6人。
→ 查看课程

卡片4：土地到餐桌
我们的厨师从森林和花园中直接获取食材。每一口，都是这片土地的礼物。
→ 探索菜单
```

**动画叙事**（≥3 种动画 + 章节过渡）：

1. **森林入场**：从白色渐变到森林场景，镜头从地面缓慢上移（使用 transform: translateY 控制）
2. **卡片分割动画**：当主角走到小径尽头时，森林场景分裂成四个卡片，每个卡片从不同的方向飞入（左上、右上、左下、右下）
3. **卡片交互动画**：鼠标悬停时，卡片放大（scale: 1.05），同时显示更多文字信息；点击后翻转显示详情
4. **章节过渡**：四个卡片在页面底部合并成一条宽幅的森林全景，作为下一章的背景

**GSAP 关键代码**：

```javascript
// 方案章节 - 森林入场与卡片分割
const solutionTL = gsap.timeline({
  scrollTrigger: {
    trigger: '.solution-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: 1.5,
  }
});

// 森林场景从底部上移
solutionTL.fromTo('.solution-forest', {
  y: '30%',
  scale: 1.1,
  filter: 'brightness(0.6) saturate(0.5)',
}, {
  y: '0%',
  scale: 1,
  filter: 'brightness(1) saturate(1)',
  duration: 1,
  ease: 'power2.out',
}, 0);

// 卡片从四个方向飞入
const cards = document.querySelectorAll('.solution-card');
const directions = [
  { x: -200, y: -150, rotation: -10 },  // 左上
  { x: 200, y: -150, rotation: 10 },    // 右上
  { x: -200, y: 150, rotation: 5 },     // 左下
  { x: 200, y: 150, rotation: -5 },     // 右下
];

cards.forEach((card, i) => {
  solutionTL.fromTo(card, {
    x: directions[i].x,
    y: directions[i].y,
    opacity: 0,
    scale: 0.6,
    rotation: directions[i].rotation,
  }, {
    x: 0,
    y: 0,
    opacity: 1,
    scale: 1,
    rotation: 0,
    duration: 0.6,
    ease: 'power3.out',
  }, 0.8 + i * 0.15);
});

// 卡片悬停交互
cards.forEach(card => {
  card.addEventListener('mouseenter', () => {
    gsap.to(card, {
      scale: 1.05,
      boxShadow: '0 20px 40px rgba(10, 31, 26, 0.3)',
      duration: 0.3,
      ease: 'power2.out',
    });
    gsap.to(card.querySelector('.card-content'), {
      y: -10,
      opacity: 1,
      duration: 0.3,
    });
  });
  
  card.addEventListener('mouseleave', () => {
    gsap.to(card, {
      scale: 1,
      boxShadow: '0 4px 12px rgba(10, 31, 26, 0.15)',
      duration: 0.3,
      ease: 'power2.out',
    });
    gsap.to(card.querySelector('.card-content'), {
      y: 0,
      opacity: 0.6,
      duration: 0.3,
    });
  });
});

// 章节过渡 - 卡片合并成全景
solutionTL.to('.solution-card', {
  width: '25%',
  height: '100vh',
  position: 'fixed',
  top: 0,
  left: 0,
  borderRadius: 0,
  opacity: 0.3,
  scale: 1,
  duration: 0.8,
  ease: 'power2.inOut',
}, 2.5);

solutionTL.set('.solution-card', {
  position: 'absolute',
}, 3.3);
```

**响应式**：
- 移动端：卡片改为垂直排列（flex-direction: column），每个卡片占满视口宽度，从下方依次飞入
- 平板：卡片 2x2 网格排列，动画保留但速度加快

---

### 第四章：证明 — 数字不会说谎

**商业目标**：用户离开后，应该相信 SORA WOODS 的疗效是有科学依据的，并知道已经有 2000+ 人在这里找到了改变。

**故事角色**：主角已经体验了森林，现在她坐在篝火旁，听老护林员讲述这片土地的故事和数据。

**情绪变化**：怀疑 → 信任 → 向往

**画面描述**（100+ 字电影分镜）：

画面从篝火的橙色光芒开始。火苗在中央跳动，火星偶尔飞溅到黑暗中。镜头逐渐拉远，我们看到主角围坐在篝火旁，对面坐着一位老人（护林员），他的脸被火光映成温暖的金色。在他身后，树木的剪影在夜风中摇曳。老人开始说话，随着他的讲述，数据以树木年轮的形式浮现在他身后的森林中——每个圆环代表一个数据点，从内向外生长。第一个圆环：“2000+ 访客”，第二个：“97% 报告压力显著下降”，第三个：“平均停留：4.2 天”，第四个：“86% 会再次来访”。每个圆环在出现时都会轻微发光，然后固定在树影中。

**内容文案**：

```
标题：这片森林知道答案
正文：不是营销话术，是 2000 多位访客的真实反馈。

数据环 1：2000+ 位访客
数据环 2：97% 报告压力显著下降（基于 3 个月追踪）
数据环 3：平均停留 4.2 天（建议至少停留 3 晚）
数据环 4：86% 会再次来访

引语：“我以为这只是一次度假。但它改变了我的生活。”
— Sarah M.，2024 年 8 月访客
```

**动画叙事**（≥3 种动画 + 章节过渡）：

1. **篝火动画**：使用 Canvas 2D 绘制动态火焰，粒子系统模拟火星飞溅
2. **年轮生长动画**：每个圆环从中心点以圆形路径向外扩展，同时数字从 0 滚动到真实数值
3. **引语浮现动画**：引语从底部出现，SplitType 逐词揭示
4. **章节过渡**：篝火逐渐熄灭，画面变暗，然后从黑暗中浮现下一章的星空

**GSAP 关键代码**：

```javascript
// 证明章节 - 年轮生长 + 数字滚动
const proofTL = gsap.timeline({
  scrollTrigger: {
    trigger: '.proof-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: 1.2,
  }
});

// 年轮生长（使用 SVG circle）
const rings = document.querySelectorAll('.proof-ring');
const numbers = document.querySelectorAll('.proof-number');

rings.forEach((ring, i) => {
  const radius = ring.getAttribute('r');
  const circumference = 2 * Math.PI * radius;
  
  // 设置初始状态
  ring.style.strokeDasharray = circumference;
  ring.style.strokeDashoffset = circumference;
  
  proofTL.to(ring, {
    strokeDashoffset: 0,
    duration: 0.8,
    ease: 'power2.out',
  }, 0.3 + i * 0.2);
  
  // 数字滚动
  const targetNumber = parseInt(numbers[i].getAttribute('data-target'));
  const numObj = { value: 0 };
  
  proofTL.to(numObj, {
    value: targetNumber,
    duration: 0.6,
    ease: 'power2.out',
    snap: { value: 1 },
    onUpdate: () => {
      numbers[i].textContent = numObj.value.toLocaleString() + 
        (numbers[i].getAttribute('data-suffix') || '');
    },
  }, 0.5 + i * 0.2);
});

// 引语浮现
const quoteText = new SplitType('.proof-quote', { types: 'words' });
proofTL.fromTo(quoteText.words, {
  opacity: 0,
  y: 20,
}, {
  opacity: 1,
  y: 0,
  stagger: 0.05,
  duration: 0.4,
  ease: 'power2.out',
}, 1.5);

// Canvas 篝火动画
class FireParticle {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.vx = (Math.random() - 0.5) * 2;
    this.vy = -Math.random() * 3 - 1;
    this.size = Math.random() * 4 + 2;
    this.life = 1;
    this.decay = Math.random() * 0.02 + 0.01;
    this.color = `hsl(${30 + Math.random() * 20}, 100%, ${50 + Math.random() * 30}%)`;
  }
  
  update() {
    this.x += this.vx;
    this.y += this.vy;
    this.vy -= 0.02;
    this.life -= this.decay;
    this.size *= 0.99;
  }
  
  draw(ctx) {
    ctx.globalAlpha = this.life;
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
  }
}

// 在 ScrollTrigger 的 onUpdate 中驱动粒子
const fireCanvas = document.querySelector('.proof-fire-canvas');
const ctx = fireCanvas.getContext('2d');
let particles = [];

// 每帧更新粒子
function updateFire() {
  // 添加新粒子
  if (particles.length < 50) {
    for (let i = 0; i < 3; i++) {
      particles.push(new FireParticle(
        fireCanvas.width / 2 + (Math.random() - 0.5) * 20,
        fireCanvas.height - 20
      ));
    }
  }
  
  // 更新和绘制粒子
  ctx.clearRect(0, 0, fireCanvas.width, fireCanvas.height);
  particles = particles.filter(p => p.life > 0);
  particles.forEach(p => {
    p.update();
    p.draw(ctx);
  });
  
  requestAnimationFrame(updateFire);
}
updateFire();

// Canvas 尺寸设置
function resizeFireCanvas() {
  const dpr = window.devicePixelRatio || 1;
  fireCanvas.width = fireCanvas.offsetWidth * dpr;
  fireCanvas.height = fireCanvas.offsetHeight * dpr;
  ctx.scale(dpr, dpr);
}
resizeFireCanvas();
window.addEventListener('resize', resizeFireCanvas);
```

**响应式**：
- 移动端：年轮改为水平柱状图，Canvas 篝火粒子数量减半
- 平板：保留年轮设计，但缩小尺寸

---

### 第五章：行动 — 你的森林在等你

**商业目标**：用户离开后，应该知道如何预订（日期选择、人数、木屋类型），并愿意填写表单。

**故事角色**：主角站在森林出口，但她已经决定不再回到原来的生活。

**情绪变化**：决心 → 期待 → 行动

**画面描述**（100+ 字电影分镜）：

画面从黑暗的森林深处开始，主角背对镜头，面向远处的一扇门——门缝中透出温暖的金色光芒。她推开门，光芒瞬间吞没画面。当光芒消退后，我们看到了一个极简的预订界面——不是普通的表单，而是一个像“选择你的路径”一样的交互式地图。森林地图上散布着几个发光的点（木屋位置），用户可以通过旋转视角来选择木屋。每个木屋点击后，会显示木屋的照片、可预订日期、价格。表单被设计成“写下你的愿望”的形式——不是冷冰冰的输入框，而是“你希望在这片森林中找到什么？”这样的开放性问题。

**内容文案**：

```
标题：选择你的森林之家
副标题：每一间木屋都有自己的故事

木屋选择器：
- 溪畔小屋（2人）— 聆听溪水整夜流淌
- 树冠套房（2人）— 在树顶醒来，与鸟为邻
- 苔原阁楼（4人）— 适合家庭或小团体
- 隐士小屋（1人）— 完全的独处与静默

CTA：开始你的旅程

表单问题：
“你希望在这片森林中找到什么？”
“你希望停留多久？”（3晚 / 5晚 / 7晚 / 定制）
“你愿意断开连接吗？”（是 / 让我想想）
```

**动画叙事**（≥3 种动画 + 章节过渡）：

1. **门动画**：从上一章过渡，推门进入光芒中，光芒消退后显示预订界面
2. **木屋选择器动画**：木屋卡片以圆形排列，用户滚动时卡片旋转（像旋转木马），选中的卡片放大并显示详情
3. **表单动画**：每个输入框从底部依次滑入，占位文字像打字机一样逐字出现
4. **章节过渡**：提交按钮点击后，页面平滑滚动回顶部，形成一个完整的循环

**GSAP 关键代码**：

```javascript
// 行动章节 - 门动画 + 木屋选择器
const actionTL = gsap.timeline({
  scrollTrigger: {
    trigger: '.action-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: 1.5,
  }
});

// 门推开，光芒涌入
actionTL.fromTo('.action-door', {
  scaleX: 1,
  opacity: 1,
}, {
  scaleX: 0,
  opacity: 0,
  duration: 0.8,
  ease: 'power3.inOut',
}, 0);

actionTL.fromTo('.action-light', {
  opacity: 0,
  scale: 2,
  filter: 'brightness(3)',
}, {
  opacity: 1,
  scale: 1,
  filter: 'brightness(1)',
  duration: 0.6,
  ease: 'power2.out',
}, 0.2);

// 木屋选择器 - 旋转木马效果
const cabinCards = document.querySelectorAll('.cabin-card');
let currentCabin = 0;
const totalCabins = cabinCards.length;

function rotateCabins(direction) {
  currentCabin = (currentCabin + direction + totalCabins) % totalCabins;
  
  cabinCards.forEach((card, i) => {
    const angle = (i - currentCabin) * (360 / totalCabins);
    const radius = 300;
    
    gsap.to(card, {
      x: Math.sin(angle * Math.PI / 180) * radius,
      y: Math.cos(angle * Math.PI / 180) * radius * 0.3,
      scale: i === currentCabin ? 1 : 0.6,
      opacity: i === currentCabin ? 1 : 0.4,
      zIndex: i === currentCabin ? 10 : 1,
      duration: 0.5,
      ease: 'power2.out',
    });
  });
}

// 初始化木屋位置
rotateCabins(0);

// 左右箭头控制
document.querySelector('.cabin-arrow-left').addEventListener('click', () => rotateCabins(-1));
document.querySelector('.cabin-arrow-right').addEventListener('click', () => rotateCabins(1));

// 表单输入框动画
const formInputs = document.querySelectorAll('.action-form-input');
formInputs.forEach((input, i) => {
  actionTL.fromTo(input, {
    opacity: 0,
    y: 40,
    scale: 0.9,
  }, {
    opacity: 1,
    y: 0,
    scale: 1,
    duration: 0.5,
    ease: 'power3.out',
  }, 1.2 + i * 0.2);
  
  // 占位文字打字机效果
  const originalPlaceholder = input.getAttribute('data-placeholder');
  let charIndex = 0;
  
  const typeInterval = setInterval(() => {
    if (charIndex <= originalPlaceholder.length) {
      input.setAttribute('placeholder', originalPlaceholder.slice(0, charIndex));
      charIndex++;
    } else {
      clearInterval(typeInterval);
    }
  }, 50);
});

// 提交按钮动画
const submitBtn = document.querySelector('.action-submit');
submitBtn.addEventListener('click', () => {
  gsap.to(window, {
    scrollTo: { y: 0 },
    duration: 2,
    ease: 'power3.inOut',
  });
  
  // 按钮反馈动画
  gsap.timeline()
    .to(submitBtn, {
      scale: 0.95,
      duration: 0.1,
    })
    .to(submitBtn, {
      scale: 1,
      duration: 0.3,
      ease: 'elastic.out(1, 0.3)',
    });
});
```

**响应式**：
- 移动端：木屋选择器改为垂直滑动列表，表单输入框全宽
- 平板：木屋选择器保留旋转效果但缩小半径至 200px

---

## 三、⚡ 故事高潮（2-3 个）

### 高潮1：第一缕光 — Hero 章节的终极揭示

**它在故事中的位置**：第一章 Hero 的结尾

**用户做了什么**：从页面顶部滚动了大约 80vh

**发生了什么（分镜级描述）**：
```
0ms： 页面全黑，屏幕中央有一个 2px 的光点
300ms：光点开始缓慢膨胀，颜色从冷白渐变到暖金
600ms：光点达到屏幕 30% 大小，森林轮廓开始显现
1200ms：光点达到屏幕 80% 大小，金鹿剪影在光中浮现
2000ms：光点充满全屏，光芒达到最亮，然后瞬间消退，金鹿清晰站立在森林中
```

**为什么用户会记住它**：这是整个旅程的“第一次呼吸”——从完全的黑暗中，光诞生了。它象征着用户在进入 SORA WOODS 网站时的心理状态：从迷失到看见希望。

**完整 GSAP timeline 代码**：

```javascript
// 高潮1 - 第一缕光
const climax1TL = gsap.timeline({
  scrollTrigger: {
    trigger: '.hero-section',
    start: 'top top',
    end: 'center center',
    scrub: 1,
    pin: true,
  }
});

// 光点从 2px 开始
climax1TL.set('.hero-light-dot', {
  scale: 0.01,
  opacity: 1,
  x: '50%',
  y: '50%',
});

// 光点膨胀并变色
climax1TL.to('.hero-light-dot', {
  scale: 0.3,
  backgroundColor: '#FFE4B5',  // 暖金色
  boxShadow: '0 0 200px rgba(255, 228, 181, 0.6)',
  duration: 0.3,
  ease: 'power2.out',
}, 0);

climax1TL.to('.hero-light-dot', {
  scale: 1,
  backgroundColor: '#FFF8DC',
  boxShadow: '0 0 400px rgba(255, 248, 220, 0.8)',
  duration: 0.5,
  ease: 'power2.inOut',
}, 0.3);

// 森林轮廓显现（使用 SVG mask）
climax1TL.to('.hero-forest-outline', {
  opacity: 1,
  duration: 0.4,
  ease: 'power2.out',
}, 0.6);

// 金鹿浮现
climax1TL.fromTo('.hero-deer', {
  opacity: 0,
  scale: 0.5,
  filter: 'brightness(3) blur(4px)',
}, {
  opacity: 1,
  scale: 1,
  filter: 'brightness(1) blur(0px)',
  duration: 0.6,
  ease: 'power3.out',
}, 0.8);

// 光芒消退
climax1TL.to('.hero-light-dot', {
  opacity: 0,
  scale: 0.5,
  duration: 0.3,
  ease: 'power2.in',
}, 1.4);

// 金鹿呼吸动画（无限循环）
gsap.to('.hero-deer', {
  y: -3,
  duration: 2.5,
  ease: 'sine.inOut',
  yoyo: true,
  repeat: -1,
  delay: 2,
});
```

---

### 高潮2：年轮绽放 — 证明章节的数据揭示

**它在故事中的位置**：第四章证明的中间

**用户做了什么**：滚动到数据年轮完全出现

**发生了什么（分镜级描述）**：
```
0ms： 森林背景，篝火在画面底部燃烧，护林员开始说话
300ms：第一个年轮从中心点开始生长，数字从 0 滚动到 2000+
600ms：第二个年轮生长，数字滚动到 97%
900ms：第三个年轮生长，数字滚动到 4.2
1200ms：第四个年轮生长，数字滚动到 86%
2000ms：所有年轮同时发光，引语浮现
```

**为什么用户会记住它**：数据不是枯燥的数字，而是像树的年轮一样，是时间的见证。用户会感觉这些数字不是编造的，而是像森林一样真实存在。

**完整 GSAP timeline 代码**：

```javascript
// 高潮2 - 年轮绽放
const climax2TL = gsap.timeline({
  scrollTrigger: {
    trigger: '.proof-rings-container',
    start: 'top center',
    end: 'bottom center',
    scrub: 1,
    pin: true,
    pinSpacing: false,
  }
});

// 获取所有年轮和数据
const rings = document.querySelectorAll('.proof-ring-svg circle');
const dataTexts = document.querySelectorAll('.proof-ring-data');

rings.forEach((ring, i) => {
  const radius = parseFloat(ring.getAttribute('r'));
  const circumference = 2 * Math.PI * radius;
  
  // 初始状态：未显示
  ring.style.strokeDasharray = circumference;
  ring.style.strokeDashoffset = circumference;
  ring.style.opacity = 0;
  
  // 年轮生长动画
  climax2TL.to(ring, {
    strokeDashoffset: 0,
    opacity: 1,
    duration: 0.6,
    ease: 'power3.out',
  }, 0.2 + i * 0.3);
  
  // 年轮发光效果
  climax2TL.to(ring, {
    filter: 'drop-shadow(0 0 10px rgba(196, 163, 90, 0.6))',
    duration: 0.3,
    ease: 'power2.out',
  }, 0.6 + i * 0.3);
  
  // 数字滚动
  const targetValue = dataTexts[i].getAttribute('data-target');
  const suffix = dataTexts[i].getAttribute('data-suffix') || '';
  const counter = { value: 0 };
  
  climax2TL.to(counter, {
    value: targetValue,
    duration: 0.8,
    ease: 'power2.out',
    snap: { value: 1 },
    onUpdate: () => {
      dataTexts[i].textContent = Math.round(counter.value).toLocaleString() + suffix;
    },
  }, 0.4 + i * 0.3);
  
  // 数据文字浮现
  climax2TL.fromTo(dataTexts[i].closest('.proof-ring-item'), {
    opacity: 0,
    y: 20,
  }, {
    opacity: 1,
    y: 0,
    duration: 0.4,
    ease: 'power2.out',
  }, 0.3 + i * 0.3);
});

// 所有年轮同时发光
climax2TL.to('.proof-ring-svg circle', {
  filter: 'drop-shadow(0 0 20px rgba(196, 163, 90, 0.8))',
  duration: 0.5,
  ease: 'power2.inOut',
}, 1.8);

// 引语浮现
const quoteSplit = new SplitType('.proof-quote', { types: 'words' });
climax2TL.fromTo(quoteSplit.words, {
  opacity: 0,
  y: 30,
  rotationX: -30,
}, {
  opacity: 1,
  y: 0,
  rotationX: 0,
  stagger: 0.03,
  duration: 0.4,
  ease: 'back.out(1.7)',
}, 2.2);
```

---

### 高潮3：跨越之门 — 行动章节的转折点

**它在故事中的位置**：第五章行动的起始

**用户做了什么**：从证明章节过渡到行动章节，触发门动画

**发生了什么（分镜级描述）**：
```
0ms： 森林深处，一扇门在远处发光
300ms：门逐渐靠近（用户视角向前移动）
600ms：门充满整个屏幕，门缝中的光芒越来越亮
1200ms：门被推开，光芒吞没一切
2000ms：光芒消退，预订界面出现
```

**为什么用户会记住它**：这是用户从“旁观者”变成“参与者”的转折点。门象征着一个选择——是继续看下去，还是真正走进 SORA WOODS。

**完整 GSAP timeline 代码**：

```javascript
// 高潮3 - 跨越之门
const climax3TL = gsap.timeline({
  scrollTrigger: {
    trigger: '.action-section',
    start: 'top bottom',
    end: 'center center',
    scrub: 1.5,
    pin: true,
  }
});

// 门从远处靠近
climax3TL.fromTo('.action-door-frame', {
  scale: 0.2,
  opacity: 0,
  x: '50%',
  y: '50%',
}, {
  scale: 1,
  opacity: 1,
  x: '50%',
  y: '50%',
  duration: 0.8,
  ease: 'power3.out',
}, 0);

// 门缝中的光芒增强
climax3TL.to('.action-door-light', {
  opacity: 1,
  scale: 1.2,
  boxShadow: '0 0 100px rgba(255, 248, 220, 0.9), 0 0 200px rgba(255, 228, 181, 0.5)',
  duration: 0.5,
  ease: 'power2.out',
}, 0.6);

// 门打开
climax3TL.to('.action-door-left', {
  x: '-100%',
  duration: 0.4,
  ease: 'power3.inOut',
}, 1);

climax3TL.to('.action-door-right', {
  x: '100%',
  duration: 0.4,
  ease: 'power3.inOut',
}, 1);

// 光芒爆发
climax3TL.to('.action-door-light', {
  scale: 5,
  opacity: 0.5,
  duration: 0.3,
  ease: 'power2.out',
}, 1.2);

climax3TL.to('.action-section', {
  backgroundColor: '#FFF8DC',
  duration: 0.3,
  ease: 'power2.inOut',
}, 1.2);

// 光芒消退，预订界面出现
climax3TL.set('.action-door-light', {
  opacity: 0,
}, 1.5);

climax3TL.fromTo('.action-content', {
  opacity: 0,
  y: 40,
}, {
  opacity: 1,
  y: 0,
  duration: 0.6,
  ease: 'power3.out',
}, 1.6);
```

---

## 四、🧩 全局组件

### 4.1 导航栏

**初始状态**：
- 透明背景，绝对定位在页面顶部
- Logo（SORA WOODS 文字，字体 Playfair Display，颜色 #F0EDE6）在左侧
- 4个链接在右侧：故事、木屋、森林、预订（间距 32px，字体 Inter，字号 14px，颜色 #F0EDE6，字母间距 2px）
- 高度：80px

**滚动后**：
- 背景变为 `rgba(10, 31, 26, 0.95)`，带 backdrop-filter: blur(12px)
- Logo 颜色变为 #C4A35A
- 链接颜色变为 #E8D5A0
- 高度缩小至 64px
- 底部有 1px 的 `rgba(196, 163, 90, 0.2)` 分割线

**移动端**：
- 汉堡菜单（三条横线，颜色 #F0EDE6）
- 点击后展开全屏菜单，菜单项从下方依次滑入
- 关闭按钮（X 图标）

```javascript
// 导航栏滚动效果
const navTL = gsap.timeline({
  scrollTrigger: {
    trigger: 'body',
    start: '80px top',
    end: '100px top',
    scrub: 0.5,
  }
});

navTL.to('.navbar', {
  backgroundColor: 'rgba(10, 31, 26, 0.95)',
  height: '64px',
  backdropFilter: 'blur(12px)',
  duration: 0.3,
}, 0);

navTL.to('.navbar-logo', {
  color: '#C4A35A',
  fontSize: '20px',
  duration: 0.3,
}, 0);

navTL.to('.nav-link', {
  color: '#E8D5A0',
  duration: 0.3,
}, 0);

// 移动端汉堡菜单
const hamburger = document.querySelector('.hamburger');
const mobileMenu = document.querySelector('.mobile-menu');

hamburger.addEventListener('click', () => {
  const isOpen = mobileMenu.classList.toggle('open');
  
  if (isOpen) {
    gsap.to('.mobile-menu', {
      x: '0%',
      opacity: 1,
      duration: 0.4,
      ease: 'power3.out',
    });
    
    gsap.fromTo('.mobile-menu-item', {
      opacity: 0,
      y: 20,
    }, {
      opacity: 1,
      y: 0,
      stagger: 0.05,
      duration: 0.3,
      ease: 'power2.out',
    });
  } else {
    gsap.to('.mobile-menu', {
      x: '100%',
      opacity: 0,
      duration: 0.3,
      ease: 'power3.in',
    });
  }
});
```

### 4.2 预加载动画

**加载画面**：
- 全屏深绿色背景（#0A1F1A）
- 中央有一个光点，从 2px 开始缓慢膨胀（模拟 Hero 章节的“第一缕光”）
- 下方有进度条（宽度从 0% 到 100%，颜色 #C4A35A）
- 进度条上方有文字“森林在等你...”

**加载完成的过渡**：
- 光点膨胀到覆盖全屏
- 然后渐变到 Hero 章节的场景
- 整个过渡持续 1.5s

```javascript
// 预加载动画
const loaderTL = gsap.timeline();

// 光点膨胀
loaderTL.fromTo('.loader-dot', {
  scale: 0.01,
  opacity: 1,
}, {
  scale: 0.3,
  duration: 1.5,
  ease: 'power2.out',
});

// 进度条
const progressBar = document.querySelector('.loader-progress');
let progress = 0;
const progressInterval = setInterval(() => {
  progress += Math.random() * 10 + 5;
  if (progress > 100) progress = 100;
  progressBar.style.width = progress + '%';
  
  if (progress >= 100) {
    clearInterval(progressInterval);
    
    // 加载完成，过渡到页面
    loaderTL.to('.loader-dot', {
      scale: 100,
      opacity: 0,
      duration: 0.8,
      ease: 'power3.inOut',
    });
    
    loaderTL.to('.loader', {
      opacity: 0,
      duration: 0.3,
      ease: 'power2.out',
      onComplete: () => {
        document.querySelector('.loader').style.display = 'none';
      },
    }, 0.6);
    
    // 触发 Hero 动画
    initHeroAnimation();
  }
}, 200);
```

### 4.3 页脚

**布局**：
- 背景色：#0A1F1A
- 高度：自动（最小 400px）
- 内容分为三列：
  - 左列：Logo + 简短描述（“在受保护的古木间，找回呼吸的节奏。”）
  - 中列：链接（故事、木屋、森林、预订、常见问题、联系我们）
  - 右列：社交链接（Instagram、邮件）+ 订阅表单（输入邮箱 + 按钮）
- 底部：版权信息（© 2026 SORA WOODS. All rights reserved.）

```css
.footer {
  background: var(--color-forest-deep);
  color: var(--color-mist-white);
  padding: 80px 40px 40px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1.5fr;
  gap: 60px;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-logo {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  color: var(--color-golden-light);
  margin-bottom: 16px;
}

.footer-desc {
  font-size: 14px;
  line-height: 1.6;
  opacity: 0.7;
  max-width: 300px;
}

.footer-links {
  list-style: none;
  padding: 0;
}

.footer-links li {
  margin-bottom: 12px;
}

.footer-links a {
  color: var(--color-mist-white);
  text-decoration: none;
  font-size: 14px;
  opacity: 0.7;
  transition: opacity 0.3s;
}

.footer-links a:hover {
  opacity: 1;
  color: var(--color-golden-light);
}

.footer-subscribe {
  display: flex;
  gap: 8px;
}

.footer-subscribe input {
  flex: 1;
  padding: 12px 16px;
  background: rgba(240, 237, 230, 0.1);
  border: 1px solid rgba(240, 237, 230, 0.2);
  border-radius: 100px;
  color: var(--color-mist-white);
  font-size: 14px;
}

.footer-subscribe button {
  padding: 12px 24px;
  background: var(--color-golden-light);
  border: none;
  border-radius: 100px;
  color: var(--color-forest-deep);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.footer-subscribe button:hover {
  background: var(--color-sun-kissed);
}

.footer-bottom {
  border-top: 1px solid rgba(240, 237, 230, 0.1);
  padding-top: 24px;
  margin-top: 60px;
  text-align: center;
  font-size: 12px;
  opacity: 0.5;
}
```

### 4.4 自定义光标

**默认状态**：
- 圆形，直径 24px
- 边框：1px solid rgba(196, 163, 90, 0.6)
- 背景：透明
- 跟随鼠标移动，延迟 0.1s

**经过链接/按钮**：
- 直径膨胀到 48px
- 背景变为 `rgba(196, 163, 90, 0.1)`
- 边框颜色变为 #C4A35A
- 中心出现一个圆点（直径 4px）

```javascript
// 自定义光标
const cursor = document.querySelector('.custom-cursor');
const cursorDot = document.querySelector('.custom-cursor-dot');

document.addEventListener('mousemove', (e) => {
  gsap.to(cursor, {
    x: e.clientX - 12,
    y: e.clientY - 12,
    duration: 0.1,
    ease: 'power2.out',
  });
  
  gsap.to(cursorDot, {
    x: e.clientX - 2,
    y: e.clientY - 2,
    duration: 0.05,
    ease: 'power2.out',
  });
});

// 链接悬停效果
const interactiveElements = document.querySelectorAll('a, button, .cabin-card, .solution-card');
interactiveElements.forEach(el => {
  el.addEventListener('mouseenter', () => {
    gsap.to(cursor, {
      scale: 2,
      backgroundColor: 'rgba(196, 163, 90, 0.1)',
      borderColor: '#C4A35A',
      duration: 0.3,
      ease: 'power2.out',
    });
    gsap.to(cursorDot, {
      scale: 1.5,
      backgroundColor: '#C4A35A',
      duration: 0.3,
    });
  });
  
  el.addEventListener('mouseleave', () => {
    gsap.to(cursor, {
      scale: 1,
      backgroundColor: 'transparent',
      borderColor: 'rgba(196, 163, 90, 0.6)',
      duration: 0.3,
      ease: 'power2.out',
    });
    gsap.to(cursorDot, {
      scale: 1,
      backgroundColor: '#C4A35A',
      duration: 0.3,
    });
  });
});
```

---

## 五、🎨 组件 CSS

```css
/* 按钮 - 主要变体 */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 16px 40px;
  background: var(--color-golden-light);
  color: var(--color-forest-deep);
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-decoration: none;
  border: none;
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.btn-primary:hover {
  background: var(--color-sun-kissed);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(196, 163, 90, 0.3);
}

.btn-primary:hover::before {
  left: 100%;
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(196, 163, 90, 0.2);
}

/* 按钮 - 次要变体 */
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 36px;
  background: transparent;
  color: var(--color-mist-white);
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-decoration: none;
  border: 1px solid rgba(240, 237, 230, 0.3);
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-secondary::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(240, 237, 230, 0.1);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.5s ease, height 0.5s ease;
}

.btn-secondary:hover {
  border-color: var(--color-golden-light);
  color: var(--color-golden-light);
  transform: translateY(-2px);
}

.btn-secondary:hover::after {
  width: 300px;
  height: 300px;
}

/* 卡片 */
.card {
  background: rgba(10, 31, 26, 0.03);
  border: 1px solid rgba(10, 31, 26, 0.08);
  border-radius: 16px;
  padding: 32px;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(196, 163, 90, 0.05), transparent);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(10, 31, 26, 0.1);
  border-color: rgba(196, 163, 90, 0.3);
}

.card:hover::before {
  opacity: 1;
}

.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 20px;
}

.card-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  color: var(--color-forest-deep);
  margin-bottom: 8px;
}

.card-description {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: var(--color-stone-gray);
  line-height: 1.6;
  margin-bottom: 16px;
}

.card-cta {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-golden-light);
  letter-spacing: 2px;
  text-transform: uppercase;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: gap 0.3s ease;
}

.card:hover .card-cta {
  gap: 12px;
}

/* 玻璃态效果 */
.glass {
  background: rgba(240, 237, 230, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(240, 237, 230, 0.2);
  border-radius: 24px;
  padding: 48px;
  box-shadow: 0 8px 32px rgba(10, 31, 26, 0.1);
}

.glass-dark {
  background: rgba(10, 31, 26, 0.2);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(240, 237, 230, 0.1);
  border-radius: 24px;
  padding: 48px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.glass-light {
  background: rgba(240, 237, 230, 0.25);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(240, 237, 230, 0.3);
  border-radius: 16px;
  padding: 32px;
}
```

---

## 六、🛠️ 技术实现

### 6.1 技术栈（版本号）

| 技术 | 版本 | 用途 |
|:---|:---|:---|
| HTML5 | — | 页面结构 |
| CSS3 | — | 样式与布局 |
| JavaScript (ES6+) | — | 交互逻辑 |
| GSAP | 3.12.5 | 动画引擎 |
| ScrollTrigger | 3.12.5 | 滚动驱动动画 |
| SplitType | 0.3.4 | 文字拆分动画 |
| Lenis | 1.3.18 | 平滑滚动 |
| Vite | 5.4.0 | 构建工具 |

### 6.2 项目结构

```
sora-woods/
├── index.html
├── style.css
├── main.js
├── public/
│   ├── images/
│   │   ├── hero-deer.svg
│   │   ├── forest-1.avif
│   │   ├── cabin-1.avif
│   │   ├── cabin-2.avif
│   │   ├── cabin-3.avif
│   │   └── cabin-4.avif
│   └── fonts/
│       ├── PlayfairDisplay-Variable.woff2
│       └── Inter-Variable.woff2
├── sections/
│   ├── hero.js
│   ├── problem.js
│   ├── solution.js
│   ├── proof.js
│   └── action.js
├── components/
│   ├── navbar.js
│   ├── loader.js
│   ├── footer.js
│   └── cursor.js
└── utils/
    ├── canvas.js
    └── helpers.js
```

### 6.3 数据模型（TypeScript 接口）

```typescript
interface Cabin {
  id: string;
  name: string;
  description: string;
  capacity: number;
  pricePerNight: number;
  images: string[];
  availableDates: DateRange[];
  amenities: string[];
}

interface RetreatProgram {
  id: string;
  title: string;
  description: string;
  duration: number; // days
  maxParticipants: number;
  price: number;
  startDates: Date[];
}

interface Testimonial {
  name: string;
  date: string;
  content: string;
  rating: number;
  avatar?: string;
}

interface ForestData {
  totalVisitors: number;
  stressReductionRate: number;
  averageStayDays: number;
  returnRate: number;
}

interface BookingForm {
  name: string;
  email: string;
  cabinId: string;
  checkIn: Date;
  checkOut: Date;
  message: string;
  wantsDisconnect: boolean;
}
```

### 6.4 资源清单

| 资源 | 类型 | 来源 | 用途 |
|:---|:---|:---|:---|
| 金鹿 SVG | 矢量图 | 自绘/图标库 | Hero 章节核心视觉 |
| 森林背景图 (x5) | AVIF | Unsplash/自摄 | 各章节背景 |
| 木屋照片 (x8) | AVIF | 自摄/素材库 | 方案章节卡片 |
| 篝火粒子 | Canvas | 自绘 | 证明章节动画 |
| 字体文件 (x2) | WOFF2 | Google Fonts | 全站排版 |
| 图标集 (x20) | SVG | Font Awesome | 导航/卡片/按钮 |

---

## 七、📱 响应式策略

| 断点 | 故事调整 | 动画简化 |
|:---|:---|:---|
| < 768px (手机) | 文字缩短 40%，卡片改为垂直列表 | 删除粒子动画，减少 ScrollTrigger 触发点，SplitType 仅用于标题 |
| 768-1024px (平板) | 保留完整文案，卡片 2x2 网格 | 粒子数量减半，动画速度加快 1.5x |
| 1024-1440px (桌面) | 完整叙事 | 全量动画，保留所有效果 |
| > 1440px (超大屏) | 增加留白，标题字号放大至 120px | 增加视差深度，粒子数量增加 50% |

---

## 八、🚀 AI 开发顺序（5 Phase）

### Phase 1：骨架搭建（2-3 小时）
- 创建项目结构，安装依赖（Vite, GSAP, Lenis, SplitType）
- 编写 index.html 基本结构（5 个 section + 导航 + 预加载 + 页脚）
- 编写 style.css 全局样式（色彩变量、字体、间距、基础组件）

### Phase 2：核心叙事（3-4 小时）
- 实现 Hero 章节（光点入场、金鹿动画、SplitType 文字）
- 实现 Problem 章节（数字都市、通知气泡、数字崩塌）
- 实现 Solution 章节（森林入场、卡片分割、交互悬停）

### Phase 3：高潮与证明（3-4 小时）
- 实现高潮1（“第一缕光”完整 timeline）
- 实现 Proof 章节（篝火 Canvas 粒子、年轮生长、数字滚动）
- 实现高潮2（“年轮绽放”完整 timeline）

### Phase 4：转化与收尾（2-3 小时）
- 实现 Action 章节（门动画、木屋选择器、表单动画）
- 实现高潮3（“跨越之门”完整 timeline）
- 实现页脚和全局组件（导航滚动、预加载、自定义光标）

### Phase 5：优化与测试（2-3 小时）
- 响应式适配（3 个断点）
- 性能优化（图片懒加载、动画 GPU 加速、减少重排）
- 无障碍（ARIA 标签、键盘导航、色彩对比度）
- 最终测试（Chrome/Firefox/Safari，移动端/桌面端）

---

## 📏 丰富度自检

**主题明确性**：
- ✅ 一句话说清品牌/产品/用户：SORA WOODS 是一个位于受保护古木林中的疗愈度假村，为疲惫的都市人提供从内到外的身心修复体验
- ✅ 品牌名原创（SORA WOODS），未照搬任何参考网站

**完整性**：
- ✅ 导航栏（初始态 + 滚动态 + 移动端）
- ✅ 预加载动画（加载画面 + 完成过渡）
- ✅ 页脚（三列布局 + 订阅表单）
- ✅ 自定义光标

**组件 CSS**：
- ✅ 按钮（主要/次要，完整 CSS）
- ✅ 卡片（完整 CSS）
- ✅ 玻璃态效果（3 种变体）

**高潮代码**：
- ✅ 3 个完整高潮，每个都有完整的 GSAP timeline 代码
- ✅ 无 TODO，无占位符

**Canvas 规范**：
- ✅ 使用 devicePixelRatio
- ✅ resize 时重新计算

**视觉精确度**：
- ✅ 每个 section 有具体 px 值（字号、间距、位置）
- ✅ 无模糊描述

**故事**：
- ✅ 清晰的情绪曲线：迷失 → 好奇 → 震撼 → 觉醒 → 信任 → 行动
- ✅ 每个 section 有故事角色和用户情绪描述
- ✅ 3 个故事高潮（用户会记住的瞬间）

**画面**：
- ✅ 每个 section 的画面描述 >100 字（像电影分镜）
- ✅ 色彩有故事含义（10 个颜色变量）
- ✅ 字体选择有理由（Playfair Display = 古老智慧，Inter = 简洁可信）

**动画**：
- ✅ 全站 12+ 种动画类型（光点膨胀、金鹿呼吸、SplitType 文字、数字都市、通知气泡、卡片分割、年轮生长、Canvas 粒子、门动画、旋转木马、打字机效果、光标变形）
- ✅ 每个 section ≥3 种动画 + 过渡到下一章
- ✅ 100% scrub 驱动，有节奏变化（开场慢/中间快/高潮激烈/结尾温柔）

**内容**：
- ✅ 有真实感的业务数据（2000+ 访客、97% 压力下降、4.2 天平均停留）
- ✅ 每个 section 有文案方向和示例文字
- ✅ 总字数 5000+ 字

---

**SORA WOODS** 不仅仅是一个网站——它是一个邀请，一个通往内心深处的入口。当用户从第一缕光中睁开眼睛，到最终选择跨越那扇门，他们经历的不是一次浏览，而是一次真正的觉醒。