import sys
import os
import re

sys.path.insert(0, "/Users/billy/SAPB1_Sim")
from process_data import ALL_SECTIONS

map_path = "/Users/billy/SAPB1_Sim/Process_Hierarchy_Map.md"

with open(map_path, "r", encoding="utf-8") as f:
    content = f.read()

# Build Markdown for Section 4
sec4_lines = []
sec4_lines.append("## 4. Level 4: Process Steps per Level 3 Process (Detailed Route Execution Matrix)\n")
sec4_lines.append("Level 4 defines the sequential **Procedural Steps & Transaction Milestones** executed within SAP Business One for each of the 28 Level 3 Route Groups.\n")
sec4_lines.append("All step names strictly adhere to the standard enterprise naming convention: **`[Step Code]: [Role] Action/Verb Document (DocType) @ Location → [Milestone/Outcome]`**, enforcing Policy 6 (Universal Direct AR Invoicing without standalone ODLN), Policy 7 (OWTQ picking for SIT transfers), Policy 5 (Two-stage landed costing), and Policy 9 (Canonical RACI Role Segregation).\n")
sec4_lines.append("---\n")

for sec_idx, sec in enumerate(ALL_SECTIONS, 1):
    banner = sec["section_banner"]
    sec4_lines.append(f"### 4.{banner}\n")
    
    for proc in sec["processes"]:
        l3_banner = proc["l3_banner"]
        sec4_lines.append(f"#### {l3_banner}\n")
        
        for step in proc["steps"]:
            l3_code, step_code, step_title, doc_table, db_name, loc, onhand, valuation, gl_entry = step
            
            # Format multi-line fields cleanly
            onhand_fmt = " ".join([line.strip() for line in onhand.strip().split("\n") if line.strip()])
            
            raw_val_lines = [l.strip() for l in valuation.strip().split("\n") if l.strip()]
            clean_val_lines = [re.sub(r'^[•\-\*]\s*', '', l) for l in raw_val_lines]
            val_fmt = " • " + " • ".join(clean_val_lines)
                
            gl_lines = [l.strip() for l in gl_entry.strip().split("\n") if l.strip()]
            gl_fmt = " ".join(gl_lines)
            
            sec4_lines.append(f"1. **`{step_code}`: {step_title}**:")
            sec4_lines.append(f"   - **SAP B1 Document & Database**: `{doc_table}` in `{db_name}` (`{loc}`)")
            sec4_lines.append(f"   - **OnHand Snapshot (`OITW.OnHand`)**: {onhand_fmt}")
            sec4_lines.append(f"   - **Inventory Valuation Calculation**: {val_fmt}")
            sec4_lines.append(f"   - **Chart of Accounts (CoA) G/L Entry (`OJDT`)**: {gl_fmt}\n")
        
        sec4_lines.append("")

sec4_text = "\n".join(sec4_lines)

# Find Section 4 and Section 5 in Process_Hierarchy_Map.md
sec4_start = content.find("## 4. Level 4: Process Steps per Level 3 Process (Detailed Route Execution Matrix)")
sec5_start = content.find("## 5. Level 5: System Table Artifacts & Accounting Triggers")

if sec4_start == -1 or sec5_start == -1:
    print(f"Error: Markers not found! sec4_start={sec4_start}, sec5_start={sec5_start}")
else:
    new_content = content[:sec4_start] + sec4_text + "---\n\n" + content[sec5_start:]
    with open(map_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated Section 4 of Process_Hierarchy_Map.md with clean bullets!")
