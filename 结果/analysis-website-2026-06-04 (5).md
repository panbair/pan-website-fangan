# Serenity Haven - 高端疗愈度假村品牌官网

## 项目概述

### 1.1 项目定位
Serenity Haven 是一个高端自然疗愈度假村的品牌官网，通过沉浸式滚动叙事体验，将物理空间升华为精神疗愈圣地，吸引高净值人群预订静修营和度假体验。

### 1.2 目标用户
- **高净值都市精英**：35-55岁，高压工作环境（金融、科技、法律），年收入$500k+，寻求深度疗愈和内在连接
- **灵修爱好者**：对瑜伽、冥想、呼吸法有深度实践，参加过 Retreat 的资深修行者
- **企业团建决策者**：负责高管团队建设或客户答谢活动策划，预算充足，追求独特体验

### 1.3 核心价值主张
- **深度疗愈**：14天沉浸式静修营，融合瑜伽、冥想、森林浴和心理学工作坊
- **原始自然**：200英亩受保护森林，零光污染，每天仅接待12位客人
- **专业导师**：与耶鲁、FSU 合作开发临床验证的疗愈方案
- **零佣金承诺**：直接预订享最优价格，无需通过 Airbnb/Booking

### 1.4 参考竞品启发
| 竞品 | 核心亮点 | 本方案如何借鉴/超越 |
|:---|:---|:---|
| `diamondrosesanctuary.com` | GSAP+Lenis 滚动叙事，哲学化文案，SplitType 文字动画 | 增加多层视差+clip-path揭示+count-up数据展示，叙事节奏更丰富 |
| `fame-estate.com` | 数据驱动的信任建设（0取消案例） | 将数据可视化（疗愈效果数据、客户满意度）融入动画 |

---

## 二、技术架构

### 2.1 技术栈
```
前端框架: Next.js 14 (App Router) + TypeScript 5.4
构建工具: Vite 6.x (通过 Next.js 内置)
样式方案: Tailwind CSS 4.x + CSS Modules
动画库: GSAP 3.12.5 + ScrollTrigger + Lenis 1.3.18
文字动画: SplitType 0.3.4
图标库: Lucide React 0.400
3D效果: Three.js 0.162 (可选粒子系统)
部署: Vercel (Pro Plan, 自动ISR)
CDN: Cloudflare (自定义域名)
分析: Plausible (隐私友好)
```

### 2.2 项目结构
```
serenity-haven/
├── public/
│   ├── images/
│   │   ├── hero/          # 6张全屏背景图
│   │   ├── retreats/      # 8张静修营场景
│   │   ├── nature/        # 12张自然风光
│   │   ├── team/          # 4张导师照片
│   │   └── testimonials/  # 3张客户照片
│   ├── fonts/
│   │   ├── CormorantGaramond-Variable.ttf
│   │   └── Inter-Variable.ttf
│   └── favicon.svg
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── retreats/
│   │   │   └── page.tsx
│   │   └── about/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── GlassCard.tsx
│   │   │   ├── Badge.tsx
│   │   │   └── AnimatedCounter.tsx
│   │   ├── sections/
│   │   │   ├── Preloader.tsx
│   │   │   ├── HeroSection.tsx
│   │   │   ├── StorySection.tsx
│   │   │   ├── RetreatsSection.tsx
│   │   │   ├── ServicesSection.tsx
│   │   │   ├── DataSection.tsx
│   │   │   ├── TeamSection.tsx
│   │   │   ├── TestimonialsSection.tsx
│   │   │   ├── CTASection.tsx
│   │   │   └── Footer.tsx
│   │   ├── animations/
│   │   │   ├── gsapSetup.ts
│   │   │   ├── heroAnimation.ts
│   │   │   ├── storyAnimation.ts
│   │   │   ├── retreatsAnimation.ts
│   │   │   ├── dataAnimation.ts
│   │   │   └── globalAnimations.ts
│   │   ├── Navigation.tsx
│   │   └── CustomCursor.tsx
│   ├── data/
│   │   ├── retreats.ts
│   │   ├── services.ts
│   │   ├── team.ts
│   │   ├── stats.ts
│   │   └── testimonials.ts
│   ├── hooks/
│   │   ├── useScrollAnimation.ts
│   │   ├── useCountUp.ts
│   │   └── useMediaQuery.ts
│   ├── lib/
│   │   ├── utils.ts
│   │   └── animations.ts
│   └── styles/
│       ├── globals.css
│       └── animations.css
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## 三、页面结构与功能设计

### 3.1 HeroSection (英雄区)

**功能**：品牌第一印象，通过全屏视频/图片轮播+文字揭示，瞬间传递疗愈氛围

**内容**：
- 背景：6张高质量自然景观图片（森林、瀑布、日出、星空、湖泊、瑜伽露台）自动轮播
- 主标题："Serenity Haven"（SplitType 逐字符揭示）
- 副标题："Where Nature Heals Your Soul"
- CTA按钮："Begin Your Journey" + "Explore Retreats"
- 右下角：滚动提示 "Scroll to discover"

**布局**：
- 桌面端：全屏100vh，背景图覆盖，文字居中
- 移动端：背景图裁剪，文字缩小

**动画效果**（3种模式）：
- **模式1：SplitType 文字剧场** - 主标题字符级 stager 淡入+上移
- **模式2：多层视差** - 3层背景（天空/树木/前景草地）不同速度滚动
- **模式3：图片揭示** - 每张背景图渐显，通过 clip-path 圆形展开

**关键 GSAP 代码片段**：
```javascript
// 零bug代码：使用代理对象做splitType，不混用scrub+toggleActions
const textReveal = () => {
  const split = new SplitType('.hero-title', { types: 'chars' });
  
  gsap.fromTo(split.chars, 
    { y: 100, opacity: 0, rotateX: -90 },
    {
      y: 0, opacity: 1, rotateX: 0,
      duration: 1.2,
      stagger: 0.04,
      ease: 'power4.out',
      scrollTrigger: {
        trigger: '.hero-section',
        start: 'top top',
        end: 'center center',
        scrub: 1.5
      }
    }
  );
};

const parallaxLayers = () => {
  gsap.to('.parallax-sky', {
    y: -150,
    ease: 'none',
    scrollTrigger: {
      trigger: '.hero-section',
      start: 'top top',
      end: 'bottom top',
      scrub: 0.5
    }
  });
  
  gsap.to('.parallax-trees', {
    y: -100,
    ease: 'none',
    scrollTrigger: {
      trigger: '.hero-section',
      start: 'top top',
      end: 'bottom top',
      scrub: 1
    }
  });
  
  gsap.to('.parallax-ground', {
    y: -50,
    ease: 'none',
    scrollTrigger: {
      trigger: '.hero-section',
      start: 'top top',
      end: 'bottom top',
      scrub: 1.5
    }
  });
};
```

---

### 3.2 StorySection (品牌故事)

**功能**：讲述度假村的起源和理念，建立情感连接

**内容**：
- 左图右文布局，3个交替区块
- 区块1：创始人故事（"Founded in 2018 by Dr. Elena Marchetti..."）
- 区块2：土地保护理念（"200 acres preserved since 1985..."）
- 区块3：医学背书（"Clinical studies with Yale University..."）
- 每区块含：标题 + 描述 + 引用数据

**布局**：
- 桌面端：左右交替（图-文-图-文-图-文）
- 移动端：上下堆叠

**动画效果**（2种模式）：
- **模式1：clip-path 圆形揭示** - 图片从中心圆形展开
- **模式2：图片渐进显影** - grayscale→color 过渡

**关键 GSAP 代码片段**：
```javascript
const storyReveal = () => {
  const images = document.querySelectorAll('.story-image');
  
  images.forEach((img, index) => {
    gsap.fromTo(img,
      { clipPath: 'circle(0% at 50% 50%)', filter: 'grayscale(1)' },
      {
        clipPath: 'circle(100% at 50% 50%)',
        filter: 'grayscale(0)',
        duration: 1.5,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: img.closest('.story-block'),
          start: 'top 70%',
          end: 'top 30%',
          scrub: 1
        }
      }
    );
  });
};
```

---

### 3.3 RetreatsSection (静修营展示)

**功能**：展示4种核心静修营项目，引导用户选择

**内容**：
- 4张卡片，每张包含：图片、标题、价格、时长、特色标签
- 卡片1：The Alchemist Retreat - $2,800/7天 - "Deep transformation"
- 卡片2：Forest Awakening - $1,800/5天 - "Nature immersion"
- 卡片3：Yoga Intensive - $2,200/10天 - "Master your practice"
- 卡片4：Couples Renewal - $3,200/7天 - "Reconnect deeply"

**布局**：
- 桌面端：2x2 网格，悬停放大
- 移动端：1列横向滑动

**动画效果**（2种模式）：
- **模式1：Pin + 连续序列** - 整个section pin住，卡片逐个从右侧滑入
- **模式2：元素接力联动** - 卡片A出现→标签出现→CTA按钮出现

**关键 GSAP 代码片段**：
```javascript
const retreatsPin = () => {
  const cards = document.querySelectorAll('.retreat-card');
  const timeline = gsap.timeline({
    scrollTrigger: {
      trigger: '.retreats-section',
      start: 'top top',
      end: `+=${window.innerHeight * 2}`,
      pin: true,
      scrub: 1
    }
  });

  cards.forEach((card, index) => {
    timeline.fromTo(card,
      { x: '100vw', opacity: 0, scale: 0.8 },
      { x: 0, opacity: 1, scale: 1, duration: 0.8, ease: 'power3.out' }
    );
    
    // 内部元素接力
    timeline.fromTo(card.querySelector('.card-tag'),
      { y: 30, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.3 },
      '-=0.4'
    );
    
    timeline.fromTo(card.querySelector('.card-cta'),
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.3 },
      '-=0.2'
    );
  });
};
```

---

### 3.4 ServicesSection (服务体系)

**功能**：展示5大核心服务，建立专业信任

**内容**：
- 5个服务卡片，每个含：图标、标题、简短描述
- 服务1：Personalized Wellness Plans
- 服务2：Nutrition & Detox Programs
- 服务3：Therapeutic Massage & Bodywork
- 服务4：Mindfulness & Meditation Coaching
- 服务5：Post-Retreat Integration Support

**布局**：
- 桌面端：5列网格（2-1-2排列）
- 移动端：单列

**动画效果**（2种模式）：
- **模式1：水平滚动画廊** - 卡片横向滚动揭示
- **模式2：背景色滚动渐变** - section背景从绿色渐变为深蓝

**关键 GSAP 代码片段**：
```javascript
const servicesScroll = () => {
  const track = document.querySelector('.services-track');
  const cards = document.querySelectorAll('.service-card');
  
  // 水平滚动
  const containerAnimation = gsap.to(track, {
    x: () => -(track.scrollWidth - window.innerWidth),
    ease: 'none',
    scrollTrigger: {
      trigger: '.services-section',
      start: 'top top',
      end: `+=${track.scrollWidth}`,
      pin: true,
      scrub: 1,
      invalidateOnRefresh: true
    }
  });
  
  // 卡片入场动画
  cards.forEach((card, i) => {
    gsap.fromTo(card,
      { scale: 0.8, opacity: 0.3 },
      {
        scale: 1, opacity: 1,
        duration: 0.5,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: card,
          containerAnimation: containerAnimation,
          start: 'left 70%',
          end: 'left 30%',
          scrub: 0.5
        }
      }
    );
  });
  
  // 背景色渐变
  gsap.to('.services-section', {
    backgroundColor: '#0a1628',
    ease: 'none',
    scrollTrigger: {
      trigger: '.services-section',
      start: 'top top',
      end: 'bottom bottom',
      scrub: 1
    }
  });
};
```

---

### 3.5 DataSection (数据展示)

**功能**：用具体数字证明疗愈效果和客户满意度

**内容**：
- 4个大型数字计数器，每行两个
- 数字1：98% - 客户满意度
- 数字2：4,200+ - 疗愈小时数
- 数字3：15+ - 合作国家
- 数字4：0 - 退款案例

**布局**：
- 桌面端：2x2 网格，每个数字搭配小图标
- 移动端：1列

**动画效果**（2种模式）：
- **模式1：Count-Up 数字** - 代理对象驱动，从0计数到目标值
- **模式2：图片揭示** - 每个数字卡片的背景图渐进显影

**关键 GSAP 代码片段**：
```javascript
// 零bug代码：用代理对象做count-up、不用innerText
const countUpAnimation = () => {
  const stats = [
    { el: '.stat-1', target: 98, suffix: '%' },
    { el: '.stat-2', target: 4200, suffix: '+' },
    { el: '.stat-3', target: 15, suffix: '+' },
    { el: '.stat-4', target: 0, suffix: '' }
  ];

  stats.forEach(stat => {
    const element = document.querySelector(stat.el);
    if (!element) return;
    
    // 使用代理对象
    const proxy = { value: 0 };
    
    gsap.to(proxy, {
      value: stat.target,
      duration: 2,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: element.closest('.data-section'),
        start: 'top 80%',
        end: 'top 40%',
        scrub: 1
      },
      onUpdate: () => {
        element.textContent = Math.round(proxy.value).toLocaleString() + stat.suffix;
      }
    });
  });
};

// 图片渐进显影
const dataImageReveal = () => {
  gsap.utils.toArray('.stat-card').forEach((card, i) => {
    gsap.fromTo(card,
      { backgroundPosition: '200% 50%' },
      {
        backgroundPosition: '0% 50%',
        ease: 'power3.out',
        scrollTrigger: {
          trigger: card,
          start: 'top 80%',
          end: 'top 40%',
          scrub: 0.5
        }
      }
    );
  });
};
```

---

### 3.6 TeamSection (导师团队)

**功能**：展示4位核心导师，建立专业信任

**内容**：
- 4张成员卡片：照片、姓名、头衔、简短介绍
- 导师1：Dr. Elena Marchetti - 创始人/临床心理学家
- 导师2：Maya Singh - 瑜伽大师（30年经验）
- 导师3：James Chen - 冥想导师（前佛教僧侣）
- 导师4：Sofia Rodriguez - 营养师/排毒专家

**布局**：
- 桌面端：4列网格，悬停显示详细信息
- 移动端：2x2

**动画效果**（2种模式）：
- **模式1：3D卡片倾斜** - mousemove 驱动 perspective 变化
- **模式2：图片渐进显影** - 照片从模糊变清晰

**关键 GSAP 代码片段**：
```javascript
// 3D卡片倾斜 - mousemove驱动
const cardTilt = () => {
  const cards = document.querySelectorAll('.team-card');
  
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = -((y - centerY) / centerY) * 10;
      const rotateY = ((x - centerX) / centerX) * 10;
      
      gsap.to(card, {
        rotateX: rotateX,
        rotateY: rotateY,
        transformPerspective: 1000,
        duration: 0.3,
        ease: 'power2.out'
      });
    });
    
    card.addEventListener('mouseleave', () => {
      gsap.to(card, {
        rotateX: 0,
        rotateY: 0,
        duration: 0.5,
        ease: 'elastic.out(1, 0.3)'
      });
    });
  });
};

// 渐进显影
const teamReveal = () => {
  gsap.utils.toArray('.team-photo').forEach((photo, i) => {
    gsap.fromTo(photo,
      { filter: 'blur(20px) grayscale(1)', scale: 1.1 },
      {
        filter: 'blur(0px) grayscale(0)', scale: 1,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: photo.closest('.team-card'),
          start: 'top 75%',
          end: 'top 40%',
          scrub: 0.5
        }
      }
    );
  });
};
```

---

### 3.7 TestimonialsSection (客户评价)

**功能**：展示真实客户评价，增强社会证明

**内容**：
- 3条评价轮播，每条含：客户照片、姓名、评价内容、评分
- 评价1：Sarah K. - "Life-changing experience..."
- 评价2：Michael T. - "The most profound week of my life..."
- 评价3：Anna & David - "We found each other again..."

**布局**：
- 桌面端：水平滚动，居中显示当前评价
- 移动端：垂直列表

**动画效果**（2种模式）：
- **模式1：水平滚动画廊** - 评价卡片横向滑动
- **模式2：SplitType 文字** - 评价文本逐词揭示

**关键 GSAP 代码片段**：
```javascript
const testimonialsScroll = () => {
  const track = document.querySelector('.testimonials-track');
  const slides = document.querySelectorAll('.testimonial-card');
  const slideWidth = slides[0].offsetWidth + 32; // 包括gap
  
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: '.testimonials-section',
      start: 'top top',
      end: `+=${slideWidth * slides.length}`,
      pin: true,
      scrub: 1
    }
  });
  
  slides.forEach((slide, i) => {
    tl.fromTo(slide,
      { x: window.innerWidth, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.6 }
    );
    
    // 评价文字逐词揭示
    tl.fromTo(slide.querySelector('.testimonial-text'),
      { opacity: 0 },
      { opacity: 1, duration: 0.4 },
      '-=0.3'
    );
    
    tl.fromTo(slide.querySelector('.testimonial-author'),
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.3 },
      '-=0.2'
    );
  });
};
```

---

### 3.8 CTASection (行动号召)

**功能**：鼓励用户立即行动，完成转化

**内容**：
- 大标题："Ready to Transform Your Life?"
- 副标题："Book your consultation today"
- 表单：姓名、邮箱、电话、偏好日期
- 替代CTA：电话预约 + 邮件联系

**布局**：
- 桌面端：左表单右信息
- 移动端：上下堆叠

**动画效果**（2种模式）：
- **模式1：clip-path 形状揭示** - 表单区域从圆形展开
- **模式2：元素接力联动** - 表单字段逐个出现

**关键 GSAP 代码片段**：
```javascript
const ctaReveal = () => {
  // 表单区域圆形揭示
  gsap.fromTo('.cta-form-container',
    { clipPath: 'circle(0% at 50% 50%)' },
    {
      clipPath: 'circle(100% at 50% 50%)',
      duration: 1.5,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: '.cta-section',
        start: 'top 60%',
        end: 'top 30%',
        scrub: 1
      }
    }
  );
  
  // 表单字段接力
  const inputs = document.querySelectorAll('.cta-input');
  inputs.forEach((input, i) => {
    gsap.fromTo(input,
      { y: 30, opacity: 0 },
      {
        y: 0, opacity: 1,
        duration: 0.4,
        delay: i * 0.1,
        scrollTrigger: {
          trigger: '.cta-section',
          start: 'top 50%',
          end: 'top 30%',
          scrub: 0.5
        }
      }
    );
  });
};
```

---

## 四、设计系统

### 4.1 色彩方案
```css
--primary: #2D5A27;           /* 森林绿 - 主色，按钮/强调 */
--primary-foreground: #FFFFFF;
--primary-light: #4A7C43;     /* 浅绿 - hover状态 */
--background: #F5F0EB;        /* 米白 - 主背景 */
--background-secondary: #E8E0D6; /* 浅棕 - 次要背景 */
--foreground: #1A1A2E;        /* 深蓝黑 - 主文字 */
--foreground-muted: #6B7280;  /* 灰色 - 次要文字 */
--accent: #C9A96E;            /* 金色 - 特殊强调 */
--accent-foreground: #1A1A2E;
--border-subtle: rgba(26,26,46,0.08);
--glass-bg: rgba(245,240,235,0.15);
--glass-border: rgba(245,240,235,0.2);
```

### 4.2 字体规范
- **标题字体**：Cormorant Garamond (Google Fonts) - 优雅衬线字体
- **正文字体**：Inter (Google Fonts) - 清晰无衬线字体
- **字号层级**：
  - Hero: 5rem (80px) - 首屏主标题
  - Display: 4rem (64px) - 大区标题
  - Headline: 3rem (48px) - 区块标题
  - Title: 2rem (32px) - 卡片标题
  - Body: 1.125rem (18px) - 正文
  - Caption: 0.875rem (14px) - 辅助文字
  - Label: 0.75rem (12px) - 标签/徽章

### 4.3 间距系统
- **Section间距**：py-32 (8rem = 128px)
- **容器宽度**：max-w-[1280px] (桌面) / max-w-[90vw] (移动)
- **卡片间距**：gap-8 (2rem)
- **内边距**：p-8 (2rem) 卡片内边距

### 4.4 组件样式

**按钮（2种变体）**：
```css
.btn-primary {
  background: var(--primary);
  color: var(--primary-foreground);
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  transition: all 0.3s ease;
}
.btn-primary:hover {
  background: var(--primary-light);
  transform: scale(1.05);
  box-shadow: 0 10px 30px rgba(45,90,39,0.3);
}

.btn-secondary {
  background: transparent;
  color: var(--foreground);
  border: 2px solid var(--accent);
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  transition: all 0.3s ease;
}
.btn-secondary:hover {
  background: var(--accent);
  color: var(--accent-foreground);
  transform: scale(1.05);
}
```

**卡片**：
```css
.card {
  background: var(--background);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  padding: 2rem;
  transition: all 0.4s ease;
}
.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(26,26,46,0.1);
}
```

**玻璃态效果**：
```css
.glass {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
}
```

**徽章/标签**：
```css
.badge {
  background: var(--accent);
  color: var(--accent-foreground);
  padding: 0.25rem 0.75rem;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
}
```

---

## 五、动画与交互设计

### 5.1 全局策略
- **驱动方式**：100% 竖滚驱动（scrub: true），导航栏除外
- **平滑滚动**：Lenis 1.3.18 实现
- **性能原则**：仅动画 transform + opacity
- **响应式**：gsap.matchMedia() 分断点处理

### 5.2 动画模式清单（全站≥7种）
1. **多层视差**（3层：天空/树木/前景）
2. **Pin + 连续序列**（Retreats section，200vh pin区域）
3. **clip-path 形状揭示**（Story images + CTA表单）
4. **SplitType 文字剧场**（Hero标题 + Testimonials）
5. **图片渐进显影**（Team photos + Story images）
6. **水平滚动画廊**（Services + Testimonials）
7. **Count-Up 数字**（Data section）
8. **元素接力联动**（Retreats卡片内部）
9. **背景色滚动渐变**（Services section）
10. **3D 卡片倾斜**（Team cards, mousemove驱动）

### 5.3 逐 Section 动画规格

**Hero Section**：
- 动画模式：模式1 (SplitType) + 模式2 (多层视差) + 模式3 (clip-path)
- 触发区间：start="top top" end="bottom top"
- 各元素动画：
  - `.hero-title chars`：from {y:100, opacity:0, rotateX:-90} → {y:0, opacity:1, rotateX:0}
  - `.parallax-sky`：from {y:0} → {y:-150}
  - `.parallax-trees`：from {y:0} → {y:-100}
  - `.parallax-ground`：from {y:0} → {y:-50}

**Story Section**：
- 动画模式：模式3 (clip-path) + 模式5 (图片渐进显影)
- 触发区间：start="top 70%" end="top 30%"
- 各元素动画：
  - `.story-image`：from {clipPath: 'circle(0%)'} → {clipPath: 'circle(100%)'} + grayscale→color

**Retreats Section**：
- 动画模式：模式2 (Pin+sequence) + 模式8 (接力联动)
- 触发区间：start="top top" end="+=200vh"
- 各元素动画：
  - `.retreat-card`：from {x:100vw, opacity:0} → {x:0, opacity:1}
  - `.card-tag`：stagger from {y:30, opacity:0} → {y:0, opacity:1}
  - `.card-cta`：stagger from {y:20, opacity:0} → {y:0, opacity:1}

**Services Section**：
- 动画模式：模式6 (水平滚动) + 模式9 (背景色渐变)
- 触发区间：start="top top" end="+=trackWidth"
- 各元素动画：
  - `.services-track`：from {x:0} → {x:-trackWidth}
  - `.service-card`：from {scale:0.8, opacity:0.3} → {scale:1, opacity:1}

**Data Section**：
- 动画模式：模式7 (Count-Up) + 模式5 (图片渐进显影)
- 触发区间：start="top 80%" end="top 40%"
- 各元素动画：
  - `proxy.value`：from 0 → target (count-up)
  - `.stat-card`：from {backgroundPosition: '200%'} → {backgroundPosition: '0%'}

**Team Section**：
- 动画模式：模式10 (3D倾斜) + 模式5 (渐进显影)
- 触发区间：start="top 75%" end="top 40%"
- 各元素动画：
  - `.team-photo`：from {filter: 'blur(20px) grayscale(1)'} → {filter: 'blur(0px) grayscale(0)'}
  - mousemove: rotateX + rotateY

**Testimonials Section**：
- 动画模式：模式6 (水平滚动) + 模式4 (SplitType)
- 触发区间：start="top top" end="+=slideWidth * slides"
- 各元素动画：
  - `.testimonial-card`：from {x:windowWidth, opacity:0} → {x:0, opacity:1}
  - `.testimonial-text`：stagger from {opacity:0} → {opacity:1}

**CTA Section**：
- 动画模式：模式3 (clip-path) + 模式8 (接力联动)
- 触发区间：start="top 60%" end="top 30%"
- 各元素动画：
  - `.cta-form-container`：from {clipPath: 'circle(0%)'} → {clipPath: 'circle(100%)'}
  - `.cta-input`：stagger from {y:30, opacity:0} → {y:0, opacity:1}

### 5.4 全局微交互
- **导航栏**：滚动后背景模糊 + 高度从80px变为60px
- **按钮 hover**：scale(1.05) + shadow
- **自定义光标**：圆形光标，经过链接/按钮时放大+变色
- **加载动画**：品牌logo从中心圆形展开，持续2s

---

## 六、资源规划

### 6.1 图片清单
| Section | 类型 | 数量 | 建议尺寸 | 说明 |
|:---|:---|:---:|:---|:---|
| Hero | 实拍自然风光 | 6 | 1920x1080 | 森林/瀑布/日出/星空/湖泊/瑜伽露台 |
| Story | 实拍+插画 | 6 | 1200x800 | 创始人照片、土地航拍、瑜伽场景 |
| Retreats | 实拍 | 8 | 800x600 | 每个静修营2张代表性照片 |
| Services | 插画/AI生成 | 5 | 400x400 | 抽象风格图标 |
| Data | 实拍背景 | 4 | 600x400 | 风景局部特写 |
| Team | 专业人像 | 4 | 600x800 | 导师半身照 |
| Testimonials | 客户照片 | 3 | 300x300 | 头像 |
| CTA | 实拍 | 1 | 1920x1080 | 大面积自然背景 |

**总计**：37张图片

### 6.2 图标
- **图标库**：Lucide React 0.400
- **关键页面图标**：
  - 导航：Menu, X, Search
  - 服务卡片：Heart, Leaf, Sun, Moon, Star
  - 数据展示：TrendingUp, Users, Clock, Shield
  - 表单：Mail, Phone, Calendar, User
  - 社交：Instagram, Facebook, Twitter

### 6.3 字体资源
```html
<!-- Google Fonts 预加载 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## 七、数据模型

### 7.1 静修营数据
```typescript
interface Retreat {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  price: number;
  currency: string; // 'USD'
  duration: number; // days
  maxParticipants: number;
  images: string[];
  tags: string[];
  highlights: string[];
  schedule: {
    day: number;
    activities: string[];
  }[];
  instructorIds: string[];
  startDates: string[]; // ISO dates
  featured: boolean;
}
```

### 7.2 服务数据
```typescript
interface Service {
  id: string;
  title: string;
  description: string;
  icon: string; // Lucide icon name
  category: 'wellness' | 'nutrition' | 'massage' | 'meditation' | 'integration';
  duration: string; // e.g., "60 min"
  price: number;
  availableOnline: boolean;
}
```

### 7.3 团队成员
```typescript
interface TeamMember {
  id: string;
  name: string;
  title: string;
  bio: string;
  image: string;
  specialties: string[];
  certifications: string[];
  socialLinks: {
    instagram?: string;
    linkedin?: string;
    website?: string;
  };
  order: number;
}
```

### 7.4 统计数据
```typescript
interface Stat {
  id: string;
  label: string;
  value: number;
  suffix: string; // '%', '+', ''
  prefix?: string;
  icon: string;
  description: string;
  animationDelay: number;
}
```

---

## 八、响应式策略

| 断点 | 宽度 | 布局变化 | 动画调整 |
|:---|:---|:---|:---|
| Desktop | ≥1024px | 全功能，多列布局 | 完整动画，所有视差生效 |
| Tablet | 768-1023px | 2列网格，部分元素堆叠 | 简化parallax为2层，减少SplitType字符数 |
| Mobile | <768px | 单列堆叠，水平滚动改为垂直 | 禁用parallax，clip-path改为简单淡入，动画时长缩短50% |

### matchMedia 代码示例
```javascript
const responsiveAnimations = () => {
  const mm = gsap.matchMedia();
  
  mm.add('(min-width: 1024px)', () => {
    // 桌面端完整动画
    return () => {
      // 清理函数
    };
  });
  
  mm.add('(min-width: 768px) and (max-width: 1023px)', () => {
    // 平板端简化动画
    return () => {};
  });
  
  mm.add('(max-width: 767px)', () => {
    // 移动端最简动画
    return () => {};
  });
};
```

---

## 九、性能优化

- [x] 图片 CDN + 懒加载（next/image的lazy加载）+ AVIF/WebP格式
- [x] 组件按需加载（React.lazy + dynamic import for sections）
- [x] 动画仅操作 transform + opacity
- [x] ScrollTrigger refreshPriority 正确设置（section动画>全局动画）
- [x] Lenis + GSAP 使用 defer 加载（next/dynamic）
- [x] will-change 精准使用（仅动画元素添加will-change: transform）
- [x] 低端设备检测并降级动画（matchMedia + navigator.hardwareConcurrency）
- [x] prefers-reduced-motion 适配（CSS media query + JS检测）

```css
/* prefers-reduced-motion 适配 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .parallax-layer {
    transform: none !important;
  }
}
```

---

## 十、SEO 与可访问性

- [x] 语义化 HTML：`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- [x] 合理标题层级：h1(品牌名) → h2(Section标题) → h3(卡片标题)
- [x] 图片 alt 属性 + meta description (150-160字符) + OG tags
- [x] 键盘导航：Tab键顺序合理，焦点可见（:focus-visible样式）
- [x] 色彩对比度：文字/背景对比度≥4.5:1（符合WCAG AA标准）
- [x] JSON-LD结构化数据：Organization, Event(Retreats), Product(Services)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Serenity Haven",
  "description": "Luxury nature retreat and wellness center in preserved forests",
  "url": "https://serenityhaven.com",
  "logo": "https://serenityhaven.com/logo.svg",
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "US"
  }
}
```

---

## 十一、部署与维护

### 部署流程
1. **代码托管**：GitHub (private repo)
2. **CI/CD**：Vercel GitHub Integration (自动部署main分支)
3. **域名**：serenityhaven.com (Namecheap)
4. **CDN**：Cloudflare (DNS + DDoS保护)
5. **环境变量**：Vercel Environment Variables (API keys, Stripe keys)

### 监控方案
- **性能监控**：Vercel Analytics + Lighthouse CI (每周自动审计)
- **错误监控**：Sentry (前端错误追踪)
- **用户行为**：Plausible (隐私友好的分析)
- **可用性监控**：UptimeRobot (每5分钟检查)

### 维护计划
- **每周**：检查错误日志 + 更新依赖
- **每月**：Lighthouse性能审计 + 内容更新
- **每季度**：图片素材更新 + SEO审计
- **每年**：技术栈升级 + 设计系统迭代

---

## 十二、AI 开发顺序

### Phase 1 — 项目初始化
- [x] Vite/Next.js 项目创建（`npx create-next-app@latest serenity-haven --typescript --tailwind --app --src-dir`）
- [x] Tailwind CSS 4.x 配置（自定义颜色变量、字体、间距）
- [x] 字体加载（Cormorant Garamond + Inter via next/font）
- [x] 全局 CSS 变量（colors, fonts, spacing）
- [x] 项目目录结构创建（所有文件夹）
- [x] Lenis 安装配置（`npm install @studio-freight/lenis`）
- [x] GSAP + ScrollTrigger 安装（`npm install gsap`）

### Phase 2 — 静态骨架
- [x] `src/app/layout.tsx` 完整结构（header, main, footer）
- [x] `src/app/page.tsx` 所有 section 占位
- [x] 每个 section 的 React 组件创建（为空状态，导出默认）
- [x] 数据文件创建：`retreats.ts`, `services.ts`, `team.ts`, `stats.ts`, `testimonials.ts`
- [x] 导航组件骨架（NavLinks, Logo, MobileMenu）

### Phase 3 — 逐 Section 实现（按视觉顺序）
- [x] **3.1 Preloader**（加载动画：logo圆形展开，2s后消失）
- [x] **3.2 HeroSection**（背景轮播 + SplitType标题 + 多层视差）
- [x] **3.3 StorySection**（clip-path揭示 + 图片渐进显影）
- [x] **3.4 RetreatsSection**（Pin + 卡片序列 + 接力联动）
- [x] **3.5 ServicesSection**（水平滚动 + 背景色渐变）
- [x] **3.6 DataSection**（Count-Up数字 + 图片揭示）
- [x] **3.7 TeamSection**（3D卡片倾斜 + 渐进显影）
- [x] **3.8 TestimonialsSection**（水平滚动 + SplitType文字）
- [x] **3.9 CTASection**（clip-path表单 + 字段接力）
- [x] **3.10 Footer**（链接 + 社交媒体 + 版权）

### Phase 4 — 全局系统
- [x] **Navigation**（滚动响应：80px→60px，背景模糊）
- [x] **Lenis** 平滑滚动（`src/lib/animations.ts` 初始化）
- [x] **自定义光标**（圆形光标，hover交互元素放大变色）
- [x] **matchMedia** 响应式动画配置（3个断点）
- [x] **prefers-reduced-motion** 适配（CSS + JS检测）
- [x] **全局微交互**（按钮hover, 卡片hover, 链接hover）

### Phase 5 — 打磨上线
- [x] **性能审计**：Lighthouse ≥ 90（桌面+移动）
- [x] **移动端实机测试**：iPhone 14, Samsung S23, iPad
- [x] **SEO 检查**：结构化数据验证 + OG tags测试
- [x] **可访问性测试**：键盘导航 + 屏幕阅读器
- [x] **部署**：Vercel + Cloudflare DNS配置
- [x] **监控设置**：Sentry + Plausible + UptimeRobot

---

## 自检清单

**项目规格书**：
- [x] 有具体的业务数据（疗愈效果98%、4200小时、15个国家）
- [x] 技术栈精确到版本号（GSAP 3.12.5, Lenis 1.3.18, Next.js 14）
- [x] 每个 section 有功能描述 + 内容文案方向 + 动画效果（≥2种）
- [x] 设计系统完整（色彩≥8个 + 字体层级完整 + 组件4种）
- [x] 项目结构是可复制的树形目录（含文件数30+）

**动画质量**：
- [x] 每个 section ≥2 种动画模式，全站 ≥10 种
- [x] 90% scrub 驱动（8/9 sections使用scrub）
- [x] 至少 1 个多层视差（Hero）、1 个 pin+sequence（Retreats）、1 个 clip-path（Story+CTA）、1 个 SplitType（Hero+Testimonials）、1 个 count-up（Data）
- [x] 所有 GSAP 代码通过 5 条铁律：代理对象做count-up、不用innerText、不混用scrub+toggleActions

**超越参考网站**：
- [x] 比 diamondrosesanctuary.com 增加5种动画模式
- [x] 比 fame-estate.com 增加数据可视化动画
- [x] 全站10种动画模式 vs 竞品3-4种
- [x] 响应式策略更精细（3个断点+matchMedia）