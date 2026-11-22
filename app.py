import streamlit as st
import pandas as pd
from datetime import date
from db import (init_db, tao_chu_ky, cap_nhat_soi, cap_nhat_no,
                danh_dau_ban, ds_dang_ap, ds_dang_nuoi, bao_cao_nam,
                get_conn, log)

init_db()
st.set_page_config(page_title="Trại Bồ Câu", page_icon="🐦", layout="wide")

# ---------- ĐĂNG NHẬP ----------
if "user" not in st.session_state:
    st.title("🐦 Đăng nhập")
    u = st.text_input("Tài khoản (chu_trai / quan_ly)")
    p = st.text_input("Mật khẩu", type="password")
    if st.button("Đăng nhập"):
        c = get_conn()
        r = c.execute("SELECT * FROM users WHERE username=? AND mat_khau=?", (u,p)).fetchone()
        c.close()
        if r:
            st.session_state.user = dict(r); st.rerun()
        else: st.error("Sai tài khoản/mật khẩu")
    st.stop()

user = st.session_state.user
st.sidebar.success(f"👤 {user['ten']} ({user['vai_tro']})")
if st.sidebar.button("Đăng xuất"):
    del st.session_state.user; st.rerun()

menu = st.sidebar.radio("Menu", [
    "📊 Dashboard", "🥚 Tạo chu kỳ mới", "🥚 Ghi trứng đẻ",
    "🔦 Soi phôi", "🐣 Kết quả nở", "💰 Bán con",
    "📈 Báo cáo năm", "⚙️ Quản lý ô"])

# ---------- DASHBOARD ----------
if menu == "📊 Dashboard":
    st.title("Dashboard & Nhắc việc")
    today = date.today()
    ap = ds_dang_ap(); nuoi = ds_dang_nuoi()
    col = st.columns(4)
    col[0].metric("Đang ấp", len(ap))
    col[1].metric("Đang nuôi", len(nuoi))
    col[2].metric("Đến bán (28–30)", sum(1 for x in nuoi
        if x["ngay_ban_dk"] and 28 <= (today-date.fromisoformat(x["ngay_no_dk"])).days + 18 <= 999
        and x["ngay_ban_dk"] <= today.isoformat()))
    col[3].metric("Ô cần loại", 0)

    st.subheader("🔔 Việc cần làm hôm nay")
    for x in ap:
        if not x["ngay_ap"]: continue
        d = (today - date.fromisoformat(x["ngay_ap"])).days
        if 2 <= d - 0 and x["ngay_ghep"]:
            dg = (today - date.fromisoformat(x["ngay_ghep"])).days
            if 2 <= dg <= 5:
                st.info(f"Ô {x['o']}: ghép {dg} ngày — kiểm tra cặp")
        if 5 <= d <= 7: st.warning(f"Ô {x['o']}: soi phôi ({d} ngày ấp)")
        if 12 <= d <= 15: st.info(f"Ô {x['o']}: hạ tổ chim con ({d} ngày)")
        if 17 <= d <= 19: st.success(f"Ô {x['o']}: dự kiến nở ({d} ngày)")
    for x in nuoi:
        d = (today - date.fromisoformat(x["ngay_no_dk"])).days
        if 28 <= d <= 30: st.success(f"Ô {x['o']}: đến ngày bán ({d} ngày tuổi)")

# ---------- TẠO CHU KỲ ----------
elif menu == "🥚 Tạo chu kỳ mới":
    st.title("Tạo chu kỳ sinh sản mới")
    with st.form("cy"):
        pid = st.number_input("Mã ô (1–1500)", 1, 1500, 1)
        g = st.date_input("Ngày ghép cặp", date.today())
        d1 = st.date_input("Ngày đẻ trứng 1", date.today())
        d2 = st.date_input("Ngày đẻ trứng 2", date.today())
        a = st.date_input("Ngày bắt đầu ấp", date.today())
        if st.form_submit_button("Lưu"):
            cid, no, ban = tao_chu_ky(pid, g.isoformat(), d1.isoformat(),
                d2.isoformat(), a.isoformat(), user["username"])
            st.success(f"Đã tạo chu kỳ #{cid} cho ô {pid}. Nở {no}, bán {ban}")

# ---------- GHI TRỨNG ----------
elif menu == "🥚 Ghi trứng đẻ":
    st.title("Ghi trứng đẻ từng ngày")
    ap = ds_dang_ap()
    if not ap: st.info("Không có chu kỳ đang ấp")
    else:
        chon = st.selectbox("Chọn ô", [f"Ô {x['o']} (chu kỳ #{x['id']})" for x in ap])
        cid = ap[[f"Ô {x['o']} (chu kỳ #{x['id']})" for x in ap].index(chon)]["id"]
        with st.form("egg"):
            ngay = st.date_input("Ngày đẻ", date.today())
            so = st.number_input("Số trứng", 1, 3, 1)
            if st.form_submit_button("Ghi"):
                c = get_conn()
                c.execute("INSERT INTO eggs(cycle_id,ngay_de,so_luong) VALUES(?,?,?)",
                          (cid, ngay.isoformat(), so))
                c.commit(); c.close()
                log(user["username"], f"Ghi trứng chu kỳ {cid}"); st.success("Đã ghi")

# ---------- SOI PHÔI ----------
elif menu == "🔦 Soi phôi":
    st.title("Cập nhật soi phôi")
    ap = ds_dang_ap()
    if not ap: st.info("Không có chu kỳ đang ấp")
    else:
        chon = st.selectbox("Chọn ô", [f"Ô {x['o']} (chu kỳ #{x['id']})" for x in ap])
        cid = ap[[f"Ô {x['o']} (chu kỳ #{x['id']})" for x in ap].index(chon)]["id"]
        with st.form("sp"):
            ngay = st.date_input("Ngày soi", date.today())
            co = st.number_input("Có phôi", 0, 5, 0)
            khong = st.number_input("Không phôi (trắng)", 0, 5, 0)
            luu = st.number_input("Phôi chết lưu", 0, 5, 0)
            if st.form_submit_button("Lưu"):
                cap_nhat_soi(cid, ngay.isoformat(), co, khong, luu, user["username"])
                if khong > 0 and co == 0 and luu == 0:
                    st.error(f"⚠️ Ô trắng hoàn toàn — cân nhắc loại")
                st.success("Đã lưu")

# ---------- KẾT QUẢ NỞ ----------
elif menu == "🐣 Kết quả nở":
    st.title("Cập nhật kết quả nở")
    ap = ds_dang_ap()
    if not ap: st.info("Không có chu kỳ đang ấp")
    else:
        chon = st.selectbox("Chọn ô", [f"Ô {x['o']} (chu kỳ #{x['id']})" for x in ap])
        cid = ap[[f"Ô {x['o']} (chu kỳ #{x['id']})" for x in ap].index(chon)]["id"]
        pid = ap[[f"Ô {x['o']} (chu kỳ #{x['id']})" for x in ap].index(chon)]["o"]
        with st.form("n"):
            ngay = st.date_input("Ngày nở", date.today())
            no = st.number_input("Số con nở", 0, 5, 0)
            chet = st.number_input("Số chim chết", 0, 5, 0)
            if st.form_submit_button("Lưu"):
                cap_nhat_no(cid, pid, ngay.isoformat(), no, chet, user["username"])
                st.success("Đã lưu — ô chuyển Đang nuôi")

# ---------- BÁN ----------
elif menu == "💰 Bán con":
    st.title("Đánh dấu bán con")
    nuoi = ds_dang_nuoi()
    if not nuoi: st.info("Không có ô đang nuôi")
    else:
        chon = st.selectbox("Chọn ô", [f"Ô {x['o']}" for x in nuoi])
        pid = nuoi[[f"Ô {x['o']}" for x in nuoi].index(chon)]["o"]
        if st.button("Xác nhận đã bán — ô chuyển Trống"):
            danh_dau_ban(pid, user["username"]); st.success(f"Ô {pid} đã bán")

# ---------- BÁO CÁO ----------
elif menu == "📈 Báo cáo năm":
    st.title("Báo cáo tổng hợp theo năm")
    nam = st.number_input("Năm", 2024, 2030, date.today().year)
    rows = bao_cao_nam(nam)
    if not rows: st.info("Chưa có dữ liệu năm này")
    else:
        df = pd.DataFrame(rows)
        df["%trang"] = (df.tong_trang / df.tong_trung.replace(0,1) * 100).round(1)
        df["%luu"]   = (df.tong_luu / df.tong_trung.replace(0,1) * 100).round(1)
        df["%no"]    = (df.tong_no / df.tong_trung.replace(0,1) * 100).round(1)
        st.dataframe(df, use_container_width=True)
        st.metric("Tổng con nở cả trại", int(df.tong_no.sum()))
        st.metric("Tổng con chết", int(df.tong_chet.sum()))
        st.metric("% nở trung bình", f"{df['%no'].mean():.1f}%")
        st.download_button("📥 Xuất CSV",
            df.to_csv(index=False).encode("utf-8-sig"), f"bao_cao_{nam}.csv")

# ---------- QUẢN LÝ Ô ----------
elif menu == "⚙️ Quản lý ô":
    st.title("Quản lý ô")
    pid = st.number_input("Mã ô", 1, 1500, 1)
    c = get_conn(); r = c.execute("SELECT * FROM pairs WHERE id=?", (pid,)).fetchone(); c.close()
    st.write(dict(r))
    with st.form("e"):
        tt = st.selectbox("Trạng thái", ["trong","dang_ap","dang_nuoi","can_loai"])
        ghi = st.text_area("Ghi chú")
        loai = st.checkbox("Đánh dấu cần loại")
        if st.form_submit_button("Lưu"):
            c = get_conn()
            c.execute("UPDATE pairs SET trang_thai=?, ghi_chu=?, can_loai=? WHERE id=?",
                      (tt, ghi, int(loai), pid))
            c.commit(); c.close()
            log(user["username"], f"Sửa ô {pid}"); st.success("Đã lưu")
