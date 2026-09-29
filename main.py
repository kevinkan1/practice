from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from database import koneksi
from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"data": {
            "judul": "Sistem Informasi Mahasiswa",
            "kampus": "UBM",
            "deskripsi": "Aplikasi pengelolaan data mahasiswa."
        }}
    )

@app.get("/mahasiwa")
def mahasiswa(request: Request):
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tbl_mahasiwa ORDER BY nim")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse(
        request=request,
        name="mahasiswa.html",
        context={"mahasiswa": mahasiswa}
    )
    
@app.get("/insert")
def form_insert(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="insert.html",
        context={}
    )
    
@app.post("/insert")
def insert(
    nim: str = Form(...),
    nama: str = Form(...),
    tugas: float = Form(...),
    uts: float = Form(...),
    uas: float = Form(...)
):
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tbl_mahasiswa VALUES (%s, %s, %s, %s, %s)",
        (nim, nama, tugas, uts, uas)
    )
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse("/mahaiswa", status_code=303)

@app.get("/edit/{nim}")
def form_edit(nim: str, request: Request):
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tbl_mahasiwa WHERE nim = %s", (nim, ))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"mahasiswa": data}
    )
    
@app.post("/edit/{nim}")
def edit(
    nim: str,
    nama: str = Form(...),
    tugas: float = Form(...),
    uts: float = Form(...),
    uas: float = Form(...)
):
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """UPDATE tbl_mahasiswa SET nama=%s, tugas=%s,
        uts=%s, uas=%s WHERE nim=%s""",
        (nama, tugas, uts, uas, nim)
    )
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse("/barang", status_code=303)

@app.post("/delete/{nim}")
def delete(nim: str):
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("DELETE FROM tbl_mahasiswa WHERE nim = %s", (nim,))
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse("/mahasiswa", status_code=303)