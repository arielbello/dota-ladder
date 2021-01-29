var ctx = document.getElementById('country_chart').getContext('2d');
var chart;
let navItems = document.getElementsByClassName("nav-item");
let navList = Array.from(navItems);
const NAV_ITEM_AMERICAS = "nav-item-americas";
const NAV_ITEM_EUROPE = "nav-item-europe";
const NAV_ITEM_SEASIA = "nav-item-seasia";
const NAV_ITEM_CHINA = "nav-item-china";
const NAV_ITEM_GLOBAL = "nav-item-global";

function main(){
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
    el.innerHTML = "Last updated: " + date.toLocaleTimeString() + ", " + date.toLocaleDateString();
}

function processLabels(labels) {
//            if (data.groups.country == "country_not_found") {
//                data.groups.country = "No country info";
    var out = [];
    var newLabel = "";
    labels.forEach(label=>{
        if (label == "country_not_found") {
            newLabel = "No country information";
        }
        else if (label.length >= 27) {
            newLabel = label.slice(0, 27).padEnd(30, ".");
        }
        else {
            newLabel = label;
        }

        out.push(newLabel);
    });
    return out;
}

//Configure and load the dataset into the table
function loadTable(data) {
    if (chart) {
//        chart.data.labels = [];
//        chart.data.datasets = [];
        chart.destroy();
    }

    let numCountries = Object.keys(data).length;
    let maxNum = Object.values(data)[0];
    if (numCountries > 2 && Object.values(data)[0]/Object.values(data)[1] > 2) {
        maxNum = Object.values(data)[1] * 2;
    }

    //Resizes the chart to fit the size of the dataset
    //otherwise it arbitrarily chooses it's size
    var chartHeight = numCountries * 30;
    chartHeight = chartHeight < 50 ? 50 : chartHeight;
    let chartDiv = document.getElementById("chart-container");
    chartDiv.style.height = String(chartHeight) + "px";

    let labels = processLabels(Object.keys(data));

    //Chart creation with A LOT of options
    chart = new Chart(ctx, {

    type: "horizontalBar",
    showTooltips:false,

    data: {
        labels: labels,
        datasets: [{
            label: 'players',
            backgroundColor: "rgba(180,200,132,0.2)",
            borderColor: "rgba(180,200,132,1)",
            borderWidth: 2,
            hoverBackgroundColor: "rgba(180,200,132,0.4)",
            hoverBorderColor: "rgba(180,200,132,1)",
            data: Object.values(data),
            maxBarThickness: 28,
            minBarLength: 20,
            barPercentage: 0.9,
            categoryPercentage: 0.9
        }],
    },

    options: {
        aspectRatio: chartDiv.clientWidth / chartHeight,
        maintainAspectRatio: true,
        hover: {
            animationDuration: 0,
        },
        legend: {
            display: true,
            position: "right",
            align: "start"
        },
        plugins: {
            datalabels: {
                color: "#CACACA",
//                align: "end",
//                anchor: "left",
                clamp: true,
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
                    // lineHeight: 2.5, doesn't work
                    fontSize: 14,
                    fontColor: "#CACACA"
                },

            }],
            xAxes:[{
                type : "linear",

                ticks: {
                    // suggestedMax: maxNum

                }
            }]
        }
    }
    });
}

//load a static text file asynchronously
function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

//load country stats into a dictionary
function onCountryDataLoad(text) {
    var lines = text.split("\n");
    var table = {};
    for (let i=1; i < lines.length; i++){
        let regex = /(?<country>[\w\W]+?),(?<num>\d+)/;
        let data = lines[i].match(regex);
        if (!data || data.length < 3){
            console.log("error reading country stats");
        }
        else {
            if (data.groups.country == "country_not_found") {
                data.groups.country = "No country info";
            }
            table[data.groups.country] = data.groups.num;
        }
    }
    loadTable(table);
}

//Not using asynchronous load for now
//readTextFile("/scrapping/generated/country_stats.csv", onCountryDataLoad);

main();