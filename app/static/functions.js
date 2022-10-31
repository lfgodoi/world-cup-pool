// Function for adding a new user
function addUser() {
    var name = document.querySelector("#input-add-name").value;
    var username = document.querySelector("#input-add-username").value;
    var password = document.querySelector("#input-add-password").value;
    $.ajax({
        url : "/adduser",
        type : "POST",
        data : { "name": name,
                 "username": username,
                 "password": password },
        success: function(data) {
            var userTable = document.querySelector("#table-users");
            userTable.innerHTML += `<tr id='tr-user-${username}'>\
                                        <td class='td-ranking' id='td-name-${name}'><input type='text' value=${name} class='input-user' id='input-name-${username}'></td>\
                                        <td class='td-ranking' id='td-username-${username}'>${username}</td>\
                                        <td class='td-ranking' id='td-password-${password}'><input type='text' value=${password} class='input-user' id='input-password-${username}'></td>\
                                        <td class='td-ranking'><input type='button' class='button-user' id='button-update-${username}' value='Atualizar' onclick='updateUser(this)'></td>\
                                        <td class='td-ranking'><input type='button' class='button-user' id='button-delete-${username}' value='Excluir' onclick='deleteUser(this)'></td>\
                                    </tr>`
            document.querySelector("#input-add-name").value = "";
            document.querySelector("#input-add-username").value = "";
            document.querySelector("#input-add-password").value = "";
            alert("Jogador adicionado com sucesso!");
        },  
        error: function() {
            alert("Erro ao adicionar jogador! Verifique já não existe um jogador com o mesmo usuário.");
        }
    })    
}

// Função de remoção de usuário
function deleteUser(target) {
    var elementId = target.id;
    var username = elementId.split("button-delete-").pop();
    $.ajax({
        url : "/deleteuser",
        type : "POST",
        data : { "username": username },
        success: function(data) {
            var userRow = document.querySelector("#tr-user-" + username);
            userRow.parentNode.removeChild(userRow)
            alert("Jogador removido com sucesso!");
        },  
        error: function() {
            alert("Erro ao remover jogador!");
        }
    })
}

// Função de atualização de usuário
function updateUser(target) {
    var elementId = target.id;
    var username = elementId.split("button-update-").pop();
    var name = document.querySelector("#input-name-" + username).value;
    var password = document.querySelector("#input-password-" + username).value;
    $.ajax({
        url : "/updateuser",
        type : "POST",
        data : { "username": username,
                 "name": name,
                 "password": password },
        success: function(data) {
            alert("Jogador atualizado com sucesso!");
        },  
        error: function() {
            alert("Erro ao atualizar jogador!");
        }
    })
}

// Salvando palpites de um jogador
function saveGuesses() {
    var guesses = {};
    var matches = document.querySelectorAll(".table-match");
    for (let i = 0; i < matches.length; ++i) {
        var goals1 = matches[i].querySelector(".goals-1").value;
        var goals2 = matches[i].querySelector(".goals-2").value;
        guesses[i + 1] = [parseInt(goals1),
                          parseInt(goals2),
                          0];
    }
    $.ajax({
        url : "/saveguesses",
        contentType: "application/json;charset=utf-8",
        type: 'POST',
        data: JSON.stringify({guesses}),
        dataType: "json",
        success: function(data) {
            alert("Palpites salvos com sucesso! Caracteres não numéricos foram ignorados.");
        },  
        error: function() {
            alert("Erro ao salvar palpites! Verifique os campos preenchidos.");
        }
    })
}

// Tab group mechanism
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById("tab-" + tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Function for updating a match result
function updateMatch(target) {
    var elementId = target.id;
    var matchId = elementId.split("button-confirm-").pop();
    var goals1 = document.querySelector("#input-goals1-" + matchId).value;
    var goals2 = document.querySelector("#input-goals2-" + matchId).value;
    $.ajax({
        url : "/updatematch",
        type : "POST",
        data : { "match_id": matchId,
                 "goals_1": goals1,
                 "goals_2": goals2 },
        success: function(data) {
            alert("Resultado atualizado com sucesso!");
        },  
        error: function() {
            alert("Erro ao atualizar resultado! Verifique se os campos foram preenchidos com valores numéricos.");
        }
    })
}

// Modal window
$(document).ready(function() {
    var modal = document.querySelector("#div-modal");
    var buttonMenu = document.querySelector("#button-menu");
    var closeSpan = document.querySelectorAll(".close")[0];
    buttonMenu.addEventListener("click", function() {
        modal.style.display = "block";
    });
    closeSpan.addEventListener("click", function() {
        modal.style.display = "none";
    });
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    })
})

// Getting the current datetime
function getCurrentDatetime() {
    var currentDatetime = new Date(); 
    return currentDatetime
}

// Checking datetimes to disable guesses
function checkDatetimes(notify) {
    var matches = document.querySelectorAll(".table-match");
    for (let i = 0; i < matches.length; ++i) {
        var rawStrDatetime = matches[i].querySelector(".col-datetime").textContent; 
        var year = rawStrDatetime.slice(6, 10);
        var month = rawStrDatetime.slice(3, 5);
        var day = rawStrDatetime.slice(0, 2);
        var hour = rawStrDatetime.slice(11, 13);
        var intHour = parseInt(hour);
        var strHour = String(intHour - 1);
        if (strHour.length == 1) {
            strHour = "0" + strHour;
        }
        var minute = rawStrDatetime.slice(14, 16);
        var strDatetime = year + "-" + month + "-" + day + "T" + strHour + ":" + minute + ":00";
        var expireDatetime = new Date(strDatetime);
        var currentDatetime = getCurrentDatetime();
        if (currentDatetime >= expireDatetime) {
            var inputGoals1 = matches[i].querySelector(".goals-1");
            var inputGoals2 = matches[i].querySelector(".goals-2");
            if (inputGoals1.disabled == false || inputGoals2.disabled == false) {
                inputGoals1.disabled = true;
                inputGoals2.disabled = true;
                if (notify) {
                    alert("Tempo expirado para o jogo " + String(i + 1) + ". Bloqueado para novos palpites.");
                }
            }
            if (matches[i].querySelector(".col-match-status").textContent == "Ainda não jogado") {
                matches[i].querySelector(".col-match-status").innerHTML = "Partida em andamento";
            }
        }
    }
}

// Periodic check of datetimes
setInterval(function() {
    var url = window.location.pathname;
    if (url == "/guesses") {
        checkDatetimes(true);
    }
}, 60000)

// Initial check of datetimes
$(document).ready(function() {
    var url = window.location.pathname;
    if (url == "/guesses") {
        checkDatetimes(false);
    }
})