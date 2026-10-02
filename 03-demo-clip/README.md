# คลิปเดโมเว็บ ทางเชื่อม (Bank × Crypto Risk Graph)

![poster](poster.jpg)

**ไฟล์:** [`tangchuem-demo.mp4`](tangchuem-demo.mp4) · 1920×1080 · 30fps · H.264 + AAC · ยาว 2:08 · ~12 MB

คลิปพาชมเว็บต้นแบบจาก [FreezingH2O/itmx-prototype-demo](https://github.com/FreezingH2O/itmx-prototype-demo) (commit `47ef53f`) ที่รันในเครื่อง
มีคำบรรยายสองภาษา (ไทยเป็นหลัก อังกฤษเป็นบรรทัดรอง) เคอร์เซอร์จำลอง และดนตรีประกอบพร้อมเสียงเอฟเฟกต์

## ลำดับฉาก

| เวลา | ฉาก | ประเด็น |
|---|---|---|
| 0:00 | Title card | ทางเชื่อม · Bank × Crypto Risk Graph |
| 0:05 | Landing page | เชื่อมหลักฐาน → หนึ่งเคส สามมุมมองของเงิน → เคสจำลอง 4 แบบ |
| 0:28 | Overview | เปิดเดโม รีสตาร์ตเคส `merchant_300` แล้วกด Play (ความเร็ว 60×) |
| 1:00 | Our Engine | กราฟเส้นทางเงิน Bank → Exchange → Chain, คะแนนพร้อมเหตุผล, บริบทปกติ, ข้อมูลที่ขาด |
| 1:15 | Institutions | เจ้าหน้าที่กด Hold withdrawal ที่ Exchange และ Restrict ฿300 only ที่ Bank B |
| 1:32 | Merchant | ร้านค้าถูกพักแค่ ฿300 ยังใช้ ฿10,000 ได้ และกดส่งหลักฐานการขาย |
| 1:50 | Experiment Results | พร้อมต่อโมเดลจากการทดลอง (ยังไม่มีผล) |
| 1:58 | Overview → Outro | Link · Trace · Explain · ข้อมูลจำลองทั้งหมด |

## เพลงและเสียง

ดนตรีและเสียงเอฟเฟกต์ทั้งหมดสังเคราะห์ขึ้นใหม่ด้วยโค้ด (`scripts/music.py`) ไม่ได้ใช้เพลงหรือแซมเปิลของใคร จึงไม่มีปัญหาลิขสิทธิ์

- เพลง: 104 BPM คอร์ด Am–F–C–G มี pad, arpeggio, เบส และกลอง ช่วง intro มีแค่ pad กลองเข้าตอนกด Play แล้วลดลงช่วง outro
- เสียงเอฟเฟกต์: whoosh ตอนเปลี่ยนฉาก, click ตอนคลิก, ping ตอนเจ้าหน้าที่ตัดสินใจ, chime ตอน title/play และ riser + impact ตอน outro
- เสียงเอฟเฟกต์ตรงกับภาพ เพราะสคริปต์บันทึกจะเก็บเวลาของแต่ละ cue ไว้ใน `timeline.json`

## สร้างคลิปใหม่

ต้องมี Python 3.11, Node 22, ffmpeg และ Chromium

```bash
# 1) รันเว็บต้นแบบ (ใน itmx-prototype-demo)
pip install -r requirements.txt && uvicorn src.api.app:app --port 8000 &
cd demo/web && npm ci && npx vite --port 5173 --host 127.0.0.1 &

# 2) อัดภาพ (CDP screencast → frames/ + timeline.json)
npm i playwright-core
node scripts/record.mjs          # แก้ executablePath ให้ตรงกับ Chromium ในเครื่อง

# 3) ต่อเฟรมเป็นวิดีโอ (สร้าง concat.txt จาก timeline.json ก่อน: แต่ละเฟรมใช้ duration = เวลาเฟรมถัดไป - เวลาเฟรมนี้)
ffmpeg -f concat -safe 0 -i concat.txt -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 silent.mp4

# 4) สร้างเพลงจาก timeline.json แล้วรวมกับภาพ
pip install numpy scipy && python3 scripts/music.py
ffmpeg -i silent.mp4 -i soundtrack.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart tangchuem-demo.mp4
```

> ข้อมูลในคลิปทั้งหมดเป็นข้อมูลจำลองจากเว็บต้นแบบ (synthetic) ไม่มีข้อมูลธนาคารหรือบล็อกเชนจริง
