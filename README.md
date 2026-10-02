# NITMX Fintech — งานรีเสิร์ช

คลังส่งต่องานรีเสิร์ชสำหรับ NITMX Fintech Bootcamp 2026 (หัวข้อบัญชีม้า / บัญชีม้าคริปโต / infra เชื่อมข้อมูลออนเชน)
อัปเดตล่าสุด 29 ก.ย. 2569 · repo เป็น Private · เอกสารทั้งหมดเป็นภาษาไทย

> **สถานะโดยรวม:** ทุกหัวข้ออยู่ขั้น "ศึกษา/พิสูจน์แนวคิดบนกระดาษ" ยังไม่ได้เลือกผู้ชนะ ไม่ได้สร้างระบบ/เดโม/MVP และยังไม่ได้ทดลองกับข้อมูลจริงหรือติดต่อผู้ซื้อ
> ข้อความที่เป็นสมมติฐานในไฟล์ต่าง ๆ อย่าอ่านเป็นข้อเท็จจริงที่ยืนยันแล้ว

## เริ่มอ่านตรงไหนดี

| ฉันเป็น... | เริ่มที่ |
|---|---|
| คนใหม่ ยังไม่รู้บริบทงาน | [`01-brief/NITMX-Fintech-Bootcamp-2026-context.md`](01-brief/NITMX-Fintech-Bootcamp-2026-context.md) สรุปโจทย์ กติกา และบริบททั้งหมดของบูตแคมป์ |
| อยากรู้ว่าตอนนี้ทีมตัดสินใจอะไรไว้ล่าสุด | [CFR Pro Max รอบ 4](02-research/crypto-mule-accounts/cfr-pro-max-round4-synthesis.md) และ [Onchain Bridge validation รอบ 2](02-research/onchain-data-infra/validation-decision-round2.md) |
| ต้องเอางานไปต่อกับ ChatGPT/Claude | [prompt-claude-cfr-pro-max.md](02-research/crypto-mule-accounts/prompt-claude-cfr-pro-max.md) และ [prompt-chatgpt-cfr-pro-max.md](02-research/crypto-mule-accounts/prompt-chatgpt-cfr-pro-max.md) |
| ต้องเตรียมนำเสนอ/เขียนข้อเสนอ | [proposal-pack](02-research/crypto-mule-accounts/cfr-pro-max-proposal-pack.md) (ข้อเสนอหนึ่งหน้า + storyboard + บทนำเสนอ) และ [one-pager Onchain Bridge](02-research/onchain-data-infra/one-pager-onchain-bridge.md) |
| ต้องหาตัวเลข/แหล่งอ้างอิง | ทะเบียนหลักฐานของแต่ละหัวข้อ (ตารางด้านล่างคอลัมน์ "หลักฐาน") |

## โครงสร้าง

```
01-brief/                      โจทย์และบริบทบูตแคมป์
02-research/
├── crypto-mule-accounts/      หัวข้อ A  บัญชีม้าคริปโต + CFR Pro Max       (ล่าสุด)
├── onchain-data-infra/        หัวข้อ B  infra เชื่อมข้อมูลออนเชน           (ล่าสุด)
└── mule-accounts/             หัวข้อ C  บัญชีม้าธนาคาร (ฐานงานเดิม, พักไว้)
03-demo-clip/                  คลิปเดโม ทันเงิน (THAN NGERN) 39 วินาที พร้อมคำบรรยายและเพลงประกอบ
```

**คลิปเดโม:** [`03-demo-clip/final_demo.mp4`](03-demo-clip/final_demo.mp4) (0:39) คลิปเดโม ทันเงิน (THAN NGERN) สำหรับกรรมการ มีคำบรรยายไทย/อังกฤษ เพลงประกอบ SRT และ EDL ดูรายละเอียดใน [03-demo-clip/README.md](03-demo-clip/README.md)

---

## A. บัญชีม้าคริปโต + CFR Pro Max — `02-research/crypto-mule-accounts/`

ภาพรวมและตัวเลข: [README.md](02-research/crypto-mule-accounts/README.md) · [evidence.md](02-research/crypto-mule-accounts/evidence.md) · [methods.md](02-research/crypto-mule-accounts/methods.md)

**ชุด CFR Pro Max (29 ก.ย.) — อ่านตามลำดับนี้**

| ลำดับ | ไฟล์ | คืออะไร |
|---|---|---|
| 1 | [cfr-pro-max-analysis.md](02-research/crypto-mule-accounts/cfr-pro-max-analysis.md) | ผลวิเคราะห์ 12 ส่วนฉบับตัดสินใจ (ไฟล์ใหญ่สุด ~178 KB) คำตัดสิน: เดินหน้าเป็นข้อเสนอพิสูจน์แนวคิดแบบมีเงื่อนไข ยังไม่ลงทุนเป็นผลิตภัณฑ์ |
| 2 | [cfr-pro-max-proof-design.md](02-research/crypto-mule-accounts/cfr-pro-max-proof-design.md) | จากสมมติฐานสู่เคสหลักและแผนพิสูจน์ ตรวจข่าวรัฐบาล (Connect the Dots / Data Bureau) ถึงต้นทาง |
| 3 | [cfr-pro-max-infra-assessment.md](02-research/crypto-mule-accounts/cfr-pro-max-infra-assessment.md) | ประเมินเส้นทาง infra / DA connector คำถามที่ค้าง ข้อคัดค้าน 10 ข้อ |
| 4 | [cfr-pro-max-round4-synthesis.md](02-research/crypto-mule-accounts/cfr-pro-max-round4-synthesis.md) | **รอบล่าสุด** รวมข้อขัดแย้ง 11 ข้อ คำตัดสินแยกระดับ (แนวคิดมีเหตุผล / พิสูจน์บนกระดาษได้ / ยังไม่พร้อมทดลองจริง ฯลฯ) |
| — | [cfr-pro-max-decision-review.md](02-research/crypto-mule-accounts/cfr-pro-max-decision-review.md) | ทบทวนการตัดสินใจ |
| — | [cfr-pro-max-evidence-update.md](02-research/crypto-mule-accounts/cfr-pro-max-evidence-update.md) | หลักฐานเพิ่มเติม (ใช้ประกอบรอบ 4) |
| — | [cfr-pro-max-validation-contract.md](02-research/crypto-mule-accounts/cfr-pro-max-validation-contract.md) | ข้อกำหนดข้อมูล/การดำเนินการ และแผนพิสูจน์ |
| — | [cfr-pro-max-proposal-pack.md](02-research/crypto-mule-accounts/cfr-pro-max-proposal-pack.md) | ข้อเสนอหนึ่งหน้า + Storyboard + บทนำเสนอ |
| Prompt | [prompt-claude-cfr-pro-max.md](02-research/crypto-mule-accounts/prompt-claude-cfr-pro-max.md) · [prompt-chatgpt-cfr-pro-max.md](02-research/crypto-mule-accounts/prompt-chatgpt-cfr-pro-max.md) | คำสั่งส่งต่อให้ AI วิเคราะห์ต่อ (รวมบริบท หลักฐาน ข้อถกเถียงที่ยังเปิด) |

**ชุดแนวคิดเชื่อมธนาคาร–คริปโต (fiat-crypto)**

| ไฟล์ | คืออะไร |
|---|---|
| [fiat-crypto-validation.md](02-research/crypto-mule-accounts/fiat-crypto-validation.md) | ผล validation + เนื้อหาข้อเสนอ/เดโม/pitch |
| [fiat-crypto-evidence.md](02-research/crypto-mule-accounts/fiat-crypto-evidence.md) | ทะเบียนหลักฐาน |
| [fiat-crypto-paper-review.md](02-research/crypto-mule-accounts/fiat-crypto-paper-review.md) | ทบทวนบนกระดาษ 8 สถานการณ์ |

**ชุด AI วิเคราะห์ on-chain (28 ก.ย.):** [opportunity](02-research/crypto-mule-accounts/onchain-ai-opportunity.md) · [evidence](02-research/crypto-mule-accounts/onchain-ai-evidence.md) · [validation](02-research/crypto-mule-accounts/onchain-ai-validation.md)

**ชุดตรวจการชักชวนและมาตรการผู้ให้บริการ (26 ก.ย.):** [audit](02-research/crypto-mule-accounts/provider-and-recruitment-audit.md) · [evidence](02-research/crypto-mule-accounts/provider-and-recruitment-evidence.md) · [methods](02-research/crypto-mule-accounts/provider-and-recruitment-methods.md)

**อื่น ๆ:** [PAUSED.md](02-research/crypto-mule-accounts/PAUSED.md) บันทึกจุดพัก · [infra-evidence/](02-research/crypto-mule-accounts/infra-evidence/) หลักฐานทะเบียน Exchange จาก ก.ล.ต.

---

## B. infra เชื่อมข้อมูลออนเชน — `02-research/onchain-data-infra/`

| ไฟล์ | คืออะไร |
|---|---|
| [validation-decision-round2.md](02-research/onchain-data-infra/validation-decision-round2.md) | **ล่าสุด** รายงานตัดสินใจ A/B และโครงสร้างร่วม: คง A/B ศึกษาต่อ ยังไม่เลือกผู้ชนะ |
| [research-recheck-2026-09-29.md](02-research/onchain-data-infra/research-recheck-2026-09-29.md) | ผลตรวจรีเสิร์ชใหม่ครบ 4 ไฟล์ (อ่านก่อนข้อสรุป A/B) |
| [one-pager-onchain-bridge.md](02-research/onchain-data-infra/one-pager-onchain-bridge.md) | ข้อความหนึ่งหน้าฉบับปรับ |
| [unified-infra-a-b.md](02-research/onchain-data-infra/unified-infra-a-b.md) | รวม A+B: แกนร่วม + ช่องทางยินยอม (A) + ช่องทางหน้าที่ตามกฎหมาย (B) และกำแพงกั้นข้อมูล |
| [onchain-data-infra-scan.md](02-research/onchain-data-infra/onchain-data-infra-scan.md) | สำรวจโอกาสเบื้องต้น |
| [foreign-models-workflows.md](02-research/onchain-data-infra/foreign-models-workflows.md) | 12 โมเดลต่างประเทศ (Pix MED 2.0, เกาหลี, ฮ่องกง, UK, FiDA ฯลฯ) |

---

## C. บัญชีม้าธนาคาร (ฐานงานเดิม, พักตั้งแต่ 26 ก.ย.) — `02-research/mule-accounts/`

เริ่มที่ [impact-first.md](02-research/mule-accounts/impact-first.md) (กรอบผลกระทบทั้งวงจร) และ [PAUSED.md](02-research/mule-accounts/PAUSED.md) (สถานะที่ค้าง)

| โฟลเดอร์ | คืออะไร | เริ่มอ่าน | หลักฐาน |
|---|---|---|---|
| `deep-research/` | ค้นคว้าเชิงลึก 25 ก.ย. กลไกเข้าสู่วงจรบัญชีม้า มาตรการไทย เทียบ UK/SG/AU | [README](02-research/mule-accounts/deep-research/README.md) → [report](02-research/mule-accounts/deep-research/report.md) | [evidence-register](02-research/mule-accounts/deep-research/evidence-register.md), [case-register](02-research/mule-accounts/deep-research/case-register.md), [claim-audit](02-research/mule-accounts/deep-research/claim-audit.md) |
| `business-opportunities/` | คัด 8 ปัญหาเป็น 3 โอกาสธุรกิจ พร้อมแบบจำลองตลาด | [README](02-research/mule-accounts/business-opportunities/README.md) → [report](02-research/mule-accounts/business-opportunities/report.md) | [evidence-register](02-research/mule-accounts/business-opportunities/evidence-register.md), [competitors](02-research/mule-accounts/business-opportunities/competitors.md), [`market-sizing.xlsx`](02-research/mule-accounts/business-opportunities/market-sizing.xlsx) |
| `…/abc-trials/` | ลองบนเอกสาร 3 ทางๆ ละ 12 กรณี (36 สถานการณ์) | [README](02-research/mule-accounts/business-opportunities/abc-trials/README.md) → [findings](02-research/mule-accounts/business-opportunities/abc-trials/findings.md) | [edge-register](02-research/mule-accounts/business-opportunities/abc-trials/edge-register.md), [trial-cases.csv](02-research/mule-accounts/business-opportunities/abc-trials/trial-cases.csv) |
| `…/early-help-audit/` | ตรวจช่องทางช่วยเหลือ 6 ผู้ให้บริการ และโจทย์ "คนที่เริ่มสงสัยและอยากหยุด" | [README](02-research/mule-accounts/business-opportunities/early-help-audit/README.md) → [report](02-research/mule-accounts/business-opportunities/early-help-audit/report.md) | [exit-evidence](02-research/mule-accounts/business-opportunities/early-help-audit/exit-evidence.md), [validation-kit](02-research/mule-accounts/business-opportunities/early-help-audit/validation-kit.md) |
| `…/lifecycle-selection/` | คัดจุดเริ่มภายใต้กรอบทั้งวงจร: แนะนำพิสูจน์ S4 ก่อน | [decision](02-research/mule-accounts/business-opportunities/lifecycle-selection/decision.md) → [proof-kit](02-research/mule-accounts/business-opportunities/lifecycle-selection/proof-kit.md) | [evidence](02-research/mule-accounts/business-opportunities/lifecycle-selection/evidence.md) |

สรุปประเด็นบัญชีม้าสั้น ๆ: [mule-account-summary.md](02-research/mule-accounts/mule-account-summary.md)

---

## ข้อควรรู้เวลาใช้งาน

- **ลำดับความน่าเชื่อถือ:** ถ้าไฟล์ขัดกัน ให้ยึดไฟล์ที่ใหม่กว่า (รอบ 4 > รอบ 3 > ...) หลายไฟล์ระบุเองว่า "ถอนข้อสรุปเดิม" ให้อ่านหมายเหตุต้นไฟล์ก่อน
- **ไม่ได้ขึ้น repo:** เด็ค/สไลด์/รูป/แอปรายงาน, `03-solution` (ตัวจำลอง MVP), งานรอบ ส.ค., ไฟล์ประวัติ (`history/`, `decision-history/`), สคริปต์และผลชั่วคราว (`_work/`), เนื้อหาดิบจากกลุ่ม Facebook, PDF บรรยายบูตแคมป์ ดังนั้นลิงก์ในเอกสารบางจุดที่ชี้ไปไฟล์เหล่านี้จะเปิดไม่ได้ (ปกติ ไม่ใช่ไฟล์หาย) — ต้นฉบับอยู่ในโฟลเดอร์ NITMX Fintech บนเครื่องของวี
- **เอกสารใช้แหล่งสาธารณะเท่านั้น** ตัวเลขทุกตัวควรตามไปดูทะเบียนหลักฐานก่อนเอาไปอ้าง
- ตัวเลข "ยอดบัญชีที่ถูกระงับ" เป็นยอดสะสมจากข่าว/ประกาศ ไม่ใช่จำนวนผู้กระทำผิดหรือยอดสดล่าสุด
- **ห้ามเปิด repo เป็น Public** เพราะมีเนื้อหาเกี่ยวกับบัญชีม้า ข้อมูลกรณีศึกษา และข้อเสนอที่ยังไม่เผยแพร่
