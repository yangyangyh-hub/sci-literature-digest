# sci-literature-digest

可配置、按需运行的学术文献速览技能。用户主动调用后，它在指定时间窗内检索在线发表的期刊论文，仅根据正式摘要整理带 DOI 的分类 Markdown 报告。技能本身不创建定时任务，也不附带任何人的研究配置、文献数据或 API 密钥。

## 安装

将本仓库作为 `sci-literature-digest` 文件夹放入 Codex 的个人技能目录（通常为 `~/.codex/skills/`），确保入口文件为 `sci-literature-digest/SKILL.md`。支持 Agent Skills 的其他工具也可读取该文件。

复制 [`assets/profile.example.json`](assets/profile.example.json)，按需修改主题、物种、来源、期刊筛选条件和输出目录，将**个人配置保存在技能目录之外**：

- Windows：`%APPDATA%/sci-literature-digest/profile.json`
- macOS/Linux：`~/.config/sci-literature-digest/profile.json`

也可在调用时指定配置文件，或设置 `SCI_LITERATURE_DIGEST_PROFILE` 指向私有配置。字段说明见 [`references/profile.md`](references/profile.md)。不要把真实配置、`.env`、密钥、期刊表或生成报告提交到公开仓库。

## 调用

- `$sci-literature-digest`：默认检索最近 **7 个自然日（含当天）**。
- `$sci-literature-digest 查找近两周的文献`：检索最近 14 个自然日。
- `$sci-literature-digest 查找 2026-10-01 至 2026-10-15 的文献`：严格使用指定日期范围。

请求中明确给出的条件优先于个人配置。目标篇数不足时报告实际篇数，不自动超出时间窗补齐。完成前仅核对必要的题录、摘要、研究范围、排除条件和 DOI 去重，不执行复杂的全局审核。

Web of Science Starter API 是可选来源。若要使用，可在个人配置中指定环境变量名或本机密钥文件；[`scripts/wos_search.py`](scripts/wos_search.py) 使用 Python 3 标准库查询，并仅输出公开题录，不输出密钥。其他书目来源由使用环境中可用的检索工具访问；不可用时如实记录。

## 许可

本项目采用 [MIT License](LICENSE)。
