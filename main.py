import json
import pandas as pd
import streamlit as st
from Logs import log_obj
from git import VCS
from Config import conf_obj, UnTrackedNew, UnTrackedMod, UnTrackedDel, TrackedNew, TrackedMod, TrackedDel
import difflib


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

        st.caption("---------------------------------------------------------------------------------------")

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
            st.success(result)

        # git add <.> / <file_name>
        elif arg_list[1] == "add":
            if vcs_obj.is_init:
                if len(arg_list) > 2:
                    vcs_obj.log(arg_list[1])
                    res = vcs_obj.add(arg_list[2:])
                    if res == "Success":
                        st.success("Files are added!")
                else:
                    st.warning("Nothing specified, nothing added!")
            else:
                st.error("Not a Git Repo!!")

        # git status
        elif arg_list[1] == "status":
            if vcs_obj.is_init:
                vcs_obj.log(arg_list[1])
                res = vcs_obj.status()
                st.write("Tracked --> ")
                if len(res["tracked_new"]) == 0 and len(res["tracked_mod"]) == 0 and len(res["tracked_del"]) == 0:
                    st.warning("No tracked files")
                else:
                    for i in res["tracked_new"]:
                        st.success("New File : " + i)
                    for i in res["tracked_mod"]:
                        st.success("Modified File : " + i)
                    for i in res["tracked_del"]:
                        st.success("Deleted File : " + i)

                st.write("Untracked --> ")
                if len(res["untracked_new"]) == 0 and len(res["untracked_mod"]) == 0 and len(res["untracked_del"]) == 0:
                    st.warning("No untracked files")
                else:
                    for i in res["untracked_new"]:
                        st.error("New File : " + i)
                    for i in res["untracked_mod"]:
                        st.error("Modified File : " + i)
                    for i in res["untracked_del"]:
                        st.error("Deleted File : " + i)

            else:
                st.error("Not a Git Repo!!")

        # git log
        elif arg_list[1] == "log":
            if vcs_obj.is_init:
                df = pd.read_csv(vcs_obj.log_info)
                st.table(data=df)
            else:
                st.error("Not a Git Repo!!")

        # git commit <options> <params>
        elif arg_list[1] == "commit":
            if vcs_obj.is_init:
                commit_id = vcs_obj.commit(arg_list)
                vcs_obj.log(arg_list, True, commit_id)
            else:
                st.error("Not a Git Repo!")

        # git rollback -s <number> / -c <commit id>
        elif arg_list[1] == "rollback":
            vcs_obj.log(arg_list[1])
            if vcs_obj.is_init:
                res = vcs_obj.rollback(arg_list[2:])
                st.write(res)
            else:
                st.error("Not a Git Repo!")

        # git diff <filename>
        elif arg_list[1] == "diff":
            vcs_obj.log(arg_list[1])
            if len(arg_list) != 3:
                st.error("Please enter : git diff <filename>")
            if vcs_obj.is_init:
                filename = arg_list[2]
                res = vcs_obj.diff(filename)
                if type(res) == str:
                    st.warning(res)
                else:
                    for msg in res:
                        st.write(msg)

                st.snow()
            else:
                st.error("Not a Git Repo!")

        elif arg_list[1] == "push":
            vcs_obj.log(arg_list[1])
            if vcs_obj.is_init:
                vcs_obj.push()
            else:
                st.error("Not a Git Repo!")

        elif arg_list[1] == "pull":
            vcs_obj.log(arg_list[1])
            if vcs_obj.is_init:
                vcs_obj.pull()
            else:
                st.error("Not a Git Repo!")
