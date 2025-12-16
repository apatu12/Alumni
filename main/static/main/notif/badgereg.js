setInterval(function(){
    $.get('/api/notification/badge/registo/request/',function(data) {
        document.getElementById("notifbadge").innerHTML = data.value;
    });
}, 5000);
