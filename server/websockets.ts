import io from 'socket.io'
import * as nodepty from 'node-pty'

export const setupWebSockets = (ioServer: io.Server, gameRoot: string) => {
    // Socket connection handling

    const hostSockets = new Set<io.Socket>()

    let seedship: nodepty.IPty | null = null

    ioServer.on('connection', (socket: io.Socket) => {
        socket.on('is-host', () => {
            hostSockets.add(socket)
        })

        socket.on('is-client', ({rows, cols}) => {
            seedship = nodepty.spawn('/usr/bin/python3', ['seedship'], {
                name: 'xterm-color',
                cwd: gameRoot,
                rows,
                cols,
            })
            seedship.on('data', (data) => {
                hostSockets.forEach(hostSocket => {
                    hostSocket.emit('seedship-data', data)
                })
                socket.emit('write', data)
            })
            socket.on('command', (data) => {
                if (seedship) {
                    seedship.write(data)
                }
            })
        })
        
        socket.on('disconnect', () => {
            if (seedship) {
                seedship.kill()
            }
            hostSockets.delete(socket)
        })
    })
}