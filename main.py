import json

import pandas as pd
import streamlit as st
from Logs import log_obj
from git import VCS
from Config import conf_obj

if __name__ == "__main__":
    vcs_obj = VCS(conf_obj["cwd"])
    st.write("""
        # Monkey Git
        *Monkey see monkey do!*
    """)
    cmd = st.text_input('Git command : ')

    if st.button("Execute command"):
        st.write("Current Command : " + cmd)
        st.write("Current Working Directory : " + conf_obj["cwd"])
        log_obj.log(cmd + " command", True)
        arg_list = cmd.split(" ")
        if vcs_obj.is_init and arg_list[1] != "init":
            df = pd.read_csv(vcs_obj.repo_info)
            vcs_obj.files_list = df['filename'].tolist()
            vcs_obj.sha_list = df['sha'].tolist()
            vcs_obj.track_flag = df['track_flag'].tolist()
            vcs_obj.update_repo()

        if arg_list[1] == "cd":
            conf_obj["cwd"] = arg_list[2]
            jsonFile = open("./Config/config.json", "w+")
            jsonFile.write(json.dumps(conf_obj))
            jsonFile.close()
            vcs_obj = VCS(arg_list[2])

        elif arg_list[1] == "init":
            result = vcs_obj.initialize()
            st.write(result)

        elif arg_list[1] == "add":
            if vcs_obj.is_init:
                if arg_list > 2:
                    vcs_obj.add(arg_list[2:])
                else:
                    print("Nothing specified,Nothing Added")
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
