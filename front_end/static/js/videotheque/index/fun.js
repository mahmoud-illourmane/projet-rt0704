/**
 |
 |  This file contains all JS code for the index page.
 |  AUTHOR: MAHMOUD ILLOURMANE
 |  DATE: 12-23-23 US DATE
 | 
 */

// Modal add movie ID
var modalAddMovie = $('#modalAddMovie');                                

/*== Loading animation ==*/
    var spinner, glowDivs, pageContent;
    $(document).ready(function() {
        // Initialisation des variables globales
        spinner = $("#loading-animation");
        glowDivs = $(".glow-div");
        pageContent = $(".body");

        spinner.show();
        glowDivs.show();

        // Charge les films
        loadMoviesIndex();
    });
/*== END/Loading animation ==*/

/*== Body content ==*/

    /**
     * Ce code permet de filtrer les films affiché sur la page d'accueil de l'application selon la catégorie.
    */
    $('.filter-movies-index').change(function() {
        var selectedCategory = $(this).val();                   // Obtenir la catégorie sélectionnée
        $('.movie').each(function() {
            if ($(this).data('category') === selectedCategory 
                || selectedCategory === "Toutes") {
                $(this).show();                                 // Affiche les films si la catégorie correspond
            } else {
                $(this).hide();                                 // Cache les films sinon
            }
        });
    });    
       
    /**
     * Cette méthode sert à récupérer les films d'un utilisateur et à les afficher sur la page d'accueil
     */
    function loadMoviesIndex() {    
        $.ajax({
            url: 'api/get-movies/index', 
            method: 'GET',
            dataType: 'json',                           // Cette option indique le type de données que j'attends de recevoir en réponse du serveur
            success: function(response) {
                if(response.status == "200") {
                    let moviesContainer = $('.movies');
                    moviesContainer.empty();            // Vide le conteneurs parant avant de charger les nouveaux films
                    
                    if (response.data.movies && response.data.movies.length > 0) {
                        response.data.movies.forEach(movie => {
                            let imageUrl;
                            let imageFormat = 'webp';
                           
                            // Extrait les 30 premiers caractères pour vérifier la présence d'une extension de fichier
                            let first30Chars = movie.cover_image_base64.substring(0, 50);

                            // Vérifie si la chaîne contient une extension de fichier commune dans les 30 premiers caractères
                            if (/\.(jpg|png|webp)/i.test(first30Chars)) {
                                // Construit l'URL de l'image externe
                                imageUrl = `https://image.tmdb.org/t/p/w500/${movie.cover_image_base64}`;
                            } else {
                                // Je dois déterminer le format de l'image afin de pouvoir la reconstruire ultérieurement
                                if (movie.cover_image_format) {
                                    imageFormat = movie.cover_image_format.toLowerCase();
                                }
                                imageUrl = `data:image/${imageFormat};base64,${movie.cover_image_base64}`;
                            }
                            
                            // Le code HTML d'un film
                            let movieHtml = `
                                <div class="movie" data-movie-id="${movie.id}" data-category="${movie.category}">
                                    <div class="movie-picture mb-1">
                                        <img class="img-movie" src="${imageUrl}">
                                    </div>
                                    <div class="movie-title">
                                        <h6>${movie.movie_name}</h6>
                                    </div>
                                    <hr>
                                    <div class="d-flex gap-1 mb-1">
                                        <span class="material-icons font-size-XL color_8">category</span>
                                        <h6 class="font-size-M categories color_8">${movie.category}</h6>
                                    </div>
                                    <div class="d-flex gap-1 mb-1">
                                        <span class="material-icons font-size-XL color_8">calendar_month</span>
                                        <h6 class="font-size-M color_8">${movie.year_of_creation}</h6>
                                    </div>
                                    <div class="movie-rating d-flex gap-1 mb-1">
                                        <span class="material-icons color_8">stars</span>
                                        <div class="movie-rating-stars ">
                                            ${'<i class="material-icons font-size-L star-gold">star</i>'.repeat(parseInt(movie.notation, 10))}
                                            ${'<i class="material-icons font-size-L star-silver">star</i>'.repeat(5 - parseInt(movie.notation, 10))}
                                        </div>
                                    </div>
                                    <hr>
                                    <div class="movie-action text-center">
                                        <a id="deleteButtonMovie${movie.id}" data-movie-id="${movie.id}" data-movie-name="${movie.movie_name}" class="material-icons color_7">delete</a>
                                        <a id="editButtonMovie${movie.id}" href="/edit-movie/${movie.id}?category=${encodeURIComponent(movie.category)}&name=${encodeURIComponent(movie.movie_name)}&year=${encodeURIComponent(movie.year_of_creation)}&director=${encodeURIComponent(movie.director)}&synopsis=${encodeURIComponent(movie.synopsis)}&rating=${encodeURIComponent(movie.notation)}" class="material-icons color_3">edit</a>
                                        <a id="showMore${movie.id}" data-movie-id="${movie.id}" data-movie-name="${movie.movie_name}" data-movie-category="${movie.category}" data-movie-creation="${movie.year_of_creation}" data-movie-notation="${movie.notation}" data-movie-image64="${movie.cover_image_base64}" data-movie-synopsis="${movie.synopsis}" data-movie-director="${movie.director}" href="#" class="material-icons color_2">open_in_new</a>
                                    </div>
                                </div>
                            `;
                            
                            moviesContainer.append(movieHtml);
                        });

                        stopLoadingAnimation();  // Arrête l'animation de chargement
                    } else {
                        stopLoadingAnimation();
                        showToastMessage("Vous n'avez aucun film pour l'instant.", "text-danger");
                    }
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("[fun.js] Statut de l'erreur : ", textStatus);
                console.log("[fun.js] Texte de l'erreur : ", errorThrown);
                console.log("[fun.js] Réponse du serveur : ", jqXHR.responseText);
                console.log("[fun.js] Code d'état : ", jqXHR.status);
                
                let responseJson = JSON.parse(jqXHR.responseText);

                if (jqXHR.status == 500) {
                    let errorMessage = "Erreur interne du serveur : " + responseJson.error;
                    showToastMessage(errorMessage, "text-danger");
                }else{
                    let errorMessage = "Erreur : " + responseJson.error;
                    showToastMessage(errorMessage, "text-danger");
                }
            }
        });
    }   

    /**
     * Gestionnaire d'événement sur l'input de recherche
     */
    $('.input-search-movie').on('input', function() {
        let searchTerm = $(this).val().toLowerCase();

        // Parcoure toutes les divs avec la classe "movie"
        $('.movie').each(function() {
            let movieName = $(this).find('.movie-title h6').text().toLowerCase(); 

            // Vérifie si le nom du film contient le terme de recherche
            if (movieName.includes(searchTerm)) {
                $(this).show(); // Affiche la div du film s'il correspond à la recherche
            } else {
                $(this).hide(); // Masque la div du film s'il ne correspond pas à la recherche
            }
        });
    });

    /*== Envoi la demande POST pour afficher le contenu détaillés d'un film ==*/

        /*
        * Gestionnnaire d'évenement sur l'icon qui permet d'afficher la vue détaillé sur un film
        * La méthode est brute il existe plus simple.
        */
        $(document).on('click', 'a[id^="showMore"]', function (event) {
            event.preventDefault(); // Empêche la navigation par défaut

            // Récupération des données du film depuis les attributs data-* du lien
            var movieId = $(this).data('movie-id');
            var category = $(this).data('movie-category');
            var movieName = $(this).data('movie-name');
            var year = $(this).data('movie-creation');
            var notation = $(this).data('movie-notation');
            var image64 = $(this).data('movie-image64');
            var synopsis = $(this).data('movie-synopsis');
            var director = $(this).data('movie-director');

            // Créeation d'un objet de données à envoyer en POST
            var postData = {
                movieId: movieId,
                category: category,
                movieName: movieName,
                year: year,
                notation: notation,
                image64: image64,
                synopsis: synopsis,
                director: director
            };

            // Créeation d'un formulaire caché pour envoyer les données en POST
            var form = $('<form></form>');
            form.attr('method', 'POST');
            form.attr('action', '/show-movie'); // L'URL de votre route Flask
            for (var key in postData) {
                var input = $('<input></input>');
                input.attr('type', 'hidden');
                input.attr('name', key);
                input.attr('value', postData[key]);
                form.append(input);
            }

            form.appendTo('body').submit();
        });
    /*== END/Envoi la demande POST pour afficher le contenu détaillés d'un film ==*/

    /*== Suppression d'un film sur la page d'index ==*/

        /*
        * Gestionnnaire d'évenement sur l'icon qui permet de supprimer un film
        */
        $(document).on('click', 'a[id^="deleteButtonMovie"]', function () {
            // Je supprime le modal car sinon la prochaine fois que je voudrais
            // supprimer un autre film si la page n'a pas été rechargée, ça ne marchera pas.
            $('.parent-container-delete-movie').find('#confirmModalDelete').remove();
            var buttonId = $(this).attr('id');
            var movieName = $(this).data('movie-name');
            var movieId = $(this).data('movie-id');

            let confirmModalDeleteHTML = 
            `
                <!-- Modal -->
                <div class="modal fade" id="confirmModalDelete" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="confirmModalDelete" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h3 class="modal-title fs-5">Confirmer la suppression du film</h3>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <p class="text-center mt-1">Confirmer la suppression du film :<br><span class="color_7">${movieName}</span></p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                                <button id="btnConfirmDeleteMovie" data-id="${movieId}" type="button" class="btn btn-danger">Confirmer la suppression</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            $('.parent-container-delete-movie').append(confirmModalDeleteHTML);
            $('#confirmModalDelete').modal('show');
        });

        /**
         * Gestionnaire d'événements pour le bouton de confirmation de suppression d'un film sur la page index hors modal
         */
        $(document).on('click', '#btnConfirmDeleteMovie', function () {
            // Récupére l'ID du film à partir de l'attribut data-id
            var movieId = $(this).data('id');

            // Requête AJAX avec l'ID du film
            $.ajax({
                url: '/delete-movie',
                method: 'DELETE',
                contentType: 'application/json',
                data: JSON.stringify({ movieId: movieId }), // Convertir les données en chaîne JSON
                success: function (response) {
                    if (response.status == "200") {
                        $('#confirmModalDelete').modal('hide');
                        showToastMessage(response.message, "text-success");
                        // Je recharge de nouveau les films pour enlever celui qui a été supprimé
                        loadMovies();       
                        loadMoviesIndex();
                    } else {
                        showToastMessage(response.error, "text-danger");
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log("Statut de l'erreur : ", textStatus);
                    console.log("Texte de l'erreur : ", errorThrown);
                    console.log("Réponse du serveur : ", jqXHR.responseText);
                    console.log("Code d'état : ", jqXHR.status);
                    showToastMessage("Une erreur est survenue : " + textStatus + " - " + errorThrown, "text-danger");
                },
                complete() {
                }
            });
        });
    /*== END/Suppression d'un film sur la page d'index ==*/
    
/*== END/Body content ==*/