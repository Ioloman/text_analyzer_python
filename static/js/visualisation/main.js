const convertToChartjsData =
    (graphData) =>
        _.map(graphData, point => ({x: graphData.indexOf(point) + 1, y: point[1], word: point[0]}))

const createChartOptions = (data, nameID) => ({
    type: 'line',
    data: {
        labels: _.map([...Array(data.length).keys()], number => number + 1),
        datasets: [{
            label: 'График материала: ' + JSON.parse(document.getElementById(nameID).textContent),
            data: data,
            borderWidth: 1,
            borderColor: 'rgb(0,0,0)',
            backgroundColor: 'rgb(255,255,255,0)',
            cubicInterpolationMode: 'monotone',
        }]
    },
    options: {
        responsive: true,
        legend: {
            display: true,
            labels: {
                boxWidth: 0,
                fontColor: '#000',
                fontSize: 20
            },
            onClick: null
        },
        tooltips: {
            callbacks: {
                label: (tooltipItem, data) => {
                    return data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].word
                        + ', TF-IDF: ' + tooltipItem.value;
                }
            },
            displayColors: false
        }
    }
})

const GATHER_DISTANCE = 15
const listenerPointerDown = (chart, canvas, selectionRect, selectionContext, mutable) =>
    evt => {
        const points = chart.getElementsAtEventForMode(evt, 'index', {
            intersect: false
        });
        mutable.startIndex = points[0]._index;
        const rect = canvas.getBoundingClientRect();
        selectionRect.startX = evt.clientX - rect.left;
        selectionRect.startY = chart.chartArea.top;
        selectionRect.startPointX = points[0]._model.x
        mutable.drag = true;
    }

const listenerPointerMove = (chart, canvas, selectionRect, selectionContext, mutable) =>
    evt => {

        const rect = canvas.getBoundingClientRect();
        if (mutable.drag) {
            const rect = canvas.getBoundingClientRect();
            selectionRect.w = (evt.clientX - rect.left) - selectionRect.startX;
            selectionContext.globalAlpha = 0.5;
            selectionContext.clearRect(0, 0, canvas.width, canvas.height);
            selectionContext.fillRect(selectionRect.startX,
                selectionRect.startY,
                selectionRect.w,
                chart.chartArea.bottom - chart.chartArea.top);
        } else {
            selectionContext.clearRect(0, 0, canvas.width, canvas.height);
            var x = evt.clientX - rect.left;
            if (x > chart.chartArea.left) {
                selectionContext.fillRect(x,
                    chart.chartArea.top,
                    1,
                    chart.chartArea.bottom - chart.chartArea.top);
            }
        }
    }

const listenerPointerUp = (chart, canvas, selectionRect, selectionContext, mutable) =>
    evt => {

        const points = chart.getElementsAtEventForMode(evt, 'index', {
            intersect: false
        });
        mutable.drag = false;
        let endIndex = points[0]._index
        const rect = canvas.getBoundingClientRect();
        if ((evt.clientX - rect.left) >= selectionRect.startX) {
            mutable.startIndex += (selectionRect.startX - selectionRect.startPointX > GATHER_DISTANCE) ? 1 : 0;
            endIndex -= ((points[0]._model.x - (evt.clientX - rect.left) > GATHER_DISTANCE) ? 1 : 0);
        }
        else{
            mutable.startIndex -= (selectionRect.startPointX - selectionRect.startX > GATHER_DISTANCE) ? 1 : 0;
            endIndex += (((evt.clientX - rect.left) - points[0]._model.x > GATHER_DISTANCE) ? 1 : 0);
            [mutable.startIndex, endIndex] = [endIndex, mutable.startIndex];
        }
        if (endIndex >= mutable.startIndex) hideRangeOfItems(mutable.attachedListID, mutable.startIndex, endIndex);
    }

const hideRangeOfItems = (listID, startIndex, endIndex) => {
    const listOfItems = Array.prototype.slice.call(document.getElementById(listID).children);
    _.map(listOfItems,
        item => {
            if (listOfItems.indexOf(item) < startIndex || listOfItems.indexOf(item) > endIndex)
                item.style.display = 'none'
        }
    )
    _.map(listOfItems,
        item => {
            if (listOfItems.indexOf(item) >= startIndex && listOfItems.indexOf(item) <= endIndex)
                item.style.display = ''
        }
    )
}

const changeHeight = (el, height) => {
    el.height = height
    return el
}
const getCanvas = canvasID => document.getElementById(canvasID)

const getChart = (canvas, data, nameID) =>
    new Chart(canvas.getContext('2d'), createChartOptions(convertToChartjsData(data), nameID))

const changeSize = (to, from) => {
    to.width = from.width
    to.height = from.height
    return to
}

const getSelectionContext = (canvasID, chartCanvas) => changeSize(getCanvas(canvasID), chartCanvas).getContext('2d')


const data = JSON.parse(JSON.parse(document.getElementById("json-data").textContent))
const [firstGraphData, secondGraphData] = data;
const HEIGHT = 200;
let firstCanvas = changeHeight(getCanvas('firstChart'), HEIGHT);
let secondCanvas = changeHeight(getCanvas('secondChart'), HEIGHT);

let firstChart = getChart(firstCanvas, firstGraphData, 'name1');
let secondChart = getChart(secondCanvas, secondGraphData, 'name2');
let firstSelectionContext = getSelectionContext('firstOverlay', firstCanvas);
let secondSelectionContext = getSelectionContext('secondOverlay', secondCanvas);
let [firstStartIndex, secondStartIndex] = [0, 0];
let [firstSelectionRect, secondSelectionRect] = [{w: 0, startX: 0, startY: 0}, {w: 0, startX: 0, startY: 0}];
let [firstDrag, secondDrag] = [false, false];
let [firstMutable, secondMutable] = [
    {drag: false, startIndex: 0, attachedListID: 'firstList'},
    {drag: false, startIndex: 0, attachedListID: 'secondList'}
]
firstCanvas.onpointerdown = listenerPointerDown(firstChart, firstCanvas, firstSelectionRect, firstSelectionContext, firstMutable)
firstCanvas.onpointermove = listenerPointerMove(firstChart, firstCanvas, firstSelectionRect, firstSelectionContext, firstMutable)
firstCanvas.onpointerup = listenerPointerUp(firstChart, firstCanvas, firstSelectionRect, firstSelectionContext, firstMutable)

secondCanvas.onpointerdown = listenerPointerDown(secondChart, secondCanvas, secondSelectionRect, secondSelectionContext, secondMutable)
secondCanvas.onpointermove = listenerPointerMove(secondChart, secondCanvas, secondSelectionRect, secondSelectionContext, secondMutable)
secondCanvas.onpointerup = listenerPointerUp(secondChart, secondCanvas, secondSelectionRect, secondSelectionContext, secondMutable)

document.getElementById('firstList').ondblclick = evt => {
    const listOfItems = Array.prototype.slice.call(document.getElementById('firstList').children);
    listOfItems.forEach(value => value.style.display = '')
}
document.getElementById('secondList').ondblclick = evt => {
    const listOfItems = Array.prototype.slice.call(document.getElementById('secondList').children);
    listOfItems.forEach(value => value.style.display = '')
}




