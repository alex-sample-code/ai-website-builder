# AI 官网建站 SaaS 平台 — 产品需求文档 (PRD)

## 1. 项目概述

### 1.1 项目背景

中小企业在建设官方网站时面临技术门槛高、设计成本大、开发周期长等痛点。传统建站方式（外包开发或自建团队）成本高昂，而现有 SaaS 建站平台（如 Wix、Squarespace）虽降低了门槛，但仍需用户花费大量时间手动编排页面。

参考 Shoplazza 在电商领域推出的 AI Store Builder —— 用户通过一句话即可生成完整店铺，本项目将此能力迁移到**企业官网**场景：通过 AI Agent 对话式引导，结合预置行业模板，一键生成专业的企业官方网站，同时提供可视化编辑器供用户精细调整。

### 1.2 产品定位

**面向中小企业的 AI 驱动官网建站 SaaS 平台**

- **核心价值**：AI 对话生成整站 + 可视化编辑器微调 + 一键发布独立网站
- **目标用户**：中小企业主、市场/品牌负责人、初创团队
- **差异化**：对话式 AI 生成（非模板填充）、发布即上线（含自定义域名）、无需任何技术背景

### 1.3 核心能力

1. **AI 对话建站**：上传企业介绍或通过对话描述需求，AI 生成完整官网
2. **可视化编辑器**：基于 GrapesJS 的拖拽式页面编辑器，用户手动微调
3. **一键发布**：生成静态站点部署到 CDN，支持自定义域名
4. **管理后台**：发布后持续管理内容、查看询盘、分析数据
5. **多租户 SaaS**：按用户隔离，支持多套餐（免费/专业/企业）

---

## 2. 用户角色与场景

### 2.1 用户角色

**平台管理员（Platform Admin）**
- 管理平台整体运营
- 用户/租户管理
- 模板库管理
- 系统配置与监控

**租户所有者（Tenant Owner）**
- 注册平台账号，创建官网
- AI 对话建站或手动建站
- 管理站点设置、域名
- 管理团队成员

**租户编辑（Tenant Editor）**
- 编辑页面内容
- 管理博客文章
- 处理询盘
- 无法修改站点设置和域名

**租户查看者（Tenant Viewer）**
- 查看数据统计
- 查看询盘记录
- 只读权限

### 2.2 核心用户场景

**场景一：AI 对话建站（主流程）**

> 用户张总经营一家机械制造公司，需要一个展示产品和公司实力的官网。他注册平台后，上传了公司介绍 PDF，AI 通过 3-5 轮对话确认行业、风格偏好和栏目需求后，30 秒内生成包含首页、关于我们、产品展示、新闻动态、联系我们等 5 个页面的完整官网。张总预览后觉得"产品展示"页面需要调整布局，进入编辑器拖拽调整后，一键发布到 www.zhangmachinery.com。

**场景二：手动编辑建站**

> 设计师小李不信任 AI 生成的效果，选择从空白模板开始，使用可视化编辑器逐页搭建客户的官网。她从组件库拖入 Hero Banner、产品卡片、团队介绍等组件，自定义颜色和字体后发布。

**场景三：发布后日常管理**

> 张总的官网上线后，每周有 3-5 条通过联系表单提交的询盘。他登录管理后台查看询盘、标记跟进状态。每月发布 1-2 篇公司新闻博客。每季度让 AI 帮忙优化一下首页文案。

---

## 3. 功能需求

### 3.1 功能全景（按模块）

**模块一：用户认证与租户管理**
- 用户注册/登录（邮箱 + 手机号 + 第三方 OAuth）
- 租户自动创建（注册即创建租户）
- 套餐管理（免费版/专业版/企业版）
- 团队成员邀请与权限管理

**模块二：AI Builder（AI 对话建站）**
- 对话式交互界面
- 企业介绍文档上传与解析（PDF/Word/TXT）
- 多轮对话引导信息收集
- 整站代码生成（HTML/CSS/JS）
- 生成结果实时预览
- 不满意可重新生成或基于反馈迭代

**模块三：可视化编辑器**
- GrapesJS 集成，拖拽式页面编辑
- 组件库（Header、Hero、Feature、Gallery、Team、Pricing、Footer 等）
- 行业模板库（预置 10-20 套）
- 多页面管理
- 响应式预览（桌面/平板/手机）
- 样式编辑（颜色、字体、间距）
- 资源管理器（图片/视频上传）
- 撤销/重做
- 自定义代码块（高级用户）

**模块四：站点发布**
- 一键发布到 CDN
- 发布前全站预览
- 自定义域名绑定（DNS 配置引导）
- SSL 证书自动签发
- 发布版本管理与回滚

**模块五：管理后台（发布后）**
- 概览仪表盘（PV/UV、询盘数、站点状态）
- 内容快速编辑（不进编辑器即可改文字/图片）
- 博客管理（文章 CRUD、分类/标签、定时发布）
- 询盘管理（表单提交列表、状态管理、导出、通知）
- 站点设置（Logo/Favicon、导航菜单、页脚、SEO）
- 域名管理（绑定/解绑、DNS 状态、SSL 状态）
- 数据统计（流量趋势、页面排行、来源分析、设备分布）
- 团队管理（邀请/移除成员、角色权限）
- 操作日志
- 第三方集成配置（统计工具、在线客服、Webhook）
- 自定义表单构建器
- AI 助手（写博客、优化 SEO、翻译内容）

**模块六：平台管理（Admin）**
- 租户列表与管理
- 模板库管理（上架/下架/排序）
- 系统监控与告警
- AI 用量统计与成本控制
- 全局配置

### 3.2 AI Builder 详细流程

**Step 1：创建项目**
用户选择"AI 建站"入口，可选择：
- 上传企业介绍文档（PDF/Word/TXT）
- 直接开始对话

**Step 2：AI 对话引导**
AI 根据上传的文档（或从零开始），通过多轮对话收集以下信息：
- 公司名称、行业、主营业务
- 官网目标（品牌展示/获客/招聘/综合）
- 风格偏好（现代简约/科技感/传统稳重/活力创意）
- 色彩偏好（可参考企业 Logo 配色）
- 需要的栏目页面（首页/关于/产品/新闻/联系/招聘/案例...）
- 特殊需求（多语言？在线客服？特定功能？）

**Step 3：AI 生成整站**
基于收集的信息 + 最匹配的行业模板，调用 Bedrock Claude Sonnet 4.6 生成：
- 所有页面的 HTML/CSS 代码
- 占位图片（使用 Unsplash/Pexels 免费图库）
- 示例文案（基于企业介绍生成）
- SEO 元数据

**Step 4：预览与确认**
- 全站实时预览（桌面 + 手机视图）
- 用户可反馈"整体不满意 → 重新生成"或"某个部分需要调整 → AI 局部修改"
- 满意后进入编辑器做精细调整，或直接发布

### 3.3 可视化编辑器组件库

**布局组件**
- Section（通栏容器）
- Container（居中容器）
- Grid（2/3/4 列网格）
- Flexbox 布局

**导航组件**
- Header（Logo + 导航菜单 + CTA 按钮）
- Footer（公司信息 + 链接 + 社交图标 + 版权）
- Sidebar 导航

**内容组件**
- Hero Banner（大图 + 标题 + 副标题 + CTA）
- Feature Grid（特性/优势展示，图标 + 文字）
- 产品/服务卡片（图片 + 标题 + 描述 + 链接）
- 团队介绍（头像 + 姓名 + 职位 + 简介）
- 时间线（公司历程/里程碑）
- 数字统计（动态计数器）
- 客户评价/Testimonial
- 合作伙伴 Logo 墙
- 案例展示（图文混排）
- FAQ 手风琴
- Pricing Table 定价表
- CTA（Call to Action 行动号召）

**媒体组件**
- 图片（单图/图集/Lightbox）
- 视频嵌入（YouTube/Bilibili/自托管）
- 图标库（Font Awesome / Material Icons）
- 地图嵌入（高德/Google Maps）

**表单组件**
- 联系表单（预置模板）
- 自定义表单（可配置字段）
- 订阅表单（邮箱收集）

**博客组件**
- 文章列表
- 文章详情
- 分类/标签导航
- 最新文章侧边栏

### 3.4 自定义域名流程

**用户操作流程：**

1. 用户在管理后台"域名管理"中输入自己的域名（如 www.example.com）
2. 系统返回一条 CNAME 记录值（如 d1234.cloudfront.net）
3. 用户到自己的域名注册商（如 GoDaddy/阿里云）添加 CNAME 解析
4. 系统自动检测 DNS 生效 → 自动签发 SSL 证书
5. 域名绑定完成，用户网站可通过自定义域名访问

**系统后台流程：**

1. 调用 CloudFront API 创建 Distribution Tenant（继承 Multi-Tenant Distribution 模板）
2. Distribution Tenant 配置 origin 指向 S3 对应租户路径
3. CloudFront 自动为域名签发管理证书
4. 定时任务轮询检测 DNS 配置状态
5. DNS 验证通过后更新状态为"已生效"

### 3.5 套餐设计（参考）

**免费版**
- 1 个站点
- 平台子域名（xxx.yourplatform.com）
- 5 个页面
- 基础组件
- 3 次 AI 生成
- 带平台品牌标识

**专业版（$19/月）**
- 1 个站点
- 自定义域名 + SSL
- 无限页面
- 全部组件
- 博客功能
- 表单询盘
- 数据统计
- 50 次/月 AI 生成
- 无品牌标识

**企业版（$49/月）**
- 3 个站点
- 自定义域名 + SSL
- 全部功能
- 团队协作（5 人）
- 高级统计
- 无限 AI 生成
- 优先客服
- 自定义代码注入

---

## 4. 技术架构

### 4.1 总体架构

本平台采用前后端分离架构，部署在 AWS 上，核心组件包括：

- **前端**：React + GrapesJS（编辑器）+ 管理后台 SPA
- **后端**：Python (FastAPI)，部署在 EKS
- **AI 引擎**：Amazon Bedrock Claude Sonnet 4.6
- **数据库**：Amazon RDS PostgreSQL（业务数据）+ DynamoDB（统计打点）
- **存储**：Amazon S3（静态站点 + 资源文件）
- **CDN**：CloudFront Multi-Tenant Distribution（租户站点分发 + 自定义域名）
- **认证**：Amazon Cognito（用户认证 + 多租户身份）
- **消息通知**：Amazon SES（邮件通知）+ SNS（Webhook 推送）

### 4.2 架构分层

**接入层**
- CloudFront → ALB → EKS（平台前端 + API）
- CloudFront Multi-Tenant Distribution → S3（用户发布的网站）

**应用层（EKS）**
- API Gateway Service：统一入口，认证、限流、路由
- AI Builder Service：对话管理、Prompt 编排、调用 Bedrock
- Site Service：站点/页面 CRUD、GrapesJS 数据管理
- Publish Service：静态站点生成、S3 上传、CloudFront Tenant 管理
- Form Service：表单定义 + 表单提交处理
- Blog Service：博客 CRUD + 渲染
- Analytics Service：PV 收集 + 聚合统计
- Admin Service：平台管理功能

**数据层**
- RDS PostgreSQL：核心业务数据（租户、站点、页面、表单、博客）
- DynamoDB：访问统计打点（高写入吞吐）
- S3：用户上传资源 + 发布的静态站点
- ElastiCache Redis：Session 缓存、AI 对话上下文、发布锁

**基础设施层**
- EKS（应用运行）
- CloudFront（CDN 分发）
- Route 53（DNS 管理）
- Cognito（认证）
- SES / SNS（通知）
- CloudWatch（监控告警）
- ECR（容器镜像仓库）

### 4.3 关键架构决策

**为什么选择 Python (FastAPI)？**
- 项目核心是 AI 生成，Python 的 AI 生态（boto3、LangChain、HTML 处理库）最成熟
- 性能瓶颈在 Bedrock API 延迟（秒级），非服务端计算
- FastAPI 原生 async 支持，适合 I/O 密集场景
- 开发效率高，适合快速迭代产品

**为什么选择 GrapesJS？**
- MIT 协议，商业 SaaS 无合规风险
- 最成熟的开源嵌入式页面构建器（21K+ GitHub Stars）
- 天然支持"加载 HTML → 可视化编辑 → 导出 HTML"流程
- Storage API 可对接任意后端
- Block/Component 系统支持自定义组件库
- 插件生态丰富

**为什么选择 CloudFront Multi-Tenant Distribution？**
- 专为 SaaS 多租户自定义域名场景设计
- 自动化 SSL 证书签发与续签
- 每个 Tenant 可独立配置 Origin Path
- API 程序化管理（CreateDistributionTenant / DeleteDistributionTenant）
- 定价合理：前 10 个免费，11-200 个 $20/月，200+ 个 $0.10/tenant/月

**为什么选择 EKS？**
- 多服务微服务架构，K8s 原生编排
- 弹性伸缩（HPA / Karpenter）
- 滚动更新、蓝绿部署
- 与 AWS 生态深度集成（IAM、CloudWatch、ALB Ingress）

### 4.4 AI Builder 技术设计

**模型选择**
- 主模型：Claude Sonnet 4.6（Bedrock Cross-Region Inference）
  - Model ID：`us.anthropic.claude-sonnet-4-6`
  - Context Window：1M tokens
  - Max Output：64K tokens
- 用途：对话引导 + 整站代码生成 + 博客写作 + SEO 优化

**Prompt 策略**
- System Prompt：定义 AI 为专业网站设计师角色，约束输出格式
- Few-shot 示例：预置 3-5 个行业生成示例
- 模板注入：选定行业模板的 HTML 骨架作为参考
- 用户上下文：企业介绍文档 + 对话历史 + 风格偏好
- 输出约束：生成 GrapesJS 兼容的 HTML，包含语义化标签和 data 属性

**生成流程**
1. 对话阶段：多轮对话收集信息 → 结构化为 JSON config
2. 生成阶段：config + 模板骨架 + System Prompt → Bedrock API → 完整 HTML/CSS
3. 后处理：HTML 校验 → 图片占位替换（Unsplash API）→ GrapesJS 格式适配
4. 加载到前端 GrapesJS 编辑器进行预览

**流式输出**
- AI 生成过程使用 Bedrock Converse Stream API
- 通过 WebSocket / SSE 实时推送生成进度到前端
- 前端实时渲染预览

### 4.5 发布系统技术设计

**静态站点生成流程**

1. 后端从数据库读取所有 Pages 的 GrapesJS JSON 数据
2. 调用 GrapesJS Headless（Node.js 服务）导出每个 Page 的 HTML + CSS
3. 注入公共元素：导航菜单、页脚、SEO meta、统计代码、自定义 JS/CSS
4. 处理资源引用：图片/字体 URL 替换为 CDN 路径
5. 生成 sitemap.xml、robots.txt、favicon
6. 打包上传到 S3：`s3://sites-bucket/{tenant_id}/{site_id}/`
7. 创建/更新 CloudFront Distribution Tenant
8. 触发 CloudFront Invalidation 刷新缓存

**动态 API 层**

发布后的网站仍需少量动态功能，通过 CloudFront 的 `/api/*` 路径规则转发到后端：
- `POST /api/v1/forms/{site_id}/submit` — 表单提交
- `GET /api/v1/blogs/{site_id}/posts` — 博客列表（用于动态加载）
- `POST /api/v1/analytics/{site_id}/track` — PV 打点

### 4.6 多租户架构设计

**隔离模型：Pool 模式（共享基础设施 + 数据隔离）**

- 所有租户共享同一套 EKS 集群、RDS 实例、Redis
- 数据通过 tenant_id 字段隔离（Row-Level Security）
- 每个租户的发布站点独立 S3 prefix
- 每个租户的自定义域名独立 CloudFront Distribution Tenant
- API 层通过 JWT token 中的 tenant_id 做请求级隔离

**RDS Row-Level Security 示例**

每张表都包含 tenant_id 字段，应用层通过中间件自动注入 tenant 过滤条件：
- 所有 SELECT 自动加 `WHERE tenant_id = ?`
- 所有 INSERT 自动填充 tenant_id
- 跨租户数据访问在中间件层拒绝

**资源隔离**
- S3：`s3://sites-bucket/{tenant_id}/{site_id}/`（prefix 隔离）
- CloudFront：每个租户一个 Distribution Tenant
- Cognito：同一 User Pool，通过 `custom:tenant_id` 属性区分

---

## 5. 数据库设计

### 5.1 ER 概览

本系统使用 Amazon RDS PostgreSQL 作为主数据库，DynamoDB 作为高吞吐统计存储。

核心实体关系：
- Tenant 1:N Users
- Tenant 1:N Sites
- Site 1:N Pages
- Site 1:N BlogPosts
- Site 1:N FormDefinitions
- FormDefinition 1:N FormSubmissions
- Site 1:N Assets
- Site 1:1 SiteSettings
- Site 1:N SiteVersions
- Site 1:N NavMenus

### 5.2 核心表结构

#### 租户与用户

**tenants 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| name | VARCHAR(255) | 公司/组织名称 |
| plan | VARCHAR(50) | 套餐类型 (free/pro/enterprise) |
| custom_domain | VARCHAR(255) | 用户自定义域名 |
| cf_tenant_id | VARCHAR(255) | CloudFront Distribution Tenant ID |
| cf_connection_group_id | VARCHAR(255) | CloudFront Connection Group ID |
| domain_status | VARCHAR(50) | 域名状态 (pending/dns_configured/ssl_provisioning/active/error) |
| status | VARCHAR(50) | 租户状态 (active/suspended/deleted) |
| ai_quota_used | INTEGER | 当月 AI 生成使用次数 |
| ai_quota_limit | INTEGER | 当月 AI 生成配额 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**users 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| tenant_id | UUID | 外键 → tenants |
| email | VARCHAR(255) | UNIQUE |
| cognito_sub | VARCHAR(255) | Cognito 用户 ID |
| name | VARCHAR(255) | 用户名 |
| role | VARCHAR(50) | 角色 (owner/editor/viewer) |
| avatar_url | VARCHAR(500) | 头像 URL |
| last_login_at | TIMESTAMP | 最后登录时间 |
| created_at | TIMESTAMP | 创建时间 |

**team_invitations 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| tenant_id | UUID | 外键 → tenants |
| email | VARCHAR(255) | 被邀请邮箱 |
| role | VARCHAR(50) | 角色 |
| token | VARCHAR(255) | UNIQUE, 邀请链接 token |
| status | VARCHAR(50) | pending/accepted/expired |
| invited_by | UUID | 外键 → users |
| created_at | TIMESTAMP | 创建时间 |
| expires_at | TIMESTAMP | 过期时间 |

#### 站点与页面

**sites 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| tenant_id | UUID | 外键 → tenants |
| name | VARCHAR(255) | 站点名称 |
| status | VARCHAR(50) | draft/published/offline |
| template_id | VARCHAR(100) | 使用的模板 ID |
| current_version_id | UUID | 外键 → site_versions, 当前生效版本 |
| published_at | TIMESTAMP | 发布时间 |
| publish_url | VARCHAR(500) | 发布 URL |
| settings_snapshot | JSONB | 快速访问的站点设置 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**pages 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| slug | VARCHAR(255) | URL 路径 (/about, /contact) |
| title | VARCHAR(255) | 页面标题 |
| seo_meta | JSONB | {title, description, og_image, og_title, keywords} |
| grapesjs_data | JSONB | GrapesJS 编辑器完整 JSON |
| html | TEXT | 导出的 HTML |
| css | TEXT | 导出的 CSS |
| js | TEXT | 导出的 JS |
| is_homepage | BOOLEAN | 是否首页 |
| sort_order | INTEGER | 排序 |
| status | VARCHAR(50) | active/hidden/deleted |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**site_versions 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| version_number | INTEGER | 自增版本号 |
| snapshot | JSONB | 完整的 pages + settings + nav 快照 |
| s3_prefix | VARCHAR(500) | 该版本的 S3 路径 |
| published_by | UUID | 外键 → users |
| published_at | TIMESTAMP | 发布时间 |
| is_current | BOOLEAN | 是否当前生效版本 |
| notes | TEXT | 发布备注 |

#### 站点设置与导航

**site_settings 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites, UNIQUE |
| logo_url | VARCHAR(500) | Logo URL |
| favicon_url | VARCHAR(500) | Favicon URL |
| company_name | VARCHAR(255) | 公司名 |
| company_address | TEXT | 公司地址 |
| company_phone | VARCHAR(50) | 电话 |
| company_email | VARCHAR(255) | 邮箱 |
| social_links | JSONB | {wechat, weibo, linkedin, twitter, facebook, instagram} |
| analytics_id | VARCHAR(255) | Google Analytics / 百度统计 ID |
| custom_head_code | TEXT | 注入 head 的自定义代码 |
| custom_body_code | TEXT | 注入 body 末尾的自定义代码 |
| color_scheme | JSONB | {primary, secondary, accent, background, text} |
| font_family | VARCHAR(255) | 字体 |
| updated_at | TIMESTAMP | 更新时间 |

**nav_menus 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| position | VARCHAR(50) | header/footer/sidebar |
| items | JSONB | 嵌套菜单结构 [{label, url, target, children: [...]}] |
| updated_at | TIMESTAMP | 更新时间 |

#### 资源管理

**assets 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| tenant_id | UUID | 外键 → tenants |
| site_id | UUID | 外键 → sites, 可为空 |
| filename | VARCHAR(255) | 文件名 |
| s3_key | VARCHAR(500) | S3 路径 |
| cdn_url | VARCHAR(500) | CDN URL |
| content_type | VARCHAR(100) | MIME 类型 |
| size_bytes | BIGINT | 文件大小 |
| width | INTEGER | 图片宽度 |
| height | INTEGER | 图片高度 |
| folder | VARCHAR(255) | 分组文件夹 |
| created_at | TIMESTAMP | 创建时间 |

#### AI 生成

**ai_sessions 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| tenant_id | UUID | 外键 → tenants |
| site_id | UUID | 外键 → sites |
| conversation | JSONB | 对话历史 |
| company_info | TEXT | 用户上传的企业介绍 |
| company_info_s3_key | VARCHAR(500) | 原始文档 S3 路径 |
| generated_config | JSONB | AI 提取的结构化配置 |
| generated_pages | JSONB | AI 生成的页面列表 |
| model_id | VARCHAR(255) | 使用的模型 ID |
| input_tokens | INTEGER | 输入 token 数 |
| output_tokens | INTEGER | 输出 token 数 |
| generation_time_ms | INTEGER | 生成耗时 |
| status | VARCHAR(50) | in_progress/completed/failed |
| created_at | TIMESTAMP | 创建时间 |

#### 博客

**blog_posts 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| category_id | UUID | 外键 → blog_categories |
| title | VARCHAR(255) | 标题 |
| slug | VARCHAR(255) | URL slug |
| content | TEXT | Markdown 内容 |
| content_html | TEXT | 渲染后的 HTML |
| excerpt | VARCHAR(500) | 摘要 |
| cover_image | VARCHAR(500) | 封面图 S3 key |
| seo_title | VARCHAR(255) | SEO 标题 |
| seo_description | VARCHAR(500) | SEO 描述 |
| author_name | VARCHAR(255) | 作者 |
| status | VARCHAR(50) | draft/published/archived |
| published_at | TIMESTAMP | 发布时间 |
| scheduled_at | TIMESTAMP | 定时发布时间 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**blog_categories 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| name | VARCHAR(255) | 分类名 |
| slug | VARCHAR(255) | URL slug |
| sort_order | INTEGER | 排序 |

**blog_tags 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| name | VARCHAR(100) | 标签名 |
| slug | VARCHAR(100) | URL slug |

**blog_post_tags 表（多对多）：**
| 字段 | 类型 | 说明 |
|------|------|------|
| post_id | UUID | 外键 → blog_posts |
| tag_id | UUID | 外键 → blog_tags |
| | | PRIMARY KEY (post_id, tag_id) |

#### 表单

**form_definitions 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| name | VARCHAR(255) | 表单名称 |
| fields | JSONB | 字段定义 [{name, type, label, required, placeholder, options}] |
| notification_emails | TEXT[] | 通知邮箱列表 |
| webhook_url | VARCHAR(500) | Webhook 推送地址 |
| success_message | VARCHAR(500) | 提交成功提示语 |
| is_enabled | BOOLEAN | 是否启用 |
| created_at | TIMESTAMP | 创建时间 |

**form_submissions 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| form_def_id | UUID | 外键 → form_definitions |
| page_id | UUID | 外键 → pages, 来自哪个页面 |
| data | JSONB | 提交的表单数据 |
| status | VARCHAR(50) | new/read/replied/archived |
| replied_at | TIMESTAMP | 回复时间 |
| notes | TEXT | 内部备注 |
| ip_address | VARCHAR(50) | IP 地址 |
| user_agent | VARCHAR(500) | User Agent |
| submitted_at | TIMESTAMP | 提交时间 |

#### 第三方集成

**integrations 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| site_id | UUID | 外键 → sites |
| type | VARCHAR(50) | google_analytics/baidu_tongji/crisp/tidio/wechat/custom_webhook |
| config | JSONB | 各集成的配置参数 |
| is_enabled | BOOLEAN | 是否启用 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

#### 操作日志

**audit_logs 表：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| tenant_id | UUID | 外键 → tenants |
| user_id | UUID | 外键 → users |
| action | VARCHAR(100) | 操作类型 |
| resource_type | VARCHAR(50) | 资源类型 |
| resource_id | UUID | 资源 ID |
| details | JSONB | 变更内容摘要 |
| ip_address | VARCHAR(50) | IP 地址 |
| created_at | TIMESTAMP | 创建时间 |

### 5.3 DynamoDB 表（高吞吐统计）

**page_views 表**
| 字段 | 类型 | 说明 |
|------|------|------|
| PK | String | site_id |
| SK | String | timestamp#visitor_id |
| page_path | String | 页面路径 |
| referrer | String | 来源 |
| user_agent | String | UA |
| country | String | 国家 |
| device_type | String | desktop/mobile/tablet |
| TTL | Number | created_at + 90 天（自动过期） |

**page_view_daily 表（聚合）**
| 字段 | 类型 | 说明 |
|------|------|------|
| PK | String | site_id |
| SK | String | date#page_path |
| pv_count | Number | PV 数 |
| uv_count | Number | UV 数 |

通过 DynamoDB Stream + Lambda 每小时聚合。

### 5.4 关键索引

```sql
-- tenants
CREATE INDEX idx_tenants_custom_domain ON tenants(custom_domain) WHERE custom_domain IS NOT NULL;
CREATE INDEX idx_tenants_status ON tenants(status);

-- sites
CREATE INDEX idx_sites_tenant_id ON sites(tenant_id);
CREATE INDEX idx_sites_status ON sites(status);

-- pages
CREATE INDEX idx_pages_site_id ON pages(site_id);
CREATE UNIQUE INDEX idx_pages_slug ON pages(site_id, slug);

-- blog_posts
CREATE INDEX idx_blog_posts_site_id ON blog_posts(site_id, status, published_at DESC);
CREATE UNIQUE INDEX idx_blog_posts_slug ON blog_posts(site_id, slug);
CREATE INDEX idx_blog_posts_scheduled ON blog_posts(scheduled_at) WHERE status = 'draft' AND scheduled_at IS NOT NULL;

-- form_submissions
CREATE INDEX idx_form_submissions_site ON form_submissions(site_id, submitted_at DESC);
CREATE INDEX idx_form_submissions_status ON form_submissions(site_id, status);

-- audit_logs
CREATE INDEX idx_audit_logs_tenant ON audit_logs(tenant_id, created_at DESC);
```

---

## 6. API 设计

### 6.1 API 总览

所有 API 遵循 RESTful 风格，基础路径 `/api/v1/`，认证使用 Bearer Token (JWT from Cognito)。

### 6.2 认证相关

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/login | 用户登录 |
| POST | /api/v1/auth/refresh | 刷新 Token |
| POST | /api/v1/auth/forgot-password | 忘记密码 |
| GET | /api/v1/auth/me | 获取当前用户信息 |

### 6.3 AI Builder

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/ai/sessions | 创建 AI 建站会话 |
| POST | /api/v1/ai/sessions/{id}/message | 发送对话消息 |
| POST | /api/v1/ai/sessions/{id}/upload | 上传企业介绍文档 |
| POST | /api/v1/ai/sessions/{id}/generate | 触发整站生成 |
| GET | /api/v1/ai/sessions/{id}/status | 查询生成状态 |
| POST | /api/v1/ai/sessions/{id}/regenerate | 重新生成 |

### 6.4 站点管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/sites | 获取站点列表 |
| POST | /api/v1/sites | 创建站点 |
| GET | /api/v1/sites/{id} | 获取站点详情 |
| PUT | /api/v1/sites/{id} | 更新站点信息 |
| DELETE | /api/v1/sites/{id} | 删除站点 |

### 6.5 页面管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/sites/{site_id}/pages | 获取页面列表 |
| POST | /api/v1/sites/{site_id}/pages | 创建页面 |
| GET | /api/v1/sites/{site_id}/pages/{id} | 获取页面详情（含 GrapesJS 数据） |
| PUT | /api/v1/sites/{site_id}/pages/{id} | 更新页面 |
| PUT | /api/v1/sites/{site_id}/pages/{id}/content | 快速更新页面内容 |
| DELETE | /api/v1/sites/{site_id}/pages/{id} | 删除页面 |
| PUT | /api/v1/sites/{site_id}/pages/reorder | 页面排序 |

### 6.6 发布管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/sites/{site_id}/publish | 发布站点 |
| GET | /api/v1/sites/{site_id}/versions | 获取发布版本历史 |
| POST | /api/v1/sites/{site_id}/versions/{id}/rollback | 回滚到指定版本 |
| GET | /api/v1/sites/{site_id}/preview | 生成预览链接 |

### 6.7 域名管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/sites/{site_id}/domain | 绑定自定义域名 |
| GET | /api/v1/sites/{site_id}/domain | 获取域名状态 |
| DELETE | /api/v1/sites/{site_id}/domain | 解绑域名 |
| POST | /api/v1/sites/{site_id}/domain/verify | 触发 DNS 验证 |

### 6.8 站点设置

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/sites/{site_id}/settings | 获取站点设置 |
| PUT | /api/v1/sites/{site_id}/settings | 更新站点设置 |
| GET | /api/v1/sites/{site_id}/nav-menus | 获取导航菜单 |
| PUT | /api/v1/sites/{site_id}/nav-menus | 更新导航菜单 |

### 6.9 资源管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/sites/{site_id}/assets | 获取资源列表 |
| POST | /api/v1/sites/{site_id}/assets/upload | 上传资源（返回 S3 预签名 URL） |
| DELETE | /api/v1/sites/{site_id}/assets/{id} | 删除资源 |

### 6.10 博客管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/sites/{site_id}/blog/posts | 获取文章列表 |
| POST | /api/v1/sites/{site_id}/blog/posts | 创建文章 |
| GET | /api/v1/sites/{site_id}/blog/posts/{id} | 获取文章详情 |
| PUT | /api/v1/sites/{site_id}/blog/posts/{id} | 更新文章 |
| DELETE | /api/v1/sites/{site_id}/blog/posts/{id} | 删除文章 |
| GET | /api/v1/sites/{site_id}/blog/categories | 获取分类列表 |
| POST | /api/v1/sites/{site_id}/blog/categories | 创建分类 |
| GET | /api/v1/sites/{site_id}/blog/tags | 获取标签列表 |

### 6.11 表单管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/sites/{site_id}/forms | 获取表单定义列表 |
| POST | /api/v1/sites/{site_id}/forms | 创建表单定义 |
| PUT | /api/v1/sites/{site_id}/forms/{id} | 更新表单定义 |
| GET | /api/v1/sites/{site_id}/forms/{id}/submissions | 获取表单提交列表 |
| PUT | /api/v1/sites/{site_id}/forms/submissions/{id}/status | 更新提交状态 |
| GET | /api/v1/sites/{site_id}/forms/{id}/submissions/export | 导出 CSV |

### 6.12 数据统计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/sites/{site_id}/analytics/overview | 概览数据（PV/UV/趋势） |
| GET | /api/v1/sites/{site_id}/analytics/pages | 页面排行 |
| GET | /api/v1/sites/{site_id}/analytics/sources | 来源分析 |
| GET | /api/v1/sites/{site_id}/analytics/devices | 设备分布 |

### 6.13 团队管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/team/members | 获取团队成员列表 |
| POST | /api/v1/team/invite | 邀请成员 |
| DELETE | /api/v1/team/members/{id} | 移除成员 |
| PUT | /api/v1/team/members/{id}/role | 更改角色 |
| GET | /api/v1/team/audit-logs | 获取操作日志 |

### 6.14 集成管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/sites/{site_id}/integrations | 获取集成列表 |
| PUT | /api/v1/sites/{site_id}/integrations/{type} | 配置/更新集成 |
| DELETE | /api/v1/sites/{site_id}/integrations/{type} | 删除集成 |

### 6.15 模板库

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/templates | 获取模板列表（按行业/风格筛选） |
| GET | /api/v1/templates/{id}/preview | 模板预览 |

### 6.16 公开 API（发布后网站调用，无需认证）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/public/forms/{site_id}/submit | 表单提交（带 CORS + Rate Limit） |
| GET | /api/v1/public/blogs/{site_id}/posts | 博客文章列表 |
| GET | /api/v1/public/blogs/{site_id}/posts/{slug} | 博客文章详情 |
| POST | /api/v1/public/analytics/{site_id}/track | PV 打点（轻量） |

---

## 7. AWS 资源清单与部署架构

### 7.1 AWS 资源清单

**计算**
- Amazon EKS：应用集群（API + Worker），2-4 个 t3.large 节点起步
- ECR：容器镜像仓库

**数据库**
- Amazon RDS PostgreSQL 16：业务数据，db.t4g.medium（Multi-AZ 生产环境）
- Amazon DynamoDB：统计打点数据（按需模式）
- Amazon ElastiCache Redis 7：Session 缓存 + AI 对话上下文 + 分布式锁

**存储**
- Amazon S3：
  - sites-bucket：发布的静态网站文件
  - assets-bucket：用户上传的资源文件
  - templates-bucket：模板库资源

**网络与分发**
- Amazon CloudFront：
  - 1 个标准 Distribution：平台前端（管理后台 + 编辑器）
  - 1 个 Multi-Tenant Distribution：用户发布的网站
  - N 个 Distribution Tenant：每个用户自定义域名一个
- Application Load Balancer：EKS Ingress
- Route 53：平台域名管理

**安全与认证**
- Amazon Cognito：用户认证（User Pool + Identity Pool）
- ACM：平台 SSL 证书（Multi-Tenant Distribution 自动管理租户证书）
- IAM：服务角色与权限
- WAF：API 防护

**AI**
- Amazon Bedrock：Claude Sonnet 4.6（Cross-Region Inference Profile）

**消息与通知**
- Amazon SES：邮件通知（表单通知、团队邀请、密码重置）
- Amazon SNS：Webhook 推送

**监控**
- Amazon CloudWatch：日志 + 指标 + 告警
- AWS X-Ray：链路追踪（可选）

### 7.2 部署架构图描述

**网络层：**
```
VPC (10.0.0.0/16)
├── Public Subnets (3 AZ): ALB, NAT Gateway
└── Private Subnets (3 AZ): EKS Nodes, RDS, Redis
```

**流量路径 — 平台访问：**
```
用户浏览器 → CloudFront (Standard) → ALB → EKS (platform services)
```

**流量路径 — 发布网站访问：**
```
访客浏览器 → CloudFront Multi-Tenant Distribution (Tenant) → S3 (静态内容)
访客浏览器 → CloudFront Multi-Tenant Distribution (Tenant) → /api/* → ALB → EKS (动态 API)
```

**流量路径 — AI 生成：**
```
用户浏览器 ← WebSocket/SSE → ALB → EKS (AI Builder Service) → Bedrock API
```

### 7.3 EKS 服务部署

**Namespace:** ai-website-builder

**Deployments:**
| 服务 | Replicas | 职责 |
|------|----------|------|
| api-gateway | 2 | 统一入口、认证、限流 |
| ai-builder | 2 | AI 对话 + 生成 |
| site-service | 2 | 站点/页面 CRUD |
| publish-service | 1 | 发布 + CloudFront 管理 |
| blog-service | 1 | 博客管理 |
| form-service | 1 | 表单处理 |
| analytics-service | 1 | 统计收集 |
| worker | 1 | 异步任务（定时发布、统计聚合、DNS 检测） |

**Ingress:**
- ALB Ingress Controller
- 路由规则：`/api/*` → api-gateway service

**HPA（Horizontal Pod Autoscaler）:**
- ai-builder: 基于 CPU 80% 触发扩容
- api-gateway: 基于 RPS 触发扩容

### 7.4 成本预估（初期/中期）

**初期（0-100 租户）— 预估 $300-500/月**
| 资源 | 规格 | 月费 |
|------|------|------|
| EKS | 2x t3.large | ~$120 |
| RDS | db.t4g.medium Single-AZ | ~$50 |
| Redis | cache.t4g.micro | ~$15 |
| S3 + CloudFront | 低流量 | ~$20 |
| Bedrock | 按 token 计费 | ~$50-100 |
| 其他 | Route 53、SES、DynamoDB | ~$20 |

**中期（100-1000 租户）— 预估 $800-1500/月**
| 资源 | 规格 | 月费 |
|------|------|------|
| EKS | 4x t3.large | ~$240 |
| RDS | db.t4g.large Multi-AZ | ~$200 |
| Redis | cache.t4g.small | ~$30 |
| S3 + CloudFront | 中等流量 | ~$100-200 |
| CloudFront SaaS Manager | tenant 费用 | ~$20-100 |
| Bedrock | 按 token 计费 | ~$200-500 |
| 其他 | | ~$50 |

---

## 8. 开发里程碑与排期建议

### Phase 1：MVP 核心（4-6 周）

**目标：** 跑通 AI 建站 → 编辑 → 发布 核心流程

**Week 1-2：基础架构**
- EKS 集群搭建 + CI/CD Pipeline
- RDS + Redis 部署
- Cognito 认证集成
- 基础 API 框架（FastAPI + SQLAlchemy）
- 数据库 Schema 建表 + Migration

**Week 3-4：AI Builder + 编辑器**
- AI 对话界面前端（React）
- Bedrock 集成 + Prompt 工程（对话引导 + 整站生成）
- GrapesJS 集成 + 自定义组件库（核心 10 个组件）
- AI 生成结果加载到 GrapesJS
- 页面 CRUD API

**Week 5-6：发布系统**
- 静态站点生成 + S3 上传
- CloudFront Multi-Tenant Distribution 配置
- 自定义域名绑定流程
- 平台子域名分配（免费用户）
- 端到端联调测试

**Phase 1 交付物：** 用户可通过 AI 对话生成网站 → 编辑器调整 → 一键发布到自定义域名

### Phase 2：管理后台（3-4 周）

**Week 7-8：核心管理**
- 管理后台前端框架
- 站点设置（Logo、导航、页脚、SEO）
- 内容快速编辑（不进编辑器改文字）
- 表单定义 + 表单提交查看
- 博客基础 CRUD

**Week 9-10：增强功能**
- 数据统计（PV 收集 + 看板展示）
- 团队管理（邀请、权限）
- 发布版本历史 + 回滚
- 操作日志

### Phase 3：产品打磨（3-4 周）

**Week 11-12：模板 + 体验**
- 行业模板库（10-15 套）
- 编辑器组件库完善（20+ 组件）
- 响应式适配优化
- AI 生成质量优化（Prompt 迭代）

**Week 13-14：商业化**
- 套餐系统 + 计费（Stripe/支付宝）
- 资源配额管理
- 第三方集成配置
- 性能优化 + 安全审计
- 上线前压测

### 总计：10-14 周完成产品上线

---

## 9. 风险与应对

| 风险 | 影响 | 应对策略 | 兜底方案 |
|------|------|----------|----------|
| AI 生成质量不稳定 | 用户体验差 | 预置行业模板作为"骨架"，AI 在模板基础上填充内容 | 生成后自动校验 HTML + 组件完整性检查 |
| GrapesJS 定制深度不够 | 功能受限 | Phase 1 先用基础功能验证 | 后续考虑 Studio SDK 商业版或自研 |
| CloudFront Multi-Tenant Distribution Terraform 支持不成熟 | IaC 管理困难 | 初期用 AWS SDK 直接管理 | Distribution Tenant <200 时 API 管理可接受 |
| 多租户数据隔离漏洞 | 安全风险 | 应用层中间件强制 tenant_id 过滤 + RLS | 关键操作增加二次确认 |
| Bedrock API 延迟导致体验差 | 用户等待焦虑 | 流式输出 + 进度动画 + 分步展示 | 超时降级到推荐预置模板 |

---

## 10. 附录

### 10.1 技术选型汇总

| 类别 | 技术选型 |
|------|----------|
| 前端框架 | React 18 + TypeScript |
| 页面编辑器 | GrapesJS v0.22+ |
| UI 组件库 | Ant Design 5 / Tailwind CSS |
| 后端框架 | Python 3.12 + FastAPI |
| ORM | SQLAlchemy 2.0 |
| 任务队列 | Celery + Redis |
| 容器运行时 | Docker + EKS (Kubernetes 1.31) |
| CI/CD | GitHub Actions → ECR → ArgoCD |
| IaC | Terraform (基础设施) + Helm (K8s 资源) |
| AI 模型 | Bedrock Claude Sonnet 4.6 (`us.anthropic.claude-sonnet-4-6`) |
| 数据库 | RDS PostgreSQL 16 + DynamoDB |
| 缓存 | ElastiCache Redis 7 |
| CDN | CloudFront Multi-Tenant Distribution |
| 认证 | Amazon Cognito |
| 对象存储 | Amazon S3 |
| 邮件 | Amazon SES |
| 监控 | CloudWatch + Container Insights |

### 10.2 参考资料

- GrapesJS 官方文档：https://grapesjs.com/docs/
- CloudFront Multi-Tenant Distribution：https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-config-options.html
- AWS SaaS 多租户架构指南：https://aws.amazon.com/solutions/guidance/multi-tenant-architectures-on-aws/
- Amazon Bedrock Claude Sonnet 4.6：https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-sonnet-4-6.html
- Shoplazza AI Store Builder 参考：https://www.shoplazza.com/blog/build-online-store-quickly
