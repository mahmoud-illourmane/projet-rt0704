var spinner, glowDivs, pageContent;

pageContent = $(".body");

/**
 * Cette méthode permet d'arrêter l'animation de préchargement des données.
*/
function stopLoadingAnimation() {
    // Fait disparaître progressivement l'élément avec la classe 'spinner' en 200 ms
    spinner.fadeOut(200);
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

        // Démarre l'animation de chargement
        spinner.show();
        glowDivs.show();
        stopLoadingAnimation();
    /*== END/Loading animation ==*/
    
    /*== Inputs pour modifier des infos sur un film ==*/
        // Je cache les boutons de confirmation de la modification par défaut
        $('.confirm-icon-button').hide();

        // Je désactive tous les inputs par défaut
        $('.input-edit-movie').prop('disabled', true);
        $('.select-edit-movie').prop('disabled', true);

        // Attache un gestionnaire de clic au bouton "edit"
        $('.edit-icon-button').on('click', function() {
            // Trouve l'élément parent '.edit-data-movie' du bouton cliqué
            var editDataMovie = $(this).closest('.edit-data-movie');
            
            // Trouve l'input enfant avec la classe '.input-edit-movie' dans '.edit-data-movie'
            var inputEditMovie = editDataMovie.find('.input-edit-movie');

            // le bouton de confirmation de la modification apporté
            var confirmDataButton = editDataMovie.find('.confirm-icon-button');
            confirmDataButton.fadeIn();

            inputEditMovie.prop('disabled', false);
            inputEditMovie.addClass('custom-input-shadow');
        });

        // Attache un gestionnaire de clic au bouton"check"
        $('.confirm-icon-button').on('click', function() {
            // Séléction de l'input adéquat
            var editDataMovie = $(this).closest('.edit-data-movie');        // Trouve le div parent sur lequel se trouve l'icon click
            var inputEditMovie = editDataMovie.find('.input-edit-movie');   // Récupère l'input qui se trouve dans le même div que l'icon click
            inputEditMovie.prop('disabled', true);
            inputEditMovie.removeClass('custom-input-shadow');

            // le bouton de confirmation de la modification apporté
            var confirmDataButton = editDataMovie.find('.confirm-icon-button');
            confirmDataButton.hide();

            // Séléction de la valeur originel
            // Sélectionne l'élément "movie-name" parent
            var movieNameContainer = $(this).closest('.movie-info');

            // Sélectionne l'élément avec la classe "original-data" à partir de "movieNameContainer"
            var originalData = movieNameContainer.find('.original-data').data('original');
            var originalDataElement = movieNameContainer.find('.original-data');

            // Informations à envoyer au serveur
            var movieId = $('#movie-id').val();
            var inputName = inputEditMovie.attr('name');
            var inputContent = inputEditMovie.val();

            // Compare la valeur originale avec la valeur actuelle de l'input
            if (inputContent === originalData || inputContent == null || parseInt(inputContent, 10) === parseInt(originalData, 10)) {
                showToastMessage("Aucun changement détecté", "text-success");
                return; // Arrête l'exécution si les données sont identiques
            }

            var data = {
                movieId: movieId,
                inputName: inputName,
                inputContent: inputContent
            };

            // Requête AJAX avec l'ID du film et la donnée à modifier
            $.ajax({
                url: '/edit-movie/send',
                method: 'PATCH',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function (response) {
                    if (response.status == "200") {
                        showToastMessage(response.message, "text-success");

                        // Je crée un nouvel élément pour le contenu existant
                        // Et je lui affecte un style css d'une rayure sur le texte
                        var existingContent = $('<span>').text(originalDataElement.text()).css({
                            'text-decoration-line': 'line-through',
                            'text-decoration-color': 'rgb(204, 105, 227)',
                            'text-decoration-style': 'solid',
                            'text-decoration-thickness': '3px'
                        });

                        // Pour écrire le nouveau texte à coté de l'ancien rayé sans rayer le nouveau texte
                        originalDataElement.html(existingContent);
                        originalDataElement.append(' ' + inputContent);
                    } else {
                        showToastMessage(response.error, "text-danger");
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log("Statut de l'erreur : ", textStatus);
                    console.log("Texte de l'erreur : ", errorThrown);
                    console.log("Réponse du serveur : ", jqXHR.responseText);
                    console.log("Code d'état : ", jqXHR.status);

                    // Affiche un message d'erreur à l'utilisateur
                    showToastMessage("Une erreur est survenue : " + textStatus + " - " + errorThrown, "text-danger");
                }
            });
        });
    /*== END/Inputs pour modifier des infos sur un film ==*/
});