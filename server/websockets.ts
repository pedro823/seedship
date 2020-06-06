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
            if (!seedship) {
                seedship = nodepty.spawn('python3', ['seedship'], {
                    name: 'xterm-color',
                    cwd: gameRoot,
                    rows,
                    cols,
                })
            } else {
                // ctrl+c character, so that the prompt reappears
                seedship.write('\x03')
            }
            seedship.on('data', (data: string) => {
                hostSockets.forEach(hostSocket => {
                    hostSocket.emit('seedship-data', data)
                })
                socket.emit('write', data)
            })
        })

        socket.on('command', (data: string) => {
            if (seedship) {
                seedship.write(data)
            }
        })
        
        socket.on('disconnect', () => {
            hostSockets.delete(socket)
        })
    })
}