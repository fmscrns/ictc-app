// DASHBOARD
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

// REQUESTS
function filterRequestsAjaxCall(queryString, listGroup) {
    while ($(listGroup.lastChild).hasClass("list-group-item-removable")) {
        listGroup.removeChild(listGroup.lastChild);
    }

    const loading = listGroup.querySelector(".rq-ld-sp");
    loading.classList.remove("d-none");
    loading.classList.add("d-block");

    const emptyFeedback = listGroup.querySelector(".rq-lg-empty");
    loading.classList.remove("d-block");
    loading.classList.add("d-none");

    $.ajax({
        type: "GET",

        url:  "api/request/" + queryString,

        success: function (response) {
            populateRequestList(listGroup, response);

            emptyFeedback.classList.remove("d-block");
            emptyFeedback.classList.add("d-none");
            loading.classList.remove("d-block");
            loading.classList.add("d-none");
        },

        error: function(xhr, textStatus, error) {
            if (xhr.status === 404) {
                emptyFeedback.classList.remove("d-none");
                emptyFeedback.classList.add("d-block");
            }
        }
    });
}

function populateRequestList(listGroup, data) {
    for (let request of data["requests"]) {
        let baseItem = listGroup.querySelector("#rq-lg-i");  

        let item = $(baseItem).clone().removeAttr("id").addClass("list-group-item list-group-item-removable");

        item.find(".rq-li-no").html("<span>" + request["no"] + "</span>");

        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
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

        item.appendTo(listGroup);
    }
}

document.querySelectorAll(".rq-lg").forEach((listGroup) => {
    filterRequestsAjaxCall("", listGroup);
});

document.querySelectorAll(".rq-tb-aa").forEach((container) => {
    container.querySelectorAll(".rq-tb-da").forEach((dateCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const yearSelect = dateCont.querySelector(".tb-da-y").querySelector("select");
        const monthSelect = dateCont.querySelector(".tb-da-m").querySelector("select");

        var newestRequestYear;
        var oldestRequestYear;

        $.ajax({
            type: "GET",

            url:  "api/request/newest",
    
            success: function (request) {
                let date = new Date(request["date"]);

                oldestRequestAjaxCall(date.getFullYear());
            }
        });

        function oldestRequestAjaxCall(newestRequestYear) {
            $.ajax({
                type: "GET",
        
                url:  "api/request/oldest",
        
                success: function (request) {
                    let date = new Date(request["date"]);

                    oldestRequestYear = date.getFullYear();

                    let inbetweenYearCount = oldestRequestYear - newestRequestYear;
                    
                    
                    while (inbetweenYearCount >= 0) {
                        let yearOption = document.createElement("option");
                        
                        yearOption.innerHTML = (newestRequestYear + inbetweenYearCount).toString();
                        
                        yearSelect.append(yearOption)
                        
                        inbetweenYearCount--;
                    }
                }
            });
        }

        const filter = dateCont.querySelector("a");

        filter.addEventListener("click", () => {
            var queryString = "year/" + yearSelect.value;

            if (monthSelect.value != "0") {
                queryString += "/month/" + monthSelect.value;
            }

            filterRequestsAjaxCall(queryString, listGroup);
        });
    });

    container.querySelectorAll(".rq-tb-o").forEach((officeCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const officeOption = officeCont.querySelector(".tb-opt-cont");

        const manageBtn = officeCont.querySelector("button");
        const manageModal = document.querySelector(manageBtn.getAttribute("data-target"));
        const manageListGroup = manageModal.querySelector("ul");

        $.ajax({
            type: "GET",

            url:  "api/office/",
    
            success: function (response) {
                for (let office of response["offices"]) {
                    let option = document.createElement("a");

                    option.classList.add("font-weight-light", "small");
                    option.innerHTML = office["name"];

                    option.addEventListener("click", () => {
                        filterRequestsAjaxCall("office/" + office["id"], listGroup);
                    });

                    officeOption.append(option);

                    let item = $(manageListGroup.querySelector("#mng-offc-mdl-i")).clone().removeAttr("id").addClass("list-group-item");

                    item.attr("data-id", office["id"]);
                    item.find("span").html(office["name"]);

                    item.appendTo(manageListGroup);
                }
            }
        });


    });

    container.querySelectorAll(".rq-tb-m").forEach((modeCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const modeOption = modeCont.querySelector(".tb-opt-cont");

        const manageBtn = modeCont.querySelector("button");
        const manageModal = document.querySelector(manageBtn.getAttribute("data-target"));
        const manageListGroup = manageModal.querySelector("ul");

        $.ajax({
            type: "GET",

            url:  "api/mode/",
    
            success: function (response) {
                for (let mode of response["modes"]) {
                    let option = document.createElement("a");

                    option.classList.add("font-weight-light", "small");
                    option.innerHTML = mode["name"];

                    option.addEventListener("click", () => {
                        filterRequestsAjaxCall("mode/" + mode["id"], listGroup);
                    });

                    modeOption.append(option);

                    let item = $(manageListGroup.querySelector("#mng-md-mdl-i")).clone().removeAttr("id").addClass("list-group-item");

                    item.attr("data-id", mode["id"]);
                    item.find("span").html(mode["name"]);

                    item.appendTo(manageListGroup);
                }
            }
        });
    });

    container.querySelectorAll(".rq-tb-na").forEach((natureCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const natureOption = natureCont.querySelector(".tb-opt-cont");

        const manageBtn = natureCont.querySelector("button");
        const manageModal = document.querySelector(manageBtn.getAttribute("data-target"));
        const manageListGroup = manageModal.querySelector("ul");

        $.ajax({
            type: "GET",

            url:  "api/nature/",
    
            success: function (response) {
                for (let nature of response["natures"]) {
                    let option = document.createElement("a");

                    option.classList.add("font-weight-light", "small");
                    option.innerHTML = nature["name"];

                    option.addEventListener("click", () => {
                        filterRequestsAjaxCall("nature/" + nature["id"], listGroup);
                    });

                    natureOption.append(option);

                    let item = $(manageListGroup.querySelector("#mng-ntr-mdl-i")).clone().removeAttr("id").addClass("list-group-item");

                    item.attr("data-id", nature["id"]);
                    item.find("span").html(nature["name"]);

                    item.appendTo(manageListGroup);
                }
            }
        });
    });

    container.querySelectorAll(".rq-tb-t").forEach((technicianCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const technicianOption = technicianCont.querySelector(".tb-opt-cont");

        const manageBtn = technicianCont.querySelector("button");
        const manageModal = document.querySelector(manageBtn.getAttribute("data-target"));
        const manageListGroup = manageModal.querySelector("ul");

        $.ajax({
            type: "GET",

            url:  "api/technician/",
    
            success: function (response) {
                for (let technician of response["technicians"]) {
                    let option = document.createElement("a");

                    option.classList.add("font-weight-light", "small");
                    option.innerHTML = technician["name"];

                    option.addEventListener("click", () => {
                        filterRequestsAjaxCall("technician/" + technician["id"], listGroup);
                    });

                    technicianOption.append(option);

                    let item = $(manageListGroup.querySelector("#mng-tch-mdl-i")).clone().removeAttr("id").addClass("list-group-item");

                    item.attr("data-id", technician["id"]);
                    item.find("span").html(technician["name"]);

                    item.appendTo(manageListGroup);
                }
            }
        });
    });

    container.querySelectorAll(".rq-tb-re").forEach((resultCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const resultOption = resultCont.querySelector(".tb-opt-cont");

        resultOption.querySelectorAll("a").forEach((option) => {

            option.addEventListener("click", () => {
                filterRequestsAjaxCall("result/" + option.getAttribute("value"), listGroup);
            });
        });
    });

    container.querySelectorAll(".rq-tb-ra").forEach((ratingCont) => {
        const listGroup = document.querySelector(".rq-lg");
        const ratingOption = ratingCont.querySelector(".tb-opt-cont");

        ratingOption.querySelectorAll("a").forEach((option) => {
            option.addEventListener("click", () => {
                filterRequestsAjaxCall("rating/" + option.getAttribute("value"), listGroup);
            });
        });
    });

    container.querySelectorAll(".rq-tb-de").forEach((detailCont) => {
        const listGroup = document.querySelector(".rq-lg");

        const detailInput = detailCont.querySelector("input");
        const detailSubmit = detailCont.querySelector("a");

        detailSubmit.addEventListener("click", () => {
            filterRequestsAjaxCall("detail/" + detailInput.value, listGroup);
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

    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    var currentMonth = parseInt(currentDate.getMonth()) + 1;
    var currentDay = parseInt(currentDate.getDate());
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