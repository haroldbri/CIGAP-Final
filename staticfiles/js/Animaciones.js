//recupercion de elementos del DOM
let dataemail = document.getElementById('email')
let datasena = document.getElementById('password')
let btnSubmit = document.getElementById('submit')

btnSubmit.onclick = function () {

    console.log(dataemail.value)
    console.log(datasena.value)
}


//Componentes a manipular para mostar la contraseña
let btnMostrarsena = document.getElementById('btnMostrarOcultar')
let iconEyeOn = document.getElementById('iconOn')
let iconEyeOff = document.getElementById('iconOff')

//Configuracion de evento de mostrar contraseña
let i = 1;
btnMostrarsena.onclick = function () {
    i += 1
    if (i % 2 === 0) {
        btnMostrarsena.style.transition = 'all 0.2s'
        btnMostrarsena.style.transform = 'rotate3d(0,2,0,-180deg)'
        datasena.type = 'text'
        iconEyeOff.style.display = 'flex';
        iconEyeOn.style.display = 'none';
    }
    else {
        btnMostrarsena.style.transition = 'all 0.2s'
        btnMostrarsena.style.transform = 'rotate3d(0,1,0,180deg)'
        datasena.type = 'password'
        iconEyeOn.style.display = 'flex';
        iconEyeOff.style.display = 'none';
    }
}






//llamar el formulario y cada uno de los componentes a tratar para la animacion de los mismos
let btnform = document.getElementById('btnform')
let container = document.getElementById('contenedor')
let sectionlogin = document.getElementById('sectionLogin')
let sectionForm = document.getElementById('sectionForm')
let coldatos = document.getElementById('col_datos')
let contentINF = document.getElementById('contentINF')
let colINF = document.getElementById('contentINF1')
let colINF2 = document.getElementById('contentINF2')
export var btnVolverLogin = document.getElementById('btnvolver')

coldatos.style.transition = 'all 0.5s linear(0 0%, 0 1.8%, 0.01 3.6%, 0.03 6.35%, 0.07 9.1%, 0.13 11.4%, 0.19 13.4%, 0.27 15%, 0.34 16.1%, 0.54 18.35%, 0.66 20.6%, 0.72 22.4%, 0.77 24.6%, 0.81 27.3%, 0.85 30.4%, 0.88 35.1%, 0.92 40.6%, 0.94 47.2%, 0.96 55%, 0.98 64%, 0.99 74.4%, 1 86.4%, 1 100%) 0s'
contentINF.style.transition = 'all 0.5s linear(0 0%, 0 1.8%, 0.01 3.6%, 0.03 6.35%, 0.07 9.1%, 0.13 11.4%, 0.19 13.4%, 0.27 15%, 0.34 16.1%, 0.54 18.35%, 0.66 20.6%, 0.72 22.4%, 0.77 24.6%, 0.81 27.3%, 0.85 30.4%, 0.88 35.1%, 0.92 40.6%, 0.94 47.2%, 0.96 55%, 0.98 64%, 0.99 74.4%, 1 86.4%, 1 100%) 0s'


//otras formas de transiciones
// coldatos.style.transition = 'all 0.8s cubic-bezier(0, 1, 1, 0) 0s'
// contentINF.style.transition = 'all 0.8s cubic-bezier(0, 1, 1, 0) 0s'

var toastTrigger = document.getElementById('liveToastBtn')
var toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
    toastTrigger.addEventListener('click', function () {
        var toast = new bootstrap.Toast(toastLiveExample)

        toast.show()
    })
}


//Ajustes de mostrar Form
btnform.onclick = function () {
    btnVolverLogin.style.display = 'flex'
    contentINF.style.transform = 'translateX(100%) rotate3d(0, 1, 0, 0deg)'
    coldatos.style.transform = 'translateX(-100%) rotate3d(0, 1, 0, 0deg)'
    colINF.style.display = 'none'
    colINF2.style.display = 'flex'
    sectionLogin.style.display = 'none';
    sectionForm.style.display = 'flex';
    btnVolverLogin.classList.remove('animacionBTNVOLVER')
};

//Ajustes de boton volver

btnVolverLogin.onclick = function () {
    contentINF.style.transform = 'translateX(0%) rotate3d(0, 1, 0, 0deg)'
    coldatos.style.transform = 'translateX(0%) rotate3d(0, 1, 0, 0deg)'
    btnVolverLogin.style.display = 'none'
    colINF.style.display = 'flex'
    colINF2.style.display = 'none'
    sectionLogin.style.display = 'flex';
    sectionForm.style.display = 'none';

}