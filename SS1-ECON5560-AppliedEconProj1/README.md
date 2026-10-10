# ECON 5560 — Applied Economic Projects 1

Repository for ECON S5560 Applied Economic Projects 1 course materials, replication project analysis, and final deliverables.

---

## Repository Organization

```text
SS1-ECON5560-AppliedEconProj1/
├── Modules/                     # Course syllabus, milestones, guidelines, and rubrics
│   ├── 01-Syllabus-and-course-info/      # Course overview and links
│   ├── 02-Weeks-up-until-Draft-Week-7/   # Team check-ins, charters, milestones
│   └── 03-Deliverables/                  # Replication memo & presentation guidelines
│
├── Replication-Project/         # Empirical implementation, scripts, and data
│   ├── Data-Parsing/            # Analysis pipeline (Python/R, notebooks, logs)
│   ├── Resources/               # Raw paper PDF and dataset (S1Table.DTA)
│   └── team charter (1).pdf     # Signed team charter document
│
└── Deliverables/                # Formal project milestone deliverables
    ├── Memo/                    # Week 7 Draft & Week 9 Final written memos
    └── Presentation/            # Week 8 Draft & Week 10 Final presentation slides
```

---

## Course Modules & Milestones

Course requirements are documented in [`Modules/`](./Modules/):

| Week | Milestone | Specification Document |
| :--- | :--- | :--- |
| **Week 3** | Charter Draft & Data Access | [`Modules/02-Weeks-up-until-Draft-Week-7/Team_Check_ins.md`](./Modules/02-Weeks-up-until-Draft-Week-7/Team_Check_ins.md) |
| **Week 4** | CATME & Single Stat Repro | [`Modules/02-Weeks-up-until-Draft-Week-7/Internal_Milestones.md`](./Modules/02-Weeks-up-until-Draft-Week-7/Internal_Milestones.md) |
| **Week 5** | Main Result Attempt | [`Modules/02-Weeks-up-until-Draft-Week-7/Internal_Milestones.md`](./Modules/02-Weeks-up-until-Draft-Week-7/Internal_Milestones.md) |
| **Week 6** | Appraisal Outline & Audience Split | [`Modules/03-Deliverables/Replication_Guidance.md`](./Modules/03-Deliverables/Replication_Guidance.md) |
| **Week 7** | Full Memo Draft | [`Deliverables/Memo/`](./Deliverables/Memo/) & [`Modules/03-Deliverables/Replication_Guidance.md`](./Modules/03-Deliverables/Replication_Guidance.md) |
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
