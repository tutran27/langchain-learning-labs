# Lab 07 · Agentic Patterns Lab

> 🤖 Kiến trúc thiết kế các mẫu Agentic Pattern nâng cao với LangChain & LangGraph.

## 📂 Cấu trúc thư mục (Architecture Layout)

```
lab07_agentic_patterns/
├── common/
│   ├── domain.py           # Domain models, User Roles, Permissions & Data Schemas
│   ├── tools.py            # Shared tools (search, db lookup, calculator, admin tools)
│   ├── llm.py              # LLM loader helper (GroqLLMModel / ChatGroq)
│   └── agent_utils.py      # Console logging formatters, execution timing, safe tool runner
├── router_agent/
│   ├── schemas.py          # Routing decisions & Intent classification schemas
│   └── main.py             # Intent Router Agent & specialized handlers
├── planner_executor/
│   ├── schemas.py          # Plan, PlanStep & Replanner schemas
│   ├── validator.py        # Plan structure & dependency validator
│   └── main.py             # Plan-and-Execute loop với dynamic re-planning
├── reflection_self_check/
│   ├── schemas.py          # Critique & ReflectedOutput schemas
│   ├── validators.py       # Content & rule-based quality validators
│   └── main.py             # Generator-Reflector-Reviser feedback loop
├── permission_aware_agent/
│   └── main.py             # Role-Based Access Control (RBAC) & Safety check agent
├── failure_recovery/
│   └── main.py             # Retry with exponential backoff & Fallback chain agent
├── tests/                  # Unit tests cho từng agent pattern
│   ├── test_router.py
│   ├── test_planner.py
│   ├── test_reflection.py
│   ├── test_permission.py
│   └── test_failure.py
├── README.md               # Tài liệu tổng quan lab
└── requirements.txt        # Danh sách thư viện cần thiết
```

## 🚀 Cách thực thi các Pattern

### 1. Router Agent
```bash
python -m labs.lab07_agentic_patterns.router_agent.main
```

### 2. Planner-Executor Agent
```bash
python -m labs.lab07_agentic_patterns.planner_executor.main
```

### 3. Reflection & Self-Check Agent
```bash
python -m labs.lab07_agentic_patterns.reflection_self_check.main
```

### 4. Permission-Aware Agent
```bash
python -m labs.lab07_agentic_patterns.permission_aware_agent.main
```

### 5. Failure Recovery Agent
```bash
python -m labs.lab07_agentic_patterns.failure_recovery.main
```

### 6. Chạy Unit Tests
```bash
pytest labs/lab07_agentic_patterns/tests
```
