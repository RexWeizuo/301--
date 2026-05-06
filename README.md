# 301 数学考研学习系统

301 数学考研学习系统，含考纲知识点、章节题目、艾宾浩斯复习调度。

## 快速启动

> **前提：** 四个项目共用 `D:\study\.venv` 虚拟环境。如果还没安装过，先执行一次环境安装：
> ```powershell
> cd D:\study
> uv venv .venv
> # 然后进入各项目的 app 目录，pip install -r requirements.txt 安装依赖
> ```

### 生产模式（最常用的启动方式）

```powershell
# 1. 构建前端（第一次或每次改前端代码后执行）
cd D:\study\301\frontend
npm install               # 仅第一次
npm run build

# 2. 启动后端（提供静态前端 + API）
cd D:\study\301\app
..\..\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --port 3011
```

浏览器访问 `http://localhost:3011`。**首次启动会自动导入数据库（终端会打印"大纲数据导入成功"）。**

### 开发模式（改代码自动刷新）

打开**两个**终端窗口：

**终端 1 — 前端 dev server：**
```powershell
cd D:\study\301\frontend
npm install        # 仅第一次运行
npm run dev        # 启动后访问 http://localhost:3010
```

**终端 2 — 后端：**
```powershell
cd D:\study\301\app
..\..\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --port 3011 --reload
```

前端会自动把 `/api` 请求代理到后端 `localhost:3011`。

## 端口说明

| 服务 | 端口 |
|------|------|
| 后端 API | 3011 |
| 前端 dev server | 3010（仅开发时用） |

## 功能模块

- **考纲浏览**：高等数学、线性代数、概率论三科考纲知识点
- **习题练习**：按知识点分类的练习题
- **学习规划**：艾宾浩斯遗忘曲线复习提醒与进度管理

## 技术栈

- 后端：FastAPI + SQLAlchemy + aiosqlite（异步 SQLite）
- 前端：Vue 3 + Vue Router + Pinia + ECharts + Tailwind CSS
- 数据库：SQLite（`301_study.db` 位于项目根目录）

## 项目结构

```
301/
├── app/              # 后端 FastAPI 应用
│   ├── main.py       # 入口（含 API 路由和前端静态文件服务）
│   ├── config.py     # 配置（考试日期 2026-12-19 等）
│   ├── database.py   # 数据库连接
│   ├── models.py     # ORM 模型（Subject, Chapter, KnowledgePoint, Question...）
│   ├── schemas.py    # Pydantic 模式
│   ├── init_db.py    # 数据库初始化（首次启动自动运行）
│   └── routes/       # API 路由
├── frontend/         # 前端 Vue 3 项目
├── scripts/          # 工具脚本
├── 极限/             # 极限章节手写笔记图片
├── 极限_latex/       # 极限章节 LaTeX 公式笔记（AI 提取）
├── requirements.txt  # Python 依赖
└── 301_study.db      # SQLite 数据库（首次启动后生成）
```

## 故障排除

**前端打开后考纲/题目都是空的：**
1. 确认后端已启动并打印了 `大纲数据导入成功`
2. 如果没看到这句话，说明数据库初始化失败——检查虚拟环境是否激活（`..\..\.venv\Scripts\Activate.ps1`）
3. 确认 `.venv` 中已安装依赖：`pip install -r requirements.txt`

**端口被占用：**
```powershell
# 查看谁占用了 3011 端口
netstat -ano | findstr :3011
# 终止进程（替换 PID）
taskkill /PID <PID> /F
```
