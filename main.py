import streamlit as st
from Logs import log_obj
from git import VCS


if __name__ == "__main__":
    vcs_obj = VCS()
    st.write("""
        # Monkey Git
        *Monkey see monkey do!*
    """)
    cmd = st.text_input('Git command : ')

    if st.button("Execute command"):
        st.write("Current Command : " + cmd)
        log_obj.log(cmd + " command", True)
        arg_list = cmd.split(" ")

        if arg_list[1] == "init":
            vcs_obj.initialize()

        elif arg_list[1] == "add":
            vcs_obj.add()

        elif arg_list[1] == "status":
            vcs_obj.status()

        elif arg_list[1] == "commit":
            vcs_obj.commit()

        elif arg_list[1] == "rollback":
            vcs_obj.rollback()

        elif arg_list[1] == "diff":
            vcs_obj.diff()

        elif arg_list[1] == "log":
            vcs_obj.log()

        elif arg_list[1] == "push":
            vcs_obj.push()

        elif arg_list[1] == "pull":
            vcs_obj.pull()
