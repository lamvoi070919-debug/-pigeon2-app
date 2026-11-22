<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quản Lý Trại Chim</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --primary: #2e7d32; --bg: #f4f7f6; --card: #ffffff; --text: #333; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg); margin: 0; padding: 15px; color: var(--text); }
        .container { max-width: 1200px; margin: auto; }
        
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px; }
        .stat-card { background: var(--card); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; border: 1px solid #eee; }
        .stat-card h3 { margin: 0; font-size: 13px; color: #666; }
        .stat-card p { margin: 10px 0 5px 0; font-size: 24px; font-weight: bold; color: var(--primary); }
        .btn-detail { background: #e3f2fd; color: #2196f3; border: 1px solid #90caf9; padding: 5px 10px; border-radius: 4px; font-size: 11px; cursor: pointer; width: 100%; margin-top: 5px; font-weight: bold; }

        .filter-result-box { display: none; background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #2196f3; }
        .filter-result-box h4 { margin: 0 0 10px 0; color: #2196f3; }
        .filter-result-box ul { margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.6; }
        .close-filter { float: right; background: #ff5252; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 12px; }

        .chart-container { background: var(--card); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }

        .form-section { background: var(--card); padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .section-title { font-size: 18px; color: var(--primary); border-bottom: 2px solid var(--primary); padding-bottom: 5px; margin-bottom: 15px; margin-top: 0; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
        .form-group { margin-bottom: 10px; }
        label { display: block; font-weight: 600; margin-bottom: 5px; font-size: 13px; }
        input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-family: inherit; }
        
        .auto-calc-box { background: #e8f5e9; border: 1px dashed #4caf50; padding: 10px; border-radius: 5px; margin-top: 5px; font-size: 13px; color: #2e7d32; font-weight: bold; }

        .btn-group { display: flex; gap: 10px; margin-top: 10px; }
        button { border: none; padding: 12px 20px; font-size: 15px; border-radius: 5px; cursor: pointer; font-weight: bold; flex: 1; }
        .btn-save { background: var(--primary); color: white; }
        .btn-cancel { background: #f44336; color: white; display: none; }
        
        .table-section { background: var(--card); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; min-width: 1100px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; font-size: 13px; }
        th { background: #e8f5e9; color: var(--primary); font-weight: bold; }
        tr:hover { background: #f1f8e9; }
        .badge { padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; color: white; display: inline-block; margin-bottom: 2px;}
        .bg-green { background: #4caf50; } .bg-red { background: #f44336; } .bg-yellow { background: #ffc107; color: #333; } .bg-blue { background: #2196f3; }
        
        .action-btns { display: flex; gap: 5px; }
        .btn-edit { background: #ffc107; color: #333; padding: 5px 10px; border-radius: 3px; cursor: pointer; }
        .btn-delete { background: #ff5252; color: white; padding: 5px 10px; border-radius: 3px; cursor: pointer; }
    </style>
</head>
<body>

<div class="container">
    <h2 style="text-align: center; color: var(--primary);">🐦 QUẢN LÝ TRẠI CHIM</h2>

    <div class="dashboard">
        <div class="stat-card" style="border-top: 4px solid #009688;"><h3>Ô Đang Hoạt Động</h3><p id="totalActiveBoxes" style="color: #009688;">0</p><button class="btn-detail" onclick="showDetail('activeBoxes')">Chi tiết</button></div>
        <div class="stat-card" style="border-top: 4px solid #673ab7;"><h3>Tổng Số Chim</h3><p id="totalBirds" style="color: #673ab7;">0</p><button class="btn-detail" onclick="showDetail('totalBirds')">Chi tiết</button></div>
        <div class="stat-card" style="border-top: 4px solid var(--primary);"><h3>Tổng Trứng Đã Đẻ</h3><p id="totalEggs">0</p><button class="btn-detail" onclick="showDetail('eggs')">Chi tiết</button></div>
        <div class="stat-card" style="border-top: 4px solid #f44336;"><h3>Tổng Chim Chết</h3><p id="totalDead" style="color: #f44336;">0</p><button class="btn-detail" onclick="showDetail('dead')">Chi tiết</button></div>
        <div class="stat-card" style="border-top: 4px solid #ffc107;"><h3>Tổng Số Tổ Ấp</h3><p id="totalIncubating" style="color: #ffc107;">0</p><button class="btn-detail" onclick="showDetail('incubating')">Chi tiết</button></div>
    </div>

    <div id="filterResultBox" class="filter-result-box">
        <button class="close-filter" onclick="closeDetail()">Đóng X</button>
        <h4 id="filterTitle">Chi tiết</h4>
        <div id="filterContent"></div>
    </div>

    <div class="chart-container"><canvas id="myChart" height="80"></canvas></div>

    <div class="form-section">
        <h3 class="section-title" id="formTitle">➕ Thêm Thông Tin Ô Mới</h3>
        <input type="hidden" id="editId" value="">
        
        <div class="grid-3">
            <div class="form-group"><label>Số Ô:</label><input type="number" id="boxNumber" placeholder="VD: 101"></div>
            <div class="form-group"><label>Tình trạng Bố Mẹ:</label>
                <select id="parentStatus">
                    <option value="Bình thường">Bình thường</option><option value="Bố bệnh">Bố bệnh</option><option value="Mẹ bệnh">Mẹ bệnh</option><option value="Cần cho uống thuốc">Cần cho uống thuốc</option><option value="Chết con trống">Chết con trống</option><option value="Chết con mái">Chết con mái</option><option value="Chết cả 2">Chết cả 2</option>
                </select>
            </div>
            <div class="form-group"><label>Đánh giá Nuôi Con:</label>
                <select id="parentingRating"><option value="Chưa đánh giá">Chưa đánh giá</option><option value="Đạt">Đạt</option><option value="Không đạt">Không đạt</option><option value="Loại">Loại</option></select>
            </div>
        </div>

        <div class="grid-3">
            <div class="form-group"><label>Trạng Thái Chim:</label>
                <select id="birdStatus" style="font-weight: bold; color: #d32f2f;">
                    <option value="Đang chờ đẻ">Đang chờ đẻ</option><option value="Đang ấp">Đang ấp</option><option value="Đang nuôi con">Đang nuôi con</option><option value="Vừa ấp vừa nuôi con">Vừa ấp vừa nuôi con</option>
                </select>
            </div>
            <div class="form-group"><label>Trạng thái Ghép Đôi:</label>
                <select id="pairingStatus"><option value="Chưa ghép">Chưa ghép</option><option value="Đã ghép">Đã ghép</option></select>
            </div>
            <div class="form-group"><label>Ngày Ghép Đôi:</label><input type="date" id="pairingDate"></div>
        </div>

        <div class="grid-3" style="background: #f9fbe7; padding: 10px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #e6ee9c;">
            <div class="form-group"><label>Ngày Đẻ Trứng:</label><input type="date" id="layDate" onchange="calculateDates()"></div>
            <div class="form-group"><label>Ngày Nở (Tự động +18 ngày):</label><div id="hatchResult" class="auto-calc-box">Chưa tính</div><input type="hidden" id="hatchDate"></div>
            <div class="form-group"><label>Ngày Ghép Con (Tự động +20 ngày):</label><div id="pairResult" class="auto-calc-box" style="background: #e3f2fd; border-color: #2196f3; color: #1565c0;">Chưa tính</div></div>
        </div>

        <div class="grid-3">
            <div class="form-group"><label>Trạng thái Tổ (Ngày tuổi):</label>
                <select id="nestStatus">
                    <option value="Chưa ấp">Chưa ấp</option><option value="1-5 ngày">1-5 ngày</option><option value="6-10 ngày">6-10 ngày</option><option value="11-20 ngày">11-20 ngày</option><option value="20-25 ngày">20-25 ngày</option><option value="25-35 ngày">25-35 ngày</option>
                </select>
            </div>
            <div class="form-group"><label>Số Tổ Ấp:</label><input type="number" id="nestCount" placeholder="Số tổ..."></div>
            <div class="form-group"><label>Tổng Số Trứng Đẻ:</label><input type="number" id="eggCount" placeholder="Số quả..."></div>
        </div>

        <div class="grid-3">
            <div class="form-group"><label>Trứng Trắng/Chết Phôi/Vỡ:</label><input type="text" id="eggIssues" placeholder="VD: Trắng ô 5..."></div>
            <div class="form-group"><label>Số Lượng Con Ghép/Tổ:</label><input type="number" id="pairedBirds" placeholder="Số con..."></div>
            <div class="form-group"><label>Ghi chú ghép:</label><input type="text" id="pairNotes" placeholder="Ghi chú..."></div>
        </div>

        <div class="grid-3">
            <div class="form-group"><label>Số Lượng Chim Con Chết:</label><input type="number" id="deadBirdCount" placeholder="Số con..."></div>
            <div class="form-group"><label>Ngày Chết & Tuổi:</label><input type="text" id="deadDetails" placeholder="VD: 15/10, 3 ngày tuổi"></div>
            <div class="form-group"><label>Lý Do Chết:</label>
                <select id="deadReason"><option value="Không có">Không có</option><option value="Bố mẹ dẫm">Bố mẹ dẫm</option><option value="Do bệnh">Do bệnh</option><option value="Khác">Lý do khác</option></select>
            </div>
        </div>

        <div class="grid-2">
            <div class="form-group"><label>Ngày Xuất Bán:</label><input type="date" id="soldDate"></div>
            <div class="form-group"><label>Tổng Dự Kiến Bán / Thực Tế Bán:</label><input type="number" id="soldCount" placeholder="Số con xuất bán..."></div>
        </div>

        <div class="form-group"><label>Ghi Chú Thêm:</label><textarea id="notes" rows="2" placeholder="Ghi chú chi tiết..."></textarea></div>

        <div class="btn-group">
            <button class="btn-save" onclick="saveData()" id="btnSave">💾 LƯU THÔNG TIN</button>
            <button class="btn-cancel" onclick="resetForm()" id="btnCancel">❌ HỦY SỬA</button>
        </div>
    </div>

    <div class="table-section">
        <h3 class="section-title">📋 Bảng Tổng Hợp Trại (Sắp xếp theo Số Ô)</h3>
        <table>
            <thead>
                <tr>
                    <th>Số Ô</th><th>Trạng Thái Bố Mẹ</th><th>Trạng Thái Chim</th><th>Ngày Đẻ / Nở / Ghép Con</th><th>Trạng Thái Tổ</th><th>Trứng</th><th>Chim Chết</th><th>Xuất Bán</th><th>Hành Động</th>
                </tr>
            </thead>
            <tbody id="tableBody"></tbody>
        </table>
    </div>
</div>

<script>
    let records = JSON.parse(localStorage.getItem('birdFarmData')) || [];
    let chartInstance = null;

    function formatDate(dateStr) {
        if(!dateStr) return "-";
        const d = new Date(dateStr);
        return `${d.getDate()}/${d.getMonth()+1}/${d.getFullYear()}`;
    }

    function calculateDates() {
        const layDateVal = document.getElementById('layDate').value;
        const hatchResult = document.getElementById('hatchResult');
        const pairResult = document.getElementById('pairResult');
        const hatchHidden = document.getElementById('hatchDate');

        if (layDateVal) {
            const layDate = new Date(layDateVal);
            const hatchDate = new Date(layDate); hatchDate.setDate(hatchDate.getDate() + 18);
            const pairDate = new Date(hatchDate); pairDate.setDate(pairDate.getDate() + 20);
            hatchResult.innerText = formatDate(hatchDate);
            pairResult.innerText = formatDate(pairDate);
            hatchHidden.value = hatchDate.toISOString().split('T')[0]; 
        } else {
            hatchResult.innerText = "Chưa tính"; pairResult.innerText = "Chưa tính"; hatchHidden.value = "";
        }
    }

    function saveData() {
        const boxNumber = document.getElementById('boxNumber').value;
        if (!boxNumber) { alert("Vui lòng nhập Số Ô!"); return; }

        const editId = document.getElementById('editId').value;
        const newRecord = {
            id: editId ? parseInt(editId) : Date.now(),
            boxNumber: parseInt(boxNumber),
            parentStatus: document.getElementById('parentStatus').value,
            parentingRating: document.getElementById('parentingRating').value,
            birdStatus: document.getElementById('birdStatus').value,
            pairingStatus: document.getElementById('pairingStatus').value,
            pairingDate: document.getElementById('pairingDate').value,
            nestCount: parseInt(document.getElementById('nestCount').value) || 0,
            nestStatus: document.getElementById('nestStatus').value,
            layDate: document.getElementById('layDate').value,
            hatchDate: document.getElementById('hatchDate').value,
            eggCount: parseInt(document.getElementById('eggCount').value) || 0,
            eggIssues: document.getElementById('eggIssues').value,
            pairedBirds: parseInt(document.getElementById('pairedBirds').value) || 0,
            pairNotes: document.getElementById('pairNotes').value,
            deadBirdCount: parseInt(document.getElementById('deadBirdCount').value) || 0,
            deadDetails: document.getElementById('deadDetails').value,
            deadReason: document.getElementById('deadReason').value,
            soldDate: document.getElementById('soldDate').value,
            soldCount: parseInt(document.getElementById('soldCount').value) || 0,
            notes: document.getElementById('notes').value
        };

        if (editId) {
            const index = records.findIndex(r => r.id === parseInt(editId));
            if (index !== -1) records[index] = newRecord;
            alert(`Đã cập nhật ô ${boxNumber}!`);
        } else {
            records.push(newRecord);
            alert(`Đã thêm mới ô ${boxNumber}!`);
        }

        localStorage.setItem('birdFarmData', JSON.stringify(records)); 
        resetForm(); renderAll(); closeDetail(); 
    }

    function editRecord(id) {
        const record = records.find(r => r.id === id); if (!record) return;
        document.getElementById('editId').value = record.id;
        document.getElementById('boxNumber').value = record.boxNumber;
        document.getElementById('parentStatus').value = record.parentStatus;
        document.getElementById('parentingRating').value = record.parentingRating;
        document.getElementById('birdStatus').value = record.birdStatus || 'Đang chờ đẻ';
        document.getElementById('pairingStatus').value = record.pairingStatus;
        document.getElementById('pairingDate').value = record.pairingDate;
        document.getElementById('nestCount').value = record.nestCount;
        document.getElementById('nestStatus').value = record.nestStatus;
        document.getElementById('layDate').value = record.layDate;
        calculateDates();
        document.getElementById('eggCount').value = record.eggCount;
        document.getElementById('eggIssues').value = record.eggIssues;
        document.getElementById('pairedBirds').value = record.pairedBirds;
        document.getElementById('pairNotes').value = record.pairNotes || '';
        document.getElementById('deadBirdCount').value = record.deadBirdCount;
        document.getElementById('deadDetails').value = record.deadDetails;
        document.getElementById('deadReason').value = record.deadReason;
        document.getElementById('soldDate').value = record.soldDate;
        document.getElementById('soldCount').value = record.soldCount;
        document.getElementById('notes').value = record.notes;
        document.getElementById('formTitle').innerText = "✏️ Chỉnh Sửa Ô " + record.boxNumber;
        document.getElementById('btnSave').innerText = "💾 CẬP NHẬT";
        document.getElementById('btnSave').style.background = "#2196f3";
        document.getElementById('btnCancel').style.display = "block";
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function deleteRecord(id) {
        if (confirm("Xóa thông tin ô này?")) {
            records = records.filter(r => r.id !== id);
            localStorage.setItem('birdFarmData', JSON.stringify(records));
            renderAll(); closeDetail();
        }
    }

    function resetForm() {
        document.querySelectorAll('input').forEach(input => input.value = '');
        document.querySelectorAll('select').forEach(select => select.selectedIndex = 0);
        document.querySelectorAll('textarea').forEach(ta => ta.value = '');
        document.getElementById('hatchResult').innerText = "Chưa tính";
        document.getElementById('pairResult').innerText = "Chưa tính";
        document.getElementById('hatchDate').value = "";
        document.getElementById('editId').value = "";
        document.getElementById('formTitle').innerText = "➕ Thêm Thông Tin Ô Mới";
        document.getElementById('btnSave').innerText = "💾 LƯU THÔNG TIN";
        document.getElementById('btnSave').style.background = "var(--primary)";
        document.getElementById('btnCancel').style.display = "none";
    }

    function renderTable() {
        const tbody = document.getElementById('tableBody'); tbody.innerHTML = '';
        if (records.length === 0) { tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;">Chưa có dữ liệu.</td></tr>'; return; }
        const sortedRecords = [...records].sort((a, b) => a.boxNumber - b.boxNumber);

        sortedRecords.forEach(r => {
            const tr = document.createElement('tr');
            let badgeClass = r.parentStatus.includes('bệnh') || r.parentStatus.includes('Chết') ? 'bg-red' : 'bg-green';
            let nestBadge = r.nestStatus.includes('25-35') ? 'bg-blue' : (r.nestStatus === 'Chưa ấp' ? 'bg-yellow' : 'bg-green');
            let birdStatusHtml = r.birdStatus ? `<span class="badge bg-blue">${r.birdStatus}</span>` : '-';
            let pairDateHtml = r.hatchDate ? (() => { const h = new Date(r.hatchDate); h.setDate(h.getDate() + 20); return `<br><span style="color:#2196f3; font-size:11px;">Ghép: ${formatDate(h)}</span>`; })() : "";

            tr.innerHTML = `
                <td><strong>${r.boxNumber}</strong></td>
                <td><span class="badge ${badgeClass}">${r.parentStatus}</span></td>
                <td>${birdStatusHtml}</td>
                <td style="font-size: 12px;">Đẻ: ${formatDate(r.layDate)}<br>Nở: <span style="color:green">${formatDate(r.hatchDate)}</span>${pairDateHtml}</td>
                <td><span class="badge ${nestBadge}">${r.nestStatus}</span><br><span style="font-size:11px;">Số tổ: ${r.nestCount || 0}</span></td>
                <td>Tổng: ${r.eggCount}<br><span style="color:red; font-size:11px;">${r.eggIssues || ''}</span></td>
                <td style="color: ${r.deadBirdCount > 0 ? 'red' : 'inherit'}">${r.deadBirdCount} con<br><span style="font-size:11px;">${r.deadDetails} - ${r.deadReason}</span></td>
                <td>Dự kiến: ${r.pairedBirds}<br>Thực tế: <strong>${r.soldCount}</strong><br><span style="font-size:11px;">${formatDate(r.soldDate)}</span></td>
                <td><div class="action-btns"><button class="btn-edit" onclick="editRecord(${r.id})">Sửa</button><button class="btn-delete" onclick="deleteRecord(${r.id})">Xóa</button></div></td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderStatsAndChart() {
        let totalActiveBoxes = 0, totalBirds = 0, totalEggs = 0, totalDead = 0, totalIncubating = 0;
        let chartData = {}; 

        records.forEach(r => {
            if (r.parentStatus !== 'Chết cả 2') totalActiveBoxes++;
            if(!r.parentStatus.includes('Chết')) totalBirds += 2; 
            totalBirds += (r.pairedBirds || 0); 
            totalEggs += (r.eggCount || 0);
            totalDead += (r.deadBirdCount || 0);
            
            if (r.birdStatus === 'Đang ấp' || r.birdStatus === 'Vừa ấp vừa nuôi con' || r.nestStatus.includes('ngày')) {
                totalIncubating += (r.nestCount || 1);
            }

            if (r.layDate) {
                const date = new Date(r.layDate);
                const monthYear = `${date.getMonth()+1}/${date.getFullYear()}`;
                if (!chartData[monthYear]) chartData[monthYear] = { eggs: 0, dead: 0 };
                chartData[monthYear].eggs += r.eggCount;
                chartData[monthYear].dead += r.deadBirdCount;
            }
        });

        document.getElementById('totalActiveBoxes').innerText = totalActiveBoxes;
        document.getElementById('totalBirds').innerText = totalBirds;
        document.getElementById('totalEggs').innerText = totalEggs;
        document.getElementById('totalDead').innerText = totalDead;
        document.getElementById('totalIncubating').innerText = totalIncubating;

        const ctx = document.getElementById('myChart').getContext('2d');
        const labels = Object.keys(chartData).sort(); 
        const dataEggs = labels.map(label => chartData[label].eggs);
        const dataDead = labels.map(label => chartData[label].dead);

        if (chartInstance) chartInstance.destroy();
        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels.length ? labels : ['Chưa có dữ liệu'],
                datasets: [
                    { label: 'Số trứng đẻ', data: dataEggs.length ? dataEggs : [0], backgroundColor: '#4caf50' },
                    { label: 'Số chim chết', data: dataDead.length ? dataDead : [0], backgroundColor: '#f44336' }
                ]
            },
            options: { responsive: true, plugins: { title: { display: true, text: 'Biểu đồ sinh sản theo Tháng' } }, scales: { y: { beginAtZero: true } } }
        });
    }

    function showDetail(type) {
        const box = document.getElementById('filterResultBox');
        const title = document.getElementById('filterTitle');
        const content = document.getElementById('filterContent');
        let listHtml = "";
        const sortedRecords = [...records].sort((a, b) => a.boxNumber - b.boxNumber);

        if (type === 'eggs') {
            title.innerText = "🐣 Chi tiết các ô có trứng đẻ:";
            sortedRecords.forEach(r => { if (r.eggCount > 0) listHtml += `<li><strong>Ô ${r.boxNumber}:</strong> ${r.eggCount} trứng (Ngày đẻ: ${formatDate(r.layDate)})</li>`; });
        } else if (type === 'dead') {
            title.innerText = "💀 Chi tiết các ô có chim chết:";
            sortedRecords.forEach(r => { if (r.deadBirdCount > 0) listHtml += `<li><strong>Ô ${r.boxNumber}:</strong> ${r.deadBirdCount} con (Lý do: ${r.deadReason})</li>`; });
        } else if (type === 'incubating') {
            title.innerText = "🪺 Chi tiết các ô đang ấp/nuôi con:";
            sortedRecords.forEach(r => { if (r.birdStatus === 'Đang ấp' || r.birdStatus === 'Đang nuôi con' || r.birdStatus === 'Vừa ấp vừa nuôi con' || r.nestStatus.includes('ngày')) listHtml += `<li><strong>Ô ${r.boxNumber}:</strong> ${r.nestCount || 1} tổ (Trạng thái: ${r.birdStatus || 'Chưa rõ'})</li>`; });
        } else if (type === 'activeBoxes') {
            title.innerText = "🟢 Chi tiết các ô đang hoạt động:";
            sortedRecords.forEach(r => { if (r.parentStatus !== 'Chết cả 2') listHtml += `<li><strong>Ô ${r.boxNumber}:</strong> Bố mẹ ${r.parentStatus}</li>`; });
        } else if (type === 'totalBirds') {
            title.innerText = "🐦 Ước tính chi tiết số lượng chim:";
            sortedRecords.forEach(r => { if (!r.parentStatus.includes('Chết')) listHtml += `<li><strong>Ô ${r.boxNumber}:</strong> 2 bố mẹ + ${r.pairedBirds || 0} con non</li>`; });
        }
        if (listHtml === "") listHtml = "<li>Không có dữ liệu.</li>";
        content.innerHTML = `<ul>${listHtml}</ul>`;
        box.style.display = "block";
        box.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function closeDetail() { document.getElementById('filterResultBox').style.display = "none"; }

    function renderAll() { renderTable(); renderStatsAndChart(); }
    renderAll();
</script>
</body>
</html>
