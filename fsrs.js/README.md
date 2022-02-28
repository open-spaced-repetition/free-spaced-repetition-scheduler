JavaScript module of Free Spaced Repetition Scheduler algorithm, based on the [DSR model](https://supermemo.guru/wiki/Two_components_of_memory) proposed by [Piotr Wozniak](https://supermemo.guru/wiki/Piotr_Wozniak), author of SuperMemo.

# Usage

`npm install fsrs.js` to import this module.

## Example

```js
const fsrs = require("fsrs.js")

//input data
var cardData={id:'id'},
    grade=-1,//Grade `-1` means learn new card,and `0, 1, 2` means review old card.
    globalData=null;

var outputData = fsrs(cardData,grade,globalData)//Return {cardData,globalData}. You can save this output data and use it as input data the next time you update grade.

console.log(outputData)
``` 