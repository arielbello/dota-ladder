var ctx = document.getElementById('country_chart').getContext('2d');
var chart;
let navItems = document.getElementsByClassName("nav-item");
let navList = Array.from(navItems);
const BAR_THICKNESS = 35;
const NO_COUNTRY_INFO_TEXT = "No country information";
const ON_MOBILE = navigator.userAgent.search("Mobi") !== -1
const NAV_ITEM_AMERICAS = "nav-item-americas";
const NAV_ITEM_EUROPE = "nav-item-europe";
const NAV_ITEM_SEASIA = "nav-item-seasia";
const NAV_ITEM_CHINA = "nav-item-china";
const NAV_ITEM_GLOBAL = "nav-item-global";


function main(){
    registerTooltipCustomPositioning();
    let navItemAmericas = document.getElementById(NAV_ITEM_AMERICAS);
    let navItemEurope = document.getElementById(NAV_ITEM_EUROPE);
    let navItemSeasia = document.getElementById(NAV_ITEM_SEASIA);
    let navItemChina = document.getElementById(NAV_ITEM_CHINA);
    let navItemGlobal = document.getElementById(NAV_ITEM_GLOBAL);
    navItemAmericas.onclick = onNavItemClick;
    navItemEurope.onclick = onNavItemClick;
    navItemSeasia.onclick = onNavItemClick;
    navItemChina.onclick = onNavItemClick;
    navItemGlobal.onclick = onNavItemClick;

    //dataset_americas and timestamp is imported from dataset_americas.js
    setNavItemSelected(navItemAmericas);
    updateDataset(dataset_americas, dataset_americas_timestamp);
}

function registerTooltipCustomPositioning() {
    Chart.Tooltip.positioners.custom = function(elements, eventPosition) {
    return { x: eventPosition.x, y: eventPosition.y };
};
}

function setNavItemSelected(target) {
    navList.forEach( item => {
        item.className = "nav-item";
    });
    target.className += " selected";
}

function onNavItemClick(event) {
    setNavItemSelected(event.target);
    switch (event.target.id) {
        case NAV_ITEM_AMERICAS:
            updateDataset(dataset_americas, dataset_americas_timestamp);
            break;
        case NAV_ITEM_EUROPE:
            updateDataset(dataset_europe, dataset_europe_timestamp);
            break;
        case NAV_ITEM_SEASIA:
            updateDataset(dataset_seasia, dataset_seasia_timestamp);
            break;
        case NAV_ITEM_CHINA:
            updateDataset(dataset_china, dataset_china_timestamp);
            break;
        case NAV_ITEM_GLOBAL:
            updateDataset(dataset_global, dataset_global_timestamp);
            break;
        default:
            console.log("unrecognized selection");
    }
}

function onNavEuropeClicked(event) {
    event.target.className += " selected";
    updateDataset(dataset_europe, dataset_europe_timestamp);
}

function onNavSeasiaClicked(event) {
    event.target.className += " selected";
    updateDataset(dataset_seasia, dataset_seasia_timestamp);
}

function onNavChinaClicked(event) {
    event.target.className += " selected";
    updateDataset(dataset_china, dataset_china_timestamp);
}

function onNavGlobalClicked(event) {
    event.target.className += " selected";
    updateDataset(dataset_global, dataset_global_timestamp);
}

function updateDataset(dataset, timestamp) {
    loadTable(dataset);
    loadTimestamp(timestamp);
}

function loadTimestamp(timestamp){
    let el = document.getElementById("timestamp");
    el.hidden = false;
    //Date in Javascript is in miliseconds since 1970, while python use seconds
    let date = new Date(timestamp * 1000);
    el.innerHTML = "Last updated " + date.toLocaleTimeString() + ", " + date.toLocaleDateString();
}

function buildChartData(dataDict) {
    var labels = [];
    var percentages = [];
    var total = Object.values( (acc, val) => acc + val);
    var newLabel = "";
    for (var key in dataDict) {
        total += dataDict[key];
        if (key == "country_not_found") {
            total -= dataDict[key];
            newLabel = NO_COUNTRY_INFO_TEXT;
        }
        else if (key.length >= 27) {
            newLabel = key.slice(0, 27).padEnd(30, ".");
        }
        else {
            newLabel = key;
        }
        labels.push(newLabel);
    }
    for (var key in dataDict) {
        let percentage = ((dataDict[key] / total) * 100).toFixed(2) + "%"
        percentages.push(percentage);
    }

    return { "labels": labels, "percentages": percentages, "values": Object.values(dataDict) };
}

//Configure and load the dataset into the table
function loadTable(data) {
    //Destroy the previous chart to update
    if (chart) {
        chart.destroy();
    }

    let numCountries = Object.keys(data).length;
    //Resizes the chart to fit the size of the dataset
    //otherwise it arbitrarily chooses it's size
    var chartHeight = numCountries * BAR_THICKNESS;
    chartHeight = chartHeight < 50 ? 50 : chartHeight;
    let chartDiv = document.getElementById("chart-container");
    chartDiv.style.height = String(chartHeight) + "px";
    let chartData = buildChartData(data);
//    let labels = processLabels(Object.keys(data));

    window.chartData = chartData;
    //Chart creation with A LOT of options
    chart = new Chart(ctx, {

    type: "horizontalBar",

    data: {
        labels: chartData["labels"],
        datasets: [{
            label: 'Players',
            backgroundColor: "rgba(180,200,132,0.2)",
            borderColor: "rgba(180,200,132,1)",
            borderWidth: 2,
            hoverBackgroundColor: "rgba(180,200,132,0.4)",
            hoverBorderColor: "rgba(180,200,132,1)",
//            data: Object.values(data),
            data: chartData["values"],
            maxBarThickness: BAR_THICKNESS,
            minBarLength: 20,
            barPercentage: 0.9,
            categoryPercentage: 0.9
        }],
    },

    options: {
        aspectRatio: chartDiv.clientWidth / chartHeight,
        maintainAspectRatio: true,

        tooltips: {
            enabled: true,
            position: "custom",
            titleFontSize: 14,
            titleFontStyle: "normal",
            bodyFontSize: 16,
            bodyFontStyle: "bold",
            backgroundColor: "rgb(65,45,60)",
            callbacks: {
                label: function(tooltipItem, data) {
                    if (chartData["labels"][tooltipItem.index] == NO_COUNTRY_INFO_TEXT) {
                        return "Percentage ignores this value";
                    }
                    return chartData["percentages"][tooltipItem.index];
                }
            }
        },

        animation: {
            duration: ON_MOBILE ? 0 : 1000,
        },

        hover: {
            animationDuration: 0,
        },
        legend: {
//            display: true,
            position: "right",
            align: "start",
            labels: {
                fontSize: 14,
                fontColor: "#CACACA",
            },
        },
        plugins: {
            datalabels: {
                color: "#DADADA",
                anchor: "end",
                align: "end",
                visibility: true,
                font: {
                    weight: "normal",
                    size: 15,
                },
            }
        },
        title: {
            display: false,
            position: "top",
            text: "Number of players by country",
            fontSize: 18,
            fontColor: "#CACACA"
        },
        scales: {
            yAxes:[{
                ticks: {
//                    mirror: true, //To display labels inside the bars
                    // lineHeight: 2.5, doesn't work
                    fontSize: 16,
                    fontColor: "#DADADA"
                },

            }],
            xAxes:[{
                type : "linear",
                ticks: {
//                     suggestedMax: maxNum,
                }
            }]
        }
    }
    });
}
main();