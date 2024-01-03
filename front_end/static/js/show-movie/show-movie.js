var spinner, glowDivs, pageContent;

pageContent = $(".body");

/**
 * Cette méthode permet d'arrêter l'animation de préchargement des données.
 */
function stopLoadingAnimation() {
    // Fait disparaître progressivement l'élément avec la classe 'spinner' en 200 ms
    spinner.fadeOut(200);

    // Fait disparaître progressivement les éléments avec la classe 'glowDivs' en 200 ms
    // Une fois que la disparition est terminée, affiche progressivement l'élément avec la classe 'pageContent' en 200 ms
    glowDivs.fadeOut(200).promise().done(function() {
        pageContent.fadeIn(200);
    });
}

$(document).ready(function() {
    /*== Loading animation ==*/
        // Initialisation des variables globales
        spinner = $("#loading-animation");
        glowDivs = $(".glow-div");

        spinner.show();
        glowDivs.show();
        stopLoadingAnimation();
    /*== END/Loading animation ==*/

    // Utilise la variable globale movieNotation
    var ratingContainer = $('.movie-rating');
    
    var ratingHTML = '';
    for (var i = 0; i < 5; i++) {
        if (i < movieNotation) {
            ratingHTML += '<i class="material-icons font-size-L star-gold">star</i>';
        } else {
            ratingHTML += '<i class="material-icons font-size-L star-silver">star_border</i>'; // Assume 'star_border' is the class for empty stars
        }
    }
    
    ratingContainer.html(ratingHTML);

    var img = document.querySelector('.movie-img img'); // Sélectionne l'image
    img.onload = function() {
        var colorThief = new ColorThief();
        var dominantColor = colorThief.getColor(img); // Obtient la couleur dominante
        var movieElement = document.querySelector('.movie');
        var rgbColor = 'rgba(' + dominantColor[0] + ', ' + dominantColor[1] + ', ' + dominantColor[2] + ', 0.6)'; // Convertir en chaîne rgba
        movieElement.style.boxShadow = '0px 0px 80px ' + rgbColor; // Applique le box-shadow
    };       
        
    // Si l'image est déjà chargée (à partir du cache), déclenchement manuel de l'événement onload
    if (img.complete) {
        img.onload();
    }        
});