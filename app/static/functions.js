// Function for adding a new user
function addUser() {
    var name = document.querySelector("#input-add-name").value;
    name = name.trim();
    var username = document.querySelector("#input-add-username").value;
    username = username.trim();
    var password = document.querySelector("#input-add-password").value;
    password = password.trim();
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
                                        <td class='td-ranking'><button type='button' class='button-user' id='button-update-${username}' onclick='updateUser(this)'><i class='fa-solid fa-floppy-disk'></button></td>\
                                        <td class='td-ranking'><button type='button' class='button-user' id='button-delete-${username}' onclick='deleteUser(this)'><i class='fa-solid fa-trash'></button></td>\
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
    let text = `Tem certeza que deseja remover o jogador '${username}'?`;
    if (confirm(text) == true) {
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
    else {
        alert("ação cancelada!");
    }
}

// Função de atualização de usuário
function updateUser(target) {
    var elementId = target.id;
    var username = elementId.split("button-update-").pop();
    username = username.trim();
    var name = document.querySelector("#input-name-" + username).value;
    name = name.trim();
    var password = document.querySelector("#input-password-" + username).value;
    password = password.trim();
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
function saveGuesses(target, verbose) {
    var elementId = target.id;
    if (elementId.includes("input-goals-1")) {
        var matchId = elementId.split("input-goals-1-").pop();
    }
    else {
        var matchId = elementId.split("input-goals-2-").pop();
    } 
    var goals1 = document.querySelector("#input-goals-1-" + matchId).value;
    var goals2 = document.querySelector("#input-goals-2-" + matchId).value;
    $.ajax({
        url : "/saveguess",
        type : "POST",
        data : { "match_id": matchId,
                 "goals_1": goals1,
                 "goals_2": goals2 },
        dataType: "json",
        success: function(data) {
            if (verbose == true) {
                alert("Palpites salvos com sucesso!");
            }
        },  
        error: function() {
            if (elementId.includes("input-goals-1")) {
                document.querySelector("#input-goals-1-" + matchId).value = target.oldValue;
            }
            else {
                document.querySelector("#input-goals-2-" + matchId).value = target.oldValue;
            } 
            alert("Erro ao salvar palpites! Verifique os campos preenchidos e o horário do jogo.");
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
            alert("Erro ao atualizar resultado! Os campos devem ser ambos numéricos ou ambos vazios.");
        }
    })
}

// Opening the menu via alternative access
function openMenu() {
    var modal = document.querySelector("#div-modal");
    var closeSpan = document.querySelectorAll(".close")[0];
    modal.style.display = "block";
    closeSpan.addEventListener("click", function() {
        modal.style.display = "none";
    });
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    })
}

// Menu modal window
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

// Result comparison modal window
$(document).ready(function() {
    var modal = document.querySelector("#div-modal-comparison");
    var buttonComparison = document.querySelectorAll(".button-comparison");
    for (let i = 0; i < buttonComparison.length; ++i) {
        buttonComparison[i].addEventListener("click", function() {
            modal.style.display = "block";
        });
    }
    var closeSpan = document.querySelectorAll(".close-comparison")[0];
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
        var inputGoals1 = matches[i].querySelector(".goals-1");
        var inputGoals2 = matches[i].querySelector(".goals-2");
        if (currentDatetime >= expireDatetime) {
            inputGoals1.disabled = true;
            inputGoals2.disabled = true;
            if (notify) {
                alert("Tempo expirado para o jogo " + String(i + 1) + ". Bloqueado para novos palpites.");
            }
            if (matches[i].querySelector(".col-match-status").textContent == "Ainda não jogado") {
                matches[i].querySelector(".col-match-status").innerHTML = "Partida em andamento";
            }
        }
        else {
            inputGoals1.disabled = false;
            inputGoals2.disabled = false;
        }
    }
}

// Periodic check of datetimes
setInterval(function() {
    var url = window.location.pathname;
    if (url == "/guesses") {
        checkDatetimes(false);
    }
}, 60000)

// Initial check of datetimes
$(document).ready(function() {
    var url = window.location.pathname;
    if (url == "/guesses") {
        checkDatetimes(false);
    }
})

// Toggle password visibility
function togglePasswordVisibility() {
    var x = document.getElementById("password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

// Showing result comparison
function openComparison(button) {
    var elementId = button.id;
    var matchId = elementId.split("button-comparison-").pop();
    var colId = document.querySelector("#col-id-" + matchId).innerHTML;
    var team1 = document.querySelector("#col-team-1-" + matchId).innerHTML;
    var team2 = document.querySelector("#col-team-2-" + matchId).innerHTML;
    var tableComparison = document.querySelector("#table-comparison"); 
    tableComparison.innerHTML = "";
    $.ajax({
        url : "/getcomparison",
        type : "POST",
        data : { "match_id": matchId },
        success: function(data) {
            tableComparison.innerHTML += `<tr>
                                              <th class="th-comparison" colspan="3">${colId} - ${team1} x ${team2}</th>
                                          </tr>
                                          <tr>\
                                              <th class="th-comparison">Jogador</th>\
                                              <th class="th-comparison">Palpite</th>\
                                              <th class="th-comparison">Pontos</th>\
                                          </tr>`;            
            for (let i = 0; i < data.comparison.length; ++i) {
                if (data.comparison[i]["guess"][0] == "Nulo" && data.comparison[i]["guess"][1] == "Nulo") {
                    tableComparison.innerHTML += `<tr>\
                                                      <td class="td-comparison">${data.comparison[i]["name"]}</td>\
                                                      <td class="td-comparison">-</td>\
                                                      <td class="td-comparison">${data.comparison[i]["guess"][2]}</td>\
                                                  </tr>`;
                }
                else {
                    tableComparison.innerHTML += `<tr>\
                                                      <td class="td-comparison">${data.comparison[i]["name"]}</td>\
                                                      <td class="td-comparison">${data.comparison[i]["guess"][0]}&nbsp;x&nbsp;${data.comparison[i]["guess"][1]}</td>\
                                                      <td class="td-comparison">${data.comparison[i]["guess"][2]}</td>\
                                                  </tr>`;
                }
            }
            console.log("Resultado atualizado com sucesso!");
        },  
        error: function() {
            alert("Não foi possível abrir a janela de comparação de resultados!");
        }
    })
}