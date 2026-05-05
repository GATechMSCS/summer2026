# ARC-AGI Project Guide for CS7637

This document is a planning guide for approaching an ARC-AGI semester project in a way that matches the spirit of CS7637’s semester-long agent project structure from the Summer 2024 syllabus: an individual Python project, milestone-style progress, code submitted separately from written work, and JDF-based reports exported to PDF.[cite:54][cite:56] It is not a claim that the Summer 2026 ARC-AGI project will be identical in every detail to the older RPM project; instead, it uses the older syllabus as a strong prior for what kinds of deliverables and habits are likely to matter.[cite:54]

## What the syllabus suggests you should expect

The Summer 2024 syllabus says the semester-long project was broken into four milestones plus a final project, and that each milestone and the final submission were graded half on performance and half on a written report.[cite:54] It also says those reports had to be written in JDF, submitted to Canvas as PDFs, and that the code was submitted separately to Gradescope.[cite:54]

The syllabus further says the final project report should explain how the agent works, provide performance metrics, describe multiple problems the agent solves correctly, analyze multiple failures, and reflect on the relationship between the agent’s reasoning and human reasoning.[cite:54] Even if ARC-AGI changes the benchmark itself, those expectations are incredibly useful because they imply that the course values not just performance, but clear explanation, reflection, and authentic connection to KBAI concepts.[cite:54]

The same syllabus also emphasizes that the project is an individual assignment, that code reuse must be cited carefully, that direct copying from AI systems is not allowed in submissions, and that students should not post their actual project code publicly.[cite:54] So a good repository structure should help you keep your own work organized, document sources cleanly, and preserve a private working history.[cite:54]

## ARC-AGI as a KBAI project

ARC-AGI is a benchmark built around solving novel visual reasoning tasks from only a few examples, which aligns naturally with KBAI’s emphasis on abstraction, analogical reasoning, concept learning, explicit representations, and metacognition.[web:79][web:86] The original ARC repository provides task files with a small number of input-output training examples plus a test input, and the ARC Prize guide frames the benchmark around strong priors such as objectness, geometry, and number rather than large-scale memorization.[web:73][web:86]

That makes ARC-AGI a strong fit for the course because almost every major KBAI topic can be interpreted as a module in an ARC agent: frames for object representation, generate-and-test for candidate rules, analogy for structural transfer, version spaces for maintaining multiple hypotheses, diagnosis for failure analysis, and meta-reasoning for strategy selection.[web:79][web:86]

## How the KBAI topics relate to ARC-AGI

### Lessons 1–7: representation and problem solving foundations

- **Intro to KBAI / Intro to CS7637**: sets the expectation that intelligence is not a single algorithm, but an organized architecture of representation, reasoning, learning, and memory.[cite:54]
- **Semantic Networks**: useful for representing objects and relations such as adjacency, containment, alignment, color, symmetry, and repetition inside a grid.[web:86]
- **Generate & Test**: one of the most natural baseline approaches for ARC, where the agent proposes transformations and checks them against training examples.[web:73][web:86]
- **Means-Ends Analysis**: useful when comparing a candidate output to a target output and asking what operation would reduce the difference.[web:79]
- **Production Systems**: a clean way to express transformation heuristics as condition-action rules.[web:79]
- **Frames**: especially valuable for representing ARC objects with slots like color, area, centroid, bounding box, shape signature, and relational roles.[web:86]

### Lessons 8–14: memory, learning, and understanding

- **Learning by Recording Cases / Case-Based Reasoning**: supports storing solved puzzle types and reusing them for similar tasks.[web:86]
- **Incremental Concept Learning / Classification**: helps form categories of ARC tasks such as symmetry, counting, object completion, recoloring, or object movement.[web:86]
- **Logic**: useful for writing explicit tests and constraints over candidate hypotheses.[web:73]
- **Planning**: relevant when a solution requires composing multiple primitive transformations instead of a single one-step rule.[web:79]
- **Understanding**: helps with disambiguation and representing a puzzle as a meaningful transformation process rather than as raw image differences.[web:86]

### Lessons 15–20: richer generalization mechanisms

- **Common Sense Reasoning**: inspires the use of primitive transformations and state changes at the object level.[web:86]
- **Scripts**: can be reinterpreted as recurring puzzle templates or transformation families.[web:79]
- **Explanation-Based Learning**: highly relevant for learning a reusable transformation from one or two examples when strong prior knowledge is available.[web:79][web:86]
- **Analogical Reasoning**: valuable when two tasks differ on the surface but share the same deep relational pattern.[web:86]
- **Version Spaces**: useful for maintaining multiple transformation hypotheses until the examples eliminate all but a few.[web:86]
- **Constraint Propagation**: important when local constraints such as symmetry, adjacency, or object counts can prune large parts of the search space.[web:86]

### Lessons 21–26: application, repair, and synthesis

- **Configuration**: useful when the output grid can be treated as a structured arrangement that must satisfy learned constraints.[web:79]
- **Diagnosis**: useful when a transformation fails and the agent must explain why.[web:79]
- **Learning by Correcting Mistakes**: turns mismatches between predicted and actual outputs into targeted revision.[web:79]
- **Meta-Reasoning**: probably one of the most important topics for ARC because a general solver likely needs to decide which strategy family to try first and when to switch.[web:79][web:86]
- **Advanced Topics / Wrap-Up**: reinforce that visuospatial reasoning, analogical representations, heuristics, and method-task matching are likely to matter more than any single generic algorithm.[cite:54][web:79]

## A practical early architecture for your Python repo

The syllabus’s older RPM project used an agent framework with a main entry point and additional support files, all in Python.[cite:54] A good ARC-AGI equivalent is a repository that separates representation, transformations, hypothesis generation, evaluation, and diagnostics so that each part can evolve without the code becoming unreadable.[cite:54][web:73]

A good first-pass architecture is:

- `src/task_io.py`: load ARC tasks and normalize them into simple Python objects.[web:73]
- `src/grid_ops.py`: utility functions for connected components, bounding boxes, colors, cropping, reflections, rotations, and comparisons.[web:86]
- `src/objects.py`: object extraction and frame-style representations.[web:86]
- `src/primitives.py`: primitive transformations such as recolor, translate, reflect, duplicate, delete, fill, and scale.[web:86]
- `src/hypotheses.py`: candidate transformation rules and compositions of rules.[web:79]
- `src/solver.py`: a simple generate-and-test loop with hooks for analogy or constraint-based pruning.[web:73][web:86]
- `src/diagnostics.py`: tools for comparing predictions to expected outputs and explaining failure modes.[web:79]
- `src/main.py`: a lightweight runner for experiments.[web:73]

## What to build first

The best early goal is not a full benchmark-winning solver, but a compact system that can solve a small, interpretable subset of tasks and explain what it is doing.[web:86] That will give you better material for milestone journals and a better conceptual fit with KBAI than rushing into a huge codebase too early.[cite:54]

A strong implementation order is:

1. Load and display tasks cleanly.[web:73]
2. Detect objects using connected components and simple color segmentation.[web:86]
3. Build frame-like object summaries with slots for size, position, color, and shape cues.[web:86]
4. Implement a handful of primitive transformations.[web:86]
5. Implement generate-and-test over those transformations.[web:73]
6. Add diagnostics that say why a candidate rule failed.[web:79]
7. Add strategy selection so the system can choose among color-based, object-based, and relation-based approaches.[web:79][web:86]

## Suggested milestone plan before the official details arrive

This milestone plan mirrors the pacing logic of the older project without assuming the exact official deliverables will be identical.[cite:54]

### Milestone 0: infrastructure and representation

Goal: parse tasks, print grids, and inspect objects. The milestone writeup would focus on how a human sees ARC tasks, what object-level representations seem natural, and what KBAI concepts appear most relevant.[cite:54][web:73][web:86]

### Milestone 1: primitive transformations and baseline solver

Goal: solve a small subset of tasks using a simple generate-and-test loop over primitive transformations.[web:73][web:86] The writeup would explain your transformation vocabulary, what kinds of tasks the baseline can solve, and what it fails to capture.

### Milestone 2: object-based reasoning

Goal: move beyond whole-grid transformations to object extraction, object matching, and relational reasoning.[web:86] The writeup would highlight how frames, semantic relations, and classification improve performance.

### Milestone 3: multiple strategies

Goal: add case-based retrieval, analogy, version-space-style pruning, or constraint propagation so the agent can choose among several approaches.[web:79][web:86] The writeup would focus on strategy selection and tradeoffs.

### Milestone 4: diagnosis and revision

Goal: build explicit failure analysis and improve the agent based on recurring error patterns.[web:79] The writeup would be centered on diagnosis, credit assignment, and the role of metacognition.

### Final report

Goal: present the overall architecture, quantitative and qualitative performance, representative successes, representative failures, and reflection on how the system compares to human reasoning.[cite:54]

## How to think about JDF reports for this project

The syllabus says milestone journals are shorter and more exploratory, while the final report is more formal and can run up to 10 pages, with appendices allowed but not graded.[cite:54] That suggests a good internal writing habit: keep a living record of representations, hypotheses, test cases, results, and diagrams so that later reports feel like synthesis rather than reconstruction.[cite:54]

A good JDF report structure for ARC-AGI would be:

1. **Introduction**: what ARC-AGI is and why it is a useful KBAI benchmark.[web:79][web:86]
2. **Human approach**: how a person might look at the tasks and decide what matters.[cite:54]
3. **Agent design**: representations, primitives, strategies, and control flow.[web:73][web:86]
4. **Performance**: metrics and a breakdown by task style if possible.[cite:54]
5. **Success cases**: several tasks solved correctly, with step-by-step reasoning.[cite:54]
6. **Failure cases**: several tasks not solved correctly, with diagnosis of what broke.[cite:54][web:79]
7. **Reflection**: how the agent compares to human reasoning and how KBAI concepts shaped the design.[cite:54]

## Habits that will save time later

- Keep screenshots or rendered grids for representative successes and failures.[cite:54]
- Log why a hypothesis was chosen, not just whether it worked.[web:79]
- Group tasks by pattern family as soon as you notice recurring structures.[web:86]
- Treat every failure as possible evidence for a missing representation, primitive, or strategy rather than just “wrong answer.”[web:79]
- Write in plain language first, then translate into course terminology for the report.[cite:54]

## What not to do

The syllabus strongly discourages brute-force or autograder-probing behavior and emphasizes authentic reasoning approaches.[cite:54] For ARC-AGI, that means avoiding a mindset of trying to exploit benchmark quirks and instead focusing on representations and reasoning processes you could actually explain and defend in a JDF report.[cite:54][web:79]

It also means not waiting for the official assignment page before beginning. The old syllabus explicitly encouraged early infrastructure setup for the project, and the same logic applies here: building a parser, object extractor, and experiment log now is low-risk, high-value prep.[cite:54]

## Most useful takeaway

The best early preparation for the ARC-AGI project is to combine three things: a private Python experimentation repo, a steady habit of JDF-friendly note-taking, and a design philosophy grounded in KBAI topics rather than generic machine learning buzzwords.[cite:54][cite:56][web:79] That combination will make it much easier to adapt once the exact Summer 2026 project details appear.[cite:58][cite:54]
