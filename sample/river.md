<!-- see files in this order: start/forest/river -->
# River

![](https://images.unsplash.com/photo-1547929798-737b93ec2515?q=80&w=640&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

/show steps,footprints,110

* <i icon=trees></i> Go back into the forest (-10 <i icon=footprints></i>)
  * [[forest]]
* {steps<10} (end demo)
  * [[start#end]]

## default

/set steps=Math.max(steps-10,0)

* {!WATER} <i icon=milk></i> Fill your bottle
  * [[#fill]]
* {WATER} <i icon=milk></i> Your bottle is already full
* <i icon=droplet></i> Drink some water
  * [[#drink]]

## fill

You fill your bottle with fresh water... <i icon=milk></i>

/set WATER=1

You also drink some and gains +10 <i icon=footprints></i>.

/set steps=steps+10

## drink

You drink water some and gains +10 <i icon=footprints></i>.

/set steps=steps+10