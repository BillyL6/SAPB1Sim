// =========================================================================
// SAP Business One (SAP B1) Web App UI Simulator Client Engine
// =========================================================================

const PRESET_QUERIES = [
  {
    title: "1. Multi-Warehouse Stock Levels",
    sql: `SELECT 
    T0.ItemCode,
    T1.ItemName,
    T0.WhsCode,
    T2.WhsName,
    T0.OnHand AS Stock,
    T0.IsCommited AS Committed,
    T0.OnOrder AS On_PO,
    (T0.OnHand - T0.IsCommited + T0.OnOrder) AS AvailableStock
FROM OITW T0
INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
INNER JOIN OWHS T2 ON T0.WhsCode = T2.WhsCode
ORDER BY T0.ItemCode, T0.WhsCode
LIMIT 15;`
  },
  {
    title: "2. Order-to-Cash (O2C) Settlements",
    sql: `SELECT 
    T0.DocNum AS Payment_Num,
    T0.DocDate AS Payment_Date,
    T0.CardCode,
    T0.CardName AS Customer_Name,
    T1.InvoiceId AS Paid_Invoice_Entry,
    T2.DocNum AS Invoice_DocNum,
    T1.SumApplied AS Settled_Amount,
    T0.DocTotal AS Total_Payment,
    T0.PrjCode AS Project_Code
FROM ORCT T0
INNER JOIN RCT2 T1 ON T0.DocEntry = T1.DocEntry
LEFT JOIN OINV T2 ON T1.InvoiceId = T2.DocEntry
ORDER BY T0.DocNum
LIMIT 15;`
  },
  {
    title: "3. Procure-to-Pay (P2P) Disbursements",
    sql: `SELECT 
    T0.DocNum AS Payment_Num,
    T0.DocDate AS Payment_Date,
    T0.CardCode,
    T0.CardName AS Vendor_Name,
    T1.InvoiceId AS AP_Invoice_Entry,
    T2.DocNum AS AP_Invoice_DocNum,
    T1.SumApplied AS Amount_Disbursed,
    T0.DocTotal AS Total_Payment
FROM OVPM T0
INNER JOIN VPM2 T1 ON T0.DocEntry = T1.DocEntry
LEFT JOIN OPCH T2 ON T1.InvoiceId = T2.DocEntry
ORDER BY T0.DocNum
LIMIT 15;`
  },
  {
    title: "4. Bill of Materials (BOM) Explosion",
    sql: `SELECT 
    T0.Code AS Parent_ItemCode,
    T1.ItemName AS Parent_Name,
    T2.Code AS Child_Component,
    T3.ItemName AS Component_Name,
    T2.Quantity AS Qty_Required,
    T2.Price AS Unit_Cost,
    (T2.Quantity * T2.Price) AS Total_Cost
FROM OITT T0
INNER JOIN OITM T1 ON T0.Code = T1.ItemCode
INNER JOIN ITT1 T2 ON T0.Code = T2.Father
INNER JOIN OITM T3 ON T2.Code = T3.ItemCode
ORDER BY T0.Code, T2.ChildNum
LIMIT 15;`
  },
  {
    title: "5. Production Orders & WIP Status",
    sql: `SELECT 
    T0.DocNum AS Work_Order,
    T0.PostDate,
    T0.ItemCode AS Assembly_Code,
    T1.ItemName AS Assembly_Name,
    T0.PlannedQty,
    T0.CmpltQty,
    T2.ItemCode AS Raw_Material,
    T2.PlannedQty AS Mat_Planned,
    T2.IssuedQty AS Mat_Issued
FROM OWOR T0
INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
INNER JOIN WOR1 T2 ON T0.DocEntry = T2.DocEntry
ORDER BY T0.DocNum
LIMIT 15;`
  },
  {
    title: "6. Multi-Tier Price List Matrix",
    sql: `SELECT 
    T0.ItemCode,
    T2.ItemName,
    T1.ListName AS Price_List,
    T0.Price,
    T0.Currency,
    T1.Factor AS Markup_Factor
FROM ITM1 T0
INNER JOIN OPLN T1 ON T0.PriceList = T1.ListNum
INNER JOIN OITM T2 ON T0.ItemCode = T2.ItemCode
ORDER BY T0.ItemCode, T0.PriceList
LIMIT 20;`
  },
  {
    title: "7. Batch Traceability & Expiration",
    sql: `SELECT 
    T0.DistNumber AS Batch_Number,
    T0.ItemCode,
    T1.ItemName,
    T0.WhsCode,
    T0.Quantity AS Stock_In_Batch,
    T0.InDate,
    T0.ExpDate
FROM OBTN T0
INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
ORDER BY T0.ExpDate ASC
LIMIT 15;`
  },
  {
    title: "8. Balanced Journal Entries Audit",
    sql: `SELECT 
    T0.TransId AS JE_Num,
    T0.RefDate AS Posting_Date,
    T0.Memo,
    T1.Account AS GL_Account,
    T2.AcctName AS Account_Name,
    T1.Debit,
    T1.Credit
FROM OJDT T0
INNER JOIN JDT1 T1 ON T0.TransId = T1.TransId
INNER JOIN OACT T2 ON T1.Account = T2.AcctCode
ORDER BY T0.TransId, T1.Line_ID
LIMIT 15;`
  },
  {
    title: "9. Landed Cost Import Allocations & GRPO",
    sql: `SELECT 
    T0.DocNum AS LC_Doc,
    T0.DocDate,
    T2.DocNum AS GRPO_Doc,
    T1.ItemCode,
    T1.WhsCode AS Whs,
    T1.OrigCost AS Base_Cost,
    T1.AllocSum AS Landed_Fee,
    ROUND(T1.OrigCost + (T1.AllocSum / T1.Quantity), 2) AS Unit_Landed_Cost,
    T4.AvgPrice AS Whs_AvgPrice,
    T5.AvgPrice AS ItemMaster_AvgPrice
FROM OIPF T0
INNER JOIN IPF1 T1 ON T0.DocEntry = T1.DocEntry
INNER JOIN OPDN T2 ON T1.BaseEntry = T2.DocEntry
INNER JOIN OITW T4 ON T1.ItemCode = T4.ItemCode AND T1.WhsCode = T4.WhsCode
INNER JOIN OITM T5 ON T1.ItemCode = T5.ItemCode
WHERE T1.ItemCode LIKE 'ITM-IMP-%'
ORDER BY T1.ItemCode, T1.WhsCode
LIMIT 15;`
  },
  {
    title: "9B. USD Factory PO to AUD GRPO Conversion (Spot Rate 0.65)",
    sql: `SELECT 
    T0.DocNum AS PO_Num,
    T0.DocCur AS PO_Cur,
    T1.ItemCode,
    T1.PriceFC AS FOB_USD,
    T1.TotalFrgn AS Total_USD,
    T2.DocRate AS GRPO_Rate,
    T2.DocNum AS GRPO_Num,
    T3.Price AS Converted_FOB_AUD,
    T3.LineTotal AS Total_AUD,
    T3.WhsCode AS Whs
FROM OPOR T0
INNER JOIN POR1 T1 ON T0.DocEntry = T1.DocEntry
INNER JOIN OPDN T2 ON T0.DocEntry = T2.BaseEntry
INNER JOIN PDN1 T3 ON T2.DocEntry = T3.DocEntry
WHERE T0.DocNum >= 5900
ORDER BY T0.DocNum;`
  },
  {
    title: "9C. Intercompany Transfer & Stacked Landed Cost Journey in AUD",
    sql: `SELECT 
    T0.ItemCode,
    T1.ItemName,
    T0.WhsCode,
    T2.WhsName,
    T0.AvgPrice AS Stacked_Cost_AUD,
    T0.OnHand AS Stock_Qty,
    T1.AvgPrice AS Enterprise_AvgPrice_AUD
FROM OITW T0
INNER JOIN OITM T1 ON T0.ItemCode = T1.ItemCode
INNER JOIN OWHS T2 ON T0.WhsCode = T2.WhsCode
WHERE T0.ItemCode LIKE 'ITM-IC-%'
ORDER BY T0.ItemCode, 
    CASE T0.WhsCode 
        WHEN 'ICCChina' THEN 1 
        WHEN 'ICCSIT' THEN 2 
        WHEN 'NZNTH' THEN 3 
        WHEN 'NZSTH' THEN 4 
        WHEN 'NZSIT' THEN 5 
        WHEN 'EuropeMarketPlace' THEN 6 
        WHEN 'EuropeSIT' THEN 7 
        WHEN 'AU-SYD' THEN 10 
        WHEN 'AU-MEL' THEN 11 
        WHEN 'AU-BNE' THEN 12 
        WHEN 'VGLPER' THEN 13 
        ELSE 99 
    END
LIMIT 20;`
  },
  {
    title: "10. CRM Sales Pipeline & Win Rates",
    sql: `SELECT 
    T0.OpprId,
    T0.Name AS Opportunity_Name,
    T0.CardCode,
    T1.CardName AS Customer_Name,
    T0.MaxSumLoc AS Potential_Value,
    T0.ClosePrcnt AS Win_Probability,
    T0.Status,
    T0.OpenDate
FROM OOPR T0
INNER JOIN OCRD T1 ON T0.CardCode = T1.CardCode
ORDER BY T0.MaxSumLoc DESC
LIMIT 15;`
  },
  {
    title: "11. Project Management Milestones",
    sql: `SELECT 
    T0.PrjCode,
    T0.PrjName,
    T2.CardName AS Client,
    T0.PlanCost AS Budget,
    T0.ActualCost AS Spend_To_Date,
    T1.Stage,
    T1.Task,
    T1.Cost AS Stage_Cost
FROM OPMG T0
INNER JOIN PMG1 T1 ON T0.AbsEntry = T1.AbsEntry
INNER JOIN OCRD T2 ON T0.CardCode = T2.CardCode
ORDER BY T0.PrjCode, T1.Stage
LIMIT 15;`
  },
  {
    title: "12. Inventory Warehouse Valuation Log",
    sql: `SELECT 
    T0.TransSeq,
    T0.DocDate,
    T0.ItemCode,
    CASE T0.TransType 
        WHEN 20 THEN 'GRPO Inward'
        WHEN 15 THEN 'Delivery Out'
        WHEN 67 THEN 'Whs Transfer'
        WHEN 59 THEN 'Receipt from Prod'
        WHEN 60 THEN 'Issue to Prod'
        ELSE 'Other'
    END AS Movement,
    T0.InQty,
    T0.OutQty,
    T0.Price AS Unit_Cost,
    T0.TransValue,
    T0.Warehouse
FROM OINM T0
ORDER BY T0.TransSeq
LIMIT 15;`
  }
];

let allTablesCache = [];

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  initCockpit();
  initDocumentExplorer();
  initRelationshipMap();
  initBPView();
  initInventoryView();
  initProductionView();
  initFinancialsView();
  initCRMView();
  initSQLStudio();
  initAllTablesView();
  initModal();
});

// -----------------------------------------------------------------
// Navigation View Switcher
// -----------------------------------------------------------------
function initNavigation() {
  const menuToggle = document.getElementById("menuToggle");
  const appSidebar = document.getElementById("appSidebar");
  menuToggle.addEventListener("click", () => {
    appSidebar.classList.toggle("collapsed");
  });

  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      navItems.forEach(i => i.classList.remove("active"));
      item.classList.add("active");
      const view = item.getAttribute("data-view");
      switchView(view);
    });
  });

  // Global search
  const globalSearch = document.getElementById("globalSearch");
  globalSearch.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && globalSearch.value.trim()) {
      const q = globalSearch.value.trim();
      if (q.startsWith("C") || q.startsWith("V")) {
        openBPInspector(q);
      } else if (q.startsWith("ITM-")) {
        openItemInspector(q);
      } else {
        // Run search in SQL studio
        document.getElementById("sqlQueryText").value = `SELECT * FROM OCRD WHERE CardCode LIKE '%${q}%' OR CardName LIKE '%${q}%' UNION ALL SELECT * FROM OITM WHERE ItemCode LIKE '%${q}%' OR ItemName LIKE '%${q}%' LIMIT 20;`;
        switchView("sqlstudio");
        executeCurrentSQL();
      }
    }
  });
}

function switchView(viewName) {
  document.querySelectorAll(".view-panel").forEach(p => p.classList.remove("active"));
  const target = document.getElementById(`view-${viewName}`);
  if (target) {
    target.classList.add("active");
    // Update active nav button
    document.querySelectorAll(".nav-item").forEach(item => {
      if (item.getAttribute("data-view") === viewName) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });

    // Auto-trigger load for specific views
    if (viewName === "bp") loadBPList();
    if (viewName === "inventory") loadStockMatrix();
    if (viewName === "production") loadBOMTrees();
    if (viewName === "financials") loadCOA();
    if (viewName === "crm") loadCRMOpportunities();
    if (viewName === "alltables") loadAllTablesList();
    if (viewName === "documents") loadDocumentsList();
  }
}

// -----------------------------------------------------------------
// 1. Executive Cockpit Logic
// -----------------------------------------------------------------
async function initCockpit() {
  document.getElementById("btnRefreshCockpit").addEventListener("click", fetchCockpitData);
  fetchCockpitData();
}

async function fetchCockpitData() {
  try {
    const res = await fetch("/api/kpis");
    const data = await res.json();

    const k = data.kpis;
    document.getElementById("kpiRevenue").textContent = `$${k.total_revenue.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById("kpiStockVal").textContent = `$${k.stock_valuation.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById("kpiReceivables").textContent = `$${k.ar_receivables.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById("kpiPayables").textContent = `$${k.ap_payables.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById("kpiOpenSO").textContent = `${k.open_so_count} Orders`;
    document.getElementById("kpiOpenSOTotal").textContent = `$${k.open_so_total.toLocaleString('en-US', {minimumFractionDigits: 2})} in Backlog`;
    document.getElementById("kpiWinRate").textContent = `${k.opp_win_rate}%`;
    document.getElementById("kpiOppTotal").textContent = `$${k.opp_total.toLocaleString('en-US', {minimumFractionDigits: 2})} Pipeline`;

    // Recent Sales Orders
    const soTbody = document.getElementById("cockpitRecentSOBody");
    soTbody.innerHTML = data.recent_orders.map(o => `
      <tr>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openDocForm('ORDR', ${o.DocEntry})" title="Drill Down to Sales Order">➡️</span>
            <strong>#${o.DocNum}</strong>
          </span>
        </td>
        <td>${o.DocDate}</td>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openBPInspector('${o.CardCode}')" title="Drill Down to Business Partner">➡️</span>
            ${o.CardName}
          </span>
        </td>
        <td><strong>$${o.DocTotal.toFixed(2)}</strong></td>
        <td><span class="sap-badge-status ${o.DocStatus === 'O' ? 'status-open' : 'status-closed'}">${o.DocStatus === 'O' ? 'Open' : 'Closed'}</span></td>
        <td>
          <button class="sap-btn sap-btn-sm" onclick="openRelationshipMap('ORDR', ${o.DocEntry})">Flow 🕸️</button>
        </td>
      </tr>
    `).join("");

    // Stock Alerts
    const alertsTbody = document.getElementById("cockpitStockAlertsBody");
    alertsTbody.innerHTML = data.stock_alerts.map(a => `
      <tr>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openItemInspector('${a.ItemCode}')" title="Drill Down to Item">➡️</span>
            ${a.ItemName}
          </span>
        </td>
        <td><strong>Whs ${a.WhsCode}</strong></td>
        <td style="color:var(--danger); font-weight:700;">${a.OnHand}</td>
        <td>${a.MinStock}</td>
      </tr>
    `).join("");

  } catch (err) {
    console.error("Cockpit load error:", err);
  }
}

// -----------------------------------------------------------------
// 2. Document Explorer Logic
// -----------------------------------------------------------------
function initDocumentExplorer() {
  document.getElementById("btnLoadDocList").addEventListener("click", loadDocumentsList);
  document.getElementById("docTypeSelect").addEventListener("change", loadDocumentsList);
  document.getElementById("docSearchInput").addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase();
    document.querySelectorAll("#docListTbody tr").forEach(tr => {
      tr.style.display = tr.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });
}

async function loadDocumentsList() {
  const docType = document.getElementById("docTypeSelect").value;
  document.getElementById("docListCardTitle").textContent = `${docType} - Document Header Records`;
  const tbody = document.getElementById("docListTbody");
  const thead = document.getElementById("docListThead");
  tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;">Loading ${docType}...</td></tr>`;

  try {
    const res = await fetch(`/api/table/${docType}?limit=50`);
    const data = await res.json();
    if (!data.rows || !data.rows.length) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;">No documents found.</td></tr>`;
      return;
    }

    const cols = data.columns;
    thead.innerHTML = `<tr>
      <th>Action</th>
      ${cols.map(c => `<th>${c}</th>`).join("")}
    </tr>`;

    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td>
          <button class="sap-btn sap-btn-sm sap-btn-primary" onclick="openDocForm('${docType}', ${r.DocEntry || r.DocNum || r.TransId || r.AbsEntry})">View Form 📑</button>
        </td>
        ${cols.map(c => {
          const val = r[c];
          if (c === "CardCode" && val) {
            return `<td><span class="cell-with-arrow"><span class="golden-arrow-btn" onclick="openBPInspector('${val}')">➡️</span>${val}</span></td>`;
          }
          if (c === "ItemCode" && val) {
            return `<td><span class="cell-with-arrow"><span class="golden-arrow-btn" onclick="openItemInspector('${val}')">➡️</span>${val}</span></td>`;
          }
          if (c === "DocStatus") {
            return `<td><span class="sap-badge-status ${val === 'O' ? 'status-open' : 'status-closed'}">${val === 'O' ? 'Open' : 'Closed'}</span></td>`;
          }
          return `<td>${val !== null ? val : ''}</td>`;
        }).join("")}
      </tr>
    `).join("");

  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" style="color:var(--danger); text-align:center;">Error loading documents: ${err.message}</td></tr>`;
  }
}

async function openDocForm(docType, docId) {
  try {
    const res = await fetch(`/api/document/${docType}/${docId}`);
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }

    const h = data.header;
    const lines = data.lines || [];

    const content = `
      <div class="doc-form-card">
        <div class="doc-form-header">
          <div class="form-group">
            <label>Document # / Status</label>
            <div class="form-val">${data.doc_name} #${h.DocNum || h.DocEntry || h.TransId} <span class="sap-badge-status ${h.DocStatus === 'O' ? 'status-open' : 'status-closed'}">${h.DocStatus === 'O' ? 'Open' : 'Closed'}</span></div>
          </div>
          <div class="form-group">
            <label>Business Partner</label>
            <div class="form-val">
              ${h.CardCode ? `<span class="cell-with-arrow"><span class="golden-arrow-btn" onclick="openBPInspector('${h.CardCode}')">➡️</span><strong>${h.CardName || h.CardCode}</strong></span>` : 'N/A'}
            </div>
          </div>
          <div class="form-group">
            <label>Document Date</label>
            <div class="form-val">${h.DocDate || h.RefDate || h.PostDate || 'N/A'}</div>
          </div>
          <div class="form-group">
            <label>Due Date / Ref</label>
            <div class="form-val">${h.DocDueDate || h.DueDate || h.TaxDate || 'N/A'}</div>
          </div>
        </div>

        <div class="doc-lines-grid">
          <h4 style="margin-bottom:10px; font-size:13px; text-transform:uppercase; color:var(--text-muted);">Line Items & Inventory</h4>
          <div class="sap-table-wrap">
            <table class="sap-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Item Code</th>
                  <th>Description</th>
                  <th>Quantity</th>
                  <th>Unit Price</th>
                  <th>Line Total</th>
                  <th>Warehouse</th>
                </tr>
              </thead>
              <tbody>
                ${lines.map((l, idx) => `
                  <tr>
                    <td>${idx + 1}</td>
                    <td>
                      ${l.ItemCode ? `<span class="cell-with-arrow"><span class="golden-arrow-btn" onclick="openItemInspector('${l.ItemCode}')">➡️</span>${l.ItemCode}</span>` : (l.Account || '')}
                    </td>
                    <td>${l.Dscription || l.ItemName || l.LineMemo || l.ItemDesc || ''}</td>
                    <td><strong>${l.Quantity || l.Debit || l.SumApplied || 1}</strong></td>
                    <td>$${(l.Price || l.Credit || 0).toFixed(2)}</td>
                    <td><strong>$${(l.LineTotal || l.AllocSum || l.SumApplied || 0).toFixed(2)}</strong></td>
                    <td>${l.WhsCode || l.WareHouse || '01'}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>

        <div class="doc-form-footer">
          <div class="form-group" style="flex:1; max-width:400px;">
            <label>Remarks / Comments</label>
            <div class="form-val" style="font-size:13px; font-weight:normal; color:var(--text-muted);">${h.Comments || h.Memo || 'None'}</div>
          </div>
          <div class="totals-box">
            <div class="totals-row">
              <span>Lines Subtotal:</span>
              <span>$${(h.DocTotal || h.LocTotal || 0).toFixed(2)}</span>
            </div>
            <div class="totals-row">
              <span>Tax (GST 10% Incl.):</span>
              <span>$${((h.DocTotal || 0) * 0.1).toFixed(2)}</span>
            </div>
            <div class="totals-row grand-total">
              <span>Document Total:</span>
              <span>$${(h.DocTotal || h.LocTotal || 0).toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
      <div style="display:flex; justify-content:flex-end; margin-top:10px;">
        <button class="sap-btn sap-btn-primary" onclick="openRelationshipMap('${docType}', ${docId})">View Document Relationship Map 🕸️</button>
      </div>
    `;

    showModal(`${data.doc_name} Details (#${docId})`, content);

  } catch (err) {
    alert("Error fetching document details: " + err.message);
  }
}

// -----------------------------------------------------------------
// 3. Interactive Relationship Map
// -----------------------------------------------------------------
function initRelationshipMap() {
  document.getElementById("btnGenerateRelMap").addEventListener("click", () => {
    const type = document.getElementById("relMapTypeSelect").value;
    const entry = document.getElementById("relMapDocEntry").value || 1;
    generateRelationshipMap(type, entry);
  });
}

async function openRelationshipMap(docType, docId) {
  switchView("relmap");
  document.getElementById("relMapTypeSelect").value = docType;
  document.getElementById("relMapDocEntry").value = docId;
  generateRelationshipMap(docType, docId);
}

async function generateRelationshipMap(docType, docId) {
  const container = document.getElementById("relMapContainer");
  container.innerHTML = "Generating relationship tree...";

  try {
    const res = await fetch(`/api/relationship-map/${docType}/${docId}`);
    const data = await res.json();
    if (data.error) {
      container.innerHTML = `<span style="color:var(--danger);">${data.error}</span>`;
      return;
    }

    document.getElementById("relMapCardTitle").textContent = `Document Relationship Map: ${data.card_name || ''}`;

    let html = "";
    data.nodes.forEach((n, idx) => {
      html += `
        <div class="rel-node ${n.current ? 'active-node' : ''}" onclick="openDocForm('${n.type}', ${docId})">
          <span class="rel-node-title">${n.type}</span>
          <span class="rel-node-val">${n.name}</span>
          <span class="rel-node-status">$${n.amount.toFixed(2)} • ${n.status}</span>
        </div>
      `;
      if (idx < data.nodes.length - 1) {
        html += `<span class="rel-arrow">➔</span>`;
      }
    });

    container.innerHTML = html;

  } catch (err) {
    container.innerHTML = `<span style="color:var(--danger);">Error: ${err.message}</span>`;
  }
}

// -----------------------------------------------------------------
// 4. Business Partner 360 View
// -----------------------------------------------------------------
function initBPView() {
  document.getElementById("btnRefreshBP").addEventListener("click", loadBPList);
  document.getElementById("bpTypeFilter").addEventListener("change", loadBPList);
}

async function loadBPList() {
  const typeFilter = document.getElementById("bpTypeFilter").value;
  const tbody = document.getElementById("bpTableBody");
  tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;">Loading Business Partners...</td></tr>`;

  try {
    const res = await fetch("/api/table/OCRD?limit=100");
    const data = await res.json();

    let rows = data.rows || [];
    if (typeFilter !== "ALL") {
      rows = rows.filter(r => r.CardType === typeFilter);
    }

    tbody.innerHTML = rows.map(r => `
      <tr>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openBPInspector('${r.CardCode}')">➡️</span>
            <strong>${r.CardCode}</strong>
          </span>
        </td>
        <td>${r.CardName}</td>
        <td><span class="sap-badge-status ${r.CardType === 'C' ? 'status-open' : 'status-closed'}">${r.CardType === 'C' ? 'Customer' : 'Supplier'}</span></td>
        <td>${r.GroupCode}</td>
        <td>${r.Phone || 'N/A'}</td>
        <td style="font-weight:700; color:${r.Balance >= 0 ? 'var(--primary)' : 'var(--danger)'};">$${r.Balance.toFixed(2)}</td>
        <td>${r.DebPayAcct || 'N/A'}</td>
        <td>
          <button class="sap-btn sap-btn-sm" onclick="openBPInspector('${r.CardCode}')">360° View 👥</button>
        </td>
      </tr>
    `).join("");

  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

async function openBPInspector(cardCode) {
  try {
    const res = await fetch(`/api/bp/${cardCode}`);
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }

    const bp = data.bp;
    const content = `
      <div class="doc-form-card">
        <div class="doc-form-header">
          <div class="form-group">
            <label>Card Code & Name</label>
            <div class="form-val">${bp.CardCode} - ${bp.CardName}</div>
          </div>
          <div class="form-group">
            <label>Partner Type</label>
            <div class="form-val"><span class="sap-badge-status ${bp.CardType === 'C' ? 'status-open' : 'status-closed'}">${bp.CardType === 'C' ? 'Customer (Client)' : 'Vendor (Supplier)'}</span></div>
          </div>
          <div class="form-group">
            <label>Current Balance</label>
            <div class="form-val" style="color:var(--primary); font-size:16px;">$${bp.Balance.toFixed(2)} ${bp.Currency}</div>
          </div>
          <div class="form-group">
            <label>Phone / Contact</label>
            <div class="form-val">${bp.Phone || 'N/A'}</div>
          </div>
        </div>

        <div style="padding:16px;">
          <h4 style="margin-bottom:8px; font-size:13px; text-transform:uppercase; color:var(--text-muted);">Addresses (CRD1)</h4>
          <div class="sap-table-wrap">
            <table class="sap-table">
              <thead><tr><th>Type</th><th>Name</th><th>Street</th><th>City</th><th>State</th></tr></thead>
              <tbody>
                ${data.addresses.map(a => `
                  <tr>
                    <td><span class="sap-badge-status ${a.AdresType === 'B' ? 'status-open' : 'status-won'}">${a.AdresType === 'B' ? 'Bill-To' : 'Ship-To'}</span></td>
                    <td>${a.Address}</td>
                    <td>${a.Street}</td>
                    <td>${a.City}</td>
                    <td>${a.State}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>

          <h4 style="margin-top:16px; margin-bottom:8px; font-size:13px; text-transform:uppercase; color:var(--text-muted);">Contact Persons (OCPR)</h4>
          <div class="sap-table-wrap">
            <table class="sap-table">
              <thead><tr><th>Contact Name</th><th>Position</th><th>Email</th><th>Phone</th></tr></thead>
              <tbody>
                ${data.contacts.map(c => `
                  <tr>
                    <td><strong>${c.Name}</strong></td>
                    <td>${c.Position}</td>
                    <td>${c.E_MailL}</td>
                    <td>${c.Tel1}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>

          <h4 style="margin-top:16px; margin-bottom:8px; font-size:13px; text-transform:uppercase; color:var(--text-muted);">Recent Orders</h4>
          <div class="sap-table-wrap">
            <table class="sap-table">
              <thead><tr><th>Doc #</th><th>Date</th><th>Total</th><th>Status</th><th>Action</th></tr></thead>
              <tbody>
                ${data.orders.map(o => `
                  <tr>
                    <td>#${o.DocNum}</td>
                    <td>${o.DocDate}</td>
                    <td>$${o.DocTotal.toFixed(2)}</td>
                    <td><span class="sap-badge-status ${o.DocStatus === 'O' ? 'status-open' : 'status-closed'}">${o.DocStatus === 'O' ? 'Open' : 'Closed'}</span></td>
                    <td><button class="sap-btn sap-btn-sm" onclick="openDocForm('${bp.CardType === 'C' ? 'ORDR' : 'OPOR'}', ${o.DocEntry})">View 📑</button></td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;

    showModal(`Business Partner 360°: ${bp.CardName}`, content);

  } catch (err) {
    alert("Error loading BP 360: " + err.message);
  }
}

// -----------------------------------------------------------------
// 5. Item 360 & Inventory
// -----------------------------------------------------------------
function initInventoryView() {
  document.getElementById("btnShowStockMatrix").addEventListener("click", () => {
    setInvBtnActive("btnShowStockMatrix");
    loadStockMatrix();
  });
  document.getElementById("btnShowBatches").addEventListener("click", () => {
    setInvBtnActive("btnShowBatches");
    loadBatches();
  });
  document.getElementById("btnShowBins").addEventListener("click", () => {
    setInvBtnActive("btnShowBins");
    loadBins();
  });
}

function setInvBtnActive(btnId) {
  ["btnShowStockMatrix", "btnShowBatches", "btnShowBins"].forEach(id => {
    document.getElementById(id).classList.toggle("active", id === btnId);
  });
}

async function loadStockMatrix() {
  document.getElementById("inventoryCardTitle").textContent = "Item Warehouse Stock Matrix (OITW + OITM)";
  const thead = document.getElementById("inventoryThead");
  const tbody = document.getElementById("inventoryTbody");

  thead.innerHTML = `<tr><th>Item Code</th><th>Item Name</th><th>Warehouse</th><th>On Hand</th><th>Committed</th><th>On Order</th><th>Available</th><th>Avg Price</th></tr>`;
  tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;">Loading warehouse matrix...</td></tr>`;

  try {
    const res = await fetch("/api/table/OITW?limit=50");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openItemInspector('${r.ItemCode}')">➡️</span>
            <strong>${r.ItemCode}</strong>
          </span>
        </td>
        <td>${r.ItemCode} Master Data</td>
        <td><strong>Whs ${r.WhsCode}</strong></td>
        <td>${r.OnHand}</td>
        <td>${r.IsCommited}</td>
        <td>${r.OnOrder}</td>
        <td style="font-weight:700; color:var(--success);">${(r.OnHand - r.IsCommited + r.OnOrder).toFixed(1)}</td>
        <td>$${r.AvgPrice.toFixed(2)}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

async function loadBatches() {
  document.getElementById("inventoryCardTitle").textContent = "Batch Tracking & Expiration Monitor (OBTN)";
  const thead = document.getElementById("inventoryThead");
  const tbody = document.getElementById("inventoryTbody");

  thead.innerHTML = `<tr><th>Batch Number</th><th>Item Code</th><th>Stock Qty</th><th>Mfg Date</th><th>Expiry Date</th><th>Warehouse</th><th>Status</th></tr>`;
  tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;">Loading batches...</td></tr>`;

  try {
    const res = await fetch("/api/table/OBTN?limit=50");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td><strong>${r.DistNumber}</strong></td>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openItemInspector('${r.ItemCode}')">➡️</span>
            ${r.ItemCode}
          </span>
        </td>
        <td>${r.Quantity}</td>
        <td>${r.MnfDate || 'N/A'}</td>
        <td style="color:var(--warning); font-weight:600;">${r.ExpDate || 'N/A'}</td>
        <td>Whs ${r.WhsCode}</td>
        <td><span class="sap-badge-status status-closed">Released</span></td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

async function loadBins() {
  document.getElementById("inventoryCardTitle").textContent = "Warehouse Bin Locations (OBIN)";
  const thead = document.getElementById("inventoryThead");
  const tbody = document.getElementById("inventoryTbody");

  thead.innerHTML = `<tr><th>Bin Code</th><th>Warehouse</th><th>Aisle</th><th>Rack</th><th>Shelf</th><th>Description</th></tr>`;
  tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;">Loading bin locations...</td></tr>`;

  try {
    const res = await fetch("/api/table/OBIN?limit=50");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td><strong>${r.BinCode}</strong></td>
        <td>Whs ${r.WhsCode}</td>
        <td>${r.Aisle}</td>
        <td>${r.Rack}</td>
        <td>${r.Shelf}</td>
        <td>${r.Descr}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

async function openItemInspector(itemCode) {
  try {
    const res = await fetch(`/api/item/${itemCode}`);
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }

    const item = data.item;
    const content = `
      <div class="doc-form-card">
        <div class="doc-form-header">
          <div class="form-group">
            <label>Item Code & Name</label>
            <div class="form-val">${item.ItemCode} - ${item.ItemName}</div>
          </div>
          <div class="form-group">
            <label>Total On Hand</label>
            <div class="form-val" style="color:var(--success); font-size:16px;">${item.OnHand} Units</div>
          </div>
          <div class="form-group">
            <label>Average Valuation Price</label>
            <div class="form-val">$${item.AvgPrice.toFixed(2)} AUD</div>
          </div>
          <div class="form-group">
            <label>Committed / On PO</label>
            <div class="form-val">${item.IsCommited} Comm. / ${item.OnOrder} On PO</div>
          </div>
        </div>

        <div style="padding:16px;">
          <h4 style="margin-bottom:8px; font-size:13px; text-transform:uppercase; color:var(--text-muted);">Warehouse Breakdown (OITW)</h4>
          <div class="sap-table-wrap">
            <table class="sap-table">
              <thead><tr><th>Warehouse</th><th>Name</th><th>City</th><th>On Hand</th><th>Committed</th><th>Available</th></tr></thead>
              <tbody>
                ${data.warehouses.map(w => `
                  <tr>
                    <td><strong>Whs ${w.WhsCode}</strong></td>
                    <td>${w.WhsName}</td>
                    <td>${w.City}</td>
                    <td>${w.OnHand}</td>
                    <td>${w.IsCommited}</td>
                    <td style="font-weight:700; color:var(--success);">${(w.OnHand - w.IsCommited + w.OnOrder).toFixed(1)}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>

          <h4 style="margin-top:16px; margin-bottom:8px; font-size:13px; text-transform:uppercase; color:var(--text-muted);">Multi-Tier Price Lists (ITM1)</h4>
          <div class="sap-table-wrap">
            <table class="sap-table">
              <thead><tr><th>List #</th><th>Price List Name</th><th>Price</th><th>Currency</th><th>Markup</th></tr></thead>
              <tbody>
                ${data.prices.map(p => `
                  <tr>
                    <td>${p.PriceList}</td>
                    <td><strong>${p.ListName}</strong></td>
                    <td>$${p.Price.toFixed(2)}</td>
                    <td>${p.Currency}</td>
                    <td>x${p.Factor}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>

          ${data.bom && data.bom.length ? `
            <h4 style="margin-top:16px; margin-bottom:8px; font-size:13px; text-transform:uppercase; color:var(--text-muted);">Bill of Materials Structure (ITT1)</h4>
            <div class="sap-table-wrap">
              <table class="sap-table">
                <thead><tr><th>Component Code</th><th>Description</th><th>Required Qty</th><th>Unit Cost</th></tr></thead>
                <tbody>
                  ${data.bom.map(b => `
                    <tr>
                      <td>${b.Code}</td>
                      <td>${b.ItemName}</td>
                      <td>${b.Quantity}</td>
                      <td>$${b.Price.toFixed(2)}</td>
                    </tr>
                  `).join("")}
                </tbody>
              </table>
            </div>
          ` : ''}
        </div>
      </div>
    `;

    showModal(`Item Master 360°: ${item.ItemName}`, content);

  } catch (err) {
    alert("Error loading item inspector: " + err.message);
  }
}

// -----------------------------------------------------------------
// 6. Production & Manufacturing View
// -----------------------------------------------------------------
function initProductionView() {
  document.getElementById("btnShowBOMTrees").addEventListener("click", () => {
    document.getElementById("btnShowBOMTrees").classList.add("active");
    document.getElementById("btnShowWorkOrders").classList.remove("active");
    loadBOMTrees();
  });
  document.getElementById("btnShowWorkOrders").addEventListener("click", () => {
    document.getElementById("btnShowWorkOrders").classList.add("active");
    document.getElementById("btnShowBOMTrees").classList.remove("active");
    loadWorkOrders();
  });
}

async function loadBOMTrees() {
  document.getElementById("prodCardTitle").textContent = "Bill of Materials (BOM) Product Trees (OITT)";
  const thead = document.getElementById("prodThead");
  const tbody = document.getElementById("prodTbody");

  thead.innerHTML = `<tr><th>Parent Item</th><th>Tree Type</th><th>Base Qty</th><th>Price List</th><th>Target Whs</th><th>Action</th></tr>`;
  tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;">Loading BOM product trees...</td></tr>`;

  try {
    const res = await fetch("/api/table/OITT?limit=50");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openItemInspector('${r.Code}')">➡️</span>
            <strong>${r.Code}</strong>
          </span>
        </td>
        <td><span class="sap-badge-status status-open">Production BOM</span></td>
        <td>${r.Quantity}</td>
        <td>List #${r.PriceList}</td>
        <td>Whs ${r.ToWhsCode}</td>
        <td>
          <button class="sap-btn sap-btn-sm sap-btn-primary" onclick="openDocForm('OITT', '${r.Code}')">Explode BOM 💥</button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

async function loadWorkOrders() {
  document.getElementById("prodCardTitle").textContent = "Production Orders & Work in Progress (OWOR)";
  const thead = document.getElementById("prodThead");
  const tbody = document.getElementById("prodTbody");

  thead.innerHTML = `<tr><th>Order #</th><th>Item Code</th><th>Status</th><th>Planned Qty</th><th>Completed</th><th>Order Date</th><th>Action</th></tr>`;
  tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;">Loading work orders...</td></tr>`;

  try {
    const res = await fetch("/api/table/OWOR?limit=50");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td><strong>#${r.DocNum}</strong></td>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openItemInspector('${r.ItemCode}')">➡️</span>
            ${r.ItemCode}
          </span>
        </td>
        <td><span class="sap-badge-status ${r.Status === 'R' ? 'status-open' : 'status-closed'}">${r.Status === 'R' ? 'Released' : 'Closed'}</span></td>
        <td>${r.PlannedQty}</td>
        <td><strong>${r.CmpltQty}</strong></td>
        <td>${r.PostDate}</td>
        <td>
          <button class="sap-btn sap-btn-sm" onclick="openDocForm('OWOR', ${r.DocEntry})">View Work Order 📑</button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

// -----------------------------------------------------------------
// 7. Financials View
// -----------------------------------------------------------------
function initFinancialsView() {
  document.getElementById("btnShowCOA").addEventListener("click", loadCOA);
  document.getElementById("btnShowJournalEntries").addEventListener("click", loadJournalEntries);
  document.getElementById("btnShowCostCenters").addEventListener("click", loadCostCenters);
}

async function loadCOA() {
  document.getElementById("finCardTitle").textContent = "General Ledger Chart of Accounts (OACT)";
  const thead = document.getElementById("finThead");
  const tbody = document.getElementById("finTbody");

  thead.innerHTML = `<tr><th>Account Code</th><th>Account Name</th><th>Type</th><th>Current Total</th><th>Levels</th><th>Financial</th></tr>`;
  tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;">Loading Chart of Accounts...</td></tr>`;

  try {
    const res = await fetch("/api/table/OACT?limit=100");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td><strong>${r.AcctCode}</strong></td>
        <td>${r.AcctName}</td>
        <td><span class="sap-badge-status ${r.ActType === 'A' ? 'status-open' : (r.ActType === 'L' ? 'status-lost' : 'status-won')}">${r.ActType}</span></td>
        <td style="font-weight:700;">$${r.CurrTotal.toFixed(2)}</td>
        <td>Level ${r.Levels}</td>
        <td>${r.Financ}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

async function loadJournalEntries() {
  document.getElementById("finCardTitle").textContent = "Balanced Financial Journal Entries (OJDT)";
  const thead = document.getElementById("finThead");
  const tbody = document.getElementById("finTbody");

  thead.innerHTML = `<tr><th>Trans ID</th><th>Ref Date</th><th>Memo</th><th>Total Amount</th><th>Action</th></tr>`;
  tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Loading journal entries...</td></tr>`;

  try {
    const res = await fetch("/api/table/OJDT?limit=50");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td><strong>#${r.TransId}</strong></td>
        <td>${r.RefDate}</td>
        <td>${r.Memo}</td>
        <td style="font-weight:700; color:var(--primary);">$${r.LocTotal.toFixed(2)}</td>
        <td>
          <button class="sap-btn sap-btn-sm sap-btn-primary" onclick="openDocForm('OJDT', ${r.TransId})">View Debits/Credits 📑</button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

async function loadCostCenters() {
  document.getElementById("finCardTitle").textContent = "Cost & Profit Centers (OPRC)";
  const thead = document.getElementById("finThead");
  const tbody = document.getElementById("finTbody");

  thead.innerHTML = `<tr><th>Center Code</th><th>Center Name</th><th>Dimension</th><th>Group</th><th>Active</th></tr>`;
  tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Loading cost centers...</td></tr>`;

  try {
    const res = await fetch("/api/table/OPRC?limit=50");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td><strong>${r.PrcCode}</strong></td>
        <td>${r.PrcName}</td>
        <td>Dim ${r.DimCode}</td>
        <td>${r.GrpCode}</td>
        <td><span class="sap-badge-status status-closed">${r.Active}</span></td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

// -----------------------------------------------------------------
// 8. CRM View
// -----------------------------------------------------------------
function initCRMView() {
  document.getElementById("btnRefreshCRM").addEventListener("click", loadCRMOpportunities);
}

async function loadCRMOpportunities() {
  const tbody = document.getElementById("crmTableBody");
  tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;">Loading CRM Pipeline...</td></tr>`;

  try {
    const res = await fetch("/api/table/OOPR?limit=50");
    const data = await res.json();
    tbody.innerHTML = data.rows.map(r => `
      <tr>
        <td><strong>#${r.OpprId}</strong></td>
        <td>${r.Name}</td>
        <td>
          <span class="cell-with-arrow">
            <span class="golden-arrow-btn" onclick="openBPInspector('${r.CardCode}')">➡️</span>
            ${r.CardCode}
          </span>
        </td>
        <td style="font-weight:700; color:var(--primary);">$${r.MaxSumLoc.toFixed(2)}</td>
        <td>${r.ClosePrcnt}%</td>
        <td><span class="sap-badge-status ${r.Status === 'W' ? 'status-won' : (r.Status === 'O' ? 'status-open' : 'status-lost')}">${r.Status === 'W' ? 'Won' : (r.Status === 'O' ? 'In Progress' : 'Lost')}</span></td>
        <td>${r.OpenDate}</td>
        <td>${r.CloseDate || 'N/A'}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

// -----------------------------------------------------------------
// 9. SQL Studio Logic
// -----------------------------------------------------------------
function initSQLStudio() {
  const presetsContainer = document.getElementById("sqlPresetsList");
  presetsContainer.innerHTML = PRESET_QUERIES.map((p, idx) => `
    <div class="preset-item" onclick="loadSQLPreset(${idx})">${p.title}</div>
  `).join("");

  document.getElementById("btnExecuteSQL").addEventListener("click", executeCurrentSQL);

  document.getElementById("sqlQueryText").addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      executeCurrentSQL();
    }
  });
}

function loadSQLPreset(idx) {
  const p = PRESET_QUERIES[idx];
  document.getElementById("sqlQueryText").value = p.sql;
  executeCurrentSQL();
}

async function executeCurrentSQL() {
  const sql = document.getElementById("sqlQueryText").value.trim();
  if (!sql) return;

  const thead = document.getElementById("sqlResultThead");
  const tbody = document.getElementById("sqlResultTbody");
  const statusEl = document.getElementById("sqlResultStatus");
  const timeEl = document.getElementById("sqlExecutionTime");

  statusEl.textContent = "Executing query...";
  tbody.innerHTML = `<tr><td style="text-align:center;">Running query on new_b1.db...</td></tr>`;

  try {
    const res = await fetch("/api/sql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: sql })
    });

    const data = await res.json();
    if (data.error) {
      statusEl.textContent = "Query Failed";
      timeEl.textContent = `${data.duration_ms || 0} ms`;
      tbody.innerHTML = `<tr><td style="color:var(--danger);">${data.error}</td></tr>`;
      return;
    }

    statusEl.textContent = `Returned ${data.count} rows`;
    timeEl.textContent = `${data.duration_ms} ms`;

    if (data.columns && data.columns.length) {
      thead.innerHTML = `<tr>${data.columns.map(c => `<th>${c}</th>`).join("")}</tr>`;
      tbody.innerHTML = data.rows.map(r => `
        <tr>
          ${data.columns.map(c => {
            const val = r[c];
            if (c === "CardCode" && val) {
              return `<td><span class="cell-with-arrow"><span class="golden-arrow-btn" onclick="openBPInspector('${val}')">➡️</span>${val}</span></td>`;
            }
            if (c === "ItemCode" && val) {
              return `<td><span class="cell-with-arrow"><span class="golden-arrow-btn" onclick="openItemInspector('${val}')">➡️</span>${val}</span></td>`;
            }
            return `<td>${val !== null ? val : ''}</td>`;
          }).join("")}
        </tr>
      `).join("");
    } else {
      thead.innerHTML = "";
      tbody.innerHTML = `<tr><td style="color:var(--success);">${data.message || 'Success'}</td></tr>`;
    }

  } catch (err) {
    statusEl.textContent = "Error";
    tbody.innerHTML = `<tr><td style="color:var(--danger);">${err.message}</td></tr>`;
  }
}

// -----------------------------------------------------------------
// 10. All 82 Tables Browser
// -----------------------------------------------------------------
function initAllTablesView() {
  document.getElementById("tablesFilterInput").addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase();
    renderAllTables(allTablesCache.filter(t => t.name.toLowerCase().includes(q) || t.category.toLowerCase().includes(q)));
  });
}

async function loadAllTablesList() {
  const tbody = document.getElementById("allTablesBody");
  tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Loading 82 tables...</td></tr>`;

  try {
    const res = await fetch("/api/tables");
    const data = await res.json();
    allTablesCache = data.tables || [];
    renderAllTables(allTablesCache);
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" style="color:var(--danger); text-align:center;">Error: ${err.message}</td></tr>`;
  }
}

function renderAllTables(tables) {
  const tbody = document.getElementById("allTablesBody");
  tbody.innerHTML = tables.map((t, idx) => `
    <tr>
      <td>${idx + 1}</td>
      <td><strong>${t.name}</strong></td>
      <td><span class="sap-badge-status status-open">${t.category}</span></td>
      <td><strong>${t.count}</strong> rows</td>
      <td>
        <button class="sap-btn sap-btn-sm sap-btn-primary" onclick="openTableBrowser('${t.name}')">Browse Data 🔍</button>
      </td>
    </tr>
  `).join("");
}

function openTableBrowser(tableName) {
  document.getElementById("sqlQueryText").value = `SELECT * FROM ${tableName} LIMIT 50;`;
  switchView("sqlstudio");
  executeCurrentSQL();
}

// -----------------------------------------------------------------
// Modal Inspector Controller
// -----------------------------------------------------------------
function initModal() {
  const modal = document.getElementById("inspectorModal");
  const closeBtn = document.getElementById("modalCloseBtn");
  closeBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });
}

function showModal(title, htmlContent) {
  document.getElementById("modalTitle").innerHTML = title;
  document.getElementById("modalBody").innerHTML = htmlContent;
  document.getElementById("inspectorModal").classList.add("open");
}

function closeModal() {
  document.getElementById("inspectorModal").classList.remove("open");
}
