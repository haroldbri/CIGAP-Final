
const divembed = document.getElementById('view_documento')
const embed = document.getElementById('embed')
const btnvisualizardocumento = document.getElementById('btn_ver')
estado = false
btnvisualizardocumento.onclick = () => {
    estado = !estado
    if (estado == true) {

        divembed.style.height = '600px';
        embed.style.height = '580px';
        divembed.style.transition = 'all 0.3s'
        btnvisualizardocumento.innerHTML = 'Cerrar'
    }
    else {
        divembed.style.height = '0px';
        embed.style.height = '0px';
        divembed.style.transition = 'all 0.3s'
        btnvisualizardocumento.innerHTML = 'Visualizar documento'


    }


}
