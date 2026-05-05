# ARC-AGI Starter Pack for CS7637

This starter pack is designed as an early-semester foundation for a KBAI project that uses ARC-AGI in the same spirit that the Summer 2024 syllabus used Ravens Progressive Matrices: an individual Python agent project with milestone-style progress, code submitted separately from written reports, and JDF-based writeups exported to PDF for submission.[cite:54][cite:56]

The Summer 2024 syllabus says the semester-long project was split into milestone submissions plus a final project, with each submission graded half on agent performance and half on a written report, and with the reports written in JDF and submitted to Canvas while code was submitted to Gradescope.[cite:54] Even though the benchmark in your semester has shifted from RPM to ARC-AGI, that prior structure is still useful for planning because it strongly suggests the value of building a clean Python repository, keeping milestone notes as you go, and treating the report as a parallel deliverable rather than an afterthought.[cite:54][cite:56]

## What is in this starter pack

- `arc_agi_project_guide.md`: a detailed planning guide connecting KBAI topics to ARC-AGI, proposing milestones, and outlining how to think about reports in JDF.[cite:56][web:79][web:86]
- `src/`: a lightweight Python scaffold for experimenting with ARC-style tasks using explicit knowledge-based representations and primitive transformations.[web:73][web:86]
- `reports/jdf_report_outline.md`: a JDF-ready report outline that mirrors the style of milestone journals and final reports described in the syllabus.[cite:54]
- `notes/experiment_log_template.md`: a lightweight log template to make later report writing easier.[cite:54]

## Why this structure matches the course

The syllabus says mini-projects and the semester project both separate code submission from writeup submission, and the semester project expects a longer final report that explains how the agent works, where it succeeds, where it struggles, and how it compares to human reasoning.[cite:54] That means the best early preparation is not only writing code, but also building a habit of documenting representations, reasoning methods, successes, failures, and revisions in a way that can later be turned into a JDF report.[cite:54]

The syllabus also says project code is expected in Python and highlights agent-style starter frameworks with a single main entry point plus support files.[cite:54] This starter pack follows that same spirit by giving you a small, modular Python codebase rather than a monolithic solver, because ARC-AGI will likely reward experimentation with multiple knowledge-based methods rather than one giant opaque routine.[web:73][web:79][web:86]

## Suggested use

Start by reading `arc_agi_project_guide.md`, then use the scaffold in `src/` to build one small capability at a time: grid parsing, object extraction, primitive transformations, candidate rule evaluation, and failure analysis.[web:73][web:86] As you test ideas, keep notes in the experiment log so that by the time the actual assignment appears, you already have the raw material for milestone journals and the final JDF report.[cite:54]
