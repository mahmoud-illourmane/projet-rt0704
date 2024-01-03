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

        /*
        * Cette méthode envoie les données au serveur pour l'ajout d'un film
        */
        function submitFormAddMovie() {
            // Sélection du formulaire avec jQuery
            var $form = $("#formAddMovie");
        
            // Vérifie si le formulaire est valide
            if (!$form[0].checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Création de l'objet FormData
                var formData = new FormData($form[0]);
                var directorInput = formData.get('director');
                if (!directorInput) formData.set('director', 'Inconnue'); // Remplace par "Inconnue"
        
                // Requête Ajax avec jQuery
                $.ajax({
                    url: '/add-movie',
                    type: 'POST',
                    data: formData,
                    processData: false, // L'objet FormData gère automatiquement ces informations.
                    contentType: false, // L'objet FormData gère automatiquement ces informations.
                    success: function (response) {
                        if (response.status === "200") {
                            showToastMessage(response.message, "text-success");
        
                            $form[0].reset(); // Réinitialiser le formulaire pour effacer son contenu
                            $('.synopsis').val(''); // Réinitialiser le champ .synopsis à vide
        
                            updateCharCount(); // Mettre à jour le compteur de caractères restants
                            loadMoviesIndex(); // Rappel de la méthode pour réafficher les films avec le nouveau
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("Statut de l'erreur : ", textStatus);
                        console.log("Texte de l'erreur : ", errorThrown);
                        console.log("Réponse du serveur : ", jqXHR.responseText);
                        console.log("Code d'état : ", jqXHR.status);
                        showToastMessage("Une erreur est survenue : " + textStatus + " - " + errorThrown, "text-danger");
                    }
                });
            }
        
            // Ajoute la classe was-validated pour déclencher les styles de validation
            $form.addClass('was-validated');
        }
        
        // Exportation de la fonction en global
        window.submitFormAddMovie = submitFormAddMovie; 

        // Attache l'événement de soumission du formulaire
        $('#formAddMovie').on('submit', function(event) {
            submitFormAddMovie(event); // Passer 'event' à la fonction
            return false;
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
                url: '/api/get-movies/gestions',     // Route coté front-end
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    moviesData = data.movies;        // Stockage des films dans le tableau
                    displayMoviesForFullScreen();   
                    displayMoviesForSmartphone();
                    nbTotalMovie.text('Nombre total de films : ' + data.nb_movies);
                },
                error: function(error) {
                    showToastMessage(error, "text-danger");
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
                        else if(response.status == "303") {
                            showToastMessage(response.error, "text-danger");
                        }
                        else if(response.status == "404") {
                            showToastMessage(response.error, "text-danger");
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("Statut de l'erreur : ", textStatus);
                        console.log("Texte de l'erreur : ", errorThrown);
                        console.log("Réponse du serveur : ", jqXHR.responseText);
                        console.log("Code d'état : ", jqXHR.status);
                        showToastMessage("Une erreur est survenue : " + textStatus + " - " + errorThrown, "text-danger");
                    }
                });
            }
        });
    /*== END/Modal gestionsMovie ==*/
});