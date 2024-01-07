/**
 * Fonction pour mettre à jour les champs de saisie en fonction du type de recherche sélectionné
 */
function updateSearchInput() {
    var searchType = $('#searchType').val();
    var searchInputContainer = $('#searchInputContainer');

    // Effacez les champs de saisie actuels
    searchInputContainer.empty();

    // Ajoutez les champs de saisie en fonction du type de recherche
    if (searchType === 'name') {
        searchInputContainer.append(`
            <label class="mt-3">2-Entrez le nom du film</label>
            <input type="text" class="mt-1 form-control" id="movieName" placeholder="Nom du Film">
        `);
    } else if (searchType === 'category') {
        // Afficher des cases à cocher pour toutes les catégories
        var categories = ['Action', 'Aventure', 'Animation', 'Comedie', 'Drame', 'Science-fiction', 'Horreur', 'Fantaisie', 'Thriller', 'Romance', 'Documentaire', 'Crime', 'Mystere', 'Guerre', 'Historique', 'Musique', 'Familial', 'Sport', 'Biographie', 'Western'];
        
        searchInputContainer.append('<label class="mt-3">2-Sélectionnez les catégories souhaitées</label>');
        for (var i = 0; i < categories.length; i++) {
            searchInputContainer.append(`
                <div class="form-check mt-1">
                    <input class="form-check-input" type="checkbox" name="movieCategory" id="category${i}" value="${categories[i]}">
                    <label class="form-check-label" for="category${i}">
                        ${categories[i]}
                    </label>
                </div>
            `);
        }
    } else if (searchType === 'year') {
        searchInputContainer.append(`
            <label class="mt-3">2-Entrez l'année souhaitée</label>
            <input type="number" class="mt-1 form-control" id="movieYear" placeholder="Année de Sortie">
        `);
    }
}

$(document).ready(function() {
    stopLoadingAnimation();

    updateSearchInput();
    $('.spinner-border').addClass('d-none');
    var btnSubmitSearch = $('#btn-submit-search');

    // Événement de changement de sélection du type de recherche
    $('#searchType').on('change', function() {
        updateSearchInput();
    });

    // Gére la soumission du formulaire de recherche
    $('#searchForm').on('submit', function(event) {

        /*== UX_UI ==*/
            // Affiche le spinner et masque le texte du bouton
            $(this).find('.spinner-border').removeClass('d-none');
            $(this).prop('disabled', true);
            $("#btn-submit-search").addClass("button-clicked");
            $("#btn-submit-search").prop('disabled', true);
        /*== END/UX_UI ==*/

        event.preventDefault();

        // Récupération des valeurs saisies par l'utilisateur
        var searchType = $('#searchType').val();

        var searchInputValue = '';  // La donnée que l'utilisateur souhaite chercher tableau de catégorie ou nom d'un film ou année de sortie de films.
        var operationId = 1;        // L'id de l'opération en fonction du choix de l'utilisateur
                                    // 1 :  Recherche d'un film par son nom
                                    // 2 :  Recherche de films par catégorie
                                    // 3 :  Recherche de films par année de sortie

        if (searchType === 'name') {
            searchInputValue = $('#movieName').val();
            operationId = 1;
        } else if (searchType === 'category') {
            // Récupération des catégories cochées sous forme de tableau JSON
            var selectedCategories = [];
            $('input[name="movieCategory"]:checked').each(function() {
                selectedCategories.push($(this).val());
            });
            searchInputValue = JSON.stringify(selectedCategories);
            operationId = 2;
        } else if (searchType === 'year') {
            searchInputValue = $('#movieYear').val();
            operationId = 3;
        }

        // Je forge la requête a envoyer au serveur
        var data = {
            operationId: operationId,
            searchInputValue: searchInputValue
        };
        
        // Requête AJAX avec l'ID du film et la donnée à modifier
        $.ajax({
            url: '/api/themoviedb/get',
            method: 'GET',
            dataType: 'json',
            data: data, // Pas besoin de JSON.stringify ici car les paramètres sont transmis dans l'url
            success: function (response) {
                if (response.status == "200") {
                    if (response.data.length === 0) {
                        showToastMessage("Aucune donnée trouvée", "text-danger");
                        searchType = '';
                        return;
                    }

                    showToastMessage(response.message, "text-success");
                    
                    // Sélection du conteneur des résultats de recherche
                    let searchResults = $("#searchResults");
                    // Efface le contenu préalable du conteneur
                    searchResults.empty();

                    // Parcoure des données des films et générer le code HTML
                    response.data.forEach((movie) => {
                        // Génération de l'URL de l'image
                        let imageUrl = `https://image.tmdb.org/t/p/w500${movie.cover_photo}`;

                        // Le code HTML d'un film
                        let movieHtml;
                        if (movie.cover_photo) {
                            movieHtml = `
                                <div class="movie" data-movie-id="${movie.id}" data-category="${movie.category}">
                                    <div class="movie-picture mb-1">
                                        <img class="img-movie" src="${imageUrl}">
                                    </div>
                                    <div class="movie-title">
                                        <h6>${movie.title}</h6>
                                    </div>
                                    <hr>
                                    <div class="d-flex gap-1 mb-1">
                                        <span class="material-icons font-size-XL color_8">category</span>
                                        <h6 class="font-size-M color_8">${movie.genres.join(', ')}</h6>
                                    </div>
                                    <div class="d-flex gap-1 mb-1">
                                        <span class="material-icons font-size-XL color_8">calendar_month</span>
                                        <h6 class="font-size-M color_8">${movie.release_date}</h6>
                                    </div>
                                    <div class="movie-rating d-flex gap-1 mb-1">
                                        <span class="material-icons color_8">stars</span>
                                        <h6 class="font-size-L color_5">${movie.user_rating}</h6>
                                    </div>
                                    <div class="text-center">
                                        <a data-movie-id="${movie.id}" data-movie-cover="${imageUrl}" class="material-icons color_2 movie_click">open_in_new</a>
                                    </div>
                                </div>
                            `;
                        } else {
                            movieHtml = `
                                <div class="movie" data-movie-id="${movie.id}" data-category="${movie.category}">
                                    <div class="movie-picture mb-1 default-image-background">
                                        Image non disponible
                                    </div>
                                    <div class="movie-title">
                                        <h6>${movie.title}</h6>
                                    </div>
                                    <hr>
                                    <div class="d-flex gap-1 mb-1">
                                        <span class="material-icons font-size-XL color_8">category</span>
                                        <h6 class="font-size-M color_8">${movie.genres.join(', ')}</h6>
                                    </div>
                                    <div class="d-flex gap-1 mb-1">
                                        <span class="material-icons font-size-XL color_8">calendar_month</span>
                                        <h6 class="font-size-M color_8">${movie.release_date}</h6>
                                    </div>
                                    <div class="movie-rating d-flex gap-1 mb-1">
                                        <span class="material-icons color_8">stars</span>
                                        <h6 class="font-size-L color_5">${movie.user_rating}</h6>
                                    </div>
                                    <div class="text-center">
                                        <a data-movie-id="${movie.id}" class="material-icons color_2 movie_click">open_in_new</a>
                                    </div>
                                </div>
                            `;
                        }

                        // Ajout du code HTML du film au conteneur de résultats de recherche
                        searchResults.append(movieHtml);
                    });

                } else {
                    showToastMessage(response.message, "text-danger");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Statut de l'erreur : ", textStatus);
                console.log("Texte de l'erreur : ", errorThrown);
                console.log("Réponse du serveur : ", jqXHR.responseText);
                console.log("Code d'état : ", jqXHR.status);

                // Affiche un message d'erreur à l'utilisateur
                showToastMessage("Une erreur est survenue : " + textStatus + " - " + errorThrown, "text-danger");
            },
            complete: function () {
                $(this).find('.spinner-border').addClass('d-none');
                $("#btn-submit-search").removeClass("button-clicked");
                $("#btn-submit-search").prop('disabled', false);
                // Une fois la requête terminée, masquer le spinner, réactiver le bouton et rétablir le texte du bouton
                $('#btn-submit-search').find('.spinner-border').addClass('d-none');
                $('#btn-submit-search').prop('disabled', false);
            }
        });
    });

    /*== Fast Search ==*/
        $('#recent-release').click(function() {
            sendAjaxRequestFastSearch(1);
        });

        $('#bests-notations').click(function() {
            sendAjaxRequestFastSearch(2);
        });

        $('#fr-movies').click(function() {
            sendAjaxRequestFastSearch(3);
        });

        function sendAjaxRequestFastSearch(operationId) {
            console.log(operationId);
            // Sélection du conteneur des résultats de recherche
            let searchResults = $("#searchResults");
            // Efface le contenu préalable du conteneur
            searchResults.empty();
            searchResults.text(operationId);
        }
    /*== END/Fast Search ==*/

    // Gestionnaire d'évenement qui sert à envoyer la requête pour afficher les détails d'un film
    $(document).on('click', '.movie_click', function() {
        var $link = $(this);
        var originalContent = $link.html();
        $link.html('<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Chargement...</span></div>');

        var movieId = $(this).data('movie-id');
        // Préparation de l'URL et des paramètres pour la requête AJAX
        var apiUrl = '/api/themoviedb/get/movie';
        var data = { movieId: movieId };

        // Requête AJAX
        $.ajax({
            url: apiUrl,
            method: 'GET',
            data: data,
            success: function(response) {
                if(response.status == "200") {
                    showToastMessage(response.message, "text-success");

                    // Je reçois un tableau associatif ['id':'name'], j'extrait simplement les noms des genres.
                    var genres = response.data['genres'];
                    var genreNames = genres.map(function(genre) {
                        return genre.name;
                    });
                    
                    // Créeation d'un objet de données à envoyer en POST
                    var postData = {
                        movieName: response.data['title'],
                        movieCategory: genreNames,
                        movieRelease: response.data['release_date'],
                        movieNotation: response.data['user_rating'],
                        movieSynopsis: response.data['synopsis'],
                        runtime: response.data['runtime'],
                        movieCover: response.data['cover_photo'],
                        backgroundImage: response.data['background_image']
                    };

                    // Création d'un formulaire caché pour envoyer les données en POST
                    var form = $('<form></form>');
                    form.attr('method', 'POST');
                    form.attr('action', '/show-movie-themoviedb/details'); // L'URL de votre route Flask
                    for (var key in postData) {
                        var input = $('<input></input>');
                        input.attr('type', 'hidden');
                        input.attr('name', key);
                        input.attr('value', postData[key]);
                        form.append(input);
                    }
                    form.appendTo('body').submit();
                }else if(response.status == "404") {
                    showToastMessage(response.error, "text-danger");
                }
                
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Erreur AJAX :', textStatus, errorThrown);
            },
            complete: function() {
                $link.html(originalContent);
            }
        });
    });
});
