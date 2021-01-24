function main(){
    //dataset_americas is imported from dataset_americas.js
    setupTable(dataset_americas);
    //same for timestamp
    setupTimestamp(dataset_americas_timestamp);
}

function setupTimestamp(timestamp){
    let el = document.getElementsByClassName("dataset-timestamp")[0];
    el.hidden = false;
    //Date in Javascript is in miliseconds since 1970, while python use seconds
    let date = new Date(timestamp * 1000);
    el.innerHTML = "last updated: " + date.toLocaleTimeString() + ", " + date.toLocaleDateString();
    console.log(el.text);
}

//Configure and load the dataset into the table
function setupTable(data){
    var ctx = document.getElementById('country_chart').getContext('2d');
    let numCountries = Object.keys(data).length;
    let maxNum = Object.values(data)[0];
    if (numCountries > 2 && Object.values(data)[0]/Object.values(data)[1] > 2) {
        maxNum = Object.values(data)[1] * 2;
    }
    var chart = new Chart(ctx, {

    type: "horizontalBar",

    data: {
        labels: Object.keys(data),
        datasets: [{
            label: 'Players',
            backgroundColor: "rgba(180,200,132,0.2)",
            borderColor: "rgba(180,200,132,1)",
            borderWidth: 2,
            hoverBackgroundColor: "rgba(180,200,132,0.4)",
            hoverBorderColor: "rgba(180,200,132,1)",
            data: Object.values(data)
        }],
    },

    options: {
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        title: {
            display: true,
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
                barPercentage: 0.9,
                categoryPercentage: 0.9,
            }],
            xAxes:[{
                type : "linear",

                minBarLength: 20,
                ticks: {
                    // suggestedMax: maxNum
                }
            }]
        }
    }
    });
    //Resizes the chart to fit the size of the dataset
    //otherwise it arbitrarily chooses it's size
    chart.canvas.parentNode.style.height = String(numCountries * 30) + "px";
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
    setupTable(table);
}

//Not using asynchronous load for now
//readTextFile("/scrapping/generated/country_stats.csv", onCountryDataLoad);

main();