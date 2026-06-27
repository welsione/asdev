<p align="center">
  <img src="assets/logo.svg" alt="asdev logo" width="760" />
</p>

<p align="center">
  <strong>把复杂软件目标交给一支会调查、会拆解、会验收的 Agent 团队</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/强制多_Agent-7DD3FC?style=flat-square" alt="强制多 Agent" />
  <img src="https://img.shields.io/badge/铁律驱动-34D399?style=flat-square" alt="铁律驱动" />
  <img src="https://img.shields.io/badge/理解腐烂防护-FDE68A?style=flat-square&color=FDE68A" alt="理解腐烂防护" />
  <img src="https://img.shields.io/badge/循环模式-A7F3D0?style=flat-square" alt="循环模式" />
</p>

---

## AI 编程失败，不是因为不会写代码

而是因为太快开始写代码。你一定经历过这些：

<table>
<tr>
<td width="48" align="center">🔴</td>
<td><strong>自审冒充验收</strong> — Agent 自己写完代码，自己检查一遍，自己说"完成了"。制造者给自己的作业打分。</td>
</tr>
<tr>
<td width="48" align="center">🔴</td>
<td><strong>一次性大风险</strong> — 拿到复杂需求直接开干，写到一半发现方向错了，回滚代价巨大。</td>
</tr>
<tr>
<td align="center">🔴</td>
<td><strong>理解腐烂</strong> — Agent 循环越快产出代码，你越看不懂代码变成了什么样，最后只能"信任"或"放弃"——认知投降。</td>
</tr>
<tr>
<td align="center">🔴</td>
<td><strong>跨目标记忆缺失</strong> — 每次新会话从零开始，重复发现上次已经知道的事实。</td>
</tr>
<tr>
<td align="center">🔴</td>
<td><strong>验收标准模糊</strong> — "看起来没问题"、"应该可以"——主观标准，无法客观验证。</td>
</tr>
</table>

`asdev` 把复杂需求改造成一套目标模式工作流：先调查真实代码，再对齐不确定性，再拆成可验收任务，最后用独立 Agent 做检查和验收。它把一次性的大风险拆成多个可发现、可纠正的小风险。

---

## Before & After：用 asdev 前后，交付质量的天壤之别

> 同样的需求，同样的模型，唯一的区别是流程。

<table>
<tr>
<th width="18%" align="center">维度</th>
<th width="41%" style="background:#1c1012;">❌&nbsp; Before — 无 asdev</th>
<th width="41%" style="background:#0a1f17;">✅&nbsp; After — 有 asdev</th>
</tr>
<tr>
<td align="center"><strong>验收方式</strong></td>
<td style="background:#1c1012;color:#fca5a5;">主 Agent 写完代码后自己检查，自己说"看起来没问题，已完成"</td>
<td style="background:#0a1f17;color:#86efac;">独立 Task Acceptance Agent 逐项验证，用命令输出、测试结果、搜索证据做判断</td>
</tr>
<tr>
<td align="center"><strong>风险控制</strong></td>
<td style="background:#1c1012;color:#fca5a5;">复杂需求直接开干，失败后回滚代价巨大</td>
<td style="background:#0a1f17;color:#86efac;">先调查→再设计→再拆解→逐任务实现验收，大风险拆成多个可纠正的小风险</td>
</tr>
<tr>
<td align="center"><strong>理解透明度</strong></td>
<td style="background:#1c1012;color:#fca5a5;">循环越快，你越看不懂，只能选择"信任"或"放弃"</td>
<td style="background:#0a1f17;color:#86efac;">四层理解腐烂防护：变更摘要→推断验证→实施确认→密度预警</td>
</tr>
<tr>
<td align="center"><strong>记忆连续性</strong></td>
<td style="background:#1c1012;color:#fca5a5;">每次会话从零开始，重复发现已知事实</td>
<td style="background:#0a1f17;color:#86efac;">.record/ 沉淀 + .knowledge/ 知识条目 + STATUS.md 聚合视图，新目标继承旧经验</td>
</tr>
<tr>
<td align="center"><strong>验收标准</strong></td>
<td style="background:#1c1012;color:#fca5a5;">"看起来没问题" / "应该可以" / "逻辑上是对的"</td>
<td style="background:#0a1f17;color:#86efac;">每个任务有客观验收项，验收 Agent 用证据说话，拒绝"看起来像"的判断</td>
</tr>
<tr>
<td align="center"><strong>迭代保障</strong></td>
<td style="background:#1c1012;color:#fca5a5;">验收不通过就手动修补，没有闭环，或直接跳过标记"已确认"</td>
<td style="background:#0a1f17;color:#86efac;">FAIL→按意见返工→重提交→直到 PASS，无跳过、无降级、无绕过</td>
</tr>
</table>

---

## 三条铁律：不可绕过，不可降级

<table>
<tr>
<td width="33%" style="background:#102A2F;border-left:4px solid #FDE68A;padding:20px;vertical-align:top;">
<h3 style="color:#F8FAFC;margin-top:0;">强制记录</h3>
<p style="color:#FDE68A;font-size:15px;font-weight:700;margin:-8px 0 12px;">不落盘，不推进</p>
<p style="color:#D1FAE5;font-size:14px;">每个 Agent 产出必须写入 <code>.record/</code>，产出未落盘，下一阶段不得启动。保存失败则停止并报告，不允许跳过。</p>
<p><code style="background:#D9F99D;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase Gate</code></p>
</td>
<td width="33%" style="background:#102A2F;border-left:4px solid #FDE68A;padding:20px;vertical-align:top;">
<h3 style="color:#F8FAFC;margin-top:0;">强制验收</h3>
<p style="color:#FDE68A;font-size:15px;font-weight:700;margin:-8px 0 12px;">没有 PASS，阶段不算完成</p>
<p style="color:#D1FAE5;font-size:14px;">设计文档、任务拆解、每个任务的实现——都必须经独立验收 Agent 审查并返回 PASS。主 Agent 自审不算验收。</p>
<p><code style="background:#D9F99D;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Independent Review</code></p>
</td>
<td width="33%" style="background:#102A2F;border-left:4px solid #FDE68A;padding:20px;vertical-align:top;">
<h3 style="color:#F8FAFC;margin-top:0;">验收不过必须返工</h3>
<p style="color:#FDE68A;font-size:15px;font-weight:700;margin:-8px 0 12px;">无跳过 · 无降级 · 无绕过</p>
<p style="color:#D1FAE5;font-size:14px;">FAIL 后必须按验收意见修改再提交，循环直到 PASS。不允许以"用户确认"代替验收，不允许跳过任何验收环节。</p>
<p><code style="background:#D9F99D;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Mandatory Rework</code></p>
</td>
</tr>
</table>

> **铁律执行检查点**：每次产出落盘后，主 Agent 必须验证文件存在才推进下一步。检查点不通过 = 步骤未完成。唯一的例外：用户显式终止任务，此时记录终止原因，状态变为 `阻塞`。

---

## 四阶段交付流：从代码事实到可验收交付

<p align="center">
  <img src="assets/workflow.svg" alt="asdev 四阶段工作流" width="880" />
</p>

<table>
<tr>
<td width="25%" style="background:#102A2F;border-top:3px solid #7DD3FC;padding:16px;vertical-align:top;">
<code style="background:#7DD3FC;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase 0</code>
<h4 style="color:#F8FAFC;margin:8px 0 4px;">能力探测</h4>
<p style="color:#D1FAE5;font-size:13px;">确认多 Agent 能力<br/>读取项目规范<br/>初始化 .record/ + STATUS.md</p>
</td>
<td width="25%" style="background:#102A2F;border-top:3px solid #34D399;padding:16px;vertical-align:top;">
<code style="background:#34D399;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase 1</code>
<h4 style="color:#F8FAFC;margin:8px 0 4px;">代码调查</h4>
<p style="color:#D1FAE5;font-size:13px;">独立 Agent 找代码事实和调用链<br/>与用户对齐不确定性<br/>设计验收</p>
</td>
<td width="25%" style="background:#102A2F;border-top:3px solid #A7F3D0;padding:16px;vertical-align:top;">
<code style="background:#A7F3D0;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase 2</code>
<h4 style="color:#F8FAFC;margin:8px 0 4px;">任务拆解</h4>
<p style="color:#D1FAE5;font-size:13px;">独立 Agent 分解设计为有序任务<br/>每个任务有原因、目标、客观验收项<br/>暂停等用户确认</p>
</td>
<td width="25%" style="background:#102A2F;border-top:3px solid #FDE68A;padding:16px;vertical-align:top;">
<code style="background:#FDE68A;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">Phase 3</code>
<h4 style="color:#F8FAFC;margin:8px 0 4px;">开发验收</h4>
<p style="color:#D1FAE5;font-size:13px;">逐任务实现<br/>独立验收 Agent 逐项验证<br/>FAIL 必须返工直到 PASS</p>
</td>
</tr>
</table>

---

## 9 个独立 Agent：制造者不给自己的作业打分

<p align="center">
  <img src="assets/agents.svg" alt="asdev 多 Agent 团队" width="880" />
</p>

<table>
<tr>
<th width="50%" style="background:#102A2F;border-top:3px solid #7DD3FC;padding:12px;">
<code style="background:#7DD3FC;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">执行角色 — Standard Tier</code>
</th>
<th width="50%" style="background:#102A2F;border-top:3px solid #FDE68A;padding:12px;">
<code style="background:#FDE68A;color:#0F172A;padding:2px 8px;border-radius:4px;font-size:12px;">审查角色 — High Tier（推荐 Opus）</code>
</th>
</tr>
<tr>
<td style="background:#102A2F;padding:16px;vertical-align:top;color:#D1FAE5;font-size:14px;">
<strong style="color:#F8FAFC;">Investigator</strong><br/>
发现代码事实、调用链、影响范围<br/><br/>
<strong style="color:#F8FAFC;">Product / Design</strong><br/>
需求探索、方案设计、风险策略<br/><br/>
<strong style="color:#F8FAFC;">Development Manager</strong><br/>
任务拆解、依赖顺序、验收标准<br/><br/>
<strong style="color:#F8FAFC;">Implementation</strong><br/>
单任务实现、测试、变更说明
</td>
<td style="background:#102A2F;padding:16px;vertical-align:top;color:#D1FAE5;font-size:14px;">
<strong style="color:#F8FAFC;">Design Acceptance</strong><br/>
完整性、可行性、一致性验收<br/><br/>
<strong style="color:#F8FAFC;">Task Check</strong><br/>
任务粒度、依赖顺序、客观验收项<br/><br/>
<strong style="color:#F8FAFC;">Task Acceptance</strong><br/>
逐项验收、证据检查、返工建议<br/><br/>
<strong style="color:#F8FAFC;">Goal Check</strong><br/>
评估停止条件是否满足
</td>
</tr>
</table>

> 审查角色推荐使用更高推理模型（如 Opus），进一步减少与执行角色的认知偏差共享。当平台不支持分模型时，回退到 prompt 级推理指令。

---

## 四层理解腐烂防护：从被动询问到主动推断验证

> 一个循环越快产出代码、用户越看不懂的循环，不是高效，是侵蚀。

<table>
<tr>
<td width="60" align="center" style="background:#7DD3FC;color:#0F172A;font-weight:900;font-size:20px;border-radius:8px;">L1</td>
<td style="background:#102A2F;padding:16px;">
<strong style="color:#F8FAFC;">每任务变更摘要</strong><br/>
<span style="color:#7DD3FC;font-size:13px;">触发：每个任务验收 PASS 后</span><br/>
<p style="color:#D1FAE5;font-size:14px;">展示变更文件、行为变化、手动验证建议。写入验收报告 AND 直接展示给用户——你不会被排除在循环外。</p>
</td>
</tr>
<tr>
<td width="60" align="center" style="background:#34D399;color:#0F172A;font-weight:900;font-size:20px;border-radius:8px;">L2</td>
<td style="background:#102A2F;padding:16px;">
<strong style="color:#F8FAFC;">推断验证（每 3 个任务）</strong><br/>
<span style="color:#34D399;font-size:13px;">触发：每完成 3 个任务</span><br/>
<p style="color:#D1FAE5;font-size:14px;">不是问"你理解吗？"，而是给出具体推断让你判断对错。说"这个推断是错的"比说"我不理解"心理门槛低得多。</p>
<blockquote style="background:#0F172A;border-left:3px solid #34D399;padding:12px;border-radius:4px;color:#D1FAE5;font-size:13px;">
[Change T01] 修改了 [文件/模块]，效果是 [行为变化]<br/>
→ 这是否意味着 [具体推断 A]？（是/否）
</blockquote>
</td>
</tr>
<tr>
<td width="60" align="center" style="background:#A7F3D0;color:#0F172A;font-weight:900;font-size:20px;border-radius:8px;">L3</td>
<td style="background:#102A2F;padding:16px;">
<strong style="color:#F8FAFC;">实施前确认</strong><br/>
<span style="color:#A7F3D0;font-size:13px;">触发：每个任务实施前</span><br/>
<p style="color:#D1FAE5;font-size:14px;">展示实施意图（任务描述、涉及文件、预期行为变化、不涉及的文件）。允许调整实施细节，但不允许绕过验收标准修改。全自动模式可跳过此层。</p>
</td>
</tr>
<tr>
<td width="60" align="center" style="background:#FDE68A;color:#0F172A;font-weight:900;font-size:20px;border-radius:8px;">L4</td>
<td style="background:#102A2F;padding:16px;">
<strong style="color:#F8FAFC;">变更密度预警</strong><br/>
<span style="color:#FDE68A;font-size:13px;">触发：同一文件/模块在连续 3 个任务中被修改</span><br/>
<p style="color:#D1FAE5;font-size:14px;">暂停并警告：你是否仍理解这个文件/模块的当前状态？交互模式和全自动模式都<strong style="color:#FDE68A;">不可跳过</strong>。</p>
</td>
</tr>
</table>

---

## 循环模式：无人值守自动迭代 + 断点恢复

<table>
<tr>
<td width="50%" style="background:#102A2F;border-top:3px solid #7DD3FC;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">🖱️ 交互模式（默认）</h4>
<p style="color:#7DD3FC;font-size:13px;">触发：/asdev 或 /goal</p>
<ul style="color:#D1FAE5;font-size:14px;padding-left:20px;">
<li>每个阶段可暂停确认</li>
<li>Layer 3 实施前确认 — 启用</li>
<li>Layer 2 推断验证 — 启用</li>
<li>停止：Goal Check PASS 或用户终止</li>
<li>收敛保护：3 轮迭代未 PASS → 暂停</li>
</ul>
</td>
<td width="50%" style="background:#102A2F;border-top:3px solid #FDE68A;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">🔄 循环模式</h4>
<p style="color:#FDE68A;font-size:13px;">触发：目标含"循环模式" / "无人值守" / "自动迭代"，或调度集成</p>
<ul style="color:#D1FAE5;font-size:14px;padding-left:20px;">
<li>自动迭代，仅在收敛保护触发时暂停</li>
<li>Layer 3 实施前确认 — <strong style="color:#FDE68A;">跳过</strong></li>
<li>Layer 2 推断验证 — 改为写入 STATUS.md</li>
<li>停止：Goal Check PASS / 收敛保护 / "终止循环"</li>
<li>收敛保护：2 轮未 PASS 或变更文件超 30 → 降级为交互模式</li>
</ul>
</td>
</tr>
</table>

**断点恢复**：循环模式启动/重启时，读取 `.record/STATUS.md`，有活跃目标则从当前阶段继续，否则从 Phase 0 开始。

**调度集成**：

```text
Claude Code:  /loop 10m "/asdev [目标描述 含循环模式关键词]"
Claude Code:  hooks / cron 定时触发
Codex:        Automations tab → 项目 + 提示词 + 频率
手动重触发:   /asdev [目标]，STATUS.md 保证连续性
```

> 一个无法收敛的循环是设计问题，不是坚持问题。

---

## 记录优先：证据不只留在聊天里

<p align="center">
  <img src="assets/records.svg" alt="asdev 记录产物链路" width="880" />
</p>

每个目标拥有独立隔离的记录目录，不同目标的记录永不混淆：

```text
.record/
├── STATUS.md                  ← 聚合状态视图，断点恢复的基石
├── .knowledge/                 ← 跨目标共享知识条目
│   └── KNOW_YYYYMMDD_*.md
├── {goal-slug}/                ← 每个目标独立子目录
│   ├── .goal/                  ← 目标配置与停止条件
│   ├── .prod/                  ← 代码调查、需求探索、方案设计
│   ├── .task/                  ← 任务拆解和验收标准
│   └── .review/                ← 检查、验收、验证报告
└── {another-goal}/             ← 另一个目标，完全隔离
```

**STATUS.md 三层同步保障**：

| 层级 | 机制 | 保障 |
|------|------|------|
| 第一层 | `scripts/sync-status.py` 从 record files 自动生成 | 无论 Agent 是否手动更新，脚本都能从 source of truth 重建 |
| 第二层 | Claude Code PostToolUse Hook，每次文件变更后自动同步 | 实时性保障，无变更时快速退出（< 100ms） |
| 第三层 | Agent 检查点约束，5 个事件点手动更新 | Hook 不可用时的防御深度 |

**跨目标记忆**：新目标启动时，先读 STATUS.md 获取聚合视图 → 扫描 .knowledge/ 获取项目经验（含置信度和过时标记） → 将历史上下文传递给调查 Agent，避免重复发现已知事实。

**知识条目提取**：

- 🟢 **Task PASS**：实现中暴露非显而易见的模式
- 🟢 **Goal Check PASS**：整体经验有跨目标复用价值
- 🟡 **FAIL → Rework → PASS**：返工原因揭示隐藏约束（失败教得最多）

---

## 什么时候用 asdev

<table>
<tr>
<td width="50%" style="background:#0a1f17;border-top:3px solid #34D399;padding:20px;vertical-align:top;">
<h4 style="color:#86efac;margin-top:0;">✅ 适合</h4>
<ul style="color:#D1FAE5;font-size:14px;padding-left:20px;">
<li>需求影响多个模块、多个角色或多个运行边界</li>
<li>需要找直接/间接调用点、状态流、数据流、事件流</li>
<li>需要先写需求探索，再拆任务，再逐步开发</li>
<li>需要在开发前让检查 Agent 审核方案或任务</li>
<li>需要在完成后让验收 Agent 按标准独立确认</li>
<li>需要无人值守自动迭代直到可验证条件满足</li>
</ul>
</td>
<td width="50%" style="background:#1c1012;border-top:3px solid #7F1D1D;padding:20px;vertical-align:top;">
<h4 style="color:#fca5a5;margin-top:0;">❌ 不适合</h4>
<ul style="color:#D1FAE5;font-size:14px;padding-left:20px;">
<li>简单的一行修改</li>
<li>普通问答</li>
<li>单文件解释</li>
<li>无需验收的小任务</li>
</ul>
</td>
</tr>
</table>

---

## 快速开始

**前置条件**：Claude Code 或 Codex 环境 + 环境支持独立子代理（Agent tool / subagent tools）+ Git

**安装**：

```bash
# Claude Code
git clone https://github.com/welsione/asdev.git /tmp/asdev
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/asdev
cp -R /tmp/asdev ~/.claude/skills/asdev

# Codex
git clone https://github.com/welsione/asdev.git /tmp/asdev
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/asdev
cp -R /tmp/asdev ~/.codex/skills/asdev
```

安装后重启 Claude Code 或开启新会话。

**使用示例**：

```text
/asdev 处理这个目标：
用户在移动端编辑资料后，头像和昵称偶尔不会同步到个人主页。
请先调查前端状态流、接口调用、缓存更新和后端响应链路；
如果有不确定的业务规则先和我对齐，再产出需求探索和任务拆解。
```

```text
/asdev 循环模式：
把旧版订单状态字段迁移到新的状态机模型，同时保持 API、后台任务和报表兼容。
停止条件：所有 test/order 相关测试通过且 lint 无新增警告。
```

---

## 设计哲学

<table>
<tr>
<td width="33%" style="background:#102A2F;border-left:4px solid #7DD3FC;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">🔍 调查先于设计</h4>
<p style="color:#D1FAE5;font-size:14px;">AI 编程失败不是因为不会写代码，而是因为太快开始写代码。asdev 强制要求先找代码事实、调用链、边界入口和现有模式，再动手设计。</p>
</td>
<td width="33%" style="background:#102A2F;border-left:4px solid #34D399;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">⚖️ 制造者不给自己的作业打分</h4>
<p style="color:#D1FAE5;font-size:14px;">单 Agent 自审是 AI 编程最大的系统性风险。9 个独立 Agent 角色分离执行和审查，审查角色推荐更高推理模型，进一步减少认知偏差共享。</p>
</td>
<td width="33%" style="background:#102A2F;border-left:4px solid #FDE68A;padding:20px;vertical-align:top;">
<h4 style="color:#F8FAFC;margin-top:0;">🧱 大风险拆成小风险</h4>
<p style="color:#D1FAE5;font-size:14px;">复杂需求直接开干，失败损失巨大。asdev 把一次性的大风险拆成调查→设计→拆解→逐任务实现→独立验收的流水线，每个环节都有检查点和返工闭环。</p>
</td>
</tr>
</table>

---

<p align="center">
  <strong style="font-size:20px;">asdev 不是让 Agent 更快动手，而是让 Agent 更可靠地交付。</strong>
</p>

<p align="center">
  <code>强制记录</code> · <code>强制验收</code> · <code>验收不过必须返工</code>
</p>
