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
    socket.emit('is-client', {cols: term.cols, rows: term.rows});

    term.on('data', (data) => {
        socket.emit('command', data);
    })

    socket.on('write', (data) => {
        term.write(data);
    })
})()
