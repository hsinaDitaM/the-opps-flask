(async function(){
    let response = await fetch('/api/users');
    let users = await response.json();

    if(users["status"] == "error") {
        boardcastMessage(users["message"], "error");
        return;
    }

    let mainTable = document.getElementById("users-table");

    async function saveEdit() {
        let input_fields = this.parentElement.parentElement.getElementsByTagName("input");

        let payload = {}
        for(let input_field of input_fields) {
            payload[input_field.name] = input_field.value;
        }

        let response = await fetch("/api/users", {
            method: "UPDATE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        })

        let reply = await response.json();
        if(reply.status == "error") {
            boardcastMessage(reply.message, "error");
            return;
        } else if(reply.status == "success") {
            boardcastMessage("Updated user successfully", "success");
        }

        for(let input_field of input_fields) {
            input_field.readOnly = true;
        }

        this.innerHTML = "Edit";
        this.onclick = saveEdit;
    }

    function editUser() {
        input_fields = this.parentElement.parentElement.getElementsByTagName("input");
        for(let input_field of input_fields) {
            if(input_field.name == "id") continue;
            input_field.readOnly = false;
        }

        this.innerHTML = "Save";
        this.onclick = saveEdit;
    }
    
    async function deleteUser() {
        let response = await fetch("/api/users", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id: this.parentElement.parentElement.getElementsByTagName("input")[0].value,
            }),
        })

        let reply = await response.json();
        if(reply.status == "error") {
            boardcastMessage(reply.message, "error");
            return;
        } else if(reply.status == "success") {
            boardcastMessage("Deleted user successfully", "success");
        }

        this.parentElement.parentElement.remove();
    }

    for(let user of users["users"]) {
        let row = document.createElement("tr");
        row.innerHTML = `
        <td><input type="text" value="${user.id}" name="id" readonly/></td>
        <td><input type="text" value="${user.email}" name="email" readonly/></td>
        <td><input type="text" value="${user.username}" name="username" readonly/></td>
        <td><input type="text" value="${user.password}" name="password" readonly/></td>
        <td><input type="text" value="${user.role}" name="role" readonly/></td>
        `;

        let td = document.createElement("td");
        let editButton = document.createElement("button");
        editButton.innerHTML = "Edit";
        editButton.onclick = editUser;

        let deleteButton = document.createElement("button");
        deleteButton.innerHTML = "Delete";
        deleteButton.onclick = deleteUser;

        td.appendChild(editButton);
        td.appendChild(deleteButton);

        row.appendChild(td);
        mainTable.appendChild(row);
    }
})();