// Source capture for the ทันเงิน demo edit: 1470×800 viewport at 2× DPR (2940×1600 frames),
// no cursor or captions. Logs named marks and click positions (source pixels) to capture.json.
import { chromium } from 'playwright-core'
import fs from 'node:fs'

const URL = 'http://127.0.0.1:5173/'
const OUT = 'src_frames'
fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT)
const b64 = (f) => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64')

// Rebrand the app UI: ทางเชื่อม -> ทันเงิน and the header mark -> the ทันเงิน banknote icon.
const rebrand = ({ icon }) => {
  const run = () => {
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT)
    let n; while ((n = w.nextNode())) if (n.nodeValue.includes('ทางเชื่อม')) n.nodeValue = n.nodeValue.replaceAll('ทางเชื่อม', 'ทันเงิน')
    document.querySelectorAll('.brand-mark, .lp-mark').forEach((m) => {
      if (!m.querySelector('img.tn')) m.innerHTML = `<img class="tn" src="${icon}" alt="" style="width:100%;height:100%;object-fit:contain;padding:3px;box-sizing:border-box">`
      m.style.background = '#fff'
    })
  }
  const start = () => {
    const s = document.createElement('style'); s.textContent = '*{cursor:none!important}'; document.head.appendChild(s)
    run(); new MutationObserver(run).observe(document.body, { childList: true, subtree: true, characterData: true })
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start()
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--font-render-hinting=none'] })
const ctx = await browser.newContext({ viewport: { width: 1470, height: 800 }, deviceScaleFactor: 2 })
await ctx.addInitScript(rebrand, { icon: b64('logo_icon.png') })
const page = await ctx.newPage()
const wait = (ms) => page.waitForTimeout(ms)
await page.goto(URL + '#home'); await wait(2500)

const cdp = await ctx.newCDPSession(page)
const frames = []
let t0 = null, firstWall = 0
const wall0 = Date.now() / 1000
const now = () => Date.now() / 1000 - wall0
// Full-resolution (2× DPR) frames via a screenshot loop running alongside the scripted actions;
// each frame is stamped at the midpoint of its capture call.
let capturing = true
firstWall = now()
const loop = (async () => {
  while (capturing) {
    const t1 = now()
    // clip is in document coordinates, so follow the window scroll
    const { result } = await cdp.send('Runtime.evaluate', { expression: '[scrollX, scrollY]', returnByValue: true })
    const [sx, sy] = result.value
    const r = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 92, clip: { x: sx, y: sy, width: 1470, height: 800, scale: 2 } })
    const name = `${OUT}/f${String(frames.length).padStart(6, '0')}.jpg`
    fs.writeFileSync(name, Buffer.from(r.data, 'base64'))
    frames.push({ name, t: (t1 + now()) / 2 - firstWall })
  }
})()
await wait(300)

const marks = [], clicks = []
const mark = (name) => { marks.push({ name, t: now() }); console.log('mark', name) }
const click = async (sel) => {
  await page.locator(sel).first().scrollIntoViewIfNeeded(); await wait(250)
  const r = await page.locator(sel).first().boundingBox()
  const x = r.x + r.width / 2, y = r.y + r.height / 2
  await page.mouse.move(x, y); await wait(120)
  clicks.push({ t: now(), x: x * 2, y: y * 2, sel })
  await page.mouse.click(x, y)
}
const smooth = (y, ms) => page.evaluate(([y, ms]) => new Promise((res) => {
  const from = scrollY, t0 = performance.now(), e = (t) => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
  const st = (n) => { const t = Math.min(1, (n - t0) / ms); scrollTo(0, from + (y - from) * e(t)); t < 1 ? requestAnimationFrame(st) : res() }
  requestAnimationFrame(st)
}), [y, ms])

// 1. Landing hero
mark('hero'); await wait(3500)
// 2. Demo cases: the ฿300 merchant card
const casesY = await page.evaluate(() => document.getElementById('lp-cases').offsetTop - 30)
await smooth(casesY, 700); await wait(300)
mark('cases'); await wait(3200)
// 3. Institutions: start merchant_300 at 120× and let Bank A's feed fill
await page.evaluate(() => { location.hash = 'institutions'; scrollTo(0, 0) }); await wait(900)
await click('button:has-text("Restart run")'); await wait(1300)
await page.selectOption('select.player-speed', '120')
mark('inst_play'); await click('button.player-main'); await wait(9000)
// 4. Our Engine: case opens (report at 10:25), graph across lanes, 0.85 score
await page.keyboard.press('2'); mark('engine'); await wait(8500)
await click('button.player-main') // pause before the officer acts
mark('engine_paused'); await wait(800)
// 5. Institutions: officer restricts only ฿300
await page.keyboard.press('1'); await wait(500)
mark('restrict'); await wait(1300)
await click('button:has-text("Restrict ฿300 only")'); await wait(2800)
// 6. Merchant: ฿300 held, ฿10,000 usable
await page.keyboard.press('3'); mark('merchant_held'); await wait(3200)
// 7. Merchant sends evidence (default receipt is pre-selected; dropdown is not opened)
await click('button:has-text("ส่งหลักฐาน")'); mark('evidence_sent'); await wait(3400)
// 8. Bank B officer console: release the hold
await page.keyboard.press('1'); await wait(400)
mark('console'); await wait(1300)
await click('button:has-text("Release this hold")'); await wait(1800)
// 9. Merchant: released
await page.keyboard.press('3'); mark('released'); await wait(3500)
// 10. Overview
await page.evaluate(() => { location.hash = 'overview' }); mark('overview'); await wait(5000)
// 11. Landing hero for the end card background
await page.evaluate(() => { location.hash = 'home'; scrollTo(0, 0) }); await wait(800)
mark('hero_end'); await wait(1500)
await page.screenshot({ path: 'hero_end.png' })

capturing = false; await loop
const end = now()
const rel = (t) => t - firstWall
fs.writeFileSync('capture.json', JSON.stringify({
  frames, end: rel(end),
  marks: marks.map((m) => ({ ...m, t: rel(m.t) })),
  clicks: clicks.map((c) => ({ ...c, t: rel(c.t) })),
}, null, 1))
console.log('frames', frames.length, 'dur', rel(end).toFixed(1))
await browser.close()
