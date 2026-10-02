// Scripted tour of the ทางเชื่อม demo. Captures frames via CDP screencast and logs SFX cue times.
import { chromium } from 'playwright-core'
import fs from 'node:fs'

const URL = 'http://127.0.0.1:5173/'
const W = 1920, H = 1080
const OUT = 'frames'
fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT)

const overlay = () => {
  const css = `
  #tc-cursor{position:fixed;left:0;top:0;width:26px;height:26px;z-index:2147483647;pointer-events:none;transform:translate(-3px,-2px);transition:opacity .3s}
  #tc-ripple{position:fixed;width:16px;height:16px;border-radius:50%;border:3px solid #5fd4c4;z-index:2147483646;pointer-events:none;opacity:0;transform:translate(-50%,-50%) scale(.4)}
  #tc-ripple.go{animation:tcr .55s ease-out}
  @keyframes tcr{0%{opacity:1;transform:translate(-50%,-50%) scale(.4)}100%{opacity:0;transform:translate(-50%,-50%) scale(4)}}
  #tc-cap{position:fixed;left:50%;bottom:44px;transform:translate(-50%,20px);z-index:2147483645;pointer-events:none;opacity:0;
    transition:opacity .45s ease,transform .45s ease;background:rgba(9,30,40,.88);backdrop-filter:blur(8px);color:#fff;
    padding:16px 30px 14px;border-radius:16px;box-shadow:0 12px 40px rgba(0,0,0,.35);text-align:center;max-width:1400px;
    white-space:nowrap;border:1px solid rgba(95,212,196,.35);font-family:system-ui,'Noto Sans Thai',sans-serif}
  #tc-cap.on{opacity:1;transform:translate(-50%,0)}
  #tc-cap b{display:block;font-size:30px;font-weight:700;letter-spacing:.2px}
  #tc-cap small{display:block;margin-top:4px;font-size:19px;color:#9fe3d8;font-weight:500}
  #tc-card{position:fixed;inset:0;z-index:2147483644;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:radial-gradient(1200px 700px at 30% 20%,#14535a 0%,#0b2a36 45%,#06161f 100%);color:#fff;opacity:0;pointer-events:none;
    transition:opacity .8s ease;font-family:system-ui,'Noto Sans Thai',sans-serif;overflow:hidden}
  #tc-card.on{opacity:1}
  #tc-card .grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:60px 60px}
  #tc-card .in{position:relative;text-align:center;transform:translateY(16px) scale(.98);opacity:0;transition:all 1.1s cubic-bezier(.2,.8,.2,1) .2s}
  #tc-card.on .in{transform:none;opacity:1}
  #tc-card .logo{width:120px;height:120px;margin:0 auto 28px;border-radius:28px;background:#0e3a46;border:1px solid rgba(95,212,196,.4);display:flex;align-items:center;justify-content:center;box-shadow:0 0 60px rgba(95,212,196,.25)}
  #tc-card h1{font-size:96px;margin:0;font-weight:800;letter-spacing:1px}
  #tc-card h2{font-size:34px;margin:10px 0 0;color:#5fd4c4;font-weight:600;letter-spacing:4px;text-transform:uppercase}
  #tc-card p{font-size:28px;margin:34px 0 0;color:#cfe7e3}
  #tc-card .tags{margin-top:40px;display:flex;gap:14px;justify-content:center}
  #tc-card .tags span{padding:8px 18px;border-radius:999px;border:1px solid rgba(95,212,196,.45);color:#bff0e8;font-size:20px}
  `
  const add = () => {
    if (document.getElementById('tc-cursor')) return
    const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s)
    const c = document.createElement('div'); c.id = 'tc-cursor'
    c.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24"><path d="M3 2l7.5 19 2.6-7.7L21 10.8z" fill="#fff" stroke="#0b2a36" stroke-width="1.6" stroke-linejoin="round"/></svg>'
    const r = document.createElement('div'); r.id = 'tc-ripple'
    const cap = document.createElement('div'); cap.id = 'tc-cap'
    const card = document.createElement('div'); card.id = 'tc-card'
    document.body.append(c, r, cap, card)
    window.addEventListener('mousemove', (e) => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px' }, true)
    window.addEventListener('mousedown', (e) => {
      r.style.left = e.clientX + 'px'; r.style.top = e.clientY + 'px'; r.classList.remove('go'); void r.offsetWidth; r.classList.add('go')
    }, true)
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', add); else add()
  window.__cap = (b, s) => {
    const el = document.getElementById('tc-cap')
    if (!b) { el.classList.remove('on'); return }
    el.classList.remove('on')
    setTimeout(() => { el.innerHTML = `<b>${b}</b>${s ? `<small>${s}</small>` : ''}`; el.classList.add('on') }, el.innerHTML ? 350 : 0)
  }
  window.__card = (html) => {
    const el = document.getElementById('tc-card')
    if (!html) { el.classList.remove('on'); return }
    el.innerHTML = `<div class="grid"></div><div class="in">${html}</div>`; void el.offsetWidth; el.classList.add('on')
  }
  window.__scroll = (to, ms) => new Promise((res) => {
    const from = window.scrollY, t0 = performance.now()
    const ease = (t) => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
    const step = (now) => { const t = Math.min(1, (now - t0) / ms); window.scrollTo(0, from + (to - from) * ease(t)); t < 1 ? requestAnimationFrame(step) : res() }
    requestAnimationFrame(step)
  })
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--font-render-hinting=none'] })
const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 })
await ctx.addInitScript(overlay)
const page = await ctx.newPage()
const wait = (ms) => page.waitForTimeout(ms)

// Reset backend state with a fresh run before filming.
await page.goto(URL + '#home'); await wait(2500)

// --- screencast ---
const cdp = await ctx.newCDPSession(page)
const frames = []
let t0 = null, firstWall = 0
cdp.on('Page.screencastFrame', async (f) => {
  const ts = f.metadata.timestamp
  if (t0 === null) { t0 = ts; firstWall = now() }
  const name = `${OUT}/f${String(frames.length).padStart(6, '0')}.jpg`
  fs.writeFileSync(name, Buffer.from(f.data, 'base64'))
  frames.push({ name, t: ts - t0 })
  cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {})
})
const wall0 = Date.now() / 1000
const now = () => Date.now() / 1000 - wall0
const cues = []
const cue = (type) => cues.push({ type, t: now() })
await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: W, maxHeight: H, everyNthFrame: 1 })

let mx = W / 2, my = H / 2
const move = async (x, y, ms = 700) => {
  const steps = Math.max(8, Math.round(ms / 16))
  const sx = mx, sy = my
  for (let i = 1; i <= steps; i++) {
    const t = i / steps, e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2
    await page.mouse.move(sx + (x - sx) * e, sy + (y - sy) * e)
    await page.waitForTimeout(ms / steps)
  }
  mx = x; my = y
}
const clickEl = async (sel, ms = 800) => {
  const b = await page.locator(sel).first().boundingBox()
  await move(b.x + b.width / 2, b.y + b.height / 2, ms)
  await wait(150); cue('click'); await page.mouse.down(); await page.mouse.up()
}
const cap = (b, s) => page.evaluate(([b, s]) => window.__cap(b, s), [b, s])
const card = (h) => page.evaluate((h) => window.__card(h), h)
const scroll = (y, ms) => page.evaluate(([y, ms]) => window.__scroll(y, ms), [y, ms])

const LOGO = '<svg width="70" height="70" viewBox="0 0 32 32" fill="none" stroke="#5fd4c4" stroke-width="2" stroke-linecap="round"><path d="M3 22h26M6 22V12M26 22V12M6 12q10 8 20 0M11 22v-6M16 22v-5M21 22v-6"/></svg>'

// ---- Scene 0: title card ----
await page.mouse.move(mx, my)
await card(`<div class="logo">${LOGO}</div><h1>ทางเชื่อม</h1><h2>Bank × Crypto Risk Graph</h2>
  <p>เชื่อมหลักฐาน ธนาคาร · Exchange · Blockchain ให้อยู่ในมุมมองเดียว</p>
  <div class="tags"><span>NITMX Fintech Bootcamp 2026</span><span>Prototype Demo</span></div>`)
cue('intro')
await wait(4800)
cue('whoosh'); await card(null); await wait(900)

// ---- Scene 1: landing page ----
await cap('เชื่อมหลักฐานจากทุกฝั่ง เพื่อช่วยการตัดสินใจ', 'Connect the evidence. Support the decision.')
await move(1290, 390, 1400)
await wait(2600)
await move(1120, 265, 700); await wait(400); await move(1290, 265, 500); await wait(400); await move(1458, 265, 500); await wait(900)
await cap('หนึ่งเคส สามมุมมองของเงิน', 'Trace · Understand the context · Act in proportion')
cue('whoosh'); await scroll(760, 1800); await wait(2600)
await cap('เคสจำลอง 4 แบบ — หลักฐานรองรับการตัดสินใจได้แค่ไหน?', 'Four synthetic demo cases')
cue('whoosh'); await page.evaluate(() => window.__scroll(document.getElementById('lp-cases').offsetTop - 40, 1800)); await wait(3200)
await cue('whoosh'); await scroll(0, 1400); await wait(400)
await cap(null)

// ---- Scene 2: open demo, run the merchant_300 case ----
await clickEl('button:has-text("Open demo")')
await wait(1200)
await page.evaluate(() => { location.hash = 'overview' }); await wait(1200)
await cap('เปิดเดโม: ภาพรวมสถาบัน · Engine · ร้านค้า', 'Overview — institutions, our engine and the merchant side by side')
await clickEl('button:has-text("Restart run")', 900); await wait(1500)
await page.selectOption('select.player-speed', '60').catch(() => {})
await clickEl('button.player-main', 800); cue('play')
await wait(800)
await cap('เคส merchant_300: ร้านค้ารับเงิน 300 บาท จากบัญชีที่ถูกแจ้ง', 'A merchant receives ฿300 from a reported account; the rest moves to an exchange')
await move(520, 380, 1200); await wait(3500)
await move(1085, 300, 1200); await wait(3500)
await move(1630, 520, 1200); await wait(2500)

// ---- Scene 3: Our Engine ----
cue('whoosh'); await page.keyboard.press('2'); await wait(600)
await cap('Engine ติดตามเส้นทางเงินข้ามธนาคาร → Exchange → Chain', 'Money-flow evidence graph: only verified deposit links are crossed')
await move(900, 420, 1200); await wait(4200)
cue('ping'); await cap('ทุกคะแนนอธิบายได้: หลักฐาน · บริบทปกติ · ข้อมูลที่ขาดหาย', 'Evidence found · Benign context · Missing data & uncertainty')
await move(1500, 700, 1200); await wait(4500)

// ---- Scene 4: Institutions ----
cue('whoosh'); await page.keyboard.press('1'); await wait(700)
await cap('Engine ส่งคำแนะนำ — เจ้าหน้าที่ของแต่ละสถาบันเป็นผู้ตัดสินใจ', 'Recommendations go to the responsible institution; an officer decides')
await move(1590, 330, 1100); await wait(900)
await clickEl('button:has-text("Hold withdrawal")', 700); cue('ping'); await wait(1600)
await clickEl('button:has-text("Restrict ฿300 only")', 900); cue('ping'); await wait(1200)
await cap('พักเฉพาะยอด 300 บาทที่เชื่อมกับเคส — ไม่อายัดทั้งบัญชี', 'Act in proportion: hold the linked ฿300, not the whole account')
await move(1080, 360, 900); await wait(3200)

// ---- Scene 5: Merchant ----
cue('whoosh'); await page.keyboard.press('3'); await wait(700)
await cap('ร้านค้ายังใช้เงินที่เหลือได้ และส่งหลักฐานการขายได้ทันที', 'The merchant keeps ฿10,000 usable and can submit sales evidence')
await move(860, 420, 1200); await wait(2600)
await move(1630, 600, 1100); await wait(1800)
await clickEl('button:has-text("ส่งหลักฐาน")', 1100); cue('ping'); await wait(3200)

// ---- Scene 6: Experiment results ----
cue('whoosh'); await page.keyboard.press('4'); await wait(600)
await cap('พร้อมต่อยอดด้วยโมเดลจากการทดลอง', 'Experiment results — plug in the trained model when ready')
await move(900, 450, 1400); await wait(4000)

// ---- Scene 7: Overview wrap-up ----
cue('whoosh'); await page.evaluate(() => { location.hash = 'overview' }); await wait(600)
await cap('ทางเชื่อม — มองเห็นภาพทั้งหมด ก่อนตัดสินใจ', 'See the whole picture before acting')
await wait(4000)
await cap(null)

// ---- Outro card ----
cue('outro'); await card(`<div class="logo">${LOGO}</div><h1>ทางเชื่อม</h1><h2>Link · Trace · Explain</h2>
  <p>ข้อมูลทั้งหมดเป็นข้อมูลจำลอง · Synthetic data only</p>
  <div class="tags"><span>Human review at every decision</span><span>Recommendations never move funds</span></div>`)
await wait(5500)
const end = now()
await cdp.send('Page.stopScreencast')
await wait(300)
fs.writeFileSync('timeline.json', JSON.stringify({ frames, cues: cues.map(c => ({ ...c, t: c.t - firstWall })), end: end - firstWall }, null, 1))
console.log('frames', frames.length, 'duration', end.toFixed(1), 'last frame t', frames.at(-1)?.t.toFixed(1))
await browser.close()
