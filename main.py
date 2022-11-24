import streamlit as st
from Logs import log_obj

if __name__ == "__main__":
    st.write("""
        # Monkey Git
        *Monkey see monkey do!*
    """)
    cmd = st.text_input('Git command : ')

    if st.button("Execute command"):
        st.write(cmd)
        log_obj.log(cmd + " command", True)
