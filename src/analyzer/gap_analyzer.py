"""
Regulatory Gap Analyzer
Cross-references internal policies against external FCA regulations using XML tagging,
and forces structured, citable JSON outputs for compliance auditing.
"""
import os
import json
import logging
from dotenv import load_dotenv
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv(".env.local")
console = Console()
logger = logging.getLogger("Gap-Analyzer")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 1. Strict Enterprise Schema for the Audit Report
gap_report_schema = {
    "name": "generate_gap_report",
    "description": "Generates a structured regulatory gap analysis report.",
    "input_schema": {
        "type": "object",
        "properties": {
            "overall_status": {
                "type": "string", 
                "enum": ["COMPLIANT", "NON_COMPLIANT"],
                "description": "The overall compliance status of the internal policy."
            },
            "findings": {
                "type": "array",
                "description": "A list of specific regulatory gaps identified.",
                "items": {
                    "type": "object",
                    "properties": {
                        "violation_topic": {"type": "string", "description": "Short title of the issue (e.g., 'Testing Frequency')."},
                        "severity": {"type": "string", "enum":["CRITICAL", "HIGH", "MEDIUM", "LOW"]},
                        "fca_rule_citation": {"type": "string", "description": "Exact quote or reference from the FCA Regulation."},
                        "internal_policy_citation": {"type": "string", "description": "Exact quote or reference from the Internal Policy causing the breach."},
                        "remediation_action": {"type": "string", "description": "What the bank must do to fix this."}
                    },
                    "required":["violation_topic", "severity", "fca_rule_citation", "internal_policy_citation", "remediation_action"]
                }
            }
        },
        "required": ["overall_status", "findings"]
    }
}

def read_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()

def run_gap_analysis():
    console.print("\n[bold cyan]⚖️ INITIATING REGULATORY GAP ANALYSIS...[/bold cyan]")
    
    # 2. Read the raw documents
    fca_law = read_file("data/regulations/fca_ai_risk_2026.txt")
    internal_policy = read_file("data/internal_policies/bank_it_policy_v2.txt")
    
    # 3. EXAM CONCEPT: XML Tagging for Context Isolation
    combined_context = f"""
    <documents>
        <fca_regulation>
        {fca_law}
        </fca_regulation>
        
        <internal_policy>
        {internal_policy}
        </internal_policy>
    </documents>
    """
    
    # 4. Invoke Claude with Forced Tool Output & Prompt Caching
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        temperature=0,
        system=[
            {
                "type": "text",
                "text": "You are a Lead Regulatory Compliance Auditor for a Tier 1 UK Bank. Cross-reference the provided internal policy against the FCA regulation. Find every discrepancy, violation, or gap. You must cite your findings accurately based on the provided text.",
                "cache_control": {"type": "ephemeral"} # Caches the system instructions and persona
            }
        ],
        messages=[{"role": "user", "content": combined_context}],
        tools=[gap_report_schema],
        tool_choice={"type": "tool", "name": "generate_gap_report"}
    )
    
    # 5. Extract and Render the JSON
    for block in response.content:
        if block.type == "tool_use":
            report_data = block.input
            
            # Print Overall Status
            status_color = "red" if report_data["overall_status"] == "NON_COMPLIANT" else "green"
            console.print(f"\n[bold {status_color}]OVERALL STATUS: {report_data['overall_status']}[/bold {status_color}]\n")
            
            # Print Individual Findings elegantly
            for i, finding in enumerate(report_data["findings"], 1):
                sev_color = "red" if finding["severity"] in ["CRITICAL", "HIGH"] else "yellow"
                
                panel_content = (
                    f"[bold]FCA Law:[/bold] {finding['fca_rule_citation']}\n"
                    f"[bold]Bank Policy:[/bold] {finding['internal_policy_citation']}\n\n"
                    f"[bold cyan]Action Required:[/bold cyan] {finding['remediation_action']}"
                )
                
                console.print(Panel(
                    panel_content, 
                    title=f"⚠️ Finding {i}: {finding['violation_topic']} [{finding['severity']}]", 
                    border_style=sev_color
                ))
            return

    console.print("[bold red]Failed to generate structured report.[/bold red]")

if __name__ == "__main__":
    run_gap_analysis()
