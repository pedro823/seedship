(function() {
    Terminal.applyAddon(fullscreen);
    Terminal.applyAddon(fit);
    Terminal.applyAddon(search);

    const term = new Terminal();
    const container = document.getElementById('terminal');
    term.open(container);

    term.toggleFullScreen(true);
    term.fit();
    
    const socket = io();
    socket.emit('is-host');

    socket.on('seedship-data', (data) => {
        term.write(data);
    });
})()
