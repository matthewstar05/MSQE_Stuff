# Sources and literature checks

Prepared 2026-10-10. The Google Doc started blank. The draft preserves space for team prose and uses committed results from `0ef7bc14e6a964ce66fe4c105a672b0b758d7277`.

## Inputs

- Team repository: https://github.com/matthewstar05/ECON5560-Team3
- Replicated paper and data: https://doi.org/10.1371/journal.pone.0165365 (local article PDF and `Resources/S1Table.DTA`). Article text and figures inspected.
- Canvas assignment: https://canvas.calpoly.edu/courses/192663/assignments/1742741. The live page was unavailable to the web reader; requirements were read from the user-provided `Draft Replication Memo.html`. It asks for the draft memo now and packaging of data/code for the end, not current data/code submission.
- Course guidance: user-provided `Replication Guidance_ ECON-S5560-S01-2268 - Applied Economics Project.html`. Five-page narrative, at least five additional scholarly sources, attribution and AI disclosure. Saved HTML files are excluded because they embed account information.
- Style example: Korpershoek, Musumeci, Stans and Totarelli (2023), I4R Discussion Paper No. 27, https://hdl.handle.net/10419/270744. Read from the user-provided `I4R-DP027.pdf`. Borrowed numbered introduction/reproducibility/appraisal structure, original-versus-replication panels, source notes and candid discrepancy reporting. No example topic, data, conclusions or article text were copied. The PDF itself is not redistributed in the repository.

## Five supporting scholarly sources

These checks establish that the sources exist and support the indicated limited use. They do not substitute for team reading or justify untested claims about this replication.

| Source | Verified primary/institutional record | Appropriate use and verification scope |
|---|---|---|
| Train (2009), *Discrete Choice Methods with Simulation*, 2nd ed. | https://eml.berkeley.edu/books/choice2.html and chapter 6: https://eml.berkeley.edu/books/choice2nd/Ch06_p134-150.pdf | Author-hosted book index and chapter 6 inspected. Mixed logit integrates logit probabilities over a coefficient distribution and can represent repeated-choice dependence. |
| Hole (2007), *The Stata Journal*, 7(3), 388-401 | https://www.stata-journal.com/article.html?article=st0133 ; DOI https://doi.org/10.1177/1536867X0700700306 | Journal record and publisher abstract inspected. Describes `mixlogit` maximum simulated likelihood. Do not infer equivalence to our implementation from this abstract alone. |
| Cameron & Miller (2015), *Journal of Human Resources*, 50(2), 317-372 | https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf ; DOI https://doi.org/10.3368/jhr.50.2.317 | Author-hosted published paper inspected. Within-cluster dependence affects inference; cluster-robust methods require assumptions and adequate clusters. It does not independently validate the custom sandwich calculation here. |
| Johnston et al. (2017), *JAERE*, 4(2), 319-405 | https://eprints.gla.ac.uk/154016/ and accepted manuscript https://eprints.gla.ac.uk/154016/1/154016.pdf ; DOI https://doi.org/10.1086/691697 | University author record, full author list, abstract and accepted manuscript inspected. Recommendations concern design and use of stated-preference research; do not claim a universal bias size. |
| Kallis, Gómez-Baggethun & Zografos (2013), *Ecological Economics*, 94, 97-105 | https://portalrecerca.uab.cat/en/publications/to-value-or-not-to-value-that-is-not-the-question/ ; DOI https://doi.org/10.1016/j.ecolecon.2013.07.002 | Author-institution record and publisher abstract inspected. Discusses when/how monetary valuation fits environmental, distributive and institutional goals. Full text was not required or claimed for this template; no quantitative empirical finding was attributed to it. |

The I4R structural example is not counted as one of the five additional topical sources. Final prose must use in-text author-date citations for specific claims, not merely list references. Additional empirical literature may improve the comparison.

## Cautions carried into the template

Upstream README/log language sometimes describes discrepancies as proven author errors. The memo deliberately uses narrower language: observed mismatches, possible reporting issues, and unconfirmed data-history/model-label explanations. In particular, the rounded town-size percentages being compatible with n = 188 does not prove the authors used that dataset or make 188 the unique possible denominator over every range. No authors were contacted and no Stata run was performed for this task.
