import re
import os

files_to_process = [
    'views/3_Detalle_Proyecto.py',
    'views/2_Gestor_de_Proyectos.py'
]

for filepath in files_to_process:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Wrap st.write(f"**Something:** {row.get...") 
    content = re.sub(
        r'st\.write\(f"\*\*([^*]+)\*\*:',
        r'st.write(f"**{i18n.t(\'\1\', lang)}**:',
        content
    )
    
    # Wrap st.expander("TITLE")
    content = re.sub(
        r'st\.expander\("([^"]+)"',
        r'st.expander(i18n.t("\1", lang)"',
        content
    )
    # Fix the missing parenthesis from the above macro
    content = content.replace('lang)"', 'lang)')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Replacement complete.")
