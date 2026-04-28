实习生周工作时长看板 - 部署指南

一、项目完成内容
================

已创建完整的数据看板应用，包括：

1. App.py - Streamlit 主应用程序
   - 数据处理：Excel 宽表转长表
   - 5 个交互式可视化
   - 自动生成业务洞察
   - KPI 仪表板
   - CSV 导出功能

2. 配置文件
   - requirements.txt - Python 依赖
   - .streamlit/config.toml - 应用配置
   - .gitignore - Git 配置
   - README.md - 英文文档

二、本地运行（仅需 3 步）
=======================

1. 安装依赖：
   pip install -r requirements.txt

2. 启动应用：
   streamlit run App.py

3. 打开浏览器：
   http://localhost:8501

三、在线部署（推荐方案）
======================

使用 Streamlit Community Cloud（免费！）

步骤：
1. 代码上传到 GitHub
2. 访问 https://share.streamlit.io
3. 选择仓库和 main file (App.py)
4. 点击 Deploy
5. 获得公开 URL，分享给团队

效果：
- 无需安装，直接打开 URL 使用
- 自动扩展，支持多人同时使用
- 云端运行，不占用本地资源

四、使用流程
===========

1. 上传 Excel 文件（侧边栏）
2. 选择要分析的部门和周数
3. 查看 5 个可视化图表
4. 阅读自动生成的业务洞察
5. 导出数据（CSV）

五、Excel 文件格式
================

列 1: Week (数字：1, 2, 3...)
列 2: Date (文本： 2024-01-01 to 2024-01-07)
列 3+: 部门名称 (PPM1, DP, PPM2, STA, PEH, IP1, IP2)

单元格值：该部门该周总工时（数字）

自动识别规则：
- 工时 > 32 小时 → 标记为 Busy（繁忙）
- 其他 → Normal（正常）

六、部署对比
===========

                | 本地运行  | 云部署 (推荐)
成本            | 免费      | 免费
访问方式        | localhost | 公网 URL
需要安装        | 需要      | 不需要
性能            | 电脑性能  | 云服务器
可靠性          | 中等      | 高
多人访问        | 不支持    | 完全支持

七、常见问题
===========

Q: 云部署需要付费吗？
A: 不需要！Streamlit Community Cloud 完全免费

Q: 支持多少用户同时访问？
A: 理论无限，一般不会有限制

Q: 数据会保存在云端吗？
A: 不会。上传的数据仅在该会话有效，刷新页面需重新上传

Q: 如何修改 Busy 的 32 小时阈值？
A: 编辑 App.py 中的数字 32

Q: 能否添加数据库存储？
A: 可以，需要修改 App.py 和购买数据库服务

八、技术栈
==========

- Streamlit: Web 应用框架
- Pandas: 数据处理
- Plotly: 交互式图表
- openpyxl: Excel 读取

九、文件结构
===========

e:\实习生工作时长可视化\
├── App.py                              (主应用)
├── requirements.txt                    (依赖)
├── .streamlit/config.toml              (配置)
├── .gitignore                          (Git 配置)
├── README.md                           (英文文档)
├── DEPLOYMENT_CN.md                    (本文档)
└── Weekly_Summary_Visualisation.xlsx   (示例数据)

十、下一步
=========

立即开始：
1. 本地测试：streamlit run App.py
2. 准备数据：格式化 Excel 文件
3. 云端部署：GitHub + Streamlit Cloud
4. 分享 URL：给团队使用

问题反馈/改进需求：联系开发团队

---
创建日期：2026-04-27
版本：1.0
