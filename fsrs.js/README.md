JS version of FSRS (free spaced repetition scheduler) algorithm, based on the DSR model proposed by Piotr Wozniak, author of SuperMemo.

# Usage

`npm install fsrs.js` to import this module.

Example: 

```js
const fsrs = require('fsrs.js');

//input data 
var cardData={id:'idname'},
    grade=-1, //Grade `-1` means learn new card,and `0, 1, 2` means review old card.
    globalData={};

fsrs(cardData,grade,globalData) //Return {cardData,globalData}. You can save this output data and use it as input data the next time you update grade.
``` 