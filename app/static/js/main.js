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
document.querySelectorAll(".rq-lg").forEach((listGroup) => {
    $.ajax({
        type: "GET",

        url: "/api/request/",

        success: function (response) {
            populateRequestList(listGroup, response);
        }
    });
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

            url:  "/api/request/newest",
    
            success: function (request) {
                let date = new Date(request["date"]);

                OldestRequestAjaxCall(date.getFullYear());
            }
        });

        function OldestRequestAjaxCall(newestRequestYear) {
            $.ajax({
                type: "GET",
        
                url:  "/api/request/oldest",
        
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

        filter.addEventListener("click", (e) => {
            while (listGroup.lastChild.id !== "rq-lg-i") {
                listGroup.removeChild(listGroup.lastChild);
            }
            
            var urlString = "/api/request/year/" + yearSelect.value;

            if (monthSelect.value != "0") {
                urlString += "/month/" + monthSelect.value;
            }

            $.ajax({
                type: "GET",
        
                url:  urlString,
        
                success: function (response) {
                    populateRequestList(listGroup, response);
                }
            });
        });
    });
});

function populateRequestList(listGroup, data) {
    for (let request of data["requests"]) {
        let baseItem = listGroup.querySelector("#rq-lg-i");  

        let item = $(baseItem).clone().removeAttr("id").addClass("list-group-item");

        item.find(".rq-li-no").html("<span>" + request["no"] + "</span>");

        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        let date = new Date(request["date"]);
        item.find(".rq-li-da").html("<span class='li-da-normal'>" + (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear() + "</span><span class='li-da-active'>" + monthNames[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear() + "</span>");

        item.find(".rq-li-o").html("<span>" + request["office"]["name"] + "</span>");
        item.find(".rq-li-mo").html("<span>" + request["mode"]["name"] + "</span>");
        item.find(".rq-li-na").html("<span>" + request["nature"]["name"] + "</span>");
        item.find(".rq-li-de").html("<span>" + request["detail"] + "</span>");
        
        var techniciansCount = 0;
        var technicians = "<span class='li-t-active'><ul>";
        for (let technician of request["technicians"]) {
            technicians += "<li>" + technician["name"] + "</li>";
            techniciansCount++;
        }
        technicians += `</ul></span><span class='badge badge-light border mx-auto'>${ techniciansCount }</span>`;
        item.find(".rq-li-t").html(technicians);

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
        } else if (!request["rating"]) {
            if (request["result"] === 1) {
                ratingBadge.classList.add("badge-warning");
                ratingBadge.innerHTML = "Pending";
            } else if (request["result"] === 2) {
                ratingBadge.classList.add("badge-danger");
                ratingBadge.innerHTML = "Cancelled";
            }
        }
        item.find(".rq-li-ra").html(ratingBadge);

        item.appendTo(listGroup);
    }
}

document.querySelectorAll(".frcr-cnt").forEach((toggle) => {
    const modal = document.querySelector(toggle.getAttribute("data-target"));

    modal.querySelectorAll(".crt-rq-pf").forEach((formGroup) => {
        const dropzone = formGroup.querySelector(".drop-zone");
        
        const input = dropzone.querySelector("input");

        const loadPrompt = dropzone.querySelector(".prompt__load-photo");
        const disposePrompt = dropzone.querySelector(".prompt__dispose-photo");

        loadPrompt.addEventListener("click", (e) => {
            input.click();
        });

        disposePrompt.addEventListener("click", (e) => {
            input.value = "";

            updateThumbnail(dropzone);

            disposePrompt.classList.remove("d-block");
            disposePrompt.classList.add("d-none");
        });

        input.addEventListener("change", (e) => {
            if (input.files.length) {
                updateThumbnail(dropzone, input.files[0]);

                disposePrompt.classList.remove("d-none");
                disposePrompt.classList.add("d-block");
            }
        });

        dropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropzone.classList.add("drop-zone--over");
        });
        
        ["dragleave", "dragend"].forEach((type) => {
            dropzone.addEventListener(type, (e) => {
                dropzone.classList.remove("drop-zone--over");
            });
        });
        
        dropzone.addEventListener("drop", (e) => {
            e.preventDefault();
        
            if (e.dataTransfer.files.length) {
              input.files = e.dataTransfer.files;
              
              updateThumbnail(dropzone, e.dataTransfer.files[0]);

              disposePrompt.classList.remove("d-none");
              disposePrompt.classList.add("d-block");
            }
        
            dropzone.classList.remove("drop-zone--over");
        });

        function updateThumbnail(dropzone, file) {
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
    });

    const noFormGroup = modal.querySelector(".crt-rq-no");
    const dateFormGroup = modal.querySelector(".crt-rq-da");

    const noInput = noFormGroup.querySelector("input");
    const dateInput = dateFormGroup.querySelector("input");

    if (noInput.value != "") {
        $(modal).modal("show");
    }

    const thisYear = new Date().getFullYear();

    const noRegex = /^([1-9]|1[012])-([1-9]|([1-9][0-9]))+$/;
    const dateRegex = /^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$/;

    var typingTimer;
    const doneTypingInterval = 500;

    noInput.addEventListener("keyup", (e) => {
        let thisInput = e.currentTarget;

        if (noRegex.test(thisInput.value) === true) {
            window.clearTimeout(typingTimer);

            let noInputMonth = parseInt(thisInput.value.split("-")[0]);

            if (noInputMonth < 10) {
                noInputMonth = "0" + noInputMonth.toString();

            } else {
                noInputMonth = noInputMonth.toString();
            }

            if (dateRegex.test(dateInput.value) === true) {
                let splitDateInputArr = dateInput.value.split("-");

                splitDateInputArr.splice(1, 1, noInputMonth);
                dateInput.value = splitDateInputArr.join("-");

            } else {
                dateInput.value = `${ thisYear }-${ noInputMonth }-01`;
            }

            thisInput.classList.remove("is-invalid");
            $(thisInput).closest(".form-group").find(".invalid-feedback").html("");

        } else {
            window.clearTimeout(typingTimer);

            thisInput.classList.remove("is-invalid");
            $(thisInput).closest(".form-group").find(".invalid-feedback").html("");

            typingTimer = setTimeout(function () {
                thisInput.classList.add("is-invalid");
                $(thisInput).closest(".form-group").find(".invalid-feedback").html("Invalid request number.");
            }, doneTypingInterval)
        }
    });

    dateInput.addEventListener("change", (e) => {
        let thisInput = e.currentTarget;

        if (dateRegex.test(thisInput.value) === true) {
            let dateInputMonth = parseInt(thisInput.value.split("-")[1]);

            if (noRegex.test(noInput.value) === true) {
                let splitNoInputArr = noInput.value.split("-");

                splitNoInputArr.splice(0, 1, dateInputMonth.toString())
                noInput.value = splitNoInputArr.join("-");

            } else {
                noInput.classList.remove("is-invalid");
                $(noInput).closest(".form-group").find(".invalid-feedback").html("");

                noInput.value = `${ (dateInputMonth).toString() }-1`;
            }
        }
    });

    const resultFormGroup = modal.querySelector(".crt-rq-re");
    const ratingFormGroup = modal.querySelector(".crt-rq-ra");
    resultFormGroup.querySelectorAll(".form-check-input").forEach((checkbox) => {
        if ((checkbox.value == 0) && (checkbox.checked == true)) {
            $(ratingFormGroup.querySelectorAll(".form-check-input")).attr("disabled", false);


        } else if ((checkbox.value == 1) && (checkbox.checked == true)) {
            ratingFormGroup.querySelector("input").setAttribute("disabled", true);

            ratingFormGroup.querySelectorAll(".form-check-input").forEach((checkbox) => {
                checkbox.checked = false;
            });
        } else if ((checkbox.value == 2) && (checkbox.checked == true)) {
            $(ratingFormGroup.querySelectorAll(".form-check-input")).attr("disabled", true);

            ratingFormGroup.querySelectorAll(".form-check-input").forEach((checkbox) => {
                checkbox.checked = false;
            });
        }

        checkbox.addEventListener("click", (e) => {
            if (e.currentTarget.value == 0) {
                $(ratingFormGroup.querySelectorAll(".form-check-input")).attr("disabled", false);

                $(ratingFormGroup.querySelectorAll(".form-check-input")).attr("required", true);

            } else if (e.currentTarget.value == 1) {
                $(ratingFormGroup.querySelectorAll(".form-check-input")).attr("disabled", true);

                $(ratingFormGroup.querySelectorAll(".form-check-input")).attr("required", false);

                ratingFormGroup.querySelectorAll(".form-check-input").forEach((checkbox) => {
                    checkbox.checked = false;
                });
            } else if (e.currentTarget.value == 2) {
                $(ratingFormGroup.querySelectorAll(".form-check-input")).attr("disabled", true);

                $(ratingFormGroup.querySelectorAll(".form-check-input")).attr("required", false);

                ratingFormGroup.querySelectorAll(".form-check-input").forEach((checkbox) => {
                    checkbox.checked = false;
                });
            }
        });
    });

    $(modal).on("show.bs.modal", function (e) {
        $(toggle).hide();
    });
    
    $(modal).on("hidden.bs.modal", function () {
        $(toggle).show();
    });
});

// COMPONENTS
$(".alert-dismissible").fadeTo(5000, 500).slideUp(500, function (e) {
    $(e).alert("close");
});