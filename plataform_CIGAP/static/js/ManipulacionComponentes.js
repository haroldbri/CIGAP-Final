// import { setLogin } from './database/login.js'
// import { setEnvioNewUser } from './database/newUser.js'
// import { setRecuperarCuenta } from './database/recuperarCuenta.js'
// import { btnVolverLogin } from './Animaciones.js'


console.log('Componentes')

//componentes de QR
let i = 1;
const panel = document.getElementById('QR_Panel')
const btnQR = document.getElementById('btnQR')
const closebtn = document.getElementById('btnCloseQR')
const body = document.getElementById('body')
btnQR.onclick = function () {
    i += 1;
    panel.style.transition = 'all 0.2s'
    panel.style.width = '0%'
    if (i % 2 == 0) {
        panel.style.transition = 'all 0.2s'
        panel.style.width = '40%'
        panel.style.transform = 'rotate(360deg)'
        panel.style.zIndex = '1000'
        panel.style.opacity = '1'
    }
    else {
        panel.style.transform = 'rotate(0deg)'
        panel.style.transition = 'all 0.2s'
        panel.style.opacity = '0'
        panel.style.zIndex = '0'
    }
}

closebtn.onclick = () => {
    panel.style.opacity = '0'
    panel.style.zIndex = '0'

}





//Componentes de accceso del login
let email = document.getElementById('email')
let password = document.getElementById('password')
// componente envio  de informacion para accceso
let btnSubmit = document.getElementById('submit')


//componentes del formulario


//cambiar y ajustar el display del label no del div
let divs_input = document.getElementById('form-label')//nombre
let divs_input2 = document.getElementById('form-label2')//Apellido
let divs_input3 = document.getElementById('form-label3')//Correo
let divs_input4 = document.getElementById('form-label4')//Rol
let divs_input5 = document.getElementById('form-label5')//Password
let divs_input6 = document.getElementById('form-label6')//VerifyPassword

//inputs
let nombre = document.getElementById('inputNombre')
let apellido = document.getElementById('inputApellido')
let correo = document.getElementById('inputCorreo')
let rol = document.getElementById('inputRol')
let newPassword = document.getElementById('inputPassword')
let verifyPassword = document.getElementById('inputVerifyPassword')
let check = document.getElementById('gridCheck')
export let btnSubmitForm = document.getElementById('btnSubmitForm')//boton exportado para el cambio a submit

//componente de recuperar cuenta
//alerta
export var toastTrigger = document.getElementById('liveToastBtn')
export var toastLiveExample = document.getElementById('liveToast')
export var toastbodytext = document.getElementById('toast-text')
var toast = new bootstrap.Toast(toastLiveExample)

// Evento de login de usuario
btnSubmit.onclick = function () {
    let contentEmail = email.value;
    let contentPassword = password.value;

    setLogin(contentEmail, contentPassword)
    console.log(contentEmail, contentPassword)
    // const { a, b } = getVariables
    // console.log(a, b, 'datos rescuoerados')
}

//Recuperacion de cuenta
let aletLinkRecuperar = document.getElementById('linkRecuperar')

aletLinkRecuperar.onclick = function () {
    setRecuperarCuenta()
}

let valido_invalido = document.createElement('p')
// divs_input3.appendChild(valido_invalido)
// divs_input4.appendChild(valido_invalido)
// divs_input5.appendChild(valido_invalido)


nombre.oninput = function (event) {

    valido_invalido.classList.add('config-verfi')
    if (nombre.value != '') {
        if ((nombre.value).length < 3) {
            valido_invalido.classList.add('config-verfi')
            divs_input.appendChild(valido_invalido)
            valido_invalido.textContent = 'Verifica si realmente es el que deseas ⚠️'
            valido_invalido.style.color = 'var(--warning)'


        } else {
            valido_invalido.classList.add('config-verfi')
            divs_input.appendChild(valido_invalido)
            valido_invalido.textContent = 'Nombre valido ✅'
            valido_invalido.style.color = 'var(--verfif)'

        }

    } else {

        if (nombre.value || nombre.value == null) {
            valido_invalido.classList.add('config-verfi')
            divs_input.appendChild(valido_invalido)
            valido_invalido.textContent = 'Ingresa un nombre ❌'
            valido_invalido.style.color = 'var(--notverif)'


        }


    }

    console.log(event)
}


let valido_invalido2 = document.createElement('p')
apellido.oninput = function (event) {

    if (apellido.value != '') {
        if ((apellido.value).length < 3) {
            valido_invalido2.classList.add('config-verfi')
            divs_input2.appendChild(valido_invalido2)
            valido_invalido2.textContent = 'Verifica si realmente es el que deseas ⚠️'
            valido_invalido2.style.color = 'var(--warning)'


        } else {
            valido_invalido2.classList.add('config-verfi')
            divs_input2.appendChild(valido_invalido2)
            valido_invalido2.textContent = 'Apellido valido ✅'
            valido_invalido2.style.color = 'var(--verfif)'

        }

    } else {

        if (apellido.value == '' || apellido.value == null) {
            valido_invalido2.classList.add('config-verfi')
            divs_input2.appendChild(valido_invalido2)
            valido_invalido2.textContent = 'Ingresa un apellido ❌'
            valido_invalido2.style.color = 'var(--notverif)'


        }
    }
    console.log(event)
}

let valido_invalido3 = document.createElement('p')
function contarArrobas(cadena) {
    return cadena.split("").filter(caracter => caracter === "@").length;
}
correo.oninput = function (event) {
    var numArroba = contarArrobas(correo.value)


    if ((correo.value).length < 3) {
        valido_invalido3.classList.add('config-verfi')
        divs_input3.appendChild(valido_invalido3)
        valido_invalido3.textContent = 'Verifica tu correo ⚠️'
        valido_invalido3.style.color = 'var(--warning)'


    } else {
        if ((numArroba > 0)) {
            valido_invalido3.classList.add('config-verfi')
            divs_input3.appendChild(valido_invalido3)
            valido_invalido3.textContent = 'Correo valido ✅'
            valido_invalido3.style.color = 'var(--verfif)'

        } else {
            valido_invalido3.classList.add('config-verfi')
            divs_input3.appendChild(valido_invalido3)
            valido_invalido3.textContent = 'Ingresa un correo valido ⚠️'
            valido_invalido3.style.color = 'var(--warning)'

        }
    }
    if (correo.value == '' || correo.value == null) {
        valido_invalido3.classList.add('config-verfi')
        divs_input3.appendChild(valido_invalido3)
        valido_invalido3.textContent = 'Ingresa un correo ❌'
        valido_invalido3.style.color = 'var(--notverif)'
    }
    console.log(event)
}
let valido_invalido4 = document.createElement('p')
rol.oninput = function (event) {

    if (rol.value === 'Selecciona un rol') {

        valido_invalido4.classList.add('config-verfi')
        divs_input4.appendChild(valido_invalido4)
        valido_invalido4.textContent = 'Selecciona un rol ⚠️'
        valido_invalido4.style.color = 'var(--warning)'


    } else {
        valido_invalido4.classList.add('config-verfi')
        divs_input4.appendChild(valido_invalido4)
        valido_invalido4.textContent = 'Rol valido ✅'
        valido_invalido4.style.color = 'var(--verfif)'

    }


    console.log(event)
}
let valido_invalido5 = document.createElement('p')
newPassword.oninput = function (event) {

    if (newPassword.value != '') {
        if ((newPassword.value).length < 8) {
            valido_invalido5.classList.add('config-verfi')
            divs_input5.appendChild(valido_invalido5)
            valido_invalido5.textContent = 'Tu contraseña debe de tener mas de 8 caracteres ⚠️'
            valido_invalido5.style.color = 'var(--warning)'


        } else {
            valido_invalido5.classList.add('config-verfi')
            divs_input5.appendChild(valido_invalido5)
            valido_invalido5.textContent = 'NewPassword valido ✅'
            valido_invalido5.style.color = 'var(--verfif)'

        }

    } else {

        if (newPassword.value == '' || newPassword.value == null) {
            valido_invalido5.classList.add('config-verfi')
            divs_input5.appendChild(valido_invalido5)
            valido_invalido5.textContent = 'Ingresa un newPassword ❌'
            valido_invalido5.style.color = 'var(--notverif)'


        }
    }
    console.log(event)
}

let valido_invalido6 = document.createElement('p')
verifyPassword.oninput = function (event) {

    if (verifyPassword.value != newPassword.value) {

        valido_invalido6.classList.add('config-verfi')
        divs_input6.appendChild(valido_invalido6)
        valido_invalido6.textContent = 'Las contraseñas no coinciden ⚠️'
        valido_invalido6.style.color = 'var(--warning)'


    } else {
        valido_invalido6.classList.add('config-verfi')
        divs_input6.appendChild(valido_invalido6)
        valido_invalido6.textContent = 'Coinciden ✅'
        valido_invalido6.style.color = 'var(--verfif)'

    }



    console.log(event)
}



//Creacion de Nuevo ususario
btnSubmitForm.onclick = function () {

    // console.log(rol.value)
    console.log(nombre.value, apellido.value, rol.value, correo.value, newPassword.value)

    //verificar contraseña
    if ((nombre.value).length < 1 || (apellido.value).length < 1 || (correo.value).length < 1 || (password.value).length < 1 === '') {
        toastbodytext.textContent = 'Debes llenar cada uno de los campos 😣'
        toast.show()
    }
    else if ((newPassword.value).length < 8) {
        toastbodytext.textContent = 'Tu contraseña debe tener más de 8 caracteres🫡'
        toast.show()
    }
    else if (newPassword.value != verifyPassword.value) {
        toastbodytext.textContent = 'Las contraseñas ingresadas deben ser iguales😬'
        toast.show()
    }
    else if (!check.checked) {
        toastbodytext.textContent = 'Acepta los términos 😎'
        toast.show()

    } else {
        setEnvioNewUser(nombre.value, apellido.value, rol.value, correo.value, newPassword.value)
    }
}


export function vaciarComponentes() {
    nombre.value = ''
    apellido.value = ''
    correo.value = ''
    rol.value = 'Selecciona un rol'
    newPassword.value = ''
    verifyPassword.value = ''
    check.checked = false;
    valido_invalido.textContent = ''
    valido_invalido2.textContent = ''
    valido_invalido3.textContent = ''
    valido_invalido4.textContent = ''
    valido_invalido5.textContent = ''
    valido_invalido6.textContent = ''
    btnVolverLogin.classList.add('animacionBTNVOLVER')
}