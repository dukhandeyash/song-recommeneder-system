$(document).ready(function() {
    // Global variables to store selected tracks
    let compatibilityTracks = [];
    let diversityTracks = [];
    
    // Predefined Playlists with expanded track lists
    const predefinedPlaylists = {
        // Mood-Based Playlists
        moodPlaylists: {
            'Happy': [
                { name: 'Can\'t Stop the Feeling!', artist: 'Justin Timberlake', features: { danceability: 0.8, energy: 0.9, valence: 0.96 } },
                { name: 'Walking on Sunshine', artist: 'Katrina and The Waves', features: { danceability: 0.7, energy: 0.85, valence: 0.95 } },
                { name: 'Don\'t Stop Me Now', artist: 'Queen', features: { danceability: 0.75, energy: 0.95, valence: 0.93 } },
                { name: 'Happy', artist: 'Pharrell Williams', features: { danceability: 0.82, energy: 0.87, valence: 0.94 } },
                { name: 'I Wanna Dance with Somebody', artist: 'Whitney Houston', features: { danceability: 0.79, energy: 0.88, valence: 0.92 } },
                { name: 'Shake It Off', artist: 'Taylor Swift', features: { danceability: 0.76, energy: 0.86, valence: 0.91 } },
                { name: 'Good Vibrations', artist: 'The Beach Boys', features: { danceability: 0.73, energy: 0.84, valence: 0.90 } },
                { name: 'Uptown Funk', artist: 'Mark Ronson ft. Bruno Mars', features: { danceability: 0.81, energy: 0.89, valence: 0.95 } },
                { name: 'Dancing Queen', artist: 'ABBA', features: { danceability: 0.77, energy: 0.83, valence: 0.92 } },
                { name: 'I Gotta Feeling', artist: 'Black Eyed Peas', features: { danceability: 0.80, energy: 0.91, valence: 0.93 } },
                { name: 'Shut Up and Dance', artist: 'Walk the Moon', features: { danceability: 0.75, energy: 0.87, valence: 0.90 } }
            ],
            'Sad': [
                { name: 'Someone Like You', artist: 'Adele', features: { danceability: 0.3, energy: 0.2, valence: 0.1 } },
                { name: 'Hurt', artist: 'Johnny Cash', features: { danceability: 0.2, energy: 0.15, valence: 0.05 } },
                { name: 'Fix You', artist: 'Coldplay', features: { danceability: 0.4, energy: 0.3, valence: 0.2 } },
                { name: 'All By Myself', artist: 'Eric Carmen', features: { danceability: 0.25, energy: 0.18, valence: 0.08 } },
                { name: 'Everybody Hurts', artist: 'R.E.M.', features: { danceability: 0.35, energy: 0.25, valence: 0.15 } },
                { name: 'The Sound of Silence', artist: 'Simon & Garfunkel', features: { danceability: 0.2, energy: 0.1, valence: 0.07 } },
                { name: 'Mad World', artist: 'Gary Jules', features: { danceability: 0.3, energy: 0.2, valence: 0.12 } },
                { name: 'Skinny Love', artist: 'Bon Iver', features: { danceability: 0.4, energy: 0.25, valence: 0.18 } },
                { name: 'Say Something', artist: 'A Great Big World', features: { danceability: 0.35, energy: 0.22, valence: 0.13 } },
                { name: 'Hallelujah', artist: 'Jeff Buckley', features: { danceability: 0.3, energy: 0.15, valence: 0.09 } },
                { name: 'Tears in Heaven', artist: 'Eric Clapton', features: { danceability: 0.25, energy: 0.2, valence: 0.11 } }
            ],
            'Energetic': [
                { name: 'Thunderstruck', artist: 'AC/DC', features: { danceability: 0.6, energy: 0.95, valence: 0.5 } },
                { name: 'Eye of the Tiger', artist: 'Survivor', features: { danceability: 0.7, energy: 0.9, valence: 0.6 } },
                { name: 'Stronger', artist: 'Kanye West', features: { danceability: 0.8, energy: 0.85, valence: 0.7 } },
                { name: 'Believer', artist: 'Imagine Dragons', features: { danceability: 0.75, energy: 0.92, valence: 0.65 } },
                { name: 'Till I Collapse', artist: 'Eminem', features: { danceability: 0.7, energy: 0.93, valence: 0.55 } },
                { name: 'Remember the Name', artist: 'Fort Minor', features: { danceability: 0.65, energy: 0.91, valence: 0.5 } },
                { name: 'Lose Yourself', artist: 'Eminem', features: { danceability: 0.8, energy: 0.94, valence: 0.6 } },
                { name: 'Can\'t Hold Us', artist: 'Macklemore & Ryan Lewis', features: { danceability: 0.75, energy: 0.90, valence: 0.7 } },
                { name: 'Power', artist: 'Kanye West', features: { danceability: 0.7, energy: 0.88, valence: 0.65 } },
                { name: 'Shipping Up to Boston', artist: 'Dropkick Murphys', features: { danceability: 0.65, energy: 0.95, valence: 0.55 } },
                { name: 'All I Do Is Win', artist: 'DJ Khaled', features: { danceability: 0.8, energy: 0.89, valence: 0.75 } }
            ]
        },
        
        // Activity-Based Playlists
        activityPlaylists: {
            'Workout': [
                { name: 'Lose Yourself', artist: 'Eminem', features: { danceability: 0.8, energy: 0.95, tempo: 170 } },
                { name: 'Til I Collapse', artist: 'Eminem', features: { danceability: 0.75, energy: 0.9, tempo: 165 } },
                { name: 'Remember the Name', artist: 'Fort Minor', features: { danceability: 0.7, energy: 0.85, tempo: 160 } },
                { name: 'Thunderstruck', artist: 'AC/DC', features: { danceability: 0.65, energy: 0.93, tempo: 175 } },
                { name: 'Eye of the Tiger', artist: 'Survivor', features: { danceability: 0.7, energy: 0.92, tempo: 168 } },
                { name: 'Believer', artist: 'Imagine Dragons', features: { danceability: 0.75, energy: 0.94, tempo: 172 } },
                { name: 'Power', artist: 'Kanye West', features: { danceability: 0.8, energy: 0.91, tempo: 162 } },
                { name: 'Can\'t Hold Us', artist: 'Macklemore & Ryan Lewis', features: { danceability: 0.85, energy: 0.93, tempo: 166 } },
                { name: 'All I Do Is Win', artist: 'DJ Khaled', features: { danceability: 0.8, energy: 0.92, tempo: 169 } },
                { name: 'Shipping Up to Boston', artist: 'Dropkick Murphys', features: { danceability: 0.7, energy: 0.95, tempo: 173 } },
                { name: 'Stronger', artist: 'Kanye West', features: { danceability: 0.8, energy: 0.90, tempo: 164 } }
            ],
            'Study': [
                { name: 'Intro', artist: 'The xx', features: { instrumentalness: 0.9, energy: 0.2, tempo: 90 } },
                { name: 'Nuvole Bianche', artist: 'Ludovico Einaudi', features: { instrumentalness: 0.8, energy: 0.15, tempo: 80 } },
                { name: 'River Flows in You', artist: 'Yiruma', features: { instrumentalness: 0.7, energy: 0.1, tempo: 70 } },
                { name: 'Gymnopédie No.1', artist: 'Erik Satie', features: { instrumentalness: 0.85, energy: 0.05, tempo: 65 } },
                { name: 'Clair de Lune', artist: 'Claude Debussy', features: { instrumentalness: 0.9, energy: 0.08, tempo: 75 } },
                { name: 'Weightless', artist: 'Marconi Union', features: { instrumentalness: 0.95, energy: 0.12, tempo: 60 } },
                { name: 'Ambient 1/Music for Airports', artist: 'Brian Eno', features: { instrumentalness: 0.92, energy: 0.15, tempo: 85 } },
                { name: 'The Theory of Everything', artist: 'Jóhann Jóhannsson', features: { instrumentalness: 0.88, energy: 0.18, tempo: 95 } },
                { name: 'Comptine d\'un autre été', artist: 'Yann Tiersen', features: { instrumentalness: 0.86, energy: 0.1, tempo: 72 } },
                { name: 'Divenire', artist: 'Ludovico Einaudi', features: { instrumentalness: 0.82, energy: 0.13, tempo: 88 } },
                { name: 'Time', artist: 'Hans Zimmer', features: { instrumentalness: 0.89, energy: 0.16, tempo: 82 } }
            ],
            'Relaxation': [
                { name: 'Weightless', artist: 'Marconi Union', features: { acousticness: 0.9, energy: 0.1, tempo: 60 } },
                { name: 'Gymnopédie No.1', artist: 'Erik Satie', features: { acousticness: 0.8, energy: 0.05, tempo: 50 } },
                { name: 'Clair de Lune', artist: 'Claude Debussy', features: { acousticness: 0.85, energy: 0.1, tempo: 55 } },
                { name: 'River Flows in You', artist: 'Yiruma', features: { acousticness: 0.75, energy: 0.08, tempo: 65 } },
                { name: 'Intro', artist: 'The xx', features: { acousticness: 0.9, energy: 0.12, tempo: 70 } },
                { name: 'Ambient 1/Music for Airports', artist: 'Brian Eno', features: { acousticness: 0.95, energy: 0.15, tempo: 58 } },
                { name: 'Comptine d\'un autre été', artist: 'Yann Tiersen', features: { acousticness: 0.88, energy: 0.07, tempo: 62 } },
                { name: 'Divenire', artist: 'Ludovico Einaudi', features: { acousticness: 0.82, energy: 0.09, tempo: 68 } },
                { name: 'The Theory of Everything', artist: 'Jóhann Jóhannsson', features: { acousticness: 0.86, energy: 0.11, tempo: 57 } },
                { name: 'Time', artist: 'Hans Zimmer', features: { acousticness: 0.89, energy: 0.13, tempo: 63 } },
                { name: 'Nuvole Bianche', artist: 'Ludovico Einaudi', features: { acousticness: 0.84, energy: 0.06, tempo: 66 } }
            ],
            'Party': [
                { name: 'I Gotta Feeling', artist: 'Black Eyed Peas', features: { danceability: 0.8, energy: 0.95, valence: 0.9 } },
                { name: 'Uptown Funk', artist: 'Mark Ronson ft. Bruno Mars', features: { danceability: 0.82, energy: 0.92, valence: 0.85 } },
                { name: 'Can\'t Stop the Feeling!', artist: 'Justin Timberlake', features: { danceability: 0.79, energy: 0.93, valence: 0.88 } },
                { name: 'Shake It Off', artist: 'Taylor Swift', features: { danceability: 0.75, energy: 0.91, valence: 0.86 } },
                { name: 'Don\'t Stop the Music', artist: 'Rihanna', features: { danceability: 0.77, energy: 0.94, valence: 0.87 } },
                { name: 'Hey Ya!', artist: 'OutKast', features: { danceability: 0.76, energy: 0.90, valence: 0.92 } },
                { name: 'SexyBack', artist: 'Justin Timberlake', features: { danceability: 0.8, energy: 0.89, valence: 0.83 } },
                { name: 'Get Lucky', artist: 'Daft Punk', features: { danceability: 0.78, energy: 0.92, valence: 0.89 } },
                { name: 'Dancing Queen', artist: 'ABBA', features: { danceability: 0.75, energy: 0.93, valence: 0.91 } },
                { name: 'Shut Up and Dance', artist: 'Walk the Moon', features: { danceability: 0.79, energy: 0.90, valence: 0.85 } },
                { name: 'Happy', artist: 'Pharrell Williams', features: { danceability: 0.77, energy: 0.91, valence: 0.87 } }
            ]
        },
        
        // Time of Day Playlists
        timeOfDayPlaylists: {
            'Morning': [
                { name: 'Here Comes the Sun', artist: 'The Beatles', features: { danceability: 0.6, energy: 0.5, valence: 0.9 } },
                { name: 'Walking on Sunshine', artist: 'Katrina and The Waves', features: { danceability: 0.7, energy: 0.6, valence: 0.95 } },
                { name: 'Good Morning', artist: 'Kanye West', features: { danceability: 0.65, energy: 0.55, valence: 0.7 } },
                { name: 'Morning Has Broken', artist: 'Cat Stevens', features: { danceability: 0.5, energy: 0.4, valence: 0.85 } },
                { name: 'Lovely Day', artist: 'Bill Withers', features: { danceability: 0.6, energy: 0.5, valence: 0.88 } },
                { name: 'Beautiful Day', artist: 'U2', features: { danceability: 0.7, energy: 0.6, valence: 0.92 } },
                { name: 'Rise', artist: 'Katy Perry', features: { danceability: 0.65, energy: 0.55, valence: 0.8 } },
                { name: 'Sunrise', artist: 'Norah Jones', features: { danceability: 0.55, energy: 0.45, valence: 0.86 } },
                { name: 'Good Vibrations', artist: 'The Beach Boys', features: { danceability: 0.7, energy: 0.6, valence: 0.93 } },
                { name: 'Happy', artist: 'Pharrell Williams', features: { danceability: 0.75, energy: 0.65, valence: 0.95 } },
                { name: 'I Gotta Feeling', artist: 'Black Eyed Peas', features: { danceability: 0.8, energy: 0.7, valence: 0.91 } }
            ],
            'Afternoon': [
                { name: 'Uptown Funk', artist: 'Mark Ronson ft. Bruno Mars', features: { danceability: 0.8, energy: 0.75, valence: 0.9 } },
                { name: 'Can\'t Stop the Feeling!', artist: 'Justin Timberlake', features: { danceability: 0.75, energy: 0.7, valence: 0.88 } },
                { name: 'Shake It Off', artist: 'Taylor Swift', features: { danceability: 0.7, energy: 0.65, valence: 0.86 } },
                { name: 'Don\'t Stop Me Now', artist: 'Queen', features: { danceability: 0.75, energy: 0.8, valence: 0.92 } },
                { name: 'I Wanna Dance with Somebody', artist: 'Whitney Houston', features: { danceability: 0.8, energy: 0.75, valence: 0.89 } },
                { name: 'Dancing Queen', artist: 'ABBA', features: { danceability: 0.7, energy: 0.65, valence: 0.93 } },
                { name: 'Get Lucky', artist: 'Daft Punk', features: { danceability: 0.75, energy: 0.7, valence: 0.87 } },
                { name: 'SexyBack', artist: 'Justin Timberlake', features: { danceability: 0.8, energy: 0.75, valence: 0.85 } },
                { name: 'Hey Ya!', artist: 'OutKast', features: { danceability: 0.75, energy: 0.7, valence: 0.91 } },
                { name: 'Shut Up and Dance', artist: 'Walk the Moon', features: { danceability: 0.7, energy: 0.65, valence: 0.88 } },
                { name: 'Can\'t Hold Us', artist: 'Macklemore & Ryan Lewis', features: { danceability: 0.8, energy: 0.75, valence: 0.90 } }
            ],
            'Evening': [
                { name: 'Fly Me to the Moon', artist: 'Frank Sinatra', features: { danceability: 0.6, energy: 0.4, valence: 0.85 } },
                { name: 'The Way You Look Tonight', artist: 'Frank Sinatra', features: { danceability: 0.55, energy: 0.35, valence: 0.87 } },
                { name: 'Moonlight Serenade', artist: 'Glenn Miller', features: { danceability: 0.5, energy: 0.3, valence: 0.8 } },
                { name: 'Smooth', artist: 'Santana ft. Rob Thomas', features: { danceability: 0.65, energy: 0.45, valence: 0.86 } },
                { name: 'All of Me', artist: 'John Legend', features: { danceability: 0.6, energy: 0.4, valence: 0.89 } },
                { name: 'Can\'t Help Falling in Love', artist: 'Elvis Presley', features: { danceability: 0.55, energy: 0.35, valence: 0.91 } },
                { name: 'At Last', artist: 'Etta James', features: { danceability: 0.5, energy: 0.3, valence: 0.88 } },
                { name: 'Thinking Out Loud', artist: 'Ed Sheeran', features: { danceability: 0.65, energy: 0.4, valence: 0.87 } },
                { name: 'Just the Way You Are', artist: 'Bruno Mars', features: { danceability: 0.6, energy: 0.35, valence: 0.90 } },
                { name: 'Make You Feel My Love', artist: 'Adele', features: { danceability: 0.55, energy: 0.3, valence: 0.85 } },
                { name: 'Perfect', artist: 'Ed Sheeran', features: { danceability: 0.6, energy: 0.4, valence: 0.92 } }
            ]
        }
    };

    // Function to render playlists
    function renderPlaylists(playlists, playlistType) {
        console.log('Rendering Playlists - Debug Info:');
        console.log('Playlist Type:', playlistType);
        console.log('Playlists Object:', playlists);

        const container = $('#playlist-container');
        container.empty();

        // Detailed error checking
        if (!predefinedPlaylists) {
            console.error('predefinedPlaylists is UNDEFINED');
            container.html('<div class="alert alert-danger">No playlists found</div>');
            return;
        }

        if (!playlists) {
            console.error(`No playlists found for ${playlistType}`);
            console.error('Available playlist types:', Object.keys(predefinedPlaylists));
            container.html(`<div class="alert alert-danger">No playlists found for ${playlistType}</div>`);
            return;
        }

        // Create a container to hold all categories
        const playlistsHtml = $('<div class="playlist-categories"></div>');

        // Iterate through all categories in the playlist object
        Object.entries(playlists).forEach(([category, tracks]) => {
            console.log(`Rendering category: ${category}`);
            console.log(`Number of tracks in ${category}:`, tracks.length);

            const tableHtml = `
                <div class="playlist-category mb-4">
                    <h4 class="text-primary">${category}</h4>
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Track Name</th>
                                <th>Artist</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${tracks.map((track, index) => `
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${track.name}</td>
                                    <td>${track.artist}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
            
            playlistsHtml.append(tableHtml);
        });

        // Append the entire playlist categories to the container
        container.append(playlistsHtml);

        // Final check
        if (container.children().length === 0) {
            console.error('No playlist categories were rendered');
            container.html('<div class="alert alert-warning">No playlists could be rendered</div>');
        }
    }

    // Ensure playlists are rendered on page load and tab click
    function initializePlaylists() {
        console.log('Initializing Playlists');
        console.log('Available Playlist Types:', Object.keys(predefinedPlaylists));
        
        // Try to render Time of Day Playlists
        if (predefinedPlaylists.timeOfDayPlaylists) {
            renderPlaylists(predefinedPlaylists.timeOfDayPlaylists, 'Time of Day Playlists');
        } else {
            console.error('Time of Day Playlists not found');
            $('#playlist-container').html('<div class="alert alert-danger">Time of Day Playlists not found</div>');
        }
    }

    // Call initialization on document ready
    $(document).ready(initializePlaylists);

    // Tab click handlers
    $('.nav-tabs .nav-link').on('click', function(e) {
        e.preventDefault();
        const playlistType = $(this).attr('id').replace('-playlist-tab', '');
        
        switch(playlistType) {
            case 'mood':
                renderPlaylists(predefinedPlaylists.moodPlaylists, 'Mood Playlists');
                break;
            case 'activity':
                renderPlaylists(predefinedPlaylists.activityPlaylists, 'Activity Playlists');
                break;
            case 'time':
                renderPlaylists(predefinedPlaylists.timeOfDayPlaylists, 'Time of Day Playlists');
                break;
            default:
                console.error('Unknown playlist type:', playlistType);
                $('#playlist-container').html('<div class="alert alert-danger">Invalid playlist type</div>');
        }
    });

    // Search functionality
    $('#search-button').click(function() {
        const query = $('#search-input').val();
        if (query.trim() === '') return;
        
        searchTracks(query);
    });
    
    $('#search-input').keypress(function(e) {
        if (e.which === 13) {
            $('#search-button').click();
        }
    });
    
    function searchTracks(query) {
        // Clear previous results and show loading
        $('#search-results').html(`
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
                <p class="mt-2">Searching for "${query}"...</p>
            </div>
        `);
        
        $.ajax({
            url: '/search',
            type: 'GET',
            data: { query: query },
            timeout: 10000,  // 10-second timeout
            success: function(data) {
                // Ensure the data is an array and not null
                const tracks = Array.isArray(data) ? data : [];
                displaySearchResults(tracks);
            },
            error: function(xhr, status, error) {
                let errorMessage = 'Error searching for tracks.';
                
                // More detailed error handling
                if (status === 'timeout') {
                    errorMessage = 'Search timed out. Please try again.';
                } else if (xhr.status === 404) {
                    errorMessage = 'Search endpoint not found.';
                } else if (xhr.status === 500) {
                    errorMessage = 'Server error. Please try again later.';
                }
                
                $('#search-results').html(`
                    <div class="alert alert-danger">
                        ${errorMessage}
                        <br>
                        <small>Details: ${error}</small>
                    </div>
                `);
                console.error('Error searching for tracks:', error);
            }
        });
    }
    
    function displaySearchResults(tracks) {
        // Clear loading state
        if (tracks.length === 0) {
            $('#search-results').html('<div class="alert alert-info">No tracks found. Try a different search term.</div>');
            return;
        }
        
        let html = '<div class="row">';
        
        tracks.forEach(track => {
            const imageHtml = track.image ? 
                `<img src="${track.image}" class="card-img-top" alt="${track.name}" style="height: 180px; object-fit: cover;">` : 
                '<div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 180px;"><i class="fas fa-music fa-3x text-secondary"></i></div>';
            
            html += `
                <div class="col-md-4 mb-3">
                    <div class="card track-card track-search-item" 
                         data-track-id="${track.id}" 
                         data-track-name="${track.name}" 
                         data-track-artist="${track.artist}">
                        ${imageHtml}
                        <div class="card-body">
                            <h5 class="card-title">${track.name}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${track.artist}</h6>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        $('#search-results').html(html);
        
        // Add click event to open YouTube search for each track
        $('.track-search-item').on('click', function() {
            const trackName = $(this).data('track-name');
            const trackArtist = $(this).data('track-artist');
            
            // Construct YouTube search URL
            const searchQuery = encodeURIComponent(`${trackName} ${trackArtist}`);
            const youtubeSearchUrl = `https://www.youtube.com/results?search_query=${searchQuery}`;
            
            // Open in a new tab
            window.open(youtubeSearchUrl, '_blank');
        });
    }
    
    // Mood-based playlists
    $('.mood-btn').click(function() {
        $('.mood-btn').removeClass('active');
        $(this).addClass('active');
        
        const mood = $(this).data('mood');
        getMoodPlaylist(mood);
    });
    
    function getMoodPlaylist(mood) {
        $('#mood-playlist-results').html('<div class="text-center"><div class="spinner-border" role="status"></div><p>Generating playlist...</p></div>');
        
        $.ajax({
            url: '/mood_playlist',
            type: 'GET',
            data: { mood: mood },
            success: function(data) {
                displayPlaylist(data, '#mood-playlist-results');
            },
            error: function(error) {
                $('#mood-playlist-results').html('<div class="alert alert-danger">Error generating playlist. Please try again.</div>');
                console.error('Error generating mood playlist:', error);
            }
        });
    }
    
    // Activity-based playlists
    $('.activity-btn').click(function() {
        $('.activity-btn').removeClass('active');
        $(this).addClass('active');
        
        const activity = $(this).data('activity');
        getActivityPlaylist(activity);
    });
    
    function getActivityPlaylist(activity) {
        $('#activity-playlist-results').html('<div class="text-center"><div class="spinner-border" role="status"></div><p>Generating playlist...</p></div>');
        
        $.ajax({
            url: '/activity_playlist',
            type: 'GET',
            data: { activity: activity },
            success: function(data) {
                displayPlaylist(data, '#activity-playlist-results');
            },
            error: function(error) {
                $('#activity-playlist-results').html('<div class="alert alert-danger">Error generating playlist. Please try again.</div>');
                console.error('Error generating activity playlist:', error);
            }
        });
    }
    
    // Time-of-day playlists
    $('.time-btn').click(function() {
        $('.time-btn').removeClass('active');
        $(this).addClass('active');
        
        const time = $(this).data('time');
        getTimePlaylist(time);
    });
    
    function getTimePlaylist(time) {
        $('#time-playlist-results').html('<div class="text-center"><div class="spinner-border" role="status"></div><p>Generating playlist...</p></div>');
        
        $.ajax({
            url: '/time_playlist',
            type: 'GET',
            data: { time: time },
            success: function(data) {
                displayPlaylist(data, '#time-playlist-results');
            },
            error: function(error) {
                $('#time-playlist-results').html('<div class="alert alert-danger">Error generating playlist. Please try again.</div>');
                console.error('Error generating time playlist:', error);
            }
        });
    }
    
    function displayPlaylist(tracks, targetElement) {
        if (tracks.length === 0) {
            $(targetElement).html('<div class="alert alert-info">No tracks found for this selection.</div>');
            return;
        }
        
        let html = '<div class="playlist-container"><table class="table table-striped">';
        html += '<thead><tr><th>#</th><th>Track</th><th>Artist</th></tr></thead><tbody>';
        
        tracks.forEach((track, index) => {
            html += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${track.track_name}</td>
                    <td>${track.artist}</td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div>';
        $(targetElement).html(html);
    }
    
    // Compatibility checker
    $('#compatibility-search-btn').click(function() {
        const query = $('#compatibility-search').val();
        if (query.trim() === '') return;
        
        searchForCompatibility(query);
    });
    
    $('#compatibility-search').keypress(function(e) {
        if (e.which === 13) {
            $('#compatibility-search-btn').click();
        }
    });
    
    function searchForCompatibility(query) {
        $('#compatibility-search-results').html('<div class="text-center"><div class="spinner-border" role="status"></div><p>Searching...</p></div>');
        
        $.ajax({
            url: '/search',
            type: 'GET',
            data: { query: query, search_type: 'compatibility' },
            success: function(data) {
                displayCompatibilitySearchResults(data);
            },
            error: function(error) {
                $('#compatibility-search-results').html('<div class="alert alert-danger">Error searching for tracks. Please try again.</div>');
                console.error('Error searching for tracks:', error);
            }
        });
    }
    
    function displayCompatibilitySearchResults(tracks) {
        if (tracks.length === 0) {
            $('#compatibility-search-results').html('<div class="alert alert-info">No tracks found. Try a different search term.</div>');
            return;
        }
        
        let html = '<div class="row">';
        
        tracks.forEach(track => {
            const imageHtml = track.image ? 
                `<img src="${track.image}" class="card-img-top" alt="${track.name}" style="height: 120px; object-fit: cover;">` : 
                '<div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 120px;"><i class="fas fa-music fa-3x text-secondary"></i></div>';
            
            html += `
                <div class="col-md-4 mb-3">
                    <div class="card track-card" data-track-id="${track.id}" data-track-name="${track.name}" data-track-artist="${track.artist}">
                        ${imageHtml}
                        <div class="card-body">
                            <h5 class="card-title">${track.name}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${track.artist}</h6>
                            <button class="btn btn-sm btn-primary add-to-compatibility-btn">Add to List</button>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        $('#compatibility-search-results').html(html);
        
        // Add click event for add buttons
        $('.add-to-compatibility-btn').click(function() {
            const card = $(this).closest('.track-card');
            const trackId = card.data('track-id');
            const trackName = card.data('track-name');
            const trackArtist = card.data('track-artist');
            
            addToCompatibilityList(trackId, trackName, trackArtist);
        });
    }
    
    function addToCompatibilityList(trackId, trackName, trackArtist) {
        // Check if already in list
        if (compatibilityTracks.find(t => t.id === trackId)) {
            return;
        }
        
        compatibilityTracks.push({
            id: trackId,
            name: trackName,
            artist: trackArtist
        });
        
        updateCompatibilityList();
    }
    
    function updateCompatibilityList() {
        let html = '';
        
        compatibilityTracks.forEach((track, index) => {
            html += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    ${track.name} - ${track.artist}
                    <button class="btn btn-sm btn-danger remove-compatibility-btn" data-index="${index}">
                        <i class="fas fa-times"></i>
                    </button>
                </li>
            `;
        });
        
        $('#compatibility-selected-songs').html(html);
        
        // Enable/disable check button
        if (compatibilityTracks.length >= 2) {
            $('#check-compatibility-btn').prop('disabled', false);
        } else {
            $('#check-compatibility-btn').prop('disabled', true);
        }
        
        // Add remove button event
        $('.remove-compatibility-btn').click(function() {
            const index = $(this).data('index');
            compatibilityTracks.splice(index, 1);
            updateCompatibilityList();
        });
    }
    
    $('#check-compatibility-btn').click(function() {
        if (compatibilityTracks.length < 2) return;
        
        const trackIds = compatibilityTracks.map(t => t.id);
        
        $('#compatibility-results').show();
        $('#compatibility-progress').css('width', '0%');
        $('#compatibility-score').text('Calculating...');
        
        $.ajax({
            url: '/compatibility',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ track_ids: trackIds }),
            success: function(data) {
                displayCompatibilityScore(data.score);
            },
            error: function(error) {
                $('#compatibility-score').text('Error calculating compatibility score.');
                console.error('Error calculating compatibility:', error);
            }
        });
    });
    
    function displayCompatibilityScore(score) {
        $('#compatibility-progress').css('width', score + '%');
        
        let message = '';
        if (score >= 80) {
            message = 'Excellent compatibility! These songs go very well together.';
            $('#compatibility-progress').removeClass('bg-warning bg-danger').addClass('bg-success');
        } else if (score >= 60) {
            message = 'Good compatibility. These songs should work well together.';
            $('#compatibility-progress').removeClass('bg-success bg-danger').addClass('bg-info');
        } else if (score >= 40) {
            message = 'Moderate compatibility. Some contrast between these songs.';
            $('#compatibility-progress').removeClass('bg-success bg-danger').addClass('bg-warning');
        } else {
            message = 'Low compatibility. These songs have very different characteristics.';
            $('#compatibility-progress').removeClass('bg-success bg-warning').addClass('bg-danger');
        }
        
        $('#compatibility-score').text(`${score}% - ${message}`);
    }
    
    // Diversity Track Addition Functionality
    $('#add-track-diversity').on('click', function() {
        const trackId = $('#track-search-diversity').val();
        
        if (!trackId) {
            alert('Please select a track first.');
            return;
        }
        
        // Find the selected track's details
        const selectedTrack = searchResults.find(track => track.id === trackId);
        
        if (!selectedTrack) {
            alert('Track not found. Please search again.');
            return;
        }
        
        // Check if track is already added
        const existingTrack = $('#diversity-tracks .track-item').filter(function() {
            return $(this).data('track-id') === trackId;
        });
        
        if (existingTrack.length > 0) {
            alert('This track is already added to the diversity list.');
            return;
        }
        
        // Create track item
        const trackItem = `
            <div class="track-item list-group-item list-group-item-action d-flex justify-content-between align-items-center" 
                 data-track-id="${selectedTrack.id}">
                <div>
                    <img src="${selectedTrack.album.images[0]?.url || 'default-album.jpg'}" 
                         class="mr-2" style="width: 50px; height: 50px;">
                    <span class="track-name">${selectedTrack.name}</span>
                    <small class="text-muted ml-2">${selectedTrack.artists[0].name}</small>
                </div>
                <button class="btn btn-sm btn-danger remove-track-diversity">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        
        // Append track to diversity tracks list
        $('#diversity-tracks').append(trackItem);
        
        // Clear search input
        $('#track-search-diversity').val('');
    });

    // Remove Track from Diversity List
    $('#diversity-tracks').on('click', '.remove-track-diversity', function() {
        $(this).closest('.track-item').remove();
    });

    // Add local song search functionality
    function localSongSearch() {
        const query = $('#local-song-search-input').val().trim();
        
        if (query === '') {
            $('#local-song-search-results').html('<div class="alert alert-info">Please enter a song name.</div>');
            return;
        }
        
        $.ajax({
            url: '/local_song_search',
            method: 'GET',
            data: { query: query },
            success: function(data) {
                displayLocalSongSearchResults(data);
            },
            error: function(error) {
                $('#local-song-search-results').html('<div class="alert alert-danger">Error searching for local tracks. Please try again.</div>');
                console.error('Error searching for local tracks:', error);
            }
        });
    }

    function displayLocalSongSearchResults(tracks) {
        if (tracks.length === 0) {
            $('#local-song-search-results').html('<div class="alert alert-info">No tracks found. Try a different search term.</div>');
            return;
        }
        
        let html = '<div class="row">';
        
        tracks.forEach(track => {
            html += `
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${track.name}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${track.artist}</h6>
                            <p class="card-text">
                                <strong>Album:</strong> ${track.album}<br>
                                <strong>Mood:</strong> ${track.mood}<br>
                                <strong>Activity:</strong> ${track.activity}<br>
                                <strong>Time of Day:</strong> ${track.time_of_day}
                            </p>
                            <button class="btn btn-primary get-local-recommendations" 
                                    data-song-name="${track.name}">
                                Get Recommendations
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        
        // Add note about limited results
        if (tracks.length === 5) {
            html += `
                <div class="alert alert-info mt-3">
                    Showing top 5 results. Refine your search for more specific matches.
                </div>
            `;
        }
        
        $('#local-song-search-results').html(html);
        
        // Add click event for recommendation buttons
        $('.get-local-recommendations').on('click', function() {
            const songName = $(this).data('song-name');
            getLocalSongRecommendations(songName);
        });
    }

    function getLocalSongRecommendations(songName) {
        $.ajax({
            url: '/local_song_recommendations',
            method: 'GET',
            data: { song_name: songName },
            success: function(data) {
                displayLocalSongRecommendations(songName, data);
            },
            error: function(error) {
                $('#local-song-recommendations').html('<div class="alert alert-danger">Error getting recommendations. Please try again.</div>');
                console.error('Error getting local song recommendations:', error);
            }
        });
    }

    function displayLocalSongRecommendations(baseSong, recommendations) {
        if (recommendations.length === 0) {
            $('#local-song-recommendations').html('<div class="alert alert-info">No recommendations found.</div>');
            return;
        }
        
        let html = `<h4>Recommendations for "${baseSong}"</h4>
                    <div class="row">`;
        
        recommendations.forEach(track => {
            html += `
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${track.name}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${track.artist}</h6>
                            <p class="card-text">
                                <strong>Album:</strong> ${track.album}<br>
                                <strong>Mood:</strong> ${track.mood}<br>
                                <strong>Activity:</strong> ${track.activity}<br>
                                <strong>Time of Day:</strong> ${track.time_of_day}
                            </p>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        $('#local-song-recommendations').html(html);
    }

    // Add event listener for local song search
    $(document).ready(function() {
        $('#local-song-search-btn').on('click', localSongSearch);
        
        // Allow pressing Enter to search
        $('#local-song-search-input').on('keypress', function(e) {
            if (e.which === 13) {  // Enter key
                localSongSearch();
            }
        });
    });
});
