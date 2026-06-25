<p align="center">
  <img src="assets/logo.svg" alt="asdev logo" width="760" />
</p>

<p align="center">
  <strong>把复杂软件目标交给一支会调查、会拆解、会验收的 Agent 团队。</strong>
</p>

<p align="center">
  <code>/asdev</code> · <code>强制多 Agent</code> · <code>代码事实优先</code> · <code>可验收交付</code>
</p>

---

## 它解决什么问题？

很多 AI 编程失败，不是因为不会写代码，而是因为太快开始写代码。

`asdev` 把复杂需求改造成一套目标模式工作流：先调查真实代码，再对齐不确定性，再拆成可验收任务，最后用独立 Agent 做检查和验收。它适合那些不能靠“一次性改一下”解决的工程问题。

<p align="center">
  <img src="assets/workflow.svg" alt="asdev 四阶段工作流" width="900" />
</p>

## 特点

- **先调查，后设计**：要求 Agent 先找代码事实、调用链、边界入口和现有模式。
- **强制多 Agent**：调查、设计、拆解、检查、验收分角色完成，不用主 Agent 自审冒充验收。
- **任务可验收**：每个任务都要有原因、目标、客观验收项和验证证据。
- **记录可追溯**：产物写入 `.record/`，后续 Agent 能读到完整上下文。
- **不锁技术栈**：适用于前端、后端、CLI、桌面端、数据迁移、架构改造、性能优化等复杂软件目标。
- **可增强但不强绑**：`codegraph`、`superpowers`、框架专用 skill 都可以作为增强能力使用。

## 适合什么时候用？

- 需求影响多个模块、多个角色或多个运行边界。
- 需要找直接/间接调用点、状态流、数据流、事件流。
- 需要先写需求探索，再拆任务，再逐步开发。
- 需要在开发前让检查 Agent 审核方案或任务。
- 需要在完成后让验收 Agent 按标准独立确认。

不适合简单的一行修改、普通问答、单文件解释或无需验收的小任务。

## 安装

让 Agent 执行下面的命令即可安装到 Claude Code：

```bash
git clone https://github.com/welsione/asdev.git /tmp/asdev
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/asdev
cp -R /tmp/asdev ~/.claude/skills/asdev
```

安装后重启 Claude Code 或开启新会话。

Codex 可安装到：

```bash
git clone https://github.com/welsione/asdev.git /tmp/asdev
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/asdev
cp -R /tmp/asdev ~/.codex/skills/asdev
```

## 使用

推荐显式触发：

```text
/asdev 处理这个目标：
用户在移动端编辑资料后，头像和昵称偶尔不会同步到个人主页。
请先调查前端状态流、接口调用、缓存更新和后端响应链路；
如果有不确定的业务规则先和我对齐，再产出需求探索和任务拆解。
```

```text
/asdev 规划一次数据迁移：
把旧版订单状态字段迁移到新的状态机模型，同时保持 API、后台任务和报表兼容。
请调查调用方、定时任务、数据修复脚本和回滚策略，
再让任务拆解 Agent 给出可逐步上线的任务计划。
```

## 产出

默认会在项目内沉淀这些记录：

```text
.record/
├── .goal/    # 目标模式配置
├── .prod/    # 代码调查、需求探索、方案设计
├── .task/    # 任务拆解和验收标准
└── .review/  # 检查、验收、验证报告
```

## 一句话

`asdev` 不是让 Agent 更快动手，而是让 Agent 更可靠地交付。
