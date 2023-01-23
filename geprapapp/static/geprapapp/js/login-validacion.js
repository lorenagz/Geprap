
function ValidarLogin(){

    let u = document.getElementById("uname").value;
    let p = document.getElementById("upass").value;

    if(u == "Empleado@gmail.com" && p == "123456"){
            window.open("indexCrud.html");
    }
    else if(u == "Admin@gmail.com"){
        if(p == "123456"){
            window.open("indexCrud.html");
        }
    }
}

document.getElementById("validar").onclick = ValidarLogin();


