import json
import pandas as pd
import streamlit as st
from Logs import log_obj
from git import VCS
from Config import conf_obj, UnTrackedNew, UnTrackedMod, UnTrackedDel, TrackedNew, TrackedMod, TrackedDel

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

        # run update before every command (if not init)
        if vcs_obj.is_init and arg_list[1] != "init":
            df = pd.read_csv(vcs_obj.repo_info)
            vcs_obj.files_list = df['filename'].tolist()
            vcs_obj.sha_list = df['sha'].tolist()
            vcs_obj.track_flag = df['track_flag'].tolist()
            vcs_obj.update_repo()

        # git cd <directory_path>
        if arg_list[1] == "cd":
            conf_obj["cwd"] = arg_list[2]
            jsonFile = open("./Config/config.json", "w+")
            jsonFile.write(json.dumps(conf_obj))
            jsonFile.close()
            vcs_obj = VCS(arg_list[2])

        # git init
        elif arg_list[1] == "init":
            result = vcs_obj.initialize()
            st.write(result)

        # git add <.> / <file_name>
        elif arg_list[1] == "add":
            if vcs_obj.is_init:
                if len(arg_list) > 2:
                    vcs_obj.log(arg_list[1])
                if len(arg_list) > 2:
                    vcs_obj.add(arg_list[2:])
                else:
                    print("Nothing specified, nothing added!")
            else:
                st.write("Not a Git Repo!!")

        elif arg_list[1] == "restore":
            vcs_obj.restore()

        # git status
        elif arg_list[1] == "status":
            if vcs_obj.is_init:
                vcs_obj.log(arg_list[1])
                res = vcs_obj.status()
                st.write("Tracked --> ")
                for i in res["tracked_new"]:
                    st.success("New File : " + i)
                for i in res["tracked_mod"]:
                    st.success("Modified File : " + i)
                for i in res["tracked_del"]:
                    st.success("Deleted File : " + i)

                st.write("Untracked --> ")
                for i in res["untracked_new"]:
                    st.error("New File : " + i)
                for i in res["untracked_mod"]:
                    st.error("Modified File : " + i)
                for i in res["untracked_del"]:
                    st.error("Deleted File : " + i)

            else:
                st.write("Not a Git Repo!!")

        # git log
        elif arg_list[1] == "log":
            if vcs_obj.is_init:
                df = pd.read_csv(vcs_obj.log_info)
                st.table(data=df)
            else:
                st.write("Not a Git Repo!!")

        elif arg_list[1] == "commit":
            if vcs_obj.is_init:
                vcs_obj.commit()
            else:
                st.write("Not a Git Repo!")

        # git rollback -s <number> / -c <commit id>
        elif arg_list[1] == "rollback":
            if vcs_obj.is_init:
                res = vcs_obj.rollback(arg_list[2:])
                st.write(res)
            else:
                st.write("Not a Git Repo!")

        elif arg_list[1] == "diff":
            if vcs_obj.is_init:
                vcs_obj.diff()
            else:
                st.write("Not a Git Repo!")

        elif arg_list[1] == "log":
            if vcs_obj.is_init:
                vcs_obj.log()
            else:
                st.write("Not a Git Repo!")

        elif arg_list[1] == "push":
            if vcs_obj.is_init:
                vcs_obj.push()
            else:
                st.write("Not a Git Repo!")

        elif arg_list[1] == "pull":
            if vcs_obj.is_init:
                vcs_obj.pull()
            else:
                st.write("Not a Git Repo!")
