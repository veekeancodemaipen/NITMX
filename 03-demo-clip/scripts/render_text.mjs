// Renders caption overlays and the end card layers (1920×1080 PNG) with IBM Plex Sans Thai in Chromium.
import { chromium } from 'playwright-core'
import fs from 'node:fs'

const segs = JSON.parse(fs.readFileSync('edit_segments.json', 'utf8'))
const font = (w) => `url(data:font/woff2;base64,${fs.readFileSync(`fonts/package/files/ibm-plex-sans-thai-thai-${w}-normal.woff2`).toString('base64')}) format('woff2')`
const latin = (w) => `url(data:font/woff2;base64,${fs.readFileSync(`fonts/package/files/ibm-plex-sans-thai-latin-${w}-normal.woff2`).toString('base64')}) format('woff2')`
const faces = [400, 600, 700].map((w) => `
  @font-face{font-family:Plex;font-weight:${w};src:${latin(w)};unicode-range:U+0000-00FF,U+2000-206F,U+20AC}
  @font-face{font-family:Plex;font-weight:${w};src:${font(w)};unicode-range:U+0E01-0E5B,U+200C-200D,U+25CC}`).join('')
const b64 = (f, t = 'png') => `data:image/${t};base64,${fs.readFileSync(f).toString('base64')}`

const base = `<style>${faces}
  html,body{margin:0;width:1920px;height:1080px;background:transparent;font-family:Plex,sans-serif;overflow:hidden}
  .cap{position:absolute;left:96px;bottom:76px;max-width:1500px;background:rgba(10,34,50,.80);border-left:8px solid #4A9FF5;
    border-radius:6px 14px 14px 6px;padding:20px 34px 20px 30px;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,.25)}
  .cap .en{font-weight:700;font-size:38px;line-height:1.25;letter-spacing:.1px}
  .cap .th{font-weight:400;font-size:29px;line-height:1.45;margin-top:4px;color:#E4EEF7}
</style>`

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } })
fs.mkdirSync('overlays', { recursive: true })
for (const [i, s] of segs.entries()) {
  if (!s.en) continue
  await page.setContent(`${base}<div class="cap"><div class="en">${s.en}</div><div class="th">${s.th}</div></div>`)
  await page.evaluate(() => document.fonts.ready)
  await page.screenshot({ path: `overlays/cap_${i}.png`, omitBackground: true })
}

// End card: background (blurred hero + navy 70%) and foreground (logo + tagline) as separate layers.
await page.setContent(`${base}<div style="position:absolute;inset:0;background:url(${b64('hero_bg.png')}) center/cover;filter:blur(28px);transform:scale(1.15)"></div>
  <div style="position:absolute;inset:0;background:rgba(10,34,50,.70)"></div>`)
await page.waitForTimeout(300)
await page.screenshot({ path: 'overlays/end_bg.png' })
await page.setContent(`${base}<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;text-align:center">
  <div style="background:#fff;border-radius:26px;padding:30px 48px;box-shadow:0 24px 70px rgba(0,0,0,.35)"><img src="${b64('logo_full.png')}" style="height:170px;display:block"></div>
  <div style="font-weight:700;font-size:50px;margin-top:58px;letter-spacing:.2px">Stop the mule money — not the innocent merchant.</div>
  <div style="font-weight:600;font-size:38px;margin-top:12px;color:#CFE3F6">หยุดเงินม้า ไม่ใช่หยุดร้านค้าบริสุทธิ์</div>
  <div style="position:absolute;bottom:54px;font-size:22px;color:#9DB6CC;letter-spacing:.4px">Prototype · Synthetic data · NITMX Fintech Bootcamp 2026</div>
</div>`)
await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(200)
await page.screenshot({ path: 'overlays/end_fg.png', omitBackground: true })
await browser.close()
console.log('overlays rendered')
