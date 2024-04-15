# Thesis: Reverse Engineering class diagrams using GPT-4
Class diagrams are an important tool for the understanding of software
projects. They provide an abstract overview of projects and can therefore be
used as an on-boarding tool for new developers. However, a substantial problem
arises due to the low frequency at which the diagrams are updated [1]. This can
cause a roadblock, since the efficacy of the diagram in helping with the
understanding of a particular project relies on the diagram being an accurate
representation of the codebase. A solution to this dilemma would be to lower
the time investment required to create and maintain the class diagram, such as
with the use of specific reverse engineering tools which can generate class
diagram from inputted code. The problem is that these tool are too literal as
they lack the ability to perform abstractions [2], causing the diagrams to look
cluttered. An improvement of these reversed engineered class diagrams was made
by Osman et al. [3] and Thung et al. [4] which both attempted to condense the
reversed engineered diagrams. Osman et al. [3] and Thung et al. [4] use
traditional machine learning techniques to abstract away classes in order to
improve readability, as not all classes are needed to understand a codebase.
Further improvements were made upon the work of Osman et al. and Thung et al.
by Yang et al. who reduced the needed for manual labeling when using machine
learning algorithms for condensing reverse engineered class diagrams [5].
Another way to tackle the problem of easily creating class diagrams is with the
use of Large Language Models (LLMs). There has been a significant increase in
the complexity and availability of LLMs over the last few years [6]. These LLMs
have an edge over traditional machine learning techniques that are restricted
to specific sizes, dimensions and modes of inputs and outputs, as explored by
Osman et al. [3] and Thung et al. [4]. The ability of modern LLMs to take
intake large amounts of multi-modal data and produce useful output makes them a
valuable tool for various industries, in particular software development and
documentation. In order for LLMs to provide utility within the realm of
software documentation, it is important to understand their handling of large
code bases as input and their ability to grasp the various complex
relationships among the code. This understanding in particular is of the utmost
importance, if these LLMs are to be tweaked for software documentation specific
use cases. Such is the purpose of this paper: to analyze, organize and fine
tune the output from a LLM to produce class diagrams in an attempt to aid the
streamlining of the software documentation process. For the purposes of this
research, we have decided to use GPT-4 as it is one of the best available LLMs
[7] [8]. GPT-4 is a multi-modal LLM that outperforms a variety of other LLMs on
the metrics of hallucination and common-sense reasoning, as found by Minaee et
al. [8], making it a good fit for this research. The research process is
divided into two phases. The first phase will put GPT-4’s code interpretation
abilities to the test, as the model is used to generate class diagrams using
code as input. The output from GPT-4 will be compared to human- generated
diagrams. Building upon the insights gathered in phase one, in phase two we
will once again generate class diagrams, but this time include the Human
Abstraction Frame- work in the prompt as well, in an attempt to imitate the
human abstractions detailed by Zhang et al. [9]. This research aims to explore
the following questions: RQ1) How effectively does GPT-4 abstract code
relationships when generating class diagram on its own, as compared to the
human-generated diagrams? RQ2) How effectively does GPT-4 abstract code
relationships when generating class diagrams, utilizing the human abstraction
framework as input along with code input? RQ3) How does the inclusion of the
human abstraction frame- work within the prompt affect the outputted diagrams,
as compared to when it is excluded? In order to address the research questions
and evaluate GPT- 4’s class diagram generating abilities, we first need to
conduct some pre-experiments. As there are several ways a file can be be
provided to GPT4, e.g the files can be attached with the prompt or their
content can be a component of the prompt. We must first determine the best
approach for file handling in order for GPT-4 to have optimal comprehension of
the codebase. Furthermore, as the prompt to a large extent determines the
output quality of the LLM [10], it is then critical to have a fine-tuned prompt
that allows GPT-4 to best generate class diagrams. The aforementioned
experiments will provide us pre-requisite knowledge, improving the overall
output from the actual experiments concerning RQ1 and RQ2. The research
questions will be answered via a controlled experiment, comparing the
performance of GPT-4 in creating class diagram with human abstractions with a
set of five class diagrams created by five development teams. The answers to
these questions will act as a stepping stone for future research to use these
rapidly improving LLMs in order to streamline the software documentation
process and aid in the on-boarding of new developers with the assurance that
the software models are accurate and up to date.
