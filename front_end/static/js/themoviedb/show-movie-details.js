$(document).ready(function () {
    stopLoadingAnimation();

    // Gestionnaire d'événement pour ajouter un film depuis theMovieDb à la vidéothèque de l'utilisateur
    $('#btnAddToVideotheque').on('click', function() {
        var link = $(this);   // Je récupère le bouton pour le désactiver
        var originalContent = link.html();  // Je stock le bouton originel
        // Je lance un spinner
        link.html('<div class="spinner-border text-primary" role="status"><span class="visually-hidden"></span></div>');
        // Je désactive le bouton
        link.prop('disabled', true);

        // Récupère le texte complet de synopsis
        var synopsis = $('.span-synopsis').text();
        // Limite le aux 500 premiers caractères
        var synopsisAbrege = synopsis.substring(0, 500);

        // Extraction du nom de l'image
        var imgMovieUrl = $('.img-movie').attr('src');
        var imgMovieWithoutMime = imgMovieUrl.split('/').pop().split('.').shift();
        var imgMovieMime = imgMovieUrl.split('.').pop();
        imgMovie = imgMovieWithoutMime+'.'+imgMovieMime;

        // Extraction de la première catégorie
        var categories = $('.category').text()
        var categorieArray = categories.split(',');
        var categorie = categorieArray[0];
        
        // Modification de la notation pour la mettre en base 5
        var notationOriginale = parseFloat($('.notation').text());  
        var notation = parseInt(Math.round(notationOriginale / 2)); 

        // Préparation de l'URL et des données pour la requête AJAX
        var apiUrl = '/api/videotheque/add/movie/from/themoviedb';

        var movieData = {
            title: $('.title').text(),
            coverImage: imgMovie,
            releaseDate: $('.release').text(),
            category: categorie,
            notation: notation,
            synopsis: synopsisAbrege,
        };

        // Requête AJAX
        $.ajax({
            url: apiUrl,
            method: 'POST',
            data: JSON.stringify(movieData),
            contentType: 'application/json',
            success: function(response) {
                if(response.status == "200") {
                    showToastMessage(response.message, "text-success");
                }else {
                    showToastMessage(response.error, "text-danger");
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Erreur AJAX :', textStatus, errorThrown);
            },
            complete: function() {
                link.hide();
            }
        });
    });

});
