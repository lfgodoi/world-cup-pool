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
                                        <td class='td-ranking' id='td-name-${name}'>${name}</td>\
                                        <td class='td-ranking' id='td-username-${username}'>${username}</td>\
                                        <td class='td-ranking' id='td-password-${password}'>${password}</td>\
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

// Salvando palpites de um jogador
function saveGuesses() {
    var guesses = {};
    var matches = document.querySelectorAll(".table-match");
    for (let i = 0; i < matches.length; ++i) {
        guesses[i + 1] = [parseInt(matches[i].querySelector(".goals-1").value),
                            parseInt(matches[i].querySelector(".goals-2").value),
                            0];
    }
    $.ajax({
        url : "/saveguesses",
        contentType: "application/json;charset=utf-8",
        type: 'POST',
        data: JSON.stringify({guesses}),
        dataType: "json",
        success: function(data) {
            alert("Palpites salvos com sucesso!");
        },  
        error: function() {
            alert("Erro ao salvar palpites! Verifique os campos preenchidos.");
        }
    })
}