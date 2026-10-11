# ECON 5560: Applied Economic Projects 1

## Folder guide

| Folder | Contents |
| --- | --- |
| [Course_Info/](Course_Info/) | Course links and syllabus location. |
| [Project_Management/](Project_Management/) | Internal milestones, team check-ins, signed team charter, and [charter examples](Project_Management/Charter_Examples/). |
| [Replication-Project/Resources/](Replication-Project/Resources/) | Paper, raw dataset, and replication assignment guidance. |
| [ECON5560-Team3/](ECON5560-Team3/) | The team replication repo ([GitHub](https://github.com/matthewstar05/ECON5560-Team3)), embedded with `git subtree`: analysis pipeline, results, dashboard, draft submission. See "Syncing the team repo" below. |
| [Deliverables/](Deliverables/) | Replication guidance and [Memo/](Deliverables/Memo/) and [Presentation/](Deliverables/Presentation/) workspaces. |

The signed charter is in `Project_Management/team charter (1).pdf`.

## Course Milestones

Course requirements are grouped in [Project_Management/](Project_Management/) and [Deliverables/](Deliverables/):

| Week | Milestone | Specification Document |
| :--- | :--- | :--- |
| **Week 3** | Charter Draft & Data Access | [`Project_Management/Team_Check_ins.md`](./Project_Management/Team_Check_ins.md) |
| **Week 4** | CATME & Single Stat Repro | [`Project_Management/Internal_Milestones.md`](./Project_Management/Internal_Milestones.md) |
| **Week 5** | Main Result Attempt | [`Project_Management/Internal_Milestones.md`](./Project_Management/Internal_Milestones.md) |
| **Week 6** | Appraisal Outline & Audience Split | [`Deliverables/Replication_Guidance.md`](./Deliverables/Replication_Guidance.md) |
| **Week 7** | Full Memo Draft | [`Deliverables/Memo/`](./Deliverables/Memo/) & [`Deliverables/Replication_Guidance.md`](./Deliverables/Replication_Guidance.md) |
| **Week 8** | Slides Draft (Appraisal Format) | [`Deliverables/Presentation/`](./Deliverables/Presentation/) |
| **Week 9** | Final Memo Submission | [`Deliverables/Memo/`](./Deliverables/Memo/) |
| **Week 10** | Final Presentation | [`Deliverables/Presentation/`](./Deliverables/Presentation/) |

---

## Replication Project (Team 3)

- **Target paper**: Eppink, Winden, Wright & Greenhalgh (2016), *"Non-Market Values in a Cost-Benefit World: Evidence from a Choice Experiment,"* *PLoS ONE* 11(10): e0165365.
- **Team repo**: [`ECON5560-Team3/`](./ECON5560-Team3/). Start with its [README](./ECON5560-Team3/README.md).
- **Analysis pipeline**: [`ECON5560-Team3/Data-Parsing/`](./ECON5560-Team3/Data-Parsing/) (`run_all.py` runs everything end to end).
- **Course assets** (Canvas pages, assignment guidance): [`Replication-Project/Resources/`](./Replication-Project/Resources/)

## Syncing the team repo

`ECON5560-Team3/` is a `git subtree` copy of https://github.com/matthewstar05/ECON5560-Team3. Run these from the MSQE_Stuff root. On this computer the shortcuts `git team3-pull` and `git team3-push` do the same thing (they're set in this repo's local git config, so they don't carry over to other clones).

Pull the team's latest changes in:

```
git subtree pull --prefix=SS1-ECON5560-AppliedEconProj1/ECON5560-Team3 https://github.com/matthewstar05/ECON5560-Team3.git main --squash
```

Send edits made here back to the team repo:

```
git subtree push --prefix=SS1-ECON5560-AppliedEconProj1/ECON5560-Team3 https://github.com/matthewstar05/ECON5560-Team3.git main
```
