import html
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

DATA_FILE = os.environ.get("RESEARCH_FILE", "/data/research.txt")

DEFAULT_RESEARCH = """ข้อมูลทั่วไป
ชื่อเรื่อง (ไทย): การพัฒนาระบบสืบค้นและตอบคำถามข้อมูลสารสนเทศและสถิติด้าน*****ด้วยเทคโนโลยี RAG และโมเดลภาษาขนาดใหญ่
ชื่อเรื่อง (อังกฤษ): Development of a Search and Question-Answering System for **** Information and Statistics Using RAG Technology and Large Language Models
ผู้วิจัย: นายยุทธศาสตร์ คำคนซื่อ (หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต)
สังกัด: สาขาวิชาวิศวกรรมคอมพิวเตอร์ วิทยาลัยวิศวกรรมศาสตร์และเทคโนโลยี มหาวิทยาลัยธุรกิจบัณฑิตย์
บทที่ 1: บทนำ
ความเป็นมาและความสำคัญของปัญหา: ระบบสารสนเทศและฐานข้อมูลด้านการ*****มีผู้ใช้งานจากหลายระดับ (ส่วนกลาง, ภูมิภาค 1–9, จังหวัด, อำเภอ, อปท.) และมีการหมุนเวียนบุคลากรต่อเนื่อง ข้อมูลแบ่งเป็น 2 ลักษณะ คือ ข้อมูลไม่มีโครงสร้าง (คู่มือการใช้งาน แนวทางปฏิบัติ ระเบียบ) และ ข้อมูลมีโครงสร้าง (สถิติผลการดำเนินงานด้านป้องกัน ปราบปราม และบำบัดรักษา) การค้นหาคู่มือด้วย Keyword แบบเดิมและการวิเคราะห์สถิติที่ต้องพึ่งทักษะ SQL หรือทีม Helpdesk ทำให้เกิดความล่าช้า จึงนำ RAG + LLM (On-premise) + Text-to-SQL มาพัฒนาเป็นระบบต้นแบบถาม-ตอบด้วยภาษาธรรมชาติ
วัตถุประสงค์ (3 ข้อ):
พัฒนาระบบต้นแบบสืบค้นและตอบคำถามด้านการใช้งานระบบสารสนเทศและฐานข้อมูลสถิติด้วย LLM + RAG
ประเมินประสิทธิภาพเชิงเทคนิคด้านความถูกต้องของการสืบค้นเอกสาร ข้อมูลเชิงโครงสร้าง และการสร้างคำตอบ
ศึกษาความพึงพอใจและการยอมรับเทคโนโลยีของผู้ใช้งาน
ขอบเขตการศึกษา:
ด้านข้อมูล: ใช้เอกสารคู่มือ/FAQ ภาษาไทย และชุดข้อมูลสถิติภาพรวมที่เปิดเผยทั่วไป/ข้อมูลจำลอง (Synthetic & Publicly Aggregated Dataset) ไม่มีข้อมูลส่วนบุคคล (PII) หรือข้อมูลชั้นความลับ และไม่เชื่อมต่อฐานข้อมูลปฏิบัติการจริง
ด้านเทคโนโลยี: Hybrid RAG + Text-to-SQL, Open-weight LLM (ตระกูล Llama และ Qwen) แบบ On-premise, PostgreSQL + pgvector และ Web Application ที่สตรีมคำตอบพร้อมอ้างอิงแหล่งที่มา
ด้านประชากร/กลุ่มตัวอย่าง: เจ้าหน้าที่ผู้ปฏิบัติงาน นักวิเคราะห์ และ Helpdesk เลือกแบบเจาะจง 30 คน
ด้านการประเมินผล: วัดประสิทธิภาพเชิงเทคนิค (RAG, Text-to-SQL, ความปลอดภัย) และวัดความพึงพอใจ/การยอมรับเทคโนโลยีของผู้ใช้
ประโยชน์ที่คาดว่าจะได้รับ: ลดเวลาค้นหาข้อมูลของเจ้าหน้าที่ ลดภาระงานซ้ำซ้อนของ Helpdesk สนับสนุนการทำงานตลอด 24 ชั่วโมง ช่วยถ่ายทอดงานบุคลากรใหม่ และเป็นต้นแบบ On-premise AI ตามแนวทางรัฐบาลดิจิทัล

บทที่ 2: แนวคิด ทฤษฎี และงานวิจัยที่เกี่ยวข้อง
ครอบคลุม 9 หัวข้อย่อยสำคัญ:
ระบบสารสนเทศด้าน****: โครงสร้างข้อมูลตัวชี้วัด/สถิติรายจังหวัด การจัดการสิทธิ์แบบ RBAC ระดับส่วนกลาง–พื้นที่ (ฝ่ายปกครอง, ศึกษาธิการ, แรงงาน, สาธารณสุข, บังคับใช้กฎหมาย) และความท้าทายของ Helpdesk
NLP และพัฒนาการ Chatbot: ตั้งแต่ Tokenization, Text Embedding, Contextual Understanding จนถึงวิวัฒนาการจาก Rule-based → Statistical ML → Transformer/LLM
LLM และการประมวลผลภายในองค์กร (On-premise): กลไก Next-Token Prediction, Transformer, Self-Attention; เปรียบเทียบขนาดโมเดล (3B–8B vs 70B+) และข้อดีของ Open-weight LLM แบบ On-premise ด้าน Data Sovereignty และ PDPA
สถาปัตยกรรม RAG: ลดปัญหา Hallucination ผ่าน 5 ขั้นตอน (Ingestion/Chunking → Embedding → Vector DB → Retrieval → Prompt Augmentation & Generation)
วิวัฒนาการ RAG: Naive RAG → Advanced RAG (Query Rewriting, Hybrid Search, Reranking) → Modular RAG (Iterative/Multi-hop, Self-RAG, GraphRAG) รวมถึง Query Intent Routing และ Layout-Aware Ingestion (แปลงตาราง PDF เป็น Markdown Table)
Text-to-SQL และความปลอดภัย: Dynamic Schema Linking (COMMENT ON COLUMN), Dynamic Few-Shot Retrieval, Self-Healing Reflection Loop และ AST Security Guardrail (สกัดกั้น DDL/DML และบังคับ LIMIT)
Microservices & Real-Time Optimization: แยกบริการด้วย Docker, Semantic Caching เพื่อลดเวลาตอบคำถามซ้ำ และ SSE Streaming เพื่อลด TTFT
กรอบการประเมินผล:
ด้านผู้ใช้: SUS (เกณฑ์มาตรฐาน ≥ 68 คะแนน) และ TAM (PU, PEOU)
ด้านเทคนิค: RAG (Context Precision, Context Recall, Faithfulness, Answer Relevancy), Text-to-SQL (Valid SQL Rate, Execution Accuracy), ความปลอดภัย/ความเร็ว (Attack Block Rate, TTFT, Total Latency)
งานวิจัยที่เกี่ยวข้อง (8 เรื่อง): งานวิจัยต่างประเทศ 7 เรื่อง (Rakesh More 2026; Ask-EDA 2024; CodeQA 2026; QuIM-RAG 2025; Kumar et al. 2026; Ganesh et al. 2026; De Silva & Asanka 2025) และงานวิจัยในประเทศ 1 เรื่อง (ประทีป หมื่นทิศ และ สุขุมาล กิติสิน 2025)

บทที่ 3: ระเบียบวิธีวิจัย
ประยุกต์ใช้ DSRM (Design Science Research Methodology) ร่วมกับ Agile SDLC แบ่งเป็น 5 ขั้นตอน:
3.1 วิเคราะห์ปัญหาและกำหนดความต้องการ:
FR1–FR5: จำแนกเจตนาอัตโนมัติ (SQL/เอกสาร/ไฮบริด/สนทนา), แปลงภาษาไทยเป็น SQL และสรุปผล, ค้นเอกสาร PDF พร้อม Citations (ชื่อไฟล์/หน้า/คะแนน), ควบคุมสิทธิ์ RBAC ตามแผนก, และตอบกลับแบบ SSE Streaming
NFR1–NFR4: ตรวจ SQL ด้วย AST ป้องกันการเขียน/ลบ 100%, ประมวลผล On-premise 100%, คำถามซ้ำตอบใน ≤ 50 ms, และ Self-Healing แก้ไข SQL ผิดพลาดได้ ≥ 2 รอบ
3.2 สถาปัตยกรรม 6 เลเยอร์ และขั้นตอนวิธี:
Gateway: Nginx (Rate Limit 15 req/min/IP, SSE Buffering)
Presentation: PHP Laravel 13
Application & Orchestration: FastAPI (Intent Routing, Pipeline, Guardrails)
Asynchronous Worker: Celery + Redis (ประมวลผล PDF เบื้องหลัง)
Storage & Data: PostgreSQL 16, Qdrant (Vector DB), MinIO (S3)
AI Hardware Acceleration: Ollama (รองรับ Intel Arc Vulkan / NVIDIA CUDA)
ขั้นตอนวิธีหลัก: Semantic Pattern Matcher แยก SQL_QUERY / DOC_SEARCH / HYBRID; Text-to-SQL พร้อม AST Guardrail + Self-Healing Loop; และ Document RAG แบบ Hybrid 2-Stage Re-ranking (Dense Vector bge-m3 1,024 มิติ + Over-fetch 3×k + Lexical Scoring คัด Top-k = 3)
3.3 การเตรียมข้อมูลและชุดทดสอบมาตรฐาน (Golden Benchmark 100 คำถาม):
Structured Data Warehouse (business_dw): ตารางสถิติจำลองระดับจังหวัด/ภูมิภาคด้าน*** (เช่น oncb_regions, provincial_drug_cases, provincial_drug_seizures, provincial_rehab_admissions, provincial_village_assessments, provincial_school_immunity, it_service_tickets ฯลฯ) พร้อม COMMENT ON COLUMN ภาษาไทย
Unstructured Corpus: เอกสาร PDF คู่มือ ระเบียบ ข้อบังคับ
Benchmark 100 ข้อ: Text-to-SQL 50 ข้อ, Document RAG 40 ข้อ, Adversarial/Security Attacks 10 ข้อ
3.4 การพัฒนาระบบ: docker-compose.yml บนเครือข่าย enterprise_rag_network, สกัด PDF ด้วย pdfplumber + format_table_as_markdown() (Chunk 800 ตัวอักษร, Overlap 100), บัญชีฐานข้อมูล readonly_dw_user + SQLGuard (sqlglot), และ SemanticCache บน Redis (TTL 24 ชั่วโมง)
3.5 เกณฑ์การประเมิน: EX, VSR, SHR, Precision@3, Recall@3, Faithfulness, Citation Accuracy, ABR (100%), Over-privileged Access (0%), TTFT, Total Latency และ VRAM Budget บนระดับ 8GB

บทที่ 4: ผลการวิจัย
4.1 ผลสัมฤทธิ์ของระบบและ UI: ติดตั้งและรัน Docker Stack ครบ 8 เซอร์วิส (Nginx, Laravel 13, FastAPI, Celery, PostgreSQL 16, Redis 7, Qdrant, MinIO) พร้อมหน้าเว็บ 4 ส่วน (Chat Workspace, RBAC Department Switcher, Document Management, Health & Data Explorer)
4.2 ผลทดสอบ Text-to-SQL (50 คำถาม):
Valid SQL Rate (VSR): ภาพรวมเพิ่มจาก 72.0% (Zero-Shot) เป็น 94.0% (Few-Shot + Self-Healing)
Execution Accuracy (EX): ภาพรวมเพิ่มจาก 64.0% เป็น 92.0% (ระดับง่าย 100.0%, ปานกลาง 95.0%, ซับซ้อน 80.0%)
Self-Healing Recovery Rate (SHR): จากคำสั่งที่ผิดพลาดครั้งแรก 7 ข้อ แก้ไขสำเร็จในรอบที่ 1 ได้ 5 ข้อ (71.4%) และรอบที่ 2 อีก 1 ข้อ รวมอัตราการกู้คืน 85.7%
4.3 ผลทดสอบ Document RAG (40 คำถาม) เทียบ Dense Search กับ Hybrid 2-Stage Re-ranking:
Precision@3: 75.0% → 92.5% (+17.5%)
Recall@3: 70.0% → 90.0% (+20.0%)
Faithfulness: 82.5% → 97.5% (+15.0%)
Table Information Extraction Accuracy: 55.0% → 95.0% (+40.0%)
Citation Accuracy: 87.5% → 100.0% (+12.5%)
4.4 ผลทดสอบความปลอดภัย (Security Guardrail): ทดสอบการโจมตีและคำสั่งต้องห้าม (DROP/DELETE/TRUNCATE, INSERT/UPDATE, SQL Injection Chaining, เข้าถึงตารางระบบ, DoS ไม่มี LIMIT) รวม 40 กรณี ได้ Attack Block Rate (ABR) 100.0% (ผ่านเข้า Database 0 ข้อ และบังคับ LIMIT 100 อัตโนมัติ)
4.5 ประสิทธิภาพเวลาตอบสนอง (100 คำขอ) และการใช้ VRAM:
Semantic Cache Hit: TTFT 12.5 ms, Total Latency 28.4 ms (เร็วกว่า Cache Miss มากกว่า 50 เท่า)
Cache Miss: Text-to-SQL (ไม่มี Error) 1.42 วินาที, Text-to-SQL (Self-Healing 1 รอบ) 2.65 วินาที, Document RAG 1.85 วินาที, Hybrid Pipeline 3.12 วินาที
VRAM (Intel Arc Pro 140T 8GB): qwen2.5:3b ใช้ 1.92 GB + bge-m3 ใช้ 1.18 GB รวม ~3.10 GB (38.7% ของ VRAM)
4.6 ผลการประเมินความพึงพอใจผู้ใช้ (UAT): ประเมินจากกลุ่มตัวอย่าง 20 คน ด้วยมาตรวัด 5 ระดับ ได้คะแนนภาพรวม 4.70 (S.D. 0.46) อยู่ในระดับ มากที่สุด (ด้านความมั่นใจความปลอดภัยสูงสุดที่ 4.80 และความน่าเชื่อถือจาก Citations 4.75)
"""


def ensure_data_file():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_RESEARCH.strip())


def read_research():
    ensure_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return f.read()


def write_research(content):
    ensure_data_file()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(content)


class ResearchHandler(BaseHTTPRequestHandler):
    def send_html(self, status_code, body):
        data = body.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        host = self.headers.get("Host", "").lower()
        query = urllib.parse.parse_qs(parsed.query)

        # หน้า Admin แก้ไขบทความ (/edit หรือ admin.id-239.com)
        if parsed.path in ("/edit", "/edit/") or (parsed.path == "/" and host.startswith("admin.")):
            content = html.escape(read_research())
            saved_banner = (
                '<div class="alert">บันทึกข้อมูลสรุปงานวิจัยเรียบร้อยแล้ว! '
                '<a href="http://www.id-239.com/research" target="_blank">เปิดดูหน้า www.id-239.com/research &rarr;</a></div>'
                if query.get("saved") == ["1"]
                else ""
            )
            page = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Admin - แก้ไขสรุปงานวิจัย (68130239)</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: 'Segoe UI', Tahoma, sans-serif;
      background: linear-gradient(135deg, #f5f3ff 0%, #fef3c7 100%);
      color: #1e293b;
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    .navbar {{
      background: rgba(255, 255, 255, 0.92);
      border-bottom: 1px solid #ddd6fe;
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand {{ font-weight: 800; font-size: 1.05rem; color: #6d28d9; display: flex; align-items: center; gap: 10px; }}
    .admin-pill {{ background: #fef3c7; color: #b45309; border: 1px solid #fcd34d; padding: 3px 10px; border-radius: 999px; font-size: 0.75rem; }}
    .nav-links {{ display: flex; gap: 18px; flex-wrap: wrap; }}
    .nav-links a {{ text-decoration: none; color: #475569; font-weight: 600; font-size: 0.95rem; }}
    .nav-links a:hover {{ color: #6d28d9; }}
    .main {{ flex: 1; padding: 36px 16px; }}
    .container {{
      max-width: 860px;
      margin: auto;
      background: #ffffff;
      padding: 32px;
      border-radius: 18px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 18px 40px rgba(109, 40, 217, 0.08);
    }}
    h1 {{ color: #5b21b6; margin: 0 0 6px; font-size: 1.6rem; }}
    .sub {{ color: #64748b; margin: 0 0 20px; font-size: 0.95rem; }}
    .alert {{
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #6ee7b7;
      padding: 12px 16px;
      border-radius: 10px;
      margin-bottom: 16px;
      font-weight: 600;
    }}
    .alert a {{ color: #047857; margin-left: 8px; }}
    textarea {{
      width: 100%;
      height: 360px;
      padding: 16px;
      border-radius: 12px;
      border: 1.5px solid #cbd5e1;
      background: #f8fafc;
      color: #0f172a;
      font-family: inherit;
      font-size: 1rem;
      line-height: 1.7;
      resize: vertical;
      outline: none;
    }}
    textarea:focus {{ border-color: #7c3aed; background: #ffffff; }}
    .toolbar {{
      margin-top: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    button {{
      background: linear-gradient(135deg, #7c3aed, #6d28d9);
      color: #ffffff;
      border: none;
      padding: 12px 26px;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 6px 16px rgba(124, 58, 237, 0.25);
    }}
    button:hover {{ opacity: 0.94; }}
    .counter {{ font-size: 0.92rem; color: #475569; background: #f1f5f9; padding: 8px 14px; border-radius: 8px; }}
    .counter.ok {{ background: #dcfce7; color: #166534; font-weight: 600; }}
  </style>
</head>
<body>
  <nav class="navbar">
    <div class="brand">Admin Panel <span class="admin-pill">ADMIN MODE</span></div>
    <div class="nav-links">
      <a href="http://www.id-239.com/">Portal</a>
      <a href="http://www.id-239.com/about">About</a>
      <a href="http://www.id-239.com/research">ดูหน้า Research</a>
    </div>
  </nav>

  <main class="main">
    <div class="container">
      <h1>แก้ไขสรุปงานวิจัยวิชาสัมมนา</h1>
      <p class="sub">Service: <strong>app-research (/edit)</strong> &bull; ข้อมูลจะถูกบันทึกลง PersistentVolumeClaim (PVC) &bull; Host: {html.escape(host)}</p>
      {saved_banner}
      <form method="POST" action="/edit">
        <textarea id="editor" name="content" required>{content}</textarea>
        <div class="toolbar">
          <button type="submit">บันทึกข้อมูล (Save to PVC)</button>
          <div id="counter" class="counter">กำลังนับคำ...</div>
        </div>
      </form>
    </div>
  </main>

  <script>
    const editor = document.getElementById('editor');
    const counter = document.getElementById('counter');
    function updateCount() {{
      const text = editor.value.trim();
      const words = text ? text.split(/\\s+/).length : 0;
      const chars = text.length;
      counter.textContent = `จำนวนคำ (Whitespace): ${{words}} คำ | ตัวอักษร: ${{chars}} ตัว`;
      counter.className = (words >= 300 && words <= 500) ? 'counter ok' : 'counter';
    }}
    editor.addEventListener('input', updateCount);
    updateCount();
  </script>
</body>
</html>"""
            self.send_html(200, page)
            return

        # หน้าแสดงผล /research
        content = read_research()
        word_count = len(content.split())
        escaped_content = html.escape(content).replace("\n", "<br>")
        page = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Research Summary - 68130239</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: 'Segoe UI', Tahoma, sans-serif;
      background: linear-gradient(135deg, #ecfdf5 0%, #f0fdfa 55%, #eff6ff 100%);
      color: #1e293b;
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    .navbar {{
      background: rgba(255, 255, 255, 0.9);
      border-bottom: 1px solid #d1fae5;
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand {{ font-weight: 800; font-size: 1.1rem; color: #047857; }}
    .nav-links {{ display: flex; gap: 18px; flex-wrap: wrap; }}
    .nav-links a {{ text-decoration: none; color: #475569; font-weight: 600; font-size: 0.95rem; }}
    .nav-links a:hover, .nav-links a.active {{ color: #059669; }}
    .main {{ flex: 1; padding: 36px 16px; }}
    .container {{
      max-width: 840px;
      margin: auto;
      background: #ffffff;
      padding: 40px;
      border-radius: 18px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 18px 40px rgba(5, 150, 105, 0.08);
    }}
    .header-meta {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; }}
    .badge {{
      display: inline-block;
      background: #d1fae5;
      color: #065f46;
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 700;
    }}
    .count-pill {{
      background: #f1f5f9;
      color: #475569;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 600;
    }}
    h1 {{ color: #0f172a; margin: 0 0 8px; font-size: 1.8rem; }}
    .author {{ color: #64748b; margin: 0 0 24px; font-size: 0.95rem; }}
    .content {{
      background: #f8fafc;
      padding: 28px;
      border-radius: 14px;
      border: 1px solid #e2e8f0;
      font-size: 1.05rem;
      line-height: 1.85;
      color: #1e293b;
    }}
    .footer {{
      margin-top: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 0.92rem;
    }}
    .edit-btn {{
      background: #059669;
      color: #ffffff;
      padding: 9px 18px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
    }}
    .edit-btn:hover {{ background: #047857; }}
  </style>
</head>
<body>
  <nav class="navbar">
    <div class="brand">K8s Ingress Portal &bull; id-239</div>
    <div class="nav-links">
      <a href="/">หน้าแรก</a>
      <a href="/about">About</a>
      <a class="active" href="/research">Research</a>
      <a href="/api/Hello%2068130239">API</a>
      <a href="http://admin.id-239.com">Admin</a>
    </div>
  </nav>

  <main class="main">
    <div class="container">
      <div class="header-meta">
        <span class="badge">Service: app-research</span>
        <span class="count-pill">ความยาว: {word_count} คำ/กลุ่มคำ</span>
      </div>
      <h1>สรุปงานวิจัยวิชาสัมมนา</h1>
      <p class="author">โดย Yutthasatr Khumkhonsue (รหัสนักศึกษา 68130239)</p>
      <div class="content">{escaped_content}</div>
      <div class="footer">
        <span style="color:#64748b;">Storage: PersistentVolumeClaim (research-pvc-239)</span>
        <a class="edit-btn" href="http://admin.id-239.com">แก้ไขบทความ (admin.id-239.com)</a>
      </div>
    </div>
  </main>
</body>
</html>"""
        self.send_html(200, page)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/edit", "/edit/", "/"):
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8")
            form = urllib.parse.parse_qs(raw)
            new_content = form.get("content", [""])[0].strip()
            if new_content:
                write_research(new_content)
            self.send_response(303)
            self.send_header("Location", "/edit?saved=1")
            self.end_headers()
            return
        self.send_html(404, "Not Found")


if __name__ == "__main__":
    ensure_data_file()
    server = HTTPServer(("0.0.0.0", 8080), ResearchHandler)
    print("app-research listening on port 8080...")
    server.serve_forever()
