# 流程圖設計 — 考古題收藏系統

## 1. 使用者流程圖（User Flow）

以下流程圖描述使用者進入網站後的所有操作路徑。

### 1.1 主要操作流程

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁]
    B --> C{要執行什麼操作？}

    C -->|瀏覽科目| D[科目列表頁]
    C -->|瀏覽教授| E[教授列表頁]
    C -->|瀏覽考古題| F[考古題列表頁]
    C -->|搜尋考古題| G[搜尋頁面]

    D --> D1{科目操作}
    D1 -->|新增科目| D2[填寫科目表單]
    D2 --> D3[儲存科目]
    D3 --> D[回到科目列表]
    D1 -->|查看科目| D4[科目詳情頁]
    D4 --> D5[查看該科目考古題]
    D1 -->|編輯科目| D6[編輯科目表單]
    D6 --> D3
    D1 -->|刪除科目| D7[確認刪除]
    D7 --> D

    E --> E1{教授操作}
    E1 -->|新增教授| E2[填寫教授表單]
    E2 --> E3[儲存教授]
    E3 --> E[回到教授列表]
    E1 -->|查看教授| E4[教授詳情頁]
    E4 --> E5[查看該教授考古題]
    E1 -->|編輯教授| E6[編輯教授表單]
    E6 --> E3
    E1 -->|刪除教授| E7[確認刪除]
    E7 --> E

    F --> F1{考古題操作}
    F1 -->|新增考古題| F2[填寫考古題表單]
    F2 --> F3[儲存考古題]
    F3 --> F[回到考古題列表]
    F1 -->|查看考古題| F4[考古題詳情頁]
    F1 -->|編輯考古題| F5[編輯考古題表單]
    F5 --> F3
    F1 -->|刪除考古題| F6[確認刪除]
    F6 --> F
    F1 -->|篩選| F7[依科目/教授/年度篩選]
    F7 --> F

    G --> G1[輸入關鍵字]
    G1 --> G2[顯示搜尋結果]
    G2 --> G3{進一步操作}
    G3 -->|查看詳情| F4
    G3 -->|再次篩選| G4[依科目/教授/年度篩選結果]
    G4 --> G2
```

### 1.2 考古題新增流程（詳細版）

```mermaid
flowchart TD
    START([使用者點擊「新增考古題」]) --> FORM[顯示考古題表單]
    FORM --> FILL[填寫欄位]

    FILL --> TITLE[輸入標題]
    FILL --> SUBJECT[選擇科目]
    FILL --> PROFESSOR[選擇教授]
    FILL --> YEAR[選擇學年度]
    FILL --> SEMESTER[選擇學期]
    FILL --> TYPE[選擇考試類型]
    FILL --> CONTENT[輸入題目內容]

    TITLE & SUBJECT & PROFESSOR & YEAR & SEMESTER & TYPE & CONTENT --> SUBMIT[點擊「送出」]

    SUBMIT --> VALIDATE{伺服器驗證}
    VALIDATE -->|驗證失敗| ERROR[顯示錯誤訊息]
    ERROR --> FORM
    VALIDATE -->|驗證成功| SAVE[儲存至資料庫]
    SAVE --> REDIRECT[重導向至考古題列表]
    REDIRECT --> SUCCESS[顯示成功訊息]
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 瀏覽考古題列表

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br/>(exam.py)
    participant Model as Model<br/>(exam.py)
    participant DB as SQLite

    User->>Browser: 點擊「考古題列表」
    Browser->>Route: GET /exams
    Route->>Model: get_all_exams()
    Model->>DB: SELECT * FROM exams<br/>JOIN subjects, professors
    DB-->>Model: 回傳考古題資料
    Model-->>Route: 回傳考古題物件列表
    Route->>Route: render_template("exams/list.html", exams=exams)
    Route-->>Browser: HTTP 200 + HTML 頁面
    Browser-->>User: 顯示考古題列表
```

### 2.2 新增考古題

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br/>(exam.py)
    participant Model as Model<br/>(exam.py)
    participant DB as SQLite

    User->>Browser: 點擊「新增考古題」
    Browser->>Route: GET /exams/create
    Route->>Route: render_template("exams/form.html")
    Route-->>Browser: HTTP 200 + 表單頁面
    Browser-->>User: 顯示空白表單

    User->>Browser: 填寫表單並點擊「送出」
    Browser->>Route: POST /exams/create
    Route->>Route: 驗證表單資料
    alt 驗證失敗
        Route-->>Browser: HTTP 200 + 表單頁面（含錯誤訊息）
        Browser-->>User: 顯示錯誤提示
    else 驗證成功
        Route->>Model: create_exam(data)
        Model->>DB: INSERT INTO exams VALUES(...)
        DB-->>Model: 成功
        Model-->>Route: 回傳新增的考古題
        Route-->>Browser: HTTP 302 redirect /exams
        Browser->>Route: GET /exams
        Route-->>Browser: HTTP 200 + 列表頁面
        Browser-->>User: 顯示考古題列表 + 成功訊息
    end
```

### 2.3 搜尋考古題

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br/>(search.py)
    participant Model as Model<br/>(exam.py)
    participant DB as SQLite

    User->>Browser: 輸入關鍵字並點擊「搜尋」
    Browser->>Route: GET /search?q=微積分
    Route->>Model: search_exams("微積分")
    Model->>DB: SELECT * FROM exams<br/>WHERE title LIKE '%微積分%'<br/>OR content LIKE '%微積分%'
    DB-->>Model: 回傳匹配的考古題
    Model-->>Route: 回傳搜尋結果列表
    Route->>Route: render_template("search/results.html", results=results)
    Route-->>Browser: HTTP 200 + 搜尋結果頁面
    Browser-->>User: 顯示搜尋結果（標示匹配關鍵字）
```

### 2.4 編輯考古題

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br/>(exam.py)
    participant Model as Model<br/>(exam.py)
    participant DB as SQLite

    User->>Browser: 點擊「編輯」按鈕
    Browser->>Route: GET /exams/1/edit
    Route->>Model: get_exam_by_id(1)
    Model->>DB: SELECT * FROM exams WHERE id = 1
    DB-->>Model: 回傳考古題資料
    Model-->>Route: 回傳考古題物件
    Route->>Route: render_template("exams/form.html", exam=exam)
    Route-->>Browser: HTTP 200 + 預填表單
    Browser-->>User: 顯示已填入資料的表單

    User->>Browser: 修改內容並點擊「更新」
    Browser->>Route: POST /exams/1/edit
    Route->>Route: 驗證表單資料
    Route->>Model: update_exam(1, data)
    Model->>DB: UPDATE exams SET ... WHERE id = 1
    DB-->>Model: 成功
    Model-->>Route: 回傳更新結果
    Route-->>Browser: HTTP 302 redirect /exams/1
    Browser->>Route: GET /exams/1
    Route-->>Browser: HTTP 200 + 詳情頁面
    Browser-->>User: 顯示更新後的考古題
```

### 2.5 刪除考古題

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br/>(exam.py)
    participant Model as Model<br/>(exam.py)
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser->>Route: POST /exams/1/delete
    Route->>Model: delete_exam(1)
    Model->>DB: DELETE FROM exams WHERE id = 1
    DB-->>Model: 成功
    Model-->>Route: 回傳刪除結果
    Route-->>Browser: HTTP 302 redirect /exams
    Browser->>Route: GET /exams
    Route-->>Browser: HTTP 200 + 列表頁面
    Browser-->>User: 顯示考古題列表 + 刪除成功訊息
```

---

## 3. 功能清單對照表

| 功能             | URL 路徑              | HTTP 方法 | 說明                       |
| ---------------- | --------------------- | --------- | -------------------------- |
| 首頁             | `/`                   | GET       | 顯示系統首頁與統計資訊     |
| 科目列表         | `/subjects`           | GET       | 顯示所有科目               |
| 新增科目         | `/subjects/create`    | GET/POST  | 顯示表單 / 處理新增        |
| 科目詳情         | `/subjects/<id>`      | GET       | 顯示科目資訊與相關考古題   |
| 編輯科目         | `/subjects/<id>/edit` | GET/POST  | 顯示編輯表單 / 處理更新    |
| 刪除科目         | `/subjects/<id>/delete` | POST    | 處理刪除科目               |
| 教授列表         | `/professors`         | GET       | 顯示所有教授               |
| 新增教授         | `/professors/create`  | GET/POST  | 顯示表單 / 處理新增        |
| 教授詳情         | `/professors/<id>`    | GET       | 顯示教授資訊與相關考古題   |
| 編輯教授         | `/professors/<id>/edit` | GET/POST | 顯示編輯表單 / 處理更新    |
| 刪除教授         | `/professors/<id>/delete` | POST  | 處理刪除教授               |
| 考古題列表       | `/exams`              | GET       | 顯示所有考古題（可篩選）   |
| 新增考古題       | `/exams/create`       | GET/POST  | 顯示表單 / 處理新增        |
| 考古題詳情       | `/exams/<id>`         | GET       | 顯示考古題完整內容         |
| 編輯考古題       | `/exams/<id>/edit`    | GET/POST  | 顯示編輯表單 / 處理更新    |
| 刪除考古題       | `/exams/<id>/delete`  | POST      | 處理刪除考古題             |
| 搜尋考古題       | `/search`             | GET       | 依關鍵字搜尋考古題         |

---

*文件產出日期：2026-04-28*
*文件版本：v1.0*
