document.addEventListener('DOMContentLoaded', function() {
    // Handle navigation clicks
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetClass = this.getAttribute('href').substring(1); 
            const targetSection = document.querySelector('.' + targetClass); 
            if (targetSection) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight; 
                const offsetPosition = targetSection.getBoundingClientRect().top + window.scrollY - navbarHeight; 
                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // Explore button functionality
    const exploreButton = document.querySelector('.showcase .button-section .explore-button');
    if (exploreButton) {
        exploreButton.addEventListener('click', function(e) {
            e.preventDefault();
            const searchSection = document.querySelector('.search');
            searchSection.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Adjust audio volume
    const audios = document.querySelectorAll('audio');
    audios.forEach(function(audio) {
        audio.volume = 0.2;
    });

    // Spotify authentication and playlist creation
    const createPlaylistButton = document.getElementById('create-playlist-button');
    createPlaylistButton.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('Create Playlist button clicked');
        authenticateSpotify();
    });

    // Spotify authentication
    function authenticateSpotify() {
        console.log('Authenticating with Spotify');
        const client_id = 'YOUR_SPOTIFY_CLIENT_ID'; // Replace with your Spotify Client ID
        const redirect_uri = window.location.origin + '/result.html'; // Redirect to result page after auth
        const scope = 'playlist-modify-public';

        const authEndpoint = 'https://accounts.spotify.com/authorize';
        const authUrl = `${authEndpoint}?client_id=${client_id}&redirect_uri=${redirect_uri}&scope=${scope}&response_type=token&show_dialog=true`;

        window.location = authUrl;
    }

    // Check if there's an access token in the URL
    if (window.location.pathname === '/result.html' && window.location.hash) {
        const hash = window.location.hash.substring(1);
        const params = new URLSearchParams(hash);
        const accessToken = params.get('access_token');
        if (accessToken) {
            console.log('Access token obtained:', accessToken);
            createPlaylist(accessToken);
        } else {
            console.error('Access token not found in URL');
        }
    }

    // Create playlist in Spotify
    async function createPlaylist(accessToken) {
        try {
            const userId = await fetch('https://api.spotify.com/v1/me', {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            }).then(res => res.json()).then(data => data.id);

            console.log('User ID obtained:', userId);

            const playlistName = 'New Playlist';
            const playlist = await fetch(`https://api.spotify.com/v1/users/${userId}/playlists`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: playlistName,
                    public: true
                })
            }).then(res => res.json());

            console.log('Playlist created:', playlist);

            // Set the source of the iframe to the new playlist URL
            const spotifyEmbed = document.getElementById('spotify-embed');
            if (spotifyEmbed) {
                spotifyEmbed.src = `https://open.spotify.com/embed/playlist/${playlist.id}`;
                console.log('Playlist iframe updated');
            } else {
                console.error('Spotify embed iframe not found');
                alert(`Playlist created! You can view it here: ${playlist.external_urls.spotify}`);
            }
        } catch (error) {
            console.error('Error creating playlist:', error);
        }
    }
});
