# 路由設計 — 考古題收藏系統

## 1. 路由總覽表格

### 1.1 首頁路由（main）

| 功能     | HTTP 方法 | URL 路徑 | 對應模板           | 說明               |
| -------- | --------- | -------- | ------------------ | ------------------ |
| 首頁     | GET       | `/`      | `index.html`       | 顯示系統首頁與統計 |

### 1.2 科目路由（subjects）

| 功能         | HTTP 方法 | URL 路徑                | 對應模板                  | 說明                     |
| ------------ | --------- | ----------------------- | ------------------------- | ------------------------ |
| 科目列表     | GET       | `/subjects`             | `subjects/list.html`      | 顯示所有科目             |
| 新增科目頁面 | GET       | `/subjects/create`      | `subjects/form.html`      | 顯示新增科目表單         |
| 建立科目     | POST      | `/subjects/create`      | —                         | 接收表單，存入 DB        |
| 科目詳情     | GET       | `/subjects/<id>`        | `subjects/detail.html`    | 顯示科目資訊與考古題     |
| 編輯科目頁面 | GET       | `/subjects/<id>/edit`   | `subjects/form.html`      | 顯示編輯表單（預填資料） |
| 更新科目     | POST      | `/subjects/<id>/edit`   | —                         | 接收表單，更新 DB        |
| 刪除科目     | POST      | `/subjects/<id>/delete` | —                         | 刪除後重導向至列表       |

### 1.3 教授路由（professors）

| 功能         | HTTP 方法 | URL 路徑                   | 對應模板                    | 說明                       |
| ------------ | --------- | -------------------------- | --------------------------- | -------------------------- |
| 教授列表     | GET       | `/professors`              | `professors/list.html`      | 顯示所有教授               |
| 新增教授頁面 | GET       | `/professors/create`       | `professors/form.html`      | 顯示新增教授表單           |
| 建立教授     | POST      | `/professors/create`       | —                           | 接收表單，存入 DB          |
| 教授詳情     | GET       | `/professors/<id>`         | `professors/detail.html`    | 顯示教授資訊與考古題       |
| 編輯教授頁面 | GET       | `/professors/<id>/edit`    | `professors/form.html`      | 顯示編輯表單（預填資料）   |
| 更新教授     | POST      | `/professors/<id>/edit`    | —                           | 接收表單，更新 DB          |
| 刪除教授     | POST      | `/professors/<id>/delete`  | —                           | 刪除後重導向至列表         |

### 1.4 考古題路由（exams）

| 功能           | HTTP 方法 | URL 路徑              | 對應模板              | 說明                       |
| -------------- | --------- | --------------------- | --------------------- | -------------------------- |
| 考古題列表     | GET       | `/exams`              | `exams/list.html`     | 顯示所有考古題（可篩選）   |
| 新增考古題頁面 | GET       | `/exams/create`       | `exams/form.html`     | 顯示新增考古題表單         |
| 建立考古題     | POST      | `/exams/create`       | —                     | 接收表單，存入 DB          |
| 考古題詳情     | GET       | `/exams/<id>`         | `exams/detail.html`   | 顯示考古題完整內容         |
| 編輯考古題頁面 | GET       | `/exams/<id>/edit`    | `exams/form.html`     | 顯示編輯表單（預填資料）   |
| 更新考古題     | POST      | `/exams/<id>/edit`    | —                     | 接收表單，更新 DB          |
| 刪除考古題     | POST      | `/exams/<id>/delete`  | —                     | 刪除後重導向至列表         |

### 1.5 搜尋路由（search）

| 功能       | HTTP 方法 | URL 路徑   | 對應模板                | 說明                     |
| ---------- | --------- | ---------- | ----------------------- | ------------------------ |
| 搜尋考古題 | GET       | `/search`  | `search/results.html`   | 依關鍵字搜尋並顯示結果   |

---

## 2. 每個路由的詳細說明

### 2.1 首頁 `GET /`

- **輸入：** 無
- **處理邏輯：**
  1. 呼叫 `Subject.get_all()` 取得科目數量
  2. 呼叫 `Exam.get_all()` 取得考古題數量
  3. 呼叫 `Professor.get_all()` 取得教授數量
- **輸出：** 渲染 `index.html`，傳入統計數據
- **錯誤處理：** 無特殊錯誤情境

### 2.2 科目列表 `GET /subjects`

- **輸入：** 無
- **處理邏輯：** 呼叫 `Subject.get_all()` 取得所有科目（含考古題數量）
- **輸出：** 渲染 `subjects/list.html`，傳入 `subjects` 列表
- **錯誤處理：** 無特殊錯誤情境

### 2.3 新增科目 `GET/POST /subjects/create`

- **GET — 顯示表單：**
  - 輸入：無
  - 輸出：渲染 `subjects/form.html`（空白表單）

- **POST — 處理新增：**
  - 輸入：表單欄位 `name`（必填）、`description`（選填）
  - 處理邏輯：
    1. 驗證 `name` 不為空
    2. 呼叫 `Subject.create(name, description)`
    3. 設定 flash 成功訊息
  - 輸出：重導向至 `/subjects`
  - 錯誤處理：驗證失敗時，重新渲染表單並顯示錯誤訊息

### 2.4 科目詳情 `GET /subjects/<id>`

- **輸入：** URL 參數 `id`
- **處理邏輯：**
  1. 呼叫 `Subject.get_by_id(id)` 取得科目資料
  2. 呼叫 `Exam.get_by_subject(id)` 取得該科目的考古題
  3. 呼叫 `Professor.get_by_subject(id)` 取得該科目的教授
- **輸出：** 渲染 `subjects/detail.html`
- **錯誤處理：** 科目不存在時回傳 404

### 2.5 編輯科目 `GET/POST /subjects/<id>/edit`

- **GET — 顯示編輯表單：**
  - 輸入：URL 參數 `id`
  - 處理邏輯：呼叫 `Subject.get_by_id(id)` 取得現有資料
  - 輸出：渲染 `subjects/form.html`（預填資料）

- **POST — 處理更新：**
  - 輸入：URL 參數 `id`、表單欄位 `name`、`description`
  - 處理邏輯：呼叫 `Subject.update(id, name, description)`
  - 輸出：重導向至 `/subjects/<id>`

### 2.6 刪除科目 `POST /subjects/<id>/delete`

- **輸入：** URL 參數 `id`
- **處理邏輯：** 呼叫 `Subject.delete(id)`
- **輸出：** 重導向至 `/subjects`
- **錯誤處理：** 科目不存在時回傳 404

### 2.7 教授路由

教授路由的設計邏輯與科目路由類似，差異在於：
- 新增/編輯表單需提供科目下拉選單（呼叫 `Subject.get_all()` 取得選項）
- 教授詳情頁額外顯示該教授出過的所有考古題

### 2.8 考古題路由

考古題路由的設計邏輯與科目路由類似，差異在於：
- 列表頁支援依科目、教授、學年度、考試類型篩選（使用 URL query 參數）
- 新增/編輯表單需提供科目與教授下拉選單
- 表單欄位較多：title, subject_id, professor_id, year, semester, exam_type, content

### 2.9 搜尋 `GET /search`

- **輸入：** Query 參數 `q`（關鍵字）、`subject_id`（選填）、`professor_id`（選填）、`year`（選填）
- **處理邏輯：**
  1. 取得搜尋關鍵字
  2. 呼叫 `Exam.search(keyword, subject_id, professor_id, year)`
  3. 呼叫 `Subject.get_all()` 和 `Professor.get_all()` 取得篩選選項
- **輸出：** 渲染 `search/results.html`，傳入搜尋結果
- **錯誤處理：** 關鍵字為空時顯示空結果

---

## 3. Jinja2 模板清單

所有模板皆繼承 `base.html` 基礎版面。

| 模板檔案                      | 繼承自      | 說明                           |
| ----------------------------- | ----------- | ------------------------------ |
| `base.html`                   | —           | 基礎版面（nav + footer）       |
| `index.html`                  | `base.html` | 首頁（統計數據 + 快速連結）    |
| `subjects/list.html`          | `base.html` | 科目列表（卡片式顯示）         |
| `subjects/detail.html`        | `base.html` | 科目詳情 + 該科目考古題列表    |
| `subjects/form.html`          | `base.html` | 科目新增/編輯表單（共用）      |
| `professors/list.html`        | `base.html` | 教授列表                       |
| `professors/detail.html`      | `base.html` | 教授詳情 + 該教授考古題列表    |
| `professors/form.html`        | `base.html` | 教授新增/編輯表單（共用）      |
| `exams/list.html`             | `base.html` | 考古題列表 + 篩選功能          |
| `exams/detail.html`           | `base.html` | 考古題詳情（完整內容）         |
| `exams/form.html`             | `base.html` | 考古題新增/編輯表單（共用）    |
| `search/results.html`         | `base.html` | 搜尋結果 + 篩選選項            |

---

*文件產出日期：2026-04-28*
*文件版本：v1.0*
