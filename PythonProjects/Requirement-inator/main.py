import os
import pandas as pd
from InquirerPy import inquirer
from InquirerPy.base import Choice

excel_path = 'C:\\Users\\og153f\\Documents\\PMPC\\T4_Review\\P1_PMPC_T4_Requirements_PEER_REVIEW_2024 - copy.xlsx'


def find_reqs():
    reqs_xlsx_df = pd.ExcelFile(excel_path)

    # finding sheets
    tier3_reqs_df = reqs_xlsx_df.parse("Tier 3 Requirements - LRU")
    tier4_reqs_df = reqs_xlsx_df.parse("Tier 4 Requirements - HW")
    reqs_xlsx_df.close()
    num_t4_rows = len(tier4_reqs_df.index)
    if "Review Comment" not in tier4_reqs_df:
        comment_blank_list = num_t4_rows * [""]
        tier4_reqs_df["Review Comment"] = comment_blank_list
    tier4_reqs_df["Review Comment"] = tier4_reqs_df["Review Comment"].fillna("")
    # picking column H in FHA
    menu_choices = ["View Modules", "View T3 Trace Requirements", "View Notes", "Add Comment", "Continue", "Exit"]
    module_choices = [
        Choice("Chassis"),
        Choice("Backplane"),
        Choice("Front Panel"),
        Choice("Fiber Optic Cable Harness"),
        Choice("OCM"),
        Choice("MIAB"),
        Choice("GPP"),
        Choice("Add Ethernet GPP"),
        Choice("RoT Ethernet+ GPP"),
        Choice("SC Add Ethernet GPP"),
        Choice("PS"),
        Choice("818 Graphics"),
        Choice("Ethernet Switch"),
        Choice("SC 818 Graphics")
    ]
    t3_req_choice_list = []

    # print(tier3_reqs_df.columns)
    # print(tier4_reqs_df.columns)
    triggered_exit = False
    for tier4_row in tier4_reqs_df.index:
        if triggered_exit:
            break

        t4_comment = tier4_reqs_df["Review Comment"][tier4_row]

        continue_exec = True
        if len(t4_comment) > 0:
            continue_exec = False
        if continue_exec:
            tier4_reqs_df.loc[tier4_row, "Review Comment"] = "X"
        while continue_exec:
            # Clearing the Screen
            os.system('cls')

            # Starting Inquirer for each requirement
            req_main_choices = inquirer.checkbox(
                message=str(tier4_reqs_df["T4 Requirement Text"][tier4_row]) + "|" + str(tier4_reqs_df["Section"][
                    tier4_row]) + "|" +
                        str(tier4_reqs_df["Verif Methoc"][tier4_row]),
                choices=menu_choices,
                validate=lambda result: len(result) >= 1,
                invalid_message="should be at least 1 selection",
                instruction="(select at least 1)",
                wrap_lines=True,
            ).execute()

            os.system('cls')
            for option in req_main_choices:
                if option == "Continue":
                    continue_exec = False

                if option == "View Modules":
                    for module in module_choices:
                        if tier4_reqs_df[module.name][tier4_row] == "X":
                            module.enabled = True
                        else:
                            module.enabled = False
                    req_module_choices = inquirer.checkbox(
                        message="Req is assigned to following modules",
                        choices=module_choices,
                        default=["Chassis", "Backplane"],
                        invalid_message="should be at least 1 selection",
                        instruction="(select at least 1)",
                        wrap_lines=True,
                    ).execute()
                    # Clear out module selections
                    for module in module_choices:
                        tier4_reqs_df[module.name][tier4_row] = ""
                    for modules in req_module_choices:
                        tier4_reqs_df[modules][tier4_row] = "X"

                if option == "View Notes":
                    (inquirer.text(message=tier4_reqs_df["Note/Orphan (Derived Requirement) Rationale"][tier4_row])
                     .execute())

                if option == "View T3 Trace Requirements":
                    t3_req_list = []
                    unsplit_t3s = tier4_reqs_df["Traces to"][tier4_row]
                    if (unsplit_t3s != "Orphan") or (unsplit_t3s != "INFO"):
                        split_t3s = unsplit_t3s.split("\n")
                        paired_down_t3_df = tier3_reqs_df[tier3_reqs_df["Requirement ID"].isin(split_t3s)]
                        combined_t3_df = (paired_down_t3_df["Requirement ID"] + " | "
                                          + paired_down_t3_df["Requirement Text"] + " | "
                                          + paired_down_t3_df["Section Title"])
                        t3_req_list = combined_t3_df.tolist()
                        t3_req_choice_list = [Choice(t3, enabled=True) for t3 in t3_req_list]
                    t3_req_choice_list.append(Choice("Add Requirement", enabled=False))
                    req_t3_choices = inquirer.checkbox(
                        message="Req is assigned to following modules",
                        choices=t3_req_choice_list,
                        invalid_message="should be at least 1 selection",
                        instruction="(select at least 1)",
                        wrap_lines=True,
                    ).execute()
                    new_t3_list = []
                    for t3s in req_t3_choices:
                        if t3s != "Add Requirement" and t3s != "Orphan" and t3s != "INFO":
                            resplit_t3_list = t3s.split(" |")
                            new_t3_list.append(resplit_t3_list[0])
                        if t3s == "Orphan":
                            new_t3_list.append("Orphan")
                        if t3s == "INFO":
                            new_t3_list.append("INFO")
                        if t3s == "Add Requirement":
                            find_new_t3_df = (tier3_reqs_df["Requirement ID"] + " | "
                                              + tier3_reqs_df["Requirement Text"] + " | "
                                              + tier3_reqs_df["Section Title"])
                            new_t3_req_list = find_new_t3_df.tolist()
                            subtracted_t3_req_list = [t3 for t3 in new_t3_req_list if t3 not in t3_req_list]
                            modified_t3_choice_req_list = [Choice(cht3, enabled=False) for cht3 in
                                                           subtracted_t3_req_list]
                            t3_req_choice_list.pop()
                            modified_t3_choice_req_list.extend(t3_req_choice_list)

                            action = inquirer.fuzzy(
                                message="Select Requirements :",
                                choices=modified_t3_choice_req_list,
                                multiselect=True,
                                match_exact=True
                            ).execute()
                            new_t3_list.clear()
                            for added_requirements in action:
                                add_t3_req_array = added_requirements.split(" |")
                                new_t3_list.append(add_t3_req_array[0])
                    t3_str = "\n".join(new_t3_list)
                    tier4_reqs_df.loc[tier4_row, "Traces to"] = t3_str

                if option == "Add Comment":
                    comment = inquirer.text(message="Enter Your comment:",
                                            default=tier4_reqs_df["Review Comment"][tier4_row]).execute()
                    tier4_reqs_df["Review Comment"][tier4_row] = comment
                if option == "Exit":
                    if tier4_reqs_df["Review Comment"][tier4_row] == "X":
                        tier4_reqs_df.loc[tier4_row, "Review Comment"] = ""
                    continue_exec = False
                    triggered_exit = True

    path = excel_path
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    tier3_reqs_df.to_excel(writer, sheet_name="Tier 3 Requirements - LRU", index=False)
    tier4_reqs_df.to_excel(writer, sheet_name="Tier 4 Requirements - HW", index=False)
    writer.close()


if __name__ == '__main__':
    find_reqs()
