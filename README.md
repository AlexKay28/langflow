
<p align="center">
  <img src="https://user-images.githubusercontent.com/55444371/157264799-d738d44b-e686-4a5b-ab2d-dcd18c30341d.png" width="50%" height="50%">
</p>


*- "The project for the most brutal and effective language learning technique" (c) Alex Kay*

  The langflow project was created for language learning purposes on the basis of continuous practicing and deep recall. The idea behind this is the constant repetition and direct experience obtained by the student as well as it leveraged in RL paradigm with agent and learning environment. The natural way of learning by this technique reminds supervised/semi-supervised learning which became one the most effective ways in ML nowadays (one of the assumptions on a user side is used - students already studied grammar and know some vocabulary and can construct simple sentences).
  
  List of analogies transfered from RL to student:
  - environment :: learning phrases space
  - agent :: student
  - optimal policy :: successfull learning
  - exploration :: new phrases, expanding vocabulary
  - reward :: student's answer correctness rate

# How to

1. On The first page it will prompt the student to choose a pair of languages in a session. The first language should be already known by the student and the second one is the target language student going to learn. Also it's possible to choose the difficulty level at a start, but it might be configured easily later. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/55444371/157267496-14eaa355-c8c3-4691-8833-7df23d3c79e5.png" width="50%" height="50%">
</p>

Take into account the fact that it doesn't require to do registrations which can be convenient while the first try, but if you want to score your own progress and to have individual progress control by RL algo - you must be authorized while learning.

2. The learning process has shown in the picture below:

<p align="center">
  <img src="https://user-images.githubusercontent.com/55444371/157269220-0c0ff490-d976-455a-ae15-d3ad0691042f.png" width="50%" height="50%">
</p>

Each step has 3 lines in the step block, it's the student's direct experience he/she should to analyze and do inferences, take notes and memorize. The first line of the block is the question that was asked, the second one is the provided by the student answer, the third line is the correct answer given by the app. 
Comparing student and real answers from questions NLP model is used to calculate semantic score of closeness. 
The best value possible is equal to 1.0, the worst-case is equal to 0.0. (Don't worry if you cant get the best score, consider 0.95 as a perfect answer you can give)

Constant practicing, day by day, allows you to master your language skills, improve your active vocabulary and help you be closer to your dreams to speak freely.

# Online version
https://langflow1.herokuapp.com/
