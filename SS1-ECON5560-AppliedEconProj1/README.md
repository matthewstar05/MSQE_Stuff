# ECON 5560: Applied Economic Projects 1

## Folder guide

| Folder | Contents |
| --- | --- |
| [Course_Info/](Course_Info/) | Course links and syllabus location. |
| [Project_Management/](Project_Management/) | Internal milestones, team check-ins, signed team charter, and [charter examples](Project_Management/Charter_Examples/). |
| [Replication-Project/Resources/](Replication-Project/Resources/) | Paper, raw dataset, and replication assignment guidance. |
| [Replication-Project/Data-Parsing/](Replication-Project/Data-Parsing/) | Existing analysis pipeline, notebooks, results, figures, dashboard, and logs. |
| [Deliverables/](Deliverables/) | Replication guidance and [Memo/](Deliverables/Memo/) and [Presentation/](Deliverables/Presentation/) workspaces. |

The replication analysis directory and its internal paths are unchanged. The signed charter is in `Project_Management/team charter (1).pdf`.

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

## Replication Project (Team 1)

- **Target Paper**: Shah, Dissanayake, Fujita, & Nunes (2019), *"Impact of a Local, Coastal Community Based Management Regime When Defining Marine Protected Areas: Empirical Results from a Study in Okinawa, Japan,"* *PLOS ONE* 14(3): e0213354.
- **Team**: Miles, Z. · Hyde, W. · Wickboldt, E. · Neralla, H.
- **Data & Paper Assets**: [`Replication-Project/Resources/`](./Replication-Project/Resources/)
- **Analysis Pipeline**:
  - `01_parse_data.py`: Loads and cleans `S1Table.DTA`.
  - `02_descriptives.py`: Summary statistics and table reproduction.
  - `03_conditional_logit.py` & `04_mixed_logit.py`: Main econometric choice models.
  - `06_slide_figures.py` & `07_paper_figures.py`: Generates visual figures.
  - `run_all.py`: End-to-end execution script.
