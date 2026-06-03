/**
 * CSS @keyframes 提取器 — 使用 csstree 解析 CSS
 *
 * 用法: node css-parser.mjs < css_text
 * 输出: JSON 数组，每个元素是一个 @keyframes 定义
 *
 * 如果 csstree 未安装: npm install css-tree
 */
import { parse, walk } from 'css-tree';
import { createInterface } from 'readline';

// 从 stdin 读取 CSS 文本
let cssText = '';
const rl = createInterface({ input: process.stdin });
rl.on('line', (line) => { cssText += line + '\n'; });

rl.on('close', () => {
    try {
        const ast = parse(cssText, {
            tolerant: true,
            parseAtrulePrelude: true,
            parseRulePrelude: true,
            parseValue: true,
        });

        const keyframes = [];

        walk(ast, {
            visit: 'Atrule',
            enter(node) {
                try {
                    const atName = (node.name || '').toLowerCase();
                    if (atName === 'keyframes' || atName === '-webkit-keyframes') {
                        const name = node.prelude ?
                            (typeof node.prelude === 'string' ? node.prelude :
                             (node.prelude.value || node.prelude.name || '')) : '';

                        const steps = [];
                        if (node.block && node.block.children) {
                            node.block.children.forEach(rule => {
                                if (rule.type === 'Percentage' || rule.type === 'Selector') {
                                    const selector = rule.prelude ?
                                        (typeof rule.prelude === 'string' ? rule.prelude :
                                         (rule.prelude.value || rule.prelude.name || '')) : '';

                                    const properties = {};
                                    if (rule.block && rule.block.children) {
                                        rule.block.children.forEach(decl => {
                                            if (decl.type === 'Declaration' && decl.property) {
                                                properties[decl.property] = decl.value ?
                                                    (typeof decl.value === 'string' ? decl.value :
                                                     decl.value.value || '') : '';
                                            }
                                        });
                                    }

                                    steps.push({ selector, properties });
                                }
                            });
                        }

                        if (name) {
                            keyframes.push({ name, steps });
                        }
                    }
                } catch (e) {
                    // 跳过解析失败的元素
                }
            }
        });

        console.log(JSON.stringify(keyframes, null, 2));
    } catch (e) {
        console.error('CSS parse error:', e.message);
        console.log(JSON.stringify([]));
    }
});
