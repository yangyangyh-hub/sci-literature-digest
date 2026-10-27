# 私有配置约定

使用 JSON 配置。优先读取用户在本次请求中指定的文件；其次读取环境变量 `SCI_LITERATURE_DIGEST_PROFILE` 指向的文件；然后读取 Windows 的 `%APPDATA%/sci-literature-digest/profile.json`，或 macOS/Linux 的 `~/.config/sci-literature-digest/profile.json`。本次消息中的明确要求总是覆盖配置。没有配置且请求缺少主题时再询问，不自行猜测研究方向。

可复制 [`assets/profile.example.json`](../assets/profile.example.json) 后修改。配置文件属于使用者本人，**不得放进将要分享或发布的技能目录**。

| 字段 | 用途 |
| --- | --- |
| `timezone` | 计算“最近一周”“近两周”等相对时间的时区；未填时使用用户当前时区。 |
| `date_window.default_days` | 未指定时间时的自然日天数，默认 7；`backfill_outside_window` 默认 `false`。 |
| `categories` | 每项有 `name`、`terms`、`target_count`；目标数不足时只报告短缺。 |
| `species` | 可选研究对象清单；空数组表示不设物种限制。 |
| `species_priority` | 可选优先研究对象，不能扩大 `species` 的纳入范围。 |
| `sources.core`、`sources.optional` | 希望尝试的检索来源；实际不可用时记录失败或未接入。 |
| `sources.publisher_targets` | 要定向查看的出版商或期刊群。 |
| `sources.china_sponsored_english_scie` | 为 `true` 时补检相关的中国机构主办英文 SCIE 期刊，并核对其主办关系。 |
| `sources.wos.api_key_env` | WoS Starter API 的环境变量名，默认 `WOS_STARTER_API_KEY`。 |
| `sources.wos.api_key_file` | 可选本地密钥文件路径；仅由查询脚本读取，不复制到技能包或报告。支持 `WOS_STARTER_API_KEY=...` 与 `APIkey: ...`。 |
| `screening.exclude_publishers`、`exclude_journals` | 硬性排除名单。 |
| `screening.journal_metrics` | 可选期刊表配置；含 `path`、`sheet`、`columns`、`required_index`、`allowed_tiers`、`min_impact_factor`、`require_match`，以及仅用于排序的 `prefer`。无表时不编造指标。 |
| `output.directory` | Markdown 输出目录；为 `null` 时默认在对话中交付。 |
| `output.filename_pattern` | 文件名模板，支持 `{start}`、`{end}`，日期写为 `YYYY-MM-DD`。 |
| `output.language` | 报告语言，例如 `zh-CN`。 |
| `output.summary_chinese_chars` | 中文摘要概述的建议字数区间；信息不足时不凑字数。 |
| `output.deduplicate_previous` | 是否与输出目录的往期报告按 DOI 去重，默认 `true`。 |
| `include_reviews` | 是否纳入综述，可设为 `false`、`true` 或 `selective`。 |

期刊表列名通过 `screening.journal_metrics.columns` 映射：`title`、`issn`、`eissn`、`index`、`tier`、`impact_factor`、`jcr_quartile`。`required_index`、`allowed_tiers` 与 `min_impact_factor` 是配置后才生效的硬条件；`prefer.jcr_quartile` 和 `prefer.impact_factor_gt` 只用于合格论文排序。`require_match=true` 时，无法可靠匹配期刊表的文章不纳入。

`sources.wos` 是可选的。用 `python scripts/wos_search.py --profile <私有配置路径> --query 'TS=(...)' --start YYYY-MM-DD --end YYYY-MM-DD --limit 20` 查询；可加 `--output <临时 JSON 路径>`。脚本只输出公开题录和检索状态，不输出密钥。API 配额、网络限制或来源不可用时继续使用其他已配置来源，并如实说明。

共享技能时只分享 `sci-literature-digest/` 文件夹或其打包文件；不要加入个人配置、`.env`、文献表、检索缓存或生成的周报。
