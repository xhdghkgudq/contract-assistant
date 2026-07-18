# 基于大模型的合同智能管理助手


> 一款融合 AI 大模型技术的智能合同管理系统，实现合同自动化审查、风险识别与全生命周期管理

## 目录

- [项目简介](#项目简介)
- [核心功能](#核心功能)
- [技术架构](#技术架构)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [功能亮点](#功能亮点)
- [数据库设计](#数据库设计)
- [API 文档](#api-文档)

---

## 项目简介

**基于大模型的合同智能管理助手** 是一款面向企业法务、财务和商务人员的智能化合同管理平台。系统深度融合智谱 AI 大模型，能够自动识别合同关键信息、智能评估合同风险，并提供合规性检查，帮助用户大幅提升合同审查效率，降低法律风险。

### 解决痛点

| 传统合同管理               | AI 智能管理              |
| -------------------------- | ------------------------ |
| 人工审查耗时 30-60 分钟/份 | AI 自动分析仅需 10-30 秒 |
| 人工提取信息易出错         | 精准识别合同要素         |
| 风险条款易遗漏             | 智能风险预警             |
| 文件管理混乱               | 全生命周期追踪           |

---

## 核心功能

### 1. 合同上传与解析

- 支持 **PDF** 和 **TXT** 格式合同文件
- 自动识别并提取合同文本内容
- 智能分类存储

### 2. AI 智能分析

- 调用智谱 AI GLM-4 大模型
- 自动提取合同 **19 项关键字段**：
  - 合同编号、甲乙方信息
  - 服务内容、期限、费用
  - 权利义务、违约责任
  - 争议解决方式等
- 生成智能审查报告

### 3. 合规性检查

- **主体合规** - 合同主体是否明确
- **标的明确** - 合同标的是否清晰
- **价款清晰** - 金额条款是否明确
- **履行可行** - 合同是否具备可执行性

### 4. 合同管理

- 合同列表展示与筛选
- 合同详情查看
- 合同审核（通过/驳回）
- 合同作废（软删除）
- 到期提醒功能

### 5. 数据看板

- 合同数量统计
- 应收/应付账款分析
- 月度财务数据图表
- 合同状态分布

### 6. 用户权限管理

- **管理员** - 全功能访问，合同审核权限
- **普通用户** - 上传、查看、AI 分析

---

## 技术架构

```
+-------------------------------------------------------------+
|                        前端 (Vue 3)                          |
|  +---------+  +---------+  +---------+  +-----------------+ |
|  | 合同管理 |  | 数据看板 |  | 用户登录 |  |   上传与分析     | |
|  +---------+  +---------+  +---------+  +-----------------+ |
+-------------------------------------------------------------+
                              |
                              v
                    +---------------------+
                    |    REST API (Axios)  |
                    +---------------------+
                              |
                              v
+-------------------------------------------------------------+
|                     后端 (Flask)                             |
|  +---------+  +---------+  +---------+  +-----------------+ |
|  | 用户认证 |  | 合同路由 |  | AI 服务  |  |   数据统计       | |
|  +---------+  +---------+  +---------+  +-----------------+ |
+-------------------------------------------------------------+
                              |
              +---------------+---------------+
              v                               v
    +-----------------+               +-----------------+
    |   MySQL 数据库   |               |   智谱 AI API   |
    +-----------------+               +-----------------+
```

---

## 技术栈

### 前端技术

| 技术         | 版本  | 说明                   |
| ------------ | ----- | ---------------------- |
| Vue.js       | 3.5.x | 渐进式 JavaScript 框架 |
| Vite         | 8.x   | 下一代前端构建工具     |
| Element Plus | 2.x   | Vue 3 UI 组件库        |
| Vue Router   | 5.x   | 前端路由管理           |
| Axios        | 1.x   | HTTP 请求库            |

### 后端技术

| 技术             | 版本 | 说明             |
| ---------------- | ---- | ---------------- |
| Python           | 3.8+ | 编程语言         |
| Flask            | 2.x  | 轻量级 Web 框架  |
| Flask-SQLAlchemy | 3.x  | ORM 框架         |
| Flask-CORS       | -    | 跨域资源共享     |
| PyMySQL          | -    | MySQL 数据库驱动 |

### AI 与数据处理

| 技术          | 说明           |
| ------------- | -------------- |
| 智谱 AI GLM-4 | 大语言模型 API |
| pdfplumber    | PDF 文件解析   |
| JWT           | Token 认证     |

### 数据库

- **MySQL 8.0+** - 关系型数据库

---

## 项目结构

```
contract-assistant/
+-- backend/                     # 后端 Flask 应用
|   +-- app.py                   # 应用入口
|   +-- config.py                # 配置文件
|   +-- extensions.py            # 扩展初始化
|   +-- models/                  # 数据模型
|   |   +-- __init__.py
|   |   +-- contract.py          # 合同模型
|   |   +-- user.py              # 用户模型
|   |   +-- review.py            # 审核模型
|   +-- routes/                  # 路由控制器
|   |   +-- contract.py          # 合同接口
|   |   +-- user.py              # 用户接口
|   +-- services/                # 业务逻辑
|   |   +-- ai.py                # AI 分析服务
|   |   +-- ai_service.py        # AI 服务扩展
|   |   +-- contract.py          # 合同服务
|   |   +-- file_parser.py       # 文件解析
|   +-- utils/                   # 工具函数
|   |   +-- auth.py              # 认证工具
|   +-- uploads/                 # 文件上传目录
|   +-- requirements.txt         # Python 依赖
|   +-- database.sql             # 数据库初始化脚本
|
+-- frontend/                    # 前端 Vue 应用
|   +-- src/
|   |   +-- views/               # 页面组件
|   |   |   +-- Home.vue         # 合同管理首页
|   |   |   +-- Dashboard.vue    # 数据看板
|   |   |   +-- Login.vue        # 登录页
|   |   |   +-- Upload.vue       # 上传页
|   |   |   +-- ContractList.vue # 合同列表
|   |   |   +-- Review.vue       # 审核页
|   |   +-- api/                 # API 接口
|   |   |   +-- request.js       # Axios 实例
|   |   |   +-- contract.js      # 合同 API
|   |   |   +-- user.js          # 用户 API
|   |   +-- router/              # 路由配置
|   |   |   +-- index.js
|   |   +-- layout/              # 布局组件
|   |   |   +-- Layout.vue
|   |   +-- components/          # 公共组件
|   |   +-- App.vue              # 根组件
|   |   +-- main.js              # 入口文件
|   +-- index.html
|   +-- vite.config.js
|   +-- package.json
|
+-- docs/                        # 文档目录
|   +-- 项目流程图.md
|   +-- 权限管理SQL.sql
|
+-- README.md
```

---

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 1. 克隆项目

```bash
git clone https://github.com/your-username/contract-assistant.git
cd contract-assistant
```

### 2. 数据库配置

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE contract_ai DEFAULT CHARACTER SET utf8mb4;

# 导入初始化脚本
USE contract_ai;
SOURCE backend/database.sql;
```

### 3. 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（可选）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 修改配置（app.py）
# db = SQLAlchemy()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_password@localhost/contract_ai'

# 启动服务
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 4. 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 `http://localhost:5173` 启动。

### 5. 默认账号

| 用户名 | 密码   | 角色     |
| ------ | ------ | -------- |
| admin  | 123456 | 管理员   |
| user   | 123456 | 普通用户 |

---


### 详细步骤

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端
    participant B as 后端
    participant AI as 智谱AI
    participant DB as 数据库

    U->>F: 上传合同文件 (PDF/TXT)
    F->>B: POST /upload
    B->>B: 保存文件到 uploads/
    B-->>F: 上传成功

    U->>F: 点击"AI分析"
    F->>B: GET /review
    B->>B: 解析文件内容
    B->>AI: 发送合同文本
    AI-->>B: 返回 JSON 分析结果
    B-->>F: 返回分析数据

    U->>F: 确认并保存
    F->>B: POST /save_contract
    B->>DB: INSERT INTO contracts
    DB-->>B: 保存成功
    B-->>F: 返回合同ID
    F-->>U: 操作完成
```

---

## 功能亮点

### 精准的 AI 分析

系统基于 **智谱 AI GLM-4** 大模型，能够：

- 智能识别 合同中的甲方、乙方、合同标的
- 自动提取 金额、日期、权利义务等关键信息
- 风险评估 识别潜在的法律风险点
- 合规检查 判断合同是否符合四项基本要求

### 安全的用户认证

- JWT Token 身份验证
- 角色权限控制（管理员/普通用户）
- API 请求安全验证

### 友好的用户界面

- 响应式布局设计
- 直观的操作流程
- 清晰的数据展示
- 实时状态反馈

### 强大的数据统计

- 合同数量、状态统计
- 应收/应付账款管理
- 月度财务数据分析
- 合同到期预警

---

## 数据库设计

### 用户表 (users)

| 字段       | 类型         | 说明              |
| ---------- | ------------ | ----------------- |
| id         | INT          | 主键自增          |
| username   | VARCHAR(50)  | 用户名            |
| password   | VARCHAR(255) | 密码              |
| role       | VARCHAR(20)  | 角色 (admin/user) |
| created_at | DATETIME     | 创建时间          |

### 合同表 (contracts)

| 字段                | 类型         | 说明         |
| ------------------- | ------------ | ------------ |
| id                  | INT          | 主键自增     |
| contract_number     | VARCHAR(100) | 合同编号     |
| name                | VARCHAR(255) | 合同名称     |
| party_a             | VARCHAR(255) | 甲方         |
| party_b             | VARCHAR(255) | 乙方         |
| service_content     | TEXT         | 服务内容     |
| service_period      | VARCHAR(255) | 服务期限     |
| service_fee         | VARCHAR(100) | 服务费用     |
| payment_method      | VARCHAR(255) | 支付方式     |
| party_a_rights      | TEXT         | 甲方权利义务 |
| party_b_rights      | TEXT         | 乙方权利义务 |
| acceptance_standard | TEXT         | 验收标准     |
| liability           | TEXT         | 违约责任     |
| dispute_resolution  | TEXT         | 争议解决     |
| signing_date        | DATE         | 签署日期     |
| expire_date         | DATE         | 到期日期     |
| content             | LONGTEXT     | 合同原文     |
| result              | TEXT         | AI 分析结论  |
| subject_ok          | BOOLEAN      | 主体合规     |
| object_clear        | BOOLEAN      | 标的明确     |
| price_clear         | BOOLEAN      | 价款清晰     |
| performable         | BOOLEAN      | 履行可行     |
| is_compliant        | BOOLEAN      | 整体合规     |
| status              | VARCHAR(20)  | 审核状态     |
| reject_reason       | TEXT         | 驳回理由     |
| is_void             | BOOLEAN      | 是否作废     |
| created_at          | DATETIME     | 创建时间     |

---

## API 文档

### 认证相关

| 方法 | 路径            | 说明     |
| ---- | --------------- | -------- |
| POST | `/api/login`    | 用户登录 |
| POST | `/api/register` | 用户注册 |

### 合同相关

| 方法 | 路径                    | 说明             |
| ---- | ----------------------- | ---------------- |
| POST | `/api/upload`           | 上传合同文件     |
| GET  | `/api/review`           | AI 分析合同      |
| GET  | `/api/contracts`        | 获取合同列表     |
| POST | `/api/save_contract`    | 保存合同到数据库 |
| POST | `/api/contract/approve` | 审核合同         |
| POST | `/api/void_contract`    | 作废合同         |
| GET  | `/api/stats`            | 获取统计数据     |
