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
           result= vcs_obj.initialize()
           st.write(result)

        elif arg_list[1] == "add":
            if vcs_obj.is_init:
                vcs_obj.add()
            else:
                st.write("not a git repo")

        elif arg_list[1] == "status":
            if vcs_obj.is_init:
                vcs_obj.status()
            else:
                st.write("not a git repo")
            # vcs_obj.status()

        elif arg_list[1] == "commit":
            if vcs_obj.is_init:
                vcs_obj.commit()
            else:
                st.write("not a git repo")
            # vcs_obj.commit()

        elif arg_list[1] == "rollback":
            if vcs_obj.is_init:
                vcs_obj.rollback()
            else:
                st.write("not a git repo")
            # vcs_obj.rollback()

        elif arg_list[1] == "diff":
            if vcs_obj.is_init:
                vcs_obj.diff()
            else:
                st.write("not a git repo")
            # vcs_obj.diff()

        elif arg_list[1] == "log":
            if vcs_obj.is_init:
                vcs_obj.log()
            else:
                st.write("not a git repo")
            # vcs_obj.log()

        elif arg_list[1] == "push":
            if vcs_obj.is_init:
                vcs_obj.push()
            else:
                st.write("not a git repo")
            # vcs_obj.push()

        elif arg_list[1] == "pull":
            if vcs_obj.is_init:
                vcs_obj.pull()
            else:
                st.write("not a git repo")

        vcs_obj.update_repo()

