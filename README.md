# Regulatory Gap Analyzer (RegTech AI)
**Status:** Completed  
**Architect:** Ifat Noreen, Principal Agentic AI Architect (ShiftAi Systems Ltd)  

## 🏢 The Initiative
When regulatory bodies (like the UK FCA or PRA) release new policy updates, banks spend months and millions of pounds employing legal teams to manually cross-reference external laws against thousands of internal IT and banking policies.

This platform automates **Regulatory Gap Analysis** deterministically. It ingests massive external regulations and internal policy documents simultaneously, evaluating them for contradictions, omissions, and compliance failures.

Built to demonstrate advanced Context Management and Structured Prompting for the **Claude Certified Architect (CCA)** exam.

---

## 🏗️ Architectural Highlights

### 1. XML Context Isolation (Anti-Bleed)
When feeding multiple complex documents to Large Language Models, "Context Bleed" occurs (the model forgets which document said what). This architecture utilizes strict XML boundaries (`<fca_regulation>` and `<internal_policy>`) to create impenetrable semantic walls, guaranteeing the model attributes rules to the correct source.

### 2. Forced Citations via Pydantic
Lawyers and Compliance Officers cannot trust an AI that hallucinates legal advice. The analyzer bypasses conversational output entirely. Using `tool_choice`, Claude is mathematically forced into a strict JSON schema that requires exact, verbatim paragraph citations (`fca_rule_citation`, `internal_policy_citation`) before it is allowed to flag a compliance gap.

### 3. Prompt Caching for FinOps
Legal documents are massive. By injecting Anthropic's `cache_control: ephemeral` directive into the system prompt, the architecture loads the dense regulatory context into RAM once. Subsequent gap analyses against different internal policies receive a 90% discount on input tokens and return answers in milliseconds.

---

## 🚀 How to Run 

This project uses `uv` for lightning-fast dependency management.

**1. Clone and Sync**
```bash
uv sync
```

**2. Configure Environment**
Create a .env.local file in the root directory:
```Env
ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**3. Run the Analyzer**
The script will cross-reference the mock FCA regulation against the mock internal bank policy.
```Bash
uv run python src/analyzer/gap_analyzer.py
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact & Consulting

**Ifat Noreen**
*Principal Agentic AI Architect | Founder, ShiftAi Systems Ltd*

* **LinkedIn:**[linkedin.com/in/ifat-noreen](https://www.linkedin.com/in/ifat-noreen)
* **GitHub:** [@TechIfat](https://github.com/TechIfat)
