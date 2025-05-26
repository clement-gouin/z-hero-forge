<!-- see files in this order: start/forest/river -->
# River

![](https://unsplash.com/photos/Kl8S7XbWbzM/download?ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzQ4Mjc0MzAyfA&force=true&w=640)

/show steps,footprints,110

* <i icon=trees></i> Go back into the forest (-10 <i icon=footprints></i>)
  * [[forest]]
* {steps<10} (end demo)
  * [[start#end]]

## default

/set steps=Math.max(steps-10,0)

* {!WATER} <i icon=milk></i> Fill you bottle
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