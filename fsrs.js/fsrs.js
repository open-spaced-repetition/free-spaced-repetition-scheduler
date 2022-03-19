(function () {
    module.exports = function (cardData, grade, globalData) {
        var cardData = cardData || { id: "default" },
            grade = 'grade' in cardData ? grade : -1,//Ratings for review have 0, 1, 2. Other ratings mean learn new card.
            globalData = globalData || {
                difficultyDecay: -0.7,
                stabilityDecay: -0.2,
                increaseFactor: 60,
                requestRetention: 0.9,
                totalCase: 0,
                totalDiff: 0,
                totalReview: 0,
                defaultDifficulty: 5,
                defaultStability: 2,
                stabilityDataArry: []

            };



        if (grade == -1) {// learn new card
            var addDay = Math.round(globalData.defaultStability * Math.log(globalData.requestRetention) / Math.log(0.9));

            cardData.due = new Date(addDay * 86400000 + new Date().getTime()).toISOString();
            cardData.interval = 0;
            cardData.difficulty = globalData.defaultDifficulty;
            cardData.stability = globalData.defaultStability;
            cardData.retrievability = 1;
            cardData.grade = -1;
            cardData.review = new Date().toISOString();
            cardData.reps = 1;
            cardData.lapses = 0;
            cardData.history = [];
        } else {// review card after learn
            var lastDifficulty = cardData.difficulty,
                lastStability = cardData.stability,
                lastLapses = cardData.lapses,
                lastReps = cardData.reps,
                lastReview = cardData.review;

            cardData.history.push({
                due: cardData.due,
                interval: cardData.interval,
                difficulty: cardData.difficulty,
                stability: cardData.stability,
                retrievability: cardData.retrievability,
                grade: cardData.grade,
                lapses: cardData.lapses,
                reps: cardData.reps,
                review: cardData.review
            });

            var diffDay = (new Date() - new Date(lastReview)) / 86400000;

            cardData.interval = diffDay > 0 ? Math.ceil(diffDay) : 0;
            cardData.review = new Date().toISOString();
            cardData.retrievability = Math.exp(Math.log(0.9) * cardData.interval / lastStability);
            cardData.difficulty = Math.min(Math.max(lastDifficulty + cardData.retrievability - grade + 0.2, 1), 10);

            if (grade == 0) {
                cardData.stability = globalData.defaultStability * Math.exp(-0.3 * (lastLapses + 1));

                if (lastReps > 1) {
                    globalData.totalDiff = globalData.totalDiff - cardData.retrievability;
                }

                cardData.lapses = lastLapses + 1;
                cardData.reps = 1;

            } else {//grade == 1 || grade == 2
                cardData.stability = lastStability * (1 + globalData.increaseFactor * Math.pow(cardData.difficulty, globalData.difficultyDecay) * Math.pow(lastStability, globalData.stabilityDecay) * (Math.exp(1 - cardData.retrievability) - 1));

                if (lastReps > 1) {
                    globalData.totalDiff = globalData.totalDiff + 1 - cardData.retrievability;
                }

                cardData.lapses = lastLapses;
                cardData.reps = lastReps + 1;
            }

            globalData.totalCase = globalData.totalCase + 1;
            globalData.totalReview = globalData.totalReview + 1;

            var addDay = Math.round(cardData.stability * Math.log(globalData.requestRetention) / Math.log(0.9));

            cardData.due = new Date(addDay * 86400000 + new Date().getTime()).toISOString();

            // Adaptive globalData.defaultDifficulty
            if (globalData.totalCase > 100) {
                globalData.defaultDifficulty = 1 / Math.pow(globalData.totalReview, 0.3) * Math.pow(Math.log(globalData.requestRetention) / Math.max(Math.log(globalData.requestRetention + globalData.totalDiff / globalData.totalCase), 0), 1 / globalData.difficultyDecay) * 5 + (1 - 1 / Math.pow(globalData.totalReview, 0.3)) * globalData.defaultDifficulty;

                globalData.totalDiff = 0
                globalData.totalCase = 0
            }

            // Adaptive globalData.defaultStability
            if (lastReps === 1 && lastLapses === 0) {
                globalData.stabilityDataArry.push({
                    interval: cardData.interval,
                    retrievability: grade === 0 ? 0 : 1
                });

                if (globalData.stabilityDataArry.length > 0 && globalData.stabilityDataArry.length % 50 === 0) {
                    var intervalSetArry = [];

                    var sumRI2S = 0,
                        sumI2S = 0;

                    for (var s = 0; s < globalData.stabilityDataArry.length; s++) {
                        var ivl = globalData.stabilityDataArry[s].interval;

                        if (intervalSetArry.indexOf(ivl) === -1) {

                            intervalSetArry.push(ivl);

                            var filterArry = globalData.stabilityDataArry.filter(fi => fi.interval === ivl);

                            var retrievabilitySum = filterArry.reduce((sum, e) => sum + e.retrievability, 0);

                            if (retrievabilitySum > 0) {
                                sumRI2S = sumRI2S + ivl * Math.log(retrievabilitySum / filterArry.length) * filterArry.length;
                                sumI2S = sumI2S + ivl * ivl * filterArry.length;
                            }
                        }
                    }

                    globalData.defaultStability = (Math.max(Math.log(0.9) / (sumRI2S / sumI2S), 0.1) + globalData.defaultStability) / 2;
                }
            }
        }

        return { cardData, globalData };
    };
})();
