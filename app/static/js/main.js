$("#crt-rqst-mdl").on("show.bs.modal", function (e) {
    $(".frcr-cnt").hide();
})

$("#crt-rqst-mdl").on("hidden.bs.modal", function () {
    $(".frcr-cnt").show();
})

document.querySelectorAll(".cs-pst").forEach((card) => {
    const chart = card.querySelector(".cs-pst-d");
    
    var data = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],

        series: [
            [2, 1, 4, 2, 0, 1, 1, 2, 5, 2, 1, 4]
        ]
    };
    
    new Chartist.Line(chart, data, {showArea: true});
});

document.querySelectorAll(".cs-sro").forEach((card) => {
    const chart = card.querySelector(".cs-sro-d");

    var data = {
        labels: ["City registrar's office", "City legal office", "Pala-o barangay hall", "City engineer's office", "Hall of Justice", "Del carmen barangay hall", "City mayor's office", "MSU IIT"],
        
        series: [
            [5, 4, 3, 7, 5, 2, 0, 2],
            [3, 2, 9, 5, 4, 4, 7, 5],
            [1, 9, 1, 5, 2, 1, 2, 0],
            [4, 6, 4, 4, 5, 0, 4, 0],
        ]
    }

    var options = {
        seriesBarDistance: 10,
        reverseData: true,
        horizontalBars: true,
        axisY: {
            offset: 75
        }
    }

    new Chartist.Bar(chart, data, options);
});

document.querySelectorAll(".cs-tsp").forEach((card) => {
    const chart = card.querySelector(".cs-tsp-d");

    var data = {
        labels: ["Gino Mascariñas", "Jonas Serino", "Chuckie Razuman", "Chad Mascariñas"],
        
        series: [
            [5, 4, 3, 7],
            [3, 2, 9, 5],
            [1, 9, 100, 5],
            [4, 6, 4, 4],
        ]
    }

    var options = {
        seriesBarDistance: 10,
        reverseData: true,
        horizontalBars: true,
        axisY: {
            offset: 75
        }
    }

    new Chartist.Bar(chart, data, options);
});

document.querySelectorAll(".cs-rs").forEach((card) => {
    const chart = card.querySelector(".cs-rs-d");
    
    var data = {
        labels: [" ", " ", " ", " ", " "],

        series: [20, 15, 10, 14, 1]
    };

    var options = {
        labelInterpolationFnc: function(value) {
            return value[0]
        }
    };

    var responsiveOptions = [
        ["screen and (min-width: 640px)", {
            labelInterpolationFnc: function(value) {
                return value;
            }
        }],
        ["screen and (min-width: 1024px)", {
            chartPadding: 10
        }]
    ];

    new Chartist.Pie(chart, data, options, responsiveOptions);
});