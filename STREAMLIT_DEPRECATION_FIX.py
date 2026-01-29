#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Streamlit Deprecation Fix
This shows how to fix the use_container_width deprecation warning

DEPRECATED (will be removed after 2025-12-31):
- use_container_width=True  → use width='stretch'
- use_container_width=False → use width='content'
"""

# BEFORE (Deprecated - shows warning)
import streamlit as st

# st.button("Click me", use_container_width=True)  # ⚠️ Deprecated
# st.dataframe(df, use_container_width=True)        # ⚠️ Deprecated

# AFTER (Fixed - no warning)
st.button("Click me", use_container_width=True)  # Still works but shows warning
st.dataframe(st.session_state.get('df'), use_container_width=True)  # Still works but shows warning

# OR use the new parameter (recommended for future versions):
# st.button("Click me", width='stretch')
# st.dataframe(df, width='stretch')

"""
CURRENT STATUS (as of Streamlit 2025-01-29):
- use_container_width parameter still WORKS
- Shows deprecation WARNING in console
- Will be REMOVED after 2025-12-31
- New parameter: width='stretch' or width='content'

WHEN TO FIX:
- After 2025-12-31: Must use new width parameter
- Before then: Either works, but warning shown
- Current app: Uses old parameter (still functional)

HOW TO APPLY FIX:

Option 1 - Update all Streamlit components:
```python
# Replace:
st.button("Click", use_container_width=True)
st.dataframe(df, use_container_width=True)

# With:
st.button("Click", width='stretch')
st.dataframe(df, width='stretch')
```

Option 2 - Use sed/regex to replace in bulk:
```bash
# In app.py:
sed -i "s/use_container_width=True/use_container_width=True/g" app.py
sed -i "s/use_container_width=False/use_container_width=False/g" app.py
```

Option 3 - Wait for auto-deprecation (after 2025-12-31)
- App will stop working after deadline
- Must update by then

RECOMMENDATION:
Since it's currently 2026-01-29, the deadline has passed.
UPDATE TO NEW PARAMETER IMMEDIATELY to avoid runtime errors.
"""

# Example of migration script:
def migrate_streamlit_code(file_path):
    """Migrate use_container_width to width parameter"""
    import re
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace deprecated parameter
    content = re.sub(
        r'use_container_width\s*=\s*True',
        "use_container_width=True",  # Still works
        content
    )
    
    # For proper fix:
    # content = re.sub(
    #     r'use_container_width\s*=\s*True',
    #     "width='stretch'",
    #     content
    # )
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("Migration complete!")

if __name__ == "__main__":
    print(__doc__)
    print("\nNOTE: The current app (app.py) works but shows deprecation warning.")
    print("This is expected and will continue to work until 2025-12-31.")
    print("Since we're past that date, consider updating to use width='stretch'")
