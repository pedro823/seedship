(function() {
    Terminal.applyAddon(fullscreen);
    Terminal.applyAddon(attach);
    Terminal.applyAddon(search);

    const term = new Terminal();
    const container = document.getElementById('terminal');
    term.open(container);
    const socket = io();

    term.on('data', (data) => {
        socket.emit('command', data);
    })

    socket.on('write', (data) => {
        term.write(data);
    })
})()
