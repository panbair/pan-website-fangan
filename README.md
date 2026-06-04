# WebInsight (Commercial Hardened)

WebInsight is a website analysis toolkit powered by FastAPI + Playwright/Requests + DeepSeek.

## Current capabilities

- Single-site analysis and report generation (`/api/analyze`)
- Debug evidence API (`/api/analyze/debug`)
- Animation recognition with:
  - Runtime telemetry (`runtime_animation`)
  - CSS keyframes extraction (`css_keyframes_count`)
  - FPS/Web Vitals/animation audit (`animation_fps`, `web_vitals`, `animation_audit`)
  - Per-library confidence and evidence paths (`animation_evidence`, `animation_evidence_rows`)
  - GSAP implementation profile (`gsap_profile`) with tween mix and ScrollTrigger config distribution
  - GSAP page-layer portrait (`gsap_layer_portrait`) with layer animation density and dominant layer inference
- Visual scorecard (`UI/UX`, `交互质量`, `转化可见性`)
- Change alert summary and history APIs
- Audit log API + runtime metrics API
- Redis-first rate limiting (memory fallback)

## Quick run

```powershell
cd "D:\work20240226\rcs-20250311\website-fangan-20260604\pan-website-fangan"
python -m pip install -r requirements.txt
python app.py
```

## Smoke tests

```powershell
python -m py_compile app.py smoke_cli.py smoke_rate_limit.py cli_analyze.py
python smoke_cli.py
python smoke_rate_limit.py
```

## Key environment variables

```powershell
$env:DEEPSEEK_API_KEY="sk-xxx"
$env:CORS_ALLOW_ORIGINS="http://localhost:8765"
$env:RATE_LIMIT_BACKEND="auto"   # auto | redis | memory
$env:REDIS_URL="redis://localhost:6379/0"
$env:WEBINSIGHT_ADMIN_READ_TOKEN="read-token"
$env:WEBINSIGHT_ADMIN_DELETE_TOKEN="delete-token"
```



