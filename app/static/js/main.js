// GLOBALS
var currentDate = new Date();
var currentYear = currentDate.getFullYear();
const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var currentMonth = parseInt(currentDate.getMonth()) + 1;
var currentDay = parseInt(currentDate.getDate());

// DASHBOARD
document.querySelectorAll(".cs-pst").forEach((card) => {
    const yearDropdown = card.querySelector(".dropdown");
    const button = yearDropdown.querySelector(".btn");
    const yearDropdownMenu = yearDropdown.querySelector(".dropdown-menu");
    const chart = card.querySelector(".cs-pst-d");

    button.innerHTML = currentYear.toString();

    let inbetweenYearCount = parseInt(currentYear) - 2015;
        
    while (inbetweenYearCount >= 0) {
        let yearItem = document.createElement("a");
        yearItem.classList.add("dropdown-item");

        let yearDisplay = (2015 + inbetweenYearCount).toString();
        yearItem.innerHTML = yearDisplay;
        
        yearItem.addEventListener("click", () => {
            button.innerHTML = yearDisplay;

            populateYearlyRequestPerformance(yearDisplay);
        });

        yearDropdownMenu.append(yearItem)
        
        inbetweenYearCount--;
    }
    
    populateYearlyRequestPerformance(parseInt(currentYear));

    function populateYearlyRequestPerformance (year) {
        let data = {};

        data.labels = [];
        data.series = [];
        data.series[0] = [];

        let maxMonth = (year == currentYear) ? currentMonth : 12;

        var activeAjaxConnections = 0;
        for(var i=1; i<=maxMonth; i++){
            data.labels[i-1] = monthNames[i-1];

            countYearMonthlyRequests(year, i);
        }

        function countYearMonthlyRequests (year, monthInt, requestCount = 0, paginateNo = 1) {
            $.ajax({
                method: "GET",
    
                beforeSend: function() {
                    activeAjaxConnections++;
                },
    
                url:  "api/request/year/" + year + "/month/" + monthInt + "/result/0?pagination_no=" + paginateNo,
    
                success: function (response) {
                    activeAjaxConnections--;

                    data.series[0][monthInt-1] = (parseInt(data.series[0][monthInt-1]) ? parseInt(data.series[0][monthInt-1]) : 0) + parseInt(response["requests"].length);

                    countYearMonthlyRequests(year, monthInt, requestCount + response["requests"].length, paginateNo + 1);
                },
    
                error: function (xhr) {
                    activeAjaxConnections--;
                    
                    if (xhr.status === 404) {
                        if (!data.series[0][monthInt-1]) {
                            data.series[0][monthInt-1] = 0;
                        }

                        if (activeAjaxConnections === 0) {
                            let chartist = new Chartist.Line(chart, data, {showArea: true});
    
                            chartist.on('draw', function(data) {
                                if(data.type === 'line' || data.type === 'area') {
                                    data.element.animate({
                                    d: {
                                        begin: 2000 * data.index,
                                        dur: 2000,
                                        from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                                        to: data.path.clone().stringify(),
                                        easing: Chartist.Svg.Easing.easeOutQuint
                                    }
                                    });
                                }
                            });
                        }
                    }
                }
            });
        }
    }
});

document.querySelectorAll(".cs-sro").forEach((card) => {
    const display = card.querySelector(".cs-sro-d");
    var containerHeight = $(display).parent().outerHeight();
    display.style.height = containerHeight + 'px';

    const legendCont = document.querySelector(".cs-sro-l");

    const traverserCont = card.querySelector(".btn-group");
    const leftTraverser = traverserCont.firstElementChild;
    const rightTraverser = traverserCont.lastElementChild;

    var officePaginateNo = 1;

    var data = {};
    data.labels = [];
    data.series = [];

    var options = {
        high: 0,
        width: '725px',
        height: containerHeight + 'px',
        axisY: {
            offset: 75
        },
        plugins: [
            Chartist.plugins.legend({
                position: legendCont,
                clickable: false
            })
        ]
    }

    readyDisplay("TOTREQ_DESC", officePaginateNo);
    populateNatureSeriesAjax();

    leftTraverser.addEventListener("click", () => {
        officePaginateNo--;

        readyDisplay("TOTREQ_DESC", officePaginateNo);

        getOfficeListAjax("TOTREQ_DESC", officePaginateNo);
    });

    rightTraverser.addEventListener("click", () => {
        officePaginateNo++;

        readyDisplay("TOTREQ_DESC", officePaginateNo);

        getOfficeListAjax("TOTREQ_DESC", officePaginateNo);
    });

    function readyDisplay (orderCommand="TOTREQ_DESC", paginate=1) {
        if (paginate > 1) {
            leftTraverser.disabled = false;

        } else {
            leftTraverser.disabled = true;
        }

        $.ajax({
            method: "GET",

            url: "api/office/?order_command=" + orderCommand + "&pagination_no=" + (paginate + 1),

            success: function () {
                rightTraverser.disabled = false;
            },

            error: function () {
                rightTraverser.disabled = true;
            }
        });
    }

    function populateNatureSeriesAjax (paginate=1) {
        $.ajax({
            method: "GET",

            url: "api/nature/?pagination_no=" + paginate,

            success: function (response) {
                for (let nature of response["natures"]) {
                    let natureObj = {};
                    natureObj["name"] = nature["name"];
                    natureObj["data"] = [];

                    data.series.push(natureObj);
                }

                populateNatureSeriesAjax(paginate + 1);
            },

            error: function () {
                if (data.series.length !== 0) {
                    getOfficeListAjax("TOTREQ_DESC", officePaginateNo);
                }
            }
        });
    }

    function getOfficeListAjax (orderCommand="TOTREQ_DESC", paginate) {
        $.ajax({
            method: "GET",

            url: "api/office/?order_command=" + orderCommand + "&pagination_no=" + paginate,

            success: function (response) {
                let offices = response["offices"];

                let i;
                for (i=0; i < offices.length; i++) {
                    data.labels[i] = offices[i]["name"];

                    for (let obj of data.series) {
                        obj["data"][i] = 0;
                    }

                    countNatureByOfficeRequests(offices[i]["id"], i);
                }
            }
        });
    }

    var activeAjaxConnection = 0;
    function countNatureByOfficeRequests (officeId, index, orderCommand="TOTREQ_DESC", paginate=1) {
        $.ajax({
            method: "GET",

            beforeSend: function () {
                activeAjaxConnection++;
            },

            url: "api/nature/office/" + officeId + "?order_command=" + orderCommand + "&pagination_no=" + paginate,

            success: function (response) {
                activeAjaxConnection--;

                for (let nature of response["natures"]) {
                    for (let obj of data.series) {
                        if (obj["name"] === nature["name"]) {
                            obj["data"][index] = nature["total_requests"];
                        }

                        if (options["high"] < nature["total_requests"]) {
                            options["high"] = nature["total_requests"];
                        }
                    }
                }

                countNatureByOfficeRequests(officeId, index, orderCommand, paginate+1);

                if (activeAjaxConnection === 0) {
                    setChart();
                }
            },

            error: function () {
                activeAjaxConnection--;

                if (activeAjaxConnection === 0) {
                    setChart();
                }
            }
        });
    }

    var legendContFirstInvoke = false;
    function setChart () {
        if (legendContFirstInvoke === true) {
            options["plugins"] = [];
        }

        legendContFirstInvoke = true;

        let chart = new Chartist.Bar(display, data, options);

        chart.on('draw', function(data) {
            if(data.type == 'bar') {
                data.element.animate({
                    y2: {
                        dur: '0.2s',
                        from: data.y1,
                        to: data.y2
                    }
                });
            }
        });
    }
});

document.querySelectorAll(".cs-tsp").forEach((card) => {
    const display = card.querySelector(".cs-tsp-d");
    var containerHeight = $(display).parent().outerHeight();
    display.style.height = containerHeight + 'px';

    const legendCont = document.querySelector(".cs-tsp-l");

    const traverserCont = card.querySelector(".btn-group");
    const leftTraverser = traverserCont.firstElementChild;
    const rightTraverser = traverserCont.lastElementChild;

    var technicianPaginateNo = 1;

    var data = {};
    data.labels = [];
    data.series = [];

    var options = {
        high: 0,
        width: '725px',
        height: containerHeight + 'px',
        axisY: {
            offset: 75
        },
        plugins: [
            Chartist.plugins.legend({
                position: legendCont,
                clickable: false
            })
        ]
    }
    
    readyDisplay("TOTREQ_DESC", technicianPaginateNo);
    populateNatureSeriesAjax();

    leftTraverser.addEventListener("click", () => {
        technicianPaginateNo--;

        readyDisplay("TOTREQ_DESC", technicianPaginateNo);

        getTechnicianListAjax("TOTREQ_DESC", technicianPaginateNo);
    });

    rightTraverser.addEventListener("click", () => {
        technicianPaginateNo++;

        readyDisplay("TOTREQ_DESC", technicianPaginateNo);

        getTechnicianListAjax("TOTREQ_DESC", technicianPaginateNo);
    });

    function readyDisplay (orderCommand="TOTREQ_DESC", paginate=1) {
        if (paginate > 1) {
            leftTraverser.disabled = false;

        } else {
            leftTraverser.disabled = true;
        }

        $.ajax({
            method: "GET",

            url: "api/technician/?order_command=" + orderCommand + "&pagination_no=" + (paginate + 1),

            success: function () {
                rightTraverser.disabled = false;
            },

            error: function () {
                rightTraverser.disabled = true;
            }
        });
    }

    function populateNatureSeriesAjax (paginate=1) {
        $.ajax({
            method: "GET",

            url: "api/nature/?pagination_no=" + paginate,

            success: function (response) {
                for (let nature of response["natures"]) {
                    let natureObj = {};
                    natureObj["name"] = nature["name"];
                    natureObj["data"] = [];

                    data.series.push(natureObj);
                }

                populateNatureSeriesAjax(paginate + 1);
            },

            error: function () {
                if (data.series.length !== 0) {
                    getTechnicianListAjax("TOTREQ_DESC", technicianPaginateNo);
                }
            }
        });
    }

    function getTechnicianListAjax (orderCommand="TOTREQ_DESC", paginate) {
        $.ajax({
            method: "GET",

            url: "api/technician/?order_command=" + orderCommand + "&pagination_no=" + paginate,

            success: function (response) {
                let technicians = response["technicians"];

                let i;
                for (i=0; i < technicians.length; i++) {
                    data.labels[i] = technicians[i]["name"];

                    for (let obj of data.series) {
                        obj["data"][i] = 0;
                    }

                    countNatureByTechnicianRequests(technicians[i]["id"], i);
                }
            }
        });
    }

    var activeAjaxConnection = 0;
    function countNatureByTechnicianRequests (technicianId, index, orderCommand="TOTREQ_DESC", paginate=1) {
        $.ajax({
            method: "GET",

            beforeSend: function () {
                activeAjaxConnection++;
            },

            url: "api/nature/technician/" + technicianId + "?order_command=" + orderCommand + "&pagination_no=" + paginate,

            success: function (response) {
                activeAjaxConnection--;

                for (let nature of response["natures"]) {
                    for (let obj of data.series) {
                        if (obj["name"] === nature["name"]) {
                            obj["data"][index] = nature["total_requests"];
                        }

                        if (options["high"] < nature["total_requests"]) {
                            options["high"] = nature["total_requests"];
                        }
                    }
                }

                countNatureByTechnicianRequests(technicianId, index, orderCommand, paginate+1);

                if (activeAjaxConnection === 0) {
                    setChart();
                }
            },

            error: function () {
                activeAjaxConnection--;

                if (activeAjaxConnection === 0) {
                    setChart();
                }
            }
        });
    }

    var legendContFirstInvoke = false;
    function setChart () {
        if (legendContFirstInvoke === true) {
            options["plugins"] = [];
        }

        legendContFirstInvoke = true;

        let chart = new Chartist.Bar(display, data, options);

        chart.on('draw', function(data) {
            if(data.type == 'bar') {
                data.element.animate({
                    y2: {
                        dur: '0.2s',
                        from: data.y1,
                        to: data.y2
                    }
                });
            }
        });
    }
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

// REQUESTS
function filterRequestsAjaxCall(queryString, listGroup, paginationNo) {
    window.scrollTo(0, 0);
    $(window).off('scroll');

    $(listGroup).find(".list-group-item-removable").remove();

    const loading = listGroup.querySelector(".rq-ld-sp");
    loading.classList.remove("d-none");
    loading.classList.add("d-block");

    const emptyFeedback = listGroup.querySelector(".rq-lg-empty");
    emptyFeedback.classList.remove("d-block");
    emptyFeedback.classList.add("d-none");

    const paginateImpasseFeedback = listGroup.querySelector(".rq-lg-paginate-impasse");
    paginateImpasseFeedback.classList.remove("d-block");
    paginateImpasseFeedback.classList.add("d-none");

    $.ajax({
        type: "GET",

        url:  "api/request/" + queryString + "?pagination_no=" + paginationNo,

        success: function (response) {
            let itemCount = populateRequestList(listGroup, response);

            emptyFeedback.classList.remove("d-block");
            emptyFeedback.classList.add("d-none");
            loading.classList.remove("d-block");
            loading.classList.add("d-none");

            if (itemCount < 20) {
                paginateImpasseFeedback.classList.remove("d-none");
                paginateImpasseFeedback.classList.add("d-block");
            } else {
                activateNextPaginate();
            }
        },

        error: function(xhr) {
            if (xhr.status === 404) {
                paginateImpasse = true;

                loading.classList.remove("d-block");
                loading.classList.add("d-none");

                emptyFeedback.classList.remove("d-none");
                emptyFeedback.classList.add("d-block");
            }
        }
    });

    function activateNextPaginate () {
        var activeAjaxConnection = false;

        $(window).scroll(function() {
            if(($(window).scrollTop() + $(window).height() == $(document).height()) && !activeAjaxConnection) {
                loading.classList.remove("d-none");
                loading.classList.add("d-block");
    
                paginationNo++;
    
                $.ajax({
                    beforeSend: function () {
                        activeAjaxConnection = true;
                    },
                    type: "GET",
            
                    url:  "api/request/" + queryString + "?pagination_no=" + paginationNo,
            
                    success: function (response) {
                        populateRequestList(listGroup, response);
            
                        loading.classList.remove("d-block");
                        loading.classList.add("d-none");
    
                        activeAjaxConnection = false;
                    },
    
                    error: function (xhr) {
                        if (xhr.status === 404) {
                            loading.classList.remove("d-block");
                            loading.classList.add("d-none");
    
                            paginateImpasseFeedback.classList.remove("d-none");
                            paginateImpasseFeedback.classList.add("d-block");
    
                            $(window).off('scroll');
                        }
                    }
                });
            }
        });
    }
}

function populateRequestList(listGroup, data) {
    var itemCount = 0;

    for (let request of data["requests"]) {
        let baseItem = listGroup.querySelector("#rq-lg-i");  

        let item = $(baseItem).clone().removeAttr("id").addClass("list-group-item list-group-item-removable");

        item.find(".rq-li-no").html("<span>" + request["no"] + "</span>");

        let date = new Date(request["date"]);
        item.find(".rq-li-da").html("<span class='li-da-normal'>" + (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear() + "</span><span class='li-da-active'>" + monthNames[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear() + "</span>");

        item.find(".rq-li-o").html("<span>" + request["client"]["name"] + "</span>");
        item.find(".rq-li-mo").html("<span>" + request["approach"]["name"] + "</span>");
        item.find(".rq-li-na").html("<span>" + request["type"]["name"] + "</span>");
        item.find(".rq-li-de").html("<span>" + request["detail"] + "</span>");
        
        var fixersCount = 0;
        var fixers = "<span id='li-t-active'><ul>";
        for (let fixer of request["fixers"]) {
            fixers += "<li>" + fixer["name"] + "</li>";
            fixersCount++;
        }
        fixers += `</ul></span><span class='badge badge-light border mx-auto'>${ fixersCount }</span>`;
        item.find(".rq-li-t").html(fixers);

        let resultBadge = document.createElement("div");
        resultBadge.classList.add("badge", "py-1");
        if (request["result"] === 0) {
            resultBadge.classList.add("badge-success");
            resultBadge.innerHTML = "Done";
        } else if (request["result"] === 1) {
            resultBadge.classList.add("badge-warning");
            resultBadge.innerHTML = "Pending";
        } else if (request["result"] === 2) {
            resultBadge.classList.add("badge-danger");
            resultBadge.innerHTML = "Cancelled";
        }
        item.find(".rq-li-re").html(resultBadge);

        let ratingBadge = document.createElement("div");
        ratingBadge.classList.add("badge", "py-1");
        if (request["rating"] === 0) {
            ratingBadge.classList.add("badge-success");
            ratingBadge.innerHTML = "Excellent";
        } else if (request["rating"] === 1) {
            ratingBadge.classList.add("badge-success");
            ratingBadge.innerHTML = "Very good";
        } else if (request["rating"] === 2) {
            ratingBadge.classList.add("badge-success");
            ratingBadge.innerHTML = "Good";
        } else if (request["rating"] === 3) {
            ratingBadge.classList.add("badge-secondary");
            ratingBadge.innerHTML = "Fair";
        } else if (request["rating"] === 4) {
            ratingBadge.classList.add("badge-danger");
            ratingBadge.innerHTML = "Poor";
        } else if (request["rating"] === 5) {
            
        }
        item.find(".rq-li-ra").html(ratingBadge);

        item.insertBefore($(listGroup).find(".rq-ld-sp"));

        itemCount++;
    }

    return itemCount;
}

document.querySelectorAll(".rq-lg").forEach((listGroup) => {
    filterRequestsAjaxCall("", listGroup, 1);
});

document.querySelectorAll(".rq-tb-aa").forEach((container) => {
    container.querySelectorAll(".rq-tb-da").forEach((dateCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const yearSelect = dateCont.querySelector(".tb-da-y").querySelector("select");
        const monthSelect = dateCont.querySelector(".tb-da-m").querySelector("select");

        $.ajax({
            type: "GET",

            url:  "api/request/",
    
            success: function (request) {
                let date = new Date(request["requests"][0]["date"]);
                let newestRequestYear = date.getFullYear();

                let inbetweenYearCount = newestRequestYear - 2015;
                    
                while (inbetweenYearCount >= 0) {
                    let yearOption = document.createElement("option");
                    
                    yearOption.innerHTML = (2015 + inbetweenYearCount).toString();
                    
                    yearSelect.append(yearOption)
                    
                    inbetweenYearCount--;
                }
            }
        });

        const filter = dateCont.querySelector("a");

        filter.addEventListener("click", () => {
            var queryString = "year/" + yearSelect.value;

            if (monthSelect.value != "0") {
                queryString += "/month/" + monthSelect.value;
            }

            filterRequestsAjaxCall(queryString, listGroup, 1);

            $(dateCont).trigger("click");
        });
    });

    container.querySelectorAll(".rq-tb-o").forEach((officeCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const officeOption = officeCont.querySelector(".tb-opt-cont");

        const manageBtn = officeCont.querySelector("button");
        const manageModal = document.querySelector(manageBtn.getAttribute("data-target"));
        const manageListGroup = manageModal.querySelector("ul");

        
        getOfficesAjaxCall(1);

        function getOfficesAjaxCall (paginationNo) {
            $.ajax({
                type: "GET",
    
                url:  "api/office/?pagination_no=" + paginationNo,
    
                success: function (response) {
                    for (let office of response["offices"]) {
                        let option = document.createElement("a");
    
                        option.classList.add("font-weight-light", "small");
                        option.innerHTML = office["name"];
    
                        option.addEventListener("click", () => {
                            filterRequestsAjaxCall("office/" + office["id"], listGroup, 1);

                            $(officeCont).trigger("click");
                        });
    
                        officeOption.append(option);
    
                        let item = $(manageListGroup.querySelector("#mng-offc-mdl-i")).clone().removeAttr("id").addClass("list-group-item");
    
                        item.attr("data-id", office["id"]);
                        item.find("span").html(office["name"]);
    
                        item.appendTo(manageListGroup);
                    }

                    getOfficesAjaxCall(paginationNo + 1);
                }
            });
        }
    });

    container.querySelectorAll(".rq-tb-m").forEach((modeCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const modeOption = modeCont.querySelector(".tb-opt-cont");

        const manageBtn = modeCont.querySelector("button");
        const manageModal = document.querySelector(manageBtn.getAttribute("data-target"));
        const manageListGroup = manageModal.querySelector("ul");

        getModesAjaxCall(1);

        function getModesAjaxCall (paginationNo) {
            $.ajax({
                type: "GET",
    
                url:  "api/mode/?pagination_no=" + paginationNo,
        
                success: function (response) {
                    for (let mode of response["modes"]) {
                        let option = document.createElement("a");
    
                        option.classList.add("font-weight-light", "small");
                        option.innerHTML = mode["name"];
    
                        option.addEventListener("click", () => {
                            filterRequestsAjaxCall("mode/" + mode["id"], listGroup, 1);

                            $(modeCont).trigger("click");
                        });
    
                        modeOption.append(option);
    
                        let item = $(manageListGroup.querySelector("#mng-md-mdl-i")).clone().removeAttr("id").addClass("list-group-item");
    
                        item.attr("data-id", mode["id"]);
                        item.find("span").html(mode["name"]);
    
                        item.appendTo(manageListGroup);
                    }

                    getModesAjaxCall(paginationNo + 1);
                }
            });
        }
    });

    container.querySelectorAll(".rq-tb-na").forEach((natureCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const natureOption = natureCont.querySelector(".tb-opt-cont");

        const manageBtn = natureCont.querySelector("button");
        const manageModal = document.querySelector(manageBtn.getAttribute("data-target"));
        const manageListGroup = manageModal.querySelector("ul");

        getNaturesAjaxCall(1);

        function getNaturesAjaxCall (paginationNo) {
            $.ajax({
                type: "GET",
    
                url:  "api/nature/?pagination_no=" + paginationNo,
        
                success: function (response) {
                    for (let nature of response["natures"]) {
                        let option = document.createElement("a");
    
                        option.classList.add("font-weight-light", "small");
                        option.innerHTML = nature["name"];
    
                        option.addEventListener("click", () => {
                            filterRequestsAjaxCall("nature/" + nature["id"], listGroup, 1);

                            $(natureCont).trigger("click");
                        });
    
                        natureOption.append(option);
    
                        let item = $(manageListGroup.querySelector("#mng-ntr-mdl-i")).clone().removeAttr("id").addClass("list-group-item");
    
                        item.attr("data-id", nature["id"]);
                        item.find("span").html(nature["name"]);
    
                        item.appendTo(manageListGroup);
                    }

                    getNaturesAjaxCall(paginationNo + 1);
                }
            });
        }
    });

    container.querySelectorAll(".rq-tb-t").forEach((technicianCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const technicianOption = technicianCont.querySelector(".tb-opt-cont");

        const manageBtn = technicianCont.querySelector("button");
        const manageModal = document.querySelector(manageBtn.getAttribute("data-target"));
        const manageListGroup = manageModal.querySelector("ul");

        getTechniciansAjaxCall(1);

        function getTechniciansAjaxCall (paginationNo) {
            $.ajax({
                type: "GET",
    
                url:  "api/technician/?pagination_no=" + paginationNo,
        
                success: function (response) {
                    for (let technician of response["technicians"]) {
                        let option = document.createElement("a");
    
                        option.classList.add("font-weight-light", "small");
                        option.innerHTML = technician["name"];
    
                        option.addEventListener("click", () => {
                            filterRequestsAjaxCall("technician/" + technician["id"], listGroup, 1);

                            $(technicianCont).trigger("click");
                        });
    
                        technicianOption.append(option);
    
                        let item = $(manageListGroup.querySelector("#mng-tch-mdl-i")).clone().removeAttr("id").addClass("list-group-item");
    
                        item.attr("data-id", technician["id"]);
                        item.find("span").html(technician["name"]);
    
                        item.appendTo(manageListGroup);
                    }

                    getTechniciansAjaxCall(paginationNo + 1);
                }
            });
        }
    });

    container.querySelectorAll(".rq-tb-re").forEach((resultCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const resultOption = resultCont.querySelector(".tb-opt-cont");

        resultOption.querySelectorAll("a").forEach((option) => {

            option.addEventListener("click", () => {
                filterRequestsAjaxCall("result/" + option.getAttribute("value"), listGroup, 1);

                $(resultCont).trigger("click");
            });
        });
    });

    container.querySelectorAll(".rq-tb-ra").forEach((ratingCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const ratingOption = ratingCont.querySelector(".tb-opt-cont");

        ratingOption.querySelectorAll("a").forEach((option) => {
            option.addEventListener("click", () => {
                filterRequestsAjaxCall("rating/" + option.getAttribute("value"), listGroup, 1);

                $(ratingCont).trigger("click");
            });
        });
    });

    container.querySelectorAll(".rq-tb-de").forEach((detailCont) => {
        const listGroup = document.querySelector(".rq-lg");

        const detailInput = detailCont.querySelector("input");
        const detailSubmit = detailCont.querySelector("a");

        detailSubmit.addEventListener("click", () => {
            filterRequestsAjaxCall("detail/" + detailInput.value, listGroup, 1);

            $(detailCont).trigger("click");
        });
    });
});

document.querySelectorAll(".frcr-cnt").forEach((toggle) => {
    const modal = document.querySelector(toggle.getAttribute("data-target"));
    const form = modal.querySelector("form");
    const formBody = form.querySelector(".modal-body");

    const submit = form.querySelector("#crtrq_submit_input");

    const photoFormGroup = formBody.querySelector(".crt-rq-pf");
    const noFormGroup = formBody.querySelector(".crt-rq-no");
    const dateFormGroup = formBody.querySelector(".crt-rq-da");

    const photoInput = photoFormGroup.querySelector("input");
    const noInput = noFormGroup.querySelector("input");
    const dateInput = dateFormGroup.querySelector("input");
    const officeInput = formBody.querySelector(".crt-rq-o").querySelector("select");
    const modeInput = formBody.querySelector(".crt-rq-m").querySelector("select");
    const natureInput = formBody.querySelector(".crt-rq-na").querySelector("select");
    const detailInput = formBody.querySelector(".crt-rq-de").querySelector("textarea");
    const technicianInput = formBody.querySelector(".crt-rq-t").querySelector("select");

    var photoInputChange = false;
    var selectInputChange = false;

    if (noInput.value != "") {
        $(modal).modal("show");
    }

    getOfficesAjaxCall(1);
    getModesAjaxCall(1);
    getNaturesAjaxCall(1);
    getTechniciansAjaxCall(1);

    function getOfficesAjaxCall (paginationNo) {
        $.ajax({
            type: "GET",

            url:  "api/office/?pagination_no=" + paginationNo,

            success: function (response) {
                for (let office of response["offices"]) {
                    let option = document.createElement("option");

                    option.value = office["id"];
                    option.innerHTML = office["name"];

                    officeInput.append(option);
                }

                getOfficesAjaxCall(paginationNo + 1);
            }
        });
    }

    function getModesAjaxCall (paginationNo) {
        $.ajax({
            type: "GET",

            url:  "api/mode/?pagination_no=" + paginationNo,
    
            success: function (response) {
                for (let mode of response["modes"]) {
                    let option = document.createElement("option");

                    option.value = mode["id"];
                    option.innerHTML = mode["name"];

                    modeInput.append(option);
                }

                getModesAjaxCall(paginationNo + 1);
            }
        });
    }

    function getNaturesAjaxCall (paginationNo) {
        $.ajax({
            type: "GET",

            url:  "api/nature/?pagination_no=" + paginationNo,
    
            success: function (response) {
                for (let nature of response["natures"]) {
                    let option = document.createElement("option");

                    option.value = nature["id"];
                    option.innerHTML = nature["name"];

                    natureInput.append(option);
                }

                getNaturesAjaxCall(paginationNo + 1);
            }
        });
    }

    function getTechniciansAjaxCall (paginationNo) {
        $.ajax({
            type: "GET",

            url:  "api/technician/?pagination_no=" + paginationNo,
    
            success: function (response) {
                for (let technician of response["technicians"]) {
                    let option = document.createElement("option");

                    option.value = technician["id"];
                    option.innerHTML = technician["name"];

                    technicianInput.append(option);
                }

                getTechniciansAjaxCall(paginationNo + 1);
            }
        });
    }

    const photoDropzone = photoFormGroup.querySelector(".drop-zone");
    const photoLoadPrompt = photoDropzone.querySelector(".prompt__load-photo");
    const photoDisposePrompt = photoDropzone.querySelector(".prompt__dispose-photo");

    photoLoadPrompt.addEventListener("click", () => {
        photoInput.click();
    });

    photoDisposePrompt.addEventListener("click", () => {
        photoInput.value = "";

        updatePhotoThumbnail(photoDropzone);

        photoDisposePrompt.classList.remove("d-block");
        photoDisposePrompt.classList.add("d-none");

        photoInputChange = false;
    });

    photoInput.addEventListener("change", () => {
        if (photoInput.files.length) {
            updatePhotoThumbnail(photoDropzone, photoInput.files[0]);

            photoDisposePrompt.classList.remove("d-none");
            photoDisposePrompt.classList.add("d-block");
        }

        photoInputChange = true;
    });

    photoDropzone.addEventListener("dragover", (e) => {
        e.preventDefault();

        photoDropzone.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
        photoDropzone.addEventListener(type, () => {
            photoDropzone.classList.remove("drop-zone--over");
        });
    });

    photoDropzone.addEventListener("drop", (e) => {
        e.preventDefault();

        if (e.dataTransfer.files.length) {
            photoInput.files = e.dataTransfer.files;

            updatePhotoThumbnail(photoDropzone, e.dataTransfer.files[0]);

            photoDisposePrompt.classList.remove("d-none");
            photoDisposePrompt.classList.add("d-block");
        }

        photoDropzone.classList.remove("drop-zone--over");
    });

    function updatePhotoThumbnail(dropzone, file) {
        if (file) {
            const reader = new FileReader();
      
            reader.readAsDataURL(file);
            reader.onload = () => {
                dropzone.style.backgroundImage = `url('${reader.result}')`;
            };

        } else {
            dropzone.style.backgroundImage = null;
        }
    }

    var currentDateString = currentYear.toString() + "-" + ((currentMonth < 10) ? ("0" + currentMonth.toString()) : (currentMonth.toString())) + "-" + ((currentDay < 10) ? ("0" + currentDay.toString()) : (currentDay.toString()));
    dateInput.setAttribute("max", currentDateString);
    var dateRegex = /^(?:19|20)(?:(?:[13579][26]|[02468][048])-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-9])|(?:(?!02)(?:0[1-9]|1[0-2])-(?:30))|(?:(?:0[13578]|1[02])-31))|(?:[0-9]{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-8])|(?:(?!02)(?:0[1-9]|1[0-2])-(?:29|30))|(?:(?:0[13578]|1[02])-31)))$/;

    var inputtedMonthFinal = "([1-9]|1[012])";
    var noRegexString = `${ inputtedMonthFinal }-([1-9]|[1-9][0-9]+)`;
    noInput.setAttribute("pattern", noRegexString);   
    
    var typingTimer;
    var doneTypingInterval = 1000;
    
    dateInput.addEventListener("change", function () {
        dateInput.classList.remove("is-valid");
        dateInput.classList.remove("is-invalid");

        if (dateRegex.test(dateInput.value) === true) {
            let splitInput = dateInput.value.split("-");
            let inputtedYear = splitInput[0];
            let inputtedMonth = splitInput[1];
            let inputtedDay = splitInput[2];

            if ((parseInt(inputtedYear) >= 2015) && (parseInt(inputtedYear) < parseInt(currentYear))) {
                inputtedMonthFinal = parseInt(inputtedMonth).toString();
                noRegexString = `${ inputtedMonthFinal }-([1-9]|[1-9][0-9]+)`;
                noInput.setAttribute("pattern", noRegexString);

                let noRegex = new RegExp("^"+noRegexString+"$");

                if (noRegex.test(noInput.value) === true) {
                    window.clearTimeout(typingTimer);

                    $(submit).attr("disabled", "true");
                    $(submit).val("Loading");

                    dateInput.classList.remove("is-invalid");
                    dateInput.classList.remove("is-valid");
                    noInput.classList.remove("is-invalid");
                    noInput.classList.remove("is-valid");


                    typingTimer = setTimeout(function () {
                        noInput.classList.remove("is-valid");
                        noInput.classList.remove("is-invalid");

                        $.ajax({
                            type: "GET",
                    
                            url:  "api/request/no/" + noInput.value + "/year/" + inputtedYear,
                    
                            success: function () {
                                dateInput.classList.add("is-invalid");
                                $(dateInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in this date year.");
                                noInput.setAttribute("pattern", "(?=" + noRegexString + ")(?=(?!" + noInput.value + ")).*");
                                noInput.classList.add("is-invalid");
                                $(noInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in the specified date year.");

                                $(submit).removeAttr("disabled");
                                $(submit).val("Create");
                                $(submit).html("Create");
                            },
                
                            error: function () {
                                dateInput.classList.add("is-valid");
                                $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                                noInput.classList.add("is-valid");
                                $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");

                                $(submit).removeAttr("disabled");
                                $(submit).val("Create");
                            }
                        });

                    }, doneTypingInterval);
    
                } else if (noInput.value) {
                    noInput.classList.remove("is-valid");
                    noInput.classList.remove("is-invalid");

                    dateInput.classList.add("is-valid");
                    $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                    noInput.classList.add("is-invalid");
                    $(noInput).closest(".form-group").find(".invalid-feedback").html("Value must follow the required format.");
    
                } else {
                    dateInput.classList.add("is-valid");
                    $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                }

            } else if ((parseInt(inputtedYear) === parseInt(currentYear))) {
                if (parseInt(inputtedMonth) < parseInt(currentMonth)) {
                    inputtedMonthFinal = parseInt(inputtedMonth).toString();
                    noRegexString = `${ inputtedMonthFinal }-([1-9]|[1-9][0-9]+)`;
                    noInput.setAttribute("pattern", noRegexString);

                    let noRegex = new RegExp("^"+noRegexString+"$");

                    if (noRegex.test(noInput.value) === true) {
                        window.clearTimeout(typingTimer);

                        $(submit).attr("disabled", "true");
                        $(submit).val("Loading");

                        dateInput.classList.remove("is-invalid");
                        dateInput.classList.remove("is-valid");
                        noInput.classList.remove("is-invalid");
                        noInput.classList.remove("is-valid");


                        typingTimer = setTimeout(function () {
                            noInput.classList.remove("is-valid");
                            noInput.classList.remove("is-invalid");

                            $.ajax({
                                type: "GET",
                        
                                url:  "api/request/no/" + noInput.value + "/year/" + inputtedYear,
                        
                                success: function () {
                                    dateInput.classList.add("is-invalid");
                                    $(dateInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in this date year.");
                                    noInput.setAttribute("pattern", "(?=" + noRegexString + ")(?=(?!" + noInput.value + ")).*");
                                    noInput.classList.add("is-invalid");
                                    $(noInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in the specified date year.");

                                    $(submit).removeAttr("disabled");
                                    $(submit).val("Create");
                                    $(submit).html("Create");
                                },
                    
                                error: function () {
                                    dateInput.classList.add("is-valid");
                                    $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                                    noInput.classList.add("is-valid");
                                    $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");

                                    $(submit).removeAttr("disabled");
                                    $(submit).val("Create");
                                }
                            });

                        }, doneTypingInterval);
        
                    } else if (noInput.value) {
                        noInput.classList.remove("is-valid");
                        noInput.classList.remove("is-invalid");

                        dateInput.classList.add("is-valid");
                        $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                        noInput.classList.add("is-invalid");
                        $(noInput).closest(".form-group").find(".invalid-feedback").html("Value must follow the required format.");
        
                    } else {
                        dateInput.classList.add("is-valid");
                        $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                    }
    
                } else if (parseInt(inputtedMonth) === parseInt(currentMonth)) {
                    if (parseInt(inputtedDay) <= parseInt(currentDay)) {
                        inputtedMonthFinal = parseInt(inputtedMonth).toString();
                        noRegexString = `${ inputtedMonthFinal }-([1-9]|[1-9][0-9]+)`;
                        noInput.setAttribute("pattern", noRegexString);

                        let noRegex = new RegExp("^"+noRegexString+"$");

                        if (noRegex.test(noInput.value) === true) {
                            window.clearTimeout(typingTimer);

                            $(submit).attr("disabled", "true");
                            $(submit).val("Loading");

                            dateInput.classList.remove("is-invalid");
                            dateInput.classList.remove("is-valid");
                            noInput.classList.remove("is-invalid");
                            noInput.classList.remove("is-valid");


                            typingTimer = setTimeout(function () {
                                noInput.classList.remove("is-valid");
                                noInput.classList.remove("is-invalid");

                                $.ajax({
                                    type: "GET",
                            
                                    url:  "api/request/no/" + noInput.value + "/year/" + inputtedYear,
                            
                                    success: function () {
                                        dateInput.classList.add("is-invalid");
                                        $(dateInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in this date year.");
                                        noInput.setAttribute("pattern", "(?=" + noRegexString + ")(?=(?!" + noInput.value + ")).*");
                                        noInput.classList.add("is-invalid");
                                        $(noInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in the specified date year.");

                                        $(submit).removeAttr("disabled");
                                        $(submit).val("Create");
                                        $(submit).html("Create");
                                    },
                        
                                    error: function () {
                                        dateInput.classList.add("is-valid");
                                        $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                                        noInput.classList.add("is-valid");
                                        $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");

                                        $(submit).removeAttr("disabled");
                                        $(submit).val("Create");
                                    }
                                });

                            }, doneTypingInterval);
            
                        } else if (noInput.value) {
                            noInput.classList.remove("is-valid");
                            noInput.classList.remove("is-invalid");
    
                            dateInput.classList.add("is-valid");
                            $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                            noInput.classList.add("is-invalid");
                            $(noInput).closest(".form-group").find(".invalid-feedback").html("Value must follow the required format.");
            
                        } else {
                            dateInput.classList.add("is-valid");
                            $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                        }
                        
                    } else {
                        dateInput.classList.add("is-invalid");
                        $(dateInput).closest(".form-group").find(".invalid-feedback").html("Value must be today or earlier.");
                    }
                } else {
                    dateInput.classList.add("is-invalid");
                    $(dateInput).closest(".form-group").find(".invalid-feedback").html("Value must be today or earlier.");
                }

            } else if (parseInt(inputtedYear) < 2015) {
                dateInput.classList.add("is-invalid");
                $(dateInput).closest(".form-group").find(".invalid-feedback").html("Value must be 01/01/2015 or later.");
               
            } else if (parseInt(inputtedYear) > parseInt(currentYear)) {
                dateInput.classList.add("is-invalid");
                $(dateInput).closest(".form-group").find(".invalid-feedback").html("Value must be today or earlier.");
            }

        } else {
            dateInput.classList.add("is-invalid");
            $(dateInput).closest(".form-group").find(".invalid-feedback").html("Value must follow the required format.");[]
        }
    });

    noInput.addEventListener("keyup", function () {
        noInput.classList.remove("is-valid");
        noInput.classList.remove("is-invalid");

        let noRegex = new RegExp("^"+noRegexString+"$");

        if (noRegex.test(noInput.value) === true) {
            if (dateRegex.test(dateInput.value) === true) {
                let splitInput = dateInput.value.split("-");
                let inputtedYear = splitInput[0];
                let inputtedMonth = splitInput[1];
                let inputtedDay = splitInput[2];

                if ((parseInt(inputtedYear) >= 2015) && (parseInt(inputtedYear) < parseInt(currentYear))) {
                    window.clearTimeout(typingTimer);

                    $(submit).attr("disabled", "true");
                    $(submit).val("Loading");

                    dateInput.classList.remove("is-invalid");
                    dateInput.classList.remove("is-valid");
                    noInput.classList.remove("is-invalid");
                    noInput.classList.remove("is-valid");

                    typingTimer = setTimeout(function () {
                        dateInput.classList.remove("is-valid");
                        dateInput.classList.remove("is-invalid");

                        $.ajax({
                            type: "GET",
                    
                            url:  "api/request/no/" + noInput.value + "/year/" + dateInput.value.split("-")[0],
                    
                            success: function () {
                                dateInput.classList.add("is-invalid");
                                $(dateInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in this date year.");
                                noInput.setAttribute("pattern", "(?=" + noRegexString + ")(?=(?!" + noInput.value + ")).*");
                                noInput.classList.add("is-invalid");
                                $(noInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in the specified date year.");

                                $(submit).removeAttr("disabled");
                                $(submit).val("Create");
                            },
                
                            error: function () {
                                dateInput.classList.add("is-valid");
                                $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                                noInput.classList.add("is-valid");
                                $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");

                                $(submit).removeAttr("disabled");
                                $(submit).val("Create");
                            }
                        });

                    }, doneTypingInterval);

                } else if ((parseInt(inputtedYear) === parseInt(currentYear))) {
                    if (parseInt(inputtedMonth) < parseInt(currentMonth)) {
                        window.clearTimeout(typingTimer);

                        $(submit).attr("disabled", "true");
                        $(submit).val("Loading");

                        dateInput.classList.remove("is-invalid");
                        dateInput.classList.remove("is-valid");
                        noInput.classList.remove("is-invalid");
                        noInput.classList.remove("is-valid");

                        typingTimer = setTimeout(function () {
                            dateInput.classList.remove("is-valid");
                            dateInput.classList.remove("is-invalid");

                            $.ajax({
                                type: "GET",
                        
                                url:  "api/request/no/" + noInput.value + "/year/" + dateInput.value.split("-")[0],
                        
                                success: function () {
                                    dateInput.classList.add("is-invalid");
                                    $(dateInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in this date year.");
                                    noInput.setAttribute("pattern", "(?=" + noRegexString + ")(?=(?!" + noInput.value + ")).*");
                                    noInput.classList.add("is-invalid");
                                    $(noInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in the specified date year.");

                                    $(submit).removeAttr("disabled");
                                    $(submit).val("Create");
                                },
                    
                                error: function () {
                                    dateInput.classList.add("is-valid");
                                    $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                                    noInput.classList.add("is-valid");
                                    $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");

                                    $(submit).removeAttr("disabled");
                                    $(submit).val("Create");
                                }
                            });

                        }, doneTypingInterval);

                    } else if (parseInt(inputtedMonth) === parseInt(currentMonth)) {
                        if (parseInt(inputtedDay) <= parseInt(currentDay)) {
                            window.clearTimeout(typingTimer);

                            $(submit).attr("disabled", "true");
                            $(submit).val("Loading");

                            dateInput.classList.remove("is-invalid");
                            dateInput.classList.remove("is-valid");
                            noInput.classList.remove("is-invalid");
                            noInput.classList.remove("is-valid");

                            typingTimer = setTimeout(function () {
                                dateInput.classList.remove("is-valid");
                                dateInput.classList.remove("is-invalid");

                                $.ajax({
                                    type: "GET",
                            
                                    url:  "api/request/no/" + noInput.value + "/year/" + dateInput.value.split("-")[0],
                            
                                    success: function () {
                                        dateInput.classList.add("is-invalid");
                                        $(dateInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in this date year.");
                                        noInput.setAttribute("pattern", "(?=" + noRegexString + ")(?=(?!" + noInput.value + ")).*");
                                        noInput.classList.add("is-invalid");
                                        $(noInput).closest(".form-group").find(".invalid-feedback").html("Request number already exist in the specified date year.");

                                        $(submit).removeAttr("disabled");
                                        $(submit).val("Create");
                                    },
                        
                                    error: function () {
                                        dateInput.classList.add("is-valid");
                                        $(dateInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                                        noInput.classList.add("is-valid");
                                        $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");

                                        $(submit).removeAttr("disabled");
                                        $(submit).val("Create");
                                    }
                                });

                            }, doneTypingInterval);

                        } else {
                            noInput.classList.add("is-valid");
                            $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                        }

                    } else {
                        noInput.classList.add("is-valid");
                        $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                    }

                } else if (parseInt(inputtedYear) < 2015) {
                    noInput.classList.add("is-valid");
                    $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");

                } else if (parseInt(inputtedYear) > parseInt(currentYear)) {
                    noInput.classList.add("is-valid");
                    $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
                }   

            } else if (!dateInput.value) {
                noInput.classList.add("is-valid");
                $(noInput).closest(".form-group").find(".valid-feedback").html("Looks good.");
            }


        } else {
            if (dateRegex.test(dateInput.value) === true) {
                noInput.classList.add("is-invalid");
                $(noInput).closest(".form-group").find(".invalid-feedback").html("Value must follow the required format.");

            } else if (!dateInput.value) {
                noInput.classList.add("is-invalid");
                $(noInput).closest(".form-group").find(".invalid-feedback").html("Value must follow the required format.");
            }
        }
    });

    [officeInput, modeInput, natureInput, technicianInput].forEach((input) => {
        input.addEventListener("click", () => {
            selectInputChange = true;
        });
    });

    const resultFormGroup = form.querySelector(".crt-rq-re");
    const ratingFormGroup = form.querySelector(".crt-rq-ra");
    resultFormGroup.querySelectorAll(".form-check-input").forEach((checkbox) => {
        ratingFormControl = ratingFormGroup.querySelector(".form-control");
        if ((checkbox.value == 0) && (checkbox.checked == true)) {
            ratingFormControl.querySelectorAll(".form-check-input").forEach((checkbox) => {
                $(checkbox).attr("required", true);

                checkbox.checked = false;
            });
            $(ratingFormControl).attr("required", "required");

        } else if ((checkbox.value == 1) && (checkbox.checked == true)) {
            $(ratingFormControl).addClass("bg-light");
            $(ratingFormControl).css("pointer-events", "none");

            ratingFormControl.querySelector("#crtrq_rating_input-5").checked = true;

        } else if ((checkbox.value == 2) && (checkbox.checked == true)) {
            $(ratingFormControl).addClass("bg-light");
            $(ratingFormControl).css("pointer-events", "none");
            
            ratingFormControl.querySelector("#crtrq_rating_input-5").checked = true;
        
        } else {
            $(ratingFormControl).addClass("bg-light");
            $(ratingFormControl).css("pointer-events", "none");
        }

        checkbox.addEventListener("click", (e) => {
            if (e.currentTarget.value == 0) {
                $(ratingFormControl).removeClass("bg-light");
                $(ratingFormControl).css("pointer-events", "all");

                ratingFormControl.querySelectorAll(".form-check-input").forEach((checkbox) => {
                    $(checkbox).attr("required", true);

                    checkbox.checked = false;
                });

            } else if (e.currentTarget.value == 1) {
                $(ratingFormControl).addClass("bg-light");
                $(ratingFormControl).css("pointer-events", "none");

                ratingFormControl.querySelector("#crtrq_rating_input-5").checked = true;
                
            } else if (e.currentTarget.value == 2) {
                $(ratingFormControl).addClass("bg-light");
                $(ratingFormControl).css("pointer-events", "none");

                ratingFormControl.querySelector("#crtrq_rating_input-5").checked = true;
            }

            selectInputChange = true;
        });
    });

    modalFooter = modal.querySelector(".modal-footer"); 
    closeWarning = modalFooter.querySelector("span");
    closeActionCont = modalFooter.querySelector(".mdl-cls-final");
    modalFormActionCont = modalFooter.querySelector(".mdl-frm-aa");
    
    modalCancelActionBtn = modalFormActionCont.querySelector(".btn-secondary");
    cancelExitBtn = closeActionCont.querySelector(".btn-outline-danger");

    $(modalCancelActionBtn).on("click", function() {
        if (noInput.value || dateInput.value || detailInput.value || selectInputChange || photoInputChange) {
            $(formBody).addClass("bg-light");
            $(formBody).find("input").css("opacity", "0.5");
            $(formBody).find("textarea").css("opacity", "0.5");
            $(formBody).find("select").css("opacity", "0.5");
            $(formBody).css("pointer-events", "none");

            modalFooter.classList.add("d-flex", "justify-content-between");
            modalFormActionCont.classList.remove("d-block");
            modalFormActionCont.classList.add("d-none");
            closeWarning.classList.remove("d-none");
            closeWarning.classList.add("d-block");
            closeActionCont.classList.remove("d-none");
            closeActionCont.classList.add("d-block");

        } else {
            $(modal).modal("hide");
        }
    });

    $(cancelExitBtn).on("click", function() {
        $(formBody).removeClass("bg-light");
        $(formBody).find("input").css("opacity", "1");
        $(formBody).find("textarea").css("opacity", "1");
        $(formBody).find("select").css("opacity", "1");
        $(formBody).css("pointer-events", "all");

        modalFooter.classList.remove("d-flex", "justify-content-between");
        modalFormActionCont.classList.add("d-block");
        modalFormActionCont.classList.remove("d-none");
        closeWarning.classList.add("d-none");
        closeWarning.classList.remove("d-block");
        closeActionCont.classList.add("d-none");
        closeActionCont.classList.remove("d-block");
    });

    $(modal).on("show.bs.modal", function () {
        $(toggle).hide(); 
    });

    $(modal).on("hide.bs.modal", function () {
        photoDisposePrompt.click();

        $(formBody).removeClass("bg-light");
        $(formBody).find("input").css("opacity", "1");
        $(formBody).find("textarea").css("opacity", "1");
        $(formBody).find("select").css("opacity", "1");
        $(formBody).css("pointer-events", "all");

        selectInputChange = false;

        noInput.value = "";
        dateInput.value = "";
        officeInput.selectedIndex = "0";
        modeInput.selectedIndex = "0";
        natureInput.selectedIndex = "0";
        technicianInput.value = "";
        detailInput.value = "";

        resultFormGroup.querySelectorAll("input").forEach((checkbox) => {
            checkbox.checked = false;
        });

        ratingFormGroup.querySelectorAll("input").forEach((checkbox) => {
            checkbox.checked = false;
        });

        form.querySelectorAll(".is-valid").forEach((input) => {
            input.classList.remove("is-valid");
        });

        form.querySelectorAll(".is-invalid").forEach((input) => {
            input.classList.remove("is-invalid");
            input.removeAttribute("placeholder");
        });

        modalFooter.classList.remove("d-flex", "justify-content-between");
        modalFormActionCont.classList.add("d-block");
        modalFormActionCont.classList.remove("d-none");
        closeWarning.classList.add("d-none");
        closeWarning.classList.remove("d-block");
        closeActionCont.classList.add("d-none");
        closeActionCont.classList.remove("d-block");
    });
    
    $(modal).on("hidden.bs.modal", function () {
        $(toggle).show(); 
    });
});

{
    const modal = $("#mng-offc-mdl");
    const modalBody = modal.find(".modal-body");
    
    const createForm = modal.find("#mdl-hdr-crtof");
    const editForm = modal.find("#mdl-hdr-edtof");
    const deleteForm = modal.find("#mdl-hdr-deltof");

    function editOffice (obj) {
        modalBody.css("pointer-events", "none");
        modalBody.addClass("d-none");
        createForm.removeClass("d-flex flex-row");
        createForm.addClass("d-none");
        editForm.removeClass("d-none");
        editForm.addClass("d-flex flex-row");

        let idInput = editForm.find("#edtof_id_input");
        idInput.val($(obj).closest("li").attr("data-id"));

        let officeName = $(obj).closest("li").find("span").html();

        let nameInput = editForm.find("#edtof_name_input");
        nameInput.attr("pattern", `^((?!(?<!\\S)${ officeName }(?!\\S)).*)$`);
        nameInput.val(officeName);
    } 

    function deleteOffice (obj) {
        modalBody.css("pointer-events", "none");
        modalBody.addClass("d-none");
        createForm.removeClass("d-flex flex-row");
        createForm.addClass("d-none");
        deleteForm.removeClass("d-none");
        deleteForm.addClass("d-flex flex-row");

        let idInput = deleteForm.find("#deltof_id_input");
        idInput.val($(obj).closest("li").attr("data-id"));

        let officeName = $(obj).closest("li").find("span").html();

        let nameInput = deleteForm.find("#deltof_name_input");
        nameInput.attr("pattern", `^(${ officeName })$`);
        nameInput.attr("placeholder", officeName);
    }

    function createOffice (obj) {
        editForm.trigger("reset");
        deleteForm.trigger("reset");

        modalBody.css("pointer-events", "all");
        modalBody.removeClass("d-none");

        let thisForm = $(obj).closest("form");
        
        thisForm.removeClass("d-flex flex-row");
        thisForm.addClass("d-none");

        createForm.removeClass("d-none");
        createForm.addClass("d-flex flex-row");
    }

    modal.on("hide.bs.modal", function () {
        createForm.trigger("reset");
        editForm.trigger("reset");
        deleteForm.trigger("reset");

        modalBody.css("pointer-events", "all");
        modalBody.removeClass("d-none");

        editForm.removeClass("d-flex flex-row");
        editForm.addClass("d-none");
        deleteForm.removeClass("d-flex flex-row");
        deleteForm.addClass("d-none");
        createForm.removeClass("d-none");
        createForm.addClass("d-flex flex-row");
    });
}

{
    const modal = $("#mng-md-mdl");
    const modalBody = modal.find(".modal-body");

    const createForm = modal.find("#mdl-hdr-crtmd");
    const editForm = modal.find("#mdl-hdr-edtmd");
    const deleteForm = modal.find("#mdl-hdr-deltmd");

    function editMode (obj) {
        modalBody.css("pointer-events", "none");
        modalBody.addClass("d-none");
        createForm.removeClass("d-flex flex-row");
        createForm.addClass("d-none");
        editForm.removeClass("d-none");
        editForm.addClass("d-flex flex-row");

        let idInput = editForm.find("#edtmd_id_input");
        idInput.val($(obj).closest("li").attr("data-id"));

        let modeName = $(obj).closest("li").find("span").html();

        let nameInput = editForm.find("#edtmd_name_input");
        nameInput.attr("pattern", `^((?!(?<!\\S)${ modeName }(?!\\S)).*)$`);
        nameInput.val(modeName);
    } 

    function deleteMode (obj) {
        modalBody.css("pointer-events", "none");
        modalBody.addClass("d-none");
        createForm.removeClass("d-flex flex-row");
        createForm.addClass("d-none");
        deleteForm.removeClass("d-none");
        deleteForm.addClass("d-flex flex-row");

        let idInput = deleteForm.find("#deltmd_id_input");
        idInput.val($(obj).closest("li").attr("data-id"));

        let modeName = $(obj).closest("li").find("span").html();

        let nameInput = deleteForm.find("#deltmd_name_input");
        nameInput.attr("pattern", `^(${ modeName })$`);
        nameInput.attr("placeholder", modeName);
    }

    function createMode (obj) {
        editForm.trigger("reset");
        deleteForm.trigger("reset");

        modalBody.css("pointer-events", "all");
        modalBody.removeClass("d-none");

        let thisForm = $(obj).closest("form");
        
        thisForm.removeClass("d-flex flex-row");
        thisForm.addClass("d-none");

        createForm.removeClass("d-none");
        createForm.addClass("d-flex flex-row");
    }

    modal.on("hide.bs.modal", function () {
        createForm.trigger("reset");
        editForm.trigger("reset");
        deleteForm.trigger("reset");

        modalBody.css("pointer-events", "all");
        modalBody.removeClass("d-none");

        editForm.removeClass("d-flex flex-row");
        editForm.addClass("d-none");
        deleteForm.removeClass("d-flex flex-row");
        deleteForm.addClass("d-none");
        createForm.removeClass("d-none");
        createForm.addClass("d-flex flex-row");
    });
}

{
    const modal = $("#mng-ntr-mdl");
    const modalBody = modal.find(".modal-body");

    const createForm = modal.find("#mdl-hdr-crtntr");
    const editForm = modal.find("#mdl-hdr-edtntr");
    const deleteForm = modal.find("#mdl-hdr-deltntr");

    function editNature (obj) {
        modalBody.css("pointer-events", "none");
        modalBody.addClass("d-none");
        createForm.removeClass("d-flex flex-row");
        createForm.addClass("d-none");
        editForm.removeClass("d-none");
        editForm.addClass("d-flex flex-row");

        let idInput = editForm.find("#edtnt_id_input");
        idInput.val($(obj).closest("li").attr("data-id"));

        let natureName = $(obj).closest("li").find("span").html();

        let nameInput = editForm.find("#edtnt_name_input");
        nameInput.attr("pattern", `^((?!(?<!\\S)${ natureName }(?!\\S)).*)$`);
        nameInput.val(natureName);
    } 

    function deleteNature (obj) {
        modalBody.css("pointer-events", "none");
        modalBody.addClass("d-none");
        createForm.removeClass("d-flex flex-row");
        createForm.addClass("d-none");
        deleteForm.removeClass("d-none");
        deleteForm.addClass("d-flex flex-row");

        let idInput = deleteForm.find("#deltnt_id_input");
        idInput.val($(obj).closest("li").attr("data-id"));

        let natureName = $(obj).closest("li").find("span").html();

        let nameInput = deleteForm.find("#deltnt_name_input");
        nameInput.attr("pattern", `^(${ natureName })$`);
        nameInput.attr("placeholder", natureName);
    }

    function createNature (obj) {
        editForm.trigger("reset");
        deleteForm.trigger("reset");

        modalBody.css("pointer-events", "all");
        modalBody.removeClass("d-none");

        let thisForm = $(obj).closest("form");
        
        thisForm.removeClass("d-flex flex-row");
        thisForm.addClass("d-none");

        createForm.removeClass("d-none");
        createForm.addClass("d-flex flex-row");
    }

    modal.on("hide.bs.modal", function () {
        createForm.trigger("reset");
        editForm.trigger("reset");
        deleteForm.trigger("reset");

        modalBody.css("pointer-events", "all");
        modalBody.removeClass("d-none");

        editForm.removeClass("d-flex flex-row");
        editForm.addClass("d-none");
        deleteForm.removeClass("d-flex flex-row");
        deleteForm.addClass("d-none");
        createForm.removeClass("d-none");
        createForm.addClass("d-flex flex-row");
    });
}

{
    const modal = $("#mng-tch-mdl");
    const modalBody = modal.find(".modal-body");

    const createForm = modal.find("#mdl-hdr-crttch");
    const editForm = modal.find("#mdl-hdr-edttch");
    const deleteForm = modal.find("#mdl-hdr-delttch");

    function editTechnician (obj) {
        modalBody.css("pointer-events", "none");
        modalBody.addClass("d-none");
        createForm.removeClass("d-flex flex-row");
        createForm.addClass("d-none");
        editForm.removeClass("d-none");
        editForm.addClass("d-flex flex-row");

        let idInput = editForm.find("#edttc_id_input");
        idInput.val($(obj).closest("li").attr("data-id"));

        let technicianName = $(obj).closest("li").find("span").html();

        let nameInput = editForm.find("#edttc_name_input");
        nameInput.attr("pattern", `^((?!(?<!\\S)${ technicianName }(?!\\S)).*)$`);
        nameInput.val(technicianName);
    } 

    function deleteTechnician (obj) {
        modalBody.css("pointer-events", "none");
        modalBody.addClass("d-none");
        createForm.removeClass("d-flex flex-row");
        createForm.addClass("d-none");
        deleteForm.removeClass("d-none");
        deleteForm.addClass("d-flex flex-row");

        let idInput = deleteForm.find("#delttc_id_input");
        idInput.val($(obj).closest("li").attr("data-id"));

        let technicianName = $(obj).closest("li").find("span").html();

        let nameInput = deleteForm.find("#delttc_name_input");
        nameInput.attr("pattern", `^(${ technicianName })$`);
        nameInput.attr("placeholder", technicianName);
    }

    function createTechnician (obj) {
        editForm.trigger("reset");
        deleteForm.trigger("reset");

        modalBody.css("pointer-events", "all");
        modalBody.removeClass("d-none");

        let thisForm = $(obj).closest("form");
        
        thisForm.removeClass("d-flex flex-row");
        thisForm.addClass("d-none");

        createForm.removeClass("d-none");
        createForm.addClass("d-flex flex-row");
    }

    modal.on("hide.bs.modal", function () {
        createForm.trigger("reset");
        editForm.trigger("reset");
        deleteForm.trigger("reset");

        modalBody.css("pointer-events", "all");
        modalBody.removeClass("d-none");

        editForm.removeClass("d-flex flex-row");
        editForm.addClass("d-none");
        deleteForm.removeClass("d-flex flex-row");
        deleteForm.addClass("d-none");
        createForm.removeClass("d-none");
        createForm.addClass("d-flex flex-row");
    });
}

// COMPONENTS
$(".alert-dismissible").fadeTo(5000, 500).slideUp(500, function (e) {
    $(e).alert("close");
});