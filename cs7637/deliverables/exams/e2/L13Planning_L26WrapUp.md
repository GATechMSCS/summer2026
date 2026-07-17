Downloaded From: https://github.com/stevenxchung/OMSCS-Notes/tree/master/CS%207637%20-%20KBAI

# Lesson 13

An intelligent agent maps perceptual histories into actions. Consequently, _planning_ is a powerful tool for action selection. In this lesson we will cover:

1. States, goals, and operators
2. Conflicts in planning
3. Partial-order planning
4. Hierarchical task networks

## Planning And State Spaces

Referring back to state spaces, a search method is inefficient because it uses no knowledge. Since we have knowledge of the goal and asset knowledge (i.e., how to select an operator), we could better select actions which allow us to obtain our goal as we saw with means-ends analysis.

Planning provides more systematic processes for selecting different operators. How to we do operator selection? We can do this the same way as mapping perceptual histories into actions. Operators represent mental representations of actions available in the world.

## Planning

In means-ends analysis we saw that we could generate states which make it impossible to achieve the goal. This is also know as **goal clobbering** a linear planning technique (e.g., means-ends analysis) that goes about generating states without reasoning conflicts which could block the goal state. How might an intelligent agent be able to reason about the order of actions such that the goal is achieved?

## Partial-order Planning

**Partial-order planning** occurs when there are multiple goals and the plan for achieving one goal clobbers with another.

## Detecting Conflicts

How might a planner detect conflicts?

For each precondition in the current plan:

- If pre-condition for an operator in the current plan is clobbered by a state in another plan:
  - Promote current plan's goal above the other plan's goal

## Open Preconditions

How does partial-order planning work in practice? We can begin to understand by examining the following principles:

1. Knowledge is not just about the world but it is control knowledge which helps us select between operators
2. Goals provide us control knowledge as they can be used to decide between different operators which help us move closer to the goal
3. We can view partial-order planning as an interaction between several different agents or abilities where each agent represents a small micro ability:
   - An agent that helps us generate plans for each goal independently
   - An agent that is responsible for detecting conflicts between them
   - An agent that is responsible for resolving these conflicts

## Hierarchical Task Network Planning

Referring to our partial order planning exercises, can we abstract some operations at a higher-level? The idea here is to make the the problem space much smaller and simpler to navigate.

## Hierarchical Decomposition

Referring to the block exercises, we can decompose several higher-level operations into micro-operations which may include definitions on pre-conditions, post-conditions, and methods.

## Hierarchical Planning

Most real-world problems have a large and complex problem space. In order for AI agents to handle such problems, it must be able to think at multiple levels of abstraction. An AI agent must be able to use knowledge at various levels of abstraction in order to solve difficult problems.

## Section Quizzes

### Partial Order Planning I Quiz

_Write the current and goal states in propositional logic_.

1. `On(D, B) ˄ On(B, A) ˄ On(A, C) ˄ On(C, Table)`
2. `On(A, B) ˄ On(B, C) ˄ On(C, D) ˄ On(D, Table)`

### Partial Order Planning II Quiz

_Write the pre- and post-conditions for the two Move operators_.

1. `Clear(x) ˄ Clear(y)`
2. `On(x, y)`
3. `Clear(x)`
4. `On(x, Table)`

### Partial Order Planning III Quiz

_Write plans for accomplishing each goal_.

1. `Move(D, Table) Move(B, Table) Move(A, B)`
2. `Move(D, Table) Move(B, Table) Move(A, Table) Move(B, C)`
3. `Move(D, Table) Move(B, Table) Move(A, Table) Move(C, D)`

### Partial Order Planning IV Quiz

_Use partial-order planning to order the plans_.

1. 3rd
2. 2nd
3. 1st

### Partial Order Planning V Quiz

_Write a final plan for converting the current state to the goal state_.

1. `Move(D, Table) Move(B, Table) Move(A, Table) Move(C, D) Move(B, C) Move(A,B)`

### Final Quiz

_What did you learn in this lesson_?

- Planning is a process central to cognition as action selection is central to cognition
- Planning is required to select the appropriate action
- Control knowledge helps us select different actions and operators
- Intelligent agents can deal with goal clobbering by detecting conflicts with one micro agent and resolving conflicts with another agent
- Intelligent agents simplify large complex problems by using knowledge at many layers of abstraction to reduce the problem space and tackle hard problems

# Lesson 14

In this lesson we will examine an intelligent agent's _understanding_ of events and stories in the world which will build on our frame concepts. We cover the following:

1. Thematic role systems
2. Ambiguity
3. Constraints

## Thematic Role Systems

A **thematic role system** is a type of frame representation system where the frame represents an action or event identified by a verb. In these frames, the verb is able to establish expectations about the roles that are connected to that particular event.

Consider the following sentence:

> Ashok made pancakes for David with a griddle

The frame representation could be as follows:

Thematic Role:

- Verb: make
- Agent: Ashok
- Beneficiary: David
- Thematic object: pancakes
- Instrument: griddle

This frame will allow us to draw inferences which will allow an agent to understand the meaning of the sentence.

## Constraints

**Constraints** also allow an agent to understand the meaning of a sentence. Below are some prepositional constraints:

| Preposition | Thematic Roles              |
| ----------- | --------------------------- |
| by          | agent, conveyance, location |
| for         | beneficiary, duration       |
| from        | source                      |
| to          | destination                 |
| with        | co-agent, instrument        |

## Resolving Ambiguity In Prepositions

However, there may exist ambiguity in sentences such as below where the word _by_ has different thematic roles:

> That was written by Ashok.
> David went to New York by train.
> David stood by the statue.

How to resolve these issues? The agent should have an _ontology_ of the world. That is, it has a conceptualization or model of the world (in lecture it looks like a tree with multiple branches) such that it is able to determine which thematic role _by_ takes in each sentence above.

## Resolving Ambiguity In Verbs

Verbs can also have many different meanings. To resolve ambiguity in verbs, we can create a frame for each meaning of the verb and then eliminate the frames that do not match the verb used in the sentence. This could be done by examining other parts of the sentence and using that knowledge to eliminate ambiguities.

## Section Quizzes

### Thematic Role Systems Quiz

_Consider the following sentence_:

> David went to the meeting with Ashok by car.

_Write the thematic role frame given by the sentence above_.

Thematic Role:

- Verb: went
- Agent: David
- Co-agent: Ashok
- Destination: meeting
- Conveyance: car

### Resolving Ambiguity In Verbs Quiz

_Use the thematic role frames below (provided) to identify the meaning of "take" in the sentence_:

1. _I took an aspirin for my headache_. D, to medicate
2. _I took my briefcase to work today_. B, to bring or transport
3. _I took the casino for \$5 million_. G, to cheat or swindle

### Final Quiz

_What did you learn in this lesson_?

- Understanding is a very general all-purpose cognitive task that has a goal of making sense of the world
- The world constantly bombards us with many different types of data but we could make sense of the world by using constraints, structured knowledge representations, and lower-level bottom-up processing
- Lower-level bottom-up processing helps us activate knowledge structures from memory which then in turn helps us generate expectations (a top-down processing task)

# Lesson 15

In this lesson we will examine how we could make an AI agent have common sensical inferences about the world. This wil involve pulling concepts from frame representation. We will also cover the following:

1. Primitive actions
2. Actions and sub-actions
3. State changes

## Primitive Actions

We can start examining how an AI agent might interpret very structurally different sentences that have the same meaning by noting **primitive actions**. These set of basic actions (e.g., move-body-part, move-object, etc.) could help an agent interpret a message as each primitive action has a frame representation associated with it which allows for stereotyping.

## Thematic Roles And Primitive Actions

As mentioned earlier, an agent may map actions in a sentence to a store containing primitive actions. These primitive actions may be represented in a thematic role frame which will allow the agent to perform top-down processing(generating expectations and interpretations).

## Implied Actions

Oftentimes a sentence might be difficult to interpret because the action does not readily map to any primitive action. In this scenario an agent might modify the sentence such that it could map to a primitive action.

## Actions And Sub-actions

What knowledge must an AI agent have such that it could make common sense inferences? Referring back to the thematic role frames, we would add to the frame not only the primitive action, agent, and object but also sub-actions.

## State Changes

A **state-change frame** may highlight different events that may occur in a given sentence. This may be inserted into a thematic role frame as a result (e.g., the result of _Ashok ate a frog_ may contain a state-change frame representing the result: _Ashok is happy_)

## Implied Actions And State Changes

Sometimes a sentence might be vague (e.g., _Susan comforted Jing_) and so the best we can do with primitive actions, thematic role frames, and state-change frames is to generalize an action.

## Actions And Resultant Actions

Thematic role frames are not limited to chaining results to state-change frames but also results to another thematic role frame (action result to another action). This is useful for sentences which contain more than one action (e.g., _Maria told Ben to throw the ball_).

## Section Quizzes

### Primitive Actions Quiz

_Write the primitive action that subsumes the verbs in the following sentences (given)_.

1. Ran
2. Pushed
3. Took
4. Ate

### Roles And Primitive Actions Quiz

_Write the action frame corresponding to the above sentence (given) using a primitive action_.

1. Move-possession
2. John
3. Mary
4. Book

### Implied Actions Quiz

_Rewrite the sentence (given) in the form of a primitive action, then construct an action frame for the sentence_.

1. Bill propelled a bullet into Bob
2. Propel
3. Bill
4. Bullet
5. Bob

### State Changes Quiz

_Complete the frame representations for these sentences (given)_.

_Sentence 1: Anika decided to have a glass of water_.

1. Action
2. Conclude; Anika
3. Action
4. Ingest; Anika; glass of water
5. Action
6. See, Marc, TED talks
7. Action
8. Marc's mood, happy

### Final Quiz

_What did you learn in this lesson_?

- Agents may interpret sentences by using primitive actions which map to thematic role frames. These frames may contain results or sub-actions which could provide more information to the Agent during top-down processing where the agent generates expectations
- We use notion of goals and context to decide what to do and what not to do. A similar notion of context is used in order to understand natural language understanding
- We could use context to disambiguate between various meanings of some action
- We make inferences about the world around us using the _TOM (Theory of Mind) Theory_ in which we ascribe goals, beliefs, and desires to each other

# Lesson 16

In this lesson we cover another knowledge representation known as _scripts_ which allow us to make sense of discourses, stories, and scenes using previous concepts (e.g., frames, understanding, and common sense reasoning). We will cover the following:

1. Defining scripts
2. Form vs. content
3. Generating expectations
4. Hierarchies of scripts

## Story Understanding For AI Agents

Stories can help agents make sense of the world and generate expectations. Stories also allows an agent to make connections between events that otherwise might appear separate.

## Definition Of Scripts

A **script** is a knowledge representation for capturing a causally coherent set of events. There are three parts to this definition:

1. **Causally**: each event sets off or causes the next event
2. **Coherent**: the causal connections between events make sense
3. **Events**: the parts are actions or scenes in the world

## Parts Of A Script

There are six parts to a script:

1. **Entry conditions**: conditions necessary to execute the script
2. **Result**: conditions that will be true after the script has taken place
3. **Props**: objects involved in the execution of the script
4. **Roles**: agents involved in the execution of the script
5. **Track**: variations or _sub-classes_ of the particular script
6. **Scenes**: the sequence of events that occurs during execution of the script

## Using A Script To Generate Expectations

A script can be used to generate expectations since a script may generate a chain of thematic role frames (a scene) which captures a causally coherent set of events. If any of the events in the scene do not occur the agent will know that the outcome is unexpected.

These types of surprises lends itself to the theory of creativity where a situation is creative if it is:

1. Novel
2. Useful or valuable
3. Unexpected or surprising

## Tracks

For each script, there may be different _tracks_ i.e., for a script that is written for _going to a restaurant or food establishment_ there may be a script for going to a coffeehouse, fast food, causal dining, formal dining, etc. Additionally, there may also be a higher level of abstraction for these events, e.g., _going to different types of social events_ not just restaurants.

## Learning A Script

The following prior topics may help an agent learn a script:

- **Semantic networks**: can help an agent store knowledge in the form of structured representation
- **Frames**: same as semantic networks but the structure for storing information is different
- **Incremental concept learning**: an agent which constantly interacts with the world could use this technique to develop a categorization scheme for different experiences
- **Planning**: can help an agent realize a path from initial state to the goal state and translate that path into a script such that the same script could be used for other scenarios
- **Common sense reasoning**: can help an agent process a script with primitive actions

## Using A Script

The following prior topics may help an agent use a script:

- **Problem reduction**: this technique can help an agent break down a scene into smaller scenes (collection of frames) and actions such that exceptions and violations are caught
- **Classification**: can help an agent determine what script to use given a particular situation
- **Logic**: since a plan can discussed in formal logic an agent could use this technique to determine what the script asserts about the state of the world at certain points of execution
- **Understanding**: can help an agent disambiguate similar events in different situations

## Section Quizzes

### Final Quiz

_What did you learn in this lesson_?

- Stories can help agents make sense of the world and generate expectations. This possible as scripts are a knowledge representation for capturing a causally coherent set of events
- Some theories say that our brain is a predictor machine. We do quick bottom-up processing followed by top-down processing. We also generate expectations of the world and then act on those expectations
- One of the questions is _do we carry these scripts in our head or do we generate them at runtime_?
- Scripts are analogous to mental models and are culturally specific (e.g., the script for tipping in the US is different than in other countries)

# Lesson 17

In _explanation-based learning_ an agent learns about new connections between existing concepts rather than learning about new concepts. Explanation-based learning could be used to introduce the notion of knowledge transfer from an old situation to a new situation. We will cover the following:

1. Concept space
2. Abstraction
3. Analogical transfer

## Concept Space

An agent might represent concepts with facts about a particular concept in the form of a concept space. What prior knowledge does an agent need to build explanations? An agent might have prior knowledge of various concepts such that a causual connection could be made between them.

## Abstraction

An agent might make use of prior knowledge in a concept space and abstract the causual connections between various concepts to come up with a solution or explanation to a problem.

## Transfer

Knowledge transfer occurs by using abstractions of concepts (obtained from prior knowledge) in the concept space and connecting those abstractions to form a new causual connection to a new concept. In practice, an agent typically starts from the given new concept and looks for ways it could draw in prior knowledge to understand a new concept by connecting top-level abstractions (which are goals for the agent to prove) to those in memory.

## Section Quizzes

### Transporting Soup Quiz

_Which of these might be useful for transporting soup from the kitchen to the table_?

The glass pitcher is most useful in this scenario.

### Explanation-based Learning I Quiz

_Given the prior knowledge (provided), can we prove this object is a mug_?

No since the prior knowledge for a mug does not have causal connections which link to the given mystery object.

### Explanation-based Learning II Quiz

_What knowledge would finish our proof that this object (given) is a mug_?

- Knowledge of a wooden spoon
- Knowledge of an oven mitt

### Final Quiz

_What did you learn in this lesson_?

- We as humans are always dealing with novel situations and we create solutions to those situations by forming connections between existing concepts
- Using existing concepts in new ways is known as _speed up learning_ as it builds connections between existing concepts to learn new concepts
- We can only explain things that are consciously accessible (e.g., we cannot easily explain memory processes)
- Although the process for generating explanations may be similar to arriving to a particular decision it is not the same process used in making a decision

# Lesson 18

**Analogical reasoning** involves understanding new problems in terms of a family of problems and transferring knowledge of relationships from known problems across domains. We will cover the following:

1. Similarity and case-based reasoning
2. Process of analogical reasoning
3. Design by analogy

## Need For Cross-domain Analogy

Cross domain connections allow an agent to solve new problems based on existing knowledge in some domain. An agent will do this by abstracting out relationships between concepts from one domain to another. These relationships are important because they are the knowledge that is transferred from the source case to the target problem.

## Spectrum Of Similarity

Shown below is table for spectrum of similarity between different KBAI methods from more similar with recording cases to less similar with analogical reasoning:

| Method               | Relations | Objects | Features | Values |
| -------------------- | --------- | ------- | -------- | ------ |
| Recording Cases      | S         | S       | S        | S      |
| Case-based Reasoning | S         | S       | S        | D      |
| Case-based Reasoning | S         | S       | D        | D      |
| Analogical Reasoning | S         | D       | D        | D      |

Where _S_ is for similar and _D_ is for dissimilar

## Process Of Analogical Reasoning

Analogical reasoning consists of five different phases which are usually not linear:

1. Retrieval
2. Mapping
3. Transfer
4. Evaluation
5. Storage

This is just one of the many models on analogical reasoning. Recall that case-based reasoning had the following steps:

1. Retrieval
2. Adaptation
3. Evaluation
4. Storage

Therefore, one of the main differences for analogical reasoning lies within the mapping step where an agent must determine the mapping between relations, objects, features, and values from the source case to the target problem. Once those mappings are determined then knowledge transfer of abstracted relationships from one domain to another can occur.

## Three Types Of Similarity

There are various types of similarity:

1. **Semantic**: conceptual similarity between the target problem an the source case
2. **Pragmatic**: similarity of external factors such as goals
3. **Structural**: similarity between representation structures

## Analogical Mapping

The key for analogical mapping is to look at deep relationships between concepts within a domain rather than looking for superficial relationships. By examining higher order relationships in the source case would allow an agent to map those relationships to the target problem.

## Analogical Transfer

Once an agent understand the mapping between the source case and the target problem the agent could also apply the solution from the source case to the target problem though a strategy transfer. Through this transfer an agent applies abstracted patterns from the source case to the target problem.

## Advanced And Open Issues In Analogy

There are several of advanced topics which have open issues in AI analogy:

- Common vocabulary
- Abstraction and transformation
- Compound and compositional analogies
- Visuospatial analogies
- Conceptual combination

## Section Quizzes

### Similarity Ratings Quiz

> A woman is climbing a ladder

_Which of the situations below is most similar to the situation above_?

1. 2
2. 3
3. 6
4. 4
5. 7
6. 1
7. 5

### Analogical Retrieval I Quiz

> A woman is climbing a ladder

_Mark whether each situation has deep similarity, superficial similarity, both, or neither with the situation above_.

1. Deep and superficial
2. Deep
3. Superficial
4. Deep
5. Neither
6. Deep and superficial
7. Deep

### Analogical Retrieval II Quiz

_What are the deep similarities between these two models (given)_?

- Something revolves around something else
- A force exists between two objects
- Two objects attract each other

### Analogical Mapping Quiz

_How would you map the solar system to the atomic structure_?

- Sun would map to a nucleus
- Planet would map to an electron

### Analogical Transfer Quiz

_What would be transferred into the atomic structure model_?

- Nucleus has mass
- Electron has mass
- Nucleus's mass greater than electron's mass

### Final Quiz

_What did you learn in this lesson_?

- Cross domain analogy is needed in order for an agent to understand a problem in terms of a family of problems and transfer abstract relationship knowledge from one domain to another
- There are many types of relationships on different levels, we think about relationships between objects, features, and values to be on the superficial level whereas relationships of relationships are on a deeper level
- Deep relationships allow an agent to correctly retrieve and map a source case to a target problem such that a strategy could be applied to the target problem
- Analogy is often thought to be a core process of cognition

# Lesson 19

In this lesson we will cover generalization and learning using _version spaces_. Generalization and learning are closely related to incremental concept learning (learning by one step at a time) which relied on background knowledge. Generalization and learning is useful in cases where background knowledge might not be available. We will also cover the following:

1. Version space definition
2. Abstract version spaces
3. Algorithm for version spaces
4. Identification trees

## Incremental Concept Learning Revisited

**Version spaces** are a technique for learning concepts incrementally. In incremental concept learning, concepts are introduced in an order such that concepts may be refined desirably. We also made use of background knowledge to help us further generalize or specialize our model of a concept (e.g., model of an arch).

However, there are many scenarios where a concept is not introduced in a useful order and background knowledge is not provided. In these scenarios, version spaces are useful in that it will allow an agent to converge to a refined concept.

## Abstract Version Spaces

Version spaces always have a general model and a specific model attached to the concept we are trying to learn:

- **Generalized model progression**: as more _negative_ examples are given, the descriptions of this model become more _specialized_
- **Specialized model progression**: as more _positive_ examples are given, the descriptions of this model become more _generalized_

We could observe then that generalized and specialized models must converge at some point where an ideal model exists.

## Version Spaces Algorithm

The algorithm for version spaces could be summarized as follows:

- For each example:
  - If the example is _positive_:
    - _Generalize_ all _specific_ models to include it
    - Prune away _general_ models that cannot include it
  - If the example is _negative_:
    - _Specialize_ all general models to include it
    - Prune away _specific_ models that cannot include it
  - Prune away any models _subsumed_ by other models

## Identification Trees

To build more efficient and optimal classification trees we could create a tree where attributes are _carefully_ selected such that examples could be separated out to their own branch. This technique to use classification trees to find examples is called _decision tree learning_. However, the tradeoff is that we need to know all the examples in order to create such a tree.

There are some differences between decision trees and discrimination trees (discussed in incremental learning):

- Decision trees are more optimal classification trees but we need all examples upfront
- Discrimination trees are sub-optimal trees but we can use them to learn incrementally

## Section Quizzes

### Version Spaces I Quiz

_What would the initial general and specific models be (based on given frame)_?

- General model has `any` for all
- Specific model includes everything in the given frame

### Version Spaces II Quiz

_Based on this example (given), would we generalize or specialize_?

We should generalize since it is a positive example.

### Version Spaces III Quiz

_After generalizing, what will the general model be_?

1. Kim's
2. Any
3. Friday
4. Cheap
5. No

### Version Spaces IV Quiz

_Based on this example (given), would we generalize or specialize_?

We should specialize since it is a negative example.

### Version Spaces V Quiz

_How many potential general models will we have after specializing based on this case (given) and pruning_?

Possibly 3 since we can specialize for:

- Kim's
- Breakfast
- Friday

### Version Spaces VI Quiz

_What model did you converge on_?

1. Kim's
2. Any
3. Any
4. Cheap
5. No

### Final Quiz

_What did you learn in this lesson_?

- Version spaces are a technique that allows convergence to the right level of abstraction
- Version spaces are related to the concept of cognitive flexibility. This flexibility occurs when the agent has multiple characterizations or perspectives on the same concept. In version spaces, an agent has several possible definitions for a concept that converges over time
- An alternative view to version spaces is to start with a generalized version of a concept and then allow the world to give us feedback to refine our definition of a concept

# Lesson 20

In this lesson we will talk about _constraint propagation_ which is a general purpose problem solving method. **Constraint propagation** is a mechanism of inference where the agent assigns values to variables to satisfy certain conditions (constraints). We will cover the following:

1. Constraint propagation definition
2. Image processing
3. Natural language understanding
4. Advanced problems

## Constraint Propagation Defined

**Constraint propagation** is a method of inference that assigns values to variables characterizing a problem in such a way that some conditions (constraints) are satisfied.

## Section Quizzes

### Recognizing 3D Figures Quiz

_Which of these wireframes depicts a 3D figure that could exist in the real world_?

The first, third, fifth, and sixth figures likely exist in the real world.

### Gibberish Sentences Quiz

_Which of these sentences are grammatically correct_?

- Colorless green ideas sleep furiously
- Wall decor notifies business cards of nonsensical whims
- Tuesday brought a sharp-edged suite of pumpernickel

### Assembling The Cube I Quiz

_Label each intersection according to the applicable constraint on the right (given)_.

1. L
2. W
3. L
4. Y
5. W
6. W
7. L

### Assembling The Cube II Quiz

_Please fill in the blanks for the corresponding line according to the constraint on the right below (given)_.

- Blades: 1, 3-5, 8, 9
- Folds: 2, 6, 7

### Final Quiz

_What did you learn in this lesson_?

- Constraint propagation is a very generalized method like means-ends analysis and it allows us to use our knowledge of the world to make sense of concepts
- Constraint propagation works by assigning values to variables such that a problem satisfies constraints

# Lesson 21

In this lesson we will cover _configuration_ which is a routine kind of design task in which all the components of the design are already known. The task of configuration is to assign values to the variables of those components so they could be arranged according to some constraints. We will cover the following:

1. Design and configuration
2. Plan refinement
3. Connections to earlier topics

## Define Design

**Design** takes in needs, goals, or functions and returns the specification and structure of some artifact that satisfies those needs, goals, and functions. The artifact does not need to a physical product, it could be a process, program, or policy.

Design is very broad, open ended, and undefined. In problem solving, typically the problem remains fixed even as the solution evolves. However in design, both the problem and the solution co-evolve (the problem evolves as the solution evolves). One of the goals of KBAI is building intelligent agents which can design.

## Defining Configuration

**Configuration** is a problem solving activity that assigns values to variables to satisfy constraints.

## The Configuration Process

The configuration process is as follows:

1. **Specification space**: which provides specification to structure mapping and receives additional specifications if arrangement model evolves
2. **Abstract and partial solutions**: the beginning state when solutioning
3. **Solution refinement and expansion**: includes pulling abstraction and component hierarchy from the configuration space
4. **Expanded and refined solutions**: the end state of solutioning
5. **Arrangement model**: the output of the configuration process which could also be refined

## Connection To Classification

Classification and configuration are both hierarchical. Configuration leverages classification's notion of prototype concepts.

We use _classification_ to make sense of the world by mapping combinations of percepts equal to its process. We use _configuration_ to act on the world by designing actions. So while _classification_ is a way to make sense of the world, _configuration_ is a way of creating the world.

## Contrast With Case-based Reasoning

_Configuration_ suggests starting with a prototype concept and assigning values to variables. _Case-based reasoning_ suggests starting from a specific chair and tweaking it as needed.

## Connection To Planning

The result of a planning task can lead to a prototype that can subsequently be configured for similar problems with differing constraints.

## Section Quizzes

### Final Quiz

_What did you learn in this lesson_?

- Configuration is a routine design that occurs every day
- Configuration is a task that could be addressed by many methods (e.g., case-based reasoning, planning refinement, generate and test, etc.)
- The configuration process usually begins in the specification space and outputs an an _arrangement model_ in the configuration space through iterations of solutioning

# Lesson 22

In this lesson we will cover _diagnosis_ which identifies the faults responsible for a malfunctioning system. We will cover the following:

- Defining diagnosis
- Data and hypothesis spaces
- Mapping data to hypothesis
- Two views of diagnosis

## Defining Diagnosis

**Diagnosis** is to determine what is wrong with a malfunctioning device or what is the fault that causes a device to malfunction.

## Data Space And Hypothesis Space

We can think of diagnosis as a process that maps data from a _data space_ to a _hypothesis space_. In diagnosis the mapping between data from the data space to hypotheses in the hypothesis space is `N * N`. This can be very complicated very quickly.

Consequently, the data space is abstracted such that it could be mapped to an abstract hypothesis (bottom-up classification). Once an abstract hypothesis has been created, the next process is to refine the hypothesis such that the finalized hypothesis will maximize all data available in the data space (top-down classification).

## Problems With Diagnosis As Classification

There are several problems with diagnosis however:

1. One data point may map to multiple hypotheses
2. One hypothesis may map to multiple sets of data
3. Multiple hypothesis may map to multiple sets of data
4. Hypotheses may be mutually exclusive
5. Data points may interact

Point 5 is difficult to account for in practice so it is useful to shift from a sole classification approach to diagnosis to an abduction approach.

## Deduction - Induction - Abduction

Below highlights the steps for deduction, induction, and abduction:

1. **Deduction**: given the rule and the cause, deduce the effect (Modus Pones)
2. **Induction**: given a cause and an effect, induce a rule
3. **Abduction**: given a rule and an effect, abduce a cause (diagnosis)

While deduction is _truth preserving_, induction and abduction are not.

## Criteria For Choosing A Hypothesis

Below are criteria for choosing a hypothesis

1. Hypothesis must cover as much of the data as possible
2. The smallest number of hypothesis ought to be used
3. Some hypotheses may be more likely than others

## Completing The Process

To complete the diagnosis process an agent would need to transfer the hypothesis from the _hypothesis space_ and select the proper treatment (action) in the _treatment space_. Depending on the results of the treatment, the data gained from treatment would be fed into the _data space_ and thus the process begins again.

## Section Quizzes

### Diagnosing Illness Quiz

_What illness (or set of illnesses) would you use to diagnose this patient (given symptoms)_?

Thetadesis: Elevated B, Reduced C, Reduced H

### Diagnosis As Abduction Quiz

_What illness (or set of illnesses) would you use to diagnose this patient (given symptoms)_?

- Betatosis: Elevated B, Reduced C, Elevated E, Reduced H
- Zetad: Elevated B, Reduced C, Reduced E, Reduced F

### Final Quiz

_What did you learn in this lesson_?

- Diagnosis occurs whenever our expectations are violated such that we could determine the cause
- Diagnosis is a task which we could use several methods to address (e.g., case-based reasoning, etc.)
- Diagnosis is a very complicated classification task which may be untangled with the use of deduction, induction, or abduction

# Lesson 23

Another method of learning is _learning by correcting mistakes_. We will also cover the following:

1. Explanation-based learning revisited
2. Isolating mistakes
3. Explaining mistakes
4. Correcting mistakes

## Questions For Correcting Mistakes

How might an agent learn to correct its mistakes? There are three relevant follow-up questions to determine:

1. How can the agent isolate the error in its former model?
2. How can the agent explain the problem that led to the error?
3. How can the agent repair the model to prevent the error from recurring?

The problem of identifying the error in one's knowledge that led to a failure is called **credit assignment** (or _blame assignment_). This assignment is concerned about: when a failure occurs, what _gap_ in one's knowledge was responsible for the failure?

Generally an error could be in one's reasoning or architecture. Some experts consider credit assignment to be the central problem in learning since the world is dynamic and so what is learned today will need to be re-learned tomorrow.

## Visualizing Error Detection

Generally, errors for agents may lie in:

1. Knowledge
2. Reasoning
3. Architecture

In this class, we will be focusing primarily on errors in _classification knowledge_.

## Error Detection Algorithm

The error detection pseudo-code may be as follows:

1. To find suspicious _true-success_ relations:
   - Intersect all _true_ successes (⋂T)
   - Union all _false_ successes (⋃F)
   - Remove assertions in union form intersection (⋂T - ⋃F)
2. To find suspicious _false-success_ relations:
   - Intersect all _false_ successes (⋂F)
   - Union all _true_ successes (⋃T)
   - Remove assertions in union form intersection (⋂F - ⋃T)

## Explanation-free Repair

While classification is ubiquitous in many schools of AI, _explanation_ is a key characteristic of KBAI. Explanation leads to deeper learning because it explains why certain features are important for the concept definition.

## Connection To Incremental Concept Learning

When we discussed incremental concept learning we covered techniques for learning but we did not discuss how a learned concept would be used. Consequently, in _learning by correcting mistakes_, we examine how an agent actually uses the knowledge it learns. This is central to KBAI for the following reasons:

1. KBAI looks at reasoning and action to decide how knowledge is to be used and determines what knowledge it to be learned (i.e., agents sets a target for learning)
2. Agents do not learn to perform action selection but also to get feedback as the result of actions performed on the world

Learning by correcting mistakes views learning as a problem solving activity. This type of learning is closely intertwined with memory, reasoning, action, and feedback from the world.

Referring back to the cognitive model, the metacognition module also includes memory, reasoning, and learning as seen in the deliberation module. Metacognition will use these sub-processes to _fix_ errors in the deliberation module. In this view, metacognition could be said to allow an agent to _think_ about thinking.

## Section Quizzes

### Identifying A Cup

_Which of these objects are cups_?

The second, fourth, and sixth images are cups.

_Which of these objects meet our definition of a cup_?

All except the third image.

### Correcting The Mistake

_Is this a good way to fix this error (provided)_?

No, because it will cause incorrect decisions about other objects.

### Final Quiz

_What did you learn in this lesson_?

- Humans are rarely passive learners - we learn as active participants in the learning process
- Similarly, agents may use knowledge and reasoning to make sense of a video for example. This allows for generating expectations. However, some expectations may be violated and so the agent may try to generate an explanation for these errors in its knowledge and reasoning
- Metacognition from the cognitive model is really a module that allows an agent to _think_ about thinking i.e., it has its own sub-process like memory, reasoning, and learning to fix errors which may have occurred during a deliberation process when generating outputs

# Lesson 24

In this lesson we discuss **meta-reasoning** which is thinking about thinking (or knowledge about knowledge). Meta-reasoning is not concerned about an agent reasoning to determine an output to the world. Instead, meta-reasoning focuses on an agent's own internal knowledge, reasoning, and learning. We will cover the following:

1. Mistakes in knowledge, reasoning, and learning
2. Gaps in knowledge and reasoning
3. Strategy selection and integration
4. Meta-meta reasoning?
5. Goal-based autonomy

## Mistakes In Reasoning And Learning

Meta-reasoning allows an agent to explore the following:

1. How was this particular knowledge learned?
2. What was wrong in the learning process that led to that particular error?
3. How to fix the learning process such that the same mistakes are not made again?

## Beyond Mistakes: Knowledge Gaps

While an agent might discover an error (_incorrectness_) in the knowledge, reasoning, or learning, the agent should also consider gaps (_incompleteness_) in the knowledge, reasoning, or learning.

Gaps allow an agent to trigger a search (or spawn a goal) to find the link which will enable connection between concepts. The ability to spawn learning goals and find a way to achieve learning goals is another aspect of meta-cognition.

## The Blurred Line Between Cognition And Metacognition

The lines between deliberation (cognition) and metacognition are actually quite blurred as a considerable amount of processes overlap. In terms of KBAI, we should not be overly concerned about whether some processes occur in the deliberation or metacognition space. Instead, we should focus on:

1. What is the content that is needed for an agent to carry out a process?
2. What is the process that the agent needs to carry out?

## Strategy Selection

**Strategy selection** is facilitated by metacognition. Recall that some examples of reasoning strategies or methods are:

- Case-based reasoning
- Analogical reasoning
- Constraint propagation
- Planning
- Generate and test
- Problem reduction
- Means-ends analysis

Also recall that some examples of learning strategies or methods are:

- Explanation-based learning
- Learning by recording cases
- Incremental concept learning
- Classification
- Version spaces

Given a problem, the agent's metacognition selects a strategy based on the following criteria:

1. The agent will select an method based on knowledge of the world
2. If knowledge exists for competing methods, the agent must select the method which satisfies the most criteria for the given problem
3. The agent may evaluate the quality of solutions as well to select the proper strategy

## Strategy Integration

**Strategy integration** allows an agent to shift to another strategy when needed as the given problem evolves.

## Process Of Meta-reasoning

Metacognition could be used to:

1. Fix errors in knowledge, reasoning, or learning
2. Fill gaps in knowledge, reasoning, or learning
3. Strategy integration

However, what is the process or strategy that metacognition uses? Metacognition can use the **same** processes and strategies that deliberation uses. In this way, an agent can achieve _goal-based autonomy_ as metacognition is able to provide continuous robustness and flexibility by allowing an agent to achieve new goals.

## Section Quizzes

### Meta-meta Reasoning Quiz

_Is this (diagram provided) a good way to think about levels of metacognition_?

No, because each level of metacognition is conceptually identical, so they are better represented as self-referential.

### Final Quiz

_What did you learn in this lesson_?

- Metacognition allows for goal-based autonomy and provides robustness and flexibility to agents for fixing errors and filling gaps in knowledge, reasoning, or learning, and integrating strategies to achieve new goals
- Meta-reasoning is not simply about learning new information but learning _how to learn_
- Meta-reasoning is about learning new reasoning strategies and integrating new information into memory structures
- Meta-reasoning is also about creativity in tha

# Lesson 25

In this lesson we will discuss a handful of very broad topics and advanced applications of KBAI. We will also touch on some of the connections between human cognition and KBAI.

## Visuospatial Reasoning Introduction

**Visuospatial reasoning** is concerned with reasoning about _what_ (visuo) and _where_ (spatial). Visuospatial knowledge is knowledge where causality is, at most, implicit. However, visuospatial knowledge enables inferences about causality.

## Two Views Of Reasoning

- Propositional representations - representations through frames
- Analogical representations - representations through structural correspondence with the external world

Humans appear to use analogical representations for mental imagery. It is not yet known how to implement mental imagery for KBAI.

## Symbol Grounding Problem

_Content_ refers to the content of knowledge while _encoding_ deals with the representation of knowledge. The table below highlights some differences:

|          | Visuospatial                          | Verbal                                 |
| -------- | ------------------------------------- | -------------------------------------- |
| Content  | Appearance: what and where            | Arbitrary: driven by inferential needs |
| Encoding | Analogical: structural correspondence | Propositional: no correspondence       |

## Systems Thinking Introduction

The world consists of many different kinds of systems. A system is composed of a heterogenous interacting components. The interaction between components lead to processes of different kinds and these processes can occur at many different levels of abstraction. Consequently, **systems thinking** is reasoning about systems with numerous components and processes at multiple, potentially invisible, levels of abstraction.

Systems thinking allows us to understand the invisible levels of abstraction e.g., bees populations are declining and pesticide use is increasing so the understanding is that the pesticide is toxic to the bees.

## Structure, Behavior, And Function

In AI, we can capture the visible levels of abstraction (structure) and invisible levels of abstraction (e.g., behavior and function) through structure, behavior, and function models. This allows capturing of visible structures and invisible causual processes.

## Design Introduction

**Design thinking** is reasoning able ill-defined, unconstrained, and open-ended problems that are situated in the world. In design thinking, the solution and problem co-evolve over time.

## Creativity Introduction

Some is _creative_ if it is:

1. Novel
2. Valuable
3. Unexpected

Some other processes of creativity may include:

- Emergence
- Re-representation
- Serendipity

## AI Ethics

AI ethics pertain to our economy and society where there are hard issues and ethical implications. Much of the modern development of AI is driven by defence applications across the world. If robots are to become like humans, then what could be said about the civil rights of KBAI robots?

## Section Quizzes

### Defining Creativity Quiz III

_For each of the following tasks (provided), mark the box if successful completion of a task would mean that the agent is creative_.

All of the above.

### Defining Creativity Quiz IV

_Do you agree with David’s assessment that none of these results are creative because we can trace through the underlying process that led to them_?

No, because under this definition, humans are only considered creative because we don't know how the brain works yet.

### Final Quiz

_What did you learn in this lesson_?

- Researchers still are unsure how to implement mental imagery for KBAI agents even though it is agreed that humans appear to use analogical representations for mental imagery
- Structure, behavior, and function models allow capturing of visible structures and invisible causual processes
- Creativity is a difficult concept to define but it has to do with novelty, value, and unexpectedness of a solution
- As AI advances, researchers and engineers should discuss ethical implications of AI solutions and ensure that all stakeholders understand risks to society

# Lesson 26

In this lesson we will reflect on some of the main themes covered in this course and other upcoming themes and topics in the AI community. We will cover:

1. Major topics revisited
2. Principles of KBAI revisited
3. Modern KBAI research
4. Final thoughts

## Cognitive Systems Revisited

Recall our model of the cognitive system which can be broken down into three main spaces:

1. **Metacognition**: monitors the deliberative reasoning and acts on the deliberative reasoning. Can also monitor and act on itself as well
2. **Deliberation**: maps percepts into actions where mappings are mediated by reasoning, learning, and memory (_see, act, and think_ cycle)
3. **Reaction**: directly maps percepts from the environment into actions on the environment (_see and act_ cycle)

Each space may overlap with each other and are not disjoint in practice. _Metacognition_ acts primarily within the cognitive space while _deliberation_ and _reaction_ acts in the world. Additionally, the cognitive system is always situated in the world (cannot be separate from the world).

Also recall that intelligence is a function that maps perceptual histories into actions to the world. Depending on the input to the cognitive system, the output may vary:

- If input is a _goal_ -> output may be a _plan_ or _action_
- If input is _knowledge_ -> output may be learned and stored in _memory_
- If input is a _percept_ -> output may be an _action_ based on the percept

The _world_ is not just a physical world but a social world as well. Cognitive systems do not just monitor and observe the world but also inputs and outputs from other cognitive systems.

## Principles Of KBAI

We have covered several principles of KBAI in this course:

1. **Represent, organize, and reason**: KBAI agents represent and organize knowledge into knowledge structures to guide and support reasoning
2. Learning in KBAI agents is often incremental (KBAI agents do not learn a ton of information at once)
3. Reasoning in KBAI is top-down as well as bottom-up
4. KBAI agents match _methods_ to _tasks_ (as well as sub-methods to sub-tasks):
   - **Methods**: generate and test, means-ends analysis, problem reduction production systems, case-based reasoning, planning, analogical reasoning -> - **Tasks**: configuration, diagnosis, design, meta-reasoning, creativity, classification, systems thinking
5. KBAI agents use heuristics to find solutions that are good enough, though not necessarily optimal (due to computational tradeoffs)
6. KBAI agents make use of reoccurring patterns in the problems they solve
7. The architecture of KBAI agents enables reasoning, learning, and memory to support and constrain each other

## Current Research

Below are a list of current research leveraging principles from KBAI:

- _External_ to OMSCS:
  - **CALO**: cognitive assistant that learns and organizes (the precursor to Apple's SIRI)
  - **Cyc and OMCS**: knowledge bases of everyday common sense knowledge
  - **Wolfram Alpha**: a computational knowledge and answer engine
- _Internal_ to OMSCS:
  - **VITA**: a computational model of visual thinking in autism based on RPM
  - **Dramatis**: a computational model of suspense and drama in stories
  - **DANE**: support for design based on analogies to natural systems
