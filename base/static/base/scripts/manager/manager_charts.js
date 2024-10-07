
$(document).ready(function () {
      
    $(".chart-container-canvas").hide();
    

    $("#chart-options").change(function() {
      let selectedOptionId;
      selectedOptionId = $("#chart-options").val()

      if ( selectedOptionId == 'option-1' ) {
        $(".chart-container-canvas").hide();
        $("#chart-container-1").show();
      } else if ( selectedOptionId == 'option-2' ) {
        $(".chart-container-canvas").hide();
        $("#chart-container-2").show();
      } else if (selectedOptionId == 'option-3') {
        $(".chart-container-canvas").hide();
        $("#chart-container-3").show();
      } else if (selectedOptionId == 'option-4') {
        $(".chart-container-canvas").hide();
        $("#chart-container-4").show();
      } else if ($("#chart-options").val() == "") {
        $(".chart-container-canvas").hide();
      }
    });



    // const ctx = document.getElementById('chart-number-of-devices-inspected-per-user');

    let myDataset = [
      { name: 'Sarah', numberOfDevices: 12 },
      { name: 'James', numberOfDevices: 19 },
      { name: 'Robert', numberOfDevices: 3 },
      { name: 'Michael', numberOfDevices: 5 },
      { name: 'Adam', numberOfDevices: 2 },
      { name: 'David', numberOfDevices: 10 },
    ];

    totalNumberOfInspectedDevicesGlobal = 0
    for (let i=0; i<myDataset.length; i++) {
      totalNumberOfInspectedDevicesGlobal = totalNumberOfInspectedDevicesGlobal + myDataset[i].numberOfDevices
    }


    let chart_1 = new Chart($("#chart-1"), {
      type: 'pie',
      data: {
        labels: myDataset.map(row => row.name),
        datasets: [{
          label: 'Precentage and Number of Inspected Devices Per User',
          data: myDataset.map(row => row.numberOfDevices),
          borderWidth: 1
        }]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: 'Precentage and Number of Inspected Devices Per User',
            font: {
              size: 15
            }
          },
          tooltip: {
            enabled: true
          },
          datalabels: {
            font: {
              size: 15
            },
            textAlign: 'center',
            formatter: (value, context) => {
              let NumOfInspectedDevicesPerUser = context.dataset.data;
              function totalSum(total, NumOfInspectedDevicesPerUser) {
                return total + NumOfInspectedDevicesPerUser;
              }
              let totalNumOfInspectedDevicesForAllUsers = NumOfInspectedDevicesPerUser.reduce(totalSum, 0)
              let percentageOfNumberOfInspectedDevicesPerUser = (value / totalNumOfInspectedDevicesForAllUsers * 100).toFixed(1);
              display = [`#${value}`, `${percentageOfNumberOfInspectedDevicesPerUser}%`, `User: ${context.chart.config._config.data.labels[context.dataIndex]}`];
              return display;
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
      plugins: [ChartDataLabels]
    });

    usernameWithNumberOfRefurbishedAndScrappedDevices = [
      { name: 'Sarah', numberOfScrappedDevices: 6, numberOfRefurbishedDevices: 6},
      { name: 'James', numberOfScrappedDevices: 10, numberOfRefurbishedDevices: 9 },
      { name: 'Robert', numberOfScrappedDevices: 3, numberOfRefurbishedDevices: 0},
      { name: 'Michael', numberOfScrappedDevices: 0,  numberOfRefurbishedDevices:5 },
      { name: 'Adam', numberOfScrappedDevices: 1,  numberOfRefurbishedDevices:1},
      { name: 'David', numberOfScrappedDevices: 9, numberOfRefurbishedDevices: 1},
    ]

    let topLabels_chart_2 = {
      id: 'topLabels_chart_2',
      afterDatasetsDraw(chart, args, pluginOption) {
        console.log(chart);


      }
    };

    let chart_2 = new Chart($("#chart-2"), {
      type: 'bar',
      data: {
        labels: usernameWithNumberOfRefurbishedAndScrappedDevices.map(row => row.name),
        datasets: [{
          label: 'Number and Percentae of Scrapped DevicesPer User',
          data: usernameWithNumberOfRefurbishedAndScrappedDevices.map(row => row.numberOfScrappedDevices),
          borderWidth: 1,
        },
        {
          label: 'Number and Percentae of Refubished DevicesPer User',
          data: usernameWithNumberOfRefurbishedAndScrappedDevices.map(row => row.numberOfRefurbishedDevices),
          borderWidth: 1,
        }]
      },
      options: {
        scales: {
          x: {
            stacked: true
          },
          y: {
            stacked: true
          }
        },
        plugins: {
          datalabels: {
            font: {
              size: 10
            },
            textAlign: 'center',
            formatter: (value, context) => {
              let percentageOfDevices = (value / totalNumberOfInspectedDevicesGlobal * 100).toFixed(1);
              let display;
              if (value == '0') {
                return null;
              }
              display = [`#${value}`, `${percentageOfDevices}%`, `User: ${context.chart.config._config.data.labels[context.dataIndex]}`];
              return display;
            }
          }
        }
      },
      plugins: [ChartDataLabels, topLabels_chart_2]
    });



    let datasets_year_numOfInspectedDevicesPerMonth = [
      {year: 2017, numOfInspectedDevicesPerMonth: [120, 135, 88, 150, 200, 465, 840, 1650, 765, 5984, 451, 812]},
      {year: 2018, numOfInspectedDevicesPerMonth: [60, 70, 44, 75, 100, 225, 420, 825, 380, 300, 226, 406]},
      {year: 2019, numOfInspectedDevicesPerMonth: [465, 782, 33, 640, 808, 734, 701, 304, 130, 6370, 480, 804]},
      {year: 2020, numOfInspectedDevicesPerMonth: [641, 305, 99, 423, 1430, 767, 134, 1650, 765, 5984, 451, 812]},
      {year: 2021, numOfInspectedDevicesPerMonth: [120, 135, 77, 150, 200, 676, 705, 727, 172, 733, 757, 812]},
      {year: 2022, numOfInspectedDevicesPerMonth: [120, 135, 66, 150, 200, 545, 1673, 346, 765, 1344, 0, 0]},
    ];
    
    function createArrayWithRandomValuesFrom0To100() {
      return [Math.floor(Math.random()*101),Math.floor(Math.random()*101),Math.floor(Math.random()*101),Math.floor(Math.random()*101),,Math.floor(Math.random()*101),,Math.floor(Math.random()*101),,Math.floor(Math.random()*101),,Math.floor(Math.random()*101),,Math.floor(Math.random()*101),,Math.floor(Math.random()*101),,Math.floor(Math.random()*101),,Math.floor(Math.random()*101),];
    }


    let datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth = [
      {year: 2017, numOfScrappedDevices: [60, 70, 44, 75, 100, 225, 420, 825, 380, 300, 226, 406], numOfRefurbishedDevices: [120, 135, 77, 150, 200, 676, 705, 727, 172, 733, 757, 812]},
      {year: 2018, numOfScrappedDevices: [60, 70, 44, 75, 100, 225, 420, 825, 380, 300, 226, 406], numOfRefurbishedDevices: [120, 135, 77, 150, 200, 676, 705, 727, 172, 733, 757, 812]},
      {year: 2019, numOfScrappedDevices: [465, 782, 33, 640, 808, 734, 701, 304, 130, 6370, 480, 804], numOfRefurbishedDevices: [465, 782, 33, 640, 808, 734, 701, 304, 130, 6370, 480, 804]},
      {year: 2020, numOfScrappedDevices: [641, 305, 99, 423, 1430, 767, 134, 1650, 765, 5984, 451, 812], numOfRefurbishedDevices: [641, 305, 99, 423, 1430, 767, 134, 1650, 765, 5984, 451, 812]},
      {year: 2021, numOfScrappedDevices: [120, 135, 77, 150, 200, 676, 705, 727, 172, 733, 757, 812], numOfRefurbishedDevices: [120, 135, 66, 150, 200, 545, 1673, 346, 765, 1344, 0, 0]},
      {year: 2022, numOfScrappedDevices: [120, 135, 66, 150, 200, 545, 1673, 346, 765, 1344, 0, 0], numOfRefurbishedDevices: [120, 135, 88, 150, 200, 465, 840, 1650, 765, 5984, 451, 812]},
    ];



    let chart_3 = new Chart($("#chart-3"), {
      type: 'bar',
      data: {
        labels: ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'],
        datasets: [{
          label: 'Number and Percentae of Scrapped Devices in Months',
          data: datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[0].numOfScrappedDevices,
          borderWidth: 1,
        },
        {
          label: 'Number and Percentae of Refubished Devices in Months',
          data: datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[0].numOfRefurbishedDevices,
        }]
      },
      options: {
        scales: {
          x: {
            stacked: true
          },
          y: {
            stacked: true
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Precentage and Number of Inspected Devices, Scrapped and Refurbished, in year 2017',
            font: {
              size: 15
            }
          },
          datalabels: {
            font: {
              size: 15
            },
            textAlign: 'center',
            formatter: (value, context) => {
              if (value == '0') {
                return null;
              }
              return `#${value}`;
            }
          }
        }
      },
      plugins: [ChartDataLabels]
    });

    let datasets_year_scrapped_refurbished_sumPerMonth;
    datasets_year_scrapped_refurbished_sumPerMonth = [];
    function sumOfDevicesPerYearInArray(arrayDataset) {
      
      for (let i=0; i<datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth; i++) {
        let year_scrapped_refurbished = {year: datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[i].year};
        
        let array_year_scrappedDevices;
        array_year_scrappedDevices = datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[i].numOfScrappedDevices;
        
        let sumOfNumberOfScrappedDevices;
        for (let j=0; j<array_year_scrappedDevices.length; j++) {
          sumOfNumberOfScrappedDevices += array_year_scrappedDevices[j];
        }

        let array_year_refurbishedDevices;
        array_year_refurbishedDevices = datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[i].numOfRefurbishedDevices;

        let sumOfNumberOfRefurbishedDevices;
        for (let j=0; j<array_year_refurbishedDevices.length; j++) {
          sumOfNumberOfRefurbishedDevices += array_year_refurbishedDevices[j];
        }

        year_scrapped_refurbished.numOfScrappedDevices = sumOfNumberOfScrappedDevices;
        year_scrapped_refurbished.numOfRefurbishedDevices = sumOfNumberOfRefurbishedDevices;
        datasets_year_scrapped_refurbished_sumPerMonth.push(year_scrapped_refurbished);
      }

    }



    // let datasets_year_sumOfNumOfScrappedAndRefurbishedDevicesPerMonth = [
    //   {year: 2017, numOfScrappedDevices: , numOfRefurbishedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[0].numOfRefurbishedDevices)},
    //   {year: 2018, numOfScrappedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[1].numOfScrappedDevices), numOfRefurbishedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[1].numOfRefurbishedDevices)},
    //   {year: 2019, numOfScrappedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[2].numOfScrappedDevices), numOfRefurbishedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[2].numOfRefurbishedDevices)},
    //   {year: 2020, numOfScrappedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[3].numOfScrappedDevices), numOfRefurbishedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[3].numOfRefurbishedDevices)},
    //   {year: 2021, numOfScrappedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[4].numOfScrappedDevices), numOfRefurbishedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[4].numOfRefurbishedDevices)},
    //   {year: 2022, numOfScrappedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[5].numOfScrappedDevices), numOfRefurbishedDevices: sumOfDevicesInArray(datasets_year_numOfScrappedAndRefurbishedDevicesPerMonth[5].numOfRefurbishedDevices)},
    
    // ];


    let chart_4 = new Chart($("#chart-4"), {
      type: "bar",
      data: {
        labels: datasets_year_scrapped_refurbished_sumPerMonth.map(row => row.year),
        datasets: [{
          label: 'Number and Percentae of Scrapped Devices in Years',
          data: datasets_year_scrapped_refurbished_sumPerMonth.map(row => row.numOfScrappedDevices),
          borderWidth: 1,
        },
        {
          label: 'Number and Percentae of Refubished Devices in Years',
          data: datasets_year_scrapped_refurbished_sumPerMonth.map(row => row.numOfRefurbishedDevices),
        }]
      },
      options: {
        scales: {
          x: {
            stacked: true
          },
          y: {
            stacked: true
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Precentage and Number of Inspected Devices, Scrapped and Refurbished, in Years',
            font: {
              size: 15
            }
          },
          datalabels: {
            font: {
              size: 15
            },
            textAlign: 'center',
            formatter: (value, context) => {
              if (value == '0') {
                return null;
              }
              return `#${value}`;
            }
          }
        }
      },
      plugins: [ChartDataLabels]
    });

  });
