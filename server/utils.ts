import os from 'os'

// flatMap implementation for finding IPs
export const flatMap = <T, U>(array: T[], mapFunc: (x: T) => U[]) : U[] =>
    array.reduce((cumulus: U[], next: T) => [...mapFunc(next), ...cumulus], <U[]> []);

export const getNetworkIPs = () => {
    // Figures out what IP the host is
    const interfaces = os.networkInterfaces()

    const networkInterfaces = flatMap(Object.values(interfaces), interfaceList =>
        interfaceList.filter(iface => !iface.internal && iface.family === 'IPv4')
                     .map(iface => iface.address)
    )
    return networkInterfaces.length > 0 ? networkInterfaces : ['localhost']
}