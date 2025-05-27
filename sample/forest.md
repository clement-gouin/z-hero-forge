<!-- see files in this order: start/forest/river -->
# Forest

![](https://images.unsplash.com/photo-1448375240586-882707db888b?w=640)

<!-- /show command set tracked values (see z-hero-quest "variables" format) in this scene/subscene (here all subscenes as it is before first subscene key) -->
/show steps,footprints,110
<!-- /global command set tracked values accross ALL SCENES -->

## default

You're walking into the forest...

<!-- /set command update variable (see z-hero-quest "changes" format) -->
/set steps=Math.max(steps-10,0)
<!-- you can make sure variables are defined like this -->
/set WATER=WATER??0

<!-- conditions can be set with {} and javascript syntax -->
* {steps>15}{20%} <i icon=rabbit></i> A rabbit is passing by, chase it (-15 <i icon=footprints></i>)
  * [[#rabbit-start]]
<!-- percent conditions will be set globally (ex: 5% and 10% in two lines will never be together) -->
* {5%} <i icon=clover></i> Look at this 4-leaf clover !
  * [[#4_leaf]] <!-- default to current scene to search subscene -->
* {steps>10}{10%} <i icon=ear></i> You ear water running nearby (-10 <i icon=footprints></i>)
  * [[river]]
<!-- shown conditions can be set with [] and javascript syntax, when not fulfilled they will be disabled -->
* <i icon=milk></i> [WATER] drink some water (+20 <i icon=footprints></i>)
  * [[#water]]
* {steps>=10} Continue into the forest (-10 <i icon=footprints></i>)
  * [[]] <!-- redirects to this subscene -->
* {steps<10} (end demo)
  * [[start#end]]

## 4_leaf

You found a 4-leaf clover !

It greatly boosts your resolve and you gain +30 <i icon=footprints></i> !

/set steps=steps+30

* {steps>=10} Continue into the forest (-10 <i icon=footprints></i>)
  * [[#]] <!-- '#' redirect to first subscene of scene -->
* {steps<10} (end demo)
  * [[start#end]]

## rabbit-start

<!-- commands can be set anywhere -->
/set steps=Math.max(steps-15,0)

It ran away...

Maybe it's hiding in this bush?

* {50%} <i icon=hand></i> Search the bush
  * [[#rabbit-success]]
* {50%} <i icon=hand></i> Search the bush
  * [[#rabbit-fail]]
* {steps>=10} Continue into the forest (-10 <i icon=footprints></i>)
  * [[#]]
* {steps<10} (end demo)
  * [[start#end]]

## rabbit-success

You catched the rabbit !

It boosts your resolve and you gain +20 <i icon=footprints></i>.

/set steps=steps+20

* {steps>=10} Continue into the forest (-10 <i icon=footprints></i>)
  * [[#]]
* {steps<10} (end demo)
  * [[start#end]]

## rabbit-fail

It wasn't in this bush...

* {steps>=10} Continue into the forest (-10 <i icon=footprints></i>)
  * [[#]]
* {steps<10} (end demo)
  * [[start#end]]

## water

You drink some refreshing water...

It feel refreshed and you gain +20 <i icon=footprints></i>.

/set WATER=0
/set steps=steps+20

* {steps>=10} Continue into the forest (-10 <i icon=footprints></i>)
  * [[#]]
* {steps<10} (end demo)
  * [[start#end]]
