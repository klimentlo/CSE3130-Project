# CSE3130 - Multiday Project - BrickBreaker

## Description
This program is a modification of brickbreaker, where the objective is to destroy as many bricks as possible without the ball hitting the bottom of the screen! You will have a bar which you can move back and fourth to deflect the ball. Good Luck!

## Planning Components
The brick is made many specific components, with 9 seperate objects required to make one brick
![] (https://cdn.discordapp.com/attachments/798067623534264331/1178562902836387870/image.png?ex=6576993c&is=6564243c&hm=baa419ee1df44a7343450e7551792ef89ec6814fee9ead86a4508ae6427221bb&)


There must be 2 functions per object per brick, meaning that there must be a total of 18 functions/methods required to position and blit a single brick. 

![](https://cdn.discordapp.com/attachments/798067623534264331/1178562059261190224/image.png?ex=65769873&is=65642373&hm=c0d4f73831c7bc6dc543791a19ba64f229ff97f208d00b54f9c07a440c6aaaff&) 

## Special Features

- The introduction to lives. You will have 3 chances to break as many bricks as possible. If the main white ball hits the bottom, you lose one life. Once your lives hit 0, GAME OVER!
-
- Every 15 seconds, an extra blue bonus ball will appear. If the blue ball hits the bottom of the screen, you will lose no lives. However, if your white ball hits the bottom, all blue balls will dissapear. (blue balls will also dissapear upon round completion)


## How to Run Program
Open the program, and hit run :D

## Reflection
After this project, I still stand my ground of disliking UML and flowcharts. I think it's my lack of ability and skill to make a smart and concise one, but I find it unnececarily time consuming and repetitive, but it's not too bad. One of the things I had to overcome was making the brick corners/how to bounce it. I've revisioned a handful of times of why it bounces weirdly, but I think its because of the way I programmed how it would bounce. The issue being it hitting multiple bricks at the same time, resulting in zero x/y change. Overal experince 7/10.
Very fun to make and problem solve, but extremely soul draining (esecially the planning tables :()