/**
 * Lighthouse 审计运行器
 *
 * 用法: node lighthouse.mjs <url>
 * 输出: JSON (Lighthouse 完整报告)
 *
 * 前置安装:
 *   npm install lighthouse chrome-launcher
 */
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

const url = process.argv[2];

if (!url) {
    console.error('Usage: node lighthouse.mjs <url>');
    process.exit(1);
}

async function run() {
    const chrome = await chromeLauncher.launch({
        chromeFlags: ['--headless', '--no-sandbox', '--disable-gpu'],
    });

    try {
        const result = await lighthouse(url, {
            port: chrome.port,
            output: 'json',
            onlyCategories: ['performance', 'seo', 'accessibility', 'best-practices'],
            settings: {
                formFactor: 'desktop',
                screenEmulation: {
                    mobile: false,
                    width: 1440,
                    height: 900,
                    deviceScaleFactor: 1,
                    disabled: false,
                },
                throttling: {
                    // 桌面端不节流，更快
                    rttMs: 0,
                    throughputKbps: 0,
                    cpuSlowdownMultiplier: 1,
                },
            },
        });

        // 输出完整 LHR (Lighthouse Result) JSON
        console.log(JSON.stringify(result.lhr));
    } catch (e) {
        console.error('Lighthouse error:', e.message);
        process.exit(1);
    } finally {
        await chrome.kill();
    }
}

run();
