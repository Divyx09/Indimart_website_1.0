$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function() {
    // console.log("plus clicked")
    var id = $(this).attr("pid").toString();

    var eml = this.parentNode.children[2];
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            // console.log(data)
            // console.log("Success")
            location.reload();
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


$('.minus-cart').click(function() {
    // console.log("plus clicked")
    var id = $(this).attr("pid").toString();

    var eml = this.parentNode.children[2];
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            // console.log(data)
            // console.log("Success")
            location.reload();
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


$('.remove-cart').click(function() {
    // console.log("plus clicked")
    var id = $(this).attr("pid").toString();

    var eml = this
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            // console.log("delete")
            // console.log("Success")
            // location.reload();
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

const refreshBtn = document.getElementById("remove ");

function handleClick() {
    history.go(0);
}

refreshBtn.addEventListener("click", handleClick);

function loadGoogleTranslate() {
    new google.translate.TranslateElement("google_element");
}