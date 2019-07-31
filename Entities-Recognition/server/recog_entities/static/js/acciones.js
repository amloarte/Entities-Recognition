$(document).ready(function() {
    $("#cont1").hide(1500);
    /*cuando el docoumento (website) este cargado haga*/
    $('.ir-arriba').click(function() {
        /*al dar click en el boton*/
        $('body, html').animate({
            /*suba*/
            scrollTop: '0px'
        }, 300);
        /*300 miliseg (tiempo de subir)*/
    });
});