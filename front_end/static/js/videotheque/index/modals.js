/**
 |
 |  This file contains all JS code for the manipulation of the content of the modals in the application on the index page.
 |  AUTHOR: MAHMOUD ILLOURMANE
 |  DATE: 12-23-23 US DATE
 | 
*/

$(document).on("DOMContentLoaded", function() {

    /*== Modal d'ajout d'un film ==*/

        /*== Rating movie ==*/

            /**
             * Ce gestionnaire d'événement permet d'obtenir 
             * le nombre d'étoiles données à un film
             */
            $('.star').click(function() {
                var index = $(this).index();
                $('.rating-input').val(index + 1);
                $('.star').removeClass('rated');
                for (var i = 0; i <= index; i++) {
                    $('.star:eq(' + i + ')').addClass('rated');
                }
            });
        /*== END/Rating movie ==*/
        
        /*== Counter synopsis ==*/
            var maxLength = 255;

            // Fonction pour mettre à jour le compte des caractères restants
            function updateCharCount() {
                var text = $('.synopsis').val();
                var remaining = maxLength - text.length;
                $('#charCount').text(remaining + ' caractères restants');
            }

            // Appel au gestionnaire d'événement lorsque des changements sont détectés dans le textarea
            $('.synopsis').on('input', function() {
                updateCharCount();
            });

            // Appel initial de la fonction pour afficher la limite par défaut
            updateCharCount();
        /*== END/Counter synopsis ==*/

        /**
         * Cette fonction est appelée lorsque le formulaire avec l'ID "formAddMovie" est soumis.
         * Elle vérifie la validité du formulaire, prépare les données, et envoie la demande.
         */
        function submitFormAddMovie() {
            var $form = $("#formAddMovie");
        
            if (validateForm($form)) {
                var formData = new FormData($form[0]);
                setDefaultDirector(formData);
                sendAddMovieRequest(formData, $form);
            }
        
            $form.addClass('was-validated');
        }
        
        /**
         * Cette fonction vérifie si le formulaire est valide.
         * Si le formulaire n'est pas valide, elle empêche la soumission.
         * @param {jQuery} $form - Le formulaire jQuery à valider.
         * @returns {boolean} - True si le formulaire est valide, sinon False.
         */
        function validateForm($form) {
            if (!$form[0].checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                return false;
            }
            return true;
        }
        
        /**
         * Cette fonction définit le directeur par défaut à "Inconnue" si le champ est vide.
         * @param {FormData} formData - Les données du formulaire.
         */
        function setDefaultDirector(formData) {
            var directorInput = formData.get('director');
            if (!directorInput) formData.set('director', 'Inconnue');
        }

        /**
         * Cette fonction envoie une requête AJAX POST pour ajouter un film.
         * @param {FormData} formData - Les données du formulaire à envoyer.
         * @param {jQuery} $form - Le formulaire jQuery associé.
         */
        function sendAddMovieRequest(formData, $form) {
            $.ajax({
                url: '/add-movie',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                beforeSend: function() {
                    disableSubmitButton(true);
                },
                success: function (response) {
                    handleSuccess(response, $form);
                },
                error: function(jqXHR) {
                    handleError(jqXHR);
                },
                complete: function() {
                    disableSubmitButton(false);
                }
            });
        }
        
        /**
         * Cette fonction désactive ou active le bouton de soumission.
         * @param {boolean} disable - True pour désactiver le bouton, False pour l'activer.
         */
        function disableSubmitButton(disable) {
            $('#submitButton').prop('disabled', disable);
        }

        /**
         * Cette fonction gère le succès de la requête AJAX.
         * Elle affiche un message toast, réinitialise le formulaire, efface le champ de synopsis,
         * met à jour un compteur de caractères et charge les films.
         * @param {object} response - La réponse de la requête AJAX.
         * @param {jQuery} $form - Le formulaire jQuery associé.
         */
        function handleSuccess(response, $form) {
            if (response.status === "200") {
                showToastMessage(response.message, "text-success");
                $form[0].reset();
                $('.synopsis').val('');
                updateCharCount();
                loadMoviesIndex();
            }
        }

        /**
         * Cette fonction gère les erreurs de la requête AJAX.
         * Elle affiche un message d'erreur en fonction de la réponse du serveur et du code d'erreur.
         * @param {object} jqXHR - L'objet représentant la réponse de la requête AJAX.
         */
        function handleError(jqXHR) {
            console.log("[modals.js] Réponse du serveur : ", jqXHR.responseText);
            let responseJson = JSON.parse(jqXHR.responseText);
            let errorMessage = jqXHR.status === 500 ? "Erreur interne du serveur : " : "Erreur : ";
            showToastMessage(errorMessage + responseJson.error, "text-danger");
        }
        
        // Exportation de la fonction en global
        window.submitFormAddMovie = submitFormAddMovie; 

        /**
         * Attache l'événement de soumission du formulaire avec l'ID "formAddMovie".
         * Lorsque le formulaire est soumis, cette fonction appelle la fonction `submitFormAddMovie`
         * en passant l'objet d'événement `event` en tant qu'argument, puis retourne `false`
         * pour empêcher la soumission normale du formulaire.
         * @param {Event} event - L'objet d'événement associé à la soumission du formulaire.
         */
        $('#formAddMovie').on('submit', function(event) {
            submitFormAddMovie(event); // Appel de la fonction 'submitFormAddMovie' en passant 'event'
            return false; // Empêche la soumission normale du formulaire
        });

    /*== END/Modal d'ajout d'un film ==*/

    /*== Modal gestionsMovie ==*/
        let nbTotalMovie = $('#nbTotalMovies'); // Le nombre de films dans le modal gestions des films
        let moviesData = [];                    // Tableau pour stocker les données des films

        // Attache l'événement de clic pour ouvrir le modal et charger les films
        $('[data-bs-target="#modalGestionsMovies"]').click(function() {
            loadMovies();
        });

        // Gestionnaire d'événement pour le changement de catégorie
        $('.form-select').on('change', function() {
            let selectedCategory = $(this).val();
            let searchTerm = $('.operation-search input').val().toLowerCase();
            displayMoviesForFullScreen(selectedCategory, searchTerm);
            displayMoviesForSmartphone(selectedCategory, searchTerm);
        });    

        // Gestionnaire d'événement pour la recherche de films
        $('.operation-search input').on('input', function() {
            let searchTerm = $(this).val().toLowerCase();
            let selectedCategory = $('.form-select').val();
            displayMoviesForFullScreen(selectedCategory, searchTerm);   // La fonction qui affiche tous les films sur un grand écran
            displayMoviesForSmartphone(selectedCategory, searchTerm);   // La fonction qui affiche tous les films sur un petit écran
        });

        /**
         * Cette fonction permet de faire un appel Ajax au serveur Flask back-end pour 
         * récupérer tous les films de l'utilisateur.
         * Ell est utilisé pour afficher la listes des films du modal "Gestions des films".
         */
        function loadMovies() {
            $.ajax({
                url: '/api/get-movies/gestions',  
                method: 'GET',
                dataType: 'json',
                success: function(response) {
                    if(response.status == "200") {
                        moviesData = response.movies;        // Stockage des films dans le tableau
                        displayMoviesForFullScreen();   
                        displayMoviesForSmartphone();
                        nbTotalMovie.text('Nombre total de films : ' + response.nb_movies);
                    }else {
                        showToastMessage("Une erreur s'est produite pendant le chargement des films.", "text-danger");
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log("[modals.js] Statut de l'erreur : ", textStatus);
                    console.log("[modals.js] Texte de l'erreur : ", errorThrown);
                    console.log("[modals.js] Réponse du serveur : ", jqXHR.responseText);
                    console.log("[modals.js] Code d'état : ", jqXHR.status);
                
                    // Afficher le message d'erreur renvoyé par Flask
                    let responseJson = JSON.parse(jqXHR.responseText);
                    
                    if (jqXHR.status === 500) {
                        let errorMessage = "Erreur interne du serveur : " + responseJson.error;
                        showToastMessage(errorMessage, "text-danger");
                    } else {
                        let errorMessage = "Erreur : " + responseJson.error;
                        showToastMessage(errorMessage, "text-danger");
                    }
                }
            });
        }
        // Exporte la fonction globalement pour être utilisé dans d'autre fichiers js (pas recommandé, mais plus simple)
        window.loadMovies = loadMovies;

        /**
         * Fonction pour afficher les films du modal "gestions des films" sur les ordinateurs de bureau
         * 
         * @param {string} category 
         * @param {string} searchTerm 
         */
        function displayMoviesForFullScreen(category = null, searchTerm = '') {
            let tableBody = $('#movieTableBody');
            tableBody.empty(); // Vider le tableau

            let filteredMovies = moviesData.filter(movie => {
                let matchesSearch = searchTerm === '' || movie.movie_name.toLowerCase().includes(searchTerm) || movie.director.toLowerCase().includes(searchTerm) || movie.category.toLowerCase().includes(searchTerm) || movie.year_of_creation.toLowerCase().includes(searchTerm);
                return category === null ? matchesSearch : (matchesSearch && (category === 'Tous' || movie.category === category));
            });

            if (filteredMovies.length === 0) {
                tableBody.append('<tr class="text-center"><td colspan="7"><strong class="color_7">AUCUN FILM</strong></td></tr>');
            } else {
                $.each(filteredMovies, function(index, movie) {
                    let row = `<tr class="text-center">
                        <th scope="row">${movie.id}</th>
                        <td>${movie.movie_name}</td>
                        <td>${movie.year_of_creation}</td>
                        <td>${movie.director}</td>
                        <td>${movie.category}</td>
                        <td>${getRatingHTML(movie.notation)}</td>
                        <td>
                            <a id="submitConfirmDeleteMovie${movie.id}" data-movie-id="${movie.id}" class="material-icons color_7">delete</a>
                        </td>
                    </tr>`;
                    tableBody.append(row);
                });
            }
        }

        /**
         * Fonction pour afficher les films sur le modal "gestions des films" sur les smartphones
         * elle affiche un tableau adapté au petit écran
         * @param {string} category 
         * @param {string} searchTerm 
         */
        function displayMoviesForSmartphone(category = null, searchTerm = '') {
            let tableBody = $('#movieTableBodySmartphone');
            tableBody.empty(); // Vide le tableau

            let filteredMovies = moviesData.filter(movie => {
                // Les termes de recherche autorisés
                let matchesSearch = searchTerm === '' || movie.movie_name.toLowerCase().includes(searchTerm) || movie.director.toLowerCase().includes(searchTerm) || movie.category.toLowerCase().includes(searchTerm) || movie.year_of_creation.toLowerCase().includes(searchTerm);
                return category === null ? matchesSearch : (matchesSearch && (category === 'Tous' || movie.category === category));
            });

            if (filteredMovies.length === 0) {
                tableBody.append('<tr class="text-center color_7"><td colspan="3"><strong class="color_7">AUCUN FILM</strong></td></tr>');
            } else {
                $.each(filteredMovies, function(index, movie) {
                    let row = `<tr>
                        <th scope="row">${movie.id}</th>
                        <td>
                            Titre : ${movie.movie_name} <br>
                            Année de sortie : ${movie.year_of_creation} <br>
                            Réalisateur : ${movie.director} <br>
                            Catégorie : ${movie.category} <br>
                            Note : ${getRatingHTML(movie.notation)} <br>
                        </td>
                        <th class="text-center">
                            <a id="submitConfirmDeleteMovie${movie.id}" data-movie-id="${movie.id}" class="material-icons color_7">delete</a>
                        </th>
                    </tr>`;
                    tableBody.append(row);
                });
            }
        }

        /**
         * Fonction pour détecter la largeur de l'écran et masquer la table inappropriée
         */
        function displayTableBasedOnScreenSize() {
            const screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

            const desktopTable = document.getElementById('desktopTable');
            const smartphoneTable = document.getElementById('smartphoneTable');

            if (screenWidth <= 768) { 
                desktopTable.style.display = 'none';
                smartphoneTable.style.display = 'table';
                displayMoviesForSmartphone();
            } else {
                desktopTable.style.display = 'table';
                smartphoneTable.style.display = 'none';
                displayMoviesForFullScreen();
            }
        }

        // Affiche le tableau adéquat
        displayTableBasedOnScreenSize();

        // Attache la fonction qui permet d'afficher le tableau responsive approprié aux événements de chargement et de redimensionnement de la fenêtre
        window.addEventListener('load', displayTableBasedOnScreenSize);
        window.addEventListener('resize', displayTableBasedOnScreenSize);

        /**
         * Cette méthode génère le code HTML de la notation d'un film
         * 
         * @param {int} rating 
         * @return html
         */
        function getRatingHTML(rating) {
            let html = '<div class="movie-rating">';
            for (let i = 0; i < 5; i++) {
                if (i < rating) {
                    html += '<i class="material-icons star-gold">star</i>';
                } else {
                    html += '<i class="material-icons star-silver">star</i>';
                }
            }
            html += '</div>';
            return html;
        }

        /**
         * Au clic sur le bouton de suppression d'un film, une requête Ajax est envoyée au serveur backend
         * pour demander la suppression du film choisi grâce à son ID.
         */
        $(document).on('click', 'a[id^="submitConfirmDeleteMovie"]', function() {
            var movieId = $(this).data('movie-id');
        
            // Affiche un message de confirmation en JavaScript avant de procéder à la suppression
            if(confirm("Êtes-vous sûr de vouloir supprimer ce film ?")) {
                $.ajax({
                    url: '/delete-movie',
                    method: 'DELETE', 
                    contentType: 'application/json', 
                    data: JSON.stringify({ movieId: movieId }), // Convertie les données en chaîne JSON
                    success: function(response) {
                        if(response.status == "200") {
                            showToastMessage(response.message, "text-success");
                            loadMovies();
                            loadMoviesIndex();
                        }
                        else {
                            showToastMessage(response.error, "text-danger");
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("Statut de l'erreur : ", textStatus);
                        console.log("Texte de l'erreur : ", errorThrown);
                        console.log("Réponse du serveur : ", jqXHR.responseText);
                        console.log("Code d'état : ", jqXHR.status);
                    
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
        });
    /*== END/Modal gestionsMovie ==*/
});