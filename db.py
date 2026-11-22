import sqlite3
from datetime import date, timedelta

DB = "pigeon.db"

def get_conn():
    c = sqlite3.connect(DB, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = get_conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, ten TEXT, vai_tro TEXT, mat_khau TEXT);
    CREATE TABLE IF NOT EXISTS pairs(id INTEGER PRIMARY KEY, trang_thai TEXT DEFAULT 'trong', ghi_chu TEXT DEFAULT '', can_loai INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS cycles(id INTEGER PRIMARY KEY AUTOINCREMENT, pair_id INTEGER, ngay_ghep TEXT, ngay_de1 TEXT, ngay_de2 TEXT, ngay_ap TEXT, ngay_no_dk TEXT, ngay_ban_dk TEXT, trang_thai TEXT DEFAULT 'dang_ap');
    CREATE TABLE IF NOT EXISTS eggs(id INTEGER PRIMARY KEY AUTOINCREMENT, cycle_id INTEGER, ngay_de TEXT, so_luong INTEGER DEFAULT 1, ghi_chu TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS soi_phoi(id INTEGER PRIMARY KEY AUTOINCREMENT, cycle_id INTEGER, ngay_soi TEXT, co_phoi INTEGER DEFAULT 0, khong_phoi INTEGER DEFAULT 0, chet_luu INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS ket_qua_no(id INTEGER PRIMARY KEY AUTOINCREMENT, cycle_id INTEGER, ngay_no TEXT, so_no INTEGER DEFAULT 0, so_chet INTEGER DEFAULT 0);
    """)
    
    n = c.execute("SELECT COUNT(*) FROM pairs").fetchone()[0]
    if n == 0:
        c.executemany("INSERT INTO pairs(id) VALUES(?)", [(i,) for i in range(1,1501)])
        
    u = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if u == 0:
        c.execute("INSERT INTO users VALUES('chu_trai', 'Chu trai', 'admin', '123456')")
        c.execute("INSERT INTO users VALUES('quan_ly', 'Quan ly', 'user', '123456')")
        
    c.commit()
    c.close()

def log(username, hanh_dong):
    pass

def tao_chu_ky(pair_id, ngay_ghep, ngay_de1, ngay_de2, ngay_ap, username):
    c = get_conn()
    no_dk = (date.fromisoformat(ngay_ap) + timedelta(days=18)).isoformat()
    ban_dk = (date.fromisoformat(no_dk) + timedelta(days=28)).isoformat()
    cur = c.execute("INSERT INTO cycles(pair_id,ngay_ghep,ngay_de1,ngay_de2,ngay_ap,ngay_no_dk,ngay_ban_dk) VALUES(?,?,?,?,?,?,?)", (pair_id, ngay_ghep, ngay_de1, ngay_de2, ngay_ap, no_dk, ban_dk))
    c.execute("UPDATE pairs SET trang_thai='dang_ap' WHERE id=?", (pair_id,))
    c.commit()
    cid = cur.lastrowid
    c.close()
    return cid, no_dk, ban_dk

def cap_nhat_soi(cycle_id, ngay, co, khong, luu, username):
    c = get_conn()
    c.execute("INSERT INTO soi_phoi(cycle_id,ngay_soi,co_phoi,khong_phoi,chet_luu) VALUES(?,?,?,?,?)", (cycle_id, ngay, co, khong, luu))
    c.commit()
    c.close()

def cap_nhat_no(cycle_id, pair_id, ngay, so_no, so_chet, username):
    c = get_conn()
    c.execute("INSERT INTO ket_qua_no(cycle_id,ngay_no,so_no,so_chet) VALUES(?,?,?,?)", (cycle_id, ngay, so_no, so_chet))
    c.execute("UPDATE cycles SET trang_thai='dang_nuoi' WHERE id=?", (cycle_id,))
    c.execute("UPDATE pairs SET trang_thai='dang_nuoi' WHERE id=?", (pair_id,))
    c.commit()
    c.close()

def danh_dau_ban(pair_id, username):
    c = get_conn()
    c.execute("UPDATE pairs SET trang_thai='trong' WHERE id=?", (pair_id,))
    c.execute("UPDATE cycles SET trang_thai='da_ban' WHERE pair_id=? AND trang_thai='dang_nuoi'", (pair_id,))
    c.commit()
    c.close()

def ds_dang_ap():
    c = get_conn()
    r = c.execute("SELECT c.*, p.id as o FROM cycles c JOIN pairs p ON p.id=c.pair_id WHERE c.trang_thai='dang_ap'").fetchall()
    c.close()
    return [dict(x) for x in r]

def ds_dang_nuoi():
    c = get_conn()
    r = c.execute("SELECT c.*, p.id as o FROM cycles c JOIN pairs p ON p.id=c.pair_id WHERE c.trang_thai='dang_nuoi'").fetchall()
    c.close()
    return [dict(x) for x in r]

def bao_cao_nam(nam):
    return []
