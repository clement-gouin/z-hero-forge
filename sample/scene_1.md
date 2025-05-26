# Scene 1

Scene content (always shown under the title)

![](https://unsplash.com/photos/Gbs3a-8C8Pc/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8cXVlc3R8ZW58MHx8fHwxNzQ3OTIxMTgxfDI&force=true&w=640)


<!-- subscene key, first one is the default -->
## subscene_1

Subscene 1 content (added to scene content)

<!-- changes utilities, can be put everywhere -->
/set force = 10
<!-- changes can be javascript, null on error -->
/set gold = Math.max(0, gold - 10)

<!-- actions, one action per list item, link in sub list item -->

<!-- standard option always shown-->
* <i icon=footprints></i> Continue walking
  * [[#subscene_2]]
<!-- conditional option, shown and disabled on fail-->
* [force > 10] <i icon=mountain></i> Climb on the side
  * [[#subscene_2]]
<!-- hidden conditional option, not shown on fail-->
* {force > 100} <i icon=mountain></i> Move the mountain
  * [[#subscene_2]]
<!-- conditional option can be random percentage-->
* {10%} <i icon=circle-pound-sterling></i> Some coins are on the floor
  * [[#subscene_2]]
<!-- you can use flags for "quests"-->
* {QUEST_1 == 1} <i icon=user></i> You see a person you know
  * [[#subscene_2]]
<!-- hidden conditional option, not shown on fail-->
* {force > 100} <i icon=mountain></i> Move the mountain
  * [[#subscene_2]]
<!-- options can be chained-->
* {QUEST_2 == 2}{10%}[force > 5] You cannot get this option without cheating
  * [[#subscene_2]]
<!-- option without link will be disabled by default-->
* Why is this not clickable

<!-- subscene key -->
## subscene_2

Subscene 2 content (added to scene content)

<!-- utility to set a flag to 1, equals to: /set QUEST_1 = 1 -->
/start QUEST_1
<!-- utility to set a flag to 2, equals to: /set QUEST_2 = 2-->
/end QUEST_2

<!-- you can link to these subscene with #-->
* Link 1
  * [[#]]
<!-- you can link to another subscene with #key-->
* Link 2
  * [[#subscene_1]]
<!-- you can link to another scene with its name--->
* Link 3
  * [[scene_2]]
<!-- you can link to another scene and subscene with its name and #key-->
* Link 4
  * [[scene_2#subscene_2]]
<!-- if a scene or subscene is not found, the link will be disabled and an error will be shown -->
* Link 5
  * [[scene_2#subscene_3]]